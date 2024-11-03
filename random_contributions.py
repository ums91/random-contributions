import os
import random
import subprocess
import requests
from datetime import datetime, timedelta

# Set the range of contributions
MIN_DAILY_CONTRIBUTIONS = 3
MAX_DAILY_CONTRIBUTIONS = 33

# Define the number of contribution days per week
MIN_CONTRIBUTION_DAYS = 4
MAX_CONTRIBUTION_DAYS = 6

# Define start and end dates for contribution range
start_date = datetime(2023, 11, 1)
end_date = datetime(2024, 10, 20)

# Generate a list of random contribution dates
def generate_contribution_dates():
    current_date = start_date
    contribution_dates = []
    
    while current_date <= end_date:
        # Randomly decide if this week has contribution days
        if random.randint(0, 1) == 1:  # 50% chance to contribute this week
            days_in_week = random.randint(MIN_CONTRIBUTION_DAYS, MAX_CONTRIBUTION_DAYS)
            for _ in range(days_in_week):
                # Select a random day in this week to contribute
                contribution_day = current_date + timedelta(days=random.randint(0, 6))
                if contribution_day <= end_date:
                    contribution_dates.append(contribution_day)
        current_date += timedelta(days=7)  # Move to the next week

    return contribution_dates

# Create a new branch for the contributions
branch_name = f"random-contributions-{datetime.now().strftime('%Y%m%d%H%M%S')}"
subprocess.run(["git", "checkout", "-b", branch_name])

# Get the contribution dates
contribution_dates = generate_contribution_dates()

# Create random commits on the generated contribution dates
for date in contribution_dates:
    # Determine how many contributions to make for this day
    num_contributions = random.randint(MIN_DAILY_CONTRIBUTIONS, MAX_DAILY_CONTRIBUTIONS)
    
    for _ in range(num_contributions):
        # Create a dummy file for the commit
        with open("dummy.txt", "a") as file:
            file.write(f"Contribution on {date.strftime('%Y-%m-%d')}\n")
        
        # Generate ISO format date for commit
        iso_date = date.strftime('%Y-%m-%dT%H:%M:%S')

        # Set environment variable for author date
        os.environ['GIT_AUTHOR_DATE'] = iso_date
        os.environ['GIT_COMMITTER_DATE'] = iso_date

        # Add and commit the changes with the specific date
        subprocess.run(["git", "add", "dummy.txt"])
        subprocess.run(["git", "commit", "-m", f"Random contribution on {date.strftime('%Y-%m-%d')}"])

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
