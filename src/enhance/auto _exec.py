import csv
from collections import OrderedDict

# Read the CSV file
with open('your_file.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Sort data by folder column
data.sort(key=lambda x: x['folder'])

# Track which folders we've seen
seen_folders = set()

# Add execution column
for row in data:
    folder_name = row['folder']
    if folder_name not in seen_folders:
        row['execution'] = 'yes'
        seen_folders.add(folder_name)
    else:
        row['execution'] = 'no'

# Write back to CSV (or a new file)
fieldnames = list(data[0].keys())  # Gets all column names including new 'execution'

with open('output_file.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

# Print to verify
for row in data:
    print(row)