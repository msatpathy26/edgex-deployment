#!/usr/bin/env python3

#####################################################################
# Name: mqtt-subscribe-test.py
#
# Usage: python3 mqtt-subscribe-test.py
#
# Dependency: paho-mqtt ( pip install paho-mqtt )
#
# Author: Milan satpathy <msatpathy@mvista.com>
#
# Description:
# This script can be used to verify the functioning of mqtt -
# broker. Once mqtt broker is running and device data starts 
# flowing through edgex stack (device --> edgex --> mqtt-broker ),
# this script can be used to subscribe to the broker and read 
# and print the device data.
#
# The default topic name is "sensor-data-dht11". The topic
# name can be altered by modifying variable 'MQTT_SUBSCRIBE_TOPIC'.
#####################################################################

import paho.mqtt.client as mqtt

MQTT_SUBSCRIBE_TOPIC = "sensor-data-dht11"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_SUBSCRIBE_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("0.0.0.0", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
