import os
import json

_settings_file_timestamp = 0
SETTINGS_FILE_NAME = './../settings.json'

async def new_settings():
    current_time_stamp = os.path.getmtime(SETTINGS_FILE_NAME)
    return current_time_stamp > _settings_file_timestamp

async def load_settings():
    global _settings_file_timestamp
    print("loading settings")
    settings_file = open(SETTINGS_FILE_NAME, 'r')
    # store the file's current modification timestamp in order
    # to detect if updated and new settings are available
    _settings_file_timestamp = os.path.getmtime(SETTINGS_FILE_NAME)
    return json.load(settings_file)

