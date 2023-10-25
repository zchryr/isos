import requests
from datetime import datetime
import json

# Get the current time
now = datetime.now()

response = requests.get("https://ubuntu.com/security/releases.json")
json_data = response.json()

lts_releases = []
last_3_lts_releases = []
matrix = []

for release in json_data["releases"]:
    if release["version"] != None:
        if release["lts"] == True:
            if now > datetime.strptime(release["release_date"], "%Y-%m-%dT%H:%M:%S"):
                lts_releases.append(release)
                last_3_lts_releases.append(float(release["version"]))

last_3_lts_releases.sort(reverse=True)
last_3_lts_releases = last_3_lts_releases[:3]

server_url = "https://releases.ubuntu.com/{}/ubuntu-{}-live-server-amd64.iso"

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

                response = requests.head(
                    url
                )  # Send a HEAD request to get the status_code
                # print("status: " + str(response.status_code))

                if response.status_code == 200:
                    lts = release
                    lts["download_url"] = url
                    matrix.append(lts)
                    # print("valid")
                    break  # Break out of the while loop if a valid link is found

                minor_version += 1
                if (
                    minor_version > 10
                ):  # Arbitrary upper limit to avoid infinite looping
                    break

print(json.dumps(matrix))
