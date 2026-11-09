import base64
import json
 
import streamlit as st
from openai import OpenAI
 
from mqtt_utils import publicar_config
 
st.set_page_config(page_title="Identificar planta", page_icon="🌿", layout="centered")
st.title("🌿 Identificar planta")
 
PROMPT = """Eres un experto en botánica. Analiza la imagen y responde SOLO con un JSON válido con estas claves:
- "es_planta": true o false
- "planta": nombre común en español
- "nombre_cientifico": nombre científico
- "descripcion": descripción breve (máximo 2 frases)
- "cuidados": lista de 3 a 6 consejos cortos (riego, luz, temperatura, sustrato)
- "frecuencia_riego": texto corto, por ejemplo "cada 7 días"
- "humedad_min": entero de 0 a 100, límite inferior del rango ideal de humedad del sustrato (%)
- "humedad_max": entero de 0 a 100, límite superior del rango ideal de humedad del sustrato (%)
Si la imagen no contiene una planta, responde {"es_planta": false}."""
 
 
def obtener_api_key():
    try:
        clave = st.secrets["OPENAI_API_KEY"]
    except Exception:
        clave = ""
    if clave:
        return clave
    return st.text_input("Clave de OpenAI", type="password")
 
 
def analizar(imagen_bytes, mime, pregunta, api_key):
    client = OpenAI(api_key=api_key)
    texto = PROMPT
    if pregunta:
        texto += f"\n\nContexto adicional del usuario: {pregunta}"
    b64 = base64.b64encode(imagen_bytes).decode("utf-8")
    respuesta = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        max_tokens=900,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": texto},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                ],
            }
        ],
    )
    return json.loads(respuesta.choices[0].message.content)
 
 
def limpiar_umbrales(ficha):
    """Valida el rango de humedad devuelto por el modelo."""
    try:
        hmin = max(0, min(100, int(ficha.get("humedad_min", 30))))
        hmax = max(0, min(100, int(ficha.get("humedad_max", 70))))
    except (TypeError, ValueError):
        hmin, hmax = 30, 70
    if hmin >= hmax:
        hmin, hmax = 30, 70
    return hmin, hmax
 
 
api_key = obtener_api_key()
 
# --- Modalidad de entrada: subir archivo o usar la cámara ---
tab_archivo, tab_camara = st.tabs(["📁 Subir foto", "📷 Usar cámara"])
with tab_archivo:
    archivo = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
with tab_camara:
    foto = st.camera_input("Toma una foto de la planta")
 
imagen = archivo or foto
if imagen:
    st.image(imagen, caption="Imagen a analizar", use_container_width=True)
 
pregunta = st.text_area(
    "¿Algo específico que quieras saber? (opcional)",
    placeholder="Ej.: sus hojas se ven amarillas, ¿qué puede ser?",
)
 
if st.button("Analizar planta", type="primary"):
    if not imagen:
        st.warning("Primero sube o toma una foto.")
    elif not api_key:
        st.warning("Ingresa tu clave de OpenAI.")
    else:
        with st.spinner("Analizando..."):
            try:
                ficha = analizar(imagen.getvalue(), imagen.type or "image/jpeg", pregunta, api_key)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
                ficha = None
        if ficha is not None:
            if not ficha.get("es_planta", False):
                st.warning("No parece haber una planta en la imagen. Prueba con otra foto.")
                st.session_state.pop("ficha", None)
            else:
                hmin, hmax = limpiar_umbrales(ficha)
                st.session_state["ficha"] = ficha
                st.session_state["planta"] = ficha.get("planta", "Planta")
                st.session_state["hmin"] = hmin
                st.session_state["hmax"] = hmax
 
# --- Resultado (se conserva entre ejecuciones) ---
ficha = st.session_state.get("ficha")
if ficha:
    st.divider()
    st.subheader(f"{ficha.get('planta', 'Planta')}")
    st.caption(ficha.get("nombre_cientifico", ""))
    st.write(ficha.get("descripcion", ""))
 
    st.markdown("**Cuidados**")
    for consejo in ficha.get("cuidados", []):
        st.markdown(f"- {consejo}")
 
    col1, col2 = st.columns(2)
    col1.metric("Frecuencia de riego", ficha.get("frecuencia_riego", "—"))
    col2.metric(
        "Humedad ideal",
        f"{st.session_state['hmin']}% – {st.session_state['hmax']}%",
    )
 
    if st.button("🪴 Enviar a mi maceta"):
        publicar_config(
            st.session_state["planta"],
            st.session_state["hmin"],
            st.session_state["hmax"],
        )
        st.success("Configuración enviada. Ve a la página «Mi maceta» para ver el resultado.")
 
