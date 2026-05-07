"""Aggregator to run all scrapers."""
import threading
from typing import List, Optional

from . import BaseScraper, Proxy
from .freeproxylist import FreeProxyListScraper
from .proxyscrape import ProxyScrapeScraper
from .openproxy import OpenProxyScraper
from .proxylistdownload import ProxyListDownloadScraper
from .geonode import GeonodeScraper
from .spysone import SpysOneScraper


ALL_SCRAPERS = [
    FreeProxyListScraper,
    ProxyScrapeScraper,
    OpenProxyScraper,
    ProxyListDownloadScraper,
    GeonodeScraper,
    SpysOneScraper,
]


class ProxyAggregator:
    """Run multiple scrapers and aggregate results."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.scrapers: List[BaseScraper] = []

    def get_all_proxies(self, scraper_names: Optional[List[str]] = None, **kwargs) -> List[Proxy]:
        """Run scrapers and return deduplicated proxy list."""
        if scraper_names:
            self.scrapers = [
                s(timeout=self.timeout)
                for s in ALL_SCRAPERS
                if s(timeout=self.timeout).get_source_name() in scraper_names
            ]
        else:
            self.scrapers = [s(timeout=self.timeout) for s in ALL_SCRAPERS]

        all_proxies = []
        threads = []

        def run_scraper(scraper: BaseScraper, **kw):
            try:
                proxies = scraper.scrape(**kw)
                all_proxies.extend(proxies)
            except Exception:
                pass

        for scraper in self.scrapers:
            t = threading.Thread(target=run_scraper, args=(scraper,), kwargs=kwargs)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        deduplicated = list(dict.fromkeys(all_proxies))
        return deduplicated

    def get_scrapers_info(self) -> List[str]:
        """Return list of available scraper names."""
        return [s(timeout=1).get_source_name() for s in ALL_SCRAPERS]
