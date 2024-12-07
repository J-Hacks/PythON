import requests
import csv

# GitLab server details
GITLAB_BASE_URL = "https://gitlab.example.com"  # Replace with your GitLab server URL
GITLAB_TOKEN = "your_private_token"  # Replace with your GitLab API token

# GitLab API URL to get all projects
PROJECTS_URL = f"{GITLAB_BASE_URL}/api/v4/projects"

# GitLab headers for authentication
headers = {
    "Private-Token": GITLAB_TOKEN
}

def fetch_all_projects():
    """Fetch all projects from GitLab."""
    projects = []
    page = 1
    per_page = 100  # Adjust the number of projects per request if needed

    while True:
        params = {
            "page": page,
            "per_page": per_page
        }
        response = requests.get(PROJECTS_URL, headers=headers, params=params)

        if response.status_code == 200:
            projects_page = response.json()
            if not projects_page:
                break
            projects.extend(projects_page)
            page += 1
        else:
            print(f"Failed to fetch projects: {response.status_code}")
            break
    
    return projects

def save_projects_to_csv(projects, filename="projects.csv"):
    """Save the list of projects and their IDs to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Project Name", "Project ID"])  # CSV header
        for project in projects:
            writer.writerow([project["name"], project["id"]])

def main():
    # Fetch all projects from GitLab
    print("Fetching projects...")
    projects = fetch_all_projects()
    
    # Save projects to CSV
    print(f"Saving {len(projects)} projects to CSV...")
    save_projects_to_csv(projects)
    print("Projects saved to 'projects.csv'.")

if __name__ == "__main__":
    main()
