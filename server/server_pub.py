import random
import time
import sys

from paho.mqtt import client as mqtt_client


# broker = '127.0.0.1'
# port = 7777
broker = 'broker.hivemq.com'
port = 1883
topic = "sister/lapor/kopit/server"
# generate client ID with pub prefix randomly
nik = sys.argv[1]
client_id = f'server-{nik}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    print(nik)
    nama = input("Masukkan nama: ")
    jemput = input("Penjemputan berapa orang?: ")
    waktu = input("Waktu penjemputan: ")
    msg = f"Nama: {nama},NIK: {nik},Jemput: {jemput} orang,Waktu: {waktu}"
    result = client.publish(topic+"/"+nik, msg)
    print(topic+"/"+nik)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}/{nik}`")
    else:
        print(f"Failed to send message to topic {topic}/{nik}")
    time.sleep(7)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
