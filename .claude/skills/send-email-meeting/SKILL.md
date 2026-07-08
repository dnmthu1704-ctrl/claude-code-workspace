---
name: send-email-meeting
description: Soạn và gửi email biên bản họp (meeting recap) cho client sau khi file meeting notes đã hoàn thiện qua skill meeting-notes. Kích hoạt khi user nói "gửi biên bản họp cho khách", "gửi recap cho client", "email meeting notes", hoặc vừa hoàn thiện file meeting-notes và muốn gửi ngay.
---

# Send Email Meeting Notes (Gmail)

Skill này soạn email gửi biên bản họp cho client, dựa trên nội dung đã hệ thống hoá từ skill `meeting-notes` (Nội dung trao đổi + Next steps).

Dùng chung cơ chế gửi Gmail với skill `send-email-report` — xem phần Setup ở đó nếu chưa cấu hình (`.claude/skills/send-email-report/config.json` hoặc `credentials.json`).

## Bước 1 — Thu thập thông tin

Lấy từ output của `meeting-notes` (không hỏi lại nếu đã có sẵn trong context):
1. Tên client
2. Ngày họp
3. Link Google Docs biên bản
4. Nội dung trao đổi (tóm tắt 2-3 ý chính)
5. Next steps (việc, PIC, deadline)

Hỏi thêm user nếu chưa rõ:
6. Email người nhận
7. Đây là khách hàng mới hay đã họp định kỳ nhiều lần? (để chọn mẫu phù hợp)
8. Số lượng next steps cần khách hàng theo dõi có nhiều/quan trọng không? (để cân nhắc dùng mẫu nhấn mạnh action items)

## Bước 2 — Chọn mẫu email

| Tình huống | Dùng mẫu |
|-----------|----------|
| Khách hàng mới, họp lần đầu/quan trọng | **Mẫu A — Chuẩn/đầy đủ** |
| Khách quen, họp định kỳ, ít next steps | **Mẫu B — Ngắn gọn** |
| Nhiều next steps quan trọng cần khách xác nhận theo dõi | **Mẫu C — Nhấn mạnh Action Items** |

### Mẫu A — Chuẩn/đầy đủ

```
Subject: [SEONGON] Biên bản họp <Dự án> ngày <DD/MM/YYYY>

Kính gửi Anh/Chị <Tên>,

Cảm ơn Anh/Chị đã dành thời gian trao đổi trong buổi họp ngày <DD/MM/YYYY> vừa qua.

Dưới đây là biên bản tóm tắt nội dung đã trao đổi và các đầu việc tiếp theo:

Nội dung trao đổi chính:
- <ý 1>
- <ý 2>
- <ý 3>

Next steps:
- <việc 1> — Phụ trách: <PIC> — Deadline: <ngày>
- <việc 2> — Phụ trách: <PIC> — Deadline: <ngày>

Biên bản chi tiết đầy đủ: <link Google Docs>

Anh/Chị vui lòng xem qua và phản hồi nếu có điều chỉnh hoặc bổ sung. Chúng tôi sẽ tiếp tục triển khai theo đúng kế hoạch đã thống nhất.

Trân trọng,
Đặng Ngọc Minh Thư
Account PM | SEONGON
📞 098.77.99.803
✉️ dnmthu1704@gmail.com
```

### Mẫu B — Ngắn gọn

```
Subject: [SEONGON] Recap họp <Dự án> - <DD/MM>

Chào Anh/Chị <Tên>,

Gửi Anh/Chị recap nhanh buổi họp hôm nay:
- <tóm tắt 1-2 ý chính>

Việc cần làm tiếp theo: <next step chính> — <PIC> — <deadline>

Chi tiết đầy đủ tại đây: <link Google Docs>

Cảm ơn Anh/Chị!

Đặng Ngọc Minh Thư
Account PM | SEONGON
📞 098.77.99.803
✉️ dnmthu1704@gmail.com
```

### Mẫu C — Nhấn mạnh Action Items

```
Subject: [SEONGON] Biên bản họp & Action Items - <Dự án> - <DD/MM/YYYY>

Kính gửi Anh/Chị <Tên>,

Biên bản họp ngày <DD/MM/YYYY> đã được tổng hợp, chi tiết đầy đủ tại link bên dưới.

Các action items cần lưu ý:
1. <Việc> — PIC: <ai> — Hạn: <ngày>
2. <Việc> — PIC: <ai> — Hạn: <ngày>
3. <Việc> — PIC: <ai> — Hạn: <ngày>

Anh/Chị vui lòng xác nhận giúp các đầu việc trên để hai bên cùng theo dõi tiến độ.

Link biên bản đầy đủ: <link Google Docs>

Trân trọng,
Đặng Ngọc Minh Thư
Account PM | SEONGON
📞 098.77.99.803
✉️ dnmthu1704@gmail.com
```

## Bước 3 — Xác nhận trước khi gửi

Điền nội dung mẫu đã chọn với thông tin thật, hiện cho user xem:
> Đây là nội dung email sẽ gửi đến [email]:
> [nội dung email đầy đủ]
>
> Bạn muốn **gửi ngay** hay **chỉnh sửa** gì không?

CHỈ gửi khi user xác nhận "gửi" hoặc "ok".

## Bước 4 — Gửi và lưu

Dùng script gửi email của skill `send-email-report`:

```
python3 /Users/dnmthw/Downloads/claude-code-workspace/.claude/skills/send-email-report/send_email.py \
  --to "<email_client>" \
  --client "<tên client>" \
  --month "<biên bản họp DD/MM/YYYY>" \
  --highlights "<ý 1>|<ý 2>|<next step chính>"
```

Lưu bản nháp email vào `outputs/meeting-email-<client>-<DD-MM-YYYY>.txt`

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|-----|------------|
| Chưa có link Google Docs biên bản | Chạy `meeting-notes` trước |
| Không rõ chọn mẫu nào | Mặc định dùng Mẫu A (chuẩn/đầy đủ) |
| Authentication failed khi gửi | Xem phần Setup của skill `send-email-report` |
