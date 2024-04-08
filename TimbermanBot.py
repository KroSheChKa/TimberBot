import cv2
import mss
import numpy
import time
import win32api, win32con
import sys, ctypes

# Check whether the key is pressed
def is_key_pressed(key):
    return ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000 != 0

def sleep_key(sec, key_code = 0x51):
    start_time = time.time()
    
    while True:
        # Key pressed during the loop? - exit the entire program
        if is_key_pressed(key_code):
            sys.exit()
        
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        # If the time has run out, exit the loop
        if elapsed_time >= sec:
            break

# This function moves the cursor to x,y position
def move(x,y):
    win32api.SetCursorPos((x,y))

def click(pos):
    if pos: # left -> right
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    else: # right -> left
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def main():
    plank = cv2.imread(r'Assets\1920\candy_cutttt.png', 0)

    mss_ = mss.mss()

    left_field = {'left': 2337,
             'top': 775,
             'width': 32,
             'height': 175}
    
    right_field = {'left': 2585,
             'top': 775,
             'width': 32,
             'height': 175}

    threshold = 0.987

    position = True # left
    while not(is_key_pressed(0x51)):

        if position: # if left grab left field
            screenshot = numpy.array(mss_.grab(left_field))
        else:
            screenshot = numpy.array(mss_.grab(right_field))

        screenshot_r = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

        plank_match = cv2.matchTemplate(screenshot_r,
                                plank,
                                cv2.TM_CCOEFF_NORMED)

        _, max_val, _, _ = cv2.minMaxLoc(plank_match)

        print(max_val, position)

        if max_val > threshold: # FOUND!
            # need to jump off
            click(position)
            print('turn!')
            sleep_key(0.055)
            click(position)
            position = not position
        else:
            click(not position)
        
        cv2.imshow('Footbot', screenshot_r)
        cv2.waitKey(1)

        sleep_key(0.052)


if __name__ == '__main__':
    # Press Q to start
    while not(is_key_pressed(0x51)):
        pass

    win32api.keybd_event(0x51, 0, win32con.KEYEVENTF_KEYUP, 0)
    
    main()
