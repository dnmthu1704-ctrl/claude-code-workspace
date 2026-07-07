# send-email-report

Soạn và gửi email báo cáo SEO tháng cho client qua Gmail API.

## Cách dùng

Gõ `/send-email-report` trong Claude Code.

## Setup Gmail App Password

1. Bật 2FA tại myaccount.google.com
2. Vào Security → App passwords → tạo mật khẩu cho "Mail"
3. Điền vào `config.json`:
   ```json
   {
     "gmail_user": "your@gmail.com",
     "gmail_app_password": "xxxx xxxx xxxx xxxx"
   }
   ```

## Output

- Email gửi đến client
- File nháp lưu tại `outputs/email-draft-<client>-<date>.txt`

## Lưu ý bảo mật

- KHÔNG commit `config.json` có chứa App Password lên GitHub
- File `.gitignore` đã loại trừ `config.json` chứa credentials
