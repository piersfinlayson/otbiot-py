# MQTT commands fulfilled by this method aren't supported by otbiot as they can be handled by the OS (at least on Raspberry Pi)
def cmd_os_unsupported(otbiot, words_iter, words) -> (bool, str):
    otbiot.mqtt.publish('unsupported_use_os')
    return True, ""

