import json

def load_settings():
    settings_file = open('./settings.json', 'r')
    return json.load(settings_file)

