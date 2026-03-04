#!/usr/bin/env python3
import socket
import json
import paho.mqtt.client as mqtt

# ---------------------------------------------------------
# Settings CHANGE IP XXX.XXX.XXX.XXX to your MQTT ip e.g. Mosquitto etc.
# Settings CHANGE MQTT topic "mqttFHEMBridge/DEVICE/VALUE" to your MQTT topic 
# Settings CHANGE MAC XXXXXXXXXXXX to somthing realistic e.g. the running system 
# ---------------------------------------------------------
UDP_PORT = 2222
SRC_ID = "shellyemg3-ec4609c439c1"

# ---------------------------------------------------------
# MQTT
# ---------------------------------------------------------
MQTT_BROKER = "XXX.XXX.XXX.XXX"
MQTT_TOPIC = "mqttFHEMBridge/DEVICE/VALUE"

CURRENT_POWER = 0.0

def on_mqtt_message(client, userdata, msg):
    global CURRENT_POWER
    try:
        CURRENT_POWER = float(msg.payload.decode())
    except:
        pass

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_mqtt_message
mqtt_client.connect(MQTT_BROKER)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

# give MQTT a moment to receive at least one value
import time
time.sleep(0.2)

# ---------------------------------------------------------
# UDP Server (one-shot)
# ---------------------------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))
sock.settimeout(2.0)

try:
    data, addr = sock.recvfrom(2048)
except socket.timeout:
    sock.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    exit(0)

try:
    req = json.loads(data.decode("utf-8"))
except:
    sock.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    exit(0)

method = req.get("method", "")
rpc_id = req.get("id", 0)

# ---------------------------------------------------------
# Responses
# ---------------------------------------------------------

def send(resp):
    sock.sendto(json.dumps(resp, separators=(",", ":")).encode("utf-8"), addr)

if method == "EM1.GetStatus":
    send({
        "id": rpc_id,
        "src": SRC_ID,
        "dst": "unknown",
        "result": {"act_power": CURRENT_POWER}
    })

elif method == "Shelly.GetDeviceInfo":
    send({
        "id": rpc_id,
        "src": SRC_ID,
        "dst": "unknown",
        "result": {
            "model": "SPEM-003CEEU",
            "mac": "EC4609C439C1",
            "fw_id": "20240202-123456/v1.0.0",
            "gen": 3
        }
    })

elif method == "Shelly.GetStatus":
    send({
        "id": rpc_id,
        "src": SRC_ID,
        "dst": "unknown",
        "result": {"act_power": CURRENT_POWER}
    })

elif method == "Shelly.GetConfig":
    send({
        "id": rpc_id,
        "src": SRC_ID,
        "dst": "unknown",
        "result": {}
    })

# ---------------------------------------------------------
# Shutdown
# ---------------------------------------------------------
sock.close()
mqtt_client.loop_stop()
mqtt_client.disconnect()
