"""Export proxies in various formats for OpenBullet2."""
import os
from typing import List, Optional

from ..scraper import Proxy


class ProxyExporter:
    """Export proxies in formats compatible with OpenBullet2."""

    def __init__(self, proxies: List[Proxy]):
        self.proxies = proxies

    def format_proxy(self, proxy: Proxy, fmt: str = "ip:port") -> str:
        """Format a single proxy string."""
        if fmt == "ip:port":
            return f"{proxy.ip}:{proxy.port}"
        elif fmt == "protocol://ip:port":
            return f"{proxy.protocol.lower()}://{proxy.ip}:{proxy.port}"
        elif fmt == "ip:port:protocol":
            return f"{proxy.ip}:{proxy.port}:{proxy.protocol}"
        elif fmt == "ip:port:country":
            return f"{proxy.ip}:{proxy.port}:{proxy.country}"
        elif fmt == "openbullet":
            return f"{proxy.protocol}|{proxy.ip}:{proxy.port}"
        elif fmt == "ip:port:user:pass":
            return f"{proxy.ip}:{proxy.port}::"
        else:
            return f"{proxy.ip}:{proxy.port}"

    def export(
        self,
        filepath: str,
        fmt: str = "ip:port",
        max_proxies: Optional[int] = None,
        min_speed: Optional[float] = None,
        protocol: Optional[str] = None,
        sort_by: str = "speed",
    ) -> str:
        """Export proxies to file."""
        proxies = self.proxies.copy()

        if protocol:
            proxies = [p for p in proxies if p.protocol.upper() == protocol.upper()]

        if min_speed:
            proxies = [p for p in proxies if p.response_time <= min_speed and p.response_time > 0]

        if sort_by == "speed":
            proxies.sort(key=lambda p: p.response_time if p.response_time > 0 else 99999)
        elif sort_by == "country":
            proxies.sort(key=lambda p: p.country)

        if max_proxies:
            proxies = proxies[:max_proxies]

        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w") as f:
            for proxy in proxies:
                f.write(self.format_proxy(proxy, fmt) + "\n")

        return filepath

    def export_openbullet(
        self,
        filepath: str,
        max_proxies: Optional[int] = None,
    ) -> str:
        """Export in OpenBullet2 proxy format: PROTOCOL|IP:PORT."""
        proxies = self.proxies.copy()
        proxies.sort(key=lambda p: p.response_time if p.response_time > 0 else 99999)

        if max_proxies:
            proxies = proxies[:max_proxies]

        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w") as f:
            for proxy in proxies:
                f.write(f"{proxy.protocol.upper()}|{proxy.ip}:{proxy.port}\n")

        return filepath

    def export_by_protocol(
        self,
        base_path: str,
        fmt: str = "ip:port",
    ) -> List[str]:
        """Export proxies grouped by protocol into separate files."""
        files = []
        protocols = {}

        for proxy in self.proxies:
            proto = proxy.protocol.upper()
            if proto not in protocols:
                protocols[proto] = []
            protocols[proto].append(proxy)

        base_dir = os.path.dirname(base_path)
        base_name = os.path.splitext(os.path.basename(base_path))[0]

        for proto, proxies in protocols.items():
            proxies.sort(key=lambda p: p.response_time if p.response_time > 0 else 99999)
            filename = f"{base_name}_{proto.lower()}.txt"
            filepath = os.path.join(base_dir, filename)

            with open(filepath, "w") as f:
                for proxy in proxies:
                    f.write(self.format_proxy(proxy, fmt) + "\n")

            files.append(filepath)

        return files

    def get_stats(self) -> dict:
        """Get proxy statistics."""
        if not self.proxies:
            return {"total": 0}

        protocols = {}
        countries = {}
        anonymity = {}
        speeds = []

        for p in self.proxies:
            protocols[p.protocol] = protocols.get(p.protocol, 0) + 1
            if p.country:
                countries[p.country] = countries.get(p.country, 0) + 1
            anonymity[p.anonymity] = anonymity.get(p.anonymity, 0) + 1
            if p.response_time > 0:
                speeds.append(p.response_time)

        return {
            "total": len(self.proxies),
            "protocols": dict(sorted(protocols.items(), key=lambda x: x[1], reverse=True)),
            "countries": dict(sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]),
            "anonymity": dict(sorted(anonymity.items(), key=lambda x: x[1], reverse=True)),
            "avg_speed_ms": round(sum(speeds) / len(speeds), 2) if speeds else 0,
            "fastest_ms": round(min(speeds), 2) if speeds else 0,
            "slowest_ms": round(max(speeds), 2) if speeds else 0,
        }
