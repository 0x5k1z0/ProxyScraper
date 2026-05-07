"""Base scraper class."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class Proxy:
    """Represents a scraped proxy."""
    ip: str
    port: str
    protocol: str = "HTTP"
    country: str = ""
    anonymity: str = "unknown"
    response_time: float = 0.0
    last_checked: str = ""
    uptime: float = 0.0

    @property
    def address(self) -> str:
        return f"{self.ip}:{self.port}"

    def __hash__(self):
        return hash(self.address)

    def __eq__(self, other):
        if isinstance(other, Proxy):
            return self.address == other.address
        return False


class BaseScraper(ABC):
    """Base class for all proxy scrapers."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.proxies: List[Proxy] = []

    @abstractmethod
    def scrape(self) -> List[Proxy]:
        """Scrape proxies from the source."""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the scraper source."""
        pass
