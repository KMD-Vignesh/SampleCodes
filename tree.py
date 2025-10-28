import os

# Directories and file name substrings to exclude
EXCLUDE_DIRS = {".venv", "__pycache__", ".git", ".idea", ".mypy_cache", "migrations"}
EXCLUDE_FILE_SUBSTRINGS = {".DS_Store", ".pyc", "__pycache__", ".log"}

def print_tree(start_path='.', prefix=''):
    try:
        entries = os.listdir(start_path)
    except PermissionError:
        print(prefix + "├── [Permission Denied]")
        return

    # Filter out unwanted entries
    filtered_entries = []
    for e in entries:
        if e in EXCLUDE_DIRS:
            continue
        full_path = os.path.join(start_path, e)
        if os.path.isfile(full_path):
            if any(sub in e for sub in EXCLUDE_FILE_SUBSTRINGS):
                continue
        filtered_entries.append(e)

    # Sort the remaining entries
    filtered_entries.sort()

    # Print each entry
    for i, entry in enumerate(filtered_entries):
        path = os.path.join(start_path, entry)
        connector = "└── " if i == len(filtered_entries) - 1 else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if i == len(filtered_entries) - 1 else "│   "
            print_tree(path, prefix + extension)

# Example usage
if __name__ == "__main__":
    print_tree("/Users/vigneshd/Projects/KMDV-CRM")