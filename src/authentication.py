import requests, urllib3, yaml, os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


dir = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.abspath( os.path.join(dir, '..', 'configfile', 'user_config.yml') )
with open(CONFIG_FILE_PATH, 'r') as f:
    config = yaml.safe_load(f)

            
CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
REFRESH_TOKEN = config["REFRESH_TOKEN"]


def get_New_Access_Tokens():
    print()
    print("Requesting new Access Token...\n")

    try:
        auth_url = "https://www.strava.com/oauth/token"
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': "refresh_token",
            'f': 'json'
        }
        res = requests.post(auth_url, data=payload, verify=False)
    except requests.RequestException:
        return None

    try:
        access_token = res.json()['access_token']
        refresh_token = res.json()['refresh_token']
    except (KeyError, TypeError, ValueError):
        return None

    #print("Access Token = {}".format(access_token))
    #print("Refresh Token = {}\n".format(refresh_token))

    return access_token