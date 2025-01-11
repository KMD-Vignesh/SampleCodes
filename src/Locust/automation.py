import os
import csv
import pytest
import subprocess
import time


# Read test cases from the CSV file
def load_test_cases_from_csv():
    config_file = "config.csv"
    test_cases = []
    with open(config_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Only include active test cases
            if row["Active"].strip().lower() == "yes":
                test_cases.append({
                    "name": row["Test Case Name"],
                    "folder": row["Folder"],
                    "scenario": row["Scenario"],
                    "active": row["Active"]
                })
    return test_cases


# Function to create a dynamic test function
def create_test_function(test_case):
    def test_func(self):
        test_folder = os.path.join("test_data", test_case["folder"])
        assert os.path.exists(test_folder), f"Folder {test_case['folder']} does not exist."

        # Start File Watcher
        watcher_process = subprocess.Popen(
            ["python", "file_watcher_data_writer.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Validate Scenario
        try:
            time.sleep(5)  # Simulate runtime
            result = subprocess.run(
                ["python", "scenario_validator.py", test_folder],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, f"Validation failed for {test_case['name']}: {result.stderr}"
        finally:
            watcher_process.terminate()
    return test_func


# Dynamically generate classes and test cases
def create_dynamic_classes_and_tests():
    test_cases = load_test_cases_from_csv()
    classes = {}

    # Loop through each test case and create classes and test functions
    for test_case in test_cases:
        scenario = test_case["scenario"]

        # Dynamically create a class for each scenario if it doesn't exist
        class_name = f"Test{scenario}"  # Classes must start with 'Test' for pytest
        if class_name not in classes:
            classes[class_name] = type(class_name, (object,), {})  # Create a new class dynamically

        # Create a test function and add it to the class
        test_func = create_test_function(test_case)
        test_func_name = f"test_{test_case['name']}"  # Test methods must start with 'test_'
        setattr(classes[class_name], test_func_name, test_func)

    # Return the dynamically created classes
    return classes


# Dynamically create classes and add them to globals
dynamic_classes = create_dynamic_classes_and_tests()
globals().update(dynamic_classes)