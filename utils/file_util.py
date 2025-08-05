# utils/file_util.py
def read_json_file(file_path):
    import json
    with open(file_path, "r") as f:
        return json.load(f)