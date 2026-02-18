import requests
import json
from datetime import datetime, timezone

SOURCES = [
    {
        "name": "MetaMask eth-phishing-detect",
        "url": "https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/config.json",
        "parser": "metamask"
    },
    {
        "name": "ScamSniffer Blacklist",
        "url": "https://raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/domains.json",
        "parser": "flat"
    }
]


def normalize_domain(raw):
    d = raw.strip().lower()
    for prefix in ["https://", "http://", "www."]:
        if d.startswith(prefix):
            d = d[len(prefix):]
    d = d.split("/")[0]
    return d


def fetch_metamask(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("blacklist", [])


def fetch_flat(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else []


PARSERS = {
    "metamask": fetch_metamask,
    "flat": fetch_flat
}


def main():
    all_domains = set()

    for source in SOURCES:
        try:
            parser = PARSERS[source["parser"]]
            domains = parser(source["url"])
            normalized = [normalize_domain(d) for d in domains if d.strip()]
            all_domains.update(normalized)
            print(f"  [+] {source['name']}: {len(domains)} raw -> {len(normalized)} normalized")
        except Exception as e:
            print(f"  [!] {source['name']} FAILED: {e}")

    all_domains.discard("")
    sorted_domains = sorted(all_domains)

    output = {
        "version": datetime.now(timezone.utc).strftime("%Y%m%d%H%M"),
        "updated": datetime.now(timezone.utc).isoformat(),
        "count": len(sorted_domains),
        "domains": sorted_domains
    }

    with open("scam_list.json", "w") as f:
        json.dump(output, f, separators=(',', ':'))

    print(f"\nDone - {len(sorted_domains)} unique domains written to scam_list.json")


if __name__ == "__main__":
    main()
