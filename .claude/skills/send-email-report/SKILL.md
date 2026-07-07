---
name: send-email-report
description: Soạn và gửi email báo cáo SEO tháng cho client qua Gmail. Kích hoạt khi user nói "gửi báo cáo", "send email report", "email cho client", hoặc muốn gửi file báo cáo qua email.
---

# Send Email Report (Gmail)

Skill này soạn email báo cáo SEO chuyên nghiệp và gửi qua Gmail API.
Đây là skill kết nối nền tảng ngoài (Gmail API).

## Setup bắt buộc (lần đầu)

Trước khi dùng, cần cấu hình Gmail API:

1. Vào Google Cloud Console → tạo project → bật Gmail API
2. Tạo OAuth 2.0 credentials → tải file `credentials.json`
3. Đặt file `credentials.json` vào folder này: `.claude/skills/send-email-report/`
4. Lần đầu chạy sẽ mở trình duyệt để xác thực → tạo file `token.json`

Hoặc dùng App Password (đơn giản hơn):
1. Bật 2FA cho Gmail
2. Tạo App Password tại myaccount.google.com → Security → App passwords
3. Thêm vào config.json: `"gmail_user"` và `"gmail_app_password"`

## Bước 1 — Thu thập thông tin

Hỏi user:
> Cần biết:
> 1. Email client (người nhận)
> 2. Tên client
> 3. Tháng báo cáo
> 4. File báo cáo đính kèm (.docx hoặc .pdf)
> 5. 2-3 highlights chính muốn nhắc trong email (KPI đạt được, điểm nổi bật)

## Bước 2 — Chạy script

```
python3 ~/.claude/skills/send-email-report/send_email.py \
  --to "<email_client>" \
  --client "<tên client>" \
  --month "<tháng>" \
  --attach "<đường dẫn file báo cáo>" \
  --highlights "<highlight 1>|<highlight 2>|<highlight 3>" \
  --draft-only
```

Chạy với `--draft-only` trước để user xem nháp email. Sau khi user confirm mới gửi thật (bỏ flag đó).

## Bước 3 — Xác nhận trước khi gửi

Hiện nội dung email cho user xem:
> Đây là nội dung email sẽ gửi đến [email]:
> [nội dung email]
>
> Bạn muốn **gửi ngay** hay **chỉnh sửa** gì không?

CHỈ gửi khi user xác nhận "gửi" hoặc "ok".

## Bước 4 — Gửi và báo kết quả

```
python3 ~/.claude/skills/send-email-report/send_email.py \
  --to "<email_client>" \
  --client "<tên client>" \
  --month "<tháng>" \
  --attach "<đường dẫn file báo cáo>" \
  --highlights "<highlight 1>|<highlight 2>|<highlight 3>"
```

Lưu bản nháp email vào `outputs/email-draft-<client>-<date>.txt`

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `Authentication failed` | Sai App Password hoặc chưa bật 2FA | Kiểm tra lại App Password trong Google Account |
| `SMTPAuthenticationError` | Gmail chặn app kém an toàn | Dùng App Password thay vì mật khẩu thường |
| `File not found` | Đường dẫn file đính kèm sai | Kiểm tra đường dẫn tuyệt đối |
| `ModuleNotFoundError` | Thiếu thư viện | `pip3 install secure-smtplib` |
