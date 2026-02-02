import requests
import json
import os

# Sources of Truth
SOURCES = [
    "https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/config.json",
    "https://raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/domains.json"
]

def update_intelligence():
    scam_domains = set()
    
    # 1. Fetch MetaMask List
    try:
        r = requests.get(SOURCES[0], timeout=10)
        data = r.json()
        scam_domains.update(data.get('blacklist', []))
    except Exception as e:
        print(f"Error fetching MetaMask list: {e}")
    
    # 2. Fetch ScamSniffer List
    try:
        r = requests.get(SOURCES[1], timeout=10)
        data = r.json()
        scam_domains.update(data)
    except Exception as e:
        print(f"Error fetching ScamSniffer list: {e}")

    # Convert to list and sort for consistency
    final_list = sorted(list(scam_domains))
    
    # 3. Save as the JSON file the extension expects
    with open("scam_list.json", "w") as f:
        json.dump(final_list, f)

    # 4. Create an index.html so GitHub Pages stays "awake"
    with open("index.html", "w") as f:
        f.write(f"<html><body><h1>Aegis Intelligence Online</h1><p>Tracking {len(final_list)} threats.</p></body></html>")

    print(f"Success: Tracked {len(final_list)} scam domains.")

if __name__ == "__main__":
    update_intelligence()
