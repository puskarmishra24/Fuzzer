from datetime import datetime
import time
import requests
from termcolor import colored
import crawler
import attack
import report_generator
from connection import connect_to_zap, get_zap_version

def main():
    zap_url = "https://localhost:8081"
    api_key = "l28p9arrq21295l3kqdqv5kurg"

    print(colored("Initializing connection to ZAP...", "blue"))
    zap = connect_to_zap(zap_url)
    if not zap:
        print(colored("Failed to connect to ZAP after 3 retries.", "red"))
        return

    print(colored(f"Connection successful! ZAP Version: {get_zap_version(zap)}", "green"))
    create_zap_session(zap_url, api_key)

    target_urls = input("Enter the URLs you want to test, separated by commas: ").strip().split(',')
    
    # Initialize combined results dictionary
    combined_results = {
        'scan_start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'total_scan_duration': 0,
        'urls_scanned': [],
        'total_vulnerabilities': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'detailed_results': []
    }

    for target_url in target_urls:
        target_url = target_url.strip()
        print(colored(f"\nProcessing URL: {target_url}", "cyan"))

        start_time = time.time()
        
        print(colored("Starting website crawl...", "blue"))
        crawl_data = crawler.crawl_website(zap, target_url)
        print(colored(f"Crawling complete! {crawl_data['num_crawls']} URLs crawled.", "green"))

        perform_attack = input(f"Do you want to attack the site {target_url}? (yes/no): ").strip().lower()
        vulnerabilities = []
        attack_type = ""

        if perform_attack == "yes":
            attack_mode = input("Choose attack mode (1. XSS, 2. SQL Injection, 3. Command Injection, 4. All): ").strip()
            attack_types = {
                "1": ("XSS", "xss"),
                "2": ("SQL Injection", "sql_injection"),
                "3": ("Command Injection", "command_injection"),
                "4": ("All Attacks", "all")
            }
            
            if attack_mode in attack_types:
                attack_type, attack_code = attack_types[attack_mode]
                print(colored(f"Starting {attack_type}...", "yellow"))
                vulnerabilities = attack.attack_website(zap, target_url, attack_type=attack_code)

        end_time = time.time()
        scan_duration = round(end_time - start_time, 2)

        # Calculate vulnerability counts
        vuln_counts = {
            'High': len([v for v in vulnerabilities if v['risk'] == "High"]),
            'Medium': len([v for v in vulnerabilities if v['risk'] == "Medium"]),
            'Low': len([v for v in vulnerabilities if v['risk'] == "Low"])
        }

        # Update combined results
        combined_results['total_scan_duration'] += scan_duration
        combined_results['urls_scanned'].append(target_url)
        for severity in ['High', 'Medium', 'Low']:
            combined_results['total_vulnerabilities'][severity] += vuln_counts[severity]

        # Store detailed results for this URL
        url_result = {
            'url': target_url,
            'scan_duration': scan_duration,
            'crawl_data': crawl_data,
            'attack_performed': perform_attack == "yes",
            'attack_type': attack_type if perform_attack == "yes" else "None",
            'vulnerabilities': vulnerabilities,
            'vulnerability_counts': vuln_counts
        }
        combined_results['detailed_results'].append(url_result)

        # Display individual URL results
        print(colored(f"\nResults for {target_url}:", "yellow"))
        print(f"- High Severity: {vuln_counts['High']}")
        print(f"- Medium Severity: {vuln_counts['Medium']}")
        print(f"- Low Severity: {vuln_counts['Low']}")

    # Generate combined report
    print(colored("\nGenerating combined report...", "yellow"))
    combined_results['scan_end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_generator.generate_combined_report(combined_results)

    # Display final summary
    print(colored("\nFinal Summary:", "green"))
    print(f"Total URLs scanned: {len(combined_results['urls_scanned'])}")
    print(f"Total scan duration: {round(combined_results['total_scan_duration'], 2)} seconds")
    print("Total vulnerabilities found:")
    print(f"- High Severity: {combined_results['total_vulnerabilities']['High']}")
    print(f"- Medium Severity: {combined_results['total_vulnerabilities']['Medium']}")
    print(f"- Low Severity: {combined_results['total_vulnerabilities']['Low']}")

def create_zap_session(zap_url, api_key):
    """Creates a new session in ZAP"""
    params = {
        'name': 'new_session',
        'overwrite': 'true',
        'apikey': api_key
    }

    try:
        response = requests.get(f'{zap_url}/JSON/core/action/newSession/', params=params, verify=False, timeout=30)
        if response.status_code == 200:
            print(colored("New session created successfully.", "green"))
        else:
            print(colored(f"Failed to create session. Response: {response.json()}", "red"))
    except requests.exceptions.RequestException as e:
        print(colored(f"Error creating session: {e}", "red"))

if __name__ == "__main__":
    main()