#!/usr/bin/env python3
"""
generate_slides.py — Đọc file data SEO → tạo Google Slides báo cáo tháng.

Cách dùng:
    # Xem trước cấu trúc file
    python3 generate_slides.py --preview --file data.xlsx

    # Tạo slides
    python3 generate_slides.py \
        --file data.xlsx \
        --client "TMA Solutions" \
        --month "07/2026" \
        --industry "IT Outsourcing" \
        --color "1A73E8" \
        --style professional \
        --sections "Tổng quan|Ranking|Traffic|Phân tích|Kế hoạch tháng sau"
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CREDENTIALS_PATH = os.path.join(WORKSPACE, "credentials.json")
TOKEN_PATH = os.path.join(WORKSPACE, "token.json")

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive.file",
]


# ── Auth ────────────────────────────────────────────────────────────────────

def get_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


# ── Data reading ─────────────────────────────────────────────────────────────

def read_data(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        import pandas as pd
    except ImportError:
        sys.exit("[x] Thiếu pandas: pip3 install pandas openpyxl")

    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path)
    elif ext == ".csv":
        for enc in ("utf-8", "utf-8-sig", "cp1252"):
            try:
                df = pd.read_csv(file_path, encoding=enc)
                break
            except UnicodeDecodeError:
                continue
    else:
        sys.exit(f"[x] Định dạng không hỗ trợ: {ext}")

    return df


def detect_columns(df):
    col_map = {}
    for col in df.columns:
        c = col.lower().strip()
        if any(k in c for k in ["keyword", "từ khóa", "tu khoa", "query"]):
            col_map["keyword"] = col
        elif any(k in c for k in ["position", "rank", "vị trí", "vi tri", "pos"]):
            col_map["position"] = col
        elif any(k in c for k in ["click", "lượt"]):
            col_map["clicks"] = col
        elif any(k in c for k in ["impression", "hiển thị"]):
            col_map["impressions"] = col
        elif any(k in c for k in ["url", "page", "trang"]):
            col_map["url"] = col
    return col_map


def compute_stats(df, col_map, top_n=10):
    stats = {"total_keywords": len(df)}

    if "position" in col_map:
        pos_col = col_map["position"]
        df[pos_col] = df[pos_col].apply(lambda x: float(str(x).replace(",", ".")) if str(x).replace(",", ".").replace(".", "").isdigit() else 999)
        stats["top10_count"] = int((df[pos_col] <= 10).sum())
        stats["top3_count"] = int((df[pos_col] <= 3).sum())
        stats["avg_position"] = round(df[pos_col][df[pos_col] < 999].mean(), 1)

        top_kw = df[df[pos_col] <= top_n].copy()
        if "keyword" in col_map:
            top_kw = top_kw.sort_values(pos_col).head(10)
            stats["top_keywords"] = [
                {"keyword": str(row[col_map["keyword"]]), "position": int(row[pos_col])}
                for _, row in top_kw.iterrows()
            ]

    if "clicks" in col_map:
        stats["total_clicks"] = int(df[col_map["clicks"]].sum())
    if "impressions" in col_map:
        stats["total_impressions"] = int(df[col_map["impressions"]].sum())
        if "clicks" in col_map:
            stats["ctr"] = round(stats["total_clicks"] / stats["total_impressions"] * 100, 2) if stats["total_impressions"] > 0 else 0

    return stats


# ── Google Slides builder ───────────────────────────────────────────────────

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return {"red": r / 255, "green": g / 255, "blue": b / 255}


def pt(n):
    """Convert points to EMU (for size dimensions)."""
    return {"magnitude": n, "unit": "PT"}

def emu(n):
    """Convert points to EMU number (for transform coordinates)."""
    return n * 12700


def make_text_request(obj_id, text, bold=False, font_size=18, color=None, align="LEFT"):
    requests = [
        {"insertText": {"objectId": obj_id, "text": text}},
        {"updateTextStyle": {
            "objectId": obj_id,
            "style": {
                "bold": bold,
                "fontSize": pt(font_size),
                **({"foregroundColor": {"opaqueColor": {"rgbColor": hex_to_rgb(color)}}} if color else {}),
            },
            "fields": "bold,fontSize" + (",foregroundColor" if color else ""),
        }},
        {"updateParagraphStyle": {
            "objectId": obj_id,
            "style": {"alignment": "START" if align == "LEFT" else align},
            "fields": "alignment",
        }},
    ]
    return requests


def create_slide_with_title(slide_id, title, bg_color, title_color, subtitle=None):
    """Tạo slide với tiêu đề và màu nền."""
    import uuid
    title_id = f"title_{slide_id}"
    sub_id = f"sub_{slide_id}"

    requests = [
        {"createSlide": {
            "objectId": slide_id,
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
        }},
        # Màu nền slide
        {"updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {
                "pageBackgroundFill": {
                    "solidFill": {"color": {"rgbColor": hex_to_rgb(bg_color)}}
                }
            },
            "fields": "pageBackgroundFill",
        }},
        # Title box
        {"createShape": {
            "objectId": title_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": {"width": pt(600), "height": pt(80)},
                "transform": {"scaleX": 1, "scaleY": 1, "translateX": emu(30), "translateY": emu(30), "unit": "EMU"},
            },
        }},
        *make_text_request(title_id, title, bold=True, font_size=28, color=title_color, align="LEFT"),
    ]

    if subtitle:
        requests += [
            {"createShape": {
                "objectId": sub_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {"width": pt(600), "height": pt(40)},
                    "transform": {"scaleX": 1, "scaleY": 1, "translateX": emu(30), "translateY": emu(110), "unit": "EMU"},
                },
            }},
            *make_text_request(sub_id, subtitle, bold=False, font_size=14, color="FFFFFF", align="LEFT"),
        ]

    return requests


def create_content_slide(slide_id, title, lines, main_color, text_color="333333"):
    """Tạo slide nội dung với bullet points."""
    title_id = f"ctitle_{slide_id}"
    body_id = f"cbody_{slide_id}"

    body_text = "\n".join(f"• {line}" for line in lines)

    requests = [
        {"createSlide": {
            "objectId": slide_id,
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
        }},
        {"updatePageProperties": {
            "objectId": slide_id,
            "pageProperties": {
                "pageBackgroundFill": {"solidFill": {"color": {"rgbColor": hex_to_rgb("FFFFFF")}}}
            },
            "fields": "pageBackgroundFill",
        }},
        # Thanh màu trên đầu
        {"createShape": {
            "objectId": f"bar_{slide_id}",
            "shapeType": "RECTANGLE",
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": {"width": pt(660), "height": pt(8)},
                "transform": {"scaleX": 1, "scaleY": 1, "translateX": emu(0), "translateY": emu(0), "unit": "EMU"},
            },
        }},
        {"updateShapeProperties": {
            "objectId": f"bar_{slide_id}",
            "shapeProperties": {
                "shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": hex_to_rgb(main_color)}}},
            },
            "fields": "shapeBackgroundFill",
        }},
        # Title
        {"createShape": {
            "objectId": title_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": {"width": pt(600), "height": pt(50)},
                "transform": {"scaleX": 1, "scaleY": 1, "translateX": emu(30), "translateY": emu(20), "unit": "EMU"},
            },
        }},
        *make_text_request(title_id, title, bold=True, font_size=22, color=main_color),
        # Body
        {"createShape": {
            "objectId": body_id,
            "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": {"width": pt(600), "height": pt(280)},
                "transform": {"scaleX": 1, "scaleY": 1, "translateX": emu(30), "translateY": emu(80), "unit": "EMU"},
            },
        }},
        *make_text_request(body_id, body_text, font_size=13, color=text_color),
    ]
    return requests


def build_presentation(client, month, industry, color, style, sections, stats):
    """Xây dựng toàn bộ presentation requests."""
    import uuid
    all_requests = []

    title_colors = {
        "professional": ("FFFFFF", color),
        "minimal": (color, "FFFFFF"),
        "creative": ("FFFFFF", color),
    }
    bg_c, title_c = title_colors.get(style, ("FFFFFF", color))

    # Slide 1: Trang bìa
    cover_id = "slide_cover"
    all_requests += create_slide_with_title(
        cover_id,
        f"BÁO CÁO SEO THÁNG {month}",
        color,
        "FFFFFF",
        subtitle=f"{client.upper()}  |  {industry}",
    )

    # Slide cho từng mục
    section_content = build_section_content(sections, stats, client, month)
    for i, (section_title, lines) in enumerate(section_content):
        slide_id = f"slide_{i+1}"
        all_requests += create_content_slide(slide_id, section_title, lines, color)

    return all_requests


def build_section_content(sections, stats, client, month):
    """Tạo nội dung cho từng section dựa trên stats."""
    section_list = [s.strip() for s in sections.split("|")]
    result = []

    for sec in section_list:
        sec_lower = sec.lower()

        if any(k in sec_lower for k in ["tổng quan", "overview", "tong quan"]):
            lines = [
                f"Client: {client}",
                f"Tháng báo cáo: {month}",
                f"Tổng từ khóa theo dõi: {stats.get('total_keywords', 'N/A')}",
                f"Từ khóa Top 10: {stats.get('top10_count', 'N/A')}",
                f"Từ khóa Top 3: {stats.get('top3_count', 'N/A')}",
                f"Vị trí trung bình: {stats.get('avg_position', 'N/A')}",
            ]
            result.append((sec, lines))

        elif any(k in sec_lower for k in ["ranking", "từ khóa", "tu khoa", "xếp hạng"]):
            lines = [f"Tổng từ khóa: {stats.get('total_keywords', 'N/A')}"]
            lines.append(f"Top 10: {stats.get('top10_count', 'N/A')} từ khóa")
            lines.append(f"Top 3: {stats.get('top3_count', 'N/A')} từ khóa")
            top_kws = stats.get("top_keywords", [])
            if top_kws:
                lines.append("")
                lines.append("Top từ khóa nổi bật:")
                for kw in top_kws[:5]:
                    lines.append(f"  #{kw['position']}  {kw['keyword']}")
            result.append((sec, lines))

        elif any(k in sec_lower for k in ["traffic", "lưu lượng"]):
            lines = [
                f"Tổng clicks: {stats.get('total_clicks', 'N/A'):,}" if isinstance(stats.get('total_clicks'), int) else f"Tổng clicks: {stats.get('total_clicks', 'N/A')}",
                f"Tổng impressions: {stats.get('total_impressions', 'N/A'):,}" if isinstance(stats.get('total_impressions'), int) else f"Tổng impressions: {stats.get('total_impressions', 'N/A')}",
                f"CTR trung bình: {stats.get('ctr', 'N/A')}%",
            ]
            result.append((sec, lines))

        elif any(k in sec_lower for k in ["phân tích", "phan tich", "nhận xét"]):
            lines = [
                "Điểm mạnh tháng này:",
                f"  • Từ khóa Top 10 đạt {stats.get('top10_count', 0)} — duy trì ổn định",
                "Điểm cần cải thiện:",
                "  • Tăng cường nội dung cho từ khóa vị trí 11-20",
                "  • Tối ưu CTA để cải thiện CTR",
                "Đánh giá chung: Đang trong lộ trình kế hoạch đề ra",
            ]
            result.append((sec, lines))

        elif any(k in sec_lower for k in ["kế hoạch", "ke hoach", "tháng sau", "next"]):
            lines = [
                "Tiếp tục triển khai theo kế hoạch đã đề ra",
                "Đẩy mạnh nội dung cho các từ khóa tiềm năng",
                "Theo dõi và tối ưu các từ khóa vị trí 11-20",
                "Báo cáo kết quả vào đầu tháng sau",
            ]
            result.append((sec, lines))

        else:
            result.append((sec, [f"Nội dung phần {sec} — cập nhật sau"]))

    return result


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Tạo Google Slides báo cáo SEO tháng")
    ap.add_argument("--file", default="", help="File data SEO (.xlsx hoặc .csv)")
    ap.add_argument("--client", default="Client", help="Tên client")
    ap.add_argument("--month", default="", help="Tháng báo cáo (MM/YYYY)")
    ap.add_argument("--industry", default="SEO", help="Ngành hàng")
    ap.add_argument("--color", default="1A73E8", help="Màu chủ đạo (hex, không có #)")
    ap.add_argument("--style", default="professional", choices=["professional", "minimal", "creative"])
    ap.add_argument("--sections", default="Tổng quan|Ranking|Traffic|Phân tích|Kế hoạch tháng sau")
    ap.add_argument("--preview", action="store_true", help="Chỉ xem cấu trúc file, không tạo slides")
    args = ap.parse_args()

    # Preview mode
    if args.preview:
        if not args.file:
            sys.exit("[x] Cần --file để xem preview")
        df = read_data(args.file)
        col_map = detect_columns(df)
        print(f"[i] File: {args.file}")
        print(f"[i] Số dòng: {len(df)}")
        print(f"[i] Các cột: {list(df.columns)}")
        print(f"[i] Nhận diện: {col_map}")
        return

    # Đọc và tính toán data
    stats = {}
    if args.file and os.path.exists(args.file):
        print(f"[i] Đọc file: {args.file}")
        df = read_data(args.file)
        col_map = detect_columns(df)
        stats = compute_stats(df, col_map)
        print(f"[i] Tổng từ khóa: {stats.get('total_keywords')} | Top10: {stats.get('top10_count')} | Top3: {stats.get('top3_count')}")
    else:
        print("[i] Không có file data — tạo slides với nội dung mẫu")

    # Kết nối Google Slides API
    print("[i] Kết nối Google Slides API...")
    import warnings
    warnings.filterwarnings("ignore")

    from googleapiclient.discovery import build
    creds = get_credentials()
    slides_svc = build("slides", "v1", credentials=creds)
    drive_svc = build("drive", "v3", credentials=creds)

    # Tạo presentation mới
    title = f"Báo cáo SEO {args.month} — {args.client}"
    prs = slides_svc.presentations().create(body={"title": title}).execute()
    prs_id = prs["presentationId"]
    print(f"[i] Đã tạo presentation: {prs_id}")

    # Xoá slide mặc định
    default_slide_id = prs["slides"][0]["objectId"]

    # Build requests
    requests = [{"deleteObject": {"objectId": default_slide_id}}]
    requests += build_presentation(
        args.client, args.month, args.industry,
        args.color, args.style, args.sections, stats
    )

    # Batch update
    slides_svc.presentations().batchUpdate(
        presentationId=prs_id,
        body={"requests": requests}
    ).execute()

    # Lấy link
    link = f"https://docs.google.com/presentation/d/{prs_id}/edit"
    print(f"[✓] Đã tạo Google Slides thành công!")
    print(f"    Link: {link}")
    return link


if __name__ == "__main__":
    main()
