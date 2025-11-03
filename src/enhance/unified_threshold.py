import os
import polars as pl
from pathlib import Path

def combine_threshold_files(main_dir, output_path, filename_pattern="threshold"):
    """
    Combine all CSV files under main_dir that contain 'threshold' in their filename.
    Adds:
      - 'testcaseid': grandparent folder (e.g., test1)
      - 'date': parent folder (e.g., 20250325)
    """
    main_path = Path(main_dir)
    if not main_path.is_dir():
        raise ValueError(f"Main directory does not exist: {main_dir}")

    all_dfs = []
    pattern_lower = filename_pattern.lower()

    # Walk through all subdirectories recursively
    for csv_path in main_path.rglob("*.csv"):
        if pattern_lower in csv_path.name.lower():
            # Get parent (date) and grandparent (testcaseid)
            parent = csv_path.parent.name          # e.g., "20250325"
            grandparent = csv_path.parent.parent.name  # e.g., "test1"

            try:
                # Read CSV with all columns as string (safe for merging)
                df = pl.read_csv(csv_path, infer_schema_length=0)
            except Exception as e:
                print(f"⚠️  Skipping {csv_path}: {e}")
                continue

            # Add metadata columns
            df = df.with_columns([
                pl.lit(grandparent).alias("testcaseid"),
                pl.lit(parent).alias("date")
            ])

            all_dfs.append(df)
            print(f"✅ Loaded: {csv_path} → testcaseid={grandparent}, date={parent}")

    if not all_dfs:
        print("❌ No files matched the pattern.")
        return

    # Combine all DataFrames
    combined = pl.concat(all_dfs, how="vertical")

    # Optional: reorder columns to put metadata first
    original_cols = [col for col in combined.columns if col not in ("testcaseid", "date")]
    combined = combined.select(["testcaseid", "date", *original_cols])

    # Save to output CSV
    combined.write_csv(output_path)
    print(f"\n🎉 Combined {len(all_dfs)} files into: {output_path}")
    print(f"📊 Total rows: {combined.shape[0]}")

# --- Usage ---
if __name__ == "__main__":
    main_directory = input("Enter main directory path: ").strip()
    output_file = input("Enter output CSV file path (e.g., combined_threshold.csv): ").strip()

    try:
        combine_threshold_files(main_directory, output_file, filename_pattern="threshold")
    except Exception as e:
        print(f"❌ Error: {e}")