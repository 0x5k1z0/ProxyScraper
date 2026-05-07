"""Proxy validator with multi-threaded checking."""
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Optional

from ..scraper import Proxy


class ProxyValidator:
    """Validate proxies for speed, anonymity, and protocol."""

    TEST_URLS = {
        "http": "http://httpbin.org/ip",
        "https": "https://httpbin.org/ip",
    }

    def __init__(
        self,
        timeout: int = 5,
        max_threads: int = 100,
        test_url: Optional[str] = None,
    ):
        self.timeout = timeout
        self.max_threads = max_threads
        self.test_url = test_url
        self.valid_proxies: List[Proxy] = []
        self.progress_callback: Optional[Callable] = None
        self.total_checked = 0
        self.total_valid = 0

    def check_proxy(self, proxy: Proxy, protocol: Optional[str] = None) -> Optional[Proxy]:
        """Check a single proxy for connectivity and speed."""
        test_protocols = [protocol] if protocol else [proxy.protocol.lower()]

        for proto in test_protocols:
            proxy_dict = {
                "http": f"{proto.lower()}://{proxy.ip}:{proxy.port}",
                "https": f"{proto.lower()}://{proxy.ip}:{proxy.port}",
            }

            url = self.test_url or self.TEST_URLS.get(proto, self.TEST_URLS["http"])

            try:
                start_time = time.time()
                response = requests.get(
                    url,
                    proxies=proxy_dict,
                    timeout=self.timeout,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                )

                if response.status_code == 200:
                    response_time = (time.time() - start_time) * 1000
                    proxy.response_time = round(response_time, 2)
                    proxy.protocol = proto.upper()
                    return proxy

            except Exception:
                continue

        return None

    def check_anonymity(self, proxy: Proxy) -> str:
        """Check proxy anonymity level."""
        proxy_dict = {
            "http": f"{proxy.protocol.lower()}://{proxy.ip}:{proxy.port}",
            "https": f"{proxy.protocol.lower()}://{proxy.ip}:{proxy.port}",
        }

        try:
            response = requests.get(
                "https://httpbin.org/headers",
                proxies=proxy_dict,
                timeout=self.timeout,
            )

            if response.status_code == 200:
                headers = response.json().get("headers", {})
                has_via = "Via" in headers
                has_forwarded = "X-Forwarded-For" in headers

                if not has_via and not has_forwarded:
                    return "elite"
                elif has_forwarded:
                    return "transparent"
                else:
                    return "anonymous"

        except Exception:
            pass

        return proxy.anonymity

    def validate_all(
        self,
        proxies: List[Proxy],
        protocol_filter: Optional[str] = None,
        min_speed: Optional[float] = None,
        anonymity_level: Optional[str] = None,
        check_anon: bool = False,
    ) -> List[Proxy]:
        """Validate all proxies with multi-threading."""
        self.valid_proxies = []
        self.total_checked = 0
        self.total_valid = 0

        protocol = protocol_filter.lower() if protocol_filter else None

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_proxy = {
                executor.submit(self.check_proxy, p, protocol): p
                for p in proxies
            }

            for future in as_completed(future_to_proxy):
                self.total_checked += 1
                proxy = future_to_proxy[future]

                try:
                    result = future.result(timeout=self.timeout + 5)
                    if result:
                        if min_speed and result.response_time > min_speed:
                            continue

                        if check_anon:
                            result.anonymity = self.check_anonymity(result)

                        if anonymity_level and result.anonymity != anonymity_level:
                            if not (anonymity_level == "elite" and result.anonymity == "elite"):
                                if anonymity_level == "elite" and result.anonymity != "elite":
                                    continue
                                elif anonymity_level == "anonymous" and result.anonymity == "transparent":
                                    continue

                        self.total_valid += 1
                        self.valid_proxies.append(result)

                except Exception:
                    pass

                if self.progress_callback:
                    self.progress_callback(self.total_checked, len(proxies), self.total_valid)

        self.valid_proxies.sort(key=lambda p: p.response_time)
        return self.valid_proxies
