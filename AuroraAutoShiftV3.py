import cv2
import numpy as np
import pyautogui
import tkinter as tk
import time
import os
import re
import shutil
import errno
from pynput.keyboard import Controller, Key

keyboard = Controller()

window = None

#AURORA

# Prompt user for path
base_path = input('Enter the base path: ')

# Get parent directory
parent_path = os.path.dirname(base_path)

# Regular expression for six digit integer
regex = r'\d{6}'

# Arrays to store subdirectories with 6-digit integer in their name
base_subdirs = []
parent_subdirs = []
original_dates = []
inv_dates = []

try:
    # Check each directory in the base path
    for dirname in os.listdir(base_path):
        if re.search(regex, dirname):
            base_subdirs.append(os.path.join(base_path, dirname))

        full_dir_path = os.path.join(base_path, dirname)

        # Check if it's a directory
        if os.path.isdir(full_dir_path):
            zip_folder = os.path.join(full_dir_path, 'zip')

            # Create 'zip' directory if not exists
            try:
                os.makedirs(zip_folder, exist_ok=True)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            # Check each file in the directory
            for filename in os.listdir(full_dir_path):
                if filename.lower().endswith(('.zip', '.ZIP', '.Zip')) and not re.search(regex, filename):
                    # Move file to 'zip' directory
                    shutil.move(os.path.join(full_dir_path, filename), os.path.join(zip_folder, filename))
except FileNotFoundError as e:
    print(f"Error: {base_path} does not exist: {e}")
except OSError as e:
    print(f"Error: {e}")
    
try:
    # Check each directory in the parent path
    for dirname in os.listdir(parent_path):
        match = re.search(regex, dirname)
        if match:
            parent_subdirs.append(os.path.join(parent_path, dirname))

            # Extract the six-digit number and rearrange the digits
            six_digit_num = match.group()
            original_dates.append(six_digit_num)
            inv_date = six_digit_num[2:] + six_digit_num[:2]
            inv_dates.append(inv_date)
            
except FileNotFoundError as e:
    print(f"Error: {parent_path} does not exist: {e}")
except OSError as e:
    print(f"Error: {e}")


