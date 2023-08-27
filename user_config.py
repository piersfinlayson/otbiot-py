from gpio import Gpio

MY_CHIP_ID = 'd76a7d'
CHIP_IDS = [MY_CHIP_ID, 'all'] # MY_CHIP_ID must be first
MQTT_ADDR = "mosquitto"
MQTT_PORT = 1883

# Use BCM pin numbers
GPIOS = [
    {
        Gpio.DEVICE:"pump",
        Gpio.BCM_PIN:27,
        Gpio.MQTT_PIN:"5",
    },
]