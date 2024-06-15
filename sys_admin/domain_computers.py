import csv
from ldap3 import Server, Connection, ALL, NTLM

def get_machines(domain, username, password, output_file):
    # Define the LDAP server and connection
    server = Server(domain, get_info=ALL)
    conn = Connection(server, user=f"{domain}\\{username}", password=password, authentication=NTLM, auto_bind=True)

    # Perform the LDAP search for computer objects
    conn.search(
        search_base='DC=yourdomain,DC=com',  # Replace with your actual domain components
        search_filter='(objectClass=computer)',
        attributes=['name']
    )

    # Extract the machine names from the search results
    machines = [(entry['attributes']['name'][0]) for entry in conn.entries]

    # Write the machine names to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Machine Name'])
        for machine in machines:
            csvwriter.writerow([machine])

    print(f"Machine names have been written to {output_file}")

# Replace the following variables with your actual domain, username, password, and desired output file name
domain = 'yourdomain.com'  # e.g., 'example.com'
username = 'your_username'
password = 'your_password'
output_file = 'output_machines.csv'

get_machines(domain, username, password, output_file)
