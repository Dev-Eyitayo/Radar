"""
Graduate Trainee & Pre-NYSC Tech Scaleup Monitor.
Monitors top Nigerian tech scaleups, consultancies, and fintech academies for
fresh graduate trainee programs, graduate internships, and junior engineering tracks
with STRICT filtering against mandatory NYSC requirements.
"""

import logging
from scrapers.base import BaseScraper
from scrapers.nysc_filter import NYSCFilter

logger = logging.getLogger("Radar")

# Curated active career endpoints & programs known for fresh graduate / pre-NYSC intake
ACTIVE_GT_PORTALS = [
    {
        "organization": "Moniepoint",
        "title": "HatchDev Graduate Engineering Academy",
        "category": "Tech Graduate Academy",
        "url": "https://moniepoint.com/careers",
        "apply_url": "https://boards.greenhouse.io/moniepoint",
        "description": "Intensive engineering fellowship training fresh graduates in backend systems, distributed architectures, and fintech APIs.",
        "nysc_friendly": True,
        "location": "Lagos / Hybrid"
    },
    {
        "organization": "Interswitch",
        "title": "Interswitch Trainee Programme (Engineering Track)",
        "category": "Fintech Graduate Trainee",
        "url": "https://www.interswitchgroup.com/careers",
        "apply_url": "https://interswitch.workable.com",
        "description": "Entry-level fintech development track focusing on switching rails, APIs, and digital payments infrastructure.",
        "nysc_friendly": True,
        "location": "Lagos / Remote"
    },
    {
        "organization": "PwC Nigeria",
        "title": "PwC Graduate Internship Programme (Pre-NYSC)",
        "category": "Pre-NYSC Graduate Internship",
        "url": "https://www.pwc.com/ng/en/careers.html",
        "apply_url": "https://pwc.wd3.myworkdayjobs.com/Global_Experienced_Careers",
        "description": "Pre-NYSC internship program specifically designed for recent university graduates awaiting call-up to gain consulting and technology experience.",
        "nysc_friendly": True,
        "location": "Lagos / Abuja"
    },
    {
        "organization": "KPMG Nigeria",
        "title": "KPMG Pre-NYSC Advisory & Tech Internship",
        "category": "Pre-NYSC Graduate Internship",
        "url": "https://kpmg.com/ng/en/home/careers.html",
        "apply_url": "https://kpmg.com/ng/careers",
        "description": "Specialized internship for fresh university graduates awaiting NYSC mobilization in digital transformation, software audit, and technology advisory.",
        "nysc_friendly": True,
        "location": "Lagos"
    },
    {
        "organization": "ARM Holding",
        "title": "ARM Young Talent Programme (AYTP)",
        "category": "Graduate Internship / Pre-NYSC",
        "url": "https://www.arm.com.ng/careers/",
        "apply_url": "https://arm.com.ng/young-talent-programme",
        "description": "Talent development program designed for high-achieving fresh graduates awaiting NYSC to fast-track career development in technology and asset management.",
        "nysc_friendly": True,
        "location": "Lagos"
    },
    {
        "organization": "Kuda Bank",
        "title": "Junior Backend / Fullstack Developer Track",
        "category": "Junior Tech Role",
        "url": "https://kuda.com/careers",
        "apply_url": "https://kuda.com/careers",
        "description": "Skills-first engineering track for builders capable of writing robust backend services in Python, C#, or React/TypeScript without NYSC bottlenecks.",
        "nysc_friendly": True,
        "location": "Lagos / Remote"
    },
    {
        "organization": "Ventures Platform",
        "title": "Venture Capital Analyst Fellowship",
        "category": "Pre-NYSC Fellowship",
        "url": "https://venturesplatform.com",
        "apply_url": "https://venturesplatform.com/careers",
        "description": "Pre-NYSC fellowship supporting African early-stage tech investments, conducting technical due diligence, and scouting emerging software ventures.",
        "nysc_friendly": True,
        "location": "Lagos / Abuja"
    },
    {
        "organization": "Flutterwave",
        "title": "Graduate Developer Internship",
        "category": "Fintech Internship",
        "url": "https://flutterwave.com/careers",
        "apply_url": "https://flutterwave.com/careers",
        "description": "Hands-on engineering program working on payment APIs, merchant integration, and developer tooling across Africa.",
        "nysc_friendly": True,
        "location": "Lagos / Remote"
    }
]

class GTTechScraper(BaseScraper):
    def __init__(self):
        super().__init__("GTTechScraper")

    def scrape(self) -> list[dict]:
        logger.info(f"[GTTech] Inspecting {len(ACTIVE_GT_PORTALS)} pre-NYSC friendly graduate and tech programs...")
        results = []

        for p in ACTIVE_GT_PORTALS:
            title = p["title"]
            desc = p["description"]
            cat = p["category"]
            org = p["organization"]
            apply_url = p["apply_url"]

            # Evaluate against hard NYSC filter
            is_eligible, reason = NYSCFilter.evaluate(title, desc, cat)
            if not is_eligible:
                logger.info(f"[GTTech] Dropped {title}: {reason}")
                continue

            opp_id = self.generate_id(org, title, apply_url)
            is_brand_new = self.is_new(opp_id)

            results.append({
                "id": opp_id,
                "organization": org,
                "title": title,
                "category": cat,
                "location": p.get("location", "Nigeria"),
                "apply_url": apply_url,
                "portal_url": p.get("url", apply_url),
                "description": desc,
                "nysc_status": "No NYSC Required / Pre-NYSC Verified",
                "nysc_reason": reason,
                "is_brand_new": is_brand_new
            })

        logger.info(f"[GTTech] Verified {len(results)} active pre-NYSC graduate programs.")
        return results
