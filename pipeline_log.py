import gitlab

gl = gitlab.Gitlab('https://gitlab.example.com', private_token='your_access_token')
project = gl.projects.get('project_id')
pipeline = project.pipelines.get('pipeline_id')
jobs = pipeline.jobs.list()

# Get logs for a specific job
job = jobs[0]
log = job.trace()
print(log)
