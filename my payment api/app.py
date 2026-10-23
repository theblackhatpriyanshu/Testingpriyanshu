
import json
import os
import secrets
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title="👑 My Payment API",
    docs_url=None,
    redoc_url=None
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sample.json"

CREATED_BY = "Priyanshu Gupta ❤️"
CONTACT = "https://t.me/priyanshuexploits"


@app.get("/", response_class=PlainTextResponse)
def home():
    return (
        "👑 MY PAYMENT API 👑\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🟢 Status: Online\n"
        "🔎 Endpoint: /lookup?phone=NUMBER\n"
        "🔐 Authentication: API Key Required\n\n"
        f"👨‍💻 Created By: {CREATED_BY}\n"
        f"📢 Telegram: {CONTACT}\n"
    )


@app.get("/lookup", response_class=PlainTextResponse)
def lookup(
    phone: str = Query(
        ...,
        min_length=10,
        max_length=15,
        pattern=r"^[0-9]+$"
    ),
    x_api_key: str = Header(default="")
):
    api_key = os.environ.get("API_KEY", "").strip()

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="🔐 API key is not configured"
        )

    if not secrets.compare_digest(x_api_key, api_key):
        raise HTTPException(
            status_code=401,
            detail="❌ Invalid API key"
        )

    try:
        with DATA_FILE.open(encoding="utf-8") as f:
            records = json.load(f)
    except (OSError, json.JSONDecodeError):
        raise HTTPException(
            status_code=500,
            detail="⚠️ Demo database unavailable"
        )

    for record in records:
        if record.get("demo") is not True:
            continue

        if str(record.get("Mobile No.", "")) == phone:
            return (
                "👑 MY PAYMENT API 👑\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "✅ STATUS: DEMO MATCH\n\n"
                f"👤 Name: {record.get('Paytm User Name', 'N/A')}\n"
                f"📧 Email: {record.get('Email Id', 'N/A')}\n"
                f"📱 Mobile: {record.get('Mobile No.', 'N/A')}\n"
                f"🎂 DOB: {record.get('Date of Birth', 'N/A')}\n"
                f"🏙️ City: {record.get('City', 'N/A')}\n"
                f"🚻 Gender: {record.get('Gender', 'N/A')}\n"
                f"🏠 Address: {record.get('Address') or 'Not Available'}\n\n"
                "⚠️ Synthetic demo data only\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"👨‍💻 Created By: {CREATED_BY}\n"
                f"📢 Telegram: {CONTACT}\n"
            )

    raise HTTPException(
        status_code=404,
        detail="❌ Demo record not found"
        )
        
