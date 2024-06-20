from scapy.all import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Disable verbose logging from scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def ping_ip(ip):
    """Ping an IP address using scapy."""
    pkt = IP(dst=ip)/ICMP()
    resp = sr1(pkt, timeout=10, verbose=0)
    return ip, resp is not None

def scan_network(network):
    """Scan a network for active IP addresses."""
    ip_list = [f"{network}.{i}" for i in range(1, 255)]
    active_ips = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(ping_ip, ip): ip for ip in ip_list}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                ip, is_active = future.result()
                if is_active:
                    active_ips.append(ip)
                    print(f"{ip} is active")
            except Exception as exc:
                print(f"IP {ip} generated an exception: {exc}")

    return active_ips

if __name__ == "__main__":
    network = "192.168.29"  # Replace with your network prefix
    active_ips = scan_network(network)
    print(f"Active IPs: {active_ips}")
