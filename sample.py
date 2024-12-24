import os
import pandas as pd
from typing import List

def generate_html(testcases: List[dict], output_file: str = "index.html"):
    # Generate dynamic HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Cases Viewer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                height: 100vh;
            }
            .container {
                display: flex;
                width: 100%;
            }
            .test-cases {
                width: 30%;
                background-color: #f4f4f4;
                padding: 10px;
                border-right: 1px solid #ddd;
                overflow-y: auto;
            }
            .test-case {
                margin: 5px 0;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                cursor: pointer;
            }
            .test-steps {
                width: 70%;
                padding: 10px;
                overflow-y: auto;
            }
            .table-popup {
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
            }
            .overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.4);
                z-index: 999;
                display: none;
            }
            .close-btn {
                display: block;
                margin-top: 10px;
                text-align: center;
                color: white;
                background: red;
                padding: 10px;
                border: none;
                cursor: pointer;
                text-transform: uppercase;
            }
            .close-btn:hover {
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Test Cases Section -->
            <div class="test-cases">
                <h3>Test Cases</h3>
    """

    for idx, testcase in enumerate(testcases):
        html_content += f'<div class="test-case" onclick="showTestCase({idx})">{testcase["name"]}</div>'

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
            const testcases = {};
            
            function showTestCase(idx) {
                const testcase = testcases[idx];
                const stepsDiv = document.getElementById('test-steps-content');
                stepsDiv.innerHTML = `<h4>${testcase.name}</h4><ul>` + 
                    testcase.steps.map((step, index) => {
                        if (step.file) {
                            return `<li>${step.text} - <a href="#" onclick="showPopup('${step.file}')">View Table</a></li>`;
                        }
                        return `<li>${step.text}</li>`;
                    }).join("") + `</ul>`;
            }

            function showPopup(file) {
                const tableContentDiv = document.getElementById('table-content');
                fetch(file)
                    .then(response => response.text())
                    .then(csv => {
                        tableContentDiv.innerHTML = `<pre>${csv}</pre>`;
                        document.getElementById('overlay').style.display = 'block';
                        document.getElementById('table-popup').style.display = 'block';
                    });
            }

            function closePopup() {
                document.getElementById('overlay').style.display = 'none';
                document.getElementById('table-popup').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """.format(testcases)

    # Write HTML to file
    with open(output_file, "w") as file:
        file.write(html_content)

def create_testcases_data(folder_path: str) -> List[dict]:
    # Create test case data structure
    testcases = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            testcase_name = os.path.splitext(filename)[0]
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            steps = [{"text": f"Step {i+1}: Perform action {row['Action']}",
                      "file": file_path if row.get('HasTable', False) else None}
                     for i, row in df.iterrows()]
            testcases.append({"name": testcase_name, "steps": steps})
    return testcases

if __name__ == "__main__":
    folder_path = "path/to/intermittent_files"  # Update with your folder path
    testcases = create_testcases_data(folder_path)
    generate_html(testcases)
