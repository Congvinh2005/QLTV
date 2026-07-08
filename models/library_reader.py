from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LibraryReader(models.Model):
    _name = "library.reader"
    _description = "Bạn đọc"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    code = fields.Char(
        string="Mã người đọc", required=False, copy=False, tracking=True,
        default=lambda self: self.env["ir.sequence"].next_by_code("library.reader"),
    )
    name = fields.Char(string="Họ tên", required=True, tracking=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Điện thoại")
    user_id = fields.Many2one("res.users", string="Tài khoản đăng nhập", readonly=True, copy=False)
    username = fields.Char(string="Tên tài khoản", copy=False)
    password = fields.Char(string="Mật khẩu")
    address = fields.Text(string="Địa chỉ")
    registration_date = fields.Date(
        string="Ngày đăng ký",
        default=fields.Date.context_today,
    )
    loan_ids = fields.One2many("library.loan", "reader_id", string="Phiếu mượn")
    partner_id = fields.Many2one("res.partner", string="Khách hàng", readonly=True, copy=False)
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

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if not vals.get("code"):
                vals["code"] = sequence.next_by_code("library.reader")
        readers = super().create(vals_list)
        for reader in readers:
            if reader.password:
                reader._create_user()
        return readers

    def write(self, vals):
        res = super().write(vals)
        if "password" in vals:
            for reader in self:
                if reader.password:
                    if reader.user_id:
                        reader.user_id.sudo().write({"password": reader.password})
                    else:
                        reader._create_user()
        return res

    def _create_user(self):
        self.ensure_one()
        if self.user_id:
            return self.user_id
        if not self.username:
            raise ValidationError(_("Vui lòng nhập tên tài khoản."))
        group_reader = self.env.ref("QLTV.group_library_reader")
        user = self.env["res.users"].sudo().create({
            "name": self.name,
            "login": self.username,
            "password": self.password,
            "email": self.email or "",
            "groups_id": [(4, group_reader.id)],
        })
        self.user_id = user
        return user

    def action_create_user(self):
        self._create_user()
