---
name: send-email-meeting
description: Soạn và gửi email biên bản họp (meeting recap) cho client sau khi file meeting notes đã hoàn thiện qua skill meeting-notes. Kích hoạt khi user nói "gửi biên bản họp cho khách", "gửi recap cho client", "email meeting notes", hoặc vừa hoàn thiện file meeting-notes và muốn gửi ngay.
---

# Send Email Meeting Notes (Gmail)

Skill này soạn email gửi biên bản họp cho client, dựa trên nội dung đã hệ thống hoá từ skill `meeting-notes` (Nội dung trao đổi + Next steps). Văn phong: lễ phép, xưng "team em", gọi khách "chị/anh + tên + team [Client]", có "ạ" cuối câu — theo đúng phong cách email thật của Đặng Ngọc Minh Thư.

Dùng chung cấu hình Gmail với skill `send-email-report` (`.claude/skills/send-email-report/config.json`) — xem phần Setup ở đó nếu chưa cấu hình. Việc gửi thật do script riêng của skill này đảm nhiệm (`send_email_meeting.py`), không dùng script của `send-email-report` vì văn phong và cấu trúc nội dung khác nhau (báo cáo tháng vs. biên bản họp).

## Bước 1 — Thu thập thông tin

Lấy từ output của `meeting-notes` (không hỏi lại nếu đã có sẵn trong context):
1. Tên client / team
2. Ngày họp
3. Link Google Docs biên bản
4. Action items (việc, PIC, deadline)

Hỏi thêm user nếu chưa rõ:
5. Email người nhận + tên người nhận (chị/anh ...)

## Bước 2 — Mẫu email

Mặc định dùng **Mẫu C — Nhấn mạnh Action Items** (văn phong chuẩn của Thư), phù hợp với hầu hết trường hợp gửi biên bản họp cho client.

```
Subject: [SEONGON] Biên bản họp & Action Items - <Client> - <DD/MM/YYYY>

Dear chị/anh <Tên> và team <Client>,

SEONGON cảm ơn chị/anh <Tên> và team <Client> đã trao đổi trong buổi họp ngày <DD/MM/YYYY> ạ. Team em xin tổng hợp lại các action items cần hai bên cùng lưu ý:

1. <Việc> — PIC: <ai> — Hạn: <ngày>
2. <Việc> — PIC: <ai> — Hạn: <ngày>
3. <Việc> — PIC: <ai> — Hạn: <ngày>

Team em mong chị/anh xác nhận giúp các đầu việc trên để hai bên cùng theo dõi tiến độ ạ.

Biên bản chi tiết đầy đủ: <link Google Docs>

SEONGON cảm ơn chị/anh <Tên> và team <Client> đã phối hợp, hỗ trợ team trong giai đoạn vừa qua. Hy vọng hai bên sẽ tiếp tục phối hợp hiệu quả để đạt được các mục tiêu đã thống nhất ạ.

Trân trọng,
Đặng Ngọc Minh Thư
Account PM | SEONGON
📞 098.77.99.803
✉️ dnmthu1704@gmail.com
```

Nếu recap không có action item nào (họp chỉ để cập nhật thông tin), bỏ đoạn "Team em mong chị/anh xác nhận..." và thay danh sách action items bằng 1-2 câu tóm tắt nội dung trao đổi.

## Bước 3 — Xác nhận trước khi gửi

Điền nội dung mẫu với thông tin thật, hiện cho user xem:
> Đây là nội dung email sẽ gửi đến [email]:
> [nội dung email đầy đủ]
>
> Bạn muốn **gửi ngay** hay **chỉnh sửa** gì không?

CHỈ gửi khi user xác nhận "gửi" hoặc "ok".

## Bước 4 — Gửi và lưu

```
python3 /Users/dnmthw/Downloads/claude-code-workspace/.claude/skills/send-email-meeting/send_email_meeting.py \
  --to "<email_client>" \
  --recipient-name "<Tên người nhận>" \
  --client "<Tên client/team>" \
  --date "<DD/MM/YYYY>" \
  --items "<Việc 1>|<PIC 1>|<Hạn 1>;;<Việc 2>|<PIC 2>|<Hạn 2>" \
  --link "<link Google Docs biên bản>"
```

Thêm `--draft-only` để chỉ xem/lưu nháp, không gửi. Bỏ flag đó để gửi thật sau khi user xác nhận.

Bản nháp được lưu tự động vào `outputs/meeting-email-<client>-<DD-MM-YYYY>.txt`.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|-----|------------|
| Chưa có link Google Docs biên bản | Chạy `meeting-notes` trước |
| Không có action item nào | Bỏ qua đoạn action items, dùng bản tóm tắt ngắn thay thế (xem cuối Bước 2) |
| Authentication failed khi gửi | Xem phần Setup của skill `send-email-report` (dùng chung config Gmail) |
