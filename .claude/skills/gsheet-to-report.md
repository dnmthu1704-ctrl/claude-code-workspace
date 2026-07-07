---
name: gsheet-to-report
description: Đọc Google Sheet tracking KPI → tạo báo cáo tiến độ dự án, highlight hạng mục trễ deadline
---

# Google Sheet to Report

## Mục tiêu
Kết nối Google Sheets chứa KPI/task tracking của dự án SEO → tự động đọc dữ liệu, phân tích tiến độ, xuất báo cáo nhanh để update cho client hoặc nội bộ.

## Kết nối ngoài
- **Google Sheets API** — đọc dữ liệu trực tiếp từ sheet qua URL

## Cách dùng
```
/gsheet-to-report [URL Google Sheet]
```

## Các bước Claude sẽ thực hiện
1. Kết nối Google Sheets qua API/URL được cung cấp
2. Đọc các cột: Task | Status | Deadline | Owner | Notes
3. Phân loại: Đúng tiến độ / Trễ deadline / Chưa bắt đầu
4. Tạo tóm tắt tiến độ dạng markdown
5. Xuất báo cáo ra file .md hoặc .docx

## Output
- File `tien-do-du-an-[client]-[DD-MM-YYYY].md`
- Highlight màu đỏ các task trễ deadline

## Lưu ý
Sheet cần có quyền "Anyone with the link can view" hoặc cung cấp credentials.
