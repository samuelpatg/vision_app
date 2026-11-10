import streamlit as st
 
from estilo import aplicar_estilo, hero
 
st.set_page_config(page_title="Maceta inteligente", page_icon="🪴", layout="centered")
aplicar_estilo()
 
hero(
    "Maceta inteligente",
    "Identifica tu planta con IA y deja que tu maceta te avise cuándo regar.",
    "🪴",
)
 
st.markdown("### ¿Cómo funciona?")
 
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        '<div class="paso"><span class="paso-num">1</span>'
        '<div class="paso-titulo">📸 Identifica</div>'
        '<div class="paso-texto">Sube o toma una foto. La IA reconoce la planta, te da sus '
        "cuidados y su rango de humedad ideal.</div></div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div class="paso"><span class="paso-num">2</span>'
        '<div class="paso-titulo">📡 Conecta</div>'
        '<div class="paso-texto">Envía ese rango a la maceta simulada en Wokwi (ESP32) '
        "por MQTT, en ambos sentidos.</div></div>",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        '<div class="paso"><span class="paso-num">3</span>'
        '<div class="paso-titulo">💧 Cuida</div>'
        '<div class="paso-texto">Mira la humedad en tiempo real. Los LEDs te dicen si regar, '
        "si todo está bien o si hay exceso de agua.</div></div>",
        unsafe_allow_html=True,
    )
 
st.write("")
b1, b2 = st.columns(2)
with b1:
    st.page_link("pages/1_Identificar_planta.py", label="Identificar planta", icon="🌿")
with b2:
    st.page_link("pages/2_Mi_maceta.py", label="Ver mi maceta", icon="🪴")
 
