import os
 
def print_files_recursive(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Extract only the file name from the full path
            file_name = os.path.relpath(os.path.join(root, file), directory)
            print(file_name)
 
directory = "/path/to/your/directory"
print_files_recursive(directory)
