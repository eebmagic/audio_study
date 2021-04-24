import os
import time
import re
from pynput import mouse
from pynput.keyboard import Key, Listener
f=open('maniac1.txt','a')

inc=1
#f.write('<mouse_new>\n')
from pynput import keyboard

def smartPrint(value):
    print(value)
    f.write(value + '\n')

def on_press(key):
    # print(f'key press {key} | {time.time()}')
    smartPrint(f'key press {key} | {time.time()}')

    # Listen for stop key
    try:
        if key.char == '0':
            pass
            # print("STOPPING KEYBOARD LISTENER")
            # return False
    except:
        pass

def on_release(key):
    # print(f'key release {key} | {time.time()}')
    smartPrint(f'key release {key} | {time.time()}')

key_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
key_listener.start()


# Vars to limit mouse position rate
last = 0
thresh = 1/20
def on_move(x, y):
    global last, thresh
    if (time.time() - last) >= thresh:
        # print(f'mouse at {x, y} | {time.time()}')
        smartPrint(f'mouse at {x, y} | {time.time()}')
        last = time.time()

def on_click(x, y, button, pressed):
    f=open('maniac1.txt','a')
    if button == mouse.Button.left:
        # print (f'Left mouse {"pressed" if pressed else "released"} | {time.time()}')
        smartPrint (f'Left mouse {"pressed" if pressed else "released"} | {time.time()}')
        #f.write('left\n')

    if button == mouse.Button.right:
        key_listener.stop()
        # print (f'right mouse {"pressed" if pressed else "released"} | {time.time()}')
        smartPrint (f'right mouse {"pressed" if pressed else "released"} | {time.time()}')
        #f.write('right\n')

    if button == mouse.Button.middle:
        # print (f'middle mouse {"pressed" if pressed else "released"} | {time.time()}')
        smartPrint (f'middle mouse {"pressed" if pressed else "released"} | {time.time()}')
        #f.write('middle\n')

        print("STOPPING MOUSE LISTENER")
        return False

with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
    try:
        listener.join()
    except MyException as e:
        print('Done'.format(e.args[0]))

f.close()
