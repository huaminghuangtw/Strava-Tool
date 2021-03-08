from client_configuration_file import *
import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_New_Access_Tokens():
    """
    Since access tokens expire after 5 hours and you don’t want to have to do all the manual work (step 1&2) all over again.
    So, We first makes a call using the refresh token to retrieve the the most recent access token to ensure your program will always run!
    """
    auth_url = "https://www.strava.com/oauth/token"

    payload = {
        'client_id': client_ID,
        'client_secret': client_secret,
        'refresh_token': "92100886064939bc80039961f98833b8456f16c1",
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting new Access Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)

    access_token = res.json()['access_token']
    refresh_token = res.json()['refresh_token']

    print("Access Token = {}".format(access_token))
    print("Refresh Token = {}\n".format(refresh_token))

    return access_token