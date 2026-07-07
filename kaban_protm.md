Hãy tạo một Kanban View cho Odoo 16 Community theo phong cách hiện đại giống giao diện CRM/Education.

Yêu cầu:

1. Card
- Card bo góc 8px.
- Background trắng.
- Có border mỏng #e5e7eb.
- Shadow nhẹ.
- Padding khoảng 16px.
- Hover nổi lên nhẹ (box-shadow lớn hơn).
- Chiều rộng khoảng 320-340px.

2. Header
Hiển thị:

Tên lớp (ví dụ)

26.TQV.TO2.L.033

font-size:18px
font-weight:700

Ngay dưới là

Tên chi nhánh hoặc cơ sở

font-size:14px
color:#666

Góc phải có menu

⋮

3. Badge

Bên trái có badge màu xanh lá

16 STUDENTS

border-radius:4px

background:#2E7D32

color:white

padding:6px 12px

font-weight:bold

4. Thông tin bên phải

Hiển thị dạng label/value

Status

Closed

Capacity

16

Available Seats

0

Lessons

25

Label màu xám

Value màu đen đậm

Status hiển thị badge màu xám.

5. Thông tin ngày

Có một hàng gồm 3 cột.

Cột 1

30/01/2026

Start Date

Cột 2

12/05/2026

End Date

Cột 3

Tên giáo viên

Teacher

Các cột có border-right.

Canh giữa.

6. Danh sách khóa học

Hiển thị

Courses:

• TOEIC 750

• IELTS

• ...

Nếu nhiều hơn 3 dòng thì hiện

+N more

7. Footer

Nếu có trạng thái

Completed

Cancelled

Opening

thì hiển thị badge màu khác nhau.

8. Kanban Layout

Sử dụng:

<t t-name="kanban-box">

<div class="oe_kanban_global_click">

....

</div>

</t>

9. Không dùng table.

Chỉ dùng

div

d-flex

justify-content-between

align-items-center

flex-column

flex-row

10. Style

Dùng class Bootstrap/Odoo:

o_kanban_record

o_kanban_card

badge

text-muted

fw-bold

small

mb-2

mb-3

mt-2

11. Nếu có avatar giáo viên thì hiển thị ảnh tròn 40x40 ở góc trên.

12. Card phải responsive.

13. Code trả về chỉ gồm XML Kanban View của Odoo 16, không giải thích.

14. Thiết kế giống 95% giao diện Education/CRM hiện đại của Odoo Enterprise.


Nếu áp dụng cho module Thư viện của bạn thì mình khuyên sửa prompt theo nghiệp vụ thư viện để giao diện đẹp và thực tế hơn. Ví dụ mỗi card sẽ là một phiếu mượn:
Tiêu đề: Mã phiếu mượn (PM0001).
Dòng dưới: Tên độc giả.
Badge màu xanh: 3 quyển sách.
Góc phải: Trạng thái (Bản nháp, Đã duyệt, Đang mượn, Quá hạn, Đã trả).
Khối thông tin:
Ngày mượn
Ngày hết hạn
Số ngày mượn
Tổng tiền
Footer hiển thị danh sách sách đã mượn (tối đa 3 cuốn, nếu nhiều hơn thì +N quyển khác).
Badge trạng thái đổi màu:
🟡 Draft
🔵 Approved
🟢 Borrowed
🔴 Overdue
⚫ Returned