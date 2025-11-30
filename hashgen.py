import hashlib
import os
import sys

# Default generated folder
DEFAULT_GEN_FOLDER = "_builds/_out"

def compute_hash(folder):
    hasher = hashlib.sha256()

    for root, dirs, files in os.walk(folder):
        for filename in sorted(files):
            if filename.endswith((".c", ".h")):
                filepath = os.path.join(root, filename)
                with open(filepath, "rb") as f:
                    hasher.update(f.read())

    return hasher.hexdigest()


def main():
    # Use argument if provided, otherwise default
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GEN_FOLDER

    if not os.path.isdir(folder):
        print(f"ERROR: Folder '{folder}' not found.")
        return

    # Compute hash
    hex_value = compute_hash(folder)

    # Ensure output folder exists
    output_folder = "_hashgen"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "hash.txt")

    # Write hash to file
    with open(output_file, "w") as f:
        f.write(hex_value)

    print(f"[INFO] Hash generated: {hex_value}")
    print(f"[INFO] Saved to {output_file}")


if __name__ == "__main__":
    main()
