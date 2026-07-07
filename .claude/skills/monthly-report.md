---
name: monthly-report
description: Tạo báo cáo SEO tháng từ file Excel/CSV data → xuất ra file .docx gửi client
---

# Monthly SEO Report

## Mục tiêu
Đọc file data SEO (ranking, traffic, conversions) và tự động tạo báo cáo tháng theo template SEONGON, lưu ra file .docx.

## Cách dùng
```
/monthly-report
```
Sau đó cung cấp:
- File Excel/CSV chứa data ranking hoặc GSC
- Tên client
- Tháng báo cáo

## Các bước Claude sẽ thực hiện
1. Đọc file data đầu vào
2. Tính toán các chỉ số: tổng từ khóa Top 10, traffic tháng, so sánh tháng trước
3. Tóm tắt highlights và điểm cần cải thiện
4. Xuất báo cáo ra file .docx theo cấu trúc: Tổng quan → Kết quả → Phân tích → Kế hoạch tháng sau

## Output
- File `bao-cao-seo-[client]-thang-[MM]-[YYYY].docx`
