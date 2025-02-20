import json

def highlight_json(json_data):
    def process_value(value):
        if isinstance(value, dict):
            return format_dict(value)
        elif isinstance(value, list):
            return format_list(value)
        else:
            return f'<span class="json-value">{json.dumps(value)}</span>'

    def format_dict(data):
        items = []
        for key, value in data.items():
            items.append(f'<span class="json-key">"{key}"</span>: {process_value(value)}')
        return f'<span class="json-bracket-curl">{{</span>{", ".join(items)}<span class="json-bracket-curl">}}</span>'

    def format_list(data):
        items = [process_value(item) for item in data]
        return f'<span class="json-bracket-source">[</span>{", ".join(items)}<span class="json-bracket-source">]</span>'

    return process_value(json_data)