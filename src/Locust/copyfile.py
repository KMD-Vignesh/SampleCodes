import os
import shutil

def copy_folder_structure_first(source_path, target_path):
    if not os.path.exists(source_path):
        print(f"Source path '{source_path}' does not exist.")
        return
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    for root, dirs, files in os.walk(source_path):
        relative_path = os.path.relpath(root, source_path)
        destination_dir = os.path.join(target_path, relative_path)
        
        for directory in dirs:
            dir_path = os.path.join(destination_dir, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"Created folder: {dir_path}")
        
        for file in files:
            file_source = os.path.join(root, file)
            file_destination = os.path.join(destination_dir, file)
            shutil.copy2(file_source, file_destination)
            print(f"Copied file: {file_source} -> {file_destination}")

source_folder = "path/to/source/TC001"
target_folder = "path/to/target/TC001"
copy_folder_structure_first(source_folder, target_folder)