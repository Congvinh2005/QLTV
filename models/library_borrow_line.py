from odoo import api, fields, models


class LibraryLoanLine(models.Model):
    _name = "library.loan.line"
    _description = "Chi tiết phiếu mượn"

    loan_id = fields.Many2one("library.loan", string="Phiếu mượn", required=True, ondelete="cascade")
    book_id = fields.Many2one("library.book", string="Sách", required=True)
    quantity = fields.Integer(string="Số lượng", default=1, required=True)
    qty_available = fields.Integer(
        string="Có sẵn",
        related="book_id.qty_available",
        readonly=True,
    )
    state = fields.Selection(related="loan_id.state", store=True, readonly=True)

    @api.onchange("book_id")
    def _onchange_book_id(self):
        if self.book_id and not self.quantity:
            self.quantity = 1
