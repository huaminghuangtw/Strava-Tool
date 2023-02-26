import os
import requests
import subprocess
import glob
import time
import re
from typing import Any, Tuple
from alive_progress import alive_bar

from authentication import *
from file_manipulation import *


def print_StravaUploadTool():
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


# -----------------------------------------------
# Function to prepare .fit file(s) to be uploaded
# -----------------------------------------------
def preprocessing():
    process_list = subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()[0]
    zwift = "ZwiftApp.exe"
    if zwift.encode() in process_list:
        exit_code = os.system("taskkill /f /im " + zwift)
        if (exit_code == 0):
            print("Successfully killed", zwift)


# ------------------------------------
# Activity uploading related functions
# ------------------------------------
def upload_Fit_Activity_Files(access_token: str):
    os.chdir(os.path.join(ZWIFT_ACTIVITY_DIR, "FixedActivities"))
    fitfile_list = glob.glob("*.fit")

    print("\nStart uploading activity files...\n")

    with alive_bar(len(fitfile_list), title='Uploading FIT activity files', bar="blocks") as bar:
        for fitfile in fitfile_list:
            with open(fitfile, 'rb') as fit_file:
                try:
                    base_url = "https://www.strava.com/api/v3/uploads"
                    data = {
                        'client_id': STRAVA_CLIENT_ID,
                        'data_type': 'fit'
                    }
                    header = {'Authorization': 'Bearer ' + access_token}
                    f = {'file': fit_file}
                    r = requests.post(
                                    base_url,
                                    data=data,
                                    headers=header,
                                    files=f
                                )
                except requests.exceptions.RequestException:
                    return None

                print("Uploading " + fitfile + "...")    
                time.sleep(0.05)        
                
                try:
                    upload_ID = r.json().get('id_str')
                except (KeyError, TypeError, ValueError):
                    return None
                    
                while True:
                    # polling the upload status per semaild
                    wait(1)
                    
                    isError, activity_id = check_Upload_Status(access_token, upload_ID)
                    time.sleep(0.05)
                    
                    # If there is an error uploading activity file or
                    # it's been successfully uploaded to Strava
                    if (isError) or (activity_id is not None):
                        fit_file.close()
                        move_To_Uploaded_Or_Malformed_Activities_Folder(fitfile)
                        
                        if (activity_id is not None):
                            print("Activity ID:", activity_id)
                            print(
                                "Congratulations! Check out your workout here: " + 
                                link(
                                    "https://www.strava.com/activities/" +
                                    str(activity_id)
                                )
                            )

                        # update progress bar
                        bar()
                        
                        break
                print("")


def check_Upload_Status(access_token: str, upload_ID: str) -> Tuple[bool, Any]:
    try:
        base_url = "https://www.strava.com/api/v3/uploads/" + upload_ID
        header = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(base_url, headers=header)
    except requests.exceptions.RequestException:
        return None
    
    try:
        error_msg = r.json().get('error')
        status = r.json().get('status')
        activity_id = r.json().get('activity_id')
    except (KeyError, TypeError, ValueError):
        return None

    if (error_msg is None) and (activity_id is None):  # Possibility 1: Your activity is still being processed.
        print(status + '.. ')
        return (False, activity_id)
    elif (error_msg):                                  # Possibility 2: There was an error processing your activity. (check for malformed data and duplicates)
        print(status + '.. ')
        print("Reason: " + error_msg + '\n')
        if findWholeWord('malformed')(error_msg):
            print("Please check this file in the 'UploadedOrMalformedActivities' folder!\n")
        return (True, activity_id)
    else:                                              # Possibility 3: Your activity is ready.
        print(status + '\n')
        return (False, activity_id)


# ----------------
# Helper functions
# ----------------
def wait(poll_interval: float):
    time.sleep(poll_interval)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def link(uri, label=None):
    """
    Source: https://stackoverflow.com/a/71309268/10351382
    """
    if label is None: 
        label = uri
    parameters = '' 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(parameters, uri, label)