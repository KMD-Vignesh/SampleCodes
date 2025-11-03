import os
import hashlib
from collections import defaultdict
import polars as pl

def normalize_and_hash_csv(filepath):
    """Read CSV with Polars, sort columns and rows, return MD5 hash of normalized content."""
    try:
        # Read all columns as Utf8 (string) to avoid type inconsistencies
        df = pl.read_csv(filepath, infer_schema_length=0)
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return None

    # Sort columns alphabetically
    sorted_cols = sorted(df.columns)
    df = df.select(sorted_cols)

    # Sort rows lexicographically across all columns
    df = df.sort(by=sorted_cols)

    # Serialize to consistent CSV string (without index, row order fixed)
    csv_str = df.write_csv(None)  # Returns string if file=None
    return hashlib.md5(csv_str.encode('utf-8')).hexdigest()

def analyze_csv_folders(main_dir):
    # Get immediate subdirectories
    folders = [f for f in os.listdir(main_dir) 
               if os.path.isdir(os.path.join(main_dir, f))]
    if not folders:
        print("No subfolders found.")
        return {}

    # Discover all CSV filenames across folders
    all_csv_files = set()
    for folder in folders:
        folder_path = os.path.join(main_dir, folder)
        try:
            files = os.listdir(folder_path)
            csvs = [f for f in files if f.endswith('.csv')]
            all_csv_files.update(csvs)
        except OSError as e:
            print(f"Error reading folder {folder_path}: {e}")

    all_csv_files = sorted(all_csv_files)

    # Build report: for each CSV file, group folders by content hash
    report = {}

    for csv_file in all_csv_files:
        hash_to_folders = defaultdict(list)
        for folder in folders:
            filepath = os.path.join(main_dir, folder, csv_file)
            if os.path.isfile(filepath):
                file_hash = normalize_and_hash_csv(filepath)
                if file_hash is not None:
                    hash_to_folders[file_hash].append(folder)
        # Only keep groups with 2 or more folders (optional)
        grouped = [group for group in hash_to_folders.values() if len(group) >= 2]
        report[csv_file] = grouped

    return report

def print_report(report):
    for csv_file, groups in report.items():
        print(f"\n=== {csv_file} ===")
        if not groups:
            print("  No duplicates found.")
        else:
            for group in groups:
                print(f"  {group}")

# Usage
if __name__ == "__main__":
    main_directory = input("Enter the main directory path: ").strip()
    if not os.path.isdir(main_directory):
        print("Invalid directory.")
    else:
        report = analyze_csv_folders(main_directory)
        print_report(report)