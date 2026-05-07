"""Scrape from proxy-scrape.com (API)."""
import requests
from typing import List

from . import BaseScraper, Proxy


class ProxyScrapeScraper(BaseScraper):
    """Scrape from proxy-scrape.com via API."""

    def get_source_name(self) -> str:
        return "proxyscrape.com"

    def scrape(self, protocol: str = "all", timeout: int = 10000, anonymity: str = "all") -> List[Proxy]:
        self.proxies = []
        try:
            url = "https://api.proxyscrape.com/v4/free-proxy-list/get"
            params = {
                "request": "displayproxies",
                "proxy_format": "ipport",
                "format": "json",
                "timeout": timeout,
                "country": "all",
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            }

            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            if "proxies" in data:
                for proxy_data in data["proxies"]:
                    ip = proxy_data.get("ip", "")
                    port = str(proxy_data.get("port", ""))
                    if ip and port:
                        proto = proxy_data.get("protocol", "HTTP").upper()
                        country = proxy_data.get("country", "")
                        anon = proxy_data.get("anonymity", "unknown")

                        self.proxies.append(Proxy(
                            ip=ip,
                            port=port,
                            protocol=proto,
                            country=country,
                            anonymity=anon,
                        ))
        except Exception:
            pass

        return self.proxies
