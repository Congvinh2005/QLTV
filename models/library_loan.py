from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Phiếu mượn"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "borrow_date desc, id desc"

    name = fields.Char(string="Mã phiếu mượn", required=True, default="/", copy=False)
    reader_id = fields.Many2one("library.reader", string="Bạn đọc", required=True, tracking=True)
    borrow_date = fields.Date(
        string="Ngày mượn",
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    due_date = fields.Date(string="Ngày hết hạn", required=True, tracking=True)
    return_date = fields.Date(string="Ngày trả", tracking=True)
    fine_amount = fields.Monetary(string="Phí phạt")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
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

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = sequence.next_by_code("library.loan") or "/"
        return super().create(vals_list)

    def action_approve(self):
        self.write({"state": "approved"})

    def action_borrow(self):
        for loan in self:
            if not loan.line_ids:
                raise UserError(_("Vui lòng thêm ít nhất một quyển sách."))
            unavailable = loan.line_ids.filtered(lambda line: line.book_id.available_count <= 0)
            if unavailable:
                raise UserError(_("Một số sách đã hết."))
            loan.state = "borrowed"

    def action_return(self):
        today = fields.Date.context_today(self)
        for loan in self:
            loan.write({"state": "returned", "return_date": today})

    def action_check_overdue(self):
        today = fields.Date.context_today(self)
        loans = self.search([("state", "=", "borrowed"), ("due_date", "<", today)])
        loans.write({"state": "overdue"})
