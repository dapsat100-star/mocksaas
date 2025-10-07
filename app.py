# -*- coding: utf-8 -*-
# DAP ATLAS — SITREP (Full Map 100vh + Floating SaaS Panel + PDF + Extensão/Área + texto branco)

import io
from datetime import datetime
import streamlit as st

# Mapa
import folium
from folium import Rectangle, PolyLine
from streamlit_folium import st_folium

# PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, HexColor

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="DAP ATLAS — SITREP",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ================== THEME ==================
PRIMARY = "#00E3A5"
BG_DARK = "#0b1221"
CARD_DARK = "#10182b"
TEXT = "#FFFFFF"      # branco puro
MUTED = "#9fb0c9"
BORDER = "rgba(255,255,255,.10)"

# ================== CSS (com hotfix anti-corte) ==================
st.markdown(f"""
<style>
  .block-container {{ padding: 0; max-width: 100%; }}
  body {{ background:{BG_DARK}; color:{TEXT}; }}

  /* Mapa ocupa a janela toda; sobreposição do painel por padrão */
  .full-map {{
    position: relative;
    height: 100vh;
    width: 100%;
    border-bottom: 1px solid {BORDER};
    padding-right: 0;                /* opcional: 560px para o mapa "desviar" do painel */
    box-sizing: border-box;
  }}

  /* Painel SaaS flutuante (respeita safe-area e não corta em baixo) */
  .side-panel {{
    position: fixed;
    top: max(14px, env(safe-area-inset-top));
    right: max(14px, env(safe-area-inset-right));
    bottom: max(14px, env(safe-area-inset-bottom));
    width: min(520px, 38vw);
    max-height: none;                 /* bottom controla a altura total */
    overflow: auto;
    background: {CARD_DARK};
    border: 1px solid {BORDER};
    box-shadow: 0 18px 44px rgba(0,0,0,.45);
    border-radius: 18px;
    padding: 16px;
    z-index: 999;
    color:{TEXT};
    box-sizing: border-box;
  }}
  .side-panel h2 {{ margin: 0 0 10px 0; }}
  .muted {{ color:{MUTED}; }}

  /* Appbar */
  .appbar {{
    position: fixed;
    left: max(14px, env(safe-area-inset-left));
    top:  max(14px, env(safe-area-inset-top));
    z-index: 998;
    background: rgba(16,24,43,.78);
    border: 1px solid {BORDER};
    border-radius: 999px;
    padding: 8px 14px;
    display:flex; align-items:center; gap:10px;
    backdrop-filter: blur(6px);
    color:{TEXT};
  }}
  .badge {{
    background: rgba(0,227,165,.12);
    color:{PRIMARY};
    border: 1px solid rgba(0,227,165,.25);
    padding: 6px 10px; border-radius: 999px; font-weight: 700; font-size:.85rem;
  }}

  .metrics {{
    display:grid; grid-template-columns: repeat(2, minmax(0,1fr));
    gap: 8px; margin: 10px 0 6px;
  }}
  .metric {{
    background: rgba(255,255,255,.04);
    border: 1px solid {BORDER};
    border-radius: 14px; padding: 10px;
    color:{TEXT};
  }}
  .metric .k {{ font-size: 1.1rem; font-weight: 800; }}
  .metric .l {{ font-size:.85rem; color:{MUTED}; }}

  table.minimal {{ width:100%; border-collapse: collapse; margin-top: 6px; color:{TEXT}; }}
  table.minimal th, table.minimal td {{
    border-bottom: 1px solid {BORDER};
    padding: 8px 6px; text-align: left; font-size: .95rem;
  }}
  table.minimal th {{ color:{MUTED}; font-weight: 600; }}

  .bullets {{ margin: 4px 0 0 0; padding-left: 1.1rem; }}
  .bullets li {{ margin: 8px 0; }}

  /* Responsivo */
  @media (max-width: 1200px) {{ .side-panel {{ width: min(480px, 46vw); }} }}
  @media (max-width: 992px)  {{ .side-panel {{ width: min(420px, 54vw); }} }}
</style>
""", unsafe_allow_html=True)

# ================== DADOS (exemplo) ==================
AOI_ID = "BR-PA-2025-01"
local = "XPTO"
data_local = "07/06/2025 – 09:25"
sensor = "BlackSky Global-16 (Sensor: Global-16)"
resolucao = "35 cm"
confianca = "92%"
extensao_km = "12.4 km"
area_km2 = "26.8 km²"
ultima_atualizacao = datetime.now().strftime("%d/%m %H:%M")
achados = [
    "Vias lineares abertas e ramificações não oficiais indicando pressão antrópica.",
    "Clareiras múltiplas conectadas às vias (abertura recente provável).",
    "Aglomerados habitacionais sugerindo presença humana ativa.",
    "Pista de pouso estimada entre 750–850 m (operação de aeronaves leves).",
]

# ================== MAPA ==================
center_latlon = (-6.6756, -57.6647)
m = folium.Map(location=center_latlon, zoom_start=12, tiles="CartoDB.DarkMatter")

