#!/bin/bash

###########################################################
# Run this script to initialize mosquitto mqtt broker build
# ./mqtt-broker-setup.sh
#
# Author: Milan Satpathy <msatpathy@mvista.com>
###########################################################

PROJECT_DIR=$(readlink -f $(pwd)/../)
MQTT_BASE_DIR="$PROJECT_DIR/containers/mqtt-broker/"
MQTT_BROKER_CONFIG_DIR="$PROJECT_DIR/containers/mqtt-broker/config"
MQTT_BROKER_DATA_DIR="$PROJECT_DIR/containers/mqtt-broker/data"
MQTT_BROKER_LOG_DIR="$PROJECT_DIR/containers/mqtt-broker/log"

mkdir -p $MQTT_BROKER_CONFIG_DIR; [ -d "$MQTT_BROKER_CONFIG_DIR" ] && rm -rf $MQTT_BROKER_CONFIG_DIR/*; chmod -R 777 $MQTT_BROKER_CONFIG_DIR
mkdir -p $MQTT_BROKER_DATA_DIR; [ -d "$MQTT_BROKER_DATA_DIR" ] && rm -rf $MQTT_BROKER_DATA_DIR/*; chmod -R 777 $MQTT_BROKER_DATA_DIR
mkdir -p $MQTT_BROKER_LOG_DIR; [ -d "$MQTT_BROKER_LOG_DIR" ] &&  rm -rf $MQTT_BROKER_LOG_DIR/*; touch "$MQTT_BROKER_LOG_DIR/mosquitto.log";chmod -R 777 $MQTT_BROKER_LOG_DIR

cp mosquitto.conf "$MQTT_BROKER_CONFIG_DIR/mosquitto.conf"
sed -i "s#^persistence_location.*#persistence_location mosquitto $MQTT_BROKER_DATA_DIR#" "$MQTT_BROKER_CONFIG_DIR/mosquitto.conf"
sed -i "s#^log_dest file .*#log_dest file  $MQTT_BROKER_LOG_DIR/mosquitto.log#" "$MQTT_BROKER_CONFIG_DIR/mosquitto.conf"

cp -rf "$MQTT_BASE_DIR/docker-compose-mqtt.template" "$MQTT_BASE_DIR/docker-compose.yml"
sed -i "s!/mqtt-config-host-path/!$MQTT_BROKER_CONFIG_DIR!" "$MQTT_BASE_DIR/docker-compose.yml"
sed -i "s!/mqtt-data-host-path/!$MQTT_BROKER_DATA_DIR!" "$MQTT_BASE_DIR/docker-compose.yml"
sed -i "s!/mqtt-log-host-path/!$MQTT_BROKER_LOG_DIR!" "$MQTT_BASE_DIR/docker-compose.yml"

