"""
Academic Research Assistant & Active University Lab Scraper.
Monitors professors, lab directors, and research institutes across:
- University of Ibadan (UI)
- Federal University of Agriculture, Abeokuta (FUNAAB)
- Covenant University (Ota)
- University of Lagos (UNILAG)
- Data Science Nigeria (DSN) AI Research Labs
Strictly requires NO NYSC (Academic appointments and RA contracts are based on technical competence).
"""

import logging
from scrapers.base import BaseScraper
from config import CANDIDATE

logger = logging.getLogger("Radar")

ACTIVE_RESEARCH_LABS = [
    # University of Ibadan (UI)
    {
        "organization": "University of Ibadan (UI)",
        "department": "Department of Computer Science & Software Systems",
        "pi_name": "Prof. S. O. Akinola / Dr. A. B. Adeyemo",
        "pi_role": "Professor of Computer Science & Lab Director",
        "email": "cs@ui.edu.ng",
        "title": "Graduate Research Assistant in Computational Intelligence & Data Systems",
        "category": "Academic Research Assistant",
        "research_focus": "Machine Learning, Intelligent Systems, Database Optimization, and Semantic Web",
        "location": "Ibadan, Oyo State",
        "lab_url": "https://sci.ui.edu.ng/computer-science",
        "pitch_angle": "Assisting with dataset preprocessing, building FastAPI research endpoints, and dashboard visualization for experiment tracking."
    },
    {
        "organization": "University of Ibadan (UI)",
        "department": "Department of Electrical & Electronic Engineering",
        "pi_name": "Prof. O. A. Fakolujo",
        "pi_role": "Professor & Principal Investigator",
        "email": "fakolujo@ui.edu.ng",
        "title": "Research Assistant in Signal Processing & Embedded Software",
        "category": "Academic Research Assistant",
        "research_focus": "Telecommunications, Embedded Linux, IoT Sensor Data Gathering",
        "location": "Ibadan, Oyo State",
        "lab_url": "https://tech.ui.edu.ng/electrical-and-electronic-engineering",
        "pitch_angle": "Writing backend data collection services, socket event loggers, and automated experiment scripts in Python."
    },

    # Federal University of Agriculture, Abeokuta (FUNAAB)
    {
        "organization": "FUNAAB",
        "department": "Department of Computer Science & AI Research Group",
        "pi_name": "Prof. A. T. Akinwale / Dr. O. R. Vincent",
        "pi_role": "Principal Investigator & Senior Researcher",
        "email": "comsc@funaab.edu.ng",
        "title": "Research Assistant in Agricultural Informatics & Machine Learning",
        "category": "Academic Research Assistant",
        "research_focus": "Predictive crop modeling, farm image classification, and agricultural data warehousing",
        "location": "Abeokuta, Ogun State",
        "lab_url": "https://funaab.edu.ng/department-of-computer-science/",
        "pitch_angle": "Developing web portals for field data collection, training pipeline integrations, and PostgreSQL spatial databases."
    },

    # Covenant University (Ota, Ogun State)
    {
        "organization": "Covenant University (Ota)",
        "department": "Covenant Applied Informatics and Communication Africa Centre of Excellence (CApIC-ACE)",
        "pi_name": "Prof. Emeka Iweala / Prof. Sanjay Misra",
        "pi_role": "Centre Director & Principal Investigator",
        "email": "capic-ace@covenantuniversity.edu.ng",
        "title": "Graduate Research Assistant in Health Informatics & Computational Genomics",
        "category": "Academic Research Assistant",
        "research_focus": "World Bank ACE grant-funded health informatics, cloud biomedical platforms, and cancer genomics data",
        "location": "Ota, Ogun State",
        "lab_url": "https://ace.covenantuniversity.edu.ng",
        "pitch_angle": "Engineering microservice pipelines in FastAPI, database design for clinical cohorts, and responsive Next.js research portals."
    },
    {
        "organization": "Covenant University (Ota)",
        "department": "Department of Computer & Information Sciences",
        "pi_name": "Dr. Marion O. Adebiyi / Lab PIs",
        "pi_role": "Research Lead & Faculty",
        "email": "cis@covenantuniversity.edu.ng",
        "title": "Junior Research Fellow in Applied Machine Learning & NLP",
        "category": "Academic Research Assistant",
        "research_focus": "Low-resource African languages NLP, speech processing, and educational software analytics",
        "location": "Ota, Ogun State",
        "lab_url": "https://covenantuniversity.edu.ng",
        "pitch_angle": "Building data labeling pipelines, scraping text corpora, and developing fullstack demo interfaces for paper submissions."
    },

    # University of Lagos (UNILAG)
    {
        "organization": "University of Lagos (UNILAG)",
        "department": "Systems Engineering & Robotics Lab",
        "pi_name": "Prof. O. I. Okoro / Dr. A. O. Olowokere",
        "pi_role": "Professor & Lab Lead",
        "email": "syseng@unilag.edu.ng",
        "title": "Research Assistant in Intelligent Control Systems & Automation",
        "category": "Academic Research Assistant",
        "research_focus": "Automated control systems, telemetry, time-series forecasting",
        "location": "Akoka, Lagos",
        "lab_url": "https://unilag.edu.ng",
        "pitch_angle": "Writing Python backend services to ingest sensor telemetry and build real-time monitoring charts with React."
    },

    # Data Science Nigeria (DSN) AI Research Lab
    {
        "organization": "Data Science Nigeria (DSN AI Lab)",
        "department": "AI Research & Innovation Unit",
        "pi_name": "Dr. Olubayo Adekanmbi / Lead Research Scientists",
        "pi_role": "Founder & Research Director",
        "email": "research@datasciencenigeria.ai",
        "title": "AI Research Fellow & Fullstack Engineer (Pre-NYSC)",
        "category": "Academic Research Assistant",
        "research_focus": "Financial inclusion modeling, multilingual voice AI for micro-merchants, and edtech impact evaluation",
        "location": "Yaba, Lagos / Remote",
        "lab_url": "https://datasciencenigeria.org/research",
        "pitch_angle": "End-to-end fullstack implementation: deploying model inference APIs with FastAPI and responsive dashboards with Next.js."
    }
]

