import json
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title="👑 PRIYANSHU OP",
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
        "👑 PRIYANSHU OP 👑\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🟢 Status: Online\n"
        "🔎 Search: /lookup?phone=9730403194\n"
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

    except (OSError, json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"⚠️ Database error: {str(e)}"
        )

    # Clean query to digits only
    clean_query = re.sub(r"\D", "", phone)

    for record in records:
        if not isinstance(record, dict):
            continue

        raw_phone = str(record.get("Mobile No.", ""))
        # Strip spaces, hyphens, parentheses to handle numbers like '256-772354015'
        clean_phone = re.sub(r"\D", "", raw_phone)

        # Match exact digits or check if query matches the cleaned mobile number
        if clean_phone == clean_query or raw_phone.strip() == phone.strip():
            return (
                "👑 PRIYANSHU OP 👑\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "✅ STATUS: MATCH FOUND\n\n"
                f"👤 Name: {record.get('Paytm User Name', 'N/A')}\n"
                f"📧 Email: {record.get('Email Id', 'N/A')}\n"
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
        detail="❌ Record not found"
    )
