import cv2
import mss
import numpy
import time
import win32api, win32con
import sys, ctypes

# Check whether the key is pressed
def is_key_pressed(key):
    return ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000 != 0

# Sleep function with the possibility to exit
# Delays are essential in this code! They should not be neglected!
def sleep_key(sec):
    start_time = time.time()
    
    while True:
        # Key pressed during the loop? - exit the entire program
        if is_key_pressed(exit_key):
            sys.exit()
        
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        # If the time has run out, exit the loop
        if elapsed_time >= sec:
            break

# This function moves the cursor to x,y position
def move(x,y):
    win32api.SetCursorPos((x,y))

# Left/right dash
def click(pos):
    if pos: # left -> right
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    else: # right -> left
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


def main():
    # Reading the image
    plank = cv2.imread(r'Assets\1920\candy_cutttt.png', 0)

    mss_ = mss.mss()

    # The threshold for detecting the plank
    threshold = 0.987

    # We always spawn on the left side of the 'tree'
    # True = left position, False = right position
    position = True

    # Inf. loop till exit key is pressed
    while not(is_key_pressed(exit_key)):

        # If left pos. grab left field else right one
        if position:
            screenshot = numpy.array(mss_.grab(left_field))
        else:
            screenshot = numpy.array(mss_.grab(right_field))

        # RGB -> Gray
        screenshot_r = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

        plank_match = cv2.matchTemplate(screenshot_r,
                                plank,
                                cv2.TM_CCOEFF_NORMED)

        _, max_val, _, _ = cv2.minMaxLoc(plank_match)

        print(max_val, position)

        if max_val > threshold: # FOUND!
            # Need to dash
            click(position)

            print('turn!')

            sleep_key(0.055)

            # Double click is always safe to do (slight optimisation)
            click(position)

            # We've moved to the opposite side
            position = not position
        else:
            # Basicaly, cut the log without changing position
            click(not position)
        
        # Show "computer sight"
        cv2.imshow('TimberBot', screenshot_r)
        cv2.waitKey(1)

        sleep_key(0.052)


if __name__ == '__main__':
    
    # Constants
    # Defining the "computer sight" areas
    area_height = 175
    area_width = 32
    area_from_top = 775

    # The sight of the computer's left eye
    left_field = {'left': 2337,
             'top': area_from_top,
             'width': area_width,
             'height': area_height}
    
    # The sight of the computer's right eye
    right_field = {'left': 2585,
             'top': area_from_top,
             'width': area_width,
             'height': area_height}

    # Q as default. To change:
    # https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    exit_key = 0x51

    # Press Q to start
    while not(is_key_pressed(exit_key)):
        pass

    # Instantly release the button
    win32api.keybd_event(exit_key, 0, win32con.KEYEVENTF_KEYUP, 0)

    # Run the code
    main()