import gitlab

gl = gitlab.Gitlab('https://gitlab.example.com', private_token='your_access_token')
runners = gl.runners.list()

for runner in runners:
    print(f"Runner ID: {runner.id}, Description: {runner.description}, Status: {runner.status}")
