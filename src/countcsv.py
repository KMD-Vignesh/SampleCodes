import os
import csv

directory = "/path/to/your/csv/files"  # Change this to your directory

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = sum(1 for _ in reader) - 1  # exclude header
        print(f"{filename}: {row_count} rows (excluding header)")