import re
import logging

logger = logging.getLogger("Radar")

# Phrases that indicate strict NYSC completion is mandatory
MANDATORY_NYSC_PATTERNS = [
    r"must\s+possess\s+(?:an\s+)?nysc\s+discharge\s+certificate",
    r"evidence\s+of\s+nysc\s+(?:completion|discharge|exemption)",
    r"nysc\s+certificate\s+is\s+(?:mandatory|compulsory|required)",
    r"must\s+have\s+completed\s+(?:the\s+)?(?:mandatory\s+)?(?:nysc|national\s+youth\s+service)",
    r"completed\s+nysc",
    r"completion\s+of\s+nysc",
    r"nysc\s+discharge\s+or\s+exemption\s+letter",
    r"candidate\s+must\s+have\s+completed\s+national\s+service",
    r"upload\s+your\s+nysc\s+certificate"
]

# Phrases that explicitly welcome fresh graduates awaiting call-up
PRE_NYSC_PATTERNS = [
    r"awaiting\s+nysc",
    r"pre-nysc",
    r"pre\s+nysc",
    r"graduate\s+intern(?:ship)?",
    r"fresh\s+graduate",
    r"waiting\s+for\s+call-up",
    r"corps\s+member",
    r"prospective\s+corps\s+member"
]

class NYSCFilter:
    @staticmethod
    def evaluate(title: str, description: str, category: str) -> tuple[bool, str]:
        """
        Returns (is_eligible, reason)
        If eligible is False, the role is HARD BLOCKED due to NYSC mandate.
        """
        combined = f"{title} {description}".lower()

        # Rule 1: Academic Research Assistant roles NEVER require NYSC
        if "research assistant" in category.lower() or "academic lab" in category.lower():
            return True, "Academic RA: No NYSC requirement (University Research)"

        # Rule 2: Explicit pre-NYSC verification
        for p in PRE_NYSC_PATTERNS:
            if re.search(p, combined):
                return True, "Pre-NYSC Friendly: Explicitly welcomes awaiting-NYSC/fresh grads"

        # Rule 3: Check for mandatory NYSC blockers
        for pattern in MANDATORY_NYSC_PATTERNS:
            match = re.search(pattern, combined)
            if match:
                logger.info(f"[NYSC Blocked] Filtered out role: '{title}' - Trigger: '{match.group(0)}'")
                return False, f"Hard Blocked: Mandates NYSC ({match.group(0)})"

        # Rule 4: Software Engineering & Tech Scaleup GTs (Default to eligible if no NYSC mentioned)
        if any(tech in title.lower() for tech in ["software", "developer", "engineering", "backend", "fullstack", "tech"]):
            return True, "Tech Role: Skills-based qualification (No NYSC clause)"

        # General roles with no explicit NYSC mandate
        return True, "Eligible: No NYSC barrier specified"
