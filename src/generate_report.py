import json
from typing import Literal
from read_intmi import get_int_files
from template import get_template


def generate_report(test_cases, test_steps_data, test_status_count, output_file):
    test_cases_html: Literal[""] = ""
    for name, status in test_cases:
        test_cases_html += f'<div class="test-case {status}" onclick="showTestSteps(\'{name}\', this)">{name}<span>{status.capitalize()}</span></div>\n'

    filled_html: str = get_template().format(
        test_cases=test_cases_html,
        test_steps_data=json.dumps(obj=test_steps_data),
        test_status_count=json.dumps(obj=test_status_count),
    )

    with open(file=output_file, mode="w") as f:
        f.write(filled_html)
    print(f"Report Generated - {output_file}")


# Example usage
if __name__ == "__main__":
    test_int_data: dict = get_int_files(base_dir="data")
    test_cases: list[tuple[str, str]] = [
        ("TC001", "pass"),
        ("TC002", "fail"),
        ("TC003", "skip"),
    ]

  

    test_steps_data: dict[str, list[str]] = {
        "TC001": [
            "Step 1: Do this",
            "Step 2: <a href='#' onclick=\"openPopup('table1.csv')\">View Table</a>",
        ],
        "TC002": [
            "Step 1: Start Process",
            "Step 2: <a href='#' onclick=\"openPopup('table2.csv')\">View Table</a>",
        ],
        "TC003": ["Step 1: Check prerequisites", "Step 2: Skipped due to dependencies"],
    }

    test_status_count: dict[str, int] = {
        "pass": 1,
        "fail": 1,
        "skip": 1,
    }

    generate_report(
        test_cases=test_cases,
        test_steps_data=test_steps_data,
        test_status_count=test_status_count,
        output_file="html/report.html",
    )
