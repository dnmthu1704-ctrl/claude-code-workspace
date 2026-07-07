---
name: meeting-notes
description: Chuyển ghi chú thô sau buổi họp client → biên bản họp chuẩn dạng .docx
---

# Meeting Notes Formatter

## Mục tiêu
Nhận ghi chú thô (bullet points, từ khóa rời) sau buổi họp → format thành biên bản họp chuyên nghiệp, có phân công công việc và deadline rõ ràng.

## Cách dùng
```
/meeting-notes
```
Sau đó paste hoặc đính kèm:
- Ghi chú thô của buổi họp
- Tên client, ngày họp, thành phần tham dự

## Các bước Claude sẽ thực hiện
1. Đọc ghi chú thô
2. Phân loại nội dung: thông tin chung → vấn đề thảo luận → quyết định → action items
3. Format lại theo cấu trúc biên bản họp chuẩn
4. Xuất ra file .docx

## Output
- File `bien-ban-hop-[client]-[DD-MM-YYYY].docx`
- Phần Action Items có cột: Nội dung | Người phụ trách | Deadline
