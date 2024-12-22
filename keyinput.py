import pydirectinput
import time


def press_key(key):
    pydirectinput.keyDown(key)
    time.sleep(0.1)  
    pydirectinput.keyUp(key)

def release_keys(keys):
    for key in keys:
        pydirectinput.keyUp(key)
