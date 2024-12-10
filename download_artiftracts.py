import gitlab

gl = gitlab.Gitlab('https://gitlab.example.com', private_token='your_access_token')
project = gl.projects.get('project_id')
pipeline = project.pipelines.get('pipeline_id')
jobs = pipeline.jobs.list()

# Download artifacts from the first successful job
for job in jobs:
    if job.status == 'success' and job.artifacts_file:
        job.artifacts.download(artifact_path='./artifacts/', job_artifacts=True)
        print(f"Downloaded artifacts for job {job.name}")
        break
else:
    print("No successful jobs with artifacts found.")
