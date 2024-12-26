import json
from typing import Literal
from read_intmi import get_int_data
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
    test_cases: list[tuple[str, str]] = [
        ("TC001", "pass"),
        ("TC002", "fail"),
        ("TC003", "skip"),
        ("TC004", "pass"),
        ("TC005", "pass"),
        ("TC006", "skip"),
        ("TC007", "pass"),
        ("TC008", "fail"),
        ("TC009", "pass"),

    ]

  
    test_steps_data: dict[str, list[str]] = get_int_data(base_dir="data")

    test_status_count: dict[str, int] = {}
    for _, status in test_cases:
        test_status_count[status] = test_status_count.get(status, 0) + 1

    generate_report(
        test_cases=test_cases,
        test_steps_data=test_steps_data,
        test_status_count=test_status_count,
        output_file="html/report.html",
    )
