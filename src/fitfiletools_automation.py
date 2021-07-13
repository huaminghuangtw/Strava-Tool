from file_manipulation import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import os, glob, pyautogui, time
from datetime import datetime


def fix_Fit_Activity_Files():
    dir = os.path.dirname(__file__)
    WEB_DRIVER_PATH = os.path.abspath( os.path.join(dir, '..', 'webdriver', 'geckodriver.exe') )
    LOG_FILE_PATH = os.path.abspath( os.path.join(dir, '..', 'logfile', 'geckodriver.log') )
    driver = webdriver.Firefox(executable_path=WEB_DRIVER_PATH, service_log_path=LOG_FILE_PATH)
    driver.maximize_window()

    # Step 1: open the webpage of FIT File Tools
    driver.get("https://www.fitfiletools.com/#/top")

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
    time.sleep(3)

    # Step 4: select the corresponding fit file to be fixed
    os.chdir(zwift_activity_dir)
    for fitfile in glob.glob("*.fit"):
        path_to_fitfile = os.path.join(zwift_activity_dir, fitfile)
        # check if the size of the fit file is larger than 10KB
        if (os.path.getsize(path_to_fitfile) < 10000):
            move_To_Temp_Folder(fitfile)
        else:
            try:
                pyautogui.write(path_to_fitfile, interval=0.05)
                pyautogui.press('return')   # TODO: sometimes not working...
                time.sleep(1)

                # Step 5: select start date the activity
                filename = fitfile.split('-')

                # convert a month number to a month name
                filename[1] = datetime.strptime(filename[1], "%m").strftime("%B")

                # convert time from 24-hour clock format to 12-hour clock format
                hours = int(filename[3])
                if hours > 12:
                    afternoon = True
                    hours -= 12
                else:
                    afternoon = False
                    if hours == 0:   # special case
                        hours = 12

                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@ng-model='dt']"))
                )
                element.clear()
                dd_mm_yyyy = filename[2] + '-' + filename[1] + '-' + filename[0]
                element.send_keys(dd_mm_yyyy)
                element.send_keys(Keys.RETURN)
                time.sleep(1)

                # Step 6: select start time (hours & minutes) of the activity
                # fill in minutes
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@ng-model='minutes']"))
                )
                element.clear()
                element.send_keys(filename[4])
                element.send_keys(Keys.RETURN)
                time.sleep(1)

                # fill in hours
                if not afternoon:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@ng-click='toggleMeridian()']"))
                    )
                    element.click()

                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@ng-model='hours']"))
                )
                element.clear()
                element.send_keys(str(hours))
                element.send_keys(Keys.RETURN)
                time.sleep(1)

                # Step 7: start fix activity file
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@ng-click='adjust()']"))
                )
                element.click()

                # Step 8: download your file
                # if Firfox asks you where to save files and specify the file name...
                # fixedfile_dir = os.path.join(zwift_activity_dir, 'FixedActivities')
                # newFilename = os.path.join(fixedfile_dir, filename[1], filename[2])  # mmdd.fit
                # pyautogui.write(newFilename, interval=0.05)
                # time.sleep(3)
                # pyautogui.press('return')
                # time.sleep(3)
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Click here to download your file!'))
                )
                element.click()
                time.sleep(3)
                pyautogui.press('return')
                time.sleep(3)

                # Step 9: rename file in Downloads folder and move to FixedActivities folder
                newfilename = filename[1] + filename[2] + '.fit'   # mmdd.fit
                rename_FitFile(newfilename)
                move_To_Fixed_Activities_Folder(newfilename)

                # Step 10: finally, move the original fit file in zwift_activity_dir to Temp folder
                move_To_Temp_Folder(fitfile)

            except TimeoutException:
                print("ERROR - Timeout!")
                driver.quit()

            except NoSuchElementException:
                print("ERROR - Cannot find the element!")
                driver.quit()
    
    # close the browser window
    driver.quit()