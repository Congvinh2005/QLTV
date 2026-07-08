# Kế hoạch tích hợp Invoicing cho QLTV

## Trạng thái hiện tại
- `account.move` đã được kế thừa với field `loan_id`
- `library.loan` có `invoice_ids` One2many
- `_create_invoice()` tạo hóa đơn khi trả sách (phí mượn + phạt)
- Dashboard đã có KPI invoice (total, paid, unpaid, today, month)
- Product `Phí thư viện` (LIBFEE) đã tạo sẵn

## Các task

### TASK 1: Thêm deposit (tiền đặt cọc) vào Loan
- Thêm field `deposit_amount` trên `library.loan`
- Hiển thị trên form view
- Include deposit vào `_create_invoice()` và `total_amount`

### TASK 2: Thanh toán – follow payment state trên Loan phiếu mượn
- Thêm computed field `payment_state` trên `library.loan`
- Lấy từ `invoice_ids.payment_state`
- Hiển thị badge trên tree/form view
- Kaban hiện trạng thái thanh toán 

### TASK 3: Record rules cho account.move
- Reader group chỉ đọc được hóa đơn của phiếu mượn mình
- User/Manager đọc được tất cả

### TASK 4: Smart button invoices trên Loan form
- Hiển thị số lượng + tổng tiền hóa đơn
- Click nhảy đến list invoice của loan đó

### TASK 5: Dashboard biểu đồ doanh thu theo tháng
- Line chart doanh thu 12 tháng gần nhất
- Tổng hợp từ `account.move` có `loan_id`

### TASK 6: Báo cáo hóa đơn tùy chỉnh
- Kế thừa template invoice Odoo
- Thêm mã phiếu mượn, thông tin sách
- Thêm QR/Barcode nếu cần

### TASK 7: Credit note khi hủy phiếu mượn
- Action hủy phiếu → tạo credit note
- Hoàn tiền deposit/fee (nếu có)

### TASK 8: Cron tự động tính phạt quá hạn + tạo invoice
- Chạy mỗi ngày
- Tính phạt quá hạn + tạo invoice bổ sung

### TASK 9: Cấu hình phí qua Settings
- Form Config cho: phí mượn mặc định, phạt/ngày, deposit mặc định
- Dùng `res.config.settings`

### TASK 10: Multi-currency support
- Hiển thị tiền tệ trên loan/invoice
- Tự động chuyển đổi theo reader
