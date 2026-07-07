---
name: monthly-report
description: Nhận file Excel/CSV data SEO → tạo báo cáo SEO tháng dạng .docx gửi client. Kích hoạt khi user nói "tạo báo cáo tháng", "monthly report", "báo cáo SEO", hoặc đưa file Excel ranking/traffic.
---

# Monthly SEO Report Generator

Skill này đọc file data SEO (ranking, traffic từ GSC, SemRush, Ahrefs...) → tính toán chỉ số →
xuất báo cáo tháng dạng .docx theo chuẩn SEONGON.

## Bước 1 — Thu thập thông tin

Hỏi user:
> Bạn cung cấp:
> 1. File data SEO (.xlsx hoặc .csv) — ranking, traffic, hoặc export từ GSC/tool
> 2. Tên client
> 3. Tháng báo cáo (MM/YYYY)
> 4. Tháng so sánh (tháng trước, để tính tăng/giảm)

## Bước 2 — Phân tích file data

Trước khi chạy script, đọc nhanh file để xác định cấu trúc:
```
python3 ~/.claude/skills/monthly-report/generate_report.py \
  --preview --file "<đường dẫn file>"
```
Báo cho user biết script nhận diện được những cột gì.

## Bước 3 — Chạy script tạo báo cáo

```
python3 ~/.claude/skills/monthly-report/generate_report.py \
  --file "<đường dẫn file data>" \
  --client "<tên client>" \
  --month "<MM-YYYY>" \
  --out outputs/bao-cao-seo-<client>-thang-<MM>-<YYYY>.docx
```

Tham số tùy chọn:
- `--prev-month <MM-YYYY>` — tháng so sánh (mặc định: tháng trước)
- `--top <N>` — số từ khóa Top N cần thống kê (mặc định: 10)

## Bước 4 — Kiểm tra và báo kết quả

Checklist trước khi giao:
- [ ] File .docx đã tạo, dung lượng > 0
- [ ] Có đủ các phần: Tổng quan, Kết quả ranking, Traffic, Phân tích, Kế hoạch tháng sau
- [ ] Số liệu tăng/giảm đã được tính và highlight

Báo kết quả:
> Đã tạo báo cáo: `outputs/bao-cao-seo-<client>-thang-<MM>-<YYYY>.docx`
> Tóm tắt: X từ khóa Top 10, traffic tháng Y, tăng/giảm Z% so với tháng trước.

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `ModuleNotFoundError` | Thiếu thư viện | `pip3 install openpyxl python-docx pandas` |
| Không nhận diện được cột | File có tên cột khác chuẩn | Chạy `--preview` để xem cột, dùng `--keyword-col` để chỉ định |
| File CSV encoding lỗi | File không phải UTF-8 | Thêm `--encoding utf-8-sig` hoặc `cp1252` |
