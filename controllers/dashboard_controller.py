from odoo import http
from odoo.http import request


class LibraryDashboardController(http.Controller):
    @http.route("/my", type="http", auth="user", website=True)
    def my_home(self):
        if request.env.user.has_group("QLTV.group_library_user"):
            return request.redirect("/web")
        return request.redirect("/my/home")

    @http.route("/library/dashboard/data", type="json", auth="user")
    def dashboard_data(self):
        Book = request.env["library.book"].sudo()
        Reader = request.env["library.reader"].sudo()
        Loan = request.env["library.loan"].sudo()
        return {
            "total_books": Book.search_count([]),
            "total_copies": sum(Book.search([]).mapped("quantity_total")),
            "total_readers": Reader.search_count([]),
            "total_loans": Loan.search_count([]),
            "borrowed": Loan.search_count([("state", "=", "borrowed")]),
            "overdue": Loan.search_count([("state", "=", "overdue")]),
            "returned": Loan.search_count([("state", "=", "returned")]),
        }


