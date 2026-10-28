# Radar

My automated opportunity radar tracking **Graduate Trainee Programs**, **Tech Academies & Internships**, and **Academic Research Assistant (RA) positions** across Nigeria.

## Why I Built This

I built Radar to monitor early-career opportunities and academic research labs without manually checking dozens of job boards and university portals every day:

1. **Track Tech & Graduate Programs**: Monitors top tech scaleups, corporate graduate trainee programs, and engineering academies.
2. **Track Active Academic Research Labs**: Monitors faculty PIs and doctors across UI, FUNAAB, Covenant, UNILAG, and DSN AI Lab, alongside recent ArXiv preprints, so I can pitch directly for RA roles.
3. **Notify Me in Real Time**: Deduplicates openings and sends fresh alerts straight to my Telegram and email.

## What I Track

- **Tech & Graduate Programs**: Moniepoint (HatchDev), Interswitch, Flutterwave, Kuda, PwC, KPMG, ARM (AYTP), and Ventures Platform.
- **Academic Research Labs**: Active faculty labs across UI, FUNAAB, Covenant, UNILAG, and DSN.
- **Recent Preprints**: ArXiv publications from Nigerian researchers in AI and software systems for targeted RA cold-outreach.

## Setup & Local Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Copy `.env.example` to `.env` and fill in secrets:
   - `SENDBYTE_API_KEY` & `SENDBYTE_FROM_EMAIL` (for email alerts)
   - `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID` (for phone alerts)

3. **Run scanner:**
   ```bash
   python3 run.py
   ```

## Telegram Bot Setup

1. Message `@BotFather` on Telegram and run `/newbot` to get a bot token.
2. Message `@userinfobot` to get your chat ID.
3. Save both in `.env` (and in GitHub repository Secrets for automated runs).

## Automation

Runs automatically twice daily via GitHub Actions (`.github/workflows/daily_scan.yml`).
