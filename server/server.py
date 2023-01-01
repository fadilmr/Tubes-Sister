import random
import subprocess

from paho.mqtt import client as mqtt_client


# broker = '127.0.0.1'
# port = 7777
broker = 'broker.hivemq.com'
port = 1883
topic = "sister/lapor/kopit"
client_id = f'server-satgas-kopit'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Berhasil Terhubung")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    nik = input("Masukkan NIK: ")
    nama = input("Masukkan nama: ")
    jemput = input("Penjemputan berapa orang?: ")
    waktu = input("Waktu penjemputan: ")
    msg = f"Nama: {nama},NIK: {nik},Jemput: {jemput} orang,Waktu: {waktu}"
    result = client.publish(topic+"/server/"+nik, msg)
    print(topic+"/server/"+nik)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}/{nik}`")
    else:
        print(f"Failed to send message to topic {topic}/{nik}")


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        f = open("nik.txt", "r")
        nik_list = f.read().splitlines()
        check = False
        nik = msg.topic.split("/")[3]
        for i in nik_list:
            if i == nik:
                check = True
        f.close()
        if(check):
            print("============================")
            print("Data lapor baru saja masuk:")
            for i in msg.payload.decode().split(","):
              print(i)
            print("============================")
            subprocess.Popen(['start', 'py', 'server_pub.py', nik], shell=True)
    client.subscribe(topic+"/#")
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()