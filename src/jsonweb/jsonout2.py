import json

# Sample JSON data (you can load this from a file using json.load())
json_data = {
    "name": "John",
    "age": 30,
    "is_student": False,
    "address": {
        "street": "123 Main St",
        "city": "Anytown"
    },
    "scores": [95, 82, 88]
}

# Function to convert JSON to HTML with coloring
def json_to_html(data, indent=0):
    html = ""
    if isinstance(data, dict):
        html += "<div style='margin-left: {}px; color: blue;'>{{</div>".format(indent)
        for key, value in data.items():
            html += "<div style='margin-left: {}px;'>".format(indent + 20)
            html += "<span style='color: red;'>\"{}\"</span>: ".format(key)
            html += json_to_html(value, indent + 20)
            html += "</div>"
        html += "<div style='margin-left: {}px; color: blue;'>}}</div>".format(indent)
    elif isinstance(data, list):
        html += "<div style='margin-left: {}px; color: green;'>[</div>".format(indent)
        for item in data:
            html += "<div style='margin-left: {}px;'>".format(indent + 20)
            html += json_to_html(item, indent + 20)
            html += "</div>"
        html += "<div style='margin-left: {}px; color: green;'>]</div>".format(indent)
    elif isinstance(data, str):
        html += "<span style='color: purple;'>\"{}\"</span>".format(data)
    elif isinstance(data, (int, float)):
        html += "<span style='color: orange;'>{}</span>".format(data)
    elif isinstance(data, bool):
        html += "<span style='color: teal;'>{}</span>".format(str(data).lower())
    elif data is None:
        html += "<span style='color: gray;'>null</span>"
    return html

# Generate HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON to HTML</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        div {
            margin-left: 20px;
        }
    </style>
</head>
<body>
    <h1>JSON Data</h1>
    {}
</body>
</html>
""".format(json_to_html(json_data))

# Save the HTML content to a file
with open("output.html", "w") as file:
    file.write(html_content)

print("HTML file generated successfully!")