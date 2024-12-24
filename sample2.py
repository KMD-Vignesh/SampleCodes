import os
import csv

def generate_html(folder_path: str, output_file: str):
    """
    Generates an HTML file to display test cases and their steps with a CSV table popup.
    :param folder_path: Path to the folder containing intermittent CSV files for each test case.
    :param output_file: Path to save the generated HTML file.
    """
    # Fetch test case files
    test_cases = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            test_cases.append(file)

    # Build test case and step information
    test_case_data = []
    for test_case_file in test_cases:
        steps = []
        with open(os.path.join(folder_path, test_case_file), "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                steps.append({
                    "text": row["Action"],
                    "file": f"{folder_path}/{row['StepID']}_Table.csv" if row["HasTable"].upper() == "TRUE" else None
                })
        test_case_data.append({
            "name": test_case_file.replace(".csv", ""),
            "steps": steps
        })

    # Generate HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Cases Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
        }}
        .container {{
            display: flex;
            width: 100%;
        }}
        .test-cases {{
            width: 30%;
            background-color: #f4f4f4;
            padding: 10px;
            border-right: 1px solid #ddd;
            overflow-y: auto;
        }}
        .test-case {{
            margin: 5px 0;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            cursor: pointer;
        }}
        .test-steps {{
            width: 70%;
            padding: 10px;
            overflow-y: auto;
        }}
        .table-popup {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            background: #fff;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            padding: 15px;
            z-index: 1000;
            display: none;
        }}
        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4);
            z-index: 999;
            display: none;
        }}
        .close-btn {{
            display: block;
            margin-top: 10px;
            text-align: center;
            color: white;
            background: red;
            padding: 10px;
            border: none;
            cursor: pointer;
            text-transform: uppercase;
        }}
        .close-btn:hover {{
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Test Cases Section -->
        <div class="test-cases">
            <h3>Test Cases</h3>
    """
    # Add test case buttons dynamically
    for idx, test_case in enumerate(test_case_data):
        html_content += f"""
            <div class="test-case" onclick="showTestCase({idx})">{test_case['name']}</div>
        """

    # Continue HTML content
    html_content += """
        </div>
        <!-- Test Steps Section -->
        <div class="test-steps" id="test-steps">
            <h3>Test Steps</h3>
            <div id="test-steps-content">
                Select a test case from the left to view details.
            </div>
        </div>
    </div>
    <div class="overlay" id="overlay"></div>
    <div class="table-popup" id="table-popup">
        <div id="table-content"></div>
        <button class="close-btn" onclick="closePopup()">Close</button>
    </div>
    <script>
        const testcases = {test_case_data};

        function showTestCase(idx) {{
            const testcase = testcases[idx];
            const stepsDiv = document.getElementById('test-steps-content');
            stepsDiv.innerHTML = `<h4>${{testcase.name}}</h4><ul>` + 
                testcase.steps.map((step, index) => {{
                    if (step.file) {{
                        return `<li>${{step.text}} - <a href="#" onclick="showPopup('${{step.file}}')">View Table</a></li>`;
                    }}
                    return `<li>${{step.text}}</li>`;
                }}).join("") + `</ul>`;
        }}

        function showPopup(file) {{
            const tableContentDiv = document.getElementById('table-content');
            fetch(file)
                .then(response => response.text())
                .then(csv => {{
                    tableContentDiv.innerHTML = `<pre>${{csv}}</pre>`;
                    document.getElementById('overlay').style.display = 'block';
                    document.getElementById('table-popup').style.display = 'block';
                }});
        }}

        function closePopup() {{
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('table-popup').style.display = 'none';
        }}
    </script>
</body>
</html>
"""
    # Write the content to the output file
    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"HTML file generated at: {output_file}")


# Specify folder with CSV files and output HTML file
generate_html("path/to/csv/folder", "test_cases_viewer.html")
