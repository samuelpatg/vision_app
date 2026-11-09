"""Comunicación MQTT entre la app Streamlit y el ESP32 simulado en Wokwi."""
import json
import random
import time
from collections import deque
 
import paho.mqtt.client as mqtt
import streamlit as st
 
BROKER = "broker.mqttdashboard.com"
PORT = 1883
BASE = "maceta_samuel"  # debe ser igual al BASE del firmware
 
T_HUMEDAD = f"{BASE}/humedad"   # ESP32 -> App
T_ESTADO = f"{BASE}/estado"     # ESP32 -> App
T_CONFIG = f"{BASE}/config"     # App -> ESP32
T_COMANDO = f"{BASE}/comando"   # App -> ESP32
 
 
def _crear_cliente():
    client_id = f"maceta-streamlit-{random.randint(0, 99999)}"
    try:  # paho-mqtt 2.x
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=client_id)
    except AttributeError:  # paho-mqtt 1.x
        return mqtt.Client(client_id=client_id)
 
 
@st.cache_resource
def get_mqtt():
    """Crea una sola conexión MQTT en segundo plano y guarda los últimos datos."""
    datos = {
        "conectado": False,
        "humedad": None,
        "estado": None,
        "ultimo": None,
        "historial": deque(maxlen=120),
    }
    client = _crear_cliente()
 
    def on_connect(c, userdata, flags, rc, *args):
        datos["conectado"] = rc == 0
        if rc == 0:
            c.subscribe([(T_HUMEDAD, 0), (T_ESTADO, 0)])
 
    def on_disconnect(c, userdata, rc, *args):
        datos["conectado"] = False
 
    def on_message(c, userdata, msg):
        valor = msg.payload.decode("utf-8", errors="ignore").strip()
        if msg.topic == T_HUMEDAD:
            try:
                h = float(valor)
            except ValueError:
                return
            datos["humedad"] = h
            datos["ultimo"] = time.time()
            datos["historial"].append((time.strftime("%H:%M:%S"), h))
        elif msg.topic == T_ESTADO:
            datos["estado"] = valor
 
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect_async(BROKER, PORT, keepalive=60)
    client.loop_start()
    return {"client": client, "datos": datos}
 
 
def publicar_config(planta, hmin, hmax):
    """App -> ESP32: envía la planta y sus umbrales de humedad."""
    payload = json.dumps(
        {"planta": planta, "min": int(hmin), "max": int(hmax)}, ensure_ascii=False
    )
    # retain=True: el ESP32 recibe la última configuración al reconectarse
    get_mqtt()["client"].publish(T_CONFIG, payload, qos=0, retain=True)
 
 
def publicar_comando(comando):
    """App -> ESP32: 'regar', 'auto' o 'manual'."""
    get_mqtt()["client"].publish(T_COMANDO, comando, qos=0)
 
