# Claude Code Workspace — Đặng Ngọc Minh Thư

Không gian làm việc cá nhân với Claude Code, xây dựng cho công việc Account PM tại SEONGON.

## Cấu trúc

```
.claude/
  skills/
    meeting-notes/          # Format recap họp → Google Docs
    monthly-report/         # Tạo báo cáo SEO tháng → Google Slides
    send-email-report/      # Soạn + gửi email báo cáo qua Gmail
outputs/                    # File output từ việc chạy skills
chat-history/               # Lịch sử trò chuyện với Claude Code
drive_upload.py             # Tiện ích upload file lên Google Drive
```

## SKILLs

| Skill | Mô tả | Kết nối ngoài | Output |
|-------|-------|---------------|--------|
| `/meeting-notes` | Nhận recap thô → hệ thống hoá → Google Docs (2 phần: Nội dung trao đổi + Next steps) | Google Drive API | Google Docs |
| `/monthly-report` | Nhận file data SEO + config dự án → tạo slide báo cáo tháng | Google Slides API | Google Slides |
| `/send-email-report` | Soạn và gửi email báo cáo cho client kèm chữ ký | Gmail SMTP + App Password | Email + .txt draft |

## Cài đặt

```bash
pip3 install python-docx openpyxl pandas google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Setup kết nối ngoài

### Gmail (send-email-report)
1. Bật 2-Step Verification tại myaccount.google.com/security
2. Tạo App Password tại myaccount.google.com/apppasswords
3. Thêm vào `.claude/skills/send-email-report/config.json`:
```json
{
  "gmail_user": "your@gmail.com",
  "gmail_app_password": "xxxx xxxx xxxx xxxx",
  "sender_name": "SEONGON"
}
```

### Google Drive & Slides API (meeting-notes, monthly-report)
1. Bật Drive API + Slides API tại console.cloud.google.com
2. Tạo OAuth 2.0 credentials (Desktop app) → download `credentials.json`
3. Đặt `credentials.json` vào thư mục gốc workspace
4. Lần đầu chạy sẽ mở trình duyệt để xác nhận quyền

## Output mẫu

- **Biên bản họp TMA Solutions 03/07/2026**: [Google Docs](https://docs.google.com/document/d/157zEbJeVirtgRkvkG_tB8I3YtPnovB2pnOq0jlvV21Y/edit)
- **Báo cáo SEO 07/2026**: [Google Slides](https://docs.google.com/presentation/d/18djhSeTBOYK4AwLE1WelD5EBRT1UuIpL_LNNBQDhs70/edit)
- **Email gửi thành công**: dangngocminhthu@seongon.com (08/07/2026)

## Ghi chú bảo mật

`credentials.json`, `token.json`, và `config.json` được gitignore — không bao giờ commit lên GitHub.
