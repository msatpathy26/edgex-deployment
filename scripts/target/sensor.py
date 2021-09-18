# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht

import sys, requests, json

edgexip = "192.168.226.14"


# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4)


while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        #temperature_c = 10 
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        #humidity = 97
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

        headers = {'content-type': 'application/json'}
        if(float(humidity) < 100):

            urlTemp = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/temperature' % edgexip
            urlHum  = 'http://%s:49986/api/v1/resource/Temp_and_Humidity_sensor_cluster_01/humidity' % edgexip
             
            response = requests.post(urlTemp, \
              data=json.dumps(int(temperature_c)), \
              headers=headers,verify=False)
            
            response = requests.post(urlHum, data=json.dumps(int(humidity)),\
                      headers=headers,verify=False)
            


    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

