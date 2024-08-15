import cv2
import numpy as np
import pyautogui
import tkinter as tk
import time
import os
import re
import shutil
from pynput.keyboard import Controller, Key

keyboard = Controller()

window = None

# Prompt user for path
base_path = input('Enter the base path: ')

# Get parent directory
parent_path = os.path.dirname(base_path)

# Create path for "Prep" folder
prep_path = os.path.join(parent_path, 'Prep')

# Regular expression for six digit integer
regex = r'\d{6}'

# Arrays to store subdirectories with 6-digit integer in their name
base_subdirs = []
parent_subdirs = []
prep_subdirs = []
original_dates = []
inv_dates = []    


for name in os.listdir(prep_path):
    subdir_path = os.path.join(prep_path, name)
    if os.path.isdir(subdir_path):
        prep_subdirs.append(subdir_path)            
                
# Loop through first-level directories in base_path
for dirname in os.listdir(base_path):
    full_dir_path = os.path.join(base_path, dirname)
    
    # Check if it's a directory
    if os.path.isdir(full_dir_path):
        base_subdirs.append(full_dir_path)
        
        zip_folder = os.path.join(full_dir_path, 'zip')
        
        # Create 'zip' directory if it doesn't exist
        if not os.path.exists(zip_folder):
            os.makedirs(zip_folder)
        
        # Check each file in the directory
        for filename in os.listdir(full_dir_path):
            if os.path.isfile(os.path.join(full_dir_path, filename)) and \
                    re.search(r'\.zip$', filename, re.IGNORECASE) and \
                    not re.search(regex, filename):
                # Move file to 'zip' directory
                shutil.move(os.path.join(full_dir_path, filename), os.path.join(zip_folder, filename))        
                

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


