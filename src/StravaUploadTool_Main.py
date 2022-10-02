from authentication import *
from StravaUploadTool_Kernel import *
from fitfiletools_automation import *


# ----------------------------------------------------------------------------------------------------------------------
#
# Step by step:
# (1) Get authorization code from authorization page. This is a one-time, manual step.
#    Paste the below code in a browser, hit enter then grab the "code" part from the resulting url.
#
# https://www.strava.com/oauth/authorize?client_id=your_client_id&redirect_uri=http://localhost&response_type=code&scope=activity:read_all,activity:write
#
# (2) Make a POST request to Strava: exchange authorization code for access token & refresh token (This also only needs to be done once)
#
# https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&code=your_code_from_previous_step&grant_type=authorization_code
#
# (3) View your activities using the access token just received from (2)
#
# https://www.strava.com/api/v3/athlete/activities?access_token=access_token_from_previous_step
#
# (4) Use refresh token to get new access tokens
#
# https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&refresh_token=your_refresh_token_from_previous_step&grant_type=refresh_token
#
# ----------------------------------------------------------------------------------------------------------------------


def main():
    """
    Since access tokens expire after 5 hours and you don't want to have to do all the manual work (step 1&2) all over again.
    So, We first makes a call using the refresh token to retrieve the the most recent access token to ensure your program will always run!
    """
    print(r"""
   _____  _                             _    _         _                    _  _______             _ 
  / ____|| |                           | |  | |       | |                  | ||__   __|           | |
 | (___  | |_  _ __  __ _ __   __ __ _ | |  | | _ __  | |  ___    __ _   __| |   | |  ___    ___  | |
  \___ \ | __|| '__|/ _` |\ \ / // _` || |  | || '_ \ | | / _ \  / _` | / _` |   | | / _ \  / _ \ | |
  ____) || |_ | |  | (_| | \ V /| (_| || |__| || |_) || || (_) || (_| || (_| |   | || (_) || (_) || |
 |_____/  \__||_|   \__,_|  \_/  \__,_| \____/ | .__/ |_| \___/  \__,_| \__,_|   |_| \___/  \___/ |_|
                                               | |                                                   
                                               |_|                                                   
    """)
    preprocessing()
    fix_Fit_Activity_Files()
    TOKEN_FILE_PATH = Path('../credentials/tokens.txt')
    access_token = get_access_token(TOKEN_FILE_PATH)
    upload_Fit_Activity_Files(access_token)


if __name__ == "__main__":
    main()