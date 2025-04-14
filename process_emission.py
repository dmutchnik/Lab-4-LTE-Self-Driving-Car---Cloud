from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

# Parameters
device_id = 0
data_path = "data2/vehicle{}.csv".format(device_id)
certificate_path = "keys/device{}.certificate.pem".format(device_id)
key_path = "keys/device{}.private.pem".format(device_id)
ca_path = "keys/AmazonRootCA1.pem"
endpoint = "a2nfcv2mpnifm9-ats.iot.us-east-1.amazonaws.com"
topic_pub = "emission/data"
topic_sub = "vehicles/0/analysis"

class MQTTClient:
    def __init__(self, device_id, cert, key):
        self.device_id = str(device_id)
        self.client = AWSIoTMQTTClient(self.device_id)
        self.client.configureEndpoint(endpoint, 8883)
        self.client.configureCredentials(ca_path, key, cert)
        self.client.configureOfflinePublishQueueing(-1)
        self.client.configureDrainingFrequency(2)
        self.client.configureConnectDisconnectTimeout(10)
        self.client.configureMQTTOperationTimeout(5)
        self.client.onMessage = self.custom_on_message

    def custom_on_message(self, message):
        logging.info("Client {} received payload {} from topic {}".format(
            self.device_id, message.payload.decode("utf-8"), message.topic))

    def custom_puback_callback(self, mid):
        pass

    def publish(self):
        df = pd.read_csv(data_path)
        logging.info("Loaded %d rows from %s", len(df), data_path)
        for _, row in df.iterrows():
            payload = json.dumps(row.to_dict())
            logging.info("Publishing data to topic: %s", topic_pub)
            self.client.publishAsync(topic_pub, payload, 0, ackCallback=self.custom_puback_callback)
            time.sleep(1)

    def subscribe(self):
        self.client.subscribeAsync(topic_sub, 1)
        logging.info("Device %s subscribed to %s", self.device_id, topic_sub)

# Execution
client = MQTTClient(device_id, certificate_path, key_path)
client.client.connect()
client.subscribe()

while True:
    x = input("Press 's' to send data or 'd' to disconnect: ")
    if x == "s":
        client.publish()
    elif x == "d":
        client.client.disconnect()
        logging.info("Disconnected.")
        break
    else:
        logging.info("Invalid input.")
