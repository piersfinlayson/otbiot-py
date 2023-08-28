from gpio import Gpio

# List of dictionaries, each describing a GPIO for this device type.  Dictonary keys:
# - Gpio.DEVICE - String with name of device attached to this pin (may just be a text pin name if there is no specific device attached)
# - Gpio.HW_PIN - Hardware pin number for this pin (on a Raspberry Pi, we mean the Broadcom pin number).  Must be an integer (as it must be a number)
# - Gpio.MQTT_PIN - The name given to this PIN over MQTT.  Must be a string, as doesn't have to be number (for example A1).
GPIOS = [
    {
        Gpio.DEVICE:"pump",
        Gpio.HW_PIN:27,
        Gpio.MQTT_PIN:"5",
    },
]
