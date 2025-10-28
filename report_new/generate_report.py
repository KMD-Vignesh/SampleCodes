import csv
import os
from datetime import datetime

def read_csv_data(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, filename)
    with open(csv_path, 'r') as file:
        return list(csv.DictReader(file))

def generate_html_report(csv_file, output_file):
    data = read_csv_data(csv_file)
    
    # Read CSS file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(script_dir, 'styles.css')
    with open(css_path, 'r') as f:
        css_content = f.read()
    
    # Calculate statistics
    total_tests = len(data)
    passed_tests = sum(1 for row in data if row['status'].lower() == 'pass')
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report</title>
    <link rel="icon" type="image/x-icon" href="https://login.zscloud.net/__zsig/f167WqMcrS45r">
    <style>{css_content}</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <img src="https://login.zscloud.net/__zsig/f167WqMcrS45r" alt="Logo" class="logo">
                <div class="header-center">
                    <h3>Test Execution Report</h3>
                </div>
                <div class="timestamp">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('summary')">Summary</div>
            <div class="tab" onclick="showTab('testcases')">Test Cases</div>
        </div>
        
        <div class="content">
            <div id="summary" class="tab-content">
                <div class="summary-grid">
                    <div class="stat-card">
                        <div class="stat-number">{total_tests}</div>
                        <div>Total Tests</div>
                    </div>
                    <div class="stat-card pass">
                        <div class="stat-number">{passed_tests}</div>
                        <div>Passed</div>
                    </div>
                    <div class="stat-card fail">
                        <div class="stat-number">{failed_tests}</div>
                        <div>Failed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{pass_rate:.1f}%</div>
                        <div>Pass Rate</div>
                    </div>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Author</th>
                                <th>Total Tests</th>
                                <th>Passed</th>
                                <th>Failed</th>
                                <th>Pass Rate</th>
                            </tr>
                        </thead>
                        <tbody>"""
    
    # Calculate author statistics
    authors = list(set(row['author'] for row in data))
    for author in authors:
        author_tests = [row for row in data if row['author'] == author]
        author_passed = sum(1 for row in author_tests if row['status'].lower() == 'pass')
        author_total = len(author_tests)
        author_failed = author_total - author_passed
        author_pass_rate = (author_passed / author_total * 100) if author_total > 0 else 0
        
        html_content += f"""
                            <tr>
                                <td>{author}</td>
                                <td>{author_total}</td>
                                <td class="status-pass">{author_passed}</td>
                                <td class="status-fail">{author_failed}</td>
                                <td>{author_pass_rate:.1f}%</td>
                            </tr>"""
    
    html_content += """
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div id="testcases" class="tab-content hidden">
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Test ID</th>
                                <th>Test Name</th>
                                <th>Description</th>
                                <th>Author</th>
                                <th>Status</th>
                                <th>Validation</th>
                            </tr>
                        </thead>
                        <tbody>"""
    
    for row in data:
        status_class = 'status-pass' if row['status'].lower() == 'pass' else 'status-fail'
        html_content += f"""
                            <tr>
                                <td>{row['testcase_id']}</td>
                                <td>{row['testcase_name']}</td>
                                <td>{row['description']}</td>
                                <td>{row['author']}</td>
                                <td class="{status_class}">{row['status'].upper()}</td>
                                <td>{row['validation_parameter']}</td>
                            </tr>"""
    
    html_content += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.getElementById(tabName).classList.remove('hidden');
            document.querySelector('[onclick="showTab(\\''+tabName+'\\')"]').classList.add('active');
        }

        document.addEventListener('DOMContentLoaded', function() {
            showTab('summary');
        });
    </script>
</body>
</html>"""
    
    output_path = os.path.join(script_dir, output_file)
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    generate_html_report('testdata.csv', 'test_report.html')
