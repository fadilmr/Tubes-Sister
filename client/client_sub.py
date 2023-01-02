import random
import sys

from paho.mqtt import client as mqtt_client


# broker = '127.0.0.1'
# port = 7777
# konfigurasi broker
broker = 'broker.hivemq.com'
port = 1883
nik = sys.argv[1]
print(nik)
topic = "sister/lapor/kopit/server/"+nik
client_id = f'client-kopit-{nik}-sub'

# fungsi untuk menghubungkan ke broker
def connect_mqtt() -> mqtt_client:
    # fungsi untuk mengecek apakah koneksi berhasil
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Berhasil Terhubung")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# fungsi untuk subscribe
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
      print("============================")
      print("Data lapor baru saja masuk:")
      for i in msg.payload.decode().split(", "):
        print(i)
      print("============================")
      client.disconnect()
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()