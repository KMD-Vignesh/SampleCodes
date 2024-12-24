import os
import pandas as pd


def generate_html(test_cases, init_files_folder, output_file="report.html"):
    """
    Generate an HTML test report dynamically with a popup to display CSV content.

    Args:
        test_cases (dict): Dictionary of test cases with steps and statuses.
        init_files_folder (str): Path to folder containing test case subdirectories with CSV files.
        output_file (str): Output HTML file name.
    """
    # HTML head
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Report</title>
        <style>
            body { margin: 0; font-family: Arial, sans-serif; display: flex; flex-direction: column; height: 100vh; }
            .menu-bar { background: #333; color: white; padding: 10px; display: flex; justify-content: space-between; }
            .menu a { color: white; text-decoration: none; margin: 0 10px; cursor: pointer; }
            .container { display: flex; flex-grow: 1; overflow: hidden; }
            .test-cases { flex: 1; background: #f4f4f4; padding: 10px; overflow-y: auto; border-right: 1px solid #ddd; }
            .test-case { padding: 10px; margin-bottom: 5px; border: 1px solid #ccc; border-radius: 5px; cursor: pointer; }
            .test-case.pass { background-color: #d4edda; }
            .test-case.fail { background-color: #f8d7da; }
            .test-case.skip { background-color: #ffeeba; }
            .test-case.active { border: 2px solid #333; }
            .test-steps { flex: 2; padding: 10px; overflow-y: auto; }
            .test-step { margin-bottom: 10px; }
            .popup-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); display: none; z-index: 1000; }
            .popup { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border-radius: 5px; max-width: 80%; max-height: 80%; overflow: auto; z-index: 1001; }
            .close-popup { float: right; background: red; color: white; border: none; padding: 5px 10px; cursor: pointer; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f4f4f4; }
        </style>
    </head>
    <body>
        <div class="menu-bar">
            <div class="menu">
                <a href="#" id="testcases-link">Test Cases</a>
                <a href="#" id="summary-link">Summary</a>
            </div>
        </div>
        <div class="container">
            <div class="test-cases" id="test-cases">
    """

    # Add test cases
    for test_case, details in test_cases.items():
        status_class = details["status"].lower()
        html += f'<div class="test-case {status_class}" onclick="showTestSteps(\'{test_case}\')">{test_case}<span>{details["status"]}</span></div>'

    html += """
            </div>
            <div class="test-steps" id="test-steps"></div>
        </div>
        <div class="popup-overlay" id="popup-overlay" onclick="closePopup()"></div>
        <div class="popup" id="popup">
            <button class="close-popup" id="close-popup" onclick="closePopup()">Close</button>
            <div id="popup-content"></div>
        </div>
        <script>
            const testStepsData = {
    """

    # Add steps for each test case
    for test_case, details in test_cases.items():
        html += f'"{test_case}": ['
        for step in details["steps"]:
            if "table" in step.lower():
                html += f'"{step} <a href=\'#\' onclick=\\"openPopup(\'{test_case}\')\\">View Table</a>", '
            else:
                html += f'"{step}", '
        html = html.rstrip(", ") + "],"

    html = html.rstrip(",") + """
            };

            const csvData = {
    """

    # Add CSV file content for each test case
    for test_case, details in test_cases.items():
        test_case_folder = os.path.join(init_files_folder, test_case)
        if os.path.exists(test_case_folder) and os.path.isdir(test_case_folder):
            csv_files = [f for f in os.listdir(test_case_folder) if f.endswith(".csv")]
            if csv_files:
                html += f'"{test_case}": {{'
                for csv_file in csv_files:
                    file_path = os.path.join(test_case_folder, csv_file)
                    df = pd.read_csv(file_path)
                    table_html = df.to_html(index=False, classes="csv-table")
                    html += f'"{csv_file}": `{table_html}`, '
                html = html.rstrip(", ") + "},"

    html = html.rstrip(",") + """
            };

            function showTestSteps(testCaseName) {
                const steps = testStepsData[testCaseName] || ["No steps available."];
                const stepDiv = document.getElementById('test-steps');
                stepDiv.innerHTML = `<h2>${testCaseName}</h2>` + steps.map(step => `<div class="test-step">${step}</div>`).join('');
            }

            function openPopup(testCaseName) {
                const popupContent = document.getElementById('popup-content');
                const files = csvData[testCaseName] || {};
                let content = "";
                for (const [fileName, tableHtml] of Object.entries(files)) {
                    content += `<h3>${fileName}</h3>${tableHtml}`;
                }
                popupContent.innerHTML = content;
                document.getElementById('popup-overlay').style.display = 'block';
                document.getElementById('popup').style.display = 'block';
            }

            function closePopup() {
                document.getElementById('popup-overlay').style.display = 'none';
                document.getElementById('popup').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML report generated: {output_file}")


# Example data
test_cases = {
    "TestCase1": {
        "steps": ["Step 1", "Step 2 with table"],
        "status": "Pass",
    },
    "TestCase2": {
        "steps": ["Step 1 with table", "Step 2"],
        "status": "Fail",
    },
    "TestCase3": {
        "steps": ["Step 1", "Step 2 with table"],
        "status": "Skip",
    },
}

# Path to CSV folder
init_files_folder = "initfiles"

# Generate HTML
generate_html(test_cases, init_files_folder)
