MY_CHIP_ID = 'd76a7d'
CHIP_IDS = [MY_CHIP_ID, 'all'] # MY_CHIP_ID must be first
MQTT_ADDR = "mosquitto"
MQTT_PORT = 1883

# Use BCM pin numbers
DEVICE="device"
BCM_PIN="pin"
MQTT_PIN="mqtt_pin"
GPIOS = [
    {
        DEVICE:"pump",
        BCM_PIN:27,
        MQTT_PIN:"5",
    },
]