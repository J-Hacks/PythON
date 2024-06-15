import socket
import csv

def resolve_hostnames(ip_file, output_file):
    try:
        with open(ip_file, 'r') as file:
            ip_addresses = file.readlines()

        resolved_hosts = []

        for ip in ip_addresses:
            ip = ip.strip()
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                resolved_hosts.append([ip, hostname])
            except socket.herror:
                resolved_hosts.append([ip, "Hostname not found"])

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "Hostname"])
            writer.writerows(resolved_hosts)

        print(f"Hostnames resolved and written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'ip_list.txt' with your input file containing IP addresses
# Replace 'output_hostnames.csv' with your desired output file
resolve_hostnames('ip_list.txt', 'output_hostnames.csv')
