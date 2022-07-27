"""
File: dweet_led.py
A Python program to control an LED using the public dweet.io service.
Dependencies:
  pip3 install gpiozero pigpio requests
Built and tested with Python 3.9 on Raspberry Pi 2 Model B
"""
import signal
import json
import os
import sys
import logging
from gpiozero import Device, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from uuid import uuid1
import requests                                                                    


# Global Variables
LED_GPIO_PIN = 17                   # GPIO Pin that LED is connected to
THING_NAME_FILE = 'thing_name.txt'  # The name of our "thing" is persisted into this file
URL = 'https://dweet.io'            # Dweet.io service API
last_led_state = None               # Current state of LED ("on", "off", "blinking")
thing_name = None                   # Thing name (as persisted in THING_NAME_FILE)
led = None                          # GPIOZero LED instance


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO)  # Debugging for this file.                           


# Initialize GPIO
Device.pin_factory = PiGPIOFactory()


# Function Definitions
def init_led():
    """Create and initialise an LED Object"""
    global led
    led = LED(LED_GPIO_PIN)
    led.off()


def resolve_thing_name(thing_file):
    """Get existing, or create a new thing name"""
    if os.path.exists(thing_file):                                                 
        with open(thing_file, 'r') as file_handle:
            name = file_handle.read()
            logger.info('Thing name ' + name + ' loaded from ' + thing_file)
            return name.strip()
    else:
        name = str(uuid1())[:8]  # UUID object to string.                          
        logger.info('Created new thing name ' + name)

        with open(thing_file, 'w') as f:                                           
            f.write(name)

    return name


def get_latest_dweet():
    """Get the last dweet made by our thing."""
    resource = URL + '/get/latest/dweet/for/' + thing_name                         
    logger.debug('Getting last dweet from url %s', resource)

    r = requests.get(resource)                                                     

    if r.status_code == 200:                                                       
        dweet = r.json()  # return a Python dict.
        logger.debug('Last dweet for thing was %s', dweet)

        dweet_content = None

        if dweet['this'] == 'succeeded':                                           
            # We're just interested in the dweet content property.
            dweet_content = dweet['with'][0]['content']                            

        return dweet_content

    else:
        logger.error('Getting last dweet failed with http status %s', r.status_code)
        return {}


def poll_dweets_forever(delay_secs=2):
    """Poll dweet.io for dweets about our thing."""
    while True:
        dweet = get_latest_dweet()                                                 
        if dweet is not None:
            process_dweet(dweet)                                                   

            sleep(delay_secs)                                                      


def process_dweet(dweet):
    """Inspect the dweet and set LED state accordingly"""
    global last_led_state

    if not 'state' in dweet:
        return

    led_state = dweet['state']

    if led_state == last_led_state:                                                
        return  # LED is already in requested state.

    if led_state == 'on':                                                          
        #UPDATE LED STATUS
    elif led_state == 'blink':
        #UPDATE LED STATUS
    else:  # Off, including any unhandled state.
        #UPDATE led_state VARIABLE
        #UPDATE LED STATUS

    if led_state != last_led_state:                                                
        #UPDATE THE LAST LED STATE WITH CURRENT LED STATE
        logger.info('LED ' + led_state)


def print_instructions():
    """Print instructions to terminal."""
    print("LED Control URLs - Try them in your web browser:")
    print("  On    : " + URL + "/dweet/for/" + thing_name + "?state=on")
    print("  Off   : " + URL + "/dweet/for/" + thing_name + "?state=off")
    print("  Blink : " + URL + "/dweet/for/" + thing_name + "?state=blink\n")


def signal_handler(sig, frame):
    """Release resources and clean up as needed."""
    print('You pressed Control+C')
    led.off()
    sys.exit(0)


# Initialise Module
thing_name = resolve_thing_name(THING_NAME_FILE)
init_led()


# Main entry point
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # Capture CTRL + C
    print_instructions()                                                           

    # Initialise LED from last dweet.
    last_dweet = get_latest_dweet()                                                
    if (last_dweet):
        process_dweet(last_dweet)

    print('Waiting for dweets. Press Control+C to exit.')
    # Only use one of the following. See notes later in Chapter.
    # stream_dweets_forever() # Stream dweets real-time.
    poll_dweets_forever()  # Get dweets by polling a URL on a schedule.            