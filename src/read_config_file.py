import os
from dotenv import load_dotenv


load_dotenv("../.env")  # take environment variables from .env


try:
    STRAVA_CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
except KeyError:
    print("[ERROR]: Please add STRAVA_CLIENT_ID to the list of environment variables!")

try:
    STRAVA_CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
except KeyError:
    print("[ERROR]: Please add STRAVA_CLIENT_SECRET to the list of environment variables")

try:
    GMAIL_USER_ID = os.environ["GMAIL_USER_ID"]
except KeyError:
    print("[ERROR]: Please add GMAIL_USER_ID to the list of environment variables")

try:
    GMAIL_PASSWORD = os.environ["GMAIL_PASSWORD"]
except KeyError:
	print("[ERROR]: Please add GMAIL_PASSWORD to the list of environment variables")

try:
    LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
except KeyError:
    print("[ERROR]: Please add LINE_CHANNEL_ACCESS_TOKEN to the list of environment variables")

try:
    LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
except KeyError:
    print("[ERROR]: Please add LINE_CHANNEL_SECRET to the list of environment variables")

try:
    ZWIFT_ACTIVITY_DIR = os.environ["ZWIFT_ACTIVITY_DIR"]
except KeyError:
    print("[ERROR]: Please add ZWIFT_ACTIVITY_DIR to the list of environment variables")