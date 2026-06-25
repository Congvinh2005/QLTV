Luồng đi của dự án
1. Khởi tạo module
__manifest__.py là entry point.
Odoo đọc manifest, đăng ký:
models,
views,
security,
data sequence/cron,
assets JS/CSS/XML,
report bindings.
2. Cấu trúc chính
models:
library_book.py: quản lý sách
library_reader.py: quản lý độc giả
library_borrow.py: quản lý phiếu mượn
library_borrow_line.py: chi tiết sách trong phiếu
library_return.py: quản lý phiếu trả
dashboard.py: nếu có model/logics dashboard chuyên dụng
views:
menu_views.xml: menu chính
library_book_views.xml: tree/form sách
library_reader_views.xml: tree/form độc giả
library_borrow_views.xml: tree/form/kanban phiếu mượn
library_return_views.xml: tree/form trả sách
library_*_search_views.xml: lọc tìm kiếm riêng
library_*_kanban_views.xml: Kanban riêng
dashboard_views.xml: action dashboard
dashboard_templates.xml: template Owl/QWeb dashboard
security: nhóm, quyền, access rules
report: QWeb PDF cho phiếu mượn/trả
data: sequence, cron, demo
static: JS/SCSS/XML client-side
3. Luồng user khi chạy module
Người dùng vào menu trên Odoo UI.
Menu gọi ir.actions.act_window hoặc ir.actions.client.
Odoo tải view tương ứng:
tree/form/search/kanban cho dữ liệu,
dashboard Owl nếu dashboard action.
Với dashboard:
client Owl (dashboard_action.js) gọi JSON route /library/dashboard/data
controller LibraryDashboardController.dashboard_data() trả về số liệu
template dashboard_templates.xml hiển thị KPI
Với data list:
library_book_views.xml cung cấp tree/form/search
book_list_extension.js mở rộng list nếu cần
Với workflow mượn trả:
tạo phiếu mượn library.loan
trạng thái draft -> approved -> borrowed -> overdue/returned
phiếu trả library.return nếu tách riêng
cron cron_data.xml kiểm tra overdue mỗi ngày
4. Luồng dữ liệu
Model được khởi tạo từ request env: request.env["library.book"]
Các trường compute, liên quan, state nằm trong models
View gọi field, hiển thị dữ liệu
Report QWeb dùng ir.actions.report liên kết template
5. Luồng phát triển
Xác định nghiệp vụ: sách, độc giả, mượn, trả, dashboard, báo cáo
Thiết kế model và quan hệ
Viết view/form/tree/search/kanban
Viết widgets/JS/QWeb nếu cần custom
Thêm security + access
Thêm dữ liệu sequence/cron
Cập nhật manifest, load module, test
6. Kết luận
Hiện tại module đã có luồng chính:

dữ liệu book/reader/loan,
form/tree,
dashboard action,
report mượn.
Nếu cần hoàn chỉnh hơn, nên tiếp tục:

thêm library_return workflow,
tách search/kanban rõ ràng,
hoàn thiện report trả sách,
thêm dashboard charts/Top 10/biểu đồ.
Raptor mini (Preview) • 0.5 credits
