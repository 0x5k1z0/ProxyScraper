"""Scrape from openproxy.space (API)."""
import requests
from typing import List

from . import BaseScraper, Proxy


class OpenProxyScraper(BaseScraper):
    """Scrape from openproxy.space via API."""

    API_URLS = [
        "https://openproxy.space/api/http",
        "https://openproxy.space/api/socks4",
        "https://openproxy.space/api/socks5",
    ]

    def get_source_name(self) -> str:
        return "openproxy.space"

    def scrape(self) -> List[Proxy]:
        self.proxies = []
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            }

            for api_url in self.API_URLS:
                response = requests.get(api_url, headers=headers, timeout=self.timeout)
                response.raise_for_status()

                data = response.json()
                if "data" in data and "list" in data["data"]:
                    protocol = api_url.split("/")[-1].upper()
                    for proxy_str in data["data"]["list"]:
                        if ":" in proxy_str:
                            parts = proxy_str.split(":")
                            ip = parts[0]
                            port = parts[1]

                            self.proxies.append(Proxy(
                                ip=ip,
                                port=port,
                                protocol=protocol,
                            ))
        except Exception:
            pass

        return self.proxies
