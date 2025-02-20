import json

def highlight_json(json_data, indent=4):
    # Define newline and indentation
    newline = "\n"
    space = " " * indent  # 4 spaces for indentation

    def process_value(value, level):
        if isinstance(value, dict):
            return format_dict(value, level + 1)
        elif isinstance(value, list):
            return format_list(value, level + 1)
        else:
            return f'<span class="json-value">{json.dumps(value)}</span>'

    def format_dict(data, level):
        items = []
        for key, value in data.items():
            items.append(f'{space * level}<span class="json-key">"{key}"</span>: {process_value(value, level)}')
        return f'<span class="json-bracket-curl">{{</span>{newline}{f",{newline}".join(items)}{newline}{space * (level - 1)}<span class="json-bracket-curl">}}</span>'

    def format_list(data, level):
        items = [f'{space * level}{process_value(item, level)}' for item in data]
        return f'<span class="json-bracket-source">[</span>{newline}{f",{newline}".join(items)}{newline}{space * (level - 1)}<span class="json-bracket-source">]</span>'

    return process_value(json_data, level=0)