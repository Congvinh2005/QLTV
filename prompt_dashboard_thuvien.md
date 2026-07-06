# PROMPT CHO AGENT: Xây dựng Dashboard "Quản lý Thư viện" trong Odoo (giao diện giống 100% ảnh mẫu)

## 0. Bối cảnh & yêu cầu chung
Bạn là AI coding agent, hãy xây dựng module Odoo tên `library_management` với một trang **Dashboard Tổng quan** (route riêng, dùng OWL component + QWeb template, không dùng view mặc định của Odoo). Giao diện phải khớp **pixel-perfect** với ảnh mẫu được cung cấp: bố cục, khoảng cách, màu sắc, font, icon, số liệu, biểu đồ.

**Stack đề xuất:**
- Backend: Odoo 17 (Python + ORM), controller `http.route` trả JSON cho dashboard.
- Frontend: OWL Component (`owl` framework có sẵn trong Odoo) + QWeb template `.xml`.
- CSS: SCSS riêng cho module, không đè style Odoo gốc.
- Biểu đồ: dùng thư viện **Chart.js** (đã có sẵn trong assets Odoo `web.chartjs_lib`) để vẽ Pie chart và Line chart.
- Icon: dùng Font Awesome (có sẵn trong Odoo) hoặc bootstrap-icons, chọn icon gần giống nhất với ảnh mẫu (đã chú thích icon cụ thể ở từng phần dưới).

---

## 1. Bố cục tổng thể (Layout)

```
┌───────────────────────────────────────────────────────────┐
│ TOP NAVBAR (fixed, full width)                              │
├───────────┬───────────────────────────────────────────────┤
│ SIDEBAR   │ MAIN CONTENT (background #F4F5FA, padding 24px)│
│ (fixed,   │  - 5 KPI cards hàng 1                           │
│  width    │  - 3 KPI cards hàng 2                           │
│  ~230px)  │  - 3 KPI cards hàng 3 (doanh thu)               │
│           │  - 2 card lớn hàng 4 (tồn kho / sắp hết)        │
│           │  - 5 KPI cards hàng 5 (hoá đơn)                 │
│           │  - 3 widget hàng 6 (pie chart / line chart /    │
│           │    top sách mượn nhiều)                         │
│           │  - 3 widget hàng 7 (bảng phiếu mượn / bảng      │
│           │    độc giả / panel cảnh báo)                    │
└───────────┴───────────────────────────────────────────────┘
```

Toàn bộ card dùng `border-radius: 12px`, `box-shadow: 0 1px 3px rgba(0,0,0,0.06)`, nền trắng `#FFFFFF`, trừ các card có nền màu nhạt riêng (đã ghi chú).

---

## 2. TOP NAVBAR

- Nền: gradient tím-indigo, từ `#4A3AB0` (trái) đến `#5B4CD6` (phải), chiều cao 60px.
- **Bên trái:**
  - Icon lưới (grid/apps) màu trắng, kích thước 20px.
  - Logo icon sách (book icon) + chữ **"Thư viện"** (font-weight 700, màu trắng, size 18px).
- **Giữa (menu ngang):** các item, chữ trắng, item đang active có nền trắng mờ `rgba(255,255,255,0.15)` + border-radius 8px + padding 8px 14px:
  1. **Dashboard** (active)
  2. Quản lý Sách
  3. Quản lý Độc giả
  4. Phiếu mượn
  5. Quản lý Mượn trả
  6. Báo cáo
- **Bên phải:**
  - Icon chat/bình luận, có badge đỏ số **"2"** ở góc trên phải icon.
  - Icon đồng hồ (lịch sử).
  - Avatar tròn màu hồng/magenta `#D6409F`, chữ **"Q"** trắng ở giữa.
  - Chữ **"Quản lý thư viện"** + icon mũi tên xuống (dropdown user menu).

---

## 3. SIDEBAR TRÁI

- Nền trắng, width ~230px, full height, border-right nhẹ `#EEEEEE`.
- Item **"Tổng quan"** (icon home) đang active: nền tím nhạt `#EEEBFB`, chữ tím đậm `#5B4CD6`, icon tím, bo góc trái phải rounded, có thanh chỉ báo hoặc nổi bật rõ so với các item khác.
- Nhóm menu, mỗi nhóm có **label nhỏ chữ hoa, màu xám** `#9CA3AF`, letter-spacing rộng, size 11px:

  **QUẢN LÝ**
  - Sách (icon: book/document)
  - Độc giả (icon: người/group)
  - Phiếu mượn (icon: id-card / ticket)
  - Mượn trả (icon: swap/arrows ngang)

  **BÁO CÁO**
  - Báo cáo (icon: bar-chart)
  - Thống kê (icon: pie-chart)

  **CÀI ĐẶT**
  - Danh mục (icon: list)
  - Cấu hình (icon: gear/settings)

- Các item không active: icon + chữ màu xám đậm `#4B5563`, hover có nền xám nhạt `#F3F4F6`.

---

## 4. HÀNG KPI CARD 1 — 5 thẻ tổng quan chính

Mỗi card: nền trắng, padding 20px, bo góc 12px, layout: icon tròn nền màu nhạt bên trái + số liệu lớn bên phải, dòng label dưới số, dòng % so sánh dưới cùng (mũi tên lên màu xanh `#16A34A` hoặc mũi tên xuống màu đỏ `#DC2626`).

| # | Icon (nền tròn nhạt) | Số | Label | % so sánh |
|---|---|---|---|---|
| 1 | 📘 sách, nền xanh dương nhạt `#DBEAFE`, icon `#2563EB` | **4** | Tổng sách | ↑ 12% so với tháng trước (xanh) |
| 2 | 👥 người, nền xanh lá nhạt `#DCFCE7`, icon `#16A34A` | **7** | Độc giả | ↑ 8% so với tháng trước (xanh) |
| 3 | 🔁 hai mũi tên xoay, nền cam nhạt `#FFEDD5`, icon `#EA580C` | **0** | Đang mượn | ↓ 100% so với tháng trước (đỏ) |
| 4 | ⚠️ tam giác cảnh báo, nền đỏ/hồng nhạt `#FEE2E2`, icon `#DC2626` | **0** | Quá hạn | ↓ 100% so với tháng trước (đỏ) |
| 5 | ✅ dấu tích trong khiên/tròn, nền tím nhạt `#EDE9FE`, icon `#7C3AED` | **90** | Có sẵn | ↑ 15% so với tháng trước (xanh) |

---

## 5. HÀNG KPI CARD 2 — 3 thẻ (không có % so sánh)

| Icon | Số | Label |
|---|---|---|
| icon layers/3D cubes, nền xanh ngọc nhạt `#CCFBF1`, icon `#0D9488` | **90** | Tổng bản |
| icon bút chì/edit, nền cam nhạt `#FFEDD5`, icon `#EA580C` | **2** | Phiếu mượn |
| icon mũi tên xoay lại (undo/history), nền xám nhạt `#F3F4F6`, icon `#6B7280` | **2** | Đã trả |

---

## 6. HÀNG KPI CARD 3 — Doanh thu (3 thẻ)

| Icon | Số | Label | % |
|---|---|---|---|
| $ tròn, nền xanh dương nhạt, icon `#2563EB` | **12,123** | Tổng doanh thu | ↑ 20% so với tháng trước |
| icon lịch, nền cam nhạt, icon `#EA580C` | **12,123** | Doanh thu hôm nay | (không có %) |
| icon lịch có dấu tick, nền xanh dương nhạt, icon `#2563EB` | **12,123** | Doanh thu tháng này | (không có %) |

Định dạng số có dấu phẩy ngăn cách hàng nghìn (12,123).

---

## 7. HÀNG 4 — 2 CARD LỚN (nửa trang mỗi card)

1. **Card trái** (nền gradient tím nhạt `#F1EEFD` → trắng): icon layers tím `#7C3AED`, số **90**, label "Tồn kho thực tế".
2. **Card phải** (nền đỏ/hồng nhạt `#FEF2F2`): icon tam giác cảnh báo đỏ, số **0**, label "Sắp hết", ghi chú nhỏ bên cạnh label "(≤ 3 bản)" màu xám.

---

## 8. HÀNG 5 — 5 thẻ hoá đơn

| Icon | Số | Label |
|---|---|---|
| icon tài liệu, nền xanh dương nhạt | **0** | Tổng hoá đơn |
| icon check tròn, nền xanh lá nhạt | **0** | Đã thanh toán |
| icon đồng hồ, nền cam nhạt | **0** | Chưa thanh toán |
| icon lịch, nền tím nhạt | **0** | Hoá đơn hôm nay |
| icon lịch check, nền xanh dương nhạt | **0** | Hoá đơn tháng này |

---

## 9. HÀNG 6 — 3 widget (chart & danh sách)

