#!/usr/bin/env python3
"""
meeting-notes/format_notes.py
Nhận ghi chú thô → tạo biên bản họp chuẩn → xuất file .docx

Cách dùng:
    python3 format_notes.py --client "TMA Solutions" --date "07-07-2026" \
        --attendees "Minh Thư (PM), Anh Khoa (SEO)" \
        --notes "bàn content tháng 7, Thư làm brief deadline 10/7..." \
        --out outputs/bien-ban-hop-TMA-07-07-2026.docx
"""

import argparse
import json
import os
import sys
import re
import urllib.request
import urllib.error
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")


def load_config():
    cfg = {"anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", "")}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    return cfg


def call_claude(prompt, api_key):
    """Gọi Claude API để phân tích và format ghi chú."""
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise SystemExit(f"[x] Claude API lỗi {e.code}: {body[:300]}")
    except urllib.error.URLError as e:
        raise SystemExit(f"[x] Lỗi mạng: {e.reason}")


def parse_structured(text):
    """Parse JSON từ response của Claude."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def format_with_claude(raw_notes, client, date, attendees, api_key):
    """Dùng Claude để phân tích ghi chú thô → JSON có cấu trúc."""
    prompt = f"""Bạn là trợ lý chuyên format biên bản họp cho công ty SEO.

Ghi chú thô từ buổi họp:
---
{raw_notes}
---

Thông tin buổi họp:
- Client / Dự án: {client}
- Ngày họp: {date}
- Thành phần tham dự: {attendees}

Hãy phân tích ghi chú trên và trả về JSON theo đúng format sau (không giải thích thêm):
{{
  "tieu_de": "Biên bản họp - {client} - {date}",
  "noi_dung_thao_luan": [
    "Nội dung 1",
    "Nội dung 2"
  ],
  "quyet_dinh": [
    "Quyết định 1",
    "Quyết định 2"
  ],
  "action_items": [
    {{"noi_dung": "Việc cần làm", "pic": "Người phụ trách", "deadline": "DD/MM/YYYY"}},
    {{"noi_dung": "Việc cần làm 2", "pic": "Người phụ trách", "deadline": "DD/MM/YYYY"}}
  ],
  "ghi_chu": "Ghi chú bổ sung nếu có (để trống nếu không có)"
}}

