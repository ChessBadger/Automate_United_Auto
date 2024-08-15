import cv2
import numpy as np
import pyautogui
import tkinter as tk
import time

window = None


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



#Clear
click_button('Images/Setup/Clear.png', .8)
click_button('Images/Setup/Clear.png', .8)
time.sleep(10)

click_button('Images/Setup/ClearOk.png', .8)

click_button('Images/Setup/ClearYes.png', .8)

click_button('Images/Setup/ClearOk2.png', .7)

# Restore
click_button('Images/Setup/Restore.png', .8)

click_button('Images/General/Navigate.png', .8)

# Shift
create_interface('Images/Setup/Shift.png', .7)

click_button('Images/Setup/ShiftOk.png', .8)

click_button('Images/Setup/ShiftYes.png', .8)
time.sleep(15)
click_button('Images/Setup/ShiftOk1.png', .7)

click_button('Images/Setup/Close.png', .8)



# Today's Info
click_button('Images/MainMenu/TodayInfo.png', .8)

click_button('Images/TodayInfo/TodayInfo2.png', .9)

create_interface('Images/TodayInfo/TodaySave.png', .8)

click_button('Images/TodayInfo/TodayClose.png', .8)

# Finalize
click_button('Images/MainMenu/Proofing.png', .8)
click_button('Images/InventoryProofing/Finalize.png', .8)
click_button('Images/InventoryProofing/FinalYes.png', .8)
click_button('Images/InventoryProofing/FinalOk.png', .8)
click_button('Images/InventoryProofing/FinalClose.png', .8)


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



create_interface('Images/Reports/Ok.png', .8)

click_button('Images/Reports/PDF.png', .8)

click_button('Images/Reports/Navigate.png', .8)

create_interface('Images/Reports/Exit.png', .8)


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



while True:
    pass
