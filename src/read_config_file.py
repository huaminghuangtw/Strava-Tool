import requests, urllib3, yaml, os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


dir = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.abspath( os.path.join(dir, '..', 'configfile', 'user_config.yml') )
with open(CONFIG_FILE_PATH, 'r') as f:
    config = yaml.safe_load(f)


CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
REFRESH_TOKEN = config["REFRESH_TOKEN"]
ZWIFT_ACTIVITY_DIR = config["ZWIFT_ACTIVITY_DIR"]
GMAIL_USER_ID = config["GMAIL_USER_ID"]
GMAIL_PASSWORD = config["GMAIL_PASSWORD"]