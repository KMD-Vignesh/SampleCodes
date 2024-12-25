import json
from template import get_template

def generate_report(test_cases, test_steps_data, test_status_count, output_file):
    test_cases_html = ""
    for name, status in test_cases:
        test_cases_html += f'<div class="test-case {status}" onclick="showTestSteps(\'{name}\', this)">{name}<span>{status.capitalize()}</span></div>\n'

    filled_html = get_template().format(
        test_cases=test_cases_html,
        test_steps_data=json.dumps(test_steps_data),
        test_status_count=json.dumps(test_status_count),
    )

    with open(output_file, "w") as f:
        f.write(filled_html)
    print(f"Report Generated - {output_file}")

# Example usage
if __name__ == "__main__":
    test_cases = [
        ("Test Case 1", "pass"),
        ("Test Case 2", "fail"),
        ("Test Case 3", "skip"),
    ]

    test_steps_data = {
        "Test Case 1": ["Step 1: Do this", "Step 2: <a href='#' onclick=\"openPopup('table1.csv')\">View Table</a>"],
        "Test Case 2": ["Step 1: Start Process", "Step 2: <a href='#' onclick=\"openPopup('table2.csv')\">View Table</a>"],
        "Test Case 3": ["Step 1: Check prerequisites", "Step 2: Skipped due to dependencies"],
    }

    test_status_count = {
        "pass": 1,
        "fail": 1,
        "skip": 1,
    }

    generate_report(test_cases, test_steps_data, test_status_count, "html/report.html")
