import os
import random
import subprocess
import requests
from datetime import datetime, timedelta

# Set the range of contributions
MIN_CONTRIBUTIONS = 3
MAX_CONTRIBUTIONS = 31

# Define start and end dates for contribution range
start_date = datetime(2023, 11, 1)
end_date = datetime(2024, 10, 20)

# Randomly determine how many contributions to make within the specified range
num_contributions = random.randint(MIN_CONTRIBUTIONS, MAX_CONTRIBUTIONS)

# Generate a random date within the defined range
def random_date():
    delta_days = (end_date - start_date).days
    random_day = start_date + timedelta(days=random.randint(0, delta_days))
    return random_day.strftime('%Y-%m-%d'), random_day.strftime('%Y-%m-%dT%H:%M:%S')

# Create a new branch for the contributions
branch_name = f"random-contributions-{datetime.now().strftime('%Y%m%d%H%M%S')}"
subprocess.run(["git", "checkout", "-b", branch_name])

# Create random commits on random dates within the specified range
for _ in range(num_contributions):
    date, iso_date = random_date()
    
    # Create a dummy file for the commit
    with open("dummy.txt", "a") as file:
        file.write(f"Contribution on {date}\n")
    
    # Set environment variable for author date
    os.environ['GIT_AUTHOR_DATE'] = iso_date
    os.environ['GIT_COMMITTER_DATE'] = iso_date

    # Add and commit the changes with the specific date
    subprocess.run(["git", "add", "dummy.txt"])
    subprocess.run(["git", "commit", "-m", f"Random contribution on {date}"])

# Push the branch to the remote repository
subprocess.run(["git", "push", "origin", branch_name])

# Create a pull request
repo = "ums91/random-contributions"  # Update this with your repository name
token = os.getenv("GITHUB_TOKEN")  # Use your GitHub token from environment variables

# Define the pull request data
pr_data = {
    "title": f"Add random contributions",
    "head": branch_name,
    "base": "main",
    "body": "This pull request adds random contributions."
}

# Create the pull request
response = requests.post(
    f"https://api.github.com/repos/{repo}/pulls",
    json=pr_data,
    headers={"Authorization": f"token {token}"}
)

if response.status_code == 201:
    print(f"Pull request created successfully: {response.json()['html_url']}")
    
    # Merge the pull request
    pr_number = response.json()['number']
    merge_response = requests.put(
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}/merge",
        headers={"Authorization": f"token {token}"}
    )
    
    if merge_response.status_code == 200:
        print("Pull request merged successfully.")
    else:
        print(f"Failed to merge pull request: {merge_response.json()}")
else:
    print(f"Failed to create pull request: {response.json()}")
