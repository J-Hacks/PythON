import os
import subprocess
import time
from datetime import datetime

def backup_and_sync(source_dir, backup_dir):
    """
    Take a backup of the source directory and sync with the old backup.

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

    # Rsync command to sync source_dir with the current backup directory
    rsync_command = [
        'rsync',
        '-avh',  # Archive mode, verbose, human-readable
        '--delete',  # Delete extraneous files from destination dirs
        source_dir + '/',  # Trailing slash ensures contents of the directory are copied
        current_backup_dir
    ]

    print(f"Running rsync command: {' '.join(rsync_command)}")
    try:
        subprocess.run(rsync_command, check=True)
        print(f"Backup and sync completed successfully. Backup stored in '{current_backup_dir}'")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running rsync: {e}")

if __name__ == "__main__":
    # Example usage
    source_directory = "/path/to/source/directory"
    backup_directory = "/path/to/backup/directory"

    backup_and_sync(source_directory, backup_directory)

