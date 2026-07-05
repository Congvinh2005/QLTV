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
    borrowed_count = fields.Integer(
        string="Số bản đang mượn",
        compute="_compute_borrowed_count",
        store=True,
    )
    loan_line_ids = fields.One2many("library.loan.line", "book_id", string="Chi tiết mượn")
    product_id = fields.Many2one("product.product", string="Sản phẩm", readonly=True, copy=False)
    qty_available = fields.Float(
        string="Tồn kho thực tế",
        compute="_compute_qty_available",
        search="_search_qty_available",
        readonly=True,
    )
    product_categ_id = fields.Many2one("product.category", string="Danh mục sản phẩm")
    price = fields.Float(string="Giá bìa")

    _sql_constraints = [
        ("code_unique", "unique(code)", "Mã sách phải là duy nhất."),
        ("isbn_unique", "unique(isbn)", "ISBN phải là duy nhất."),
    ]

    @api.depends("product_id")
    def _compute_qty_available(self):
        StockLocation = self.env.ref("stock.stock_location_stock")
        for book in self:
            if not book.product_id:
                book.qty_available = 0
                continue
            quant = self.env["stock.quant"].search([
                ("product_id", "=", book.product_id.id),
                ("location_id", "=", StockLocation.id),
            ], limit=1)
            book.qty_available = quant.quantity if quant else 0

    def _search_qty_available(self, operator, value):
        StockLocation = self.env.ref("stock.stock_location_stock")
        quants = self.env["stock.quant"].search([
            ("location_id", "=", StockLocation.id),
        ])
        matching_products = set()
        for quant in quants:
            qty = quant.quantity
            if operator == "=" and qty == value:
                matching_products.add(quant.product_id.id)
            elif operator == "!=" and qty != value:
                matching_products.add(quant.product_id.id)
            elif operator == ">" and qty > value:
                matching_products.add(quant.product_id.id)
            elif operator == ">=" and qty >= value:
                matching_products.add(quant.product_id.id)
            elif operator == "<" and qty < value:
                matching_products.add(quant.product_id.id)
            elif operator == "<=" and qty <= value:
                matching_products.add(quant.product_id.id)
            elif operator == "in" and qty in value:
                matching_products.add(quant.product_id.id)
            elif operator == "not in" and qty not in value:
                matching_products.add(quant.product_id.id)
        if not matching_products:
            return [("id", "=", False)]
        return [("product_id", "in", list(matching_products))]

    @api.depends("loan_line_ids.state")
    def _compute_borrowed_count(self):
        for book in self:
            active_lines = book.loan_line_ids.filtered(
                lambda line: line.state in ("approved", "borrowed", "overdue")
            )
            book.borrowed_count = len(active_lines)

    @api.model
    def _get_book_product_category(self):
        categ = self.env.ref("QLTV.product_category_books", raise_if_not_found=False)
        if not categ:
            categ = self.env["product.category"].create({
                "name": "Sách",
                "parent_id": self.env.ref("product.product_category_all").id,
            })
            self.env["ir.model.data"].create({
                "module": "QLTV",
                "name": "product_category_books",
                "model": "product.category",
                "res_id": categ.id,
            })
        return categ

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
        return books

    def write(self, vals):
        res = super().write(vals)
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
