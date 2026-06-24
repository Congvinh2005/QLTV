from odoo import fields, models


class LibraryLoanLine(models.Model):
    _name = "library.loan.line"
    _description = "Chi tiết phiếu mượn"

    loan_id = fields.Many2one("library.loan", string="Phiếu mượn", required=True, ondelete="cascade")
    book_id = fields.Many2one("library.book", string="Sách", required=True)
    state = fields.Selection(related="loan_id.state", store=True, readonly=True)
