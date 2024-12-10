import gitlab

gl = gitlab.Gitlab('https://gitlab.example.com', private_token='your_access_token')
project = gl.projects.get('project_id')
pipelines = project.pipelines.list()

if pipelines:
    last_pipeline = pipelines[0]
    print(f"Pipeline ID: {last_pipeline.id}, Status: {last_pipeline.status}")
else:
    print("No pipelines found.")
las
