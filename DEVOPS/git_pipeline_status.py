import requests
from datetime import datetime, timedelta
import pytz
from concurrent.futures import ThreadPoolExecutor, as_completed
GITLAB_BASE_URL = "https://xxxxxxxxxxxxxxxxxxx.com/"
GITLAB_TOKEN = "xxxxxxxxxxxxxxxx"    
kolkata_tz = pytz.timezone("Asia/Kolkata")
PROJECTS_URL = f"{GITLAB_BASE_URL}/api/v4/projects"
PIPELINES_URL_TEMPLATE = f"{GITLAB_BASE_URL}/api/v4/projects/{{project_id}}/pipelines"
headers = {
    "Private-Token": GITLAB_TOKEN
}

# List of all your project names
PROJECT_NAMES = ["project1", "project2", "project4"]  
twelve_hour_ago = (datetime.utcnow() - timedelta(hours=12)).isoformat()

def get_project_id_by_name(project_name):
    params = {"search": project_name}
    response = requests.get(PROJECTS_URL, headers=headers, params=params)
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            if project["name"] == project_name:
                return project["id"]
    return None

def get_pipelines_by_status_and_time(project_id, status, updated_after):
    """
    Fetch pipelines by their status (e.g., running, pending, passed, failed) for a specific project.
    Filter pipelines updated after a specific time.
    """
    pipelines_url = PIPELINES_URL_TEMPLATE.format(project_id=project_id)
    params = {
        "status": status,
        "updated_after": updated_after 
    }
    response = requests.get(pipelines_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return []

def convert_to_ist(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_time = pytz.utc.localize(utc_time)
    ist_time = utc_time.astimezone(kolkata_tz)
    date_str = ist_time.strftime("%Y-%m-%d") 
    time_str = ist_time.strftime("%H:%M") 
    return date_str, time_str

def display_pipelines(pipelines, status, project_name):
    """
    Display a list of pipelines with their ID, status, and timestamp for a specific project.
    """
    if pipelines:
        print(f"\n{status.capitalize()} Pipelines for project '{project_name}':")
        for pipeline in pipelines:
            pipeline["updated_at"] = convert_to_ist(pipeline["updated_at"])
            print(f"- Region: {pipeline['ref']} | Status: {pipeline['status']} | Updated At: {pipeline['updated_at']}")

def fetch_and_display_pipelines(project_name):
    """
    This function is treated as a separate job for each project.
    It fetches pipelines for all statuses of a project.
    """
    statuses = ["running", "pending", "success", "failed"]
    project_id = get_project_id_by_name(project_name)
    if project_id:
        for status in statuses:
            pipelines = get_pipelines_by_status_and_time(project_id, status, twelve_hour_ago)
            display_pipelines(pipelines, status, project_name)
    else:
        print(f"Project '{project_name}' not found.")

def main():
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_and_display_pipelines, project_name) for project_name in PROJECT_NAMES]

        # # Wait for all jobs to complete
        for future in as_completed(futures):
            future.result()  # Ensures exceptions are raised if any

if __name__ == "__main__":
    main()
