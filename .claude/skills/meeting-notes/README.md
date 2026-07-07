# meeting-notes

Chuyển ghi chú thô sau buổi họp → biên bản họp chuẩn dạng .docx.

## Cách dùng

Gõ `/meeting-notes` trong Claude Code, sau đó cung cấp ghi chú thô.

## Output

File `outputs/bien-ban-hop-<client>-<date>.docx` gồm:
- Thông tin buổi họp
- Nội dung thảo luận
- Các quyết định đã chốt
- Action items (Nội dung | PIC | Deadline)

## Setup (tùy chọn)

Thêm `anthropic_api_key` vào `config.json` để dùng Claude AI phân tích thông minh hơn.
Nếu không có key, script vẫn chạy được với parser cơ bản.

## Cài thư viện

```bash
pip3 install python-docx
```