def click_button(button_image_path, setThreshold):
    for attempt in range(100):  # Retry for up to 15 attempts
        try:
            # Take a screenshot
            pyautogui.screenshot('screenshot.png')

            # Read the images from the file
            small_image = cv2.imread(button_image_path)
            large_image = cv2.imread('screenshot.png')

            # Check if images loaded successfully
            if small_image is None:
                raise ValueError(f"Could not read image {button_image_path}")
            if large_image is None:
                raise ValueError("Could not read image screenshot.png")

            result = cv2.matchTemplate(small_image, large_image, cv2.TM_CCOEFF_NORMED)

            # Get the maximum correlation value (small_image's top-left corner in large_image)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Set a threshold for match
            threshold = setThreshold
				
            if max_val >= threshold:
                # Calculate the center point of the matched region
                h, w, d = small_image.shape
                center = (max_loc[0] + w // 2, max_loc[1] + h // 2)

                # Move the mouse cursor to the center of the matched region
                pyautogui.moveTo(center[0], center[1])

                # Use PyAutoGUI to click at the current mouse position
                pyautogui.click()

                # Print success message
                print(f"Clicked {button_image_path} successfully!")

                # Return after successfully clicking the button
                return
            else:
                print(f"No match found for {button_image_path} after attempt {attempt + 1}. Max_val = {max_val}")

        except Exception as e:
            print(f"Error occurred while processing {button_image_path}: {e}")
            # Wait for a short duration before retrying
            time.sleep(0.5)

    print(f"No good match found for {button_image_path} after 15 attempts. Last max_val =", max_val)


def create_interface(button_image_path, setThreshold):
    def click_and_destroy():
        click_button(button_image_path, setThreshold)
        if window is not None:
            window.destroy()

    global window
    window = tk.Tk()

    # Set the window size
    window.geometry('300x100')  # Width x Height

    button2 = tk.Button(window, text="Continue", command=click_and_destroy, width=250, height=50)
    button2.pack()

    window.mainloop()

for i in range(len(base_subdirs)):
    current_store = base_subdirs[i]  # The current_store for this iteration
    invPath = parent_subdirs[i]  # This replaces the user input for invPath

    # Parse the invDate from the directory name (assuming it's at the end of the name)
    invDate = inv_dates[i]
    origDate = original_dates[i]
        
    # Clear/Restore
    click_button('Images/Setup/ClearRestore.png', .8)

    time.sleep(0.5)

    click_button('Images/General/Navigate.png', .8)

    time.sleep(0.5)

    pyautogui.press('f4', interval=1.25)

    pyautogui.hotkey('ctrl', 'a')

    pyautogui.write(current_store)

    pyautogui.press('enter', interval=1.5)

    click_button('Images/Setup/ZipIcon.png', .7)

    click_button('Images/Setup/Open.png', .8)

    click_button('Images/Setup/OkClearRestore.png', .8)

    click_button('Images/Setup/ClearOk2.png', .7)
 
    click_button('Images/Setup/Close.png', .8)


    # Today's Info
    click_button('Images/MainMenu/TodayInfo.png', .8)

    time.sleep(.5)

    click_button('Images/TodayInfo/TodayInfo2.png', .999)

    pyautogui.write(invDate)

    pyautogui.press('tab', presses=6, interval=0.25)

    pyautogui.write('1')

    pyautogui.press('tab', presses=2, interval=0.25)

    pyautogui.write('1')

    click_button('Images/TodayInfo/TodaySave.png', .8)

    click_button('Images/TodayInfo/TodayClose.png', .8)


    # Create Reports
    click_button('Images/MainMenu/Reports.png', .8)

    click_button('Images/Reports/OptionsOk.png', .8)

    click_button('Images/Reports/Custom.png', .8)

    click_button('Images/Reports/Area.png', .8)

    click_button('Images/Reports/SelectAreas.png', .8)

    click_button('Images/Reports/Pharmacy.png', .8)

    click_button('Images/Reports/Ok.png', .8)

    time.sleep(0.5)

    click_button('Images/Reports/PDF.png', .8)

    click_button('Images/Reports/NoPreview.png', .8)

    click_button('Images/Reports/Navigate.png', .8)

    # 
    pyautogui.press('f4', interval=1.25)

    pyautogui.hotkey('ctrl', 'a')

    pyautogui.write(invPath)

    pyautogui.press('enter', interval=.5)

    pyautogui.hotkey('alt', 'n')

    pyautogui.write('worksheet')

    pyautogui.press('enter', interval=.5)

    pyautogui.press('enter')


    click_button('Images/Reports/Exit.png', .8)


    click_button('Images/Reports/Cancel.png', .8)

    click_button('Images/Reports/ReturnHome.png', .8)

    click_button('Images/Reports/ReturnHome2.png', .8)


    # Backup
    click_button('Images/MainMenu/Setup.png', .8)

    click_button('Images/Setup/Backup.png', .8)

    time.sleep(.3)

    click_button('Images/General/Navigate.png', .8)
    
    # 
    pyautogui.press('f4')

    pyautogui.hotkey('ctrl', 'a', interval=1.25)

    pyautogui.write(current_store)
    
    pyautogui.press('enter', interval=.5)
    
    click_button('Images/Setup/ZipIcon.png', .7)
    
    pyautogui.press('f4')

    pyautogui.hotkey('ctrl', 'a', interval=1.25)

    pyautogui.write(invPath)
    
    pyautogui.press('enter', interval=.5)
    
    pyautogui.hotkey('alt', 'n')
    
    pyautogui.press('left', interval=.5)
    
    pyautogui.hotkey('ctrl', 'right', interval=.5)
    
    pyautogui.hotkey('ctrl', 'right', interval=.5)
    
    pyautogui.press('delete')
    
    pyautogui.press('delete')
    
    pyautogui.press('delete')
    
    pyautogui.press('delete')
    
    pyautogui.press('delete')
    
    pyautogui.press('delete')

    pyautogui.write(origDate)

    pyautogui.press('enter', interval=.5)
    
    pyautogui.press('enter', interval=.5)
    
    click_button('Images/Setup/BackupYes.png', .7)
    
    time.sleep(.5)
    
    click_button('Images/Setup/BackupOk.png', .7)
    
 
while True:
    pass