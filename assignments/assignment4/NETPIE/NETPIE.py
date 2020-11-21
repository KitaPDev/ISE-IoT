import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import json
import random
import ssl

port = 1883
serverIP = "broker.netpie.io"

subscriptionTopic = "@msg/LED"
publishTopic = "@shadow/data/update"

clientID = "b96b22c3-7ba0-4227-99c1-4be9af7406fa"
token = "TPcid5UuZQdb5V6dzU5mBJtrgN16ZHGD"
secret = "VqVgAA64xK!u8fn32NjL7gu3HQsfZFY_"

mqttUser_Pass = {"username":token, "password":secret}

LEDStatus = "ON"
payload = {
    "Temp":0,
    "Humi":0,
    "LED":LEDStatus
}

def onConnect(client, userdata, flags, rc):
    print("Connected with response: " +str(rc))
    client.subscribe(subscriptionTopic)
    
def onMessage(client, userdata, msg):
    global LEDStatus
    print(msg.topic + " " + str(msg.payload))
    
    receivedData = msg.payload.decode("UTF-8")
    LEDStatus = receivedData
    
client = mqtt.Client(protocol=mqtt.MQTTv311, client_id=clientID, clean_session=True)
client.on_connect = onConnect
client.on_message = onMessage

client.subscribe(subscriptionTopic)
client.username_pw_set(token, secret)
client.connect(serverIP, port)
client.loop_start()

while True:
    payload["Temp"] = random.randrange(25, 40)
    payload["Humi"] = random.randrange(50, 80)
    payload["LED"] = LEDStatus
    jsonData = json.dumps({"data":payload})
    print(jsonData)
    
    client.publish(publishTopic, jsonData, retain=True)
    print("Published...")
    time.sleep(2)