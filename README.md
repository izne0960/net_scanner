# 🛡️ Advanced Python Network Scanner

**A high-performance, multi-threaded network scanner built in Python.** Designed for speed, modularity, and clean terminal aesthetics.
✨ Core Features

🌐 Dynamic Subnet: Input any custom network range dynamically (e.g., 192.168.1, 10.0.0, etc.).

⚡ Multi-Threaded: Blazing-fast scanning across the entire subnet (1-254) in seconds using ThreadPoolExecutor.

🔍 Hostname Resolution: Automatically resolves device hostnames via socket connections.

🏷️ MAC Address Extraction: Queries the system's local ARP table to capture and format physical MAC addresses.

🔓 Smart Port Checking: Scans critical open ports (21, 22, 80, 443, 445) on active hosts.

🤖 Auto-Dependency: Automatically detects and installs missing packages (like colorama) without manual effort.

🎨 Styled CLI Output: Clean, color-coded terminal interface for maximum readability.

How to Run 🚀

Open your terminal and run the script by typing:

cd net_scanner
and 
python net_scanner.py