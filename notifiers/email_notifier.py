"""
Email Notification Client for Radar.
"""

import logging
import requests
from config import EMAIL_CONFIG

logger = logging.getLogger("Radar")

class EmailNotifier:
    def __init__(self):
        self.base_url = EMAIL_CONFIG["base_url"].rstrip("/")
        self.api_key = EMAIL_CONFIG["api_key"]
        self.from_email = EMAIL_CONFIG["from_email"]
        self.from_name = EMAIL_CONFIG["from_name"]
        self.recipient_email = EMAIL_CONFIG["recipient_email"]

    def is_configured(self) -> bool:
        return bool(self.api_key and self.recipient_email)

    def send_digest(self, new_opportunities: list[dict]) -> bool:
        if not self.is_configured():
            logger.warning("[EmailNotifier] Email API Key or recipient not configured. Skipping email.")
            return False

        if not new_opportunities:
            logger.info("[EmailNotifier] No new opportunities to email.")
            return True

        count = len(new_opportunities)
        subject = f"🎯 Radar Alert: {count} New Pre-NYSC & Research Opportunities Detected"

        # Build clean HTML email body
        items_html = ""
        for opp in new_opportunities:
            org = opp.get("organization", "Company / Lab")
            title = opp.get("title", "Opportunity")
            cat = opp.get("category", "")
            loc = opp.get("location", "")
            apply_url = opp.get("apply_url") or opp.get("lab_url") or opp.get("url", "")
            desc = opp.get("description", "")
            pi = opp.get("pi_name", "")
            email = opp.get("email", "")

            pi_info = f"<p style='margin: 4px 0; color: #475569;'><strong>Lead PI / Contact:</strong> {pi} ({email})</p>" if pi else ""

            items_html += f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <h3 style="margin: 0; color: #0f172a; font-size: 16px;">{title}</h3>
                </div>
                <p style="margin: 4px 0 8px 0; color: #0284c7; font-weight: 600; font-size: 14px;">{org} &bull; <span style="color: #64748b;">{loc}</span></p>
                <div style="display: inline-block; background: #ecfdf5; color: #065f46; font-size: 12px; font-weight: bold; padding: 3px 8px; border-radius: 4px; margin-bottom: 8px;">
                    {opp.get('nysc_status', 'No NYSC Required')}
                </div>
                {pi_info}
                <p style="margin: 8px 0; color: #334155; font-size: 13px; line-height: 1.5;">{desc}</p>
                <div style="margin-top: 12px;">
                    <a href="{apply_url}" style="background: #0284c7; color: #ffffff; padding: 8px 16px; text-decoration: none; border-radius: 6px; font-size: 13px; font-weight: bold; display: inline-block;">View & Apply &rarr;</a>
                </div>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{subject}</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; padding: 24px; margin: 0;">
            <div style="max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 28px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9;">
                <div style="border-bottom: 2px solid #0284c7; padding-bottom: 16px; margin-bottom: 24px;">
                    <h1 style="color: #0f172a; margin: 0; font-size: 22px;">Radar Opportunity Scanner</h1>
                    <p style="color: #64748b; margin: 6px 0 0 0; font-size: 14px;">Real-time Pre-NYSC, Tech Scaleups & Academic Research Assistant Alerts</p>
                </div>
                <p style="color: #334155; font-size: 14px;">Hello Ezekiel,</p>
                <p style="color: #334155; font-size: 14px;">Radar detected <strong>{count} fresh opportunities</strong> that do not mandate NYSC completion:</p>
                
                {items_html}

                <div style="border-top: 1px solid #e2e8f0; margin-top: 28px; padding-top: 16px; color: #94a3b8; font-size: 12px; text-align: center;">
                    Radar Automated Scanner &bull; Tailored for Ezekiel Eyitayo Feranmi (<a href="https://eyitayo.online" style="color: #0284c7;">eyitayo.online</a>)
                </div>
            </div>
        </body>
        </html>
        """

        endpoint = f"{self.base_url}/v1/emails"
        sender = f"{self.from_name} <{self.from_email}>"

        try:
            resp = requests.post(
                endpoint,
                json={
                    "from": sender,
                    "to": self.recipient_email,
                    "subject": subject,
                    "html": html
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=15
            )
            if resp.status_code < 400:
                logger.info(f"[EmailNotifier] Digest email sent successfully to {self.recipient_email} (Status {resp.status_code})")
                return True
            else:
                logger.warning(f"[EmailNotifier] Failed to send email (HTTP {resp.status_code}): {resp.text}")
        except Exception as e:
            logger.error(f"[EmailNotifier] Email send exception: {e}")

        return False
