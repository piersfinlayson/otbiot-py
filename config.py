# Configuration for this type of hardware
from config_device_type import *

# Configuration for this specific otbiot deployment
from config_deployment import *

# Configuration for this specific device
from config_device import *

# List of chip IDs this device listens for messages for via MQTT.  DEVICE_CHIP_IP must always be first, as this is how otbiot knows this device's actual chip ID
CHIP_IDS = [DEVICE_CHIP_ID, 'all']
