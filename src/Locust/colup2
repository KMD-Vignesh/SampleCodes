import os
import pandas as pd

def update_csv_data(reference_csv_path, base_folder, log_file_path, table_name, date, column_mapping):
    reference_df = pd.read_csv(reference_csv_path)
    mismatched_log = []

    for root, _, files in os.walk(base_folder):
        for file_name in files:
            if file_name.endswith(".csv") and table_name in file_name and date in file_name:
                file_path = os.path.join(root, file_name)
                target_df = pd.read_csv(file_path)

                # Find mismatched transactTime
                missing_values = target_df.loc[
                    ~target_df["transactTime"].isin(reference_df["transactTime"]),
                    "transactTime"
                ]
                if not missing_values.empty:
                    mismatched_log.append({
                        "file": file_path,
                        "mismatched_values": missing_values.tolist()
                    })

                # Add missing columns with values from reference_df
                for column in reference_df.columns:
                    if column not in target_df.columns:
                        target_df[column] = target_df["transactTime"].map(
                            reference_df.set_index("transactTime")[column]
                        )

                # Remove excess columns not in reference_df
                reference_columns = set(reference_df.columns)
                excess_columns = set(target_df.columns) - reference_columns
                target_df.drop(columns=list(excess_columns), inplace=True)

                # Update specific columns based on column_mapping
                columns_to_update = column_mapping.get(table_name, [])
                for column in columns_to_update:
                    if column in reference_df.columns and column in target_df.columns:
                        target_df[column] = target_df["transactTime"].map(
                            reference_df.set_index("transactTime")[column]
                        )

                # Save the updated CSV
                target_df.to_csv(file_path, index=False)

    # Log mismatched transactTime
    with open(log_file_path, "w") as log_file:
        for entry in mismatched_log:
            log_file.write(f"File: {entry['file']}\n")
            log_file.write(f"Mismatched transactTime: {', '.join(map(str, entry['mismatched_values']))}\n\n")

if __name__ == "__main__":
    reference_csv_path = "data/reference/20231114/dxQuote_20231114.csv"
    file_name = os.path.basename(reference_csv_path)
    table_name, date = file_name.split(".csv")[0].split("_")
    base_folder = "data/base_dir"
    log_file_path = f"{table_name}_{date}_mismatch_log.txt"

    column_mapping = {
        "dxQuote": ["column1", "column2", "column3"],  # Replace with actual column names
        "dxTrade": ["column4", "column5"],            # Replace with actual column names
    }

    update_csv_data(
        reference_csv_path=reference_csv_path, 
        base_folder=base_folder, 
        log_file_path=log_file_path, 
        table_name=table_name, 
        date=date, 
        column_mapping=column_mapping
    )