from datetime import timedelta

from odoo import fields, http
from odoo.http import request


class LibraryReaderController(http.Controller):

    @http.route("/library/my-books", type="json", auth="user")
    def my_books(self):
        books = request.env["library.book"].search_read(
            [],
            ["code", "name", "author", "category", "qty_available"],
        )
        return books

    @http.route("/library/my-loans", type="json", auth="user")
    def my_loans(self):
        reader = request.env["library.reader"].search([("user_id", "=", request.env.uid)], limit=1)
        if not reader:
            return []
        loans = request.env["library.loan"].search_read(
            [("reader_id", "=", reader.id)],
            ["name", "borrow_date", "due_date", "return_date", "state", "borrow_fee", "fine_amount", "total_amount"],
            order="borrow_date desc",
        )
        return loans

    @http.route("/library/create-loan", type="json", auth="user", methods=["POST"])
    def create_loan(self, **kwargs):
        reader = request.env["library.reader"].search([("user_id", "=", request.env.uid)], limit=1)
        if not reader:
            return {"error": "Bạn chưa được đăng ký là bạn đọc."}
        book_ids = kwargs.get("book_ids", [])
        if not book_ids:
            return {"error": "Vui lòng chọn ít nhất một quyển sách."}
        available = request.env["library.book"].browse(book_ids).filtered(lambda b: b.qty_available > 0)
        if not available:
            return {"error": "Không có sách nào còn để mượn."}
        loan = request.env["library.loan"].create({
            "reader_id": reader.id,
            "borrow_date": fields.Date.today(),
            "due_date": fields.Date.today() + timedelta(days=14),
            "line_ids": [(0, 0, {"book_id": b.id}) for b in available],
        })
        return {"loan_id": loan.id, "name": loan.name}
