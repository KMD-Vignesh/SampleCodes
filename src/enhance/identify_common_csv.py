import os
import hashlib
from collections import defaultdict
import polars as pl

def normalize_and_hash_csv(filepath):
    """Read CSV with Polars as string, sort cols + rows, return hash."""
    try:
        df = pl.read_csv(filepath, infer_schema_length=0)
    except Exception as e:
        print(f"Warning: Skipping {filepath} (error: {e})")
        return None

    # Sort columns
    cols = sorted(df.columns)
    df = df.select(cols)
    # Sort rows
    df = df.sort(by=cols)
    # Serialize to canonical string
    csv_str = df.write_csv(None)
    return hashlib.md5(csv_str.encode('utf-8')).hexdigest()

def analyze_nested_csv_folders(main_dir):
    """
    Structure:
    main_dir/
      test1/
        20250325/
          dxquote.csv, dxorder.csv, ...
        20250326/
          ...
      test2/
        ...
    """
    test_folders = [
        f for f in os.listdir(main_dir)
        if os.path.isdir(os.path.join(main_dir, f)) and f.startswith('test')
    ]

    if not test_folders:
        print("No test folders (e.g., test1, test2) found.")
        return {}

    # Map: (date_folder, csv_name) -> hash -> list of test folders
    content_map = defaultdict(lambda: defaultdict(list))

    for test_folder in test_folders:
        test_path = os.path.join(main_dir, test_folder)
        date_folders = [
            d for d in os.listdir(test_path)
            if os.path.isdir(os.path.join(test_path, d))
        ]

        for date_folder in date_folders:
            date_path = os.path.join(test_path, date_folder)
            csv_files = [f for f in os.listdir(date_path) if f.endswith('.csv')]

            for csv_file in csv_files:
                filepath = os.path.join(date_path, csv_file)
                file_hash = normalize_and_hash_csv(filepath)
                if file_hash is not None:
                    content_map[(date_folder, csv_file)][file_hash].append(test_folder)

    # Convert to report: list of groups for each (date_folder, csv_file)
    report = {}
    for (date_folder, csv_file), hash_groups in content_map.items():
        key = (date_folder, csv_file)
        groups = list(hash_groups.values())  # list of lists of test folders
        report[key] = groups

    return report

def print_report(report):
    for (date_folder, csv_file), groups in sorted(report.items()):
        print(f"\n=== {date_folder} {csv_file} ===")
        for group in groups:
            print(f"  {sorted(group)}")

# Usage
if __name__ == "__main__":
    main_directory = input("Enter the main directory path: ").strip()
    if not os.path.isdir(main_directory):
        print("Invalid directory.")
    else:
        report = analyze_nested_csv_folders(main_directory)
        print_report(report)