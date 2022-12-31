import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "sister/lapor/kopit"
# generate client ID with pub prefix randomly
client_id = f'pelapor-kopit'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
      print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    nik = input("Masukkan NIK: ")
    client.subscribe(topic+"/"+nik)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
