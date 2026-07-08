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
                "available": sum(Book.search([]).mapped("available_quantity")),
                "borrowed": sum(Book.search([]).mapped("borrowed_count")),
                "out_of_stock": Book.search_count([("available_quantity", "=", 0)]),
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

        def percent_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return int(round((current - previous) * 100.0 / previous))

        def prev_month(date):
            if date.month == 1:
                return date.replace(year=date.year - 1, month=12)
            return date.replace(month=date.month - 1)

        def next_month(date):
            if date.month == 12:
                return date.replace(year=date.year + 1, month=1)
            return date.replace(month=date.month + 1)

        Book = request.env["library.book"].sudo()
        Reader = request.env["library.reader"].sudo()
        Loan = request.env["library.loan"].sudo()
        Invoice = request.env["account.move"].sudo()
        Category = request.env["library.book.category"].sudo()

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

        books = Book.search([])
        total_stock_qty = sum(books.mapped("qty_available")) or 0
        low_stock_count = len(books.filtered(lambda b: b.available_quantity <= 3))

        inv_domain = [("loan_id", "!=", False), ("move_type", "=", "out_invoice")]
        invoices = Invoice.search(inv_domain)
        invoice_total = sum(invoices.mapped("amount_total")) or 0
        invoice_paid = sum(invoices.filtered(lambda i: i.payment_state == "paid").mapped("amount_total")) or 0
        invoice_unpaid = sum(invoices.filtered(lambda i: i.payment_state != "paid").mapped("amount_total")) or 0

        inv_domain_today = inv_domain + [("invoice_date", "=", fields.Date.today())]
        invoice_today = sum(Invoice.search(inv_domain_today).mapped("amount_total")) or 0

        inv_domain_month = inv_domain + [("invoice_date", ">=", fields.Date.today().replace(day=1))]
        invoice_month = sum(Invoice.search(inv_domain_month).mapped("amount_total")) or 0

        category_counts = {}
        for book in books:
            category = book.category_id.name or "Khác"
            category_counts[category] = category_counts.get(category, 0) + 1
        sorted_categories = sorted(
            category_counts.items(), key=lambda item: item[1], reverse=True
        )[:5]
        sample_colors = ["#2F5DA9", "#3F8F47", "#B85A28", "#E2AC34", "#7B4BCB"]
        book_categories = [
            {"name": name, "value": value, "color": sample_colors[idx]}
            for idx, (name, value) in enumerate(sorted_categories)
        ]
        if not book_categories:
            book_categories = [
                {"name": "Văn học", "value": 35, "color": "#2F5DA9"},
                {"name": "Công nghệ", "value": 25, "color": "#3F8F47"},
                {"name": "Kinh tế", "value": 18, "color": "#B85A28"},
                {"name": "Thiếu nhi", "value": 12, "color": "#E2AC34"},
                {"name": "Ngoại ngữ", "value": 5, "color": "#7B4BCB"},
            ]

        top_book_colors = ["#FF6B6B", "#FBBF24", "#FB923C", "#F472B6", "#A78BFA"]
        top_books = []
        max_borrowed = 1
        sorted_books = books.sorted(key=lambda b: b.borrowed_count, reverse=True)[:5]
        for book in sorted_books:
            if book.borrowed_count > max_borrowed:
                max_borrowed = book.borrowed_count
        for idx, book in enumerate(sorted_books):
            top_books.append({
                "rank": idx + 1,
                "name": book.name,
                "borrowed": book.borrowed_count,
                "percent": int((book.borrowed_count or 0) * 100 / max_borrowed) if max_borrowed else 0,
                "color": top_book_colors[idx] if idx < len(top_book_colors) else "#4361EE",
            })
        if not top_books:
            top_books = [
                {"rank": 1, "name": "Đắc nhân tâm", "borrowed": 25, "percent": 100, "color": "#FF6B6B"},
                {"rank": 2, "name": "Nhà giả kim", "borrowed": 18, "percent": 72, "color": "#FBBF24"},
                {"rank": 3, "name": "Cho tôi xin một vé đi tuổi thơ", "borrowed": 15, "percent": 60, "color": "#FB923C"},
                {"rank": 4, "name": "Dế mèn phiêu lưu ký", "borrowed": 12, "percent": 48, "color": "#F472B6"},
                {"rank": 5, "name": "Atomic Habits", "borrowed": 10, "percent": 40, "color": "#A78BFA"},
            ]

        def normalize_date(dt):
            return dt.replace(day=1)

        def next_month(dt):
            if dt.month == 12:
                return dt.replace(year=dt.year + 1, month=1)
            return dt.replace(month=dt.month + 1)

        today = fields.Date.today()
        current_month = normalize_date(today)
        months = [current_month]
        for _ in range(5):
            previous = months[0]
            if previous.month == 1:
                months.insert(0, previous.replace(year=previous.year - 1, month=12))
            else:
                months.insert(0, previous.replace(month=previous.month - 1))

        loan_trend_labels = [m.strftime("%m/%Y") if hasattr(m, 'strftime') else m for m in months]
        loan_trend_borrowed = []
        loan_trend_returned = []
        for month in months:
            month_start = month
            month_end = next_month(month_start)
            borrowed_count = Loan.search_count([
                ("borrow_date", ">=", month_start),
                ("borrow_date", "<", month_end),
            ])
            returned_count = Loan.search_count([
                ("return_date", ">=", month_start),
                ("return_date", "<", month_end),
                ("state", "=", "returned"),
            ])
            loan_trend_borrowed.append(borrowed_count)
            loan_trend_returned.append(returned_count)

        last_loans = []
        for loan in Loan.search([], order="borrow_date desc", limit=5):
            last_loans.append({
                "name": loan.name,
                "reader": loan.reader_id.name or "",
                "borrow_date": loan.borrow_date.strftime("%d/%m/%Y") if loan.borrow_date else "",
                "due_date": loan.due_date.strftime("%d/%m/%Y") if loan.due_date else "",
                "status": dict(loan._fields["state"].selection).get(loan.state, loan.state),
                "state": loan.state,
            })

        last_readers = []
        for reader in Reader.search([], order="registration_date desc", limit=5):
            last_readers.append({
                "code": reader.code,
                "name": reader.name,
                "phone": reader.phone or "",
                "registration_date": fields.Date.to_string(reader.registration_date) if reader.registration_date else "",
            })

        loan_trend = {
            "labels": loan_trend_labels,
            "borrowed": loan_trend_borrowed,
            "returned": loan_trend_returned,
        }

        return {
            "kpis": {
                "total_books": Book.search_count([]),
                "total_copies": sum(books.mapped("qty_available")),
                "available": sum(books.mapped("available_quantity")),
                "total_readers": Reader.search_count([]),
                "total_loans": Loan.search_count([]),
                "borrowed": sum(books.mapped("borrowed_count")),
                "overdue": Loan.search_count([("state", "=", "overdue")]),
                "returned": Loan.search_count([("state", "=", "returned")]),
                "total_revenue": total_revenue,
                "revenue_today": revenue_today,
                "revenue_month": revenue_month,
                "total_stock_qty": total_stock_qty,
                "low_stock_count": low_stock_count,
                "invoice_total": invoice_total,
                "invoice_paid": invoice_paid,
                "invoice_unpaid": invoice_unpaid,
                "invoice_today": invoice_today,
                "invoice_month": invoice_month,
                "total_categories": Category.search_count([]),
                "category_most_books": max(
                    (c.book_count for c in Category.search([])),
                    default=0,
                ),
            },
            "bookCategories": book_categories,
            "loanTrend": loan_trend,
            "topBooks": top_books,
            "latestLoans": last_loans,
            "latestReaders": last_readers,
        }


