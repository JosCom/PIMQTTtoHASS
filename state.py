#rbPI MQTT State
from sense_hat import SenseHat
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
sense = SenseHat()

Broker = "192.168.1.10"

sub_topic = "pisensor/instructions"    # receive messages on this topic

pub_topic = "pisensor/data"       # send messages to this topic


############### sensehat inputs ##################

def read_temp():
    t = sense.get_temperature()
    t = round(t,1)
    t = '"temperature":'+str(t)
    return t

def read_humidity():
    h = sense.get_humidity()
    h = round(h,1)
    h = '"humidity":'+str(h)
    return h

def read_pressure():
    p = sense.get_pressure()
    p = round(p,1)
    p = '"pressure":'+str(p)
    return p

def display_sensehat(message):
    sense.show_message(message)
    time.sleep(10)

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)
    display_sensehat(message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.username_pw_set("mqtt", "password")
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()

while True:
    sensor_data = '{'+str(read_temp())+','+str(read_humidity())+','+str(read_pressure())+'}'
    client.publish("homeassistant/sensor/drivhustest/state", str(sensor_data))
    time.sleep(1*60)
