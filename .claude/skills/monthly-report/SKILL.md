---
name: monthly-report
description: Nhận file data thô + config dự án → tự tạo slide báo cáo tháng → đẩy lên Google Slides. Kích hoạt khi user nói "tạo báo cáo tháng", "monthly report", "làm slide báo cáo", hoặc đưa file data dự án.
---

# Monthly Report — Google Slides Generator

Nhận thông tin dự án + file data thô → tạo Google Slides báo cáo tháng chuẩn SEONGON.

## Bước 1 — Thu thập thông tin

Hỏi user lần lượt (hoặc đọc từ project-config.json nếu đã có):

1. **Tên dự án / client** (vd: TMA Solutions, Vĩnh Tường...)
2. **Tháng báo cáo** (MM/YYYY)
3. **Ngành hàng** (vd: IT outsourcing, vật liệu xây dựng...)
4. **Màu chủ đạo** (hex code hoặc mô tả — vd: #1A73E8 xanh dương, #E8341A đỏ cam)
5. **Phong cách slide** (chuyên nghiệp / tối giản / sáng tạo)
6. **Thứ tự các mục báo cáo** (vd: Tổng quan → Ranking → Traffic → Phân tích → Kế hoạch)
7. **File data** (Excel/CSV ranking, traffic, hoặc export từ GSC/SemRush)

Nếu đã có file `project-config.json` trong thư mục outputs/, đọc và bỏ qua các câu hỏi đã có.

## Bước 2 — Đọc và phân tích file data

```
python3 /Users/dnmthw/Downloads/claude-code-workspace/.claude/skills/monthly-report/generate_slides.py \
  --preview --file "<đường dẫn file>"
```

Báo cho user biết đã nhận diện được những cột/dữ liệu gì.

## Bước 3 — Tạo Google Slides

```
python3 /Users/dnmthw/Downloads/claude-code-workspace/.claude/skills/monthly-report/generate_slides.py \
  --file "<đường dẫn file data>" \
  --client "<tên client>" \
  --month "<MM/YYYY>" \
  --industry "<ngành hàng>" \
  --color "<hex màu chủ đạo, vd: 1A73E8>" \
  --style "<professional|minimal|creative>" \
  --sections "<Tổng quan|Ranking|Traffic|Phân tích|Kế hoạch tháng sau>"
```

Script sẽ:
1. Đọc file data → tính toán chỉ số
2. Tạo Google Slides presentation qua API
3. Điền nội dung vào từng slide theo thứ tự mục
4. Trả về link Google Slides

## Bước 4 — Trả kết quả

> Đã tạo báo cáo tháng MM/YYYY cho [client]:
> Link Google Slides: [link]
> Gồm: X slides, Y từ khóa Top 10, traffic Z clicks

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|-----|------------|
| `ModuleNotFoundError` | `pip3 install openpyxl pandas google-api-python-client` |
| Slides API chưa bật | Vào console.cloud.google.com → Enable Google Slides API |
| Token hết hạn | Xoá token.json, chạy lại để re-auth |