Lưu ý:
- Nếu ghi chú không đề cập deadline cụ thể, ghi "Thỏa thuận"
- Nếu không rõ PIC, ghi "Cần xác nhận"
- Tóm tắt ngắn gọn, súc tích, dùng tiếng Việt"""

    response = call_claude(prompt, api_key)
    parsed = parse_structured(response)
    if not parsed:
        # Fallback: tạo cấu trúc mặc định
        return {
            "tieu_de": f"Biên bản họp - {client} - {date}",
            "noi_dung_thao_luan": [raw_notes[:500]],
            "quyet_dinh": ["Xem ghi chú đính kèm"],
            "action_items": [{"noi_dung": "Xác nhận lại với team", "pic": "PM", "deadline": "Thỏa thuận"}],
            "ghi_chu": "Ghi chú thô đính kèm bên dưới:\n" + raw_notes,
        }
    return parsed


def format_manual(raw_notes, client, date, attendees):
    """Fallback khi không có API key: tạo cấu trúc từ keyword đơn giản."""
    lines = [l.strip() for l in raw_notes.strip().splitlines() if l.strip()]
    action_items = []
    discussion = []
    decisions = []

    action_keywords = ["deadline", "làm", "gửi", "hoàn thành", "chuẩn bị", "tạo", "viết", "check", "review"]
    decision_keywords = ["chốt", "quyết định", "đồng ý", "thống nhất", "approved", "ok"]

    for line in lines:
        line_lower = line.lower()
        if any(k in line_lower for k in decision_keywords):
            decisions.append(line.lstrip("-•* "))
        elif any(k in line_lower for k in action_keywords):
            action_items.append({"noi_dung": line.lstrip("-•* "), "pic": "Cần xác nhận", "deadline": "Thỏa thuận"})
        else:
            discussion.append(line.lstrip("-•* "))

    if not discussion:
        discussion = ["Xem ghi chú chi tiết bên dưới"]
    if not decisions:
        decisions = ["Chưa có quyết định cụ thể"]
    if not action_items:
        action_items = [{"noi_dung": "Xác nhận lại action items với team", "pic": "PM", "deadline": "Thỏa thuận"}]

    return {
        "tieu_de": f"Biên bản họp - {client} - {date}",
        "noi_dung_thao_luan": discussion,
        "quyet_dinh": decisions,
        "action_items": action_items,
        "ghi_chu": "",
    }


def write_docx(data, client, date, attendees, out_path):
    """Xuất biên bản họp ra file .docx."""
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        raise SystemExit("[x] Thiếu thư viện python-docx. Chạy: pip3 install python-docx")

    doc = Document()

    # Tiêu đề
    title = doc.add_heading(data["tieu_de"], 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Thông tin chung
    doc.add_heading("I. THÔNG TIN BUỔI HỌP", level=1)
    info_table = doc.add_table(rows=3, cols=2)
    info_table.style = "Table Grid"
    cells = [
        ("Ngày họp", date),
        ("Client / Dự án", client),
        ("Thành phần tham dự", attendees),
    ]
    for i, (label, value) in enumerate(cells):
        info_table.rows[i].cells[0].text = label
        info_table.rows[i].cells[1].text = value
        run = info_table.rows[i].cells[0].paragraphs[0].runs[0]
        run.bold = True

    doc.add_paragraph()

    # Nội dung thảo luận
    doc.add_heading("II. NỘI DUNG THẢO LUẬN", level=1)
    for i, item in enumerate(data["noi_dung_thao_luan"], 1):
        doc.add_paragraph(f"{i}. {item}", style="List Number")

    doc.add_paragraph()

    # Quyết định
    doc.add_heading("III. CÁC QUYẾT ĐỊNH ĐÃ CHỐT", level=1)
    for item in data["quyet_dinh"]:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_paragraph()

    # Action items table
    doc.add_heading("IV. ACTION ITEMS", level=1)
    action_table = doc.add_table(rows=1, cols=4)
    action_table.style = "Table Grid"
    headers = ["STT", "Nội dung công việc", "PIC", "Deadline"]
    for i, h in enumerate(headers):
        cell = action_table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True

    for idx, item in enumerate(data["action_items"], 1):
        row = action_table.add_row()
        row.cells[0].text = str(idx)
        row.cells[1].text = item.get("noi_dung", "")
        row.cells[2].text = item.get("pic", "")
        row.cells[3].text = item.get("deadline", "")

    # Ghi chú
    if data.get("ghi_chu"):
        doc.add_paragraph()
        doc.add_heading("V. GHI CHÚ BỔ SUNG", level=1)
        doc.add_paragraph(data["ghi_chu"])

    # Footer
    doc.add_paragraph()
    footer_para = doc.add_paragraph(
        f"Biên bản được tạo tự động bởi Claude Code | {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_para.runs[0].font.size = Pt(9)

    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    doc.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Format ghi chú họp → biên bản .docx")
    ap.add_argument("--client", required=True, help="Tên client hoặc dự án")
    ap.add_argument("--date", required=True, help="Ngày họp DD-MM-YYYY")
    ap.add_argument("--attendees", required=True, help="Thành phần tham dự")
    ap.add_argument("--notes", default="", help="Ghi chú thô (paste trực tiếp)")
    ap.add_argument("--notes-file", help="File chứa ghi chú thô")
    ap.add_argument("--out", default="bien-ban-hop.docx", help="File output .docx")
    args = ap.parse_args()

    # Đọc ghi chú
    raw_notes = args.notes
    if args.notes_file:
        with open(args.notes_file, "r", encoding="utf-8") as f:
            raw_notes = f.read()
    if not raw_notes.strip():
        raise SystemExit("[x] Chưa có ghi chú. Dùng --notes hoặc --notes-file.")

    cfg = load_config()
    api_key = cfg.get("anthropic_api_key", "")

    print(f"[i] Client: {args.client} | Ngày: {args.date}")
    print(f"[i] Thành phần: {args.attendees}")

    if api_key:
        print("[i] Phân tích ghi chú bằng Claude AI...")
        data = format_with_claude(raw_notes, args.client, args.date, args.attendees, api_key)
    else:
        print("[!] Không có API key → dùng parser cơ bản (thêm anthropic_api_key vào config.json để dùng AI)")
        data = format_manual(raw_notes, args.client, args.date, args.attendees)

    print("[i] Xuất file .docx...")
    out_path = write_docx(data, args.client, args.date, args.attendees, args.out)

    print(f"[✓] Đã tạo: {out_path}")
    print(f"    → {len(data['noi_dung_thao_luan'])} nội dung thảo luận")
    print(f"    → {len(data['quyet_dinh'])} quyết định")
    print(f"    → {len(data['action_items'])} action items")


if __name__ == "__main__":
    main()
