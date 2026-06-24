from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Library Loan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "borrow_date desc, id desc"

    name = fields.Char(string="Loan Reference", required=True, default="/", copy=False)
    reader_id = fields.Many2one("library.reader", string="Reader", required=True, tracking=True)
    borrow_date = fields.Date(
        string="Borrow Date",
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    due_date = fields.Date(string="Due Date", required=True, tracking=True)
    return_date = fields.Date(string="Return Date", tracking=True)
    fine_amount = fields.Monetary(string="Fine")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved", "Approved"),
            ("borrowed", "Borrowed"),
            ("returned", "Returned"),
            ("overdue", "Overdue"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    line_ids = fields.One2many("library.loan.line", "loan_id", string="Books", copy=True)

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = sequence.next_by_code("library.loan") or "/"
        return super().create(vals_list)

    def action_approve(self):
        self.write({"state": "approved"})

    def action_borrow(self):
        for loan in self:
            if not loan.line_ids:
                raise UserError(_("Please add at least one book."))
            unavailable = loan.line_ids.filtered(lambda line: line.book_id.available_count <= 0)
            if unavailable:
                raise UserError(_("Some selected books are out of stock."))
            loan.state = "borrowed"

    def action_return(self):
        today = fields.Date.context_today(self)
        for loan in self:
            loan.write({"state": "returned", "return_date": today})

    def action_check_overdue(self):
        today = fields.Date.context_today(self)
        loans = self.search([("state", "=", "borrowed"), ("due_date", "<", today)])
        loans.write({"state": "overdue"})
