import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "sister/lapor/kopit"
# generate client ID with pub prefix randomly
client_id = f'server-lapor-kopit'

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


def publish(client):
    nik = input("Masukkan NIK: ")
    nama = input("Penjemputan berapa orang?: ")
    msg = f"nama: {nama}, nik: {nik}, alamat: {alamat}, gejala: {gejala}"
    result = client.publish(topic+"/"+nik, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}/{nik}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()