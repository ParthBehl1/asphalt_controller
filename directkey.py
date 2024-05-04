import time
from Quartz import CGEventCreateKeyboardEvent, CGEventPost, kCGEventKeyDown, kCGEventKeyUp
from Quartz import kCGEventFlagMaskCommand

def press_key(key_code):
    key_event = CGEventCreateKeyboardEvent(None, key_code, True)
    CGEventPost(kCGEventKeyDown, key_event)

def release_key(key_code):
    key_event = CGEventCreateKeyboardEvent(None, key_code, False)
    CGEventPost(kCGEventKeyUp, key_event)

if __name__ == '__main__':
    # Define key codes for macOS
    W = 13
    A = 0
    S = 1
    D = 2
    Space = 49

    # Example usage
    press_key(W)
    time.sleep(1)
    release_key(W)
    time.sleep(1)