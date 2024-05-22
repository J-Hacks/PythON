import ipaddress
import socket
def is_port_open(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Adjust timeout as needed
    try:
        sock.connect((ip, 3389))
        return True
    except (socket.timeout, socket.error):
        return False
    finally:
        sock.close()
network = ipaddress.ip_network('192.168.237.0/24')
l = []
for ip in network:
    add=str(ip)
    p= is_port_open(add)
    if p is True:
        l.append(add)
