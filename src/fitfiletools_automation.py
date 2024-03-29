import os
import sys
import time
import glob
import calendar
import pyautogui
import pyperclip
from alive_progress import alive_bar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from typing import Any
from pathlib import Path

from file_manipulation import *


def fix_Fit_Activity_Files():
    owd = os.getcwd()
    os.chdir(ZWIFT_ACTIVITY_DIR)
    fitfile_list = glob.glob("*.fit")
    if not fitfile_list:
        sys.exit("\nNo .fit file(s) to be fixed and uploaded to Strava.\nAborting...")
    else:
        for fitfile in fitfile_list:
            if (fitfile == 'inProgressActivity.fit') or \
               (os.path.getsize(fitfile) < 10000):   # check if the size of the fit file is smaller than 10KB
                    fitfile_list.remove(fitfile)
                    os.remove(os.path.join(ZWIFT_ACTIVITY_DIR, fitfile))

        with alive_bar(1, title='Opening the webpage of FIT File Tools', bar="blocks", spinner="classic") as bar:
            dir = os.path.dirname(__file__)
            WEB_DRIVER_PATH = os.path.abspath( os.path.join(dir, '..', 'webdriver', 'geckodriver.exe') )
            LOG_FILE_PATH = os.path.abspath( os.path.join(dir, '..', 'logfile', 'geckodriver.log') )
            driver = webdriver.Firefox(executable_path=WEB_DRIVER_PATH, service_log_path=LOG_FILE_PATH)
            #driver.maximize_window()
            #driver.minimize_window()

            # Step 1: open the webpage of FIT File Tools
            driver.get("https://www.fitfiletools.com/#/top")
            
            # update progress bar
            bar()

        with alive_bar(len(fitfile_list), title='Fixing FIT activity files', bar="blocks") as bar:
            for fitfile in fitfile_list:
                try:
                    bar.text("Fixing " + fitfile + "...")

                    # Step 2: click the "Launch" button of "Time Adjuster"
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//a[@href='#/adjuster']"))
                    )
                    element.click()

                    # Step 3: click the "... or select files" button
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@ng-file-select='']"))
                    )
                    element.click()
                    time.sleep(1)
                    
                    # Step 4: select the corresponding fit file to be fixed
                    pyperclip.copy(os.path.join(ZWIFT_ACTIVITY_DIR, fitfile))   # copy to clipboard
                    pyautogui.hotkey('ctrl', "v")   # ctrl-v to paste from clipboard
                    finish_file_selection(element)
                    time.sleep(1)

                    # Step 5: select the start date of the activity
                    fitfilebasename = Path(fitfile).stem
                    fitfilebasename_arr = fitfilebasename.split('-')   # YYYY-MM-DD-hh-mm-ss
                    # parsing
                    year = int(fitfilebasename_arr[0])
                    month = int(fitfilebasename_arr[1])
                    day = int(fitfilebasename_arr[2])
                    hour = int(fitfilebasename_arr[3])
                    minute = int(fitfilebasename_arr[4])
                    second = int(fitfilebasename_arr[5])
                    
                    # convert time from 24-hour clock format to 12-hour clock format
                    if (hour > 12):
                        afternoon = True
                        hour -= 12
                    else:
                        afternoon = False
                        if (hour == 0):   # special case
                            hour = 12

                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@ng-model='dt']"))
                    )
                    element.clear()
                    # convert a month number to a month name
                    month_name = calendar.month_name[month]
                    DD_MM_YYYY = str(day) + '-' + month_name + '-' + str(year)
                    element.send_keys(DD_MM_YYYY)
                    time.sleep(1)

                    # Step 6: select the start time (hours & minutes) of the activity
                    # fill in minutes
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@ng-model='minutes']"))
                    )
                    element.clear()
                    element.send_keys(minute)
                    time.sleep(1)

                    # choose A.M. or P.M.
                    if (not afternoon):
                        element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//button[@ng-click='toggleMeridian()']"))
                        )
                        element.click()
                        time.sleep(1)
                    
                    # fill in hours
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@ng-model='hours']"))
                    )
                    element.clear()
                    element.send_keys(str(hour))
                    time.sleep(1)

                    # Step 7: start fixing the activity file
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//a[@ng-click='adjust()']"))
                    )
                    element.click()

                    # Step 8: download your file
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.LINK_TEXT, 'Click here to download your file!'))
                    )
                    element.click()
                    time.sleep(3)
                    # pyautogui.press('return')
                    # time.sleep(3)
                    
                    # update progress bar
                    bar()

                    # Step 9: click the "Close" button of "Time Adjuster"
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.LINK_TEXT, '« Close'))
                    )
                    element.click()

                    # Step 10: rename file in Downloads folder and move to FixedActivities folder
                    newfitfilename = fitfilebasename + "-fixed" + ".fit"
                    rename_FitFile(newfitfilename)
                    move_To_Fixed_Activities_Folder(newfitfilename)

                    # Step 11: move the original fit file in ZWIFT_ACTIVITY_DIR to OriginalActivities folder
                    move_To_Original_Activities_Folder(fitfile)

                except TimeoutException:
                    print("ERROR - Timeout!")
                    driver.quit()

                except NoSuchElementException:
                    print("ERROR - Cannot find the element!")
                    driver.quit()

        # Step 12: finally, close the web browser window and change back to the original working directory
        driver.quit()
        os.chdir(owd)
        print()


def finish_file_selection(element: Any):
    try:
        pyautogui.click()   # simulate a single, left-button mouse click at the mouse’s current position
    except:
        element.send_keys(Keys.RETURN)   # in case the mouse's click doesn't work... 