# Library Management System - Odoo 16

## 1. Giới thiệu

Library Management System là module quản lý thư viện được phát triển trên nền tảng Odoo 16.

Mục tiêu của hệ thống:

* Quản lý danh mục sách.
* Quản lý độc giả.
* Quản lý quá trình mượn và trả sách.
* Theo dõi số lượng tồn kho.
* Thống kê số lượt mượn.
* Dashboard trực quan.
* Báo cáo QWeb PDF.
* Giao diện Kanban Pipeline.
* Tùy biến bằng Owl/QWeb/JavaScript.

---

# 2. Chức năng hệ thống

## 2.1 Dashboard tổng quan

Dashboard hiển thị các chỉ số quan trọng:

### KPI Cards

* Tổng số đầu sách.
* Tổng số bản sách.
* Tổng số độc giả.
* Tổng số phiếu mượn.
* Số sách đang được mượn.
* Số sách quá hạn.
* Số sách đã trả.

### Dashboard Charts

* Top 10 sách được mượn nhiều nhất.
* Thống kê lượt mượn theo tháng.
* Thống kê sách theo thể loại.
* Thống kê sách đang mượn và đã trả.

### Công nghệ

* Owl Component.
* JavaScript.
* QWeb Template.
* RPC Service.

---

## 2.2 Quản lý sách

### Chức năng

* Thêm sách.
* Sửa thông tin sách.
* Xóa sách.
* Tìm kiếm sách.
* Lọc sách.
* Nhóm sách theo thể loại.

### Thông tin sách

* Mã sách.
* Tên sách.
* Tác giả.
* Thể loại.
* Nhà xuất bản.
* Năm xuất bản.
* ISBN.
* Vị trí kệ.
* Số lượng tồn kho.
* Ảnh bìa.

### Thống kê

* Tổng số lượt mượn.
* Số lượng đang mượn.
* Số lượng còn lại.

---

## 2.3 Quản lý độc giả

### Chức năng

* Thêm độc giả.
* Cập nhật thông tin độc giả.
* Xóa độc giả.
* Tìm kiếm độc giả.

### Thông tin độc giả

* Mã độc giả.
* Họ tên.
* Email.
* Số điện thoại.
* Địa chỉ.
* Ngày đăng ký.

### Theo dõi

* Tổng số lần mượn.
* Sách đang mượn.
* Sách quá hạn.

---

## 2.4 Quản lý mượn sách

### Chức năng

* Tạo phiếu mượn.
* Chọn độc giả.
* Chọn danh sách sách.
* Xác nhận mượn.

### Quy tắc

* Không được mượn vượt quá tồn kho.
* Mỗi phiếu có hạn trả.
* Cập nhật số lượng tồn kho khi mượn.

### Trạng thái

* Draft.
* Approved.
* Borrowed.
* Returned.
* Overdue.

---

## 2.5 Quản lý trả sách

### Chức năng

* Trả sách.
* Cập nhật tồn kho.
* Kiểm tra quá hạn.
* Tính tiền phạt.

### Kết quả

* Hoàn tất trả sách.
* Cập nhật trạng thái phiếu.

---

## 2.6 Kanban Pipeline

Mỗi phiếu mượn được quản lý bằng Kanban.

### Cột trạng thái

Draft
→ Approved
→ Borrowed
→ Returned

Hoặc

Draft
→ Approved
→ Borrowed
→ Overdue
→ Returned

### Chức năng

* Kéo thả trạng thái.
* Theo dõi tiến trình xử lý.
* Màu sắc theo trạng thái.

---

## 2.7 Extend List View

Danh sách sách hiển thị:

| Tên sách | Tồn kho | Đang mượn | Tổng lượt mượn |
| -------- | ------- | --------- | -------------- |

### Chức năng mở rộng

* Highlight sách sắp hết.
* Highlight sách quá hạn.
* Sắp xếp theo lượt mượn.
* Hiển thị badge trạng thái.

---

## 2.8 Search View

### Tìm kiếm

* Tên sách.
* Mã sách.
* Tác giả.
* Nhà xuất bản.

### Bộ lọc

* Đang mượn.
* Đã trả.
* Quá hạn.
* Hết sách.

### Group By

* Thể loại.
* Tác giả.
* Nhà xuất bản.

---

## 2.9 Báo cáo QWeb

### Phiếu mượn sách

Thông tin:

* Mã phiếu.
* Người mượn.
* Ngày mượn.
* Hạn trả.
* Danh sách sách.

### Phiếu trả sách

Thông tin:

* Ngày trả.
* Danh sách sách.
* Tiền phạt.

### Báo cáo thống kê

* Sách được mượn nhiều nhất.
* Sách tồn kho.
* Sách quá hạn.

---

## 2.10 JavaScript Custom

### Dashboard Owl

* KPI Cards.
* Refresh dữ liệu.
* RPC gọi backend.

### List View Extension

* Nút Refresh.
* Badge trạng thái.
* Màu sắc động.

### Kanban Enhancement

* Hiển thị thống kê nhanh.
* Hiệu ứng kéo thả.
* Action Button.

---

# 3. Yêu cầu kỹ thuật

## Backend

* Python
* Odoo ORM
* Computed Fields
* Constraints
* Scheduled Actions

## Frontend

* XML Views
* QWeb
* Owl
* JavaScript

## Reports

* QWeb PDF

---

# 4. Các loại View sử dụng

* Form View
* Tree View
* Search View
* Kanban View
* Pivot View
* Graph View
* Dashboard View
* QWeb Report

---

# 5. Mục tiêu học tập

Module giúp thực hành:

* ORM.
* Security.
* Menu & Actions.
* Tree/Form/Kanban.
* Dashboard.
* QWeb Reports.
* Owl Framework.
* Custom JavaScript.
* RPC Service.
* Asset Management.

Name: Odoo16 Local

Host name/address: host.docker.internal
Port: 5432
Maintenance database: postgres
Username: odoo
Password: (mật khẩu của user odoo)