package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: <program> <filename-to-search>")
		return
	}

	filename := os.Args[1]
	filePath := "SHA256SUMS"

	file, err := os.Open(filePath)
	if err != nil {
		fmt.Printf("Error opening file: %v\n", err)
		return
	}
	defer file.Close()

	var matchingLine string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.Contains(line, filename) {
			matchingLine = line
			break
		}
	}

	if matchingLine == "" {
		fmt.Println("No matching line found for given filename.")
		return
	}

	err = os.WriteFile(filePath, []byte(matchingLine+"\n"), 0644)
	if err != nil {
		fmt.Printf("Error writing to file: %v\n", err)
		return
	}

	fmt.Println("File updated successfully!")
}


