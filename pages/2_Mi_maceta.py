import time
 
import altair as alt
import pandas as pd
import streamlit as st
 
from estilo import (
    aplicar_estilo,
    barra_rango,
    hero,
    leds_html,
    maceta_svg,
    tarjeta_estado,
)
from mqtt_utils import get_mqtt, publicar_comando, publicar_config
 
st.set_page_config(page_title="Mi maceta", page_icon="🪴", layout="centered")
aplicar_estilo()
 
mq = get_mqtt()
 
planta = st.session_state.get("planta", "Maceta sin planta identificada")
hero("Mi maceta", planta, "🪴")
 
 
def grafica(historial, hmin, hmax):
    df = pd.DataFrame(list(historial), columns=["hora", "humedad"])
    df["n"] = range(len(df))
    banda = (
        alt.Chart(pd.DataFrame({"y1": [hmin], "y2": [hmax]}))
        .mark_rect(color="#66BB6A", opacity=0.18)
        .encode(y="y1:Q", y2="y2:Q")
    )
    area = (
        alt.Chart(df)
        .mark_area(color="#2E7D32", opacity=0.15, interpolate="monotone")
        .encode(x=alt.X("n:Q", axis=None), y=alt.Y("humedad:Q", scale=alt.Scale(domain=[0, 100])))
    )
    linea = (
        alt.Chart(df)
        .mark_line(color="#2E7D32", strokeWidth=3, interpolate="monotone")
        .encode(
            x=alt.X("n:Q", axis=None),
            y=alt.Y("humedad:Q", scale=alt.Scale(domain=[0, 100]), title="Humedad (%)"),
            tooltip=["hora", "humedad"],
        )
    )
    return (banda + area + linea).properties(height=220).configure_view(strokeWidth=0)
 
 
# --- Monitoreo en vivo (ESP32 -> App), se refresca cada 2 s ---
@st.fragment(run_every=2)
def monitor():
    datos = mq["datos"]
    hmin = st.session_state.get("hmin", 30)
    hmax = st.session_state.get("hmax", 70)
 
    if not datos["conectado"]:
        st.warning("Conectando con el broker MQTT...")
    humedad = datos["humedad"]
    if humedad is None:
        st.info("Esperando datos del ESP32. Verifica que la simulación en Wokwi esté corriendo.")
        return
 
    if datos["ultimo"] and time.time() - datos["ultimo"] > 10:
        st.warning("Sin datos recientes del ESP32. ¿Sigue corriendo la simulación?")
 
    estado = datos["estado"]
    col_maceta, col_info = st.columns([1, 1.4])
    with col_maceta:
        st.markdown(maceta_svg(humedad, estado), unsafe_allow_html=True)
    with col_info:
        st.markdown(tarjeta_estado(humedad, estado), unsafe_allow_html=True)
        st.markdown(leds_html(estado), unsafe_allow_html=True)
        st.markdown(barra_rango(hmin, hmax, humedad), unsafe_allow_html=True)
 
    if datos["historial"]:
        st.markdown("#### 📈 Historial de humedad")
        st.altair_chart(grafica(datos["historial"], hmin, hmax), use_container_width=True)
 
 
monitor()
 
# --- Comandos (App -> ESP32) ---
st.markdown("#### 🎛️ Controles")
c1, c2, c3 = st.columns(3)
if c1.button("💧 Regar ahora"):
    publicar_comando("regar")
    st.toast("Comando de riego enviado 💧")
if c2.button("🤖 Modo automático"):
    publicar_comando("auto")
    st.session_state["modo"] = "automático"
    st.toast("Modo automático activado")
if c3.button("✋ Modo manual"):
    publicar_comando("manual")
    st.session_state["modo"] = "manual"
    st.toast("Modo manual activado")
st.caption(f"Último modo enviado: {st.session_state.get('modo', 'ninguno todavía')}")
 
# --- Configuración: rango de humedad (App -> ESP32) ---
hmin = st.session_state.get("hmin", 30)
hmax = st.session_state.get("hmax", 70)
with st.expander("⚙️ Ajustar rango de humedad ideal"):
    rango = st.slider("Rango ideal (%)", 0, 100, (hmin, hmax))
    if st.button("Enviar configuración"):
        st.session_state["hmin"], st.session_state["hmax"] = rango
        publicar_config(planta, rango[0], rango[1])
        st.toast("Configuración enviada al ESP32 🌱")
 
