import gitlab

gl = gitlab.Gitlab('https://gitlab.example.com', private_token='your_access_token')
project = gl.projects.get('project_id')
issues = project.issues.list()

for issue in issues:
    print(f"Issue ID: {issue.id}, Title: {issue.title}, Status: {issue.state}")
