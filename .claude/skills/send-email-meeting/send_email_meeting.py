#!/usr/bin/env python3
"""
send-email-meeting/send_email_meeting.py
Soạn và gửi email biên bản họp (meeting recap) qua Gmail (SMTP + App Password).
Dùng chung cấu hình Gmail với skill send-email-report.

Cách dùng:
    # Xem nháp trước khi gửi
    python3 send_email_meeting.py --to "client@example.com" \
        --recipient-name "Thư" --client "FPTU HO" --date "09/07/2026" \
        --items "Viết outline cụm AI Agent|Thư|15/07;;Thêm CTA footer|Kỹ thuật|12/07" \
        --link "https://docs.google.com/document/d/xxx" \
        --draft-only

    # Gửi thật
    python3 send_email_meeting.py --to "client@example.com" \
        --recipient-name "Thư" --client "FPTU HO" --date "09/07/2026" \
        --items "Viết outline cụm AI Agent|Thư|15/07;;Thêm CTA footer|Kỹ thuật|12/07" \
        --link "https://docs.google.com/document/d/xxx"
"""

import argparse
import json
import os
import smtplib
import ssl
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HERE = os.path.dirname(os.path.abspath(__file__))
# Dùng chung config Gmail với skill send-email-report
CONFIG_PATH = os.path.join(HERE, "..", "send-email-report", "config.json")


def load_config():
    cfg = {
        "gmail_user": os.environ.get("GMAIL_USER", ""),
        "gmail_app_password": os.environ.get("GMAIL_APP_PASSWORD", ""),
        "sender_name": "SEONGON",
        "cc": "",
    }
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    return cfg


def parse_items(items_str):
    """Parse '--items' dạng 'việc|pic|hạn;;việc2|pic2|hạn2' thành list dict."""
    items = []
    if not items_str:
        return items
    for chunk in items_str.split(";;"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = [p.strip() for p in chunk.split("|")]
        task = parts[0] if len(parts) > 0 else ""
        pic = parts[1] if len(parts) > 1 else "Chưa xác định"
        deadline = parts[2] if len(parts) > 2 else "Chưa xác định"
        if task:
            items.append({"task": task, "pic": pic, "deadline": deadline})
    return items


def compose_email(recipient_name, client, date, items, link, sender_name):
    """Soạn nội dung email biên bản họp — Mẫu C (nhấn mạnh action items)."""
    if items:
        items_lines = "\n".join(
            f"{i}. {it['task']} — PIC: {it['pic']} — Hạn: {it['deadline']}"
            for i, it in enumerate(items, start=1)
        )
        items_block = f"""Team em xin tổng hợp lại các action items cần hai bên cùng lưu ý:

{items_lines}

Team em mong chị/anh xác nhận giúp các đầu việc trên để hai bên cùng theo dõi tiến độ ạ."""
    else:
        items_block = "Team em xin gửi lại biên bản để chị/anh và team tiện theo dõi ạ."

    link_line = f"\nBiên bản chi tiết đầy đủ: {link}\n" if link else ""

    body = f"""Dear chị/anh {recipient_name} và team {client},

SEONGON cảm ơn chị/anh {recipient_name} và team {client} đã trao đổi trong buổi họp ngày {date} ạ. {items_block}
{link_line}
SEONGON cảm ơn chị/anh {recipient_name} và team {client} đã phối hợp, hỗ trợ team trong giai đoạn vừa qua. Hy vọng hai bên sẽ tiếp tục phối hợp hiệu quả để đạt được các mục tiêu đã thống nhất ạ.

Trân trọng,
Đặng Ngọc Minh Thư
Account PM | {sender_name}
📞 098.77.99.803
✉️ dnmthu1704@gmail.com"""

    subject = f"[{sender_name}] Biên bản họp & Action Items - {client} - {date}"
    return subject, body


def build_message(from_email, to_email, cc, subject, body, sender_name):
    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{from_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc
    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg


def save_draft(subject, body, to_email, client):
    date_str = datetime.now().strftime("%d-%m-%Y")
    draft_path = f"outputs/meeting-email-{client.replace(' ', '-')}-{date_str}.txt"
    os.makedirs("outputs", exist_ok=True)
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(f"To: {to_email}\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("-" * 50 + "\n\n")
        f.write(body)
    return draft_path


def send_via_smtp(msg, gmail_user, app_password, to_email, cc):
    recipients = [to_email]
    if cc:
        recipients.extend([e.strip() for e in cc.split(",") if e.strip()])
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(gmail_user, app_password)
        server.sendmail(gmail_user, recipients, msg.as_string())


def main():
    ap = argparse.ArgumentParser(description="Gửi email biên bản họp qua Gmail")
    ap.add_argument("--to", required=True, help="Email người nhận (client)")
    ap.add_argument("--recipient-name", required=True, help="Tên người nhận (vd: Thư)")
    ap.add_argument("--client", required=True, help="Tên client/team (vd: FPTU HO)")
    ap.add_argument("--date", required=True, help="Ngày họp (vd: 09/07/2026)")
    ap.add_argument("--items", default="", help="Action items: 'việc|pic|hạn;;việc2|pic2|hạn2'")
    ap.add_argument("--link", default="", help="Link Google Docs biên bản")
    ap.add_argument("--cc", default="", help="Email CC (nếu có)")
    ap.add_argument("--draft-only", action="store_true", help="Chỉ tạo bản nháp, không gửi")
    args = ap.parse_args()

    cfg = load_config()
    sender_name = cfg.get("sender_name", "SEONGON")
    cc = args.cc or cfg.get("cc", "")

    items = parse_items(args.items)
    subject, body = compose_email(
        args.recipient_name, args.client, args.date, items, args.link, sender_name
    )

    print("\n" + "=" * 55)
    print("NỘI DUNG EMAIL:")
    print("=" * 55)
    print(f"To: {args.to}")
    print(f"Subject: {subject}")
    print("-" * 55)
    print(body)
    print("=" * 55 + "\n")

    draft_path = save_draft(subject, body, args.to, args.client)
    print(f"[✓] Đã lưu bản nháp: {draft_path}")

    if args.draft_only:
        print("[i] Chế độ --draft-only: không gửi email.")
        print("    → Xem lại nội dung, sau đó chạy lại không có --draft-only để gửi thật.")
        return

    gmail_user = cfg.get("gmail_user", "")
    app_password = cfg.get("gmail_app_password", "")
    if not gmail_user or not app_password:
        raise SystemExit(
            "[x] Chưa cấu hình Gmail.\n"
            "    Thêm 'gmail_user' và 'gmail_app_password' vào "
            "../send-email-report/config.json.\n"
            "    Hướng dẫn tạo App Password: myaccount.google.com → Security → App passwords"
        )

    print(f"[i] Đang gửi từ: {gmail_user} ...")
    msg = build_message(gmail_user, args.to, cc, subject, body, sender_name)

    try:
        send_via_smtp(msg, gmail_user, app_password, args.to, cc)
        print(f"[✓] Đã gửi email thành công đến: {args.to}")
        if cc:
            print(f"    CC: {cc}")
    except smtplib.SMTPAuthenticationError:
        raise SystemExit(
            "[x] Xác thực Gmail thất bại.\n"
            "    Kiểm tra lại gmail_user và gmail_app_password trong config.json."
        )
    except Exception as e:
        raise SystemExit(f"[x] Lỗi gửi email: {e}")


if __name__ == "__main__":
    main()
