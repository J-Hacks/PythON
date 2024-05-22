import os
import socket

def is_up(ip):
    try:
        socket.create_connection((ip, 445), timeout=2)
        return True
    except OSError:
        return False

def get_folders(ip):
    folders = []
    root_path = f"\\\\{ip}\\c$\\Users"
    if not os.path.exists(root_path):
        return folders
    
    for folder in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder)
        if os.path.isdir(folder_path):
            folders.append(folder_path)
    return folders

def main():
    network_prefix = "192.168.53"
    for i in range(1, 255):
        ip = f"{network_prefix}.{i}"
        if is_up(ip):
            folders = get_folders(ip)
            print(f"IP: {ip}")
            if folders:
                print("Folders:")
                for folder in folders:
                    print(folder)
            else:
                print("No folders found.")

if __name__ == "__main__":
    main()

