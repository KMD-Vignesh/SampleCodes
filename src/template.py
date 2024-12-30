def get_template() -> str:
    template_content: str = (
        """<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <title>Test Report</title>
        """
        + get_styles()
        + """
      </head>
      <body>"""
        + get_menu_bar()
        + get_test_case_section()
        + get_summary_popup()
        + get_script_content()
        + """</body>
    </html>
    """
    )
    return template_content


def get_test_case_section() -> str:
    try:
        with open(file="src/web/testcase.html", mode="r") as file:
            html_content: str = file.read()
            return f"""{html_content}"""
    except FileNotFoundError:
        return "/* get_test_case_section html not found */"


def get_summary_popup() -> str:
    try:
        with open(file="src/web/summary_popup.html", mode="r") as file:
            html_content: str = file.read()
            return f"""{html_content}"""
    except FileNotFoundError:
        return "/* get_summary_section html not found */"


def get_menu_bar() -> str:
    try:
        with open(file="src/web/menubar.html", mode="r") as file:
            html_content: str = file.read()
            return f"""{html_content}"""
    except FileNotFoundError:
        return "/* get_menu_bar html not found */"


def get_script_content() -> str:
    try:
        with open(file="src/web/script.js", mode="r", encoding="utf-8") as file:
            data: str = """
            const testStepsData = {test_steps_data};
            const testStatusCount = {test_status_count};
            """
            js_script: str = data + file.read().replace("{", "{{").replace("}", "}}")
            return f"""<script>{js_script}</script>"""
    except FileNotFoundError:
        return "<script>/* Script file not found */</script>"


def get_styles() -> str:
    try:
        with open(file="src/web/style.css", mode="r") as file:
            css_content: str = file.read().replace("{", "{{").replace("}", "}}")
            return f"""<style>{css_content}</style>"""
    except FileNotFoundError:
        return "<style>/* Stylesheet not found */</style>"
