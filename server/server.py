import random
import subprocess

from paho.mqtt import client as mqtt_client


# broker = '127.0.0.1'
# port = 7777

# konfigurasi broker
broker = 'broker.hivemq.com'
port = 1883
topic = "sister/lapor/kopit"
client_id = f'server-satgas-kopit'

# fungsi untuk menghubungkan ke broker
def connect_mqtt() -> mqtt_client:
    # fungsi untuk mengecek apakah terhubung ke broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Berhasil Terhubung")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# fungsi untuk publish
def publish(client):
    # input data untuk publish ke client
    nik = input("Masukkan NIK: ")
    nama = input("Masukkan nama: ")
    jemput = input("Penjemputan berapa orang?: ")
    waktu = input("Waktu penjemputan: ")
    # membuat pesan yang akan dikirim
    msg = f"Nama: {nama},NIK: {nik},Jemput: {jemput} orang,Waktu: {waktu}"
    # publish pesan ke client
    result = client.publish(topic+"/server/"+nik, msg)
    print(topic+"/server/"+nik)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}/{nik}`")
    else:
        print(f"Failed to send message to topic {topic}/{nik}")


# fungsi untuk subscribe
def subscribe(client: mqtt_client):
    # fungsi untuk mengecek apakah ada pesan yang masuk
    def on_message(client, userdata, msg):
        # membuka file nik.txt
        f = open("nik.txt", "r")
        nik_list = f.read().splitlines()
        check = False
        # memisahkan nik dari topic
        nik = msg.topic.split("/")[3]
        for i in nik_list:
            if i == nik:
                check = True
        f.close()
        # mengecek apakah nik ada di file nik.txt
        if(check):
            print("============================")
            print("Data lapor baru saja masuk:")
            # merapihkan data yang diterima dari client
            for i in msg.payload.decode().split(", "):
              print(i)
            print("============================")
            # menjalankan file server_pub.py
            subprocess.Popen(['start', 'py', 'server_pub.py', nik], shell=True)
    # subscribe ke topic
    client.subscribe(topic+"/#")
    client.on_message = on_message

# fungsi utama
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


# menjalankan fungsi utama
if __name__ == '__main__':
    run()