"""
Graduate Trainee & Early-Career Tech Monitor.
Queries live ATS APIs (Greenhouse, Workable, etc.) and curated graduate programs
to detect exact live postings (title, job description snippet, location, and direct application URL)
with strict filtering against mandatory NYSC requirements.
"""

import logging
import re
import html
import requests
from scrapers.base import BaseScraper
from scrapers.nysc_filter import NYSCFilter

logger = logging.getLogger("Radar")

# Curated high-prestige graduate programs (annual intakes & pre-NYSC pipelines)
CURATED_GRADUATE_PROGRAMS = [
    {
        "organization": "PwC Nigeria",
        "title": "PwC Graduate Internship Programme (Pre-NYSC)",
        "category": "Pre-NYSC Graduate Internship",
        "url": "https://www.pwc.com/ng/en/careers.html",
        "apply_url": "https://pwc.wd3.myworkdayjobs.com/Global_Experienced_Careers",
        "description": "Pre-NYSC internship program specifically designed for recent university graduates awaiting call-up to gain consulting, data, and technology advisory experience.",
        "location": "Lagos / Abuja"
    },
    {
        "organization": "KPMG Nigeria",
        "title": "KPMG Pre-NYSC Advisory & Technology Internship",
        "category": "Pre-NYSC Graduate Internship",
        "url": "https://kpmg.com/ng/en/home/careers.html",
        "apply_url": "https://kpmg.com/ng/careers",
        "description": "Specialized internship for fresh university graduates awaiting NYSC mobilization in digital transformation, software audit, and technology consulting.",
        "location": "Lagos"
    },
    {
        "organization": "ARM Holding",
        "title": "ARM Young Talent Programme (AYTP)",
        "category": "Graduate Internship / Pre-NYSC",
        "url": "https://armholdco.com",
        "apply_url": "https://arm.seamlesshiring.com",
        "description": "Annual talent development track for high-achieving fresh graduates awaiting NYSC in investment tech, software systems, and asset management.",
        "location": "Lagos"
    },
    {
        "organization": "Ventures Platform",
        "title": "Venture Capital Analyst Fellowship",
        "category": "Pre-NYSC Fellowship",
        "url": "https://venturesplatform.com",
        "apply_url": "https://venturesplatform.com/careers",
        "description": "Fellowship supporting African early-stage tech investments, conducting technical due diligence on software startups, and ecosystem mapping.",
        "location": "Lagos / Abuja"
    }
]

# Relevant keywords for early-career / junior / software / data roles
TARGET_ROLE_KEYWORDS = [
    "graduate", "trainee", "intern", "internship", "junior", "associate",
    "developer", "engineer", "software", "backend", "frontend", "fullstack",
    "data", "analyst", "fellow", "hatchdev", "entry", "qa"
]

# Keywords to skip executive / senior management roles
SENIOR_EXCLUDE_KEYWORDS = [
    "senior", "lead", "principal", "director", "head of", "chief", "manager", "vp", "staff"
]

def clean_html(text: str, max_chars: int = 300) -> str:
    if not text:
        return ""
    unescaped = html.unescape(text)
    clean = re.sub(r'<[^>]+>', ' ', unescaped)
    clean = " ".join(clean.split())
    if len(clean) > max_chars:
        return clean[:max_chars].rstrip() + "..."
    return clean

class GTTechScraper(BaseScraper):
    def __init__(self):
        super().__init__("GTTechScraper")

    def _scrape_greenhouse(self, board_token: str, org_name: str) -> list[dict]:
        """Fetch exact live job postings from Greenhouse API."""
        url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"
        jobs_found = []
        try:
            resp = requests.get(url, timeout=12)
            if resp.status_code != 200:
                logger.warning(f"[GTTech] Greenhouse {board_token} returned HTTP {resp.status_code}")
                return []
            
            jobs = resp.json().get("jobs", [])
            for j in jobs:
                title = j.get("title", "").strip()
                t_lower = title.lower()
                loc = j.get("location", {}).get("name", "Nigeria / Remote")
                l_lower = loc.lower()
                content = j.get("content", "")

                # Must be in Nigeria or Remote/Hybrid
                if not any(p in l_lower for p in ["nigeria", "lagos", "abuja", "ibadan", "remote", "hybrid"]):
                    continue

                # Exclude purely senior/lead roles unless junior/associate/trainee is specified
                if any(s in t_lower for s in SENIOR_EXCLUDE_KEYWORDS) and not any(ok in t_lower for ok in ["junior", "associate", "trainee", "entry"]):
                    continue

                # Must match early-career, engineering, or data keywords
                if not any(k in t_lower for k in TARGET_ROLE_KEYWORDS):
                    continue

                apply_url = j.get("absolute_url")
                desc_snippet = clean_html(content) or f"Open engineering / early-career role at {org_name}."

                is_eligible, reason = NYSCFilter.evaluate(title, content, "Tech Scaleup")
                if not is_eligible:
                    continue

                jobs_found.append({
                    "organization": org_name,
                    "title": title,
                    "category": "Tech / Early-Career Role",
                    "location": loc,
                    "apply_url": apply_url,
                    "portal_url": apply_url,
                    "description": desc_snippet,
                    "nysc_status": "No NYSC Required / Tech Track",
                    "nysc_reason": reason
                })
        except Exception as e:
            logger.error(f"[GTTech] Error querying Greenhouse for {org_name}: {e}")
        return jobs_found

    def _scrape_workable(self, account: str, org_name: str) -> list[dict]:
        """Fetch exact live job postings from Workable API."""
        url = f"https://apply.workable.com/api/v3/accounts/{account}/jobs"
        jobs_found = []
        try:
            resp = requests.post(url, json={}, timeout=10)
            if resp.status_code != 200:
                logger.warning(f"[GTTech] Workable {account} returned HTTP {resp.status_code}")
                return []
            
            results = resp.json().get("results", [])
            for j in results:
                title = j.get("title", "").strip()
                t_lower = title.lower()
                country = j.get("location", {}).get("country", "")
                city = j.get("location", {}).get("city", "")
                loc = f"{city}, {country}".strip(", ")
                l_lower = loc.lower()

                if not any(p in l_lower for p in ["nigeria", "lagos", "abuja", "ibadan", "remote"]):
                    continue

                if any(s in t_lower for s in SENIOR_EXCLUDE_KEYWORDS) and not any(ok in t_lower for ok in ["junior", "associate", "trainee", "entry"]):
                    continue

                if not any(k in t_lower for k in TARGET_ROLE_KEYWORDS):
                    continue

                shortcode = j.get("shortcode", "")
                apply_url = f"https://apply.workable.com/{account}/j/{shortcode}/"
                desc_snippet = clean_html(j.get("description", "")) or f"Open position at {org_name} ({loc})."

                is_eligible, reason = NYSCFilter.evaluate(title, desc_snippet, "Fintech / Tech Scaleup")
                if not is_eligible:
                    continue

                jobs_found.append({
                    "organization": org_name,
                    "title": title,
                    "category": "Fintech / Tech Scaleup",
                    "location": loc,
                    "apply_url": apply_url,
                    "portal_url": apply_url,
                    "description": desc_snippet,
                    "nysc_status": "No NYSC Required / Skills-First",
                    "nysc_reason": reason
                })
        except Exception as e:
            logger.error(f"[GTTech] Error querying Workable for {org_name}: {e}")
        return jobs_found

    def scrape(self) -> list[dict]:
        logger.info("[GTTech] Scanning live ATS feeds (Greenhouse, Workable) and curated graduate programs...")
        raw_items = []

        # 1. Moniepoint via live Greenhouse API
        raw_items.extend(self._scrape_greenhouse("moniepoint", "Moniepoint"))

        # 2. Kuda & FairMoney via live Workable APIs
        raw_items.extend(self._scrape_workable("kuda", "Kuda Bank"))
        raw_items.extend(self._scrape_workable("fairmoney", "FairMoney"))

        # 3. Curated Graduate Programs (ARM, PwC, KPMG, Ventures Platform)
        for p in CURATED_GRADUATE_PROGRAMS:
            eligible, reason = NYSCFilter.evaluate(p["title"], p["description"], p["category"])
            if eligible:
                raw_items.append({
                    "organization": p["organization"],
                    "title": p["title"],
                    "category": p["category"],
                    "location": p["location"],
                    "apply_url": p["apply_url"],
                    "portal_url": p.get("url", p["apply_url"]),
                    "description": p["description"],
                    "nysc_status": "Pre-NYSC Verified",
                    "nysc_reason": reason
                })

        # Process IDs and deduplicate
        results = []
        for opp in raw_items:
            opp_id = self.generate_id(opp["organization"], opp["title"], opp["apply_url"])
            is_brand_new = self.is_new(opp_id)
            opp["id"] = opp_id
            opp["is_brand_new"] = is_brand_new
            results.append(opp)

        logger.info(f"[GTTech] Discovered {len(results)} exact live opportunities.")
        return results
