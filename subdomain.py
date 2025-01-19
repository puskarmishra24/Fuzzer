import dns.resolver
import concurrent.futures
import requests
from datetime import datetime
import sys
import time
import json
from urllib.parse import urlparse
import re

class SubdomainScanner:
    def __init__(self, domain: str):
        # Clean up the domain input
        parsed = urlparse(domain if '://' in domain else 'http://' + domain)
        self.domain = parsed.netloc if parsed.netloc else parsed.path
        self.domain = self.domain.strip('/')
        
        self.threads = 10
        self.results = []
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 2
        self.resolver.lifetime = 2
        self.resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']

    def load_wordlist(self) -> list:
        try:
            with open('wordlist.txt', 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print("Error: wordlist.txt file not found in current directory")
            sys.exit(1)

    def check_subdomain(self, subdomain: str) -> dict:
        full_domain = f"{subdomain}.{self.domain}"
        result = {
            "subdomain": full_domain,
            "status": "not_found",
            "ip_addresses": [],
            "http_status": None,
            "https_status": None
        }

        try:
            answers = self.resolver.resolve(full_domain, 'A')
            result["status"] = "found"
            result["ip_addresses"] = [str(rdata) for rdata in answers]

            for protocol in ['http', 'https']:
                try:
                    response = requests.get(
                        f"{protocol}://{full_domain}",
                        timeout=5,
                        verify=False,
                        allow_redirects=True
                    )
                    result[f"{protocol}_status"] = response.status_code
                except requests.RequestException:
                    pass

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            pass
        except dns.resolver.Timeout:
            result["status"] = "timeout"
        except Exception as e:
            result["status"] = f"error: {str(e)}"

        return result

    def scan(self) -> None:
        wordlist = self.load_wordlist()
        start_time = time.time()
        print(f"\nStarting scan of {self.domain} with {len(wordlist)} potential subdomains...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_subdomain = {
                executor.submit(self.check_subdomain, subdomain): subdomain 
                for subdomain in wordlist
            }

            completed = 0
            for future in concurrent.futures.as_completed(future_to_subdomain):
                completed += 1
                result = future.result()
                if result["status"] == "found":
                    self.results.append(result)
                    self.print_progress(result, completed, len(wordlist))

        self.save_results()
        print(f"\nScan completed in {time.time() - start_time:.2f} seconds")
        print(f"Found {len(self.results)} active subdomains")

    def print_progress(self, result: dict, completed: int, total: int) -> None:
        if result["status"] == "found":
            progress = (completed / total) * 100
            print(f"\rProgress: {progress:.1f}% | Found: {result['subdomain']} "
                  f"| IPs: {', '.join(result['ip_addresses'])}", end="")

    def save_results(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize domain name for filename
        safe_domain = re.sub(r'[<>:"/\\|?*]', '_', self.domain)
        filename = f"scan_{safe_domain}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                "domain": self.domain,
                "scan_date": timestamp,
                "total_found": len(self.results),
                "results": self.results
            }, f, indent=4)
        
        print(f"\nResults saved to {filename}")

# Main execution
if __name__ == "__main__":
    # Get domain from user input
    target_domain = input("Enter the target domain (e.g., example.com): ")
    
    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings()
    
    # Create and run scanner
    scanner = SubdomainScanner(target_domain)
    scanner.scan()