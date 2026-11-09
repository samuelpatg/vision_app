import time
 
import pandas as pd
import streamlit as st
 
from mqtt_utils import get_mqtt, publicar_comando, publicar_config
 
st.set_page_config(page_title="Mi maceta", page_icon="🪴", layout="centered")
st.title("🪴 Mi maceta")
 
mq = get_mqtt()
 
planta = st.session_state.get("planta", "Maceta sin planta identificada")
hmin = st.session_state.get("hmin", 30)
hmax = st.session_state.get("hmax", 70)
 
st.subheader(planta)
 
# --- Configuración: rango de humedad (App -> ESP32) ---
with st.expander("⚙️ Rango de humedad ideal", expanded=False):
    rango = st.slider("Rango ideal (%)", 0, 100, (hmin, hmax))
    if st.button("Enviar configuración"):
        st.session_state["hmin"], st.session_state["hmax"] = rango
        publicar_config(planta, rango[0], rango[1])
        st.toast("Configuración enviada al ESP32")
 
# --- Comandos (App -> ESP32) ---
st.markdown("**Controles**")
c1, c2, c3 = st.columns(3)
if c1.button("💧 Regar ahora"):
    publicar_comando("regar")
    st.toast("Comando de riego enviado")
if c2.button("🤖 Modo automático"):
    publicar_comando("auto")
    st.session_state["modo"] = "automático"
    st.toast("Modo automático activado")
if c3.button("✋ Modo manual"):
    publicar_comando("manual")
    st.session_state["modo"] = "manual"
    st.toast("Modo manual activado")
st.caption(f"Último modo enviado: {st.session_state.get('modo', 'ninguno todavía')}")
 
st.divider()
 
MENSAJES = {
    "seco": ("🔴", "Seco: hay que regar"),
    "ok": ("🟢", "Humedad ideal: no hace falta regar"),
    "humedo": ("🟡", "Exceso de agua: no riegues"),
}
 
 
# --- Monitoreo en vivo (ESP32 -> App), se refresca cada 2 s ---
@st.fragment(run_every=2)
def monitor():
    datos = mq["datos"]
 
    if not datos["conectado"]:
        st.warning("Conectando con el broker MQTT...")
    humedad = datos["humedad"]
    if humedad is None:
        st.info("Esperando datos del ESP32. Verifica que la simulación en Wokwi esté corriendo.")
        return
 
    if datos["ultimo"] and time.time() - datos["ultimo"] > 10:
        st.warning("Sin datos recientes del ESP32. ¿Sigue corriendo la simulación?")
 
    icono, mensaje = MENSAJES.get(datos["estado"], ("⚪", "Estado desconocido"))
    col1, col2 = st.columns(2)
    col1.metric("Humedad actual", f"{humedad:.0f}%")
    col2.metric("Estado", f"{icono} {datos['estado'] or '—'}")
    st.progress(min(max(int(humedad), 0), 100) / 100)
    st.markdown(f"### {icono} {mensaje}")
 
    if datos["historial"]:
        df = pd.DataFrame(list(datos["historial"]), columns=["hora", "humedad"]).set_index("hora")
        st.line_chart(df, height=220)
 
 
monitor()
 
