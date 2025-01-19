import subprocess

def zap_subdomain_discovery(domain, wordlist):
    print(f"Discovering subdomains for: {domain}")
    result = subprocess.run(
        ["amass", "enum", "-d", domain],
        capture_output=True,
        text=True
    )
    subdomains = result.stdout.splitlines()
    for sub in subdomains:
        print(f"Subdomain: {sub}")
    return subdomains

# Usage
subdomains = zap_subdomain_discovery("example.com", "wordlist.txt")