import requests
import zlib
from pybloom_live import BloomFilter # You will need to pip install this
import json

# 1. Sources of Truth (Free & Open Source)
SOURCES = [
    "https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/config.json",
    "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE-ONLY.txt"
]

def fetch_scam_data():
    scam_domains = set()
    
    # Fetch MetaMask List
    try:
        r = requests.get(SOURCES[0])
        data = r.json()
        scam_domains.update(data.get('blacklist', []))
    except Exception as e: print(f"Error fetching MetaMask: {e}")

    # Fetch Phishing Database
    try:
        r = requests.get(SOURCES[1])
        lines = r.text.splitlines()
        scam_domains.update([line.strip() for line in lines if line.strip()])
    except Exception as e: print(f"Error fetching PhishDB: {e}")

    return scam_domains

def build_filter():
    domains = fetch_scam_data()
    print(f"Total scam domains found: {len(domains)}")

    # Create a Bloom Filter (Error rate 0.1%, Capacity for 200k items)
    bf = BloomFilter(capacity=200000, error_rate=0.001)
    
    for domain in domains:
        bf.add(domain)

    # Serialize and Save
    # We save as a bit-array to keep it tiny
    with open("scam_filter.bin", "wb") as f:
        bf.tofile(f)
    
    # Save a small version info file
    with open("version.json", "w") as f:
        json.dump({"count": len(domains), "updated": "2023-10-27"}, f)

if __name__ == "__main__":
    build_filter()
