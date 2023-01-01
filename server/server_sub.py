import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "sister/lapor/kopit/#"
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
         # read nik.txt
        f = open("nik.txt", "r")
        nik_list = f.read().splitlines()
        check = False
        for i in nik_list:
            if i == msg.topic.split("/")[3]:
                check = True
        f.close()
        if(check):
            print("============================")
            print("Data lapor baru saja masuk:")
            for i in msg.payload.decode().split(","):
              print(i)
            print("============================")
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()