#!/usr/bin/python3

import sys, logging, time
from signal import signal,SIGINT
import RPi.GPIO as GPIO
from mqtt import Mqtt
from user_config import *

VERSION = 'otbiot-pi v0.0.1a'

MAIN_TIMER = 1
MAIN_LOOP_TIMEOUT = 30

global connected, run

logging.basicConfig(
  level=logging.DEBUG,
    format="[%(asctime)s.%(msecs)03d] [%(levelname)-8s] %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    stream=sys.stdout,
  )
logger=logging.getLogger('main')

def exit():
    global run
    run = False

def get_gpio(mqtt_pin):
    for gpio in GPIOS:
        if gpio[MQTT_PIN] == mqtt_pin:
            return gpio
    return None

def on_message(mqtt, user_data, payload):
    logger.info("MQTT message received: %s" % payload)
    words = payload.split(':')
    if words[0] == 'gpio':
        if len(words) > 1:
            if words[1] in ('get', 'set'):
                if len(words) > 2:
                    gpio = get_gpio(words[2])
                    if gpio:
                        bcm_pin = gpio[BCM_PIN]
                        if words[1] == 'get':
                            logger.info("Get state of BCM pin %d" % bcm_pin)
                            state = GPIO.input(bcm_pin)
                            if state:
                                val = 1
                            else:
                                val = 0
                            mqtt.publish('gpio:get:ok:%d' % val)
                        else:
                            assert(words[1] == 'set')
                            if len(words) > 3:
                                if words[3] == '1':
                                    state = GPIO.HIGH
                                elif words[3] == '0':
                                    state = GPIO.LOW
                                else:
                                    logger.error("Unknown requested gpio state %s" % words[3])
                                    state = None
                                if state != None:
                                    logger.info("Set state of BCM pin %d to %s" % (bcm_pin, words[3]))
                                    GPIO.output(bcm_pin, state)
                                    mqtt.publish(':'.join((words[0],words[1],'ok')))
                                else:
                                    logger.warning("Received unexpected gpio set request: %s" % payload)
                            else:
                                logger.warning("Received malformed gpio request: %s" % payload)
                    else:
                        logger.warning("Received request for unknown GPIO %s" % payload)
                else:
                    logger.warning("Received malformed gpio request: %s" % payload)
            else:
                logger.warning("Received malformed gpio request: %s" % payload)
        else:
            logger.warning("Received malformed gpio request: %s" % payload)
    elif words[0] == 'version':
        if (len(words) > 1) and words[1] == 'get':
            mqtt.publish(':'.join((words[0], VERSION)))
        else:
            logger.warning("Received malformed version request: %s" % payload)
    elif words[0] == 'ping':
        logger.info("Received ping request - respond with pong")
        mqtt.publish('pong')
    elif words[0] in ('reset', 'reboot', 'restart', 'exit', 'quit'):
        logger.error("Exiting due to MQTT command")
        exit()
    else:
        logger.warning("Unknown MQTT message received %s" % payload)

def on_disconnect(userdata, rc):
    logger.error("MQTT disconnected - exiting")
    exit()

def setup_gpios():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  for gpio in GPIOS:
    GPIO.setup(gpio[BCM_PIN], GPIO.OUT)
    logger.info("Set GPIO %d for device %s to output" % (gpio[BCM_PIN], gpio[DEVICE]))

def signal_handler(signal_received, frame):
    logger.error("SIGINT caught - exiting")
    exit()

def main():
    global connected, run
    logger.setLevel(logging.INFO)
    logger.info("Started")
    signal(SIGINT, signal_handler)
    setup_gpios()
    connected = False
    mqtt = Mqtt(MQTT_ADDR, MQTT_PORT, CHIP_IDS)
    mqtt.connect(None, on_disconnect, on_message)
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