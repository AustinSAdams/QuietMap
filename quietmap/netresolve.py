# Module for DNS/IP analysis
import subprocess
import platform
import re

def get_ip_from_domain(domain: str) -> str:
    # Ping the domain to retrieve its IP address.
    system = platform.system()
    if system == "Windows":
        ping_cmd = ["ping", "-c", "1", domain]
    else:
        ping_cmd = ["ping", "-c", "1", domain]

    try:
        output = subprocess.check_output(ping_cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to ping '{domain}'\n\nError: {e}")

    # Return the IP address
    ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", output)
    if ip_match:
        return ip_match.group(0)
    else:
        raise RuntimeError(f"IP address not found in ping output for domain '{domain}'")

# Main runner for dns.py
def run(domain):
    print("[dns] COMING SOON")
