from authentication import *
from StravaAnalysisTool_Kernel import *


# ----------------------------------------------------------------------------------------------------------------------
#
# Step by step:
# 1) Get authorization code from authorization page. This is a one-time, manual step.
#    Paste the below code in a browser, hit enter then grab the "code" part from the resulting url.
#
# https://www.strava.com/oauth/authorize?client_id=your_client_id&redirect_uri=http://localhost&response_type=code&scope=activity:read_all,activity:write
#
# 2) Make a POST request to Strava: exchange authorization code for access token & refresh token (This also only needs to be done once)
#
# https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&code=your_code_from_previous_step&grant_type=authorization_code
#
# 3) View your activities using the access token just received from 2)
#
# https://www.strava.com/api/v3/athlete/activities?access_token=access_token_from_previous_step
#
# 3) Use refresh token to get new access tokens (i.e., getNewAccessTokens())
#
# https://www.strava.com/oauth/token?client_id=your_client_id&client_secret=your_client_secret&refresh_token=your_refresh_token_from_previous_step&grant_type=refresh_token
#
# ----------------------------------------------------------------------------------------------------------------------


def main():
    """
    Since access tokens expire after 5 hours and you don’t want to have to do all the manual work (step 1&2) all over again.
    So, We first makes a call using the refresh token to retrieve the the most recent access token to ensure your program will always run!
    """
    print(r"""
         _______..___________..______           ___   ____    ____  ___           ___      .__   __.      ___       __      ____    ____  _______. __       _______..___________.  ______     ______    __      
        /       ||           ||   _  \         /   \  \   \  /   / /   \         /   \     |  \ |  |     /   \     |  |     \   \  /   / /       ||  |     /       ||           | /  __  \   /  __  \  |  |     
       |   (----``---|  |----`|  |_)  |       /  ^  \  \   \/   / /  ^  \       /  ^  \    |   \|  |    /  ^  \    |  |      \   \/   / |   (----`|  |    |   (----``---|  |----`|  |  |  | |  |  |  | |  |     
        \   \        |  |     |      /       /  /_\  \  \      / /  /_\  \     /  /_\  \   |  . `  |   /  /_\  \   |  |       \_    _/   \   \    |  |     \   \        |  |     |  |  |  | |  |  |  | |  |     
    .----)   |       |  |     |  |\  \----. /  _____  \  \    / /  _____  \   /  _____  \  |  |\   |  /  _____  \  |  `----.    |  | .----)   |   |  | .----)   |       |  |     |  `--'  | |  `--'  | |  `----.
    |_______/        |__|     | _| `._____|/__/     \__\  \__/ /__/     \__\ /__/     \__\ |__| \__| /__/     \__\ |_______|    |__| |_______/    |__| |_______/        |__|      \______/   \______/  |_______|

	""")

    new_access_token = get_New_Access_Tokens()

    ## Getting activity data from Strava
    my_dataset = get_Latest_Activity_Data(new_access_token, 1)
    #my_dataset = get_All_Activity_Data(new_access_token)
    #my_dataset = get_Timeinterval_Activity_Data(new_access_token, "1546300799", "1514764800")

	
    print( json.dumps(my_dataset, indent=4, sort_keys=True) ) # pretty printing a json file
	

    # ============================================
    # Data Manipulation & Analysis & Visualization
    # ============================================
    #activities = pd.json_normalize(my_dataset) # pandas.json_normalize: normalizes semi-structured JSON data into a flat "table".
    # print(activities.columns) # list of all column names in the table
    # print(activities.shape) # dimensions of the table


    #activities = create_Activity_DataFrame(activities)
    #print(activities.head(5))


    # activities.to_csv('myfile.csv')


    # for id in activities['id']:
    #     if id == 4912393140:
    #         print( activities[activities['id'] == id][['type', 'external_id', 'start_date_local']] )
    #         activities[activities['id'] == id].to_csv('myfile.csv')
    #         break
    #     if id == activities['id'].iloc[-1]:
    #         print( "This activity doesn't exist!" )
    # print("\n")


    # Break start date into start time and date
    #activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
    #activities['start_time'] = activities['start_date_local'].dt.time
    #activities['start_date'] = activities['start_date_local'].dt.date
    #print(activities.head(5))


    #print( activities['type'].value_counts() )


    # rides = activities.loc[activities['type'] == 'Ride']
    # virtualrides = activities.loc[activities['type'] == 'VirtualRide']
    # hike = activities.loc[activities['type'] == 'Hike']
    # run = activities.loc[activities['type'] == 'Run']


    #plot_colour_palette = ["#2C3E50", "#E74C3C", "#ECF0F1", "#3498DB", "#2980B9",
    #                       "#195962", "#F56F6C", "#FFFFFF", "#252932", "#191C21"]
    #display_Activity_Count_Plot(activities, plot_colour_palette)


    #display_Summary_Statistics(activities)


if __name__ == "__main__":
    main()