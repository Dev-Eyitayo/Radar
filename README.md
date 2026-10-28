# Radar: Pre-NYSC & Academic Research Opportunity Scanner

An automated opportunity radar built specifically for **Ezekiel Eyitayo Feranmi** ([eyitayo.online](https://eyitayo.online)).

Radar continuously monitors for **Pre-NYSC Graduate Trainee Programs**, **Tech Scaleup Graduate Academies**, and **Academic Research Assistant Roles** with professors/doctors across Southwest Nigeria (UI, FUNAAB, Covenant, UNILAG, DSN) and dispatches real-time alerts to your email and Telegram.

---

## 🚫 Hard Gate: No-NYSC Requirement (Strict Mode)

Because I just graduated and do not yet have an NYSC discharge certificate:
- **Hard Blocker:** Any opportunity requiring mandatory NYSC completion (such as traditional commercial bank ELTPs or oil & gas multinationals) is **strictly filtered out**.
- **Eligible Only:** Only roles verified as **Pre-NYSC**, **Awaiting NYSC**, **Graduate Internships**, **Tech Skills-First Tracks**, or **Academic Research Assistant appointments** are processed.

---

## 🚀 Key Features

1. **Tech Scaleup & Graduate Trainee Monitor**:
   - Tracks Moniepoint (HatchDev), Interswitch, Flutterwave, Kuda Bank, PwC Pre-NYSC Graduate Internships, KPMG Pre-NYSC, ARM Young Talent Programme, and Ventures Platform.
2. **Academic Research Assistant Labs**:
   - Tracks active lab PIs at **University of Ibadan (UI)**, **FUNAAB**, **Covenant University**, **UNILAG**, and **Data Science Nigeria (DSN)**.
3. **Live ArXiv Preprints (2025–2026 Academic Research)**:
   - Scrapes recent preprints authored by active Nigerian researchers in AI, Computer Science, and Health Informatics to pitch directly as a software/data research assistant.
4. **Zero-Staleness & Deduplication Engine**:
   - Hashing engine prevents duplicate alerts. Only fresh, newly detected opportunities trigger notifications.
5. **Multi-Channel Alerts**:
   - **Email Digest**: Configured via SendByte (same provider as Kontributa) delivering directly to `ezekieleyitayo2020@gmail.com`.
   - **Telegram Push Alerts**: Instant lock-screen push notifications via Telegram Bot.
6. **100% Free Cloud Automation via GitHub Actions**:
   - Runs on GitHub's free runners twice daily (`07:00 AM` and `03:00 PM` West Africa Time). **$0.00 hosting cost.**

---

## 📁 Project Structure

```
/home/eyitayo/Projects/Radar/
├── .env                              # Secrets (SendByte API key, Telegram tokens)
├── .env.example
├── .gitignore
├── requirements.txt
├── config.py                         # Candidate profile & target hub settings
├── run.py                            # Main runner
├── .github/
│   └── workflows/
│       └── daily_scan.yml            # Automated GitHub Actions cron workflow
├── data/
│   ├── seen_opportunities.json       # State database tracking notified roles
│   └── latest_digest.json            # Latest active opportunities
├── scrapers/
│   ├── base.py                       # Base HTTP client & state hasher
│   ├── nysc_filter.py                # Hard NYSC blocking gate
│   ├── gt_tech_scraper.py            # Tech scaleups & pre-NYSC graduate programs
│   ├── ra_academic_scraper.py        # University faculty research labs
│   └── ra_preprints_scraper.py       # Live ArXiv preprints (recent 2025-2026 papers)
└── notifiers/
    ├── email_notifier.py             # SendByte email dispatcher
    ├── telegram_notifier.py          # Telegram push notifier
    └── dispatcher.py                 # Multi-channel router
```

---

## 🛠️ Local Usage

To run the scanner manually:

```bash
cd /home/eyitayo/Projects/Radar
python3 run.py
```

---

## 📱 Setting Up Instant Telegram Phone Alerts (Optional)

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`, follow prompts, and copy the **HTTP API Token**.
3. Search for `@userinfobot` on Telegram and send `/start` to get your **Chat ID**.
4. Add them to `/home/eyitayo/Projects/Radar/.env`:
   ```bash
   TELEGRAM_BOT_TOKEN="your_token_here"
   TELEGRAM_CHAT_ID="your_chat_id_here"
   ```
5. In your GitHub repository settings, add the same secrets under **Settings > Secrets and variables > Actions** so GitHub Actions can send push alerts to your phone.
