import json

# Path to the JSON file
JSON_FILE_PATH = 'data.json'

# Path to the output HTML file
HTML_FILE_PATH = 'display_json.html'

# Read the JSON file
with open(JSON_FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

# Convert JSON data to a string
json_string = json.dumps(data, indent=4)

# HTML template with JavaScript and CSS for syntax highlighting
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beautiful JSON Display</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        .json-container {{
            background-color: #282c34;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            color: #abb2bf;
            font-family: monospace;
            font-size: 16px;
            line-height: 1.5;
        }}
        .json-key {{
            color: #61afef;
        }}
        .json-value {{
            color: #98c379;
        }}
        .json-bracket {{
            color: #e06c75;
        }}
        .json-number {{
            color: #d19a66;
        }}
        .json-string {{
            color: #98c379;
        }}
        .json-boolean {{
            color: #d19a66;
        }}
        .json-null {{
            color: #d19a66;
        }}
    </style>
</head>
<body>
    <div class="json-container">
        <h1 style="color: #fff;">JSON Content</h1>
        <pre id="json-content"></pre>
    </div>

    <script>
        // JSON data
        const jsonData = {json_string};

        // Function to highlight JSON syntax
        function highlightJson(json) {{
            const jsonString = JSON.stringify(json, null, 4);
            return jsonString
                .replace(/("(\\u[a-zA-Z0-9]{{4}}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(\.\d*)?([eE][+-]?\d+)?)/g, (match) => {{
                    let cls = 'json-value';
                    if (/^"/.test(match)) {{
                        if (/:$/.test(match)) {{
                            cls = 'json-key';
                        }} else {{
                            cls = 'json-string';
                        }}
                    }} else if (/true|false/.test(match)) {{
                        cls = 'json-boolean';
                    }} else if (/null/.test(match)) {{
                        cls = 'json-null';
                    }} else if (/^-?\d+(\.\d*)?([eE][+-]?\d+)?$/.test(match)) {{
                        cls = 'json-number';
                    }}
                    return `<span class="${{cls}}">${{match}}</span>`;
                }})
                .replace(/\{|\}|\[|\]/g, (match) => `<span class="json-bracket">${{match}}</span>`);
        }}

        // Display highlighted JSON
        document.getElementById('json-content').innerHTML = highlightJson(jsonData);
    </script>
</body>
</html>
"""

# Write the HTML content to a file
with open(HTML_FILE_PATH, 'w') as html_file:
    html_file.write(html_content)

print(f"HTML file generated successfully: {HTML_FILE_PATH}")