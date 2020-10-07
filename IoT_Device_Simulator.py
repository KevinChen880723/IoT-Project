### section 1

!pip install AWSIoTPythonSDK


### section 2

import ssl
ssl.OPENSSL_VERSION

### section 3


import csv
import random
import json
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient


### section 4


CLIENT_NAME = "KEVIN_IoT"
TOPIC = "kevin_topic"

# Broker path is under AWS IoT > Settings (at the bottom left)
# Uncomment the next line after setting it
BROKER_PATH = "aie5kv3e5pj62-ats.iot.us-east-1.amazonaws.com"

# RSA 2048 bit key: Amazon Root CA 1 found here:
# https://docs.aws.amazon.com/iot/latest/developerguide/managing-device-certs.html
ROOT_CA_PATH = './AmazonRootCA1.pem.txt'

# These two keys are downloaded from the AWS IoT Console
# Upload them inside the Jupyter notebook and update/uncomment them
PRIVATE_KEY_PATH = './0dfd65f0da-private.pem.key'
CERTIFICATE_PATH = './0dfd65f0da-certificate.pem.crt'


 ### section 5


IoTclient = AWSIoTMQTTClient(CLIENT_NAME)
IoTclient.configureEndpoint(BROKER_PATH, 8883)
IoTclient.configureCredentials(
    ROOT_CA_PATH, 
    PRIVATE_KEY_PATH, 
    CERTIFICATE_PATH
)

# Allow the device to queue infinite messages
IoTclient.configureOfflinePublishQueueing(-1)

# Number of messages to send after a connection returns
IoTclient.configureDrainingFrequency(2)  # 2 requests/second

# How long to wait for a [dis]connection to complete (in seconds)
IoTclient.configureConnectDisconnectTimeout(10)

# How long to wait for publish/[un]subscribe (in seconds)
IoTclient.configureMQTTOperationTimeout(5) 


IoTclient.connect()


 ### section 6


def customCallbackUpdateDocument(client, userdata, message):
    global currentColor , currentPower
    payload = json.loads(message.payload)
    # First we need to know user wants change to which state, so keep the desired data
    #print(payload)
    
    if "desired" in payload["current"]["state"] :
        desiredColor = payload["current"]["state"]["desired"]["color"]
        desiredPower = payload["current"]["state"]["desired"]["power"]
        # If this is the first version shadow, there doesn't exist reported data, so we can't assign it, or it will happen some error
        if "reported" in payload["current"]["state"] :
            currentColor = payload["current"]["state"]["reported"]["color"]
            currentPower = payload["current"]["state"]["reported"]["power"]

        if (currentColor != desiredColor) or (currentPower != desiredPower):
            currentColor = desiredColor
            currentPower = desiredPower
            data["state"]["reported"]["color"] = currentColor
            data["state"]["reported"]["power"] = currentPower
            IoTclient.publish("$aws/things/KEVIN_IoT_Thing/shadow/update", json.dumps(data), 0)
            # "changed" is a flag, only if led or power state is changed will set to "1"
            global changed
            changed = True
    
    
def customCallbackGetAccepted(client, userdata, message):
    payload = json.loads(message.payload)
    global currentColor , currentPower
    currentColor = payload["state"]["reported"]["color"]
    currentPower = payload["state"]["reported"]["power"]
    
def main():
    # Set default data(if we are using physical device, we don't need to set default data, 
    #                  because we can always monitor the data from sensor)
    global currentColor, currentPower, data   
    currentColor = "red"
    currentPower = "on"
    data = {
        "state" : {
            "reported" : {
                "color" : currentColor,
                "power" : currentPower
            }
        }
    }
    
    IoTclient.subscribe("$aws/things/KEVIN_IoT_Thing/shadow/update/documents", 1, customCallbackUpdateDocument)
    IoTclient.publish("$aws/things/KEVIN_IoT_Thing/shadow/update", json.dumps(data), 0)
    print('Buld color is : ', currentColor)
    print('Power is : ', currentPower)
    previousColor = currentColor
    previousPower = currentPower
    global changed
    changed = False
    while True:
        # when publis a new state to shadow, changed will set to "1"
        if changed:
            print("Buld color is change to " , currentColor)
            print("Power is turn " , currentPower)
            changed = False
            MessageData = json.dumps({
                "power":currentPower,
                "color":currentColor
            })
            IoTclient.publish(TOPIC, MessageData, 0)
    
main()