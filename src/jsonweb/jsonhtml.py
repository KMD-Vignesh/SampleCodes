import json

# Path to the JSON file
JSON_FILE_PATH = 'data.json'

# Path to the output HTML file
HTML_FILE_PATH = 'display_json.html'

# Read the JSON file
with open(JSON_FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

# Convert JSON data to a formatted string
formatted_json = json.dumps(data, indent=4)

# HTML template
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
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 16px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="json-container">
        <h1>JSON Content</h1>
        <pre>{formatted_json}</pre>
    </div>
</body>
</html>
"""

# Write the HTML content to a file
with open(HTML_FILE_PATH, 'w') as html_file:
    html_file.write(html_content)

print(f"HTML file generated successfully: {HTML_FILE_PATH}")