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

otbiot_cmd_tree = {
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
#        'config': {
#            'all':config_get_all,
#            'gpio': {
#                'pin': {
#                    'state':config_get_gpio_pin_state,
#                }
#            },
#            'serial': {
#                'enable':,
#                'rx':,
#                'rx_pin':,
#                'rxpin':,
#                'tx':,
#                'tx_pin':,
#                'txpin':,
#                'baud':,
#                'baudrate':,
#                'baud_rate':,
#                'bit_rate':,
#                'bitrate':,
#                'speed':,
#                'stopbit':,
#                'stop_bit':,
#                'parity':,
#                'mezz': {
#                    'uart':,
#                },
#            },
#        'wifi': {
#            'ssid':,
#            'password':,
#            'pass':,
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
    'ping':cmd_system_ping,
    'reset':cmd_system_reset,
    'restart':cmd_system_reset,
    'reboot':cmd_system_reset,
    'exit':cmd_system_reset,
    'quit':cmd_system_reset,
}
