
import streamlit as st
 
st.set_page_config(page_title="Maceta inteligente", page_icon="🪴", layout="centered")
 
st.title("🪴 Maceta inteligente")
st.write(
    "Identifica tu planta con inteligencia artificial y conecta la información "
    "con una maceta simulada en Wokwi que mide la humedad y te avisa con LEDs "
    "cuándo regar."
)
 
st.subheader("¿Cómo funciona?")
st.markdown(
    """
1. **Identificar planta:** sube o toma una foto. La IA reconoce la planta, te da
   sus cuidados y el rango de humedad ideal.
2. **Mi maceta:** envía ese rango al ESP32 y monitorea la humedad en tiempo real.
   Los LEDs indican si debes regar (rojo), si todo está bien (verde) o si hay
   exceso de agua (amarillo).
"""
)
 
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Identificar_planta.py", label="Identificar planta", icon="🌿")
with col2:
    st.page_link("pages/2_Mi_maceta.py", label="Mi maceta", icon="🪴")
 
