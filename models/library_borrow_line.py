from odoo import api, fields, models


class LibraryLoanLine(models.Model):
    _name = "library.loan.line"
    _description = "Chi tiết phiếu mượn"

    loan_id = fields.Many2one("library.loan", string="Phiếu mượn", required=True, ondelete="cascade")
    book_id = fields.Many2one("library.book", string="Sách", required=True)
    quantity = fields.Integer(string="Số lượng", default=1, required=True)
    qty_available = fields.Integer(
        string="Tổng số bản",
        related="book_id.qty_available",
        readonly=True,
    )
    available_quantity = fields.Integer(
        string="Có sẵn",
        related="book_id.available_quantity",
        readonly=True,
    )
    state = fields.Selection(related="loan_id.state", store=True, readonly=True)

    @api.onchange("book_id")
    def _onchange_book_id(self):
        if self.book_id and not self.quantity:
            self.quantity = 1

    def name_get(self):
        result = []
        for line in self:
            name = line.loan_id.name or ""
            if line.book_id:
                name += " - %s" % line.book_id.name if name else line.book_id.name
            result.append((line.id, name))
        return result
