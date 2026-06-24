from odoo import api, fields, models


class LibraryReader(models.Model):
    _name = "library.reader"
    _description = "Bạn đọc"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    code = fields.Char(string="Mã người đọc", required=True, copy=False, tracking=True)
    name = fields.Char(string="Họ tên", required=True, tracking=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Điện thoại")
    address = fields.Text(string="Địa chỉ")
    registration_date = fields.Date(
        string="Ngày đăng ký",
        default=fields.Date.context_today,
    )
    loan_ids = fields.One2many("library.loan", "reader_id", string="Phiếu mượn")
    total_loan_count = fields.Integer(compute="_compute_loan_stats", string="Tổng số phiếu mượn")
    current_loan_count = fields.Integer(compute="_compute_loan_stats", string="Đang mượn")
    overdue_loan_count = fields.Integer(compute="_compute_loan_stats", string="Quá hạn")

    _sql_constraints = [
        ("code_unique", "unique(code)", "Mã người đọc phải là duy nhất."),
    ]

    @api.depends("loan_ids.state")
    def _compute_loan_stats(self):
        for reader in self:
            reader.total_loan_count = len(reader.loan_ids)
            reader.current_loan_count = len(
                reader.loan_ids.filtered(lambda loan: loan.state == "borrowed")
            )
            reader.overdue_loan_count = len(
                reader.loan_ids.filtered(lambda loan: loan.state == "overdue")
            )
