---
name: meeting-notes
description: Chuyển ghi chú thô sau buổi họp → biên bản họp chuẩn có task, PIC và deadline. Kích hoạt khi user nói "format biên bản", "tạo biên bản họp", "meeting notes", hoặc paste ghi chú họp thô vào.
---

# Meeting Notes Formatter

Skill này nhận ghi chú thô (bullet points, text rối) sau buổi họp → format thành biên bản họp
chuyên nghiệp → xuất file .docx.

## Bước 1 — Thu thập thông tin

Nếu user chưa cung cấp, hỏi lần lượt:

> Bạn cung cấp cho mình:
> 1. Ghi chú thô của buổi họp (paste trực tiếp)
> 2. Tên client / dự án
> 3. Ngày họp (DD/MM/YYYY)
> 4. Thành phần tham dự (tên + vai trò)

Nếu user đã paste ghi chú, chỉ hỏi những thông tin còn thiếu.

## Bước 2 — Phân tích ghi chú

Đọc kỹ ghi chú thô và phân loại thành 4 nhóm:
- **Thông tin chung**: thời gian, địa điểm, thành phần
- **Nội dung thảo luận**: các vấn đề đã bàn
- **Quyết định**: các kết luận đã chốt
- **Action items**: việc cần làm, ai làm, deadline

## Bước 3 — Chạy script

```
python3 ~/.claude/skills/meeting-notes/format_notes.py \
  --client "<tên client>" \
  --date "<DD-MM-YYYY>" \
  --attendees "<người 1>, <người 2>" \
  --notes "<ghi chú thô>" \
  --out outputs/bien-ban-hop-<client>-<DD-MM-YYYY>.docx
```

Nếu ghi chú thô dài, lưu vào file tạm trước:
```
python3 ~/.claude/skills/meeting-notes/format_notes.py \
  --client "<tên client>" \
  --date "<DD-MM-YYYY>" \
  --attendees "<người 1>, <người 2>" \
  --notes-file /tmp/notes.txt \
  --out outputs/bien-ban-hop-<client>-<DD-MM-YYYY>.docx
```

## Bước 4 — Kiểm tra và báo kết quả

Trước khi báo xong, kiểm tra:
- [ ] File .docx đã tạo thành công (dùng `ls -lh` kiểm tra)
- [ ] Có đủ 4 phần: thông tin chung, nội dung, quyết định, action items
- [ ] Action items có đủ: Nội dung | PIC | Deadline

Báo kết quả:
> Đã tạo biên bản họp: `outputs/bien-ban-hop-<client>-<date>.docx`
> Tóm tắt: X nội dung thảo luận, Y quyết định, Z action items.

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `ModuleNotFoundError: docx` | Chưa cài python-docx | Chạy `pip3 install python-docx` |
| File rỗng | Ghi chú không có action items | Báo user bổ sung, không xuất file thiếu |
| Encoding lỗi | Ký tự tiếng Việt | Script đã xử lý UTF-8, nếu vẫn lỗi thử `--notes-file` |
