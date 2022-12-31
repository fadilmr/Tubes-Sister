import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "sister/lapor/kopit"
client_id = f'satgas-kopit'


def connect_mqtt() -> mqtt_client:
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
         # read nik.txt
        f = open("nik.txt", "r")
        nik_list = f.read().splitlines()
        check = False
        for i in nik_list:
            # print(i)
            print(msg.topic.split("/")[3])
            if i == msg.topic.split("/")[3]:
                check = True
        f.close()
        if(check):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            publish(client)

    client.subscribe(topic+"/#")
    client.on_message = on_message

def publish(client):
    nik = input("Masukkan NIK: ")
    nama = input("Masukkan nama: ")
    jemput = input("Penjemputan berapa orang?: ")
    msg = f"nama: {nama}, nik: {nik}, jemput: {jemput}"
    result = client.publish(topic+"/"+nik, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}/{nik}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()