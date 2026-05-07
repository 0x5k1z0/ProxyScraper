"""Scrape from free-proxy-list.net."""
import requests
from bs4 import BeautifulSoup
from typing import List

from . import BaseScraper, Proxy


class FreeProxyListScraper(BaseScraper):
    """Scrape from free-proxy-list.net."""

    def get_source_name(self) -> str:
        return "free-proxy-list.net"

    def scrape(self, ssl: bool = True, anonymous: bool = True) -> List[Proxy]:
        self.proxies = []
        try:
            url = "https://free-proxy-list.net/"
            params = {}
            if ssl:
                params["ssl"] = "1"
            if anonymous:
                params["an"] = "1"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }

            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            table = soup.find("table", id="proxylisttable")
            if not table:
                return self.proxies

            for row in table.find("tbody").find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 8:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    code = cols[3].text.strip()
                    anonymity = cols[4].text.strip()
                    https = cols[6].text.strip()

                    protocol = "HTTPS" if https == "yes" else "HTTP"
                    if anonymity == "elite proxy":
                        anonymity = "elite"
                    elif anonymity == "anonymous":
                        anonymity = "anonymous"
                    else:
                        anonymity = "transparent"

                    self.proxies.append(Proxy(
                        ip=ip,
                        port=port,
                        protocol=protocol,
                        country=code,
                        anonymity=anonymity,
                    ))
        except Exception:
            pass

        return self.proxies
