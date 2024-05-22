import socket

def get_domain_name(ip):
    try:
        domain_name, _, _ = socket.gethostbyaddr(ip)
        return domain_name
    except socket.herror:
        return "Unknown"

def main():
    subnet = "192.168.0"
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        domain_name = get_domain_name(ip)
        print(f"IP: {ip}   Domain Name: {domain_name}")

if __name__ == "__main__":
    main()

