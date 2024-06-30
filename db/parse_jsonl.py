import json

def json_to_jsonl(json_file, jsonl_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for entry in data:
            json_line = json.dumps(entry)
            f.write(json_line + '\n')

# Example usage
json_file = 'tuning.json'
jsonl_file = 'finetuning.jsonl'
json_to_jsonl(json_file, jsonl_file)
