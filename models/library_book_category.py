from odoo import api, fields, models


class LibraryBookCategory(models.Model):
    _name = "library.book.category"
    _description = "Thể loại sách"
    _order = "name"

    code = fields.Char(
        string="Mã thể loại", required=False, copy=False,
        default=lambda self: self.env["ir.sequence"].next_by_code("library.book.category"),
    )
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

    _sql_constraints = [
        ("code_unique", "unique(code)", "Mã thể loại phải là duy nhất."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if not vals.get("code"):
                vals["code"] = sequence.next_by_code("library.book.category")
        return super().create(vals_list)
