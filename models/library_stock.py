from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    loan_id = fields.Many2one("library.loan", string="Phiếu mượn", ondelete="set null")
