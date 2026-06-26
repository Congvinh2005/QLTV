from datetime import timedelta

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
    borrow_date = fields.Date(
        string="Ngày mượn",
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    borrow_days = fields.Integer(string="Số ngày mượn", compute="_compute_borrow_days", store=True)
    due_date = fields.Date(
        string="Ngày hết hạn", compute="_compute_due_date", store=True,
        tracking=True,
    )
    return_date = fields.Date(string="Ngày trả", tracking=True)
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
                loan.due_date = loan.borrow_date + timedelta(days=loan.borrow_days)
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
        today = fields.Date.today()
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

    def action_borrow(self):
        for loan in self:
            if not loan.line_ids:
                raise UserError(_("Vui lòng thêm ít nhất một quyển sách."))
            if not loan.borrow_fee or loan.borrow_fee <= 0:
                raise UserError(_("Vui lòng nhập phí mượn."))
            unavailable = loan.line_ids.filtered(lambda line: line.book_id.available_count <= 0)
            if unavailable:
                raise UserError(_("Một số sách đã hết."))
            loan.state = "borrowed"

    def _get_overdue_fee_per_day(self):
        return int(self.env["ir.config_parameter"].sudo().get_param("qltv.overdue_fee_per_day", "1000"))

    def action_return(self):
        today = fields.Date.context_today(self)
        for loan in self:
            overdue_days = 0
            if loan.due_date and today > loan.due_date:
                overdue_days = (today - loan.due_date).days
            fine = 0
            if overdue_days > 0:
                fine = overdue_days * self._get_overdue_fee_per_day()
            loan.write({
                "state": "returned",
                "return_date": today,
                "fine_amount": fine,
            })

    def action_check_overdue(self):
        today = fields.Date.context_today(self)
        loans = self.search([("state", "=", "borrowed"), ("due_date", "<", today)])
        for loan in loans:
            overdue_days = (today - loan.due_date).days
            fine = overdue_days * self._get_overdue_fee_per_day()
            loan.write({
                "state": "overdue",
                "fine_amount": fine,
            })
