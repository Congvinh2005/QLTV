from odoo import api, fields, models


class LibraryReader(models.Model):
    _name = "library.reader"
    _description = "Library Reader"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    code = fields.Char(string="Reader Code", required=True, copy=False, tracking=True)
    name = fields.Char(string="Full Name", required=True, tracking=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    registration_date = fields.Date(
        string="Registration Date",
        default=fields.Date.context_today,
    )
    loan_ids = fields.One2many("library.loan", "reader_id", string="Loans")
    total_loan_count = fields.Integer(compute="_compute_loan_stats", string="Total Loans")
    current_loan_count = fields.Integer(compute="_compute_loan_stats", string="Borrowing")
    overdue_loan_count = fields.Integer(compute="_compute_loan_stats", string="Overdue")

    _sql_constraints = [
        ("code_unique", "unique(code)", "The reader code must be unique."),
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
