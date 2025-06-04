# Module for port scanning
import subprocess
from colorama import Fore
from quietmap.netresolve import get_ip_from_domain

# Determine if the IP address is valid
def is_ip_address(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

# Scan the ports of a given domain
def run(domain):
    print(f"{Fore.BLUE}[scan] Finding port info for {domain}")

    target = domain
    if not is_ip_address(domain):
        try:
            target = get_ip_from_domain(domain)
            print(f"{Fore.BLUE}[scan] Resolved domain to IP: {target}")
        except RuntimeError as e:
            print(f"{Fore.RED}[scan] Error resolving domain: {e}")
            return

    try:
        result = subprocess.run(
            ["sudo", "nmap", "-sS", "-T1", "-Pn", target],
            # ["sudo", "nmap", "-sS", "-Pn", target],
            capture_output=True,
            text=True,
            check=True
        )
        return(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}[scan] nmap scan failed: {e}")
