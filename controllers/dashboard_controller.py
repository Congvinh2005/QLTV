from odoo import fields, http
from odoo.http import request


class LibraryDashboardController(http.Controller):
    @http.route("/my", type="http", auth="user", website=True)
    def my_home(self):
        if request.env.user.has_group("QLTV.group_library_user"):
            return request.redirect("/web")
        return request.redirect("/my/home")

    @http.route("/library/dashboard/data", type="json", auth="user")
    def dashboard_data(self):
        today = fields.Date.today()
        Book = request.env["library.book"].sudo()
        Reader = request.env["library.reader"].sudo()
        Loan = request.env["library.loan"].sudo()

        # Doanh thu
        all_loans = Loan.search([("state", "in", ("returned", "overdue"))])
        total_revenue = sum(all_loans.mapped("total_amount"))
        today_loans = Loan.search([
            ("state", "in", ("returned", "overdue")),
            ("return_date", "=", today),
        ])
        revenue_today = sum(today_loans.mapped("total_amount"))
        month_start = today.replace(day=1)
        month_loans = Loan.search([
            ("state", "in", ("returned", "overdue")),
            ("return_date", ">=", month_start),
        ])
        revenue_month = sum(month_loans.mapped("total_amount"))

        return {
            "total_books": Book.search_count([]),
            "total_copies": sum(Book.search([]).mapped("quantity_total")),
            "available": sum(Book.search([]).mapped("available_count")),
            "total_readers": Reader.search_count([]),
            "total_loans": Loan.search_count([]),
            "borrowed": Loan.search_count([("state", "=", "borrowed")]),
            "overdue": Loan.search_count([("state", "=", "overdue")]),
            "returned": Loan.search_count([("state", "=", "returned")]),
            "total_revenue": total_revenue,
            "revenue_today": revenue_today,
            "revenue_month": revenue_month,
        }


