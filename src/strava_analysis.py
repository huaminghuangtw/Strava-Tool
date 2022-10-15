import pandas as pd  # Pandas will be the backbone of our data manipulation.


def print_StravaAnalysisTool():
	print(r"""
   _____  _                                                     _              _    _______             _ 
  / ____|| |                               /\                  | |            (_)  |__   __|           | |
 | (___  | |_  _ __  __ _ __   __ __ _    /  \    _ __    __ _ | | _   _  ___  _  ___ | |  ___    ___  | |
  \___ \ | __|| '__|/ _` |\ \ / // _` |  / /\ \  | '_ \  / _` || || | | |/ __|| |/ __|| | / _ \  / _ \ | |
  ____) || |_ | |  | (_| | \ V /| (_| | / ____ \ | | | || (_| || || |_| |\__ \| |\__ \| || (_) || (_) || |
 |_____/  \__||_|   \__,_|  \_/  \__,_|/_/    \_\|_| |_| \__,_||_| \__, ||___/|_||___/|_| \___/  \___/ |_|
                                                                    __/ |                                 
                                                                   |___/                                  
    """)


def create_Activity_DataFrame(activity_data: list, filters=None) -> pd.DataFrame:
    activity_dataframe = pd.DataFrame(activity_data, columns=filters)
    return activity_dataframe