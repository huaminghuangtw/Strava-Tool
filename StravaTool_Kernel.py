import os, glob, requests, shutil, time, json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd # Pandas will be the backbone of our data manipulation.
from pandas.io.json import json_normalize
import seaborn as sns # Seaborn is a data visualization library.
import matplotlib as mpl # Matplotlib is a data visualization library.
import matplotlib.pyplot as plt
import numpy as np # Numpy will help us handle some work with arrays.
from datetime import datetime # Datetime will allow Python to recognize dates as dates, not strings.



# client_ID = 'Your_client_ID'
# client_secret = 'Your_client_secret'



# -------------------------------
# data analysis related functions
# -------------------------------
def get_New_Access_Tokens():
    """
    Since access tokens expire after 6 mins and you don’t want to have to do all the manual work (step 1&2) all over again.
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


def get_Latest_Activity_Data(access_token: str, numberOfActivities: str) -> list:
    """
    Arguments:
        numberOfActivities: number of the latest activities you want to retrieve from your Strava feed.
    """
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': numberOfActivities, 'page': 1}

    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    return my_dataset


def get_Timeinterval_Activity_Data(access_token: str, before: str, after: str) -> list:
    """
    Arguments:
        before, after - should be in UNIX time format
    """
    page_id = 1
    per_page = 50

    my_dataset = []

    while True:
        # get page of activities from Strava
        activites_url = "https://www.strava.com/api/v3/athlete/activities"
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'before': before, 'after': after, 'per_page': per_page, 'page': page_id}

        dataset = requests.get(activites_url, headers=header, params=param).json()

        # if no results then exit loop
        if (not dataset):
            break

        # increment page
        page_id += 1
        my_dataset += dataset

    return my_dataset


def get_All_Activity_Data(access_token: str) -> list:
    page_id = 1
    per_page = 50

    my_dataset = []

    while True:
        # get page of activities from Strava
        activites_url = "https://www.strava.com/api/v3/athlete/activities"
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': per_page, 'page': page_id}

        dataset = requests.get(activites_url, headers=header, params=param).json()

        # if no results then exit loop
        if (not dataset):
            break

        # increment page
        page_id += 1
        my_dataset += dataset

    return my_dataset


def create_Activity_DataFrame(activity_data: list, filters=None) -> pd.DataFrame:

    activity_dataframe = pd.DataFrame(activity_data, columns=filters)

    return activity_dataframe


def _generate_Activity_Count_Plot(activity_data: pd.DataFrame, ax: mpl.axes.Axes, colour_palette: list):
    """
    Generate a bar plot of activity counts over time (by type).

    Arguments:
        activity data - A pandas DataFrame containing the activity data.
        ax - A set of matplotlib axes to generate the plot on.
        colour_palette - The colour palette to generate the plot with.
    """

    # Group the activity data by month and calculate the count of each activity type
    activity_data.index = pd.to_datetime(activity_data.index)
    data = (activity_data.groupby([activity_data.index.to_period('M'), 'type'])
            .size().to_frame('count').reset_index())

    # Generate and format the bar plot
    sns.barplot(x='start_date_local',
                y='count',
                hue='type',
                data=data,
                palette=colour_palette,
                ax=ax)
    ax.set(title='Activities over time', ylabel='Number of activities', xlabel='Month')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.grid(b=True, which='major', linewidth=1.0)
    ax.yaxis.grid(b=True, which='minor', linewidth=0.5)
    ax.set_axisbelow(True)


def display_Activity_Count_Plot(activity_data: pd.DataFrame, colour_palette: list):
    """
    Generate and display a bar plot of activity counts over time (by type).

    Arguments:
        activity_dataframe - A pandas DataFrame containing the activity data.
        colour_palette - The colour palette to generate the plot with.
    """

    # Get only the activity types and start dates
    activity_data = activity_data[['type', 'start_date_local']]
    activity_data = activity_data.set_index('start_date_local')

    # Create an empty set of axes
    fig = plt.figure()
    fig.set_tight_layout(True)
    ax = fig.add_subplot(1, 1, 1)

    # Generate and display the plot
    _generate_Activity_Count_Plot(activity_data, ax, colour_palette)
    plt.show()


def _generate_Summary_Statistics(x: pd.Series) -> pd.Series:
    """
    Generate basic statistics from a given pandas Series.

    Arguments:
        x - The Series to generate basic commute statistics from.
    Return:
        A Series containing the following statistics:
            - Total and average distance
            - Total and average moving time
            - Total and average elevation gain
            - Average speed
    """

    rows = {'Number of activities': x['type'].count(),
            'Total distance (km)': x['distance'].sum() / 1000,
            'Average distance (km)': x['distance'].mean() / 1000,
            'Total moving time (hours)': x['moving_time'].sum() / 3600,
            'Average moving time (mins)': x['moving_time'].mean() / 60,
            'Total elevation gain (km)': x['total_elevation_gain'].sum() / 1000,
            'Average elevation gain (m)': x['total_elevation_gain'].mean(),
            'Average speed (km/h)': x['average_speed'].mean() * 3.6}

    series = pd.Series(rows, index=['Number of activities',
                                    'Total distance (km)',
                                    'Average distance (km)',
                                    'Total moving time (hours)',
                                    'Average moving time (mins)',
                                    'Total elevation gain (km)',
                                    'Average elevation gain (m)',
                                    'Average speed (km/h)'])

    return series


def display_Summary_Statistics(activity_data: pd.DataFrame):
    """
    Display basic statistics for each activity type.

    Arguments:
        activity_dataframe - A pandas DataFrame containing the activity data.
    """

    if not activity_data.empty:
        summary_statistics = activity_data.groupby('type').apply(_generate_Summary_Statistics)

        print()
        print('Summary statistics:')
        print()
        print(summary_statistics.T)
        print()
    else:
        print('Analysis: No activities found!')


# ------------------------------------
# activity uploading related functions
# ------------------------------------
def upload_Fit_Activity_Files(access_token: str, dirpath: str):
    uploads_url = "https://www.strava.com/api/v3/uploads"
    payload = {'client_id': client_ID, 'data_type': 'fit', 'trainer': 1, 'commute': 0}
    header = {'Authorization': 'Bearer ' + access_token}
    
    os.chdir(dirpath)
    for filename in glob.glob("*.fit"):   # glob.glob("%s/*.fit" % dirpath)
        with open(filename, 'rb') as fitfile:
            f = {'file' : fitfile}
            r = requests.post( uploads_url,
                               data=payload,
                               headers=header,
                               files=f )
            print("Uploading your workout activity... " + filename)
            # initial checks will be done for malformed data and duplicates.
            if r.json().get('error') == None:
                while (True):
                    upload_ID = r.json().get('id_str')

                    # polling the upload status per second
                    wait(1)

                    uploads_url = "https://www.strava.com/api/v3/uploads/" + upload_ID
                    header = {'Authorization': 'Bearer ' + access_token}

                    r = requests.get(uploads_url, headers=header)

                    error = r.json().get('error')
                    status = r.json().get('status')
                    activity_id = r.json().get('activity_id')

                    if (error is None) and (activity_id is None): # Possibility 1: Your activity is still being processed.
                        print(status + '... ' + filename)
                    elif (error):                                 # Possibility 2: There was an error processing your activity.
                        print(status + '... ' + filename)
                        print("Error: " + error)
                        print("\n")
                        break
                    else:                                         # Possibility 3: Your activity is ready.
                        print(status + ' ( ' + filename + ' )')
                        fitfile.close()
                        move_To_Uploaded_Activities_Folder(filename)
                        print("\n")
                        break
            else:
                print(r.json().get('status') + filename)
                print("Error: " + r.json().get('error'))
                print("\n")
    
       
def wait(poll_interval):
    time.sleep(poll_interval)


def move_To_Uploaded_Activities_Folder(filename: str):
    source = os.path.join(os.getcwd(), filename)
    dest = r"C:\Users\USER\Documents\Zwift\Activities\UploadedActivities"
    shutil.move(source, dest)
