import os
import json

def load_config():
    config_path = os.getenv('CONFIG_PATH', 'config.json')
    with open(config_path) as f:
        return json.load(f)
    

    