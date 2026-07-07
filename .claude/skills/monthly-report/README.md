# monthly-report

Nhận file Excel/CSV data SEO → tạo báo cáo SEO tháng dạng .docx.

## Cách dùng

Gõ `/monthly-report` trong Claude Code, đính kèm file Excel data.

## Hỗ trợ file đầu vào

- Export từ Google Search Console (.csv)
- Export từ SemRush / Ahrefs / Keyword tool (.xlsx, .csv)
- File tracking ranking tự tạo (.xlsx)

## Output

File `outputs/bao-cao-seo-<client>-thang-<MM>-<YYYY>.docx` gồm:
- Tổng quan (tổng KW, Top 10, Top 3, clicks)
- Phân bổ từ khóa theo vị trí
- Top từ khóa nổi bật
- Phân tích & đánh giá
- Kế hoạch tháng sau

## Cài thư viện

```bash
pip3 install openpyxl python-docx
```
