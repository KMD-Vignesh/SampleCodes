import os
import pandas as pd

def get_int_files(base_dir: str) -> dict[str, dict[str, pd.DataFrame]]:
    testcase_data: dict[str,dict[str,pd.DataFrame]] = {}
    testcase_folders: list[str] = sorted(
        [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    )
    for testcase_folder in testcase_folders:
        folder_path: str = os.path.join(base_dir, testcase_folder)
        csv_files_data: dict = {}
        csv_files_with_ctime: list = []
        for file_name in os.listdir(path=folder_path):
            if file_name.endswith('.csv'): 
                file_path: str = os.path.join(folder_path, file_name)
                creation_time: float = os.path.getctime(filename=file_path) 
                csv_files_with_ctime.append((file_name, file_path, creation_time))
        csv_files_with_ctime.sort(key=lambda x: x[2])
        for file_name, file_path, _ in csv_files_with_ctime:
            df: pd.DataFrame = pd.read_csv(filepath_or_buffer=file_path)
            csv_files_data[file_name] = df
        testcase_data[testcase_folder] = csv_files_data
    return testcase_data

test_int_data: dict[str, dict[str, pd.DataFrame]] = get_int_files(base_dir="data")
test_step_data: dict = {}
for key, value in test_int_data.items():
    print(key)
    for key1, value1 in value.items():
        print(key1)