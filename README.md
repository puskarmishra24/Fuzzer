# Fuzzer Tool to Find Vulnerability with Crawl and Attack Simulation

## Description:

The **Fuzzer Tool to Find Vulnerability with Crawl and Attack Simulation** is an advanced automated security testing tool designed to uncover vulnerabilities in web applications. It seamlessly integrates web crawling to map application structure, simulates various security attacks to identify potential weaknesses, and generates detailed reports for comprehensive security analysis. This tool ensures a thorough audit of web applications, enhancing their resilience against potential threats and ensuring they meet security standards.

This project performs the following operations:
1. **Web Crawling**: Scans the provided web application URLs to identify endpoints, forms, and other accessible resources.  
2. **Attack Simulation**: Executes simulated attacks, including XSS (Cross-Site Scripting), SQL Injection, and Command Injection, on the discovered endpoints.  
3. **Fuzzing**: Applies diverse attack patterns to detect vulnerabilities and evaluate how the application responds to malicious inputs.  
4. **Real-Time Reporting**: Produces comprehensive vulnerability reports, classifying issues by severity levels (High, Medium, Low) for each scanned URL.  

This tool enables security experts and developers to evaluate their applications for known vulnerabilities and strengthen their defenses against prevalent web threats.

---

## Features:

- **Automated Scanning**: Systematically explores target URLs to identify all reachable endpoints.  
- **Simulated Security Attacks**: Performs a range of attack scenarios, including XSS, SQL Injection, and Command Injection.  
- **Fuzz Testing**: Executes automated fuzzing to reveal hidden vulnerabilities in the web application.  
- **Comprehensive Reporting**: Delivers real-time vulnerability reports, prioritized by severity levels.  
- **Flexible Attack Options**: Enables users to customize attack types or execute a full suite of tests.  
- **Session Handling**: Automatically initiates and manages sessions in ZAP (OWASP Zed Attack Proxy) to organize and monitor scans.

---

## Prerequisites:

Before using the tool, ensure the following are installed and properly set up:  

- **OWASP ZAP (Zed Attack Proxy)**: Used for simulating security attacks.  
- **Python 3.x**: Necessary to run the fuzzer and related scripts.  
- **Required Python Libraries**:  
  - `requests`: Handles HTTP requests.  
  - `termcolor`: Adds color to terminal outputs.  
  - `datetime`: Tracks and manages time.  
  - Custom modules: `crawler`, `attack`, `report_generator`, `connection` for handling crawling, attack execution, and reporting.  

To install the Python libraries, use:  
```bash
pip install requests termcolor
```  