# overlays de exemplo (substitua pelos seus vetores/geojson)
PolyLine(
    locations=[(-6.665, -57.70), (-6.662, -57.675)],
    color=PRIMARY, weight=4, tooltip="Pista (estimada)"
).add_to(m)

Rectangle(
    bounds=[(-6.70, -57.71), (-6.66, -57.67)],
    color="#ffd95a", weight=2, fill=False, tooltip="AOI principal"
).add_to(m)

# ================== APPBAR ==================
st.markdown(
    f"""
    <div class="appbar">
      <div style="font-weight:800;">DAP ATLAS — SITREP</div>
      <div class="badge">AOI {AOI_ID} • Live 24/7</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================== MAPA FULL (altura real) ==================
st.markdown('<div class="full-map">', unsafe_allow_html=True)
st_folium(m, height=820, width=None)   # altura real do iframe do Folium (720–900 ok)
st.markdown('</div>', unsafe_allow_html=True)

# ================== PAINEL SAAS ==================
st.markdown(
    f"""
    <div class="side-panel">
      <h2 style="display:flex;align-items:center;justify-content:space-between;">
        <span>Relatório de Situação</span>
        <span class="muted" style="font-weight:600;">Radar SAR + IA</span>
      </h2>

      <div class="metrics">
        <div class="metric"><div class="k">{confianca}</div><div class="l">Confiança</div></div>
        <div class="metric"><div class="k">{extensao_km}</div><div class="l">Extensão</div></div>
        <div class="metric"><div class="k">{area_km2}</div><div class="l">Área</div></div>
        <div class="metric"><div class="k">{resolucao}</div><div class="l">Resolução</div></div>
      </div>

      <p class="muted" style="margin:.2rem 0 .3rem;">Resumo</p>
      <p>
        A cena mostra detecções sobrepostas à imagem base, com registro geométrico submétrico.
        O pipeline combina <b>SAR + IA + fusão multi-sensor</b> para gerar insights acionáveis em <b>tempo quase-real</b>.
      </p>

      <h4>Principais Achados</h4>
      <ul class="bullets">
        {"".join(f"<li>{item}</li>" for item in achados)}
      </ul>

      <h4 style="margin-top:12px;">Metadados</h4>
      <table class="minimal">
        <tr><th>Local</th><td>{local}</td></tr>
        <tr><th>Data/Hora</th><td>{data_local}</td></tr>
        <tr><th>Fonte</th><td>{sensor}</td></tr>
        <tr><th>Extensão</th><td>{extensao_km}</td></tr>
        <tr><th>Área</th><td>{area_km2}</td></tr>
        <tr><th>Resolução</th><td>{resolucao}</td></tr>
        <tr><th>Sistema</th><td>DAP ATLAS — SITREP</td></tr>
      </table>
    """,
    unsafe_allow_html=True,
)

# ================== PDF EXPORT ==================
def build_pdf() -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4
    margin = 1.6 * cm
    primary = HexColor(PRIMARY)

    # Faixa topo
    c.setFillColor(primary); c.rect(0, H-2.1*cm, W, 2.1*cm, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 16); c.setFillColorRGB(1,1,1)
    c.drawString(margin, H-1.5*cm, f"DAP ATLAS — SITREP  •  AOI {AOI_ID}")
    c.setFont("Helvetica", 10)
    c.drawRightString(W - margin, H-1.4*cm, datetime.now().strftime("%d/%m/%Y %H:%M"))

    # Metadados
    y = H - 3.2*cm
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12); c.drawString(margin, y, "Metadados")
    y -= 0.4*cm; c.setFont("Helvetica", 10)
    meta = [
        f"Local: {local}",
        f"Data/Hora: {data_local}",
        f"Fonte: {sensor}",
        f"Extensão: {extensao_km}",
        f"Área: {area_km2}",
        f"Resolução: {resolucao}",
        "Sistema: DAP ATLAS — SITREP",
    ]
    for ln in meta:
        c.drawString(margin, y, ln); y -= 0.4*cm

    # Achados
    y -= 0.3*cm
    c.setFont("Helvetica-Bold", 12); c.drawString(margin, y, "Principais Achados")
    y -= 0.5*cm; c.setFont("Helvetica", 10)
    for item in achados:
        c.drawString(margin+10, y, u"• " + item); y -= 0.5*cm

    c.showPage(); c.save(); buffer.seek(0)
    return buffer.getvalue()

pdf_bytes = build_pdf()
st.download_button(
    label="📄 Exportar PDF",
    data=pdf_bytes,
    file_name=f"SITREP_{AOI_ID}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
    mime="application/pdf",
    use_container_width=True,
    key="export_pdf_dl",
)

# Fecha a div do painel após o botão
st.markdown("</div>", unsafe_allow_html=True)

# ================== FOOTER ==================
st.markdown(
    f"""
    <div style="position:fixed; left:max(14px, env(safe-area-inset-left)); bottom:max(14px, env(safe-area-inset-bottom)); color:{MUTED}; font-size:.86rem;">
      © {datetime.now().year} MAVIPE Sistemas Espaciais — DAP ATLAS
    </div>
    """,
    unsafe_allow_html=True,
)


