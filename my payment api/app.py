
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
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
        "━━━━━━━━━━━━━━━━━━\n"
        "🟢 Status: Online\n"
        "🔎 Search: /lookup?phone=9000000001\n"
        "🧪 Mode: Synthetic Demo Only\n"
        "🔓 API Key: Not Required\n"
        "━━━━━━━━━━━━━━━━━━\n"
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
    )
):
    try:
        with DATA_FILE.open(encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError("Expected a list")

    except (OSError, json.JSONDecodeError, ValueError):
        raise HTTPException(
            status_code=500,
            detail="⚠️ Demo database unavailable or invalid"
        )

    for record in records:
        if not isinstance(record, dict):
            continue

        # Only explicitly marked synthetic records are searchable.
        if record.get("demo") is not True:
            continue

        if str(record.get("Mobile No.", "")) == phone:
            return (
                "👑 MY PAYMENT API 👑\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "✅ STATUS: DEMO MATCH\n"
                "🧪 TYPE: SYNTHETIC TEST DATA\n\n"
                f"👤 Name: {record.get('Paytm User Name', 'Demo User')}\n"
                f"📧 Email: {record.get('Email Id', 'demo@example.com')}\n"
                f"📱 Mobile: {record.get('Mobile No.', 'N/A')}\n"
                f"🎂 DOB: {record.get('Date of Birth', 'N/A')}\n"
                f"🏙️ City: {record.get('City', 'N/A')}\n"
                f"🚻 Gender: {record.get('Gender', 'N/A')}\n"
                f"🏠 Address: {record.get('Address') or 'Not Available'}\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"👨‍💻 Created By: {CREATED_BY}\n"
                f"📢 Telegram: {CONTACT}\n"
            )

    raise HTTPException(
        status_code=404,
        detail="❌ Demo record not found"
    )