for i in range(len(base_subdirs)):
    current_store = base_subdirs[i]  # The current_store for this iteration
    invPath = parent_subdirs[i]  # This replaces the user input for invPath
    card_folder = prep_subdirs[i] + '\Cards'

    # Parse the invDate from the directory name (assuming it's at the end of the name)
    invDate = inv_dates[i]
    og_date = original_dates[i]
    
    
    #Clear
    click_button('Images/Setup/Clear.png', .8)
    click_button('Images/Setup/Clear.png', .8)
    time.sleep(30)

    click_button('Images/Setup/ClearBar.png', .8)
    
    click_button('Images/Setup/ClearOk.png', .8)

    click_button('Images/Setup/ClearYes.png', .8)
    
    click_button('Images/Setup/ClearOk2.png', .7)
    
    time.sleep(20)


    click_button('Images/Setup/ClearOk2.png', .7)

    # Restore
    click_button('Images/Setup/Restore.png', .8)

    click_button('Images/General/Navigate.png', .8)
    
    time.sleep(1.5)

    pyautogui.press('f4', interval=1.25)
    
    time.sleep(1.5)

    pyautogui.hotkey('ctrl', 'a')
    
    time.sleep(1.5)

    pyautogui.write(current_store)
    
    time.sleep(1.5)

    pyautogui.press('enter', interval=1.5)
    
    time.sleep(1.5)

    click_button('Images/Setup/ZipIcon.png', .7)

    click_button('Images/Setup/Open.png', .8)

    click_button('Images/Setup/OkRestore.png', .7)

    click_button('Images/Setup/RestoreYes.png', .8)

    click_button('Images/Setup/RestoreOk.png', .8)
    
    click_button('Images/Setup/Close.png', .8)



    # Today's Info
    click_button('Images/MainMenu/TodayInfo.png', .8)

    click_button('Images/TodayInfo/TodayInfo2.png', .9)

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
    time.sleep(15)

    click_button('Images/General/OK.png', .8)

    click_button('Images/Reports/Custom.png', .8)

    click_button('Images/Reports/Area.png', .8)

    click_button('Images/Reports/SelectAreas.png', .8)

    click_button('Images/Reports/SelectKroWorksheet.png', .8)

    click_button('Images/Reports/Ok.png', .8)

    pyautogui.press('right', interval=1.25)

    pyautogui.press('down', interval=1.25)
    
    time.sleep(1.5)

    pyautogui.write('000', interval=1.25)

    pyautogui.press('enter', interval=1.25)

    pyautogui.write('000', interval=1.25)

    pyautogui.press('enter', interval=1.25)

    click_button('Images/Reports/Ok.png', .8)

    click_button('Images/Reports/PDF.png', .8)

    click_button('Images/Reports/NoPreview.png', .8)

    click_button('Images/Reports/Navigate.png', .8)

    # 
    time.sleep(1.5)
    
    pyautogui.press('f4', interval=1.25)

    pyautogui.hotkey('ctrl', 'a')

    pyautogui.write(invPath)

    pyautogui.press('enter', interval=.5)

    pyautogui.hotkey('alt', 'n')

    pyautogui.write('worksheet')

    pyautogui.press('enter', interval=.5)

    pyautogui.press('enter')
    
    time.sleep(1.5)

    click_button('Images/Reports/Exit.png', .8)

    click_button('Images/Reports/Cancel.png', .8)

    click_button('Images/Reports/ReturnHome.png', .8)


    # Export to Wintakes
    click_button('Images/MainMenu/Export.png', .8)

    click_button('Images/Exports/ExportsOk.png', .8)

    click_button('Images/Exports/Wintakes.png', .8)

    click_button('Images/Exports/Save.png', .8)

    click_button('Images/Exports/Save.png', .8)

    click_button('Images/Exports/Save.png', .8)

    click_button('Images/Exports/Cancel.png', .8)

    click_button('Images/Exports/Cancel.png', .8)

    click_button('Images/Exports/Cancel.png', .8)

    click_button('Images/Exports/ExportsOk2.png', .65)

    click_button('Images/Exports/Close.png', .8)


    # Backup
    click_button('Images/MainMenu/Setup.png', .8)

    click_button('Images/Setup/Backup.png', .8)

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

    pyautogui.write(og_date)

    pyautogui.press('enter', interval=.5)
    
    pyautogui.press('enter', interval=.5)
    
    click_button('Images/Setup/BackupYes.png', .7)
    
    click_button('Images/Setup/BackupOk.png', .7)

    #Wintakes
    click_button('Images/Wintakes/Wintakes.png', .8)
    click_button('Images/Wintakes/Y.png', .8)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    click_button('Images/Wintakes/CategoryDbf.png', .8)
    with keyboard.pressed(Key.ctrl):
        keyboard.press('a')
        keyboard.release('a')
    time.sleep(1)
    with keyboard.pressed(Key.ctrl):
        keyboard.press('x')
        keyboard.release('x')
    click_button('Images/Wintakes/SkuDlf.png', .8)
    with keyboard.pressed(Key.ctrl):
        keyboard.press('v')
        keyboard.release('v')
    click_button('Images/Wintakes/2.png', .8)
    click_button('Images/Wintakes/1Area.png', .8)
    time.sleep(5)
    click_button('Images/Wintakes/BackArea.png', .8)
    click_button('Images/Wintakes/2Location.png', .8)
    time.sleep(5)
    click_button('Images/Wintakes/BackArea.png', .8)
    click_button('Images/Wintakes/3Category.png', .8)
    time.sleep(5)
    click_button('Images/Wintakes/BackArea.png', .8)
    click_button('Images/Wintakes/BackArea.png', .8)
    click_button('Images/Wintakes/3.png', .8)
    click_button('Images/Wintakes/Send.png', .8)
    click_button('Images/Wintakes/Downloads.png', .8)
    click_button('Images/Wintakes/AreaDownload.png', .8)
    click_button('Images/Wintakes/ItemDownload.png', .8)
    click_button('Images/Wintakes/Store.png', .8)
    click_button('Images/Wintakes/CreateDownloads.png', .7)
    time.sleep(110)
    click_button('Images/Wintakes/Ok.png', .8)
    click_button('Images/Wintakes/BackDownloads.png', .8)
    click_button('Images/Wintakes/Item.png', .8)
    click_button('Images/Wintakes/Config.png', .8)
    click_button('Images/Wintakes/Directories.png', .8)
    click_button('Images/Wintakes/Copy.png', .8)
    click_button('Images/Wintakes/CardPrep.png', .8)
    click_button('Images/Wintakes/Ok2.png', .8)
    click_button('Images/Wintakes/Ok.png', .8)
    click_button('Images/Wintakes/BackSend.png', .8)
    click_button('Images/Wintakes/BackArea.png', .8)
    click_button('Images/Wintakes/5.png', .8)
    click_button('Images/Wintakes/Select.png', .8)
    click_button('Images/Wintakes/AreaCheck.png', .8)
    click_button('Images/Wintakes/LocationCheck.png', .8)
    click_button('Images/Wintakes/CategoryCheck.png', .8)
    click_button('Images/Wintakes/ItemCheck.png', .8)
    click_button('Images/Wintakes/Proceed.png', .8)
    click_button('Images/Wintakes/CardPrep.png', .8)
    click_button('Images/Wintakes/Ok2.png', .8)
    time.sleep(.75)
    click_button('Images/Wintakes/Ok.png', .8)
    click_button('Images/Wintakes/Delete.png', .8)
    click_button('Images/Wintakes/ItemCheck.png', .8)
    click_button('Images/Wintakes/Proceed.png', .8)
    click_button('Images/Wintakes/Yes.png', .8)
    click_button('Images/Wintakes/Ok.png', .8)
    click_button('Images/Wintakes/BackFinal.png', .8)

        
    #Cards
    click_button('Images/Wintakes/Explorer.png', .8)
    
    pyautogui.press('f4', interval=.6)

    pyautogui.hotkey('ctrl', 'a', interval=.6)

    pyautogui.write('C:\CardPrep')
    
    pyautogui.press('enter', interval=.5)
    
    time.sleep(1.5)
    
    click_button('Images/Setup/ZipIcon.png', .7)
    
    pyautogui.hotkey('ctrl', 'a', interval=.6)
    
    pyautogui.hotkey('ctrl', 'x', interval=.6)
    
    pyautogui.press('f4', interval=1.0)

    pyautogui.hotkey('ctrl', 'a', interval=.6)

    pyautogui.write(card_folder)
    
    pyautogui.press('enter', interval=1.0)
    
    pyautogui.hotkey('ctrl', 'v', interval=.6)
    
    click_button('Images/Wintakes/Setup.png', .7)
    
    pyautogui.hotkey('ctrl', 'x', interval=.6)
    
    pyautogui.press('f4', interval=1.0)

    pyautogui.hotkey('ctrl', 'a', interval=.6)

    pyautogui.write(invPath)
    
    pyautogui.press('enter', interval=1.0)
    
    pyautogui.hotkey('ctrl', 'v', interval=.6)
    
    click_button('Images/Wintakes/United.png', .8)

while True:
    pass
