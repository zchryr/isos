import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: <program> <filename-to-search>")
        return

    filename = sys.argv[1]
    file_path = "SHA256SUMS"

    try:
        with open(file_path, "r") as file:
            matching_line = ""
            for line in file:
                if filename in line:
                    matching_line = line.strip()
                    break

        if not matching_line:
            print("No matching line found for given filename.")
            return

        with open(file_path, "w") as file:
            file.write(matching_line + "\n")

        print("File updated successfully!")

    except IOError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
