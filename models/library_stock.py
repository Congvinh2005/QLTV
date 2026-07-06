from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    loan_id = fields.Many2one("library.loan", string="Phiếu mượn", ondelete="set null")


class AccountMove(models.Model):
    _inherit = "account.move"

    loan_id = fields.Many2one("library.loan", string="Phiếu mượn", ondelete="set null")


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def write(self, vals):
        res = super().write(vals)
        if "quantity" in vals:
            self._sync_book_copies()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        quants = super().create(vals_list)
        quants._sync_book_copies()
        return quants

    def _sync_book_copies(self):
        for quant in self:
            book = self.env["library.book"].search(
                [("product_id", "=", quant.product_id.id)], limit=1
            )
            if book:
                book.action_sync_copies_from_stock()
