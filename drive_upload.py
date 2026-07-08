#!/usr/bin/env python3
"""
drive_upload.py — Upload file lên Google Drive, tự convert sang Google Docs/Sheets.
Dùng chung cho tất cả skills trong workspace.

Cách dùng:
    python3 drive_upload.py <đường_dẫn_file> [--folder-id <ID>]
"""

import argparse
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

HERE = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(HERE, "credentials.json")
TOKEN_PATH = os.path.join(HERE, "token.json")

MIME_CONVERT = {
    ".docx": "application/vnd.google-apps.document",
    ".xlsx": "application/vnd.google-apps.spreadsheet",
    ".csv": "application/vnd.google-apps.spreadsheet",
}

SOURCE_MIME = {
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".csv": "text/csv",
}


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise SystemExit(
                    "[x] Không tìm thấy credentials.json.\n"
                    "    Tải về tại: console.cloud.google.com → APIs & Services → Credentials"
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


def upload_file(file_path, folder_id=None):
    ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)
    display_name = os.path.splitext(file_name)[0]

    source_mime = SOURCE_MIME.get(ext, "application/octet-stream")
    convert_mime = MIME_CONVERT.get(ext)

    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    metadata = {"name": display_name}
    if convert_mime:
        metadata["mimeType"] = convert_mime
    if folder_id:
        metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, mimetype=source_mime, resumable=True)
    result = service.files().create(
        body=metadata,
        media_body=media,
        fields="id,name,webViewLink",
    ).execute()

    return result


def main():
    ap = argparse.ArgumentParser(description="Upload file lên Google Drive")
    ap.add_argument("file", help="Đường dẫn file cần upload")
    ap.add_argument("--folder-id", default="", help="ID folder Google Drive (tùy chọn)")
    args = ap.parse_args()

    if not os.path.exists(args.file):
        raise SystemExit(f"[x] File không tồn tại: {args.file}")

    print(f"[i] Đang upload: {os.path.basename(args.file)} ...")
    result = upload_file(args.file, args.folder_id or None)

    print(f"[✓] Upload thành công!")
    print(f"    Tên: {result['name']}")
    print(f"    Link: {result['webViewLink']}")
    return result["webViewLink"]


if __name__ == "__main__":
    main()
