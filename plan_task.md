# Kế hoạch tích hợp Inventory & Accounting vào QLTV

## Mục tiêu
Kế thừa module **stock** (Inventory) và **account** (Accounting) của Odoo để:
- Sách có tồn kho, nhập/xuất tự động
- Phí mượn và phí phạt tạo hoá đơn (invoice) tự động

---

## Task 1: Thêm dependency và cấu hình cơ bản
- Thêm `stock` và `account` vào `depends` trong `__manifest__.py`
- Thêm quyền truy cập cho model stock/account cho nhóm thư viện
- Cập nhật `hooks.py` nếu cần

## Task 2: Tích hợp `library.book` với `product.product`
- Mỗi `library.book` sẽ tự động tạo 1 `product.product` tương ứng
- Product category, type = service/product, v.v.
- Cập nhật view để hiển thị thông tin tồn kho

## Task 3: Xử lý kho khi mượn/trả sách
- Khi mượn: tạo delivery order (xuất kho)
- Khi trả: tạo receipt (nhập kho)
- Cập nhật số lượng tồn tự động

## Task 4: Tích hợp Accounting cho phí mượn & phí phạt
- Khi trả sách có phí: tự động tạo `account.move` (invoice)
- Theo dõi doanh thu
- Cấu hình tài khoản kế toán mặc định

## Task 5: Nâng cấp Dashboard & báo cáo
- Dashboard hiển thị thêm chỉ số tồn kho, doanh thu kế toán
- Báo cáo PDF tích hợp thông tin mới

---

Chờ bạn xác nhận **Task 1** để bắt đầu.
