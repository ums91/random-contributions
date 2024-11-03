import os
import random
import subprocess
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

# Create random commits on random dates within the specified range
for _ in range(num_contributions):
    date, iso_date = random_date()
    
    # Create a dummy file for the commit
    with open("dummy.txt", "a") as file:
        file.write(f"Contribution on {date}\n")
    
    # Add and commit the changes with the specific date
    subprocess.run(["git", "add", "dummy.txt"])
    subprocess.run(["git", "commit", "-m", f"Random contribution on {date}", "--date", iso_date])

# Inform the user of the number of contributions created
print(f"Created {num_contributions} random contributions between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}. You can now push to your GitHub repository.")
