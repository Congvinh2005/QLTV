from odoo import api, fields, models


class LibraryBookCategory(models.Model):
    _name = "library.book.category"
    _description = "Thể loại sách"
    _order = "name"

    name = fields.Char(string="Tên thể loại", required=True, tracking=True)
    description = fields.Text(string="Mô tả")
    book_count = fields.Integer(
        string="Số sách", compute="_compute_book_count", store=True
    )

    @api.depends("book_ids")
    def _compute_book_count(self):
        for cat in self:
            cat.book_count = len(cat.book_ids)

    book_ids = fields.One2many("library.book", "category_id", string="Sách")
