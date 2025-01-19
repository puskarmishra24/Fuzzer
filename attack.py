from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
import time
from termcolor import colored

def load_payload(file_path):
    """Load payloads from the specified file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Payload file not found: {file_path}")
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def attack_website(zap, target_url, attack_type="all"):
    """Main function to handle attack logic."""
    mode = attack_type  # Accept attack type directly instead of user input
    
    # Load all payloads
    xss_payloads = load_payload("Payload/xss_payload.txt")
    sql_payloads = load_payload("Payload/sql_payload.txt")
    cmd_injection_payloads = load_payload("Payload/cmd_injection_payload.txt")
    
    vulnerabilities = []

    # Perform attacks based on the provided attack type
    if mode == "xss" or mode == "all":
        # print(colored("Starting XSS attack...", "yellow"))
        vulnerabilities += perform_attack(zap, target_url, xss_payloads, "XSS")
    
    if mode == "sql_injection" or mode == "all":
        # print(colored("Starting SQL Injection attack...", "yellow"))
        vulnerabilities += perform_attack(zap, target_url, sql_payloads, "SQL Injection")
    
    if mode == "command_injection" or mode == "all":
        # print(colored("Starting Command Injection attack...", "yellow"))
        vulnerabilities += perform_attack(zap, target_url, cmd_injection_payloads, "Command Injection")
    
    return vulnerabilities

def perform_attack(zap, target_url, payloads, attack_type):
    """Perform the attack using the provided payloads."""
    def send_payload(payload):
        response = zap.urlopen(f"{target_url}?input={payload}")
        time.sleep(0.1)  # Short delay for processing
        return zap.core.alerts()

    vulnerabilities = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(send_payload, payloads), total=len(payloads)))

    # Collect all vulnerabilities
    for result in results:
        vulnerabilities.extend(result)

    # Display summary in terminal
    # high_risk = [v for v in vulnerabilities if v["risk"] == "High"]
    # medium_risk = [v for v in vulnerabilities if v["risk"] == "Medium"]

    # print(colored(f"{attack_type} - High Severity: {len(high_risk)}", "red"))
    # print(colored(f"{attack_type} - Medium Severity: {len(medium_risk)}", "yellow"))

    return vulnerabilities
