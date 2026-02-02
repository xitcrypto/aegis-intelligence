import requests
import json

SOURCES = [
    "https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/config.json",
    "https://raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/domains.json"
]

def update_intelligence():
    scam_domains = set()
    # Fetch MetaMask List
    try:
        r = requests.get(SOURCES[0]).json()
        scam_domains.update(r.get('blacklist', []))
    except: pass
    
    # Fetch ScamSniffer List
    try:
        r = requests.get(SOURCES[1]).json()
        scam_domains.update(r)
    except: pass

    # Save as a simple JSON list (Aegis will download this)
    with open("scam_list.json", "w") as f:
        json.dump(list(scam_domains), f)

if __name__ == "__main__":
    update_intelligence()
