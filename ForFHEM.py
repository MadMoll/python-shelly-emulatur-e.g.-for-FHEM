#!/usr/bin/env python3
import socket
import json
import sys

# ---------------------------------------------------------
# Settings CHANGE MAC XXXXXXXXXXXX to somthing realistic e.g. the running system
# ---------------------------------------------------------
UDP_PORT = 2222
SRC_ID = "shellyemg3-ec4609c439c1"

# ---------------------------------------------------------
# Power value from FHEM argument
# ---------------------------------------------------------
try:
    CURRENT_POWER = float(sys.argv[1])
except:
    CURRENT_POWER = 0.0

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
    sys.exit(0)

try:
    req = json.loads(data.decode("utf-8"))
except:
    sock.close()
    sys.exit(0)

method = req.get("method", "")
rpc_id = req.get("id", 0)

def send(resp):
    sock.sendto(json.dumps(resp, separators=(",", ":")).encode("utf-8"), addr)

# ---------------------------------------------------------
# Responses
# ---------------------------------------------------------
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
            "mac": "XXXXXXXXXXXX",
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

sock.close()
