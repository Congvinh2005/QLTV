from odoo import fields, models


class LibraryLoanLine(models.Model):
    _name = "library.loan.line"
    _description = "Library Loan Line"

    loan_id = fields.Many2one("library.loan", string="Loan", required=True, ondelete="cascade")
    book_id = fields.Many2one("library.book", string="Book", required=True)
    state = fields.Selection(related="loan_id.state", store=True, readonly=True)
