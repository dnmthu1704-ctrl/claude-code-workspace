---
name: meeting-notes
description: Nhận recap thô sau buổi họp → hệ thống hoá, viết lại chuyên nghiệp → xuất Google Docs gồm 2 phần: Nội dung trao đổi + Next steps (công việc, PIC, deadline). Kích hoạt khi user paste recap họp thô vào.
---

# Meeting Notes Formatter

Nhận recap thô → phân loại, viết lại → xuất Google Docs với 2 phần chuẩn.

## Bước 1 — Thu thập thông tin

Nếu user đã paste recap, chỉ hỏi những gì còn thiếu:

- Tên client / dự án
- Ngày họp (DD/MM/YYYY)
- Thành phần tham dự (tên + vai trò)

## Bước 2 — Phân tích recap thô

Đọc kỹ và phân loại thành 2 nhóm:

**Phần 1 — Nội dung trao đổi**
- Tóm tắt các vấn đề đã thảo luận theo từng mảng (GEO, CRO, SEO...)
- Viết lại súc tích, rõ ràng, chuyên nghiệp
- Bỏ các icon thừa (@mention, emoji trang trí)
- Giữ các thông tin quan trọng: quyết định, lưu ý, rủi ro

**Phần 2 — Next steps**
- Liệt kê từng việc cần làm
- Xác định PIC (người thực hiện)
- Xác định Deadline

## Bước 3 — Chạy script

Lưu recap thô vào file tạm rồi chạy:

```
python3 /Users/dnmthw/Downloads/claude-code-workspace/.claude/skills/meeting-notes/format_notes.py \
  --client "<tên client>" \
  --date "<DD-MM-YYYY>" \
  --attendees "<người 1 (vai trò), người 2 (vai trò)>" \
  --notes-file /tmp/notes.txt \
  --out /Users/dnmthw/Downloads/claude-code-workspace/outputs/recap-<client>-<DD-MM-YYYY>.docx
```

Sau khi tạo .docx xong, upload lên Google Drive:

```
python3 /Users/dnmthw/Downloads/claude-code-workspace/drive_upload.py \
  /Users/dnmthw/Downloads/claude-code-workspace/outputs/recap-<client>-<DD-MM-YYYY>.docx
```

## Bước 4 — Trả kết quả

Báo kết quả với:
- Link Google Docs
- Tóm tắt: X nội dung trao đổi, Y next steps

Ví dụ:
> Đã tạo recap: [Link Google Docs]
> Gồm: 4 mảng nội dung trao đổi, 7 next steps có PIC và deadline.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|-----|------------|
| `ModuleNotFoundError: docx` | `pip3 install python-docx` |
| Upload Drive lỗi auth | Xoá token.json và chạy lại |
| Encoding lỗi tiếng Việt | Dùng `--notes-file` thay vì `--notes` |
