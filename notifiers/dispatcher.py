"""
Notification Dispatcher for Radar.
Coordinates Telegram instant push alerts and SendByte email digests.
"""

import logging
from notifiers.email_notifier import EmailNotifier
from notifiers.telegram_notifier import TelegramNotifier

logger = logging.getLogger("Radar")

class AlertDispatcher:
    def __init__(self):
        self.email_notifier = EmailNotifier()
        self.telegram_notifier = TelegramNotifier()

    def dispatch(self, new_opportunities: list[dict]) -> None:
        if not new_opportunities:
            logger.info("[Dispatcher] Zero new opportunities detected. No alerts triggered.")
            return

        logger.info(f"[Dispatcher] Dispatching alerts for {len(new_opportunities)} new opportunities...")

        # 1. Telegram Push Alerts
        if self.telegram_notifier.is_configured():
            for opp in new_opportunities:
                self.telegram_notifier.send_alert(opp)
        else:
            logger.info("[Dispatcher] Telegram not yet configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env or GitHub Secrets for phone push alerts.")

        # 2. Email Digest via SendByte / Senviok
        if self.email_notifier.is_configured():
            self.email_notifier.send_digest(new_opportunities)
        else:
            logger.info("[Dispatcher] Email provider not fully configured. Skipping email dispatch.")
