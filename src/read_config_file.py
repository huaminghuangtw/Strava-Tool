import yaml
import sys
from pathlib import Path


CONFIG_FILE_PATH = Path('../credentials/config.yaml')
with CONFIG_FILE_PATH.open(mode='r') as file:
    config = yaml.safe_load(file)


try:
    STRAVA_CLIENT_ID = config["STRAVA_CLIENT_ID"]
except KeyError:
    sys.exit("[ERROR]: Please add STRAVA_CLIENT_ID to '{}'".format(CONFIG_FILE_PATH))

try:
    STRAVA_CLIENT_SECRET = config["STRAVA_CLIENT_SECRET"]
except KeyError:
    sys.exit("[ERROR]: Please add STRAVA_CLIENT_SECRET to '{}'".format(CONFIG_FILE_PATH))
    
try:
    ZWIFT_ACTIVITY_DIR = config["ZWIFT_ACTIVITY_DIR"]
except KeyError:
    sys.exit("[ERROR]: Please add ZWIFT_ACTIVITY_DIR to '{}'".format(CONFIG_FILE_PATH))

try:
    GMAIL_USER_ID = config["GMAIL_USER_ID"]
except KeyError:
    sys.exit("[ERROR]: Please add GMAIL_USER_ID to '{}'".format(CONFIG_FILE_PATH))

try:
    GMAIL_PASSWORD = config["GMAIL_PASSWORD"]
except KeyError:
    sys.exit("[ERROR]: Please add GMAIL_PASSWORD to '{}'".format(CONFIG_FILE_PATH))

try:
    LINE_CHANNEL_ACCESS_TOKEN = config["LINE_CHANNEL_ACCESS_TOKEN"]
except KeyError:
    sys.exit("[ERROR]: Please add LINE_CHANNEL_ACCESS_TOKEN to '{}'".format(CONFIG_FILE_PATH))

try:
    LINE_CHANNEL_SECRET = config["LINE_CHANNEL_SECRET"]
except KeyError:
    sys.exit("[ERROR]: Please add LINE_CHANNEL_SECRET to '{}'".format(CONFIG_FILE_PATH))