# Cau truc thu muc module QLTV

```text
QLTV/
├── __init__.py
├── __manifest__.py
├── Readme.md
├── controllers/
│   ├── __init__.py
│   └── library_dashboard.py
├── data/
│   └── library_cron.xml
├── docs/
│   └── cau_trc.md
├── models/
│   ├── __init__.py
│   ├── library_book.py
│   ├── library_reader.py
│   ├── library_loan.py
│   └── library_loan_line.py
├── report/
│   ├── library_reports.xml
│   └── library_report_templates.xml
├── security/
│   ├── library_security.xml
│   └── ir.model.access.csv
├── static/
│   └── src/
│       ├── dashboard/
│       │   ├── library_dashboard.js
│       │   ├── library_dashboard.xml
│       │   └── library_dashboard.scss
│       └── list/
│           ├── library_list_renderer.js
│           └── library_list_renderer.scss
└── views/
    ├── library_book_views.xml
    ├── library_reader_views.xml
    ├── library_loan_views.xml
    ├── library_dashboard_views.xml
    └── library_menus.xml
```

## Mo ta nhanh

- `__manifest__.py`: khai bao thong tin module, dependency, data file va assets.
- `__init__.py`: nap cac package Python cua module.
- `models/`: chua cac model ORM cho sach, doc gia, phieu muon va dong phieu muon.
- `views/`: chua tree, form, search, kanban, dashboard action va menu.
- `security/`: chua nhom quyen va file phan quyen truy cap model.
- `data/`: chua sequence va scheduled action/cron.
- `report/`: chua khai bao report va template QWeb PDF.
- `controllers/`: chua route JSON phuc vu dashboard Owl.
- `static/src/`: chua JavaScript, QWeb template va SCSS cho frontend/backend assets.
- `docs/`: chua tai lieu cau truc va ghi chu ky thuat cua module.
