import subprocess
import sys

# Function to automatically check and install colorama if missing
def install_dependencies():
    try:
        import colorama
    except ImportError:
        print("[*] Colorama not found. Installing it automatically...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
            print("[✔] Colorama installed successfully!\n")
        except Exception as e:
            print(f"[!] Failed to install colorama automatically: {e}")
            sys.exit(1)

install_dependencies()

import socket
import platform
import concurrent.futures
import time
import re
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

def ping_ip(ip):
    system = platform.system().lower()
    if system == 'windows':
        command = ['ping', '-n', '1', '-w', '100', ip]
    else:
        command = ['ping', '-c', '1', '-W', '1', ip]
    
    response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if response == 0:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Unknown"
        return ip, hostname
    return None

def get_mac_address(ip):
    try:
        output = subprocess.check_output(['arp', '-a'], universal_newlines=True)
        for line in output.splitlines():
            if ip in line:
                match = re.search(r"([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})", line)
                if match:
                    return match.group(1).replace('-', ':').upper()
    except Exception:
        pass
    return "Unknown MAC"

def check_common_ports(ip):
    # Common ports to scan: FTP(21), SSH(22), HTTP(80), HTTPS(443), SMB(445)
    common_ports = [21, 22, 80, 443, 445]
    open_ports = []
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(str(port))
            sock.close()
        except Exception:
            pass
            
    return open_ports

def scan_network():
    print(Fore.CYAN + "=== ADVANCED PYTHON NETWORK SCANNER ===")
    user_subnet = input(Fore.YELLOW + "[?] Enter subnet to scan (e.g., 192.168.1 or 10.0.0) [Default: 192.168.1]: ").strip()
    
    if not user_subnet:
        subnet = "192.168.1"
    else:
        subnet = user_subnet

    print(Fore.CYAN + f"\n[*] Scanning network range {subnet}.1 to {subnet}.254...\n")
    start_time = time.time()
    active_hosts = []

    ips = [f"{subnet}.{i}" for i in range(1, 255)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(ping_ip, ips)
        
        for result in results:
            if result:
                ip, hostname = result
                mac = get_mac_address(ip)
                open_ports = check_common_ports(ip)
                ports_str = ", ".join(open_ports) if open_ports else "None"
                
                print(Fore.GREEN + f"[+] Active Host: {ip} " + 
                      Fore.BLUE + f"| Hostname: {hostname} " + 
                      Fore.MAGENTA + f"| MAC: {mac} " + 
                      Fore.YELLOW + f"| Open Ports: [{ports_str}]")
                
                active_hosts.append((ip, hostname, mac, open_ports))

    end_time = time.time()
    print(Fore.CYAN + f"\n[✔] Scan finished in {round(end_time - start_time, 2)} seconds.")
    print(Fore.CYAN + f"[✔] Total active hosts discovered: {len(active_hosts)}")

if __name__ == "__main__":
    scan_network()