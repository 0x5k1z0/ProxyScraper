# ProxyScraper Pro

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge)
![OpenBullet2](https://img.shields.io/badge/OpenBullet2-Compatible-red?style=for-the-badge)

**Professional Proxy Scraper & Validator for OpenBullet2**

Scrape, validate, and export high-quality proxies from multiple sources with multi-threaded checking and OpenBullet2-compatible output formats.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Export Formats](#-export-formats) • [API](#-python-api)

</div>

---

## 🎯 Features

### Scraping
- **6 Premium Sources** - Free-proxy-list, ProxyScrape, OpenProxy, Proxy-List.Download, Geonode, Spys.one
- **Multi-threaded** - Concurrent scraping for maximum speed
- **Deduplication** - Automatic removal of duplicate proxies
- **Protocol Support** - HTTP, HTTPS, SOCKS4, SOCKS5
- **Anonymity Detection** - Elite, Anonymous, Transparent

### Validation
- **Multi-threaded Checking** - Up to 200+ concurrent threads
- **Response Time Measurement** - Speed-based sorting
- **Anonymity Verification** - Real anonymity level verification
- **Protocol Filtering** - Filter by protocol type
- **Speed Filtering** - Exclude slow proxies

### Export
- **OpenBullet2 Format** - `PROTOCOL|IP:PORT` ready to import
- **Multiple Formats** - ip:port, protocol://ip:port, ip:port:user:pass, etc.
- **Protocol Splitting** - Export separate files by protocol
- **Statistics** - Detailed proxy analytics

---

## 📦 Installation

### Requirements
- Python 3.10+
- pip

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/proxyscraper.git
cd proxyscraper

# Install dependencies
pip install -r requirements.txt

# That's it!
```

---

## 🚀 Usage

### Basic Commands

```bash
# Scrape all sources and validate
python main.py scrape

# Scrape only (skip validation)
python main.py scrape --no-check

# Show available sources
python main.py info
```

### OpenBullet2 Export

```bash
# Export in OpenBullet2 format
python main.py scrape --ob-format --save ob_proxies.txt

# Split by protocol (HTTP, HTTPS, SOCKS4, SOCKS5)
python main.py scrape --ob-format --separate

# HTTPS proxies only
python main.py scrape --protocol HTTPS --ob-format
```

### Advanced Filtering

```bash
# Elite proxies only
python main.py scrape --anonymity elite --ob-format

# Fast proxies only (under 500ms)
python main.py scrape --max-speed 500 --stats

# Custom threads + timeout
python main.py scrape --threads 200 --check-timeout 3

# Specific sources only
python main.py scrape --sources free-proxy-list.net proxyscrape.com
```

### Full Example

```bash
python main.py scrape \
  --protocol HTTPS \
  --anonymity elite \
  --max-speed 1000 \
  --threads 150 \
  --ob-format \
  --separate \
  --stats \
  --save proxies_elite_https.txt
```

---

## 📋 CLI Options

### Scrape Command

| Option | Description | Default |
|--------|-------------|---------|
| `--sources` | Specific scrapers to use | All sources |
| `--protocol` | Filter by protocol (HTTP/HTTPS/SOCKS4/SOCKS5) | All |
| `--anonymity` | Filter by anonymity (elite/anonymous/transparent) | All |
| `--max-speed` | Max response time in ms | No limit |
| `--threads` | Threads for checking | 100 |
| `--timeout` | Scrape timeout (seconds) | 10 |
| `--check-timeout` | Check timeout (seconds) | 5 |
| `--check-anonymity` | Verify anonymity during check | False |
| `--no-check` | Skip proxy validation | False |
| `--save` | Output file path | proxies.txt |
| `--save-checked` | Output file for checked proxies | auto |
| `--format` | Proxy format string | ip:port |
| `--ob-format` | Export as OpenBullet2 format | False |
| `--separate` | Split output by protocol | False |
| `--stats` | Show proxy statistics | False |
| `--limit` | Limit number of proxies to save | No limit |

---

## 📤 Export Formats

| Format | Example | Use Case |
|--------|---------|----------|
| `ip:port` | `192.168.1.1:8080` | General use |
| `protocol://ip:port` | `https://192.168.1.1:8080` | Curl, requests |
| `ip:port:protocol` | `192.168.1.1:8080:HTTPS` | Some tools |
| `ip:port:country` | `192.168.1.1:8080:US` | Geo-filtered |
| `openbullet` | `HTTPS\|192.168.1.1:8080` | **OpenBullet2** |
| `ip:port:user:pass` | `192.168.1.1:8080:user:pass` | Auth proxies |

---

## 📊 Statistics Output

When using `--stats`, you'll see detailed analytics:

```
Statistics:

┌──────────────────┬──────────────────────┐
│ Total Proxies    │ 1247                 │
│ Avg Speed        │ 342.15ms             │
│ Fastest          │ 45.23ms              │
│ Protocols        │ HTTPS: 823, HTTP: 424│
│ Anonymity        │ elite: 891, anon: 356│
│ Top Countries    │ US: 412, DE: 198     │
└──────────────────┴──────────────────────┘
```

---

## 🔌 Python API

```python
from proxyscraper.scraper.aggregator import ProxyAggregator
from proxyscraper.validators.validator import ProxyValidator
from proxyscraper.exporters.exporter import ProxyExporter

# Scrape
aggregator = ProxyAggregator(timeout=10)
proxies = aggregator.get_all_proxies()

# Validate
validator = ProxyValidator(timeout=5, max_threads=100)
valid_proxies = validator.validate_all(
    proxies,
    protocol_filter="HTTPS",
    min_speed=500,
    check_anon=True,
)

# Export
exporter = ProxyExporter(valid_proxies)
exporter.export_openbullet("ob_proxies.txt")
exporter.export("proxies.txt", fmt="ip:port", protocol="HTTPS")

# Stats
stats = exporter.get_stats()
print(stats)
```

---

## 🗂️ Project Structure

```
proxyscraper/
├── main.py                          # CLI entry point
├── requirements.txt
├── proxyscraper/
│   ├── scraper/
│   │   ├── __init__.py              # Base scraper + Proxy class
│   │   ├── freeproxylist.py         # free-proxy-list.net
│   │   ├── proxyscrape.py           # proxyscrape.com API
│   │   ├── openproxy.py             # openproxy.space API
│   │   ├── proxylistdownload.py     # proxy-list.download API
│   │   ├── geonode.py               # geonode.com API
│   │   ├── spysone.py               # spys.one
│   │   └── aggregator.py            # Multi-scraper runner
│   ├── validators/
│   │   └── validator.py             # Multi-threaded validation
│   └── exporters/
│       └── exporter.py              # Format exporters
```

---

## 📝 Examples

### OpenBullet2 Ready

```bash
# Scrape elite HTTPS proxies, validate, export for OB2
python main.py scrape \
  --protocol HTTPS \
  --anonymity elite \
  --max-speed 800 \
  --threads 200 \
  --ob-format \
  --save ob_elite.txt
```

### SOCKS Proxies Only

```bash
python main.py scrape --no-check --protocol SOCKS5 --save socks5.txt
```

### Country-Specific

```bash
# Geonode provides country data
python main.py scrape --sources geonode.com --stats
```

---

## ⚡ Performance Tips

| Setting | Recommendation |
|---------|---------------|
| `--threads` | 100-200 for fast connections |
| `--check-timeout` | 3-5s for speed, 10s for thoroughness |
| `--max-speed` | 500-1000ms for quality proxies |
| `--anonymity elite` | Best for OB2, fewer but higher quality |

---

## ⚠️ Disclaimer

This tool is for educational and legitimate testing purposes only. The author is not responsible for any misuse of this software. Always ensure you have proper authorization before using proxies.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with 5K1Z0 ❤️**

⭐ Star this repo if you found it useful!

</div>
