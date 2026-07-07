from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LibraryBookCopy(models.Model):
    _name = "library.book.copy"
    _description = "Bản sao sách"
    _rec_name = "display_name"
    _order = "book_id, code"

    book_id = fields.Many2one("library.book", string="Sách", required=True, ondelete="cascade")
    code = fields.Char(string="Mã bản sao", required=True)
    state = fields.Selection([
        ("available", "Có sẵn"),
        ("borrowed", "Đang mượn"),
        ("damaged", "Hư hỏng"),
        ("lost", "Mất"),
    ], string="Trạng thái", default="available", required=True)
    loan_line_id = fields.Many2one("library.loan.line", string="Phiếu mượn", ondelete="set null")
    reader_name = fields.Char(string="Người mượn", compute="_compute_reader_name", store=True)

    display_name = fields.Char(string="Tên hiển thị", compute="_compute_display_name", store=True)

    _sql_constraints = [
        ("book_copy_code_unique", "unique(book_id, code)", "Mã bản sao phải là duy nhất trong cùng một sách."),
    ]

    @api.depends("loan_line_id.loan_id.reader_id.name")
    def _compute_reader_name(self):
        for copy in self:
            copy.reader_name = copy.loan_line_id.loan_id.reader_id.name if copy.loan_line_id and copy.loan_line_id.loan_id and copy.loan_line_id.loan_id.reader_id else ""

    @api.depends("book_id.name", "code")
    def _compute_display_name(self):
        for copy in self:
            copy.display_name = "%s - %s" % (copy.book_id.name, copy.code) if copy.book_id else copy.code

    def unlink(self):
        if not self.env.context.get("skip_copy_delete_check"):
            raise UserError(_("Không thể xoá bản sao trực tiếp. Hãy điều chỉnh tồn kho trong Inventory để đồng bộ."))
        return super().unlink()

    def action_mark_available(self):
        self.write({"state": "available", "loan_line_id": False})

    def action_mark_damaged(self):
        self.write({"state": "damaged"})

    def action_mark_lost(self):
        self.write({"state": "lost"})
