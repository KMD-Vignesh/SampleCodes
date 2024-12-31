import os
import pandas as pd

# Path to the reference (full data) CSV
reference_csv_path = "path/to/full_data.csv"

# Base folder containing the other minimal CSVs
base_folder = "path/to/your/base/folder"

# Path for the log file
log_file_path = "path/to/mismatch_log.txt"

# Load the reference CSV
reference_df = pd.read_csv(reference_csv_path)

# Track mismatched timespan values
mismatched_timespan_log = []

# Loop through all files in the directory and subdirectories
for root, _, files in os.walk(base_folder):
    for file_name in files:
        if file_name.endswith(".csv") and "quote" in file_name:
            file_path = os.path.join(root, file_name)
            
            # Load the minimal CSV
            target_df = pd.read_csv(file_path)
            
            # Find timespan mismatches
            missing_timespan = target_df.loc[~target_df['timespan'].isin(reference_df['timespan']), 'timespan']
            if not missing_timespan.empty:
                # Log the mismatched timespan with the file path
                mismatched_timespan_log.append({
                    "file": file_path,
                    "mismatched_timespans": missing_timespan.tolist()
                })
            
            # Perform a VLOOKUP-like operation (merge on 'timespan')
            updated_df = pd.merge(
                target_df, 
                reference_df, 
                on='timespan', 
                how='left', 
                suffixes=('', '_ref')
            )
            
            # Update existing columns and add missing columns
            for column in reference_df.columns:
                if column != 'timespan':  # 'timespan' is used for the merge
                    # Update the column values if they exist
                    if f"{column}_ref" in updated_df.columns:
                        updated_df[column] = updated_df[f"{column}_ref"]
                        updated_df.drop(columns=[f"{column}_ref"], inplace=True)
                    # Add missing columns
                    elif column not in updated_df.columns:
                        updated_df[column] = reference_df[column]
            
            # Save the updated file back to its original location
            updated_df.to_csv(file_path, index=False)

# Save mismatched timespan information to the log file
with open(log_file_path, "w") as log_file:
    for entry in mismatched_timespan_log:
        log_file.write(f"File: {entry['file']}\n")
        log_file.write(f"Mismatched Timespans: {', '.join(map(str, entry['mismatched_timespans']))}\n\n")

print("All files processed and mismatches logged.")
