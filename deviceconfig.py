from uuid import getnode as get_mac
import string
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

##- Info -##
# Config
broker = "192.168.1.10"
username = "mqtt"
password = "password"
device_type = "sensor"
device_class = ["temperature","humidity", "pressure"]
device_name = "drivhustest"
device_status = 1
device_manufacturer = "JosCom"
device_model = "rbpi3"
device_sw_version = "1.0"

##- MQTT -##

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected to "+str(broker)+" with result code "+str(rc))
    #client.subscribe(str(config_topic))

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)
client.loop_start()

##- Homeassistant -##

# Register device in homeassistant
def device_config(x):
  entity_name = str(device_name)+" "+str(x)
  unique_id = str(get_mac())+"_"+str(x)
  config_topic = "homeassistant/"+str(device_type)+"/"+str(device_name)+"_"+str(x)+"/config"
  state_topic = "homeassistant/"+str(device_type)+"/"+str(device_name)+"/state"
  if device_status == 1:
    #print(string.capwords(x+":"))
    client.publish(config_topic, str('{"name": "'+string.capwords(entity_name)+'", "unique_id": "'+str(unique_id)+'", "device_class": "'+str(x)+'","value_template": "{{value_json.'+str(x)+'}}", "state_topic": "'+str(state_topic)+'", "device": {"name": "'+string.capwords(device_name)+'", "connections":[["mac", "'+str(get_mac())+'"]],"manufacturer": "'+str(device_manufacturer)+'", "model": "'+str(device_model)+'", "sw_version": "'+str(device_sw_version)+'"}}'))
  else:
    print("Device "+str(device_name)+" is deleted")
    client.publish(config_topic, str(""))

# Update device state in homeassistant
#def device_state(x):


##- Execute -##

for x in device_class:
  device_config(x)
