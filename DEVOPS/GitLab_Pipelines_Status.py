import requests
from datetime import datetime, timedelta
import pytz

# GitLab server details
GITLAB_BASE_URL = "https://gitlab.example.com"  # Replace with your GitLab server URL
GITLAB_TOKEN = "your_private_token"  # Replace with your GitLab API token

# GitLab API URLs
PROJECTS_URL = f"{GITLAB_BASE_URL}/api/v4/projects"
PIPELINES_URL_TEMPLATE = f"{GITLAB_BASE_URL}/api/v4/projects/{{project_id}}/pipelines"

# GitLab headers for authentication
headers = {
    "Private-Token": GITLAB_TOKEN
}

# List of project IDs you want to monitor (you can replace these with your project IDs)
PROJECT_IDS = ["193","23","73","14","47","78","62"]  # Replace with your project names

# Get current time and one hour ago in ISO format
one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat()

# Set up timezone for Kolkata (IST)
kolkata_tz = pytz.timezone("Asia/Kolkata")

def convert_to_ist(utc_time_str):
    """Convert UTC time string to IST and return as separate date and time."""
    # Parse the UTC time string into a datetime object
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Localize the UTC time to UTC timezone
    utc_time = pytz.utc.localize(utc_time)
    # Convert to Kolkata time
    ist_time = utc_time.astimezone(kolkata_tz)
    
    # Return as separate date and time strings
    date_str = ist_time.strftime("%Y-%m-%d")  # Date in format YYYY-MM-DD
    time_str = ist_time.strftime("%H:%M")  # Time in format HH:MM:SS
    
    return date_str, time_str

def get_project_name(project_id):
    """Fetch the project name using the project ID."""
    project_url = f"{PROJECTS_URL}/{project_id}"
    response = requests.get(project_url, headers=headers)
    
    if response.status_code == 200:
        project = response.json()
        return project["name"]
    else:
        print(f"Failed to fetch project name for project ID {project_id}: {response.status_code}")
    return None

def get_pipelines_by_status_and_time(project_id, status, updated_after):
    """Fetch pipelines by their status (e.g., running, pending, passed, failed) for a specific project."""
    pipelines_url = PIPELINES_URL_TEMPLATE.format(project_id=project_id)
    params = {
        "status": status,
        "ref": "preprod",
        "updated_after": updated_after  # Filter by pipelines updated after this time
    }
    response = requests.get(pipelines_url, headers=headers, params=params)
    
    if response.status_code == 200:
        pipelines = response.json()
        return pipelines
    else:
        print(f"Failed to fetch pipelines with status '{status}' for project {project_id}: {response.status_code}")
    return []

def display_pipelines(pipelines, status, project_id, project_name):
    """Display a list of pipelines with their ID, status, date, and time for a specific project."""
    if pipelines:
        print("\n####################################################################################################")
        print(f"\n Pipelines for project '{project_name}':")
        for pipeline in pipelines:
            updated_at_utc = pipeline['updated_at']  # UTC timestamp
            date_str, time_str = convert_to_ist(updated_at_utc)  # Convert to IST
            print(f"- REGION: {pipeline['ref']} | Status: {pipeline['status']} | Date: {date_str} | Time: {time_str}")
    # else:
    #     print(f"No {status} pipelines found for project '{project_name}' (ID: {project_id}) in the last hour.")

def main():
    # Define the statuses we want to check for, including 'success' (as a synonym of 'passed')
    statuses = ["running", "success"]

    # Iterate through project IDs
    for project_id in PROJECT_IDS:
        # Fetch project name
        project_name = get_project_name(project_id)
        if project_name:
            for status in statuses:
                pipelines = get_pipelines_by_status_and_time(project_id, status, one_hour_ago)
                display_pipelines(pipelines, status, project_id, project_name)
        else:
            print(f"Project with ID {project_id} not found.")

if __name__ == "__main__":
    main()
