import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_disk_usage_windows(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        
        command = 'wmic logicaldisk get size,freespace,caption'
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        
        client.close()
        return ip, output
    except Exception as e:
        return ip, f"Error: {e}"

def check_disk_usage_concurrently_windows(servers, username, password):
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_server = {executor.submit(check_disk_usage_windows, server, username, password): server for server in servers}
        for future in as_completed(future_to_server):
            ip = future_to_server[future]
            try:
                ip, output = future.result()
                print(f"Disk usage for {ip}:\n{output}")
            except Exception as exc:
                print(f"Server {ip} generated an exception: {exc}")

if __name__ == "__main__":
    # List of servers to check
    servers = [
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.3",
        # Add more servers as needed
    ]
    
    username = "admin"
    password = "password"
    
    check_disk_usage_concurrently_windows(servers, username, password)
