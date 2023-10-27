import argparse
import os
import sys


# Arg parse with a required argument.
def parse_args():
    parser = argparse.ArgumentParser(description="Process codename and SKU arguments.")

    # Add the "-sku" argument
    parser.add_argument(
        "-sku", type=str, required=True, help="The SKU to be processed."
    )

    return parser.parse_args()


# Open SHA256SUMS, find the correct SHA, and re-write the file.
def rewrite_sha(sku):
    new = ""

    # Open the file to find the correct SHA.
    try:
        with open("SHA256SUMS") as file:
            lines = [line.rstrip() for line in file]

            for line in lines:
                if sku in line:
                    new = line
    finally:
        file.close()

    # Re-write the file.
    with open("SHA256SUMS", "w") as file:
        file.write(new)


# Main.
def main():
    args = parse_args()

    # Check if the file exists
    if not os.path.exists("SHA256SUMS"):
        print(f"The file SHA256SUMS does not exist!")
        sys.exit(1)

    rewrite_sha(sku=args.sku)


if __name__ == "__main__":
    main()
