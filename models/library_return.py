from odoo import api, fields, models


class LibraryReturn(models.Model):
    _name = "library.return"
    _description = "Phiếu trả"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "return_date desc, id desc"

    name = fields.Char(string="Mã phiếu trả", required=True, default="/", copy=False)
    loan_id = fields.Many2one("library.loan", string="Phiếu mượn", required=True)
    return_date = fields.Date(string="Ngày trả", default=fields.Date.context_today, required=True)
    fine_amount = fields.Monetary(string="Tiền phạt")
    currency_id = fields.Many2one(
        "res.currency",
        string="Tiền tệ",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    notes = fields.Text(string="Ghi chú")

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = sequence.next_by_code("library.return") or "/"
        return super().create(vals_list)
