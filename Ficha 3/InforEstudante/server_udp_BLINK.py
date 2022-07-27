#!/usr/bin/env python3
import sys
import socket
import pigpio
import time

def setup():
    # Configure PiGPIO and the LED's GPIO pin
    global pi, LedPin
    LedPin = 17
    pi = pigpio.pi()  # create an instance of PiGPIO and assign it to pi variable

    pi.set_mode(LedPin, pigpio.OUTPUT)  # configure GPIO pin LedPin to be an output pin
                                        # we want to use that pin to control something
                                        # connected to it from our Python code - in this example a LED

def runBlink():
    while True:
        # As the loop executes, we are toggling GPIO pin LedPin, our output pin, on and off
        print ('...LED ON')
        # Turn on LED
        pi.write(LedPin, 1) # 1 = High = On
        time.sleep(1)
        print ('LED OFF...')
        # Turn off LED
        pi.write(LedPin, 0) # 0 = Low = Off
        time.sleep(1)

# Define a destroy function for clean up everything after the script finished
def destroy():

    ## 1 - INSERT CODE HERE:
    ## COMPLETE THE CODE TO TURN OFF THE LED AND CLOSE THE SOCKET

def main():
    global ServerSocket

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host, port = sys.argv[1], int(sys.argv[2])

    ## 2 - INSERT CODE HERE:
    ## COMPLETE THE CODE TO RECEIVE THE MESSAGE FROM CLIENT USING SOCKETS
    ## IF MESSAGE RECEIVED IS 'BLINK' THE LED IN THE BOARD MUST BLINK

    
#
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
    except KeyboardInterrupt:
        print("\nCaught keyboard interrupt, exiting")
    finally:
        destroy()
