#!/usr/bin/python3

import sys, logging, time
from signal import signal,SIGINT
from mqtt import Mqtt
from gpio import Gpio
from config import *
from cmd_tree import otbiot_cmd_tree
from system import exit, start, running
from defines import VERSION

MAIN_TIMER = 0.1
MAIN_LOOP_TIMEOUT = 30

global otbiot

logging.basicConfig(
  level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] [%(levelname)-8s] %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    stream=sys.stdout,
  )

logger=logging.getLogger('main')

class Otbiot:
    def __init__(self, mqtt, gpio):
        self.mqtt = mqtt
        self.gpio = gpio

def on_connect(mqtt, user_data, flags, rc):
    logger.info("MQTT Connected")
    mqtt.publish("booted:slot:0")

def on_message(mqtt, user_data, payload):
    global otbiot
    logger.info("MQTT message received: %s" % payload)
    
    # Find who handles this message
    words = payload.split(':')
    words_iter = iter(words)
    branch = otbiot_cmd_tree
    error = True
    handler = None
    try:
        while not handler:
            word = words_iter.__next__()
            if word in branch:
                next_branch = branch[word]
                if type(next_branch) != dict:
                    handler = next_branch
                else:
                    branch = next_branch
    except StopIteration:
        pass

    # Handle it
    if handler:
        logger.debug("Passing msg %s to handler %s" % (payload, str(handler)))
        rc, error_str = handler(otbiot, words_iter, words)
        if rc:
            error = False
        else:
            logger.warning("Handler returned an error %s" % error_str)
    else:
        logger.warning("Unknown MQTT message received %s" % payload)
        error = True
        error_str = 'unknown_mqtt_command'
    if error:
        mqtt.publish('error:%s:%s' % (payload, error_str))

def on_disconnect(userdata, rc):
    logger.error("MQTT disconnected - exiting")
    exit()

def signal_handler(signal_received, frame):
    logger.error("SIGINT caught - exiting")
    exit()

def main():
    # Globals
    global connected, run, otbiot
    
    # Set up logging
    logger.setLevel(logging.INFO)
    logger.info("otbiot-py version %s started on device %s" % (VERSION, DEVICE_CHIP_ID))
    
    # Set up signal handling
    signal(SIGINT, signal_handler)

    # Set up GPIOs
    gpio = Gpio(GPIOS)
    
    # Set up MQTT
    mqtt = Mqtt(MQTT_ADDR, MQTT_PORT, CHIP_IDS)
    mqtt.connect(on_connect, on_disconnect, on_message)
    
    # Set up otbiot object, used to access stuff like GPIOs from other method (as a global)
    otbiot = Otbiot(mqtt, gpio)
    
    # Run the main loop, checking if we should exit, as only main thread can exit
    start()
    run = True
    counter = 0
    while True:
        time.sleep(MAIN_TIMER)
        counter += 1
        if not mqtt.connected and ((counter * MAIN_TIMER) > MAIN_LOOP_TIMEOUT):
            logger.error("Failed to connect to MQTT broker in %d seconds - exiting" % MAIN_LOOP_TIMEOUT)
            exit()
        if not running():
            logger.info("Main thread has been instructed to exit, so exiting")
            sys.exit(0)
    
if __name__ == "__main__":
    main()
    