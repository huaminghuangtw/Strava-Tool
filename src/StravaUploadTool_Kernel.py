from authentication import *
from file_manipulation import *
from typing import Any, Tuple
from alive_progress import alive_bar
import requests
import sys, os, subprocess, glob
import time, datetime
import imaplib, email
import re


# --------------------------------
# Function to prepare .fit file(s)
# --------------------------------
def preprocessing():
    # print(subprocess.getoutput('tasklist'))
    process_list = subprocess.Popen('tasklist', stdout=subprocess.PIPE).communicate()[0]
    process_name = "ZwiftApp.exe"
    if process_name.encode() in process_list:
        exit_code = os.system("taskkill /f /im " + process_name) # Or: subprocess.call("taskkill /f /im " + process_name)
        if (exit_code == 0):
            print("Successfully kill the running process: " + process_name)
        else:
            sys.exit("Aborting...")
    else:
        # Enable less secure apps on your Google account:
        # https://myaccount.google.com/lesssecureapps
        print(process_name + " is not running." + "\n" + "Try to find .fit file(s) from GMAIL...")
        gmail = imaplib.IMAP4_SSL("imap.gmail.com")
        typ, accountDetails = gmail.login(GMAIL_USER_ID, GMAIL_PASSWORD)
        if (typ != 'OK'):
            print('Not able to sign in!')
            raise
        typ, data = gmail.select('Inbox')
        if (typ != 'OK'):
            print('Error searching Inbox!')
            raise
        today = datetime.date.today().strftime("%d-%b-%Y")
        typ, email_list = gmail.search(None, f'(ON {today} TO {GMAIL_USER_ID})')
        # print(email_list)
        # Useful links:
        #    1. https://docs.python.org/3/library/imaplib.html#imaplib.IMAP4.search
        #    2. https://gist.github.com/martinrusev/6121028
        email_list = email_list[0].split()
        for email_id in email_list:
            downloaAttachmentsInEmail(gmail, email_id, ZWIFT_ACTIVITY_DIR)
        gmail.close()
        gmail.logout()


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

def downloaAttachmentsInEmail(connection, email_id, download_folder):
    """
    Function to download all attachment files for a given email
    """
    try:
        typ, data = connection.fetch(email_id, "(BODY.PEEK[])") # use PEEK so we don't change the UNSEEN status of the email messages
        if (typ != 'OK'):
            print('Error fetching email!')
            raise
        email_body = data[0][1]
        raw_emails = email.message_from_bytes(email_body)
        # print(raw_emails)
        for mail in raw_emails.walk():
            if (mail.get_content_maintype() == 'multipart'):
                # print(mail.as_string())
                continue
            if (mail.get('Content-Disposition') is None):
                # print(mail.as_string())
                continue
            fileName = mail.get_filename()
            if fileName.endswith('.fit'):
                attachment_path = os.path.join(download_folder, fileName)
                if not os.path.isfile(attachment_path):
                    print('Downloading email attachment: ' + fileName + '...')
                    f = open(attachment_path, 'wb')
                    f.write(mail.get_payload(decode=True))
                    f.close()
    except:
        print('Error downloading all attachments!')