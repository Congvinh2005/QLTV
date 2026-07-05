from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Phiếu mượn"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "borrow_date desc, id desc"

    name = fields.Char(string="Mã phiếu mượn", required=True, default="/", copy=False)
    reader_id = fields.Many2one(
        "library.reader", string="Bạn đọc", required=True, tracking=True,
        default=lambda self: self._default_reader_id(),
    )
    borrow_date = fields.Datetime(
        string="Ngày mượn",
        default=fields.Datetime.now,
        required=True,
        tracking=True,
    )
    borrow_days = fields.Integer(string="Số ngày mượn", compute="_compute_borrow_days", store=True)
    due_date = fields.Datetime(
        string="Ngày hết hạn", compute="_compute_due_date", store=True,
        tracking=True,
    )
    return_date = fields.Datetime(string="Ngày trả", tracking=True)
    borrow_fee = fields.Monetary(
        string="Phí mượn",
        currency_field="currency_id",
        tracking=True,
    )
    fine_amount = fields.Monetary(
        string="Phí phạt",
        currency_field="currency_id",
        tracking=True,
    )
    total_amount = fields.Monetary(
        string="Tổng tiền",
        currency_field="currency_id",
        compute="_compute_total_amount",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: (self.env.ref("base.VND", raise_if_not_found=False) or self.env.company.currency_id).id,
    )
    state = fields.Selection(
        [
            ("draft", "Bản nháp"),
            ("approved", "Đã duyệt"),
            ("borrowed", "Đang mượn"),
            ("returned", "Đã trả"),
            ("overdue", "Quá hạn"),
        ],
        string="Trạng thái",
        default="draft",
        required=True,
        tracking=True,
    )
    line_ids = fields.One2many("library.loan.line", "loan_id", string="Sách", copy=True)
    picking_ids = fields.One2many("stock.picking", "loan_id", string="Phiếu kho")
    invoice_ids = fields.One2many("account.move", "loan_id", string="Hoá đơn")

    @api.depends("borrow_date", "return_date")
    def _compute_borrow_days(self):
        for loan in self:
            if loan.borrow_date and loan.return_date and loan.return_date > loan.borrow_date:
                loan.borrow_days = (loan.return_date - loan.borrow_date).days
            else:
                loan.borrow_days = 0

    @api.depends("borrow_date", "borrow_days")
    def _compute_due_date(self):
        for loan in self:
            if loan.borrow_date and loan.borrow_days:
                bd = loan.borrow_date
                if isinstance(bd, datetime):
                    loan.due_date = bd.replace(hour=23, minute=59, second=59) + timedelta(days=loan.borrow_days - 1)
                else:
                    loan.due_date = bd + timedelta(days=loan.borrow_days)
            else:
                loan.due_date = False

    @api.depends("borrow_fee", "fine_amount")
    def _compute_total_amount(self):
        for loan in self:
            loan.total_amount = (loan.borrow_fee or 0) + (loan.fine_amount or 0)

    @api.model
    def _default_reader_id(self):
        reader = self.env["library.reader"].search([("user_id", "=", self.env.uid)], limit=1)
        if reader:
            return reader.id
        if self.env.user.has_group("QLTV.group_library_reader"):
            user = self.env.user
            reader = self.env["library.reader"].create({
                "code": user.login.upper(),
                "name": user.name,
                "email": user.email or "",
                "user_id": user.id,
            })
            return reader.id
        return False

    @api.model_create_multi
    def create(self, vals_list):
        today = fields.Datetime.now()
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = sequence.next_by_code("library.loan") or "/"
            if not vals.get("borrow_date"):
                vals["borrow_date"] = today
            if not vals.get("reader_id"):
                vals["reader_id"] = self._default_reader_id()
        return super().create(vals_list)

    def action_approve(self):
        self.write({"state": "approved"})

    def _get_borrowed_location(self):
        return self.env.ref("QLTV.stock_location_borrowed")

    def _get_stock_location(self):
        return self.env.ref("stock.stock_location_stock")

    def _create_stock_picking(self, move_type):
        self.ensure_one()
        if not self.line_ids:
            return
        location_src = location_dst = False
        if move_type == "borrow":
            location_src = self._get_stock_location()
            location_dst = self._get_borrowed_location()
        elif move_type == "return":
            location_src = self._get_borrowed_location()
            location_dst = self._get_stock_location()
        else:
            return
        picking = self.env["stock.picking"].create({
            "location_id": location_src.id,
            "location_dest_id": location_dst.id,
            "picking_type_id": self.env.ref("stock.picking_type_internal").id,
            "loan_id": self.id,
        })
        for line in self.line_ids:
            if not line.book_id.product_id:
                continue
            self.env["stock.move"].create({
                "picking_id": picking.id,
                "name": self.name,
                "product_id": line.book_id.product_id.id,
                "product_uom_qty": line.quantity,
                "product_uom": line.book_id.product_id.uom_id.id,
                "location_id": location_src.id,
                "location_dest_id": location_dst.id,
            })
        picking.action_confirm()
        picking.action_assign()
        if picking.state == "assigned":
            for move in picking.move_ids:
                move.quantity_done = move.product_uom_qty
            picking.button_validate()
        return picking

    def action_borrow(self):
        for loan in self:
            if not loan.line_ids:
                raise UserError(_("Vui lòng thêm ít nhất một quyển sách."))
            if not loan.borrow_fee or loan.borrow_fee <= 0:
                raise UserError(_("Vui lòng nhập phí mượn."))
            for line in loan.line_ids:
                if line.book_id.qty_available < line.quantity:
                    raise UserError(_("Sách '%s' chỉ còn %d, không đủ %d.") % (
                        line.book_id.name, line.book_id.qty_available, line.quantity))
            loan.state = "borrowed"
            loan._create_stock_picking("borrow")

    def _get_overdue_fee_per_day(self):
        return int(self.env["ir.config_parameter"].sudo().get_param("qltv.overdue_fee_per_day", "1000"))

    def action_return(self):
        today = fields.Datetime.now()
        for loan in self:
            overdue_days = 0
            if loan.due_date and today > loan.due_date:
                bd = loan.borrow_date.date() if loan.borrow_date else today.date()
                dd = loan.due_date.date() if loan.due_date else today.date()
                overdue_days = (today.date() - dd).days
            fine = 0
            if overdue_days > 0:
                fine = overdue_days * self._get_overdue_fee_per_day()
            loan.write({
                "state": "returned",
                "return_date": today,
                "fine_amount": fine,
            })
            loan._create_stock_picking("return")
            loan._create_invoice()

    def _get_invoice_product(self):
        return self.env.ref("QLTV.product_library_fee", raise_if_not_found=False)

    def _get_sale_journal(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        if not journal:
            journal = self.env["account.journal"].search([("type", "=", "general")], limit=1)
        return journal

    def _create_invoice(self):
        self.ensure_one()
        total = (self.borrow_fee or 0) + (self.fine_amount or 0)
        if total <= 0:
            return
        partner = self.reader_id._get_or_create_partner()
        product = self._get_invoice_product()
        journal = self._get_sale_journal()
        if not product or not journal:
            return
        invoice_lines = []
        if self.borrow_fee:
            invoice_lines.append((0, 0, {
                "product_id": product.id,
                "name": "Phí mượn sách - %s" % self.name,
                "quantity": 1,
                "price_unit": self.borrow_fee,
                "tax_ids": False,
            }))
        if self.fine_amount:
            invoice_lines.append((0, 0, {
                "product_id": product.id,
                "name": "Phí phạt quá hạn - %s" % self.name,
                "quantity": 1,
                "price_unit": self.fine_amount,
                "tax_ids": False,
            }))
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": partner.id,
            "journal_id": journal.id,
            "loan_id": self.id,
            "currency_id": self.currency_id.id,
            "invoice_date": fields.Date.today(),
            "invoice_line_ids": invoice_lines,
        })
        invoice.action_post()
        return invoice

    def action_check_overdue(self):
        today = fields.Datetime.now()
        loans = self.search([("state", "=", "borrowed"), ("due_date", "<", today)])
        for loan in loans:
            bd = loan.borrow_date.date() if loan.borrow_date else today.date()
            dd = loan.due_date.date() if loan.due_date else today.date()
            overdue_days = (today.date() - dd).days
            fine = overdue_days * self._get_overdue_fee_per_day()
            loan.write({
                "state": "overdue",
                "fine_amount": fine,
            })
