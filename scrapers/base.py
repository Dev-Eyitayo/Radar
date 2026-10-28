"""
Base Scraper Client with state hashing, date parsing, and error resilience.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
import requests
from config import SEEN_DB_PATH

logger = logging.getLogger("Radar")

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

class BaseScraper:
    def __init__(self, name: str):
        self.name = name
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.timeout = 10
        self.seen_ids = self._load_seen_db()

    def _load_seen_db(self) -> set[str]:
        if SEEN_DB_PATH.exists():
            try:
                with open(SEEN_DB_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data.keys())
            except Exception as e:
                logger.warning(f"Could not read seen DB: {e}")
        return set()

    def generate_id(self, organization: str, title: str, url: str) -> str:
        key = f"{organization.strip().lower()}|{title.strip().lower()}|{url.strip().lower()}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def is_new(self, opp_id: str) -> bool:
        return opp_id not in self.seen_ids

    def get(self, url: str, params: dict = None, headers: dict = None) -> requests.Response | None:
        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            if resp.status_code == 200:
                return resp
            logger.debug(f"[{self.name}] GET {url} status {resp.status_code}")
        except Exception as e:
            logger.debug(f"[{self.name}] GET {url} failed: {e}")
        return None

    def post(self, url: str, json_data: dict = None, headers: dict = None) -> requests.Response | None:
        try:
            resp = self.session.post(url, json=json_data, headers=headers, timeout=self.timeout)
            if resp.status_code == 200:
                return resp
            logger.debug(f"[{self.name}] POST {url} status {resp.status_code}")
        except Exception as e:
            logger.debug(f"[{self.name}] POST {url} failed: {e}")
        return None
