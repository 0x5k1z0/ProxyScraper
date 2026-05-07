"""Scrape from spys.one."""
import re
import requests
from bs4 import BeautifulSoup
from typing import List

from . import BaseScraper, Proxy


class SpysOneScraper(BaseScraper):
    """Scrape from spys.one."""

    def get_source_name(self) -> str:
        return "spys.one"

    def scrape(self, proxy_type: str = "HTTP", country: str = "", anonymity: str = "") -> List[Proxy]:
        self.proxies = []
        try:
            url = "https://spys.one/en/free-proxy-list/"
            data = {
                "xf0": proxy_type,
                "xxf1": proxy_type,
                "xxf2": country if country else "0",
                "xxf3": anonymity if anonymity else "0",
                "xxf4": "0",
                "xxf5": "0",
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://spys.one/en/free-proxy-list/",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = requests.post(url, headers=headers, data=data, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+).*?<font.*?>[:](\d+)</font>")

            table = soup.find("table", class_="spy14")
            if table:
                rows = table.find_all("tr", class_="spy14")
                for row in rows[1:]:
                    tds = row.find_all("td")
                    if len(tds) >= 2:
                        first_td = tds[0]

                        ip_script = first_td.find("script")
                        if ip_script:
                            ip_match = re.search(r"document\.write\(\s*\"([^\"]+)\"\s*\+\s*\"([^\"]+)\"\s*\)", ip_script.text)
                            if ip_match:
                                ip = ip_match.group(1) + ip_match.group(2)
                            else:
                                ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", first_td.text)
                                ip = ip_match.group(1) if ip_match else ""
                        else:
                            ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", first_td.text)
                            ip = ip_match.group(1) if ip_match else ""

                        port_td = tds[1]
                        port_script = port_td.find("script")
                        if port_script:
                            port_match = re.search(r"\)\^(\d+)", port_script.text)
                            if port_match:
                                try:
                                    xor_key = int(port_match.group(1))
                                    port_match2 = re.search(r"\\(\d+)", port_script.text)
                                    if port_match2:
                                        port = str(int(port_match2.group(1)) ^ xor_key)
                                    else:
                                        port = ""
                                except ValueError:
                                    port = ""
                            else:
                                port_match = re.search(r"[:](\d+)", first_td.text)
                                port = port_match.group(1) if port_match else ""
                        else:
                            port_match = re.search(r"[:](\d+)", port_td.text)
                            port = port_match.group(1) if port_match else ""

                        if ip and port:
                            country = ""
                            if len(tds) >= 3:
                                country = tds[2].text.strip().split(" ")[0]

                            anonymity = ""
                            if len(tds) >= 5:
                                anon_text = tds[4].text.strip()
                                if "Elite" in anon_text or "Level" in anon_text:
                                    anonymity = "elite"
                                elif "Anonymous" in anon_text:
                                    anonymity = "anonymous"
                                elif "Transparent" in anon_text:
                                    anonymity = "transparent"

                            self.proxies.append(Proxy(
                                ip=ip,
                                port=port,
                                protocol=proxy_type,
                                country=country,
                                anonymity=anonymity,
                            ))
        except Exception:
            pass

        return self.proxies
