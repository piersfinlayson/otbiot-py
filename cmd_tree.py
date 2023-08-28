from gpio import (
    cmd_gpio_get,
    cmd_gpio_set,
)
from mqtt import (
    cmd_mqtt_get_server,
    cmd_mqtt_get_port,
    cmd_mqtt_get_user,
    cmd_mqtt_get_password
)
from system import (
    cmd_system_get_version,
    cmd_system_ping,
    cmd_system_reset,
)
from os_handler import (
    cmd_os_unsupported,
)

otbiot_cmd_tree = {
    'gpio': {
        'get': cmd_gpio_get,
        'set': cmd_gpio_set,
    },
    'get': {
#        'sensor': {
#                'temp': {
#                    'ds18b20': {
#                        'num': ds18b20_get_num,
#                        'value':ds18b20_get_value,
#                        'addr':da18b20_get_addr,
#                    },
#                },
#                'adc': {
#                    'ads': ads_get,
#                } ,
#        },
        'gpio': cmd_gpio_get,
        'config': {
#            'all':config_get_all,
#            'gpio': {
#                'pin': {
#                    'state':config_get_gpio_pin_state,
#                }
#            },
            'serial': {
                'enable':cmd_os_unsupported,
                'rx':cmd_os_unsupported,
                'rx_pin':cmd_os_unsupported,
                'rxpin':cmd_os_unsupported,
                'tx':cmd_os_unsupported,
                'tx_pin':cmd_os_unsupported,
                'txpin':cmd_os_unsupported,
                'baud':cmd_os_unsupported,
                'baudrate':cmd_os_unsupported,
                'baud_rate':cmd_os_unsupported,
                'bit_rate':cmd_os_unsupported,
                'bitrate':cmd_os_unsupported,
                'speed':cmd_os_unsupported,
                'stopbit':cmd_os_unsupported,
                'stop_bit':cmd_os_unsupported,
                'parity':cmd_os_unsupported,
                'mezz': {
                    'uart':cmd_os_unsupported,
                },
            },
        },
        'wifi': {
            'ssid':cmd_os_unsupported,
            'password':cmd_os_unsupported,
            'pass':cmd_os_unsupported,
        },
        'version': cmd_system_get_version,
        'mqtt': {
            'server':cmd_mqtt_get_server,
            'addr':cmd_mqtt_get_server,
            'address':cmd_mqtt_get_server,
            'host':cmd_mqtt_get_server,
            'svr':cmd_mqtt_get_server,
            'port':cmd_mqtt_get_port,
            'username':cmd_mqtt_get_user,
            'user':cmd_mqtt_get_user,
            'password':cmd_mqtt_get_password,
            'pass':cmd_mqtt_get_password,
        }
    },
    'set': {
        'gpio': cmd_gpio_set,
    },
    'version': {
        'get': cmd_system_get_version,
    },
    'trigger':{
        'ping':cmd_system_ping,
        'reset':cmd_system_reset,
        'reboot':cmd_system_reset,
        'restart':cmd_system_reset,
        'reboot':cmd_system_reset,
        'exit':cmd_system_reset,
        'quit':cmd_system_reset,
    },
    'ping':cmd_system_ping,
    'reset':cmd_system_reset,
    'reboot':cmd_system_reset,
}
