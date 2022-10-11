"""
Authenticates access to the Strava V3 API using OAuth2
"""

import pathlib
import time
import webbrowser
import requests
from stravalib import Client
from read_config_file import *


client = Client()


def get_Access_Token(file_path: pathlib.Path = pathlib.Path('../tokens.txt')) -> str:
    """
    Obtain and return an OAuth2 access token for the Strava V3 API
    @params:
        file_path - The path of the file to store the tokens to
    @return:
        The access token as a string if access to the API is successfully authenticated
        None if an access token cannot be generated
    """
    client_info = {}

    client_info['id'] = STRAVA_CLIENT_ID
    client_info['secret'] = STRAVA_CLIENT_SECRET

    # Read the authentication tokens and expiry time from the file
    tokens = _read_tokens_from_file(file_path)
    if tokens:
        # Refresh the tokens if the access token has expired and write them to the file
        if (int(tokens['expires_at']) <= time.time()):
            tokens = _refresh_expired_tokens(client_info, tokens)
            _write_tokens_to_file(file_path, tokens)
    else:
        # Get the initial authentication tokens and write them to the file
        tokens = _get_initial_tokens(client_info)
        _write_tokens_to_file(file_path, tokens)

    print('[Strava]: Access to the API authenticated!')
    access_token = str(tokens['access_token'])

    return access_token


# ----------------
# Helper functions
# ----------------
def _read_tokens_from_file(file_path: pathlib.Path) -> dict:
    """
    Read the authentication tokens and expiry time from a text file
    and return them as a dictionary
    @params:
        file_path - The path of the file to read the tokens from
    @return:
        A dictionary containing the authentication tokens and expiry time
        An empty dictionary if the file cannot be read from successfully
    """
    print("[Strava]: Reading authentication tokens from '{}'".format(file_path))

    tokens = {}

    try:
        with file_path.open(mode='r') as file:
            for line in file:
                if line.startswith('STRAVA_ACCESS_TOKEN ='):
                    tokens['access_token'] = line.split('=')[1].strip()
                elif line.startswith('STRAVA_REFRESH_TOKEN ='):
                    tokens['refresh_token'] = line.split('=')[1].strip()
                elif line.startswith('STRAVA_TOKEN_EXPIRY_TIME ='):
                    tokens['expires_at'] = line.split('=')[1].strip()
                else:
                    pass
    except IOError:
        print('[Strava]: No authentication tokens found :(')

    return tokens


def _write_tokens_to_file(file_path: pathlib.Path, tokens: dict):
    """
    Write the authentication tokens and expiry time to a text file
    @params:
        file_path - The path of the file to write the tokens to
        tokens - A dictionary containing the authentication tokens and expiry time to write to the file
    """
    print("[Strava]: Writing authentication tokens to '{}'".format(file_path))
    
    # Delete the tokens file to remove any expired tokens
    try:
        file_path.unlink()
    except OSError:
        pass

    # Write the authentication tokens and expiry time to a new text file
    with file_path.open(mode='w') as file:
        file.write('STRAVA_ACCESS_TOKEN = {}\n'.format(tokens['access_token']))
        file.write('STRAVA_REFRESH_TOKEN = {}\n'.format(tokens['refresh_token']))
        file.write('STRAVA_TOKEN_EXPIRY_TIME = {}\n'.format(tokens['expires_at']))


def _refresh_expired_tokens(client_info: dict, expired_tokens: dict) -> dict:
    """
    Refresh the authentication tokens and return them as a dictionary
    @params:
        client_info - A dictionary containing the client ID and client secret
        expired_tokens - A dictionary containing the expired authentication tokens and expiry time
    @return:
        A dictionary containing the new authentication tokens and expiry time
    """
    print('[Strava]: Refreshing expired authentication tokens...')

    new_tokens = client.refresh_access_token(
					client_id=client_info['id'],
					client_secret=client_info['secret'],
					refresh_token=expired_tokens['refresh_token']
				)

    return new_tokens


def _get_auth_code(client_info: dict) -> str:
    """
    Get and return the authorization code required to obtain the initial authentication tokens
    @params:
        client_info - A dictionary containing the client ID and client secret
    @return:
        The authorization code as a string
    """
    try:
        authorization_url = client.authorization_url(
								client_id=client_info['id'],
								redirect_uri='http://127.0.0.1:5000/authorization',
								scope=[
									'read',
									'read_all',
									'profile:read_all',
									'profile:write',
									'activity:read',
									'activity:read_all',
									'activity:write'
								]
							)
        # Prepare the authorization code GET request and open it in a web browser window
        r = requests.Request('GET', authorization_url).prepare()
        webbrowser.open(r.url)
    except requests.exceptions.RequestException:
        return None

    # Copy and paste the authorization code (&code="code_to_be_copied"&)
    # from the URL response in the web browser window
    auth_code = str(input("Enter authorization code: "))

    return auth_code


def _exchange_tokens(client_info: dict, auth_code: str) -> dict:
    """
    Exchange the authorization code against the initial authentication tokens
    @params:
        client_info - A dictionary containing the client ID and client secret
        auth_code - The authorization code as a string
    @return:
        A dictionary containing the initial authentication tokens and expiry time
    """
    init_tokens = client.exchange_code_for_token(
					client_id=client_info['id'],
					client_secret=client_info['secret'],
					code=auth_code
				)

    return init_tokens


def _get_initial_tokens(client_info: dict) -> dict:
    """
    Get and return the initial authentication tokens
    @params:
        client_info - A dictionary containing the client ID and client secret
    @return:
        A dictionary containing the initial authentication tokens and expiry time
    """
    print('[Strava]: Getting initial authentication tokens...')

    # Get the authorization code and exchange it against the initial authentication tokens
    auth_code = _get_auth_code(client_info)
    init_tokens = _exchange_tokens(client_info, auth_code)

    return init_tokens