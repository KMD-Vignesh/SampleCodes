from flask import Flask, render_template_string
import json

app = Flask(__name__)

def highlight_json(json_data):
    json_string = json.dumps(json_data, indent=4)
    highlighted_json = json_string.replace('"', '<span class="json-string">"</span>')
    highlighted_json = highlighted_json.replace(':', '<span class="json-colon">:</span>')
    highlighted_json = highlighted_json.replace('{', '<span class="json-bracket">{</span>')
    highlighted_json = highlighted_json.replace('}', '<span class="json-bracket">}</span>')
    highlighted_json = highlighted_json.replace('[', '<span class="json-bracket">[</span>')
    highlighted_json = highlighted_json.replace(']', '<span class="json-bracket">]</span>')
    highlighted_json = highlighted_json.replace('true', '<span class="json-boolean">true</span>')
    highlighted_json = highlighted_json.replace('false', '<span class="json-boolean">false</span>')
    highlighted_json = highlighted_json.replace('null', '<span class="json-null">null</span>')
    return highlighted_json

@app.route('/')
def index():
    json_data = {
        "name": "John Doe",
        "age": 30,
        "isStudent": False,
        "address": {
            "city": "New York",
            "zip": "10001"
        }
    }
    formatted_json = highlight_json(json_data)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>JSON Highlighting</title>
            <style>
                .json-string { color: green; }
                .json-number { color: blue; }
                .json-boolean { color: purple; }
                .json-null { color: gray; }
                .json-bracket { color: black; }
                .json-colon { color: black; }
            </style>
        </head>
        <body>
            <pre>{{ formatted_json | safe }}</pre>
        </body>
        </html>
    ''', formatted_json=formatted_json)

if __name__ == '__main__':
    app.run(debug=True)
