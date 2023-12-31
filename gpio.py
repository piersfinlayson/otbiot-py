
import logging
import RPi.GPIO as GPIO

logger=logging.getLogger('mqtt')

GPIO_DEVICE="device"
GPIO_HW_PIN="pin"
GPIO_MQTT_PIN="mqtt_pin"

class Gpio:
    DEVICE="device"
    HW_PIN="pin"
    MQTT_PIN="mqtt_pin"

    def __init__(self, gpios):
        self.gpios=gpios
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for gpio in self.gpios:
            GPIO.setup(gpio[self.HW_PIN], GPIO.OUT)
            logger.info("Set GPIO %d, MQTT %s for device %s to output" % (gpio[self.HW_PIN], gpio[self.MQTT_PIN], gpio[self.DEVICE]))
            
    def _get_hw_gpio_from_mqtt(self, mqtt_gpio):
        for gpio in self.gpios:
            if gpio[self.MQTT_PIN] == mqtt_gpio:
                return gpio[self.HW_PIN]
        logger.info("Failed to find MQTT GPIO %s" % mqtt_gpio)
        return None
    
    def get_gpio_state_from_mqtt(self, mqtt_gpio):
        HW_PIN = self._get_hw_gpio_from_mqtt(mqtt_gpio)
        rc = None
        if HW_PIN != None:
            state = GPIO.input(HW_PIN)
            if state:
                rc = 1
            else:
                rc = False
        logger.info("Get state of HW pin %s %s" % (str(HW_PIN), str(rc)))
        return rc
                
    def set_gpio_state_from_mqtt(self, mqtt_gpio, mqtt_state):
        HW_PIN = self._get_hw_gpio_from_mqtt(mqtt_gpio)
        if mqtt_state == '1':
            desired_state = GPIO.HIGH
        elif mqtt_state == '0':
            desired_state = GPIO.LOW
        else:
            logging.info("Invalid GPIO state requested %s" % mqtt_state)
            desired_state = None
        rc = None
        if HW_PIN != None and desired_state != None:
            logger.info("Set state of HW pin %d to %s" % (HW_PIN, desired_state))
            GPIO.output(HW_PIN, desired_state)
            rc = True
        return rc
            
def cmd_gpio_get(otbiot, words_iter, words) -> (bool, str):
    rc = False
    error_str = "unknown_error"
    
    try:
        pin = words_iter.__next__()
    except:
        return False, "invalid_get_gpio_command"

    val = otbiot.gpio.get_gpio_state_from_mqtt(pin)
    if val != None:
        otbiot.mqtt.publish('gpio:get:ok:%d' % val)
        rc = True
    else:
        logger.warning("Received get for unknown GPIO %s" % ':'.join(words))
        rc = False
        error_str = "unknown_gpio"
    
    return rc, error_str

def cmd_gpio_set(otbiot, words_iter, words) -> (bool, str):
    rc = False
    error_str = "unknown_error"
    
    try:
        pin = words_iter.__next__()
        state = words_iter.__next__()
    except:
        return False, "invalid_set_gpio_command"

    rc = otbiot.gpio.set_gpio_state_from_mqtt(pin, state)
    if rc:
        otbiot.mqtt.publish(':'.join((words[0],words[1],'ok')))
    else:
        logger.warning("Received set for unknown GPIO or invalid state%s " % ':'.join(words))
        error_str
   
    return rc, error_str
