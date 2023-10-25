import requests
from datetime import datetime
import json
import os


# Function to add to GITHUB_OUTPUT env var.
def set_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"{name}={value}", file=fh)


# Variables.
now = datetime.now()  # Get the current time.
lts_releases = []  # List for LTS releases.
last_3_lts_releases = []  # List for latest LTS release versions.
matrix = []  # List for Python matrix for output.
github_actions = False

# Sets github_actions = True if running in GitHub Actions environment.
if os.environ.get("GITHUB_ACTION") != None:
    github_actions = True

# Get Ubuntu releases from Ubuntu API.
response = requests.get("https://ubuntu.com/security/releases.json")
json_data = response.json()

# Iterate over releases and save LTS versions to lists.
for release in json_data["releases"]:
    if release["version"] != None:
        if release["lts"] == True:
            if now > datetime.strptime(release["release_date"], "%Y-%m-%dT%H:%M:%S"):
                lts_releases.append(release)
                last_3_lts_releases.append(float(release["version"]))

# Sort list in reverse.
last_3_lts_releases.sort(reverse=True)

# Shorten list to latest 3 releases.
last_3_lts_releases = last_3_lts_releases[:3]

# URL for live-server downloads from Ubuntu.
server_url = "https://releases.ubuntu.com/{}/ubuntu-{}-live-server-amd64.iso"

# Check release URL for valid versions.
for lts in last_3_lts_releases:
    for release in lts_releases:
        if float(release["version"]) == lts:
            minor_version = 0
            while True:  # Keep trying minor versions
                if minor_version == 0:  # If it's the base version
                    version_string = release["version"]
                else:
                    version_string = "{}.{}".format(release["version"], minor_version)

                url = server_url.format(release["codename"], version_string)

                print(
                    "Testing: "
                    + release["version"]
                    + "."
                    + str(minor_version)
                    + " - "
                    + release["codename"]
                )
                response = requests.head(
                    url
                )  # Send a HEAD request to get the status_code

                if response.status_code == 200:
                    lts = release
                    lts["download_url"] = url
                    matrix.append(lts)
                    print(
                        "Found valid version: "
                        + release["version"]
                        + "."
                        + str(minor_version)
                        + " - "
                        + release["codename"]
                    )

                    break  # Break out of the while loop if a valid link is found

                minor_version += 1
                if (
                    minor_version > 10
                ):  # Arbitrary upper limit to avoid infinite looping
                    break

if github_actions:
    set_output("matrix", json.dumps(matrix))
else:
    print(json.dumps(matrix))
