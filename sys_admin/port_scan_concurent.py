import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout after 1 second
    result = sock.connect_ex((ip, port))
    sock.close()
    return ip, port, result == 0

def check_ports_concurrently(ip_list, port):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ip = {executor.submit(check_port, ip, port): ip for ip in ip_list}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                ip, port, is_open = future.result()
                status = "open" if is_open else "closed"
                print(f"IP: {ip}, Port: {port} is {status}")
            except Exception as exc:
                print(f"IP: {ip} generated an exception: {exc}")

if __name__ == "__main__":
    # List of IP addresses to check
    ip_addresses = [
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.3",
        "192.168.1.4",
        # Add more IP addresses as needed
    ]
    
    port_to_check = 80  # Change this to the port you want to check

    check_ports_concurrently(ip_addresses, port_to_check)
