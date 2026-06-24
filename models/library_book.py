from odoo import api, fields, models


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    code = fields.Char(string="Book Code", required=True, copy=False, tracking=True)
    name = fields.Char(string="Title", required=True, tracking=True)
    author = fields.Char(string="Author", tracking=True)
    category = fields.Char(string="Category")
    publisher = fields.Char(string="Publisher")
    publication_year = fields.Integer(string="Publication Year")
    isbn = fields.Char(string="ISBN")
    shelf_location = fields.Char(string="Shelf Location")
    cover_image = fields.Image(string="Cover")
    quantity_total = fields.Integer(string="Total Copies", default=1)
    borrowed_count = fields.Integer(
        string="Borrowed Copies",
        compute="_compute_borrow_stats",
        store=True,
    )
    available_count = fields.Integer(
        string="Available Copies",
        compute="_compute_borrow_stats",
        store=True,
    )
    total_borrow_count = fields.Integer(
        string="Total Borrows",
        compute="_compute_borrow_stats",
        store=True,
    )
    loan_line_ids = fields.One2many("library.loan.line", "book_id", string="Loan Lines")

    _sql_constraints = [
        ("code_unique", "unique(code)", "The book code must be unique."),
        ("isbn_unique", "unique(isbn)", "The ISBN must be unique."),
    ]

    @api.depends("quantity_total", "loan_line_ids.state")
    def _compute_borrow_stats(self):
        for book in self:
            active_lines = book.loan_line_ids.filtered(
                lambda line: line.state in ("approved", "borrowed", "overdue")
            )
            book.borrowed_count = len(active_lines)
            book.available_count = max(book.quantity_total - book.borrowed_count, 0)
            book.total_borrow_count = len(book.loan_line_ids)
