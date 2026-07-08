#!/usr/bin/env python3
"""
send-email-report/send_email.py
Soạn và gửi email báo cáo SEO tháng qua Gmail (SMTP + App Password).

Cách dùng:
    # Xem nháp trước khi gửi
    python3 send_email.py --to "client@example.com" --client "TMA Solutions" \
        --month "07/2026" --attach outputs/bao-cao.docx \
        --highlights "Top 10 tăng 15 từ|Traffic tăng 23%|4 từ khóa vào Top 3" \
        --draft-only

    # Gửi thật
    python3 send_email.py --to "client@example.com" --client "TMA Solutions" \
        --month "07/2026" --attach outputs/bao-cao.docx \
        --highlights "Top 10 tăng 15 từ|Traffic tăng 23%|4 từ khóa vào Top 3"
"""

import argparse
import json
import os
import smtplib
import ssl
import sys
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")


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


def compose_email(client, month, highlights, sender_name):
    """Soạn nội dung email báo cáo SEO."""
    hl_lines = ""
    if highlights:
        items = [h.strip() for h in highlights.split("|") if h.strip()]
        hl_lines = "\n".join(f"  ✓ {item}" for item in items)

    body = f"""Kính gửi Anh/Chị {client},

Đây là báo cáo SEO tháng {month} từ đội ngũ {sender_name}.

📊 KẾT QUẢ NỔI BẬT THÁNG {month}:
{hl_lines if hl_lines else "  (Xem chi tiết trong file đính kèm)"}

Chi tiết đầy đủ được đính kèm trong file báo cáo. Anh/Chị vui lòng xem và phản hồi nếu có câu hỏi.

Chúng tôi sẽ tiếp tục triển khai các kế hoạch đã đề ra trong tháng tới để duy trì và cải thiện kết quả.

Trân trọng,
Đặng Ngọc Minh Thư
Account PM | {sender_name}
📞 098.77.99.803
✉️ dnmthu1704@gmail.com"""

    subject = f"[{sender_name}] Báo cáo SEO tháng {month} — {client}"
    return subject, body


def build_message(from_email, to_email, cc, subject, body, attach_path, sender_name):
    """Tạo MIME message với file đính kèm."""
    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{from_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc

    msg.attach(MIMEText(body, "plain", "utf-8"))

    if attach_path:
        if not os.path.exists(attach_path):
            raise SystemExit(f"[x] File đính kèm không tồn tại: {attach_path}")
        with open(attach_path, "rb") as f:
            filename = os.path.basename(attach_path)
            part = MIMEApplication(f.read(), Name=filename)
            part["Content-Disposition"] = f'attachment; filename="{filename}"'
            msg.attach(part)
        print(f"[i] Đính kèm: {filename} ({os.path.getsize(attach_path):,} bytes)")

    return msg


def save_draft(subject, body, to_email, attach_path, client):
    """Lưu bản nháp email ra file .txt."""
    date_str = datetime.now().strftime("%d-%m-%Y")
    draft_path = f"outputs/email-draft-{client.replace(' ', '-')}-{date_str}.txt"
    os.makedirs("outputs", exist_ok=True)
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(f"To: {to_email}\n")
        f.write(f"Subject: {subject}\n")
        if attach_path:
            f.write(f"Attachment: {os.path.basename(attach_path)}\n")
        f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("-" * 50 + "\n\n")
        f.write(body)
    return draft_path


def send_via_smtp(msg, gmail_user, app_password, to_email, cc):
    """Gửi email qua Gmail SMTP."""
    recipients = [to_email]
    if cc:
        recipients.extend([e.strip() for e in cc.split(",") if e.strip()])

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(gmail_user, app_password)
        server.sendmail(gmail_user, recipients, msg.as_string())


def main():
    ap = argparse.ArgumentParser(description="Gửi email báo cáo SEO tháng qua Gmail")
    ap.add_argument("--to", required=True, help="Email người nhận (client)")
    ap.add_argument("--client", required=True, help="Tên client")
    ap.add_argument("--month", required=True, help="Tháng báo cáo (vd: 07/2026)")
    ap.add_argument("--attach", default="", help="Đường dẫn file báo cáo đính kèm")
    ap.add_argument("--highlights", default="", help="Highlights tháng, ngăn cách bằng | ")
    ap.add_argument("--cc", default="", help="Email CC (nếu có)")
    ap.add_argument("--draft-only", action="store_true", help="Chỉ tạo bản nháp, không gửi")
    args = ap.parse_args()

    cfg = load_config()
    sender_name = cfg.get("sender_name", "SEONGON")
    cc = args.cc or cfg.get("cc", "")

    print(f"[i] Soạn email gửi đến: {args.to}")
    subject, body = compose_email(args.client, args.month, args.highlights, sender_name)

    # Hiển thị nội dung email
    print("\n" + "=" * 55)
    print("NỘI DUNG EMAIL:")
    print("=" * 55)
    print(f"To: {args.to}")
    print(f"Subject: {subject}")
    if args.attach:
        print(f"Attachment: {os.path.basename(args.attach)}")
    print("-" * 55)
    print(body)
    print("=" * 55 + "\n")

    # Lưu bản nháp
    draft_path = save_draft(subject, body, args.to, args.attach, args.client)
    print(f"[✓] Đã lưu bản nháp: {draft_path}")

    if args.draft_only:
        print("[i] Chế độ --draft-only: không gửi email.")
        print("    → Xem lại nội dung, sau đó chạy lại không có --draft-only để gửi thật.")
        return

    # Kiểm tra config
    gmail_user = cfg.get("gmail_user", "")
    app_password = cfg.get("gmail_app_password", "")
    if not gmail_user or not app_password:
        raise SystemExit(
            "[x] Chưa cấu hình Gmail.\n"
            "    Thêm 'gmail_user' và 'gmail_app_password' vào config.json.\n"
            "    Hướng dẫn tạo App Password: myaccount.google.com → Security → App passwords"
        )

    print(f"[i] Đang gửi từ: {gmail_user} ...")
    msg = build_message(gmail_user, args.to, cc, subject, body, args.attach, sender_name)

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
