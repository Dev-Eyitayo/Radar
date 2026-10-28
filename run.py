"""
Radar Opportunity Scanner: Execution Orchestrator.
Discovers Pre-NYSC Graduate Trainee Programs and Academic Research Assistant Roles.
Strictly blocks any opportunity requiring NYSC completion.

Author: Antigravity for Ezekiel Eyitayo Feranmi
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from config import (
    CANDIDATE,
    SEEN_DB_PATH,
    DIGEST_PATH,
    DATA_DIR,
    ENFORCE_NO_NYSC_ONLY
)
from scrapers.gt_tech_scraper import GTTechScraper
from scrapers.ra_academic_scraper import RAAcademicScraper
from scrapers.ra_preprints_scraper import RAPreprintsScraper
from scrapers.nysc_filter import NYSCFilter
from notifiers.dispatcher import AlertDispatcher

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Radar")

def load_seen_db() -> dict:
    if SEEN_DB_PATH.exists():
        try:
            with open(SEEN_DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_seen_db(data: dict) -> None:
    with open(SEEN_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    console.print(Panel.fit(
        f"[bold cyan]Radar Opportunity Scanner[/bold cyan] (Pre-NYSC & Fresh Graduate Edition)\n"
        f"Candidate: [bold green]{CANDIDATE['name']}[/bold green] ([link={CANDIDATE['portfolio']}]{CANDIDATE['portfolio']}[/link])\n"
        f"Alert Inboxes: [bold yellow]{CANDIDATE['email']}[/bold yellow] & Telegram\n"
        f"Filter Mode: [bold red]HARD BLOCK ON NYSC-MANDATORY ROLES[/bold red]",
        border_style="cyan"
    ))

    seen_db = load_seen_db()
    all_opportunities = []

    # 1. Graduate Trainees & Tech Scaleups
    console.print("[yellow]▶ Scanning Pre-NYSC Graduate Trainee & Tech Academy Programs...[/yellow]")
    gt_scraper = GTTechScraper()
    gt_opps = gt_scraper.scrape()
    console.print(f"  [green]✔ Loaded {len(gt_opps)} pre-NYSC graduate programs.[/green]")
    all_opportunities.extend(gt_opps)

    # 2. Academic Research Assistant Labs
    console.print("[yellow]▶ Scanning Academic Research Labs (UI, FUNAAB, Covenant, UNILAG, DSN)...[/yellow]")
    ra_scraper = RAAcademicScraper()
    ra_opps = ra_scraper.scrape()
    console.print(f"  [green]✔ Loaded {len(ra_opps)} active university research labs.[/green]")
    all_opportunities.extend(ra_opps)

    # 3. ArXiv Live Preprints (Recent 2025/2026 Academic Research)
    console.print("[yellow]▶ Scanning Live ArXiv Research Publications (Recent 2025-2026 Preprints)...[/yellow]")
    arxiv_scraper = RAPreprintsScraper()
    arxiv_opps = arxiv_scraper.scrape(max_per_query=3)
    console.print(f"  [green]✔ Loaded {len(arxiv_opps)} recent research paper authors.[/green]")
    all_opportunities.extend(arxiv_opps)

    # Filter out anything with NYSC requirement if enabled
    filtered = []
    for opp in all_opportunities:
        if ENFORCE_NO_NYSC_ONLY:
            is_eligible, reason = NYSCFilter.evaluate(
                opp.get("title", ""),
                opp.get("description", ""),
                opp.get("category", "")
            )
            if not is_eligible:
                continue
        filtered.append(opp)

    console.print(f"\n[cyan]⚡ Total eligible opportunities: {len(filtered)}. Detecting new additions...[/cyan]")

    # Identify brand new opportunities
    now_iso = datetime.now(timezone.utc).isoformat()
    new_opps = []

    for opp in filtered:
        opp_id = opp["id"]
        if opp_id not in seen_db:
            new_opps.append(opp)
            seen_db[opp_id] = {
                "organization": opp.get("organization"),
                "title": opp.get("title"),
                "apply_url": opp.get("apply_url") or opp.get("lab_url"),
                "first_seen": now_iso
            }

    # Save state
    save_seen_db(seen_db)

    # Save latest digest file
    with open(DIGEST_PATH, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    # Display Results Table
    table = Table(title="Radar Opportunities (100% No NYSC Required)", show_header=True, header_style="bold magenta")
    table.add_column("Organization / University", style="bold white", width=25)
    table.add_column("Opportunity Title", style="cyan", width=35)
    table.add_column("Category", style="green", width=24)
    table.add_column("NYSC Eligibility", style="bold green", width=24)
    table.add_column("Status", style="yellow", width=12)

    for opp in filtered[:12]:
        status_tag = "[bold green]NEW[/bold green]" if opp in new_opps else "Tracked"
        table.add_row(
            opp.get("organization", "")[:24],
            opp.get("title", "")[:34],
            opp.get("category", "")[:22],
            opp.get("nysc_status", "No NYSC Needed")[:22],
            status_tag
        )

    console.print("\n")
    console.print(table)

    # Dispatch alerts
    if new_opps:
        console.print(f"\n[bold green]🚀 Found {len(new_opps)} brand new opportunities! Dispatching alerts...[/bold green]")
        dispatcher = AlertDispatcher()
        dispatcher.dispatch(new_opps)
    else:
        console.print("\n[dim]No brand new opportunities since last scan. Inboxes kept clean.[/dim]")

    console.print(f"\n📁 Latest Digest JSON: [link=file://{DIGEST_PATH}]{DIGEST_PATH}[/link]")
    console.print(f"📊 State Tracker:      [link=file://{SEEN_DB_PATH}]{SEEN_DB_PATH}[/link]\n")

if __name__ == "__main__":
    main()
