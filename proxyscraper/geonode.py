"""Scrape from geonode.com (API)."""
import requests
from typing import List

from . import BaseScraper, Proxy


class GeonodeScraper(BaseScraper):
    """Scrape from geonode.com via API."""

    def get_source_name(self) -> str:
        return "geonode.com"

    def scrape(self, limit: int = 500, protocol: str = "http") -> List[Proxy]:
        self.proxies = []
        try:
            url = "https://proxylist.geonode.com/api/proxy-list"
            params = {
                "limit": limit,
                "page": 1,
                "sort_by": "lastChecked",
                "sort_type": "desc",
                "protocols": protocol,
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            }

            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            if "data" in data:
                for item in data["data"]:
                    ip = item.get("ip", "")
                    port = str(item.get("port", ""))
                    if ip and port:
                        protocols = item.get("protocols", [])
                        country = item.get("country", "")
                        anonymity = item.get("anonymityLevel", "unknown")
                        response_time = item.get("responseTime", 0)
                        uptime = item.get("uptime", 0)

                        proto = protocols[0].upper() if protocols else "HTTP"

                        self.proxies.append(Proxy(
                            ip=ip,
                            port=port,
                            protocol=proto,
                            country=country,
                            anonymity=anonymity,
                            response_time=response_time,
                            uptime=uptime,
                        ))
        except Exception:
            pass

        return self.proxies
