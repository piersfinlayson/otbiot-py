import logging
import paho.mqtt.client as mqtt

logger=logging.getLogger('mqtt')

MQTT_CONNECT_DEFAULT_TIMEOUT = 60
MQTT_TOPIC_STATUS = "/otb_iot/%s/status"
MQTT_TOPIC_SYSTEM = "/otb_iot/%s/system"
MQTT_TOPICS_SUBSCRIBE = [
    MQTT_TOPIC_SYSTEM,
]

class Mqtt:
    def __init__(self, addr, port, chip_ids, username=None, password=None, topics=None):
        self.addr=addr
        self.port=port
        self.chip_ids=chip_ids
        self.username=username
        self.password=password
        self.topics=None
        if topics == None:
            topics = MQTT_TOPICS_SUBSCRIBE
        self.client=mqtt.Client(mqtt.MQTTv31)
        self.connected = False

    def connect(self, on_connect=None, on_disconnect=None, on_message=None, timeout=MQTT_CONNECT_DEFAULT_TIMEOUT):
        logger.debug("Mqtt: connect: %s" % self)
        self.on_connect=on_connect
        self.on_disconnect=on_disconnect
        self.on_message=on_message
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.connect_async(self.addr, self.port, timeout)
        self.client.loop_start()

    def __str__(self):
        return "Mqtt addr: %s port: %d" % (self.addr, self.port)

    def _on_connect(self, client, userdata, flags, rc):
        logger.debug("Mqtt: _on_connect: %s" % self)
        self.connected = True
        for id in self.chip_ids:
            for topic in self.topics:
                topic = topic % id
                logger.info("Mqtt: Subscribe to topic %s" % topic)
                self.client.subscribe(topic)

        if self.on_connect:
            self.on_connect(self, userdata, flags, rc)

    def _on_disconnect(self, client, userdata, rc):
        logger.debug("Mqtt: _on_disconnect: %s" % self)
        self.connected = False
        if self.on_disconnect:
            self.on_disconnect(self, userdata, userdata, rc)

    def _on_message(self, client, userdata, msg):
        logger.debug("Mqtt: _on_message: %s : %s" % (self, msg))
        if self.on_message:
            self.on_message(self, userdata, str(msg.payload, 'utf-8'))

    def publish(self, msg, topic=None):
        logger.debug("Mqtt: publish: %s : %s" % (self, msg))
        if not topic:
            topic = MQTT_TOPIC_STATUS % (self.chip_ids[0]) # Always publish using our chip ID, which is the first
        logger.debug("Mqtt: Publish msg: %s %s" % (topic, msg))
        self.client.publish(topic, msg)


    


