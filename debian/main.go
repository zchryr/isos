package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

func getDebianStableVersion() (string, error) {
	resp, err := http.Get("https://ftp.debian.org/debian/dists/stable/Release")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return "", fmt.Errorf("Failed with status code: %d", resp.StatusCode)
	}

	var buf bytes.Buffer
	if _, err := io.Copy(&buf, resp.Body); err != nil {
		return "", err
	}

	for _, line := range strings.Split(buf.String(), "\n") {
		if strings.HasPrefix(line, "Version:") {
			parts := strings.Split(line, ":")
			if len(parts) > 1 {
				return strings.TrimSpace(parts[1]), nil
			}
		}
	}

	return "", fmt.Errorf("Version not found in the release file")
}

func formatURL(version string) string {
	const baseURL = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-{VERSION}.0-amd64-netinst.iso"
	return strings.ReplaceAll(baseURL, "{VERSION}", version)
}

func main() {
	version, err := getDebianStableVersion()
	if err != nil {
		log.Fatalf("Error: %s", err)
	}
	url := formatURL(version)
	fmt.Println(url)

	// If within GitHub Actions context, set the output.
	githubEnv := os.Getenv("GITHUB_ENV")
	if githubEnv != "" {
		outputString := fmt.Sprintf("download_url=%s\n", url)
		err := os.WriteFile(githubEnv, []byte(outputString), 0644)
		if err != nil {
			log.Fatalf("Failed to write to %s: %s", githubEnv, err)
		}
	} else {
		// If not within GitHub Actions, simply print.
		fmt.Println("Not within a GitHub Actions context, skipping setting output.")
	}
}
