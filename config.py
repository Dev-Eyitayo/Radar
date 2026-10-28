"""
Configuration & Environment Settings for Radar Opportunity Scanner.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Load .env if present
load_dotenv(BASE_DIR / ".env")

# Candidate Profile
CANDIDATE = {
    "name": os.getenv("CANDIDATE_NAME", "Ezekiel Eyitayo Feranmi"),
    "portfolio": os.getenv("CANDIDATE_PORTFOLIO", "https://eyitayo.online"),
    "github": os.getenv("CANDIDATE_GITHUB", "https://github.com/Dev-Eyitayo"),
    "email": os.getenv("ALERT_RECIPIENT_EMAIL", "ezekieleyitayo2020@gmail.com"),
    "skills": ["Python", "FastAPI", "Django", "Next.js", "React", "PostgreSQL", "Data Pipelines"]
}

# Notification Settings
EMAIL_CONFIG = {
    "base_url": os.getenv("EMAIL_BASE_URL", "https://api.sendbyte.africa"),
    "api_key": os.getenv("EMAIL_API_KEY", ""),
    "from_email": os.getenv("EMAIL_FROM_EMAIL", "kontributa@eyitayo.online"),
    "from_name": os.getenv("EMAIL_FROM_NAME", "Radar Opportunities"),
    "recipient_email": os.getenv("ALERT_RECIPIENT_EMAIL", "ezekieleyitayo2020@gmail.com")
}

TELEGRAM_CONFIG = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID", "")
}

# NYSC Hard Gate Setting
# When True: ANY position that mandates completion of NYSC is permanently dropped.
ENFORCE_NO_NYSC_ONLY = os.getenv("ENFORCE_NO_NYSC_ONLY", "True").lower() in ("true", "1", "yes")

# Target Universities for Research Assistant & Active Lab Tracking
TARGET_UNIVERSITIES = [
    {"name": "University of Ibadan", "domain": "ui.edu.ng", "state": "Oyo"},
    {"name": "Federal University of Agriculture, Abeokuta", "domain": "funaab.edu.ng", "state": "Ogun"},
    {"name": "Covenant University", "domain": "covenantuniversity.edu.ng", "state": "Ogun"},
    {"name": "University of Lagos", "domain": "unilag.edu.ng", "state": "Lagos"},
    {"name": "Obafemi Awolowo University", "domain": "oauife.edu.ng", "state": "Osun"}
]

# State Storage
SEEN_DB_PATH = DATA_DIR / "seen_opportunities.json"
DIGEST_PATH = DATA_DIR / "latest_digest.json"
