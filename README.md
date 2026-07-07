# Claude Code Workspace — Đặng Ngọc Minh Thư

Không gian làm việc cá nhân với Claude Code, xây dựng cho công việc Account PM tại SEONGON.

## Cấu trúc

```
.claude/
  skills/
    meeting-notes/          # Format biên bản họp → .docx
    monthly-report/         # Tạo báo cáo SEO tháng → .docx
    send-email-report/      # Gửi email báo cáo qua Gmail
outputs/                    # File output từ việc chạy skills
chat-history/               # Lịch sử trò chuyện với Claude Code
```

## SKILLs

| Skill | Mô tả | Kết nối ngoài | Output |
|-------|-------|---------------|--------|
| `/meeting-notes` | Chuyển ghi chú thô → biên bản họp có task, PIC, deadline | — | .docx |
| `/monthly-report` | Đọc file Excel/CSV SEO data → báo cáo tháng | — | .docx |
| `/send-email-report` | Soạn và gửi email báo cáo cho client | Gmail SMTP | email + .txt |

## Cài đặt thư viện

```bash
pip3 install python-docx openpyxl
```

## Setup Gmail (cho skill send-email-report)

Xem hướng dẫn tại `.claude/skills/send-email-report/README.md`
