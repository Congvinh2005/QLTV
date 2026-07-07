from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
    total_copies = fields.Integer(string="Số bản", default=1)
    copy_ids = fields.One2many("library.book.copy", "book_id", string="Các bản sao")
    available_copy_ids = fields.One2many(
        "library.book.copy", "book_id", string="Bản có sẵn",
        domain=[("state", "=", "available")],
    )
    borrowed_count = fields.Integer(
        string="Số bản đang mượn",
        compute="_compute_borrowed_count",
        store=True,
    )
    loan_line_ids = fields.One2many("library.loan.line", "book_id", string="Chi tiết mượn")
    product_id = fields.Many2one("product.product", string="Sản phẩm", readonly=True, copy=False)
    qty_available = fields.Integer(
        string="Tổng số bản",
        compute="_compute_total_quantity",
        search="_search_total_quantity",
        readonly=True,
    )
    available_quantity = fields.Integer(
        string="Có sẵn",
        compute="_compute_available_quantity",
        search="_search_available_quantity",
        readonly=True,
    )
    product_categ_id = fields.Many2one("product.category", string="Danh mục sản phẩm")
    price = fields.Float(string="Giá bìa")

    _sql_constraints = [
        ("code_unique", "unique(code)", "Mã sách phải là duy nhất."),
        ("isbn_unique", "unique(isbn)", "ISBN phải là duy nhất."),
    ]

    @api.depends("product_id")
    def _compute_total_quantity(self):
        for book in self:
            book.qty_available = book.product_id.qty_available if book.product_id else 0

    def _search_total_quantity(self, operator, value):
        products = self.env["product.product"].search([("qty_available", operator, value)])
        return [("product_id", "in", products.ids)] if products else [("product_id", "=", False)]

    @api.depends("qty_available", "borrowed_count")
    def _compute_available_quantity(self):
        for book in self:
            book.available_quantity = (book.qty_available or 0) - (book.borrowed_count or 0)

    def _search_available_quantity(self, operator, value):
        books = self.search([])
        result = []
        sanitized = int(value)
        for book in books:
            book._compute_available_quantity()
            if operator == "=" and book.available_quantity == sanitized:
                result.append(book.id)
            elif operator == ">" and book.available_quantity > sanitized:
                result.append(book.id)
            elif operator == ">=" and book.available_quantity >= sanitized:
                result.append(book.id)
            elif operator == "<" and book.available_quantity < sanitized:
                result.append(book.id)
            elif operator == "<=" and book.available_quantity <= sanitized:
                result.append(book.id)
            elif operator == "!=" and book.available_quantity != sanitized:
                result.append(book.id)
        return [("id", "in", result)] if result else [("id", "=", False)]

    @api.depends("copy_ids.state")
    def _compute_borrowed_count(self):
        for book in self:
            book.borrowed_count = len(book.copy_ids.filtered(lambda c: c.state == "borrowed"))

    @api.model
    def _get_book_product_category(self):
        categ = self.env["product.category"].search([("name", "=", "Sách")], limit=1)
        if not categ:
            categ = self.env["product.category"].create({
                "name": "Sách",
                "parent_id": self.env.ref("product.product_category_all").id,
            })
        return categ

    def _generate_copies(self):
        self.ensure_one()
        self._sync_copies_to_target(self.total_copies)

    def action_sync_copies_from_stock(self):
        self.ensure_one()
        if not self.product_id:
            raise ValidationError(_("Sách chưa có sản phẩm tồn kho liên kết."))
        stock_qty = int(self.product_id.qty_available)
        self._sync_copies_to_target(stock_qty)
        return True

    def _sync_copies_to_target(self, target):
        self.ensure_one()
        existing = self.env["library.book.copy"].search_count([("book_id", "=", self.id)])
        if existing < target:
            for i in range(existing + 1, target + 1):
                self.env["library.book.copy"].create({
                    "book_id": self.id,
                    "code": "%s-%02d" % (self.code, i),
                    "state": "available",
                })
        elif existing > target:
            excess = self.env["library.book.copy"].search([
                ("book_id", "=", self.id),
                ("state", "=", "available"),
            ], order="code desc")
            to_delete = excess[:existing - target]
            to_delete.unlink()

    @api.model_create_multi
    def create(self, vals_list):
        books = super().create(vals_list)
        for book in books:
            categ = book.product_categ_id or self._get_book_product_category()
            product = self.env["product.product"].create({
                "name": book.name,
                "default_code": book.code,
                "barcode": book.isbn or "",
                "type": "product",
                "categ_id": categ.id,
                "list_price": book.price or 0,
                "description": book.author or "",
            })
            book.product_id = product
            if not book.product_categ_id:
                book.product_categ_id = categ
            book._generate_copies()
        return books

    def write(self, vals):
        res = super().write(vals)
        if "total_copies" in vals:
            for book in self:
                book._generate_copies()
        if "name" in vals or "isbn" in vals or "price" in vals:
            for book in self:
                if book.product_id:
                    product_vals = {}
                    if "name" in vals:
                        product_vals["name"] = book.name
                    if "isbn" in vals:
                        product_vals["barcode"] = book.isbn or ""
                    if "price" in vals:
                        product_vals["list_price"] = book.price or 0
                    if product_vals:
                        book.product_id.write(product_vals)
        return res

    def unlink(self):
        for book in self:
            if book.product_id:
                raise ValidationError(
                    _("Không thể xoá sách '%s' vì đã có sản phẩm tồn kho liên kết. Hãy xoá sản phẩm trước.") % book.name
                )
        return super().unlink()
