import os
import hashlib
from collections import defaultdict
import polars as pl

def normalize_and_hash_csv(filepath):
    try:
        df = pl.read_csv(filepath, infer_schema_length=0)
    except Exception as e:
        print(f"Warning: Skipping {filepath} (error: {e})")
        return None

    cols = sorted(df.columns)
    df = df.select(cols).sort(by=cols)
    csv_str = df.write_csv(None)
    return hashlib.md5(csv_str.encode('utf-8')).hexdigest()

def analyze_nested_csv_folders(main_dir):
    test_folders = [
        f for f in os.listdir(main_dir)
        if os.path.isdir(os.path.join(main_dir, f)) and f.startswith('test')
    ]

    if not test_folders:
        print("No test folders (e.g., test1, test2) found.")
        return []

    content_map = defaultdict(lambda: defaultdict(list))

    for test_folder in test_folders:
        test_path = os.path.join(main_dir, test_folder)
        if not os.path.isdir(test_path):
            continue
        date_folders = [
            d for d in os.listdir(test_path)
            if os.path.isdir(os.path.join(test_path, d))
        ]

        for date_folder in date_folders:
            date_path = os.path.join(test_path, date_folder)
            csv_files = [f for f in os.listdir(date_path) if f.endswith('.csv')]

            for csv_file in csv_files:
                filepath = os.path.join(date_path, csv_file)
                if not os.path.isfile(filepath):
                    continue
                file_hash = normalize_and_hash_csv(filepath)
                if file_hash is not None:
                    content_map[(date_folder, csv_file)][file_hash].append(test_folder)

    # Build list of rows for CSV
    rows = []
    for (date_folder, csv_file), hash_groups in content_map.items():
        for test_list in hash_groups.values():
            # Sort test folders for consistent output (e.g., test1,test2 not test2,test1)
            test_list_sorted = sorted(test_list)
            rows.append({
                "date_folder": date_folder,
                "csv_file": csv_file,
                "test_folders": ",".join(test_list_sorted)
            })

    return rows

def main():
    main_directory = input("Enter the main directory path: ").strip()
    output_csv = input("Enter output CSV file path (e.g., report.csv): ").strip()

    if not os.path.isdir(main_directory):
        print("Error: Main directory not found.")
        return

    print("Analyzing folders...")
    rows = analyze_nested_csv_folders(main_directory)

    if not rows:
        print("No CSV files found to compare.")
        return

    # Create Polars DataFrame and write to CSV
    df = pl.DataFrame(rows)
    df.write_csv(output_csv)
    print(f"✅ Report saved to: {output_csv}")
    print(f"📊 Total groups: {len(rows)}")

if __name__ == "__main__":
    main()