"""
Telegram Bot Notification Client for Radar.
Sends real-time lock-screen push alerts directly to your phone via Telegram.
"""

import logging
import requests
from config import TELEGRAM_CONFIG

logger = logging.getLogger("Radar")

class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_CONFIG["bot_token"]
        self.chat_id = TELEGRAM_CONFIG["chat_id"]

    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def send_alert(self, opp: dict) -> bool:
        if not self.is_configured():
            return False

        org = opp.get("organization", "Company")
        title = opp.get("title", "New Opportunity")
        loc = opp.get("location", "Nigeria")
        cat = opp.get("category", "")
        url = opp.get("apply_url") or opp.get("lab_url") or opp.get("url", "")
        pi = opp.get("pi_name", "")
        nysc_tag = opp.get("nysc_status", "No NYSC Required")

        message = (
            f"🎯 <b>NEW RADAR ALERT (NO NYSC)</b>\n\n"
            f"💼 <b>{title}</b>\n"
            f"🏢 <b>Org:</b> {org} ({loc})\n"
            f"🏷️ <b>Category:</b> {cat}\n"
            f"✅ <b>Eligibility:</b> {nysc_tag}\n"
        )

        if pi:
            message += f"👨‍🏫 <b>Lead PI / Contact:</b> {pi}\n"

        message += f"\n🔗 <a href='{url}'>Click Here to View & Apply</a>"

        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        try:
            resp = requests.post(
                api_url,
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                },
                timeout=10
            )
            if resp.status_code == 200:
                logger.info(f"[Telegram] Sent push alert for: {title}")
                return True
            else:
                logger.warning(f"[Telegram] Send failed: {resp.text}")
        except Exception as e:
            logger.error(f"[Telegram] Exception: {e}")

        return False
