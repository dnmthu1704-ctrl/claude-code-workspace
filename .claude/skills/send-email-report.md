---
name: send-email-report
description: Tạo và gửi email báo cáo SEO tháng cho client qua Gmail
---

# Send Email Report

## Mục tiêu
Soạn email báo cáo SEO tháng theo tone chuyên nghiệp, đính kèm file báo cáo và gửi thẳng đến email client qua Gmail.

## Kết nối ngoài
- **Gmail API / MCP** — gửi email trực tiếp từ tài khoản Gmail SEONGON

## Cách dùng
```
/send-email-report
```
Sau đó cung cấp:
- Tên client và email nhận
- File báo cáo đính kèm (.docx hoặc .pdf)
- Tháng báo cáo
- Các điểm nổi bật muốn nhắc trong email

## Các bước Claude sẽ thực hiện
1. Soạn nội dung email theo tone chuyên nghiệp, thân thiện
2. Tóm tắt 2–3 highlights chính của tháng trong body email
3. Đính kèm file báo cáo
4. Gửi email qua Gmail đến địa chỉ client
5. Xác nhận đã gửi thành công

## Output
- Email đã gửi đến client
- Bản nháp email lưu lại dạng .txt để lưu hồ sơ
