import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os, glob, shutil, time



# ------------------------------------
# activity uploading related functions
# ------------------------------------
def upload_Fit_Activity_Files(access_token: str, dirpath: str):
    uploads_url = "https://www.strava.com/api/v3/uploads"
    payload = {'client_id': client_ID, 'data_type': 'fit'}
    header = {'Authorization': 'Bearer ' + access_token}

    os.chdir(dirpath)
    for filename in glob.glob("*.fit"):  # glob.glob("%s/*.fit" % dirpath)
        with open(filename, 'rb') as fitfile:
            f = {'file': fitfile}
            r = requests.post(uploads_url,
                              data=payload,
                              headers=header,
                              files=f)
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

                    if (error is None) and (
                            activity_id is None):  # Possibility 1: Your activity is still being processed.
                        print(status + '... ' + filename)
                    elif (error):  # Possibility 2: There was an error processing your activity.
                        print(status + '... ' + filename)
                        print("Error: " + error)
                        print("\n")
                        break
                    else:  # Possibility 3: Your activity is ready.
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