import os
import pandas as pd

# ---------- CONFIGURE ----------
INDEX_FILE   = r"test-data/rework.csv"          # master list
MAIN_DIR     = r"test-data"                     # root folder to search
OUTPUT_FILE  = r"test-data/compiled_output.csv" # final combined file
THRESHOLD_NAME_CONTAINS = "sample3"  # This can be passed from the main if needed

# ---------- UTIL ----------
def find_folder(root: str, target: str) -> str | None:
    """Return full path of the first folder whose basename == target."""
    for dirpath, dirnames, _ in os.walk(root):
        if target in dirnames:
            return os.path.join(dirpath, target)
    return None

def read_sheet(file_path: str) -> pd.DataFrame:
    """Read file into DataFrame, drop empty rows and columns."""
    try:
        if file_path.endswith(('.xlsx', '.xlsm', '.xls', '.xltm', '.xltx')):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        return df.dropna(how="all").dropna(axis=1, how="all")
    except Exception as e:
        print(f"[WARN] Error reading {file_path}: {e}")
        return pd.DataFrame()

# ---------- TASK A ----------
def task_a_update(folder_path: str, file_name: str, col_name: str) -> None:
    """Update the workbook <file_name> in <folder_path> with folder name."""
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
        print(f"[WARN] Task-A: {file_name} not found in {folder_path}")
        return

    df = read_sheet(file_path)
    if df.empty:
        print(f"[WARN] Task-A: {file_name} is empty or could not be read.")
        return

    folder_name = os.path.basename(folder_path)
    df[col_name] = folder_name

    if file_path.endswith(('.xlsx', '.xlsm', '.xls', '.xltm', '.xltx')):
        df.to_excel(file_path, index=False)
    elif file_path.endswith('.csv'):
        df.to_csv(file_path, index=False)
    print(f"[A] Updated {file_name} in {folder_path}")

# ---------- TASK B ----------
def task_b_collect(folder_path: str, file_name_contains: str) -> pd.DataFrame | None:
    """Return DataFrame from the first CSV file in <folder_path> whose name contains <file_name_contains>."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv') and file_name_contains in file_name:
            file_path = os.path.join(folder_path, file_name)
            df = read_sheet(file_path)
            if not df.empty:
                df["Folder"] = os.path.basename(folder_path)
                return df
    print(f"[WARN] Task-B: No CSV file containing '{file_name_contains}' found in {folder_path}")
    return None

# ---------- MAIN ----------
def main():
    idx = pd.read_csv(INDEX_FILE)
    b_frames: list[pd.DataFrame] = []

    for _, row in idx.iterrows():
        folder_name = str(row["FolderName"]).strip()
        file_name   = str(row["FileName"]).strip()
        col_name    = str(row["ColumnName"]).strip()

        folder_path = find_folder(MAIN_DIR, folder_name)
        if not folder_path:
            print(f"[WARN] Folder '{folder_name}' not found under {MAIN_DIR}")
            continue

        # ---- run both tasks ----
        task_a_update(folder_path, file_name, col_name)

        b_df = task_b_collect(folder_path, THRESHOLD_NAME_CONTAINS)
        if b_df is not None:
            b_frames.append(b_df)

    # ---- concatenate Task-B results ----
    if b_frames:
        final_df = pd.concat(b_frames, ignore_index=True)
        final_df.to_csv(OUTPUT_FILE, index=False)
        print(f"[DONE] Compiled Task-B data into {OUTPUT_FILE}")
    else:
        print("[WARN] No Task-B data to save.")

if __name__ == "__main__":
    main()