import ctypes
import time
import random

# Constants for mouse event
MOUSEEVENTF_MOVE = 0x0001

def move_mouse():
    # Get the current mouse position
    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    
    # Move the mouse slightly
    x = cursor.x + random.randint(-1, 1)
    y = cursor.y + random.randint(-1, 1)
    ctypes.windll.user32.SetCursorPos(x, y)

def keep_awake():
    print("Press Ctrl+C to stop the script.")
    try:
        while True:
            move_mouse()
            time.sleep(60)  # Move the mouse every 60 seconds
    except KeyboardInterrupt:
        print("Script stopped.")

if __name__ == "__main__":
    keep_awake()