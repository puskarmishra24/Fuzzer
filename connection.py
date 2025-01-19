from zapv2 import ZAPv2
import time
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# Suppress insecure HTTPS warnings
urllib3.disable_warnings(InsecureRequestWarning)

def connect_to_zap(zap_url):
    retries = 3
    for attempt in range(retries):
        try:
            zap = ZAPv2(proxies={"http": zap_url, "https": zap_url}, apikey="l28p9arrq21295l3kqdqv5kurg")
            # Check if the API is accessible
            if zap.core.version:
                return zap
        except Exception:
            print(f"Retry {attempt + 1} of {retries}...")
            time.sleep(3)
    return None

def get_zap_version(zap):
    return zap.core.version
