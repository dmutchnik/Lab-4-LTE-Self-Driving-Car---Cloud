from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json

device_id = "controller"
cert = "./keys/device0.certificate.pem"  # reuse an existing cert
key = "./keys/device0.private.pem"
root_ca = "./keys/AmazonRootCA1.pem"
endpoint = "a2nfcv2mpnifm9-ats.iot.us-east-1.amazonaws.com"

client = AWSIoTMQTTClient(device_id)
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, key, cert)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)
client.connect()

topic = "vehicle/emission/command"

print("Connected. Ready to send messages to devices.")
while True:
    msg = input("Enter a command to send to all devices: ")
    payload = {
        "sender": device_id,
        "command": msg,
        "timestamp": time.time()
    }
    client.publish(topic, json.dumps(payload), 0)
    print("Command sent.")