### 9.1. Widget "Sách theo danh mục" (Pie/Donut chart)
- Header: tiêu đề trái, dropdown **"Tất cả"** (select box nhỏ, viền xám, icon chevron) bên phải.
- Biểu đồ tròn (pie chart, không phải donut — full pie), chia 5 phần với % hiển thị trực tiếp trên từng lát:
  - Văn học — 35% — màu xanh dương `#3B82F6`
  - Khoa học — 25% — màu xanh lá `#22C55E`
  - Thiếu nhi — 20% — màu cam `#F97316`
  - Kinh tế — 10% — màu tím `#8B5CF6`
  - Công nghệ — 10% — màu đỏ hồng `#EC4899`
- Legend bên phải chart: ô vuông màu nhỏ + tên danh mục, xếp theo cột.

### 9.2. Widget "Tình trạng mượn sách (6 tháng qua)" (Line chart)
- Header: tiêu đề trái.
- Legend trên cùng của chart: đường tròn nhỏ tím = "Đã mượn", đường tròn nhỏ xanh lá = "Đã trả".
- Line chart 2 đường:
  - **Đã mượn** — màu tím `#7C3AED`, có điểm tròn (dot marker) tại mỗi tháng.
  - **Đã trả** — màu xanh lá `#22C55E`, có điểm tròn tại mỗi tháng.
- Trục X: T1, T2, T3, T3, T4, T5, T6 *(giữ đúng như ảnh mẫu — lưu ý ảnh gốc có 2 nhãn "T3" liên tiếp, xác nhận lại với dữ liệu thật hoặc sửa thành T1–T6 tuần tự)*.
- Trục Y: 0 đến 50, bước nhảy 10 (0,10,20,30,40,50).
- Dữ liệu mẫu Đã mượn: [15, 20, 34, 27, 32, 42]
- Dữ liệu mẫu Đã trả: [5, 8, 12, 25, 20, 22]

### 9.3. Widget "Top sách được mượn nhiều"
- Header: tiêu đề trái, link **"Xem tất cả"** màu tím, bên phải.
- Danh sách 5 dòng, mỗi dòng gồm: số thứ tự (1–5, chữ xám), tên sách, progress bar ngang (màu tím `#7C3AED` trên nền xám nhạt `#E5E7EB`, bo tròn 2 đầu, độ rộng tỉ lệ theo số lượt mượn so với max=25), số lượt mượn bên phải cùng dòng.

| # | Tên sách | Lượt mượn |
|---|---|---|
| 1 | Đắc nhân tâm | 25 |
| 2 | Nhà giả kim | 18 |
| 3 | Cho tôi xin một vé đi tuổi thơ | 15 |
| 4 | Dế mèn phiêu lưu ký | 12 |
| 5 | Atomic Habits | 10 |

---

## 10. HÀNG 7 — 3 widget (bảng & cảnh báo)

### 10.1. Bảng "Phiếu mượn mới nhất"
- Header: tiêu đề trái, link "Xem tất cả" tím bên phải.
- Cột: Mã phiếu | Độc giả | Ngày mượn | Hạn trả | Trạng thái.
- Trạng thái hiển thị dạng **badge pill**:
  - "Đang mượn" — nền xanh dương nhạt `#DBEAFE`, chữ xanh dương `#2563EB`.
  - "Đã trả" — nền xanh lá nhạt `#DCFCE7`, chữ xanh lá `#16A34A`.
- Dữ liệu mẫu:

| Mã phiếu | Độc giả | Ngày mượn | Hạn trả | Trạng thái |
|---|---|---|---|---|
| PM0002 | Nguyễn Văn A | 05/07/2025 | 12/07/2025 | Đang mượn |
| PM0001 | Trần Thị B | 04/07/2025 | 11/07/2025 | Đã trả |

### 10.2. Bảng "Độc giả mới nhất"
- Header: tiêu đề trái, link "Xem tất cả" tím bên phải.
- Cột: Mã độc giả | Tên độc giả | SĐT | Ngày đăng ký.
- Dữ liệu mẫu:

| Mã độc giả | Tên độc giả | SĐT | Ngày đăng ký |
|---|---|---|---|
| DG0007 | Phạm Văn E | 0901234567 | 03/07/2025 |
| DG0006 | Lê Thị D | 0912345678 | 02/07/2025 |
| DG0005 | Nguyễn Văn C | 0923456789 | 30/06/2025 |

