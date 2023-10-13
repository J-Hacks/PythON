import re
import csv
import os
# Define the regular expression pattern to extract changeset number and items
pattern = r'Changeset:(\s+\d*).*?Date:(.*?\n).*?Comment:(.+?)(?:\n\s*\n|\Z).*?Items:(.+?)(?:\n\s*\n|\Z)'
# Directory path containing the text files and where the CSV files will be saved
directory_path = r'C:\Users\jeejandra.a\Desktop\NVKIDS_TFS\NVKIDS_OCTOBER_03_TO_08\NVKIDS_OCTOBER_03_TO_08'
# Iterate through all text files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        # Construct the full file paths for text and CSV files
        text_file_path = os.path.join(directory_path, filename)
        csv_file_path = os.path.join(directory_path, os.path.splitext(filename)[0] + '.csv')
        # Read the input text file
        with open(text_file_path) as file:
            log_content = file.read()
        # Find all matches in the log content
        matches = re.findall(pattern, log_content, re.MULTILINE | re.DOTALL)
        # Write the extracted data to a CSV file with the same name as the text file
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header
            csv_writer.writerow(['Changeset', 'Date', 'Comment', 'Items'])
            # Write data for each match
            for match in matches:
                changeset, Date, Comment,items = match
                csv_writer.writerow([changeset.strip(), Date, Comment, items.strip()])
        print(f'Data extracted and saved to {csv_file_path}')