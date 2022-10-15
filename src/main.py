from authentication import *
from fitfiletools_automation import *
from strava_upload import *
from strava_analysis import *


# ----------------------------------------------------------------------------------------------------------------------
#
# Step by step:
# (1) Get authorization code from authorization page. This is a one-time, manual step.
#     Paste the below code in a browser, hit "Enter" then grab the "code" part from the resulting url.
#
# https://www.strava.com/oauth/authorize?client_id=your_client_id&redirect_uri=http://localhost&response_type=code&scope=activity:read_all,activity:write
#
# (2) Make a POST request to Strava: exchange authorization code for access token & refresh token (This also only needs to be done once).
#
# https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&code=your_code_from_previous_step&grant_type=authorization_code
#
# (3) View your activities using the access token just received from (2).
#
# https://www.strava.com/api/v3/athlete/activities?access_token=access_token_from_previous_step
#
# (4) Use refresh token to get new access tokens.
#
# https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&refresh_token=your_refresh_token_from_previous_step&grant_type=refresh_token
#
# ----------------------------------------------------------------------------------------------------------------------


def main():
    print_StravaUploadTool()
    preprocessing()
    fix_Fit_Activity_Files()
    upload_Fit_Activity_Files(get_Access_Token())


if __name__ == "__main__":
    main()