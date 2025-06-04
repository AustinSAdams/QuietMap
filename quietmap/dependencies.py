import subprocess
import sys
import platform

# Check if command is installed or not
def is_installed(command):
    try:
        subprocess.run([command, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Install the NMap dependency
def install_nmap():
    os_name = platform.system()
    try:
        if os_name == 'Linux':
            print("Attempting to install nmap via apt-get...")
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nmap'], check=True)
        elif os_name == 'Darwin':
            print("Attempting to install nmap via brew...")
            subprocess.run(['brew', 'install', 'nmap'], check=True)
        elif os_name == 'Windows':
            print("Please install nmap manually from https://nmap.org/download.html")
            return False
        else:
            print(f"Unsupported OS: {os_name}. Please install nmap manually.")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install nmap automatically: {e}")
        return False

# Automatically check for dependenies and install them.
def check_and_install_dependencies():
    if not is_installed('nmap'):
        print("nmap not found.")
        if not install_nmap():
            print("Please install 'nmap' manually to continue.")
            sys.exit(1)
