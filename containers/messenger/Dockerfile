FROM pypy:3
RUN pip3 install paho-mqtt
RUN pip3 install influxdb
ADD app.py /
CMD ["python3", "-u",  "app.py"]
