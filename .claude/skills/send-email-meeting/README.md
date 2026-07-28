# send-email-meeting

Soạn và gửi email biên bản họp (meeting recap) cho client qua Gmail, dựa trên nội dung đã hệ thống hoá từ skill `meeting-notes`.

## Cách dùng

Gõ `/send-email-meeting` trong Claude Code, sau khi đã có biên bản họp (link Google Docs + action items) từ skill `meeting-notes`.

## Setup Gmail App Password

Dùng chung cấu hình với skill `send-email-report`:

1. Bật 2FA tại myaccount.google.com
2. Vào Security → App passwords → tạo mật khẩu cho "Mail"
3. Điền vào `.claude/skills/send-email-report/config.json`:
   ```json
   {
     "gmail_user": "your@gmail.com",
     "gmail_app_password": "xxxx xxxx xxxx xxxx",
     "sender_name": "SEONGON"
   }
   ```

## Output

- Email gửi đến client (mẫu nhấn mạnh Action Items, văn phong lễ phép chuẩn SEONGON)
- File nháp lưu tại `outputs/meeting-email-<client>-<date>.txt`

## Lưu ý

- Dùng `--draft-only` để chỉ tạo/xem bản nháp, không gửi thật
- LUÔN cho user xem nháp và chỉ gửi khi user xác nhận

## Lưu ý bảo mật

- KHÔNG commit `config.json` có chứa App Password lên GitHub
- File `.gitignore` đã loại trừ `config.json` chứa credentials
