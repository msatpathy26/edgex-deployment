#!/usr/bin/env python3

###################################################################
# Title:        messenger
#
# Description:  Fetches MQTT messages from broker and feeds into influxdb
# Author:       Milan Satpathy <msatpathy@mvista.com>
###################################################################
import paho.mqtt.client as mqtt
import time
import json
import argparse
from influxdb import InfluxDBClient
from datetime import datetime

# Set environment variables
# MQTTT authentication + port need to be set separately
broker_address  = "0.0.0.0"
topic           = "sensor-data-dht11"
dbhost          = "0.0.0.0"
dbport          = 8086
dbuser          = "root"
dbpassword      = "password"
dbname          = "sensordata"


def influxDBconnect():

    """Instantiate a connection to the InfluxDB."""
    influxDBConnection = InfluxDBClient(dbhost, dbport, dbuser, dbpassword, dbname)

    return influxDBConnection



def influxDBwrite(device, sensorName, sensorValue):

    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    measurementData = [
        {
            "measurement": device,
            "tags": {
                "gateway": device,
                "location": "Bhubaneswar"
            },
            "time": timestamp,
            "fields": {
                sensorName: sensorValue
            }
        }
    ]
    print("Writing data to db..")
    print(measurementData)
    influxDBConnection.write_points(measurementData, time_precision='ms')



def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))

    # Create a dictionary and extract the current values
    obj = json.loads(m)
    # current date and time
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Extract the data from each sensor, even if the MQTT message contain multiple entries
    for entry in obj["readings"]:
        print("Sensor: %s: Reading: %s" % (entry["name"], entry["value"]) )

        device      = entry["device"]
        sensorName  = entry["name"]
        sensorValue = entry["value"]

        # Write data to influxDB
        influxDBwrite(device, sensorName, sensorValue)




influxDBConnection = influxDBconnect()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, 1883, 60)

client.loop_forever()
