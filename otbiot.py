#!/usr/bin/python3

import sys, logging, time
from signal import signal, SIGINT
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from user_config import *

VERSION = 'otbiot-pi v0.0.1a'

MQTT_TOPIC_SYSTEM = "/otb_iot/%s/system"
MQTT_TOPIC_STATUS = "/otb_iot/%s/status"
MQTT_TOPICS = [
    MQTT_TOPIC_SYSTEM,
]
MQTT_CONNECT_TIMEOUT = 60
MAIN_TIMER = 1

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

def mqtt_publish(mqtt_client, message):
    topic = MQTT_TOPIC_STATUS % MY_CHIP_ID
    logger.info("Publish MQTT %s %s" % (topic, message))
    mqtt_client.publish(topic, message)

def on_message(mqtt_client, user_data, msg):
    payload = str(msg.payload, 'utf-8')
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
                            mqtt_publish(mqtt_client, 'gpio:get:ok:%d' % val)
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
                                    mqtt_publish(mqtt_client, ':'.join((words[0],words[1],'ok')))
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
            mqtt_publish(mqtt_client, ':'.join((words[0], VERSION)))
        else:
            logger.warning("Received malformed version request: %s" % payload)
    elif words[0] == 'ping':
        logger.info("Received ping request - respond with pong")
        mqtt_publish(mqtt_client, 'pong')
    elif words[0] in ('reset', 'reboot', 'restart', 'exit', 'quit'):
        logger.error("Exiting due to MQTT command")
        exit()
    else:
        logger.warning("Unknown MQTT message received %s" % payload)

def on_connect(mqtt_client, userdata, flags, rc):
    global connected
    logger.info("MQTT connected")
    for id in CHIP_IDS:
        for topic in MQTT_TOPICS:
            topic = topic % id
            logger.info("Subscribe to topic %s" % topic)
            mqtt_client.subscribe(topic)
    mqtt_publish(mqtt_client, 'booted:slot:0')
    connected = True

def on_disconnect(mqtt_client, userdata, rc):
    logger.error("MQTT disconnected - exiting")
    exit()

def mqtt_client_connect():
    mqtt_client = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.connect_async(MQTT_ADDR, MQTT_PORT, MQTT_CONNECT_TIMEOUT)
    mqtt_client.loop_start()
    return mqtt_client

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
    mqtt_client = mqtt_client_connect()
    run = True
    counter = 0
    while True:
        time.sleep(MAIN_TIMER)
        counter += 1
        if not connected and ((counter * MAIN_TIMER) > MQTT_CONNECT_TIMEOUT):
            logger.error("Failed to connect to MQTT broker in %d seconds - exiting" % MQTT_CONNECT_TIMEOUT)
            exit()
        if not run:
            logger.info("Main thread - have been instructed to exit, so exiting")
            sys.exit(0)
    
if __name__ == "__main__":
    main()