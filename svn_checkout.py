import subprocess
 
def svn_checkout(repo_url, destination, username, password):

    try:

        subprocess.run(["svn", "checkout", repo_url, destination, "--username", username, "--password", password])

        print("Checkout successful!")

    except subprocess.CalledProcessError as e:

        print("Error:", e)
 

repo_url = "https://svn.example.com/svn/project/trunk"

destination = "/path/to/checkout/directory"

username = "your_username"

password = "your_password"

svn_checkout(repo_url, destination, username, password)

