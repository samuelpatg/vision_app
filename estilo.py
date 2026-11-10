"""Estilo visual y componentes HTML de la maceta inteligente."""
import html
 
import streamlit as st
 
CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Nunito:wght@400;600;700;800&display=swap');
.stApp, .stApp p, .stApp label, .stApp li, .stApp button { font-family: 'Nunito', sans-serif; }
.stApp h1, .stApp h2, .stApp h3, .titulo-serif { font-family: 'Fraunces', serif !important; color: #1B3A1F; }
.stApp { background: linear-gradient(180deg, #F6FAF3 0%, #E6F1DC 100%); }
[data-testid="stSidebar"] { background: #DCEBD2; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 900px; }
 
.hero { position: relative; overflow: hidden; background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 60%, #A5D6A7 100%); border-radius: 24px; padding: 28px 130px 28px 32px; color: #fff; margin-bottom: 22px; box-shadow: 0 8px 24px rgba(46,125,50,.25); }
.hero-titulo { font-family: 'Fraunces', serif; font-size: 2.1rem; font-weight: 700; line-height: 1.15; }
.hero-sub { margin-top: 6px; font-size: 1.05rem; opacity: .95; }
.hero-emoji { position: absolute; right: 24px; top: 50%; transform: translateY(-50%); font-size: 4.6rem; }
 
.paso { background: #fff; border-radius: 18px; padding: 18px 20px; box-shadow: 0 4px 14px rgba(27,58,31,.08); border-top: 5px solid #66BB6A; min-height: 170px; }
.paso-num { display: inline-block; background: #E4F0DC; color: #2E7D32; font-weight: 800; border-radius: 999px; padding: 2px 12px; font-size: .85rem; }
.paso-titulo { font-family: 'Fraunces', serif; font-size: 1.2rem; font-weight: 700; margin: 8px 0 4px; color: #1B3A1F; }
.paso-texto { color: #3d5a40; font-size: .97rem; }
 
.tarjeta { background: #fff; border-radius: 20px; padding: 20px 22px; box-shadow: 0 4px 14px rgba(27,58,31,.08); margin-bottom: 14px; }
.tarjeta-titulo { font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 700; color: #1B3A1F; }
.tarjeta-cientifico { font-style: italic; color: #5d7a60; margin-bottom: 8px; }
.tarjeta h4 { margin: 14px 0 6px; font-family: 'Fraunces', serif; color: #2E7D32; }
.tarjeta ul { margin: 0; padding-left: 1.2rem; color: #2f4a32; }
.tarjeta li { margin-bottom: 4px; }
.mini-datos { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
.mini { flex: 1; min-width: 150px; background: #F1F8EC; border-radius: 14px; padding: 10px 14px; }
.mini-etq { font-size: .8rem; color: #5d7a60; text-transform: uppercase; letter-spacing: .04em; }
.mini-val { font-size: 1.15rem; font-weight: 800; color: #1B3A1F; }
 
.estado-card { display: flex; gap: 16px; align-items: center; border-radius: 20px; padding: 18px 20px; margin-bottom: 12px; border: 2px solid; }
.estado-card.seco { background: #FDECEA; border-color: #EF9A9A; }
.estado-card.ok { background: #E8F5E9; border-color: #81C784; }
.estado-card.humedo { background: #FFF8E1; border-color: #FFD54F; }
.estado-emoji { font-size: 3rem; line-height: 1; }
.estado-titulo { font-family: 'Fraunces', serif; font-size: 1.35rem; font-weight: 700; color: #1B3A1F; }
.estado-detalle { color: #3d5a40; font-size: .95rem; margin: 2px 0 6px; }
.estado-valor { font-size: 2rem; font-weight: 800; color: #1B3A1F; }
.estado-valor span { font-size: .9rem; font-weight: 600; color: #5d7a60; margin-left: 6px; }
 
.leds { background: #fff; border-radius: 18px; padding: 14px 18px; box-shadow: 0 4px 14px rgba(27,58,31,.08); margin-bottom: 12px; }
.leds-titulo { font-size: .8rem; color: #5d7a60; text-transform: uppercase; letter-spacing: .04em; margin-bottom: 8px; }
.leds-fila { display: flex; gap: 26px; }
.led-item { text-align: center; font-size: .8rem; color: #5d7a60; }
.led { width: 28px; height: 28px; border-radius: 50%; margin: 0 auto 4px; opacity: .22; }
.led.on { opacity: 1; box-shadow: 0 0 16px 3px currentColor; }
 
.rango { position: relative; height: 14px; background: #E0E7DB; border-radius: 999px; margin: 10px 0 4px; }
.rango-banda { position: absolute; top: 0; bottom: 0; background: #A5D6A7; border-radius: 999px; }
.rango-marca { position: absolute; top: -5px; width: 8px; height: 24px; background: #1B3A1F; border-radius: 4px; transform: translateX(-4px); }
.rango-leyenda { display: flex; justify-content: space-between; font-size: .8rem; color: #5d7a60; }
 
.maceta-box { background: #fff; border-radius: 20px; padding: 12px; box-shadow: 0 4px 14px rgba(27,58,31,.08); text-align: center; }
 
[data-testid="stMetric"] { background: #fff; border-radius: 16px; padding: 14px 18px; box-shadow: 0 4px 14px rgba(27,58,31,.08); }
.stButton > button, .stDownloadButton > button { border-radius: 999px; border: 2px solid #2E7D32; background: #fff; color: #1B3A1F; font-weight: 700; padding: .45rem 1.2rem; transition: all .15s ease; }
.stButton > button:hover { background: #2E7D32; color: #fff; border-color: #2E7D32; transform: translateY(-1px); }
.stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"] { background: #2E7D32; color: #fff; }
.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover { background: #1B5E20; }
div[data-testid="stExpander"] { background: #fff; border-radius: 16px; border: none; box-shadow: 0 4px 14px rgba(27,58,31,.08); }
.stTabs [data-baseweb="tab"] { font-weight: 700; }
</style>"""
 
 
def aplicar_estilo():
    st.markdown(CSS, unsafe_allow_html=True)
 
 
def hero(titulo, subtitulo, emoji):
    st.markdown(
        f'<div class="hero"><div class="hero-titulo">{html.escape(titulo)}</div>'
        f'<div class="hero-sub">{html.escape(subtitulo)}</div>'
        f'<div class="hero-emoji">{emoji}</div></div>',
        unsafe_allow_html=True,
    )
 
 
ESTADOS = {
    "seco": ("🥀", "Tu planta tiene sed", "La humedad está por debajo del rango ideal. Es momento de regar."),
    "ok": ("🌿", "Todo en orden", "La humedad está dentro del rango ideal. No hace falta regar."),
    "humedo": ("💦", "Demasiada agua", "La humedad supera el rango ideal. Espera antes de volver a regar."),
}
 
 
def tarjeta_estado(humedad, estado):
    emoji, titulo, detalle = ESTADOS.get(
        estado, ("🌱", "Estado desconocido", "Esperando información del sensor.")
    )
    clase = estado if estado in ESTADOS else ""
    return (
        f'<div class="estado-card {clase}"><div class="estado-emoji">{emoji}</div><div>'
        f'<div class="estado-titulo">{titulo}</div>'
        f'<div class="estado-detalle">{detalle}</div>'
        f'<div class="estado-valor">{humedad:.0f}%<span>de humedad</span></div>'
        f"</div></div>"
    )
 
 
def leds_html(estado):
    items = [
        ("seco", "#E53935", "Regar"),
        ("ok", "#43A047", "Ideal"),
        ("humedo", "#FBC02D", "Exceso"),
    ]
    partes = []
    for clave, color, etiqueta in items:
        encendido = " on" if estado == clave else ""
        partes.append(
            f'<div class="led-item"><div class="led{encendido}" '
            f'style="background:{color};color:{color}"></div>{etiqueta}</div>'
        )
    return (
        '<div class="leds"><div class="leds-titulo">LEDs de la maceta</div>'
        f'<div class="leds-fila">{"".join(partes)}</div></div>'
    )
 
 
def barra_rango(hmin, hmax, valor=None):
    marca = ""
    if valor is not None:
        pos = max(0, min(100, valor))
        marca = f'<div class="rango-marca" style="left:{pos}%"></div>'
    return (
        f'<div class="rango"><div class="rango-banda" style="left:{hmin}%;width:{hmax - hmin}%"></div>{marca}</div>'
        f'<div class="rango-leyenda"><span>0%</span><span>Rango ideal {hmin}% – {hmax}%</span><span>100%</span></div>'
    )
 
 
def maceta_svg(humedad, estado):
    """Maceta con el nivel de agua del sustrato y una planta que cambia con el estado."""
    h = max(0, min(100, humedad))
    hoja = {"ok": "#4CAF50", "humedo": "#2E9C6A", "seco": "#C8A63A"}.get(estado, "#9CCC65")
    angulo = -35 if estado == "seco" else 28  # hojas caídas cuando está seco
    hojas = ""
    for y in (104, 80, 56):
        hojas += (
            f'<ellipse cx="78" cy="{y}" rx="26" ry="10" fill="{hoja}" transform="rotate({angulo} 100 {y})"/>'
            f'<ellipse cx="122" cy="{y}" rx="26" ry="10" fill="{hoja}" transform="rotate({-angulo} 100 {y})"/>'
        )
    svg = (
        '<svg viewBox="0 0 200 250" width="100%" style="max-width:230px">'
        '<defs><clipPath id="macetaClip"><path d="M46 128 L154 128 L141 220 Q139 228 131 228 L69 228 Q61 228 59 220 Z"/></clipPath></defs>'
        '<path d="M100 128 L100 46" stroke="#3E7B3A" stroke-width="5" fill="none" stroke-linecap="round"/>'
        f'{hojas}'
        f'<ellipse cx="100" cy="40" rx="11" ry="19" fill="{hoja}"/>'
        '<g clip-path="url(#macetaClip)">'
        '<rect x="40" y="128" width="120" height="100" fill="#6B4A2B"/>'
        f'<rect x="40" y="{228 - h}" width="120" height="{h}" fill="#4FA3D9" opacity="0.7"/>'
        "</g>"
        '<path d="M46 128 L154 128 L141 220 Q139 228 131 228 L69 228 Q61 228 59 220 Z" fill="none" stroke="#B0562F" stroke-width="6" stroke-linejoin="round"/>'
        '<rect x="34" y="116" width="132" height="18" rx="7" fill="#C8693D"/>'
        "</svg>"
    )
    return f'<div class="maceta-box">{svg}</div>'
 
