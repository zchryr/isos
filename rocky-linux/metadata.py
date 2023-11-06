import requests  # Make HTTP requests.
from bs4 import BeautifulSoup  # Parse HTML.
import re  # Regex.
import json  # JSON.
import os  # OS.


# Function to add to GITHUB_OUTPUT env var.
def set_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"{name}={value}", file=fh)


# Variables.
github_actions = False  # If in GitHub Actions context.

if os.environ.get("GITHUB_ACTION") != None:
    github_actions = True


def get_latest_version():
    # Send HTTP GET request to the Rocky Linux download page.
    response = requests.get("https://download.rockylinux.org/pub/rocky/")

    # Parse HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all "href" attributes in anchor tags, extract numbers (versions), and save them to a list.
    versions = [
        re.search(r"([0-9]\.[0-9]+)", a["href"]).group()
        for a in soup.find_all("a", href=True)
        if re.search(r"([0-9]\.[0-9]+)", a["href"])
    ]

    # Return the latest version (maximum number).
    return max(versions, key=float)


def get_iso_url(file_name):
    # Get the latest Rocky Linux version.
    latest_version = get_latest_version()

    # Construct file name using latest version.
    url = "https://download.rockylinux.org/pub/rocky/{}/isos/x86_64/{}".format(
        latest_version, file_name
    )

    return url  # This is the download URL for the requested ISO type (either boot or minimal).


# Create two dictionaries in a list, each containing an "iso_url" with the download URL for the corresponding Rocky Linux ISO.
matrix = [
    {
        "name": "boot",
        "download_url": get_iso_url(
            "Rocky-{}-x86_64-boot.iso".format(get_latest_version())
        ),
        "version": get_latest_version(),
        "major_version": get_latest_version().split(".")[0],
    },
    {
        "name": "minimal",
        "download_url": get_iso_url(
            "Rocky-{}-x86_64-minimal.iso".format(get_latest_version())
        ),
        "version": get_latest_version(),
        "major_version": get_latest_version().split(".")[0],
    },
]

if github_actions:
    set_output("matrix", json.dumps(matrix))
else:
    print(json.dumps(matrix, indent=4))
