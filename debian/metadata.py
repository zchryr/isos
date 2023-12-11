import os
import requests


def get_debian_stable_version():
    """
    Fetches the Debian stable version from the Debian release information URL.
    """
    url = "https://ftp.debian.org/debian/dists/stable/Release"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed with status code: {response.status_code}")

    for line in response.text.split("\n"):
        if line.startswith("Version:"):
            parts = line.split(":")
            if len(parts) > 1:
                return parts[1].strip()

    raise Exception("Version not found in the release file")


def format_url(version):
    """
    Formats the URL for downloading the Debian image using the provided version.
    """
    base_url = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-{}.0-amd64-netinst.iso"
    return base_url.format(version)


# Example usage
debian_version = get_debian_stable_version()
debian_download_url = format_url(debian_version)

# Check if running in GitHub Actions (CI environment variable set)
if os.getenv("CI") == "true":
    # Append the 'debian_download_url' to the 'GITHUB_ENV' file
    env_file = os.getenv("GITHUB_ENV")
    with open(env_file, "a") as myfile:
        myfile.write(f"download_url={debian_download_url}\n")
else:
    print(debian_download_url)
