import pandas as pd
from pathlib import Path

def generate_html_with_dfs(csv_folder: str, output_file: str) -> None:
    """
    Generate a single HTML file with multiple DataFrames displayed dynamically based on button clicks.

    :param csv_folder: Folder containing the CSV files.
    :param output_file: Path to the output HTML file.
    """
    # Get all CSV files in the folder
    csv_files = list(Path(csv_folder).glob("*.csv"))
    if not csv_files:
        print("No CSV files found in the folder.")
        return

    # Create a dictionary to store DataFrame HTML by filename
    df_html_tables = {}
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df_html_tables[csv_file.stem] = df.to_html(index=False, border=1)

    # Generate HTML content
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>CSV DataFrames Viewer</title>
    <style>
        .button-container {
            margin-bottom: 20px;
        }
        .button-container button {
            margin-right: 10px;
            padding: 10px;
            font-size: 16px;
        }
        #table-container {
            margin-top: 20px;
        }
    </style>
    <script>
        // Store HTML tables as a JavaScript object
        const dfTables = """ + str(df_html_tables) + """;

        function showTable(filename) {
            document.getElementById('table-container').innerHTML = dfTables[filename];
        }
    </script>
</head>
<body>
    <div class="button-container">
"""

    # Add buttons for each CSV file
    for filename in df_html_tables.keys():
        html_content += f'<button onclick="showTable(\'{filename}\')">{filename}</button>\n'

    # Add table container
    html_content += """
    </div>
    <div id="table-container">
        <p>Select a dataset to view the table.</p>
    </div>
</body>
</html>
"""

    # Write the HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file generated: {output_file}")

# Example usage
csv_folder = "data"
output_file = "html/df-html.html"
generate_html_with_dfs(csv_folder, output_file)
