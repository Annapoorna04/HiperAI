import json

def load_jd_inputs():
    with open("data/jd_inputs.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
