import pyautogui
import keyboard
import time

pyautogui.FAILSAFE = True

#Images (update these to match your files)
COM_SERVER_IMAGE = 'Community_Servers_1.png'
REFRESH_IMAGE = 'refresh.png'
SERVER_NAME_IMAGE = 'PT_Realism1.png'
CONFIRM_JOIN_IMAGE = 'confirm.png'
CONFIRM_PASS_IMAGE = 'confirm_2.png'
OK_RETRY_IMAGE = 'ok_retry.png'

#Settings
RETRY_INTERVAL = 10
STOP_HOTKEY = 'esc'
CONFIDENCE = 0.9
SERVER_NAME = 'pt: realism'

def wait_and_click(image_path, timeout=15):
    print(f"Looking for {image_path}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if keyboard.is_pressed(STOP_HOTKEY):
            print("Stop hotkey pressed. Exiting.")
            return False
        location = pyautogui.locateCenterOnScreen(image_path, confidence=CONFIDENCE)
        if location:
            pyautogui.moveTo(location)
            pyautogui.click()
            print(f"Clicked on {image_path}")
            return True
        time.sleep(1)
    print(f"Failed to find {image_path} in time.")
    return False

def find_and_click_specific(image_path, prefer='top', timeout=15):
    """
    Clicks a specific instance of an image based on vertical screen position.
    prefer: 'top', 'bottom', or 'middle'
    """
    print(f"Searching for all matches of {image_path}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if keyboard.is_pressed(STOP_HOTKEY):
            print("Stop hotkey pressed. Exiting.")
            return False

        matches = list(pyautogui.locateAllOnScreen(image_path, confidence=CONFIDENCE))
        if matches:
            print(f"Found {len(matches)} matches for {image_path}")

            if prefer == 'top':
                match = sorted(matches, key=lambda x: x.top)[0]
            elif prefer == 'bottom':
                match = sorted(matches, key=lambda x: x.top)[-1]
            elif prefer == 'middle':
                match = sorted(matches, key=lambda x: x.top)[len(matches)//2]
            else:
                match = matches[0]

            center = pyautogui.center(match)
            pyautogui.moveTo(center)
            pyautogui.click()
            print(f"Clicked on {prefer} match of {image_path}")
            return True

        time.sleep(1)

    print(f"No suitable match for {image_path} found in time.")
    return False

def check_for_join_fail(timeout=15):
    """Checks if the join failed popup appears and clicks OK if it does."""
    print("Monitoring for join failure popup...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if keyboard.is_pressed(STOP_HOTKEY):
            print("Stopped by user.")
            return False

        try:
            fail_popup = pyautogui.locateCenterOnScreen(OK_RETRY_IMAGE, confidence=CONFIDENCE)
        except pyautogui.ImageNotFoundException:
            fail_popup = None

        if fail_popup:
            print("Join failed popup detected! Clicking OK...")
            pyautogui.moveTo(fail_popup)
            pyautogui.click()
            return True

        time.sleep(0.5)
    return False

def join_server():
    print("Starting join attempt... Please be patient!")
    time.sleep(1)
    
    if not wait_and_click(COM_SERVER_IMAGE):
        return False
    time.sleep(3)

    print("Focusing search bar with Tab and typing...")
    pyautogui.press('tab', presses=2, interval=0.3)
    pyautogui.write(SERVER_NAME, interval=0.05)
    time.sleep(2)
    
    if not wait_and_click(REFRESH_IMAGE):
        return False
    time.sleep(2)

    if not find_and_click_specific(SERVER_NAME_IMAGE, prefer='bottom'): #'top' or 'bottom'
        return False
    time.sleep(1)

    if not wait_and_click(CONFIRM_JOIN_IMAGE):
        return False
    time.sleep(1)
    
    if not wait_and_click(CONFIRM_PASS_IMAGE):
        return False
    
    #Watch for join failure popup immediately
    if check_for_join_fail(timeout=15):
        print("Retrying join_server() after failure.")
        return join_server()

    #If no popup detected assume it succeeded
    return True

def main():
    print("Autojoin script running. Press ESC to stop.")
    while not keyboard.is_pressed(STOP_HOTKEY):
        success = join_server()
        if success:
            print("Join attempt successful or in progress.")
        else:
            print("Join attempt failed. Retrying...")
        for _ in range(RETRY_INTERVAL):
            if keyboard.is_pressed(STOP_HOTKEY):
                print("Stopped by user.")
                return
            time.sleep(1)

if __name__ == "__main__":
    main()
