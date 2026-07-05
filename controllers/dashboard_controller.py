from datetime import timedelta

from odoo import fields, http
from odoo.http import request


class LibraryDashboardController(http.Controller):

    @http.route("/library/kanban/stats", type="json", auth="user")
    def kanban_stats(self, model):
        Book = request.env["library.book"].sudo()
        Reader = request.env["library.reader"].sudo()
        Loan = request.env["library.loan"].sudo()
        if model == "library.book":
            return {
                "total": Book.search_count([]),
                "available": sum(Book.search([]).mapped("available_count")),
                "borrowed": sum(Book.search([]).mapped("borrowed_count")),
                "out_of_stock": Book.search_count([("available_count", "=", 0)]),
            }
        if model == "library.reader":
            return {
                "total": Reader.search_count([]),
                "borrowing": Reader.search_count([("current_loan_count", ">", 0)]),
                "overdue": Reader.search_count([("overdue_loan_count", ">", 0)]),
            }
        if model == "library.loan":
            return {
                "total": Loan.search_count([]),
                "borrowed": Loan.search_count([("state", "=", "borrowed")]),
                "returned": Loan.search_count([("state", "=", "returned")]),
                "overdue": Loan.search_count([("state", "=", "overdue")]),
            }
        return {}

    @http.route("/my", type="http", auth="user", website=True)
    def my_home(self):
        if request.env.user.has_group("QLTV.group_library_user"):
            return request.redirect("/web")
        return request.redirect("/my/home")

    @http.route("/library/dashboard/data", type="json", auth="user")
    def dashboard_data(self):
        now = fields.Datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        month_start = today_start.replace(day=1)

        Book = request.env["library.book"].sudo()
        Reader = request.env["library.reader"].sudo()
        Loan = request.env["library.loan"].sudo()

        def revenue_domain(start=None, end=None):
            domain = [("state", "in", ("returned", "overdue"))]
            if start:
                domain.append(("return_date", ">=", start))
            if end:
                domain.append(("return_date", "<", end))
            return domain

        revenue_today = sum(
            Loan.search(revenue_domain(today_start, today_end)).mapped("total_amount")
        ) or 0
        revenue_month = sum(
            Loan.search(revenue_domain(month_start, None)).mapped("total_amount")
        ) or 0
        total_revenue = sum(
            Loan.search(revenue_domain(None, None)).mapped("total_amount")
        ) or 0

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


