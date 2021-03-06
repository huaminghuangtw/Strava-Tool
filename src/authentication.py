from read_config_file import *


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