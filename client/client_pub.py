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
        if rc != 0:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    nama = input("Masukkan nama: ")
    nik = input("Masukkan NIK: ")
    alamat = input("Masukkan alamat: ")
    gejala = input("Masukkan gejala: ")
    msg = f"Nama: {nama},NIK: {nik},Alamat: {alamat},Gejala: {gejala}"
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