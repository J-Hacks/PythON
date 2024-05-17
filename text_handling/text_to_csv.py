import csv
import re

# Read the data from the file
with open('new.txt', 'r') as file:
    content = file.read()

# Define patterns to extract information using regular expressions
patterns = {
    'Hostname': r'Hostname\s*:\s*(.*)',
    'Serial Number': r'serialnumber\s*:\s*(.*)',
    'IP Address': r'IPaddress\s*:\s*(.*)',
    'RAM': r'RAM\s*:\s*(.*)',
    'Disk Size': r'DISK\ssize\s*:\s*(.*)'
}

# Initialize a list to store dictionaries of extracted information for each system
systems_info = []

# Split the content into individual system information blocks
system_blocks = re.split(r'\n\s*\n', content.strip())

# Iterate over each system block
for system_block in system_blocks:
    # Initialize a dictionary to store extracted information for the current system
    system_info = {}
    
    # Iterate over patterns and extract information for the current system block
    for key, pattern in patterns.items():
        match = re.search(pattern, system_block, re.IGNORECASE)
        if match:
            system_info[key] = match.group(1).strip()
    
    # Append the extracted information for the current system to the list
    systems_info.append(system_info)

# Write the extracted information into a CSV file
with open('computer_info.csv', 'w', newline='') as csvfile:
    fieldnames = ['Hostname', 'Serial Number', 'IP Address', 'RAM', 'Disk Size']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data for each system
    for system_info in systems_info:
        writer.writerow(system_info)
