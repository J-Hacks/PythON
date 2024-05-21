import os
import subprocess
from datetime import datetime

def backup_and_sync(source_dir, backup_dir):
    """
    Take a backup of the source directory and sync with the old backup using robocopy.

    Args:
        source_dir (str): The source directory to back up.
        backup_dir (str): The destination directory where the backup will be stored.
    """
    # Ensure source directory exists
    if not os.path.isdir(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Ensure backup directory exists, create if not
    if not os.path.isdir(backup_dir):
        print(f"Backup directory '{backup_dir}' does not exist. Creating it...")
        os.makedirs(backup_dir)

    # Generate timestamp for current backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_backup_dir = os.path.join(backup_dir, f'backup_{timestamp}')

    # Create a new directory for the current backup
    os.makedirs(current_backup_dir)

    # Robocopy command to sync source_dir with the current backup directory
    robocopy_command = [
        'robocopy',
        source_dir,
        current_backup_dir,
        '/MIR',  # Mirror source and destination directories
        '/E',    # Copy subdirectories, including empty ones
        '/R:3',  # Retry 3 times (default is 1 million)
        '/W:5'   # Wait 5 seconds between retries (default is 30 seconds)
    ]

    print(f"Running robocopy command: {' '.join(robocopy_command)}")
    try:
        subprocess.run(robocopy_command, check=True)
        print(f"Backup and sync completed successfully. Backup stored in '{current_backup_dir}'")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running robocopy: {e}")

if __name__ == "__main__":
    # Example usage
    source_directory = "C:\\path\\to\\source\\directory"
    backup_directory = "D:\\path\\to\\backup\\directory"

    backup_and_sync(source_directory, backup_directory)

