# NOEMVEX-DOMAIN v1.0 [DOMAIN HUNTER EDITION]
![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-grey) ![Focus](https://img.shields.io/badge/Focus-Active%20Directory-red) ![Attack](https://img.shields.io/badge/Attack-Kerberos-orange)

> **"Pillage the Forest, Rule the Domain."**
> Automated Active Directory Reconnaissance & Attack suite. Integrates the industry's most powerful tools into a single Red Team workflow.
> ⚠️ **Disclaimer:** This tool is for educational purposes only. [Read the full Legal Disclaimer](#️-legal-disclaimer)

---
## About
**NOEMVEX-DOMAIN** is a high-speed reconnaissance and attack automation engine designed for Active Directory environments. It automates the heavy lifting of initial discovery, enumeration, and post-exploitation attacks like AS-REP Roasting and Kerberoasting. By integrating tools like BloodHound and CrackMapExec, it provides a structured path from zero-knowledge to full domain compromise.



## Capabilities
* **Full AD Discovery:** Scans DNS, Kerberos, LDAP, and SMB services with specialized Nmap scripts.
* **Anonymous Enumeration:** Automatically checks for guest shares and user lists via `enum4linux` and `CrackMapExec`.
* **Credentialless Attacks:** Automated AS-REP Roasting attempts to capture Kerberos pre-auth hashes.
* **Authenticated Dominance:** Once credentials are found, it automates Kerberoasting (TGS extraction) and SMB share deep-scanning.
* **BloodHound Integration:** Automated data ingestion via `bloodhound-python` for visual attack path analysis.
* **Loot Management:** All scan results, hashes, and data files are organized into structured directories for reporting.

---
## Usage

### 1. Requirements
This tool acts as an orchestrator for several industry-standard tools. Ensure you have the following installed:
`nmap`, `enum4linux`, `crackmapexec`, `impacket-scripts`, `bloodhound-python`

### 2. Basic Execution (No Auth)
# Clone the Domain Hunter
git clone https://github.com/noemvex/NOEMVEX-DOMAIN.git
cd NOEMVEX-DOMAIN

# Run initial enumeration against a DC
python3 noemvex_domain.py --ip 10.10.10.10 --domain spookysec.local

### 3. Full Domain Attack (With Auth)
# Run with compromised credentials to extract hashes and BloodHound data
python3 noemvex_domain.py --ip 10.10.10.10 --domain spookysec.local --user svc-admin --password 'P@ssw0rd123!'

---

## Output Preview

    ███╗   ██╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗███████╗██╗  ██╗
    ████╗  ██║██╔═══██╗██╔════╝████╗ ████║██║   ██║██╔════╝╚██╗██╔╝
    ██╔██╗ ██║██║   ██║█████╗  ██╔████╔██║██║   ██║█████╗   ╚███╔╝ 
    ██║╚██╗██║██║   ██║██╔══╝  ██║╚██╔╝██║╚██╗ ██╔╝██╔══╝   ██╔██╗ 
    ██║ ╚████║╚██████╔╝███████╗██║ ╚═╝ ██║ ╚████╔╝ ███████╗██╗  ██╗
    ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
                   [ NOEMVEX DOMAIN V1.0 HUNTER EDITION ]

    Target IP: 10.10.10.10 | Domain: spookysec.local
    [+] Loot directory created: ad_loot_10.10.10.10

    --- [ PHASE 1: NETWORK DISCOVERY ] ---
    [*] Initiating: AD Port & Script Scan...
    [+] AD Port & Script Scan Completed Successfully.

    --- [ PHASE 2: USER & SHARE ENUMERATION ] ---
    [*] Initiating: Enum4linux Scan...
    [*] Initiating: CrackMapExec Guest Share Check...

    --- [ PHASE 4: AUTHENTICATED ATTACKS ] ---
    [*] Initiating: Kerberoasting (TGS Extraction)...
    [+] Kerberoasting Completed. Hashes saved to ad_loot_10.10.10.10/kerberoast_hashes.txt
    [*] Initiating: BloodHound Data Ingestion...

    [√] OPERATION COMPLETE. LOOT SAVED IN: ad_loot_10.10.10.10


---

## ⚠️ Legal Disclaimer
**Usage of NOEMVEX-DOMAIN for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.**
**This project is designed for educational purposes and authorized security testing only.**

---

### Developer
**Emre 'noemvex' Sahin**
*Cybersecurity Specialist & Tool Developer*
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/emresahin-sec) [![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/noemvex)

