#!/usr/bin/python3

import sys, logging, time
from signal import signal,SIGINT
from mqtt import Mqtt
from gpio import Gpio
from user_config import *

VERSION = 'otbiot-pi v0.0.1a'

MAIN_TIMER = 0.1
MAIN_LOOP_TIMEOUT = 30

global connected, run, otbiot

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

def exit():
    global run
    run = False

def on_connect(mqtt, user_data, flags, rc):
    logger.info("MQTT Connected")
    mqtt.publish("booted:slot:0")

def on_message(mqtt, user_data, payload):
    global otbiot
    logger.info("MQTT message received: %s" % payload)
    words = payload.split(':')
    error = True
    if words[0] == 'gpio':
        if len(words) > 1:
            if words[1] in ('get', 'set'):
                if len(words) > 2:
                    if words[1] == 'get':
                        val = otbiot.gpio.get_gpio_state_from_mqtt(words[2])
                        if val != None:
                            mqtt.publish('gpio:get:ok:%d' % val)
                            error = False
                        else:
                            logger.warning("Received get for unknown GPIO %s" % payload)
                    else:
                        assert(words[1] == 'set')
                        if len(words) > 3:
                            rc = otbiot.gpio.set_gpio_state_from_mqtt(words[2], words[3])
                            if rc:
                                mqtt.publish(':'.join((words[0],words[1],'ok')))
                                error = False
                            else:
                                logger.warning("Received get for unknown GPIO %s" % payload)
                        else:
                            logger.warning("Received malformed gpio set request: %s" % payload)
                else:
                    logger.warning("Received malformed gpio request: %s" % payload)
            else:
                logger.warning("Received malformed gpio request: %s" % payload)
        else:
            logger.warning("Received malformed gpio request: %s" % payload)
    elif words[0] == 'version':
        if (len(words) > 1) and words[1] == 'get':
            mqtt.publish(':'.join((words[0], VERSION)))
            error = False
        else:
            logger.warning("Received malformed version request: %s" % payload)
    elif words[0] == 'ping':
        logger.info("Received ping request - respond with pong")
        mqtt.publish('pong')
        error = False
    elif words[0] in ('reset', 'reboot', 'restart', 'exit', 'quit'):
        logger.error("Exiting due to MQTT command")
        mqtt.publish('ok:%s' % words[0])
        error = False
        exit()
    else:
        logger.warning("Unknown MQTT message received %s" % payload)
    if error:
        mqtt.publish('error:%s' % payload)

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
    logger.info("Started")
    
    # Set up signal handling
    signal(SIGINT, signal_handler)

    # Set up GPIOs
    gpio = Gpio(GPIOS)
    connected = False
    
    # Set up MQTT
    mqtt = Mqtt(MQTT_ADDR, MQTT_PORT, CHIP_IDS)
    mqtt.connect(on_connect, on_disconnect, on_message)
    
    # Set up otbiot object, used to access stuff like GPIOs from other method (as a global)
    otbiot = Otbiot(mqtt, gpio)
    
    # Run the main loop, checking if we should exit, as only main thread can exit
    run = True
    counter = 0
    while True:
        time.sleep(MAIN_TIMER)
        counter += 1
        if not mqtt.connected and ((counter * MAIN_TIMER) > MAIN_LOOP_TIMEOUT):
            logger.error("Failed to connect to MQTT broker in %d seconds - exiting" % MAIN_LOOP_TIMEOUT)
            exit()
        if not run:
            logger.info("Main thread - have been instructed to exit, so exiting")
            sys.exit(0)
    
if __name__ == "__main__":
    main()
    