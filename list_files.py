import os

# Set the directory path
path = '/home/jeej/projects/'

# Read the content of the file
files = os.listdir(path)

# Print the content of the directory
for file in files:
    print(file)