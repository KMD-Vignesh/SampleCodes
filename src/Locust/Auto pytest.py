import pandas as pd
import pytest

# Read the CSV file
csv_file = "your_file.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Filter only active tests (if 'active' column is present)
if 'active' in df.columns:
    df = df[df['active'] == True]

# Dynamically create pytest test functions
for _, row in df.iterrows():
    test_id = row['testid']
    scenario = row['scenario name']
    test_name = f"test_{scenario.replace(' ', '_')}_{test_id}"

    # Define the test function dynamically
    def make_test_function(test_id, scenario):
        def test_function():
            # Replace this with the actual test logic
            print(f"Running test {test_id} for scenario {scenario}")
            assert True  # Replace with actual assertions
        return test_function

    # Add the test function to the global namespace
    globals()[test_name] = make_test_function(test_id, scenario)

# Run pytest
if __name__ == "__main__":
    pytest.main()
