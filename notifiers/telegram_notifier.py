"""
Telegram Bot Notification Client for Radar.
Sends consolidated digests directly to your phone via Telegram.
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

    def _post_message(self, text: str) -> bool:
        """Send a single message to the configured chat."""
        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        try:
            resp = requests.post(
                api_url,
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True
                },
                timeout=10
            )
            if resp.status_code == 200:
                return True
            else:
                logger.warning(f"[Telegram] Send failed: {resp.text}")
        except Exception as e:
            logger.error(f"[Telegram] Exception: {e}")
        return False

    def send_digest(self, opportunities: list[dict]) -> bool:
        """Consolidates multiple opportunities into a single clean message."""
        if not self.is_configured() or not opportunities:
            return False

        total = len(opportunities)
        header = f"🎯 <b>Radar Alert: {total} New Opportunities Detected</b>\n\n"

        chunks = []
        current_chunk = header

        for i, opp in enumerate(opportunities, 1):
            org = opp.get("organization", "Company / Lab")
            title = opp.get("title", "Opportunity")
            loc = opp.get("location", "Nigeria")
            url = opp.get("apply_url") or opp.get("lab_url") or opp.get("url", "")
            pi = opp.get("pi_name", "")

            item_text = f"<b>{i}. {title}</b>\n🏢 {org} &bull; <i>{loc}</i>\n"
            if pi:
                item_text += f"👨‍🏫 Contact / PI: {pi}\n"
            item_text += f"👉 <a href='{url}'>View & Apply</a>\n\n"

            # Check if adding this item would exceed Telegram's 4096 limit
            if len(current_chunk) + len(item_text) > 3800:
                chunks.append(current_chunk.strip())
                current_chunk = f"🎯 <b>Radar Alert (Cont'd)</b>\n\n" + item_text
            else:
                current_chunk += item_text

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        all_ok = True
        for chunk in chunks:
            ok = self._post_message(chunk)
            if not ok:
                all_ok = False

        if all_ok:
            logger.info(f"[Telegram] Delivered consolidated digest for {total} opportunities.")
        return all_ok

    def send_alert(self, opp: dict) -> bool:
        """Fallback for sending a single standalone alert."""
        return self.send_digest([opp])
