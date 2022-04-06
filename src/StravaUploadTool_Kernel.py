from authentication import *
from file_manipulation import *
from alive_progress import alive_bar
import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os, subprocess, glob, time
from typing import Any, Tuple



# --------------------------
# function to kill a process
# --------------------------
def kill_process(process_name: str):
    # print(subprocess.getoutput('tasklist'))
    process_list = subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()[0]
    if process_name.encode() in process_list:
        os.system("taskkill /im " + process_name + " /f") # Or: subprocess.call("taskkill /f /im " + process_name)
        print("Successfully kill the running process: " + process_name)
    else:
        print("Error: " + process_name + " is not running\n" + "Aborting...")
        raise SystemExit(0)


# ------------------------------------
# activity uploading related functions
# ------------------------------------
def upload_Fit_Activity_Files(access_token: str):
    os.chdir(os.path.join(zwift_activity_dir, "FixedActivities"))
    fitfile_list = glob.glob("*.fit")

    print("Start uploading activity files...\n")

    with alive_bar(len(fitfile_list), title='Uploading FIT activity files', bar="blocks") as bar:
        for fitfile in fitfile_list:
            with open(fitfile, 'rb') as fit_file:
                try:
                    uploads_url = "https://www.strava.com/api/v3/uploads"
                    payload = {'client_id': CLIENT_ID, 'data_type': 'fit'}
                    header = {'Authorization': 'Bearer ' + access_token}
                    f = {'file': fit_file}
                    r = requests.post(uploads_url,
                                      data=payload,
                                      headers=header,
                                      files=f)
                except requests.RequestException:
                    return None

                print("Uploading " + fitfile + "...")    
                time.sleep(0.05)        
                
                try:
                    upload_ID = r.json().get('id_str')
                except (KeyError, TypeError, ValueError):
                    return None
                    
                while (True):
                    # polling the upload status per second
                    wait(1)
                    
                    isError, activity_id = check_Upload_Status(access_token, fitfile, upload_ID)
                    time.sleep(0.05)
                                                                
                    if (isError):                     # There is an error uploading activity file.
                        # update progress bar
                        bar()
                    
                        break

                    if (activity_id is not None):     # Successfully uploading activity file to Strava!
                        fit_file.close()
                        move_To_Uploaded_Activities_Folder(fitfile)

                        # update progress bar
                        bar()

                        break


def check_Upload_Status(access_token: str, filename: str, upload_ID: str) -> Tuple[bool, Any]:
    try:
        uploads_url = "https://www.strava.com/api/v3/uploads/" + upload_ID
        header = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(uploads_url, headers=header)
    except requests.RequestException:
        return None
    
    try:
        error = r.json().get('error')
        status = r.json().get('status')
        activity_id = r.json().get('activity_id')
    except (KeyError, TypeError, ValueError):
        return None

    if (error is None) and (activity_id is None):  # Possibility 1: Your activity is still being processed.
        print(status + '.. ' + filename)
        return (False, activity_id)
    elif (error):                                  # Possibility 2: There was an error processing your activity. (check for malformed data and duplicates)
        print(status + '.. ' + filename)
        print("ERROR - " + error + '\n')
        return (True, activity_id)
    else:                                          # Possibility 3: Your activity is ready.
        print(status + ' (' + filename + ')' + '\n')
        return (False, activity_id)


def wait(poll_interval: float):
    time.sleep(poll_interval)