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
    user_id = fields.Many2one("res.users", string="Tài khoản đăng nhập")
    address = fields.Text(string="Địa chỉ")
    registration_date = fields.Date(
        string="Ngày đăng ký",
        default=fields.Date.context_today,
    )
    loan_ids = fields.One2many("library.loan", "reader_id", string="Phiếu mượn")
    partner_id = fields.Many2one("res.partner", string="Khách hàng", readonly=True, copy=False)

    def _get_or_create_partner(self):
        self.ensure_one()
        if self.partner_id:
            return self.partner_id
        partner = self.env["res.partner"].create({
            "name": self.name,
            "email": self.email or "",
            "phone": self.phone or "",
            "street": self.address or "",
            "company_type": "person",
        })
        self.partner_id = partner
        return partner
    total_loan_count = fields.Integer(compute="_compute_loan_stats", store=True, string="Tổng số phiếu mượn")
    current_loan_count = fields.Integer(compute="_compute_loan_stats", store=True, string="Đang mượn")
    overdue_loan_count = fields.Integer(compute="_compute_loan_stats", store=True, string="Quá hạn")

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
