# Kế hoạch tích hợp Inventory & Accounting vào QLTV

## Mục tiêu
Kế thừa module **stock** (Inventory) và **account** (Accounting) của Odoo để:
- Sách có tồn kho, nhập/xuất tự động
- Phí mượn và phí phạt tạo hoá đơn (invoice) tự động

---

## ✅ Task 1: Thêm dependency và cấu hình cơ bản
- Thêm `stock` và `account` vào `depends` trong `__manifest__.py`
- Thêm quyền truy cập cho model stock/account cho nhóm thư viện (`ir.model.access.csv`)
- Sửa `hooks.py` nếu cần

## ✅ Task 2: Tích hợp `library.book` với `product.product`
- Mỗi `library.book` tự động tạo 1 `product.product` khi create
- Đồng bộ `name`, `isbn` → `barcode`, `price` → `list_price` khi write
- Ngăn xoá sách nếu đã có product
- Thêm field: `product_id`, `qty_available` (related), `product_categ_id`, `price`
- Cập nhật views (form, tree, kanban, search) để hiển thị tồn kho

## ✅ Task 3: Xử lý kho khi mượn/trả sách
- Tạo stock location "Sách đang mượn" (`stock_location_borrowed`) nằm dưới `stock_location_stock`
- `library.loan` thêm field `picking_ids`
- `_create_stock_picking()` tạo internal transfer: Stock ↔ Borrowed khi mượn/trả
- Inherit `stock.picking`, thêm field `loan_id`
- Validate pickings tự động (quantity_done)

## ✅ Task 4: Tích hợp Accounting cho phí mượn & phí phạt
- Tạo product service "Phí thư viện" trong `account_data.xml`
- `library.reader`: thêm `partner_id` + `_get_or_create_partner()`
- `library.loan`: thêm `invoice_ids`, `_create_invoice()` tạo `account.move` (out_invoice) khi trả
- Inherit `account.move`, thêm field `loan_id`

## ✅ Task 5: Dashboard KPIs, Reader Login & Hoàn thiện
### Dashboard & Báo cáo
- Controller trả về stock KPIs (`total_stock_qty`, `low_stock_count`) + invoice KPIs (`invoice_total`, `invoice_paid`, `invoice_unpaid`, `invoice_today`, `invoice_month`)
- Dashboard template: 5 row cards (overview, loans, revenue, stock, accounting)
- Report PDF hiển thị fees, pickings, invoices

### Đơn giản hoá model sách
- Xoá `quantity_total`, `available_count`, `total_borrow_count` khỏi `library.book`
- Chỉ giữ `qty_available` (từ stock) + `borrowed_count` (từ loan) làm nguồn dữ liệu duy nhất
- Dọn views, kanban, search, controller tương ứng

### Đăng nhập bạn đọc
- Thêm `username`, `password` vào `library.reader`
- `_create_user()` auto-tạo `res.users` với `group_library_reader` (dùng username làm login)
- Dùng `sudo()` để bypass permission
- Form hiển thị "Tài khoản đăng nhập" group với 2 field cạnh nhau

### Password toggle (con mắt hiện/ẩn)
- Tạo custom widget OWL `password_toggle_widget.js` + XML template
- Đổi từ `password="True"` → `widget="password_toggle"`
- Thêm CSS cho nút toggle trong input-group

### Dọn DB
- Sửa constraint `library_return_loan_id_fkey` → `ON DELETE SET NULL`
- Xoá return record cũ gây lỗi xoá loan

---

## Lưu ý kỹ thuật
- `location_dest_id` (đúng), **không** `location_dst_id`
- `quantity_done` (đúng) để validate stock.move, **không** `quantity`
- `stock_location_borrowed` có XML ID `QLTV.stock_location_borrowed`
- `res.dongnghiep` chưa có access rules (chỉ dùng được qua sudo)
- Dùng `sudo()` khi tạo `res.users` để librarian không cần quyền đặc biệt