### 10.3. Panel "Cảnh báo"
- Danh sách 3 dòng, mỗi dòng: icon tròn nhỏ nền màu nhạt bên trái + text + (có thể có) link "Xem chi tiết" tím bên phải:
  1. Icon tam giác cảnh báo cam (nền cam nhạt) — "0 sách quá hạn" — link "Xem chi tiết".
  2. Icon "i" thông tin xanh dương (nền xanh dương nhạt) — "0 sách sắp hết (≤ 3 bản)" — link "Xem chi tiết".
  3. Icon check xanh lá (nền xanh lá nhạt) — "Hệ thống hoạt động bình thường" — không có link.

---

## 11. Bảng màu tổng hợp (dùng biến SCSS)

```scss
$bg-page: #F4F5FA;
$card-bg: #FFFFFF;
$navbar-gradient: linear-gradient(90deg, #4A3AB0, #5B4CD6);
$primary-purple: #7C3AED;
$blue: #2563EB;
$blue-bg: #DBEAFE;
$green: #16A34A;
$green-bg: #DCFCE7;
$orange: #EA580C;
$orange-bg: #FFEDD5;
$red: #DC2626;
$red-bg: #FEE2E2;
$teal: #0D9488;
$teal-bg: #CCFBF1;
$gray-text: #6B7280;
$text-dark: #111827;
$border-color: #E5E7EB;
$radius-card: 12px;
$shadow-card: 0 1px 3px rgba(0,0,0,0.06);
```

Font: dùng font hệ thống Odoo hiện tại (thường là `Inter` hoặc `Roboto`) — số liệu KPI: `font-weight: 700; font-size: 24px;`, label: `font-size: 13px; color: $gray-text;`.

---

## 12. Yêu cầu kỹ thuật cụ thể cho Odoo

1. Tạo module `library_management` với cấu trúc chuẩn: `__manifest__.py`, `models/`, `controllers/`, `static/src/js/`, `static/src/xml/`, `static/src/scss/`.
2. Controller Python trả về JSON tổng hợp toàn bộ số liệu (tổng sách, độc giả, đang mượn, quá hạn, doanh thu, top sách mượn nhiều, phiếu mượn mới nhất, độc giả mới nhất...) — tính từ các model `library.book`, `library.member`, `library.borrow`, v.v.
3. OWL Component load dữ liệu qua `this.orm` hoặc `rpc` khi `willStart`/`onWillStart`, render qua QWeb template khớp bố cục ở trên.
4. Chart.js: khởi tạo trong `onMounted`, hủy instance trong `onWillUnmount` để tránh leak khi chuyển trang.
5. Thêm route menu "Dashboard" (`ir.actions.client`) trỏ tới action `library_management.dashboard` gắn với tag component OWL.
6. Đảm bảo responsive: ở màn hình < 1200px, các hàng KPI card tự động xuống 2–3 cột; sidebar có thể thu gọn thành icon-only.
7. Toàn bộ text hiển thị bằng tiếng Việt như trong bảng mô tả, không dịch sang tiếng Anh.
8. Số liệu hiện tại đều là dữ liệu mẫu/tĩnh trong ảnh — cần map đúng field thật khi có dữ liệu, nhưng bố cục/style phải giữ nguyên as-is.

---

## 13. Checklist đối chiếu (agent tự kiểm tra trước khi báo hoàn thành)

- [ ] Navbar đúng màu gradient tím, đủ 6 menu, đúng icon phải (chat badge, clock, avatar hồng "Q").
- [ ] Sidebar đúng 3 nhóm mục, đúng item active "Tổng quan" có nền tím nhạt.
- [ ] Đủ 5+3+3+2+5 = 18 KPI card ở 5 hàng đầu, đúng icon/màu/số liệu như bảng.
- [ ] 2 card lớn hàng 4 đúng nền màu gradient tím & đỏ nhạt.
- [ ] Pie chart đúng 5 danh mục, đúng %, đúng màu, có legend.
- [ ] Line chart đúng 2 đường, đúng màu, đúng legend, đúng trục.
- [ ] Top sách mượn nhiều đúng progress bar tỉ lệ theo số liệu.
- [ ] 2 bảng dữ liệu đúng cột, đúng badge trạng thái có màu.
- [ ] Panel cảnh báo đúng 3 icon màu (cam/xanh dương/xanh lá).
- [ ] Toàn trang nền `#F4F5FA`, card trắng bo góc 12px, đổ bóng nhẹ, khoảng cách giữa card đồng nhất (~20-24px).
