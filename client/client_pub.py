import random
import time
import subprocess

from paho.mqtt import client as mqtt_client


# broker = '127.0.0.1'
# port = 7777
broker = 'broker.hivemq.com'
port = 1883
topic = "sister/lapor/kopit"
# generate client ID with pub prefix randomly

nama = input("Masukkan nama: ")
nik = input("Masukkan NIK: ")
alamat = input("Masukkan alamat: ")
gejala = input("Masukkan gejala: ")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f'client-kopit-{nik}-pub')
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg = f"Nama: {nama},NIK: {nik},Alamat: {alamat},Gejala: {gejala}"
    result = client.publish(topic+"/"+nik, msg)
    # result: [0, 1]
    status = result[0]
    print(status)
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}/{nik}`")
        subprocess.run(["python", "client_sub.py", nik], shell=True)
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()