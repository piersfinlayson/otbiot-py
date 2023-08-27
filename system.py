from defines import VERSION

global run

def exit():
    global run
    run = False

def start():
    global run
    run = True
    
def running():
    global run
    return run

def cmd_system_get_version(otbiot, words_iter, words) -> (bool, str):
    otbiot.mqtt.publish(':'.join((words[0], VERSION)))
    return True, ""

def cmd_system_ping(otbiot, words_iter, words) -> (bool, str):
    otbiot.mqtt.publish('pong')
    return True, ""

def cmd_system_reset(otbiot, words_iter, words) -> (bool, str):
    otbiot.mqtt.publish('ok:%s' % words[0])
    exit()
    return True, ""
