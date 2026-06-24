from odoo import api, fields, models


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Sách"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    code = fields.Char(string="Mã Sách", required=True, copy=False, tracking=True)
    name = fields.Char(string="Tiêu đề", required=True, tracking=True)
    author = fields.Char(string="Tác giả", tracking=True)
    category = fields.Char(string="Thể loại")
    publisher = fields.Char(string="Nhà xuất bản")
    publication_year = fields.Integer(string="Năm xuất bản")
    isbn = fields.Char(string="ISBN")
    shelf_location = fields.Char(string="Vị trí kệ")
    cover_image = fields.Image(string="Bìa")
    quantity_total = fields.Integer(string="Tổng số bản", default=1)
    borrowed_count = fields.Integer(
        string="Số bản đang mượn",
        compute="_compute_borrow_stats",
        store=True,
    )
    available_count = fields.Integer(
        string="Số bản còn lại",
        compute="_compute_borrow_stats",
        store=True,
    )
    total_borrow_count = fields.Integer(
        string="Tổng số lượt mượn",
        compute="_compute_borrow_stats",
        store=True,
    )
    loan_line_ids = fields.One2many("library.loan.line", "book_id", string="Chi tiết mượn")

    _sql_constraints = [
        ("code_unique", "unique(code)", "Mã sách phải là duy nhất."),
        ("isbn_unique", "unique(isbn)", "ISBN phải là duy nhất."),
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
