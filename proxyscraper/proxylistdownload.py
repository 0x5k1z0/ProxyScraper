"""Scrape from proxy-list.download (API)."""
import requests
from typing import List

from . import BaseScraper, Proxy


class ProxyListDownloadScraper(BaseScraper):
    """Scrape from proxy-list.download via API."""

    API_URLS = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=json&timeout=5000",
    ]

    def get_source_name(self) -> str:
        return "proxy-list.download"

    def scrape(self, protocol: str = "all", country: str = "all", anonymity: str = "all") -> List[Proxy]:
        self.proxies = []
        try:
            url = "https://www.proxy-list.download/api/v1/get"
            params = {
                "type": protocol,
                "country": country,
                "anon": anonymity,
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            }

            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            for line in response.text.strip().split("\n"):
                line = line.strip()
                if line and ":" in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        ip = parts[0]
                        port = parts[1]
                        protocol = protocol.upper() if protocol != "all" else "HTTP"

                        self.proxies.append(Proxy(
                            ip=ip,
                            port=port,
                            protocol=protocol,
                        ))
        except Exception:
            pass

        return self.proxies