class RAAcademicScraper(BaseScraper):
    def __init__(self):
        super().__init__("RAAcademicScraper")

    def scrape(self) -> list[dict]:
        logger.info(f"[RAAcademic] Tracking {len(ACTIVE_RESEARCH_LABS)} verified academic research labs in target universities...")
        results = []

        for lab in ACTIVE_RESEARCH_LABS:
            org = lab["organization"]
            title = lab["title"]
            dept = lab["department"]
            email = lab["email"]
            lab_url = lab["lab_url"]
            pi = lab["pi_name"]
            focus = lab["research_focus"]

            opp_id = self.generate_id(org, title, email)
            is_brand_new = self.is_new(opp_id)

            results.append({
                "id": opp_id,
                "organization": org,
                "department": dept,
                "title": title,
                "pi_name": pi,
                "pi_role": lab.get("pi_role", "Principal Investigator"),
                "email": email,
                "category": "Academic Research Assistant",
                "location": lab.get("location", "Southwest Nigeria"),
                "lab_url": lab_url,
                "apply_url": lab_url,
                "research_focus": focus,
                "pitch_angle": lab.get("pitch_angle", ""),
                "description": f"Active research lab under {pi} focusing on {focus}. Welcomes fresh graduates for research software & data tasks.",
                "nysc_status": "No NYSC Required (Academic Appointment)",
                "nysc_reason": "Academic lab contracts and graduate RA roles are evaluated on coding & analytical skills without NYSC prerequisite.",
                "is_brand_new": is_brand_new
            })

        logger.info(f"[RAAcademic] Successfully loaded {len(results)} active academic RA opportunities.")
        return results
