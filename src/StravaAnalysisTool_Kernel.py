import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd  # Pandas will be the backbone of our data manipulation.
from pandas.io.json import json_normalize
import seaborn as sns  # Seaborn is a data visualization library.
import matplotlib as mpl  # Matplotlib is a data visualization library.
import matplotlib.pyplot as plt
import json
import numpy as np  # Numpy will help us handle some work with arrays.
from datetime import datetime  # Datetime will allow Python to recognize dates as dates, not strings.



# -------------------------------
# data analysis related functions
# -------------------------------
def get_Latest_Activity_Data(access_token: str, numberOfActivities: str) -> list:
    """
    Arguments:
        numberOfActivities: number of the latest activities you want to retrieve from your Strava feed.
    """
    try:
        activites_url = "https://www.strava.com/api/v3/athlete/activities"
        header = {'Authorization': 'Bearer ' + access_token}
        param = {'per_page': numberOfActivities, 'page': 1}
        r = requests.get(activites_url, headers=header, params=param)
    except requests.RequestException:
        return None

    my_dataset = r.json()

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
        try:
            activites_url = "https://www.strava.com/api/v3/athlete/activities"
            header = {'Authorization': 'Bearer ' + access_token}
            param = {'before': before, 'after': after, 'per_page': per_page, 'page': page_id}
            r = requests.get(activites_url, headers=header, params=param)
        except requests.RequestException:
            return None
        
        dataset = r.json()

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
        try:
            activites_url = "https://www.strava.com/api/v3/athlete/activities"
            header = {'Authorization': 'Bearer ' + access_token}
            param = {'per_page': per_page, 'page': page_id}
            r = requests.get(activites_url, headers=header, params=param)
        except requests.RequestException:
            return None
        
        dataset = r.json()

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