# -*- coding: utf-8 -*-
# DAP ATLAS – SITREP (Full-width Map + Floating SaaS Panel + Export PDF)

import io
from datetime import datetime
from pathlib import Path

import streamlit as st

# —— mapa
import folium
from folium import GeoJson, Rectangle, PolyLine
from streamlit_folium import st_folium

# —— PDF
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

# ================== THEME & CSS ==================
PRIMARY = "#00E3A5"
BG_DARK = "#0b1221"
CARD_DARK = "#10182b"
TEXT = "#E6EEFC"
MUTED = "#9fb0c9"
BORDER = "rgba(255,255,255,.10)"

st.markdown(
    f"""
    <style>
      .block-container {{
        padding: 0;
        max-width: 100%;
      }}
      body {{ background:{BG_DARK}; color:{TEXT}; }}

      /* Mapa em full width */
      .full-map {{
        position: relative;
        height: calc(100vh - 0px);
        width: 100%;
        overflow: hidden;
        border-bottom: 1px solid {BORDER};
      }}

      /* Painel SaaS flutuante (direita) */
      .side-panel {{
        position: fixed;
        top: 14px; right: 14px;
        width: min(520px, 38vw);
        max-height: calc(100vh - 28px);
        overflow: auto;
        background: {CARD_DARK};
        border: 1px solid {BORDER};
        box-shadow: 0 18px 44px rgba(0,0,0,.45);
        border-radius: 18px;
        padding: 16px 16px 12px 16px;
        z-index: 999;
      }}
      .side-panel h2 {{ margin: 0 0 10px 0; }}
      .muted {{ color: {MUTED}; }}

      .appbar {{
        position: fixed; left: 14px; top: 14px; z-index: 998;
        background: rgba(16,24,43,.78);
        border: 1px solid {BORDER};
        border-radius: 999px;
        padding: 8px 14px;
        display:flex; align-items:center; gap:10px;
        backdrop-filter: blur(6px);
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
      }}
      .metric .k {{ font-size: 1.1rem; font-weight: 800; }}
      .metric .l {{ font-size:.85rem; color:{MUTED}; }}

      .actions {{ display:flex; gap:8px; flex-wrap: wrap; margin-top: 8px; }}
      .btn {{
        background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
        border: 1px solid {BORDER}; color:{TEXT};
        padding: 9px 12px; border-radius: 10px;
        font-weight: 700; text-decoration: none; font-size:.92rem;
      }}
      .btn.primary {{ background:{PRIMARY}; color:#08121f; border:none; }}

      table.minimal {{ width:100%; border-collapse: collapse; margin-top: 6px; }}
      table.minimal th, table.minimal td {{
        border-bottom: 1px solid {BORDER};
        padding: 8px 6px; text-align: left; font-size: .95rem;
      }}
      table.minimal th {{ color:{MUTED}; font-weight: 600; }}

      .bullets {{ margin: 4px 0 0 0; padding-left: 1.1rem; }}
      .bullets li {{ margin: 8px 0; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ================== DATA (EXEMPLO / TROCAR PELO PIPELINE) ==================
AOI_ID = "BR-PA-2025-01"
local = "XPTO"
data_local = "07/06/2025 – 09:25"
sensor = "BlackSky Global-16 (Sensor: Global-16)"
resolucao = "35 cm"
confianca = "92%"
extensao_km = "26.8 km"
ultima_atualizacao = datetime.now().strftime("%d/%m %H:%M")

achados = [
    "Vias lineares abertas e ramificações não oficiais indicando pressão antrópica.",
    "Clareiras múltiplas conectadas às vias (abertura recente provável).",
    "Aglomerados habitacionais sugerindo presença humana ativa.",
    "Pista de pouso estimada entre 750–850 m (operação de aeronaves leves).",
]

# ================== MAPA (FOLIUM) ==================
# centro próximo ao exemplo da screenshot
center_latlon = (-6.6756, -57.6647)

m = folium.Map(location=center_latlon, zoom_start=12, tiles="CartoDB.DarkMatter")

# —— exemplo de overlay: pista (linha), AOIs (retângulos) — substitua pelos seus vetores
PolyLine(
    locations=[(-6.665, -57.70), (-6.662, -57.675)],
    color="#00E3A5",
    weight=4,
    tooltip="Pista (estimada)",
).add_to(m)

Rectangle(
    bounds=[(-6.70, -57.71), (-6.66, -57.67)],
    color="#ffd95a",
    weight=2,
    fill=False,
    tooltip="AOI principal",
).add_to(m)

Rectangle(
    bounds=[(-6.682, -57.685), (-6.675, -57.676)],
    color="#ffd95a",
    weight=2,
    fill=False,
    tooltip="Box de inspeção",
).add_to(m)

# ================== LAYOUT ==================
# appbar (esquerda)
st.markdown(
    f"""
    <div class="appbar">
      <div style="font-weight:800;">DAP ATLAS — SITREP</div>
      <div class="badge">AOI {AOI_ID} • Live 24/7</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# mapa full
with st.container():
    st.markdown('<div class="full-map">', unsafe_allow_html=True)
    st_folium(m, height=0, width=0)  # o CSS da div pai controla a altura/largura
    st.markdown('</div>', unsafe_allow_html=True)

# painel flutuante (conteúdo HTML + elementos streamlit)
st.markdown(
    f"""
    <div class="side-panel">
      <h2 style="display:flex;align-items:center;justify-content:space-between;">
        <span>Relatório de Situação</span>
        <span style="font-size:.95rem;color:{MUTED};font-weight:600;">Radar SAR + IA</span>
      </h2>

      <div class="metrics">
        <div class="metric"><div class="k">{confianca}</div><div class="l">Confiança</div></div>
        <div class="metric"><div class="k">{extensao_km}</div><div class="l">Extensão (estim.)</div></div>
        <div class="metric"><div class="k">{resolucao}</div><div class="l">Resolução</div></div>
        <div class="metric"><div class="k">{ultima_atualizacao}</div><div class="l">Última atualização</div></div>
      </div>

      <p class="muted" style="margin:.2rem 0 .3rem;">Resumo</p>
      <p style="margin-top:0">
        A cena mostra detecções sobrepostas à imagem base, com registro geométrico submétrico.
        O pipeline combina <b>SAR + IA + fusão multi-sensor</b> para gerar insights acionáveis em <b>tempo quase-real</b>.
      </p>

      <h4 style="margin-top:10px;">Principais Achados</h4>
      <ul class="bullets">
        {"".join(f"<li>{item}</li>" for item in achados)}
      </ul>

      <h4 style="margin-top:12px;">Metadados</h4>
      <table class="minimal">
        <tr><th>Local</th><td>{local}</td></tr>
        <tr><th>Data/Hora (local)</th><td>{data_local}</td></tr>
        <tr><th>Fonte</th><td>{sensor}</td></tr>
        <tr><th>Resolução Espacial</th><td>{resolucao}</td></tr>
        <tr><th>Sistema</th><td>DAP ATLAS — SITREP</td></tr>
      </table>
    """,
    unsafe_allow_html=True,
)

# ================== EXPORT PDF (REPORTLAB) ==================
def build_pdf() -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4
    margin = 1.6 * cm

    # Paleta PDF (segue a do painel)
    primary = HexColor(PRIMARY)
    text = black

    # Cabeçalho
    c.setFillColor(primary); c.rect(0, H-2.1*cm, W, 2.1*cm, stroke=0, fill=1)
    c.setFillColorRGB(0.05, 0.09, 0.16)  # fundo faixa de título
    c.rect(0, H-3.5*cm, W, 1.4*cm, stroke=0, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, H-2.8*cm, "DAP ATLAS — SITREP (Export)")
    c.setFont("Helvetica", 10)
    c.drawRightString(W - margin, H-2.8*cm, datetime.now().strftime("%d/%m/%Y %H:%M"))

    # Bloco Metadados
    y = H - 4.2*cm
    c.setFillColor(text)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Metadados")
    y -= 0.5*cm
    c.setFont("Helvetica", 10)
    lines = [
        f"AOI: {AOI_ID}",
        f"Local: {local}",
        f"Data/Hora (local): {data_local}",
        f"Fonte: {sensor}",
        f"Resolução Espacial: {resolucao}",
        "Sistema: DAP ATLAS — SITREP",
    ]
    for ln in lines:
        c.drawString(margin, y, ln)
        y -= 0.42*cm

    # Bloco Métricas
    y -= 0.3*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Métricas")
    y -= 0.5*cm
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, f"Confiança: {confianca}")
    y -= 0.42*cm
    c.drawString(margin, y, f"Extensão (estim.): {extensao_km}")
    y -= 0.42*cm
    c.drawString(margin, y, f"Última atualização: {ultima_atualizacao}")

    # Bloco Achados
    y -= 0.7*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Principais Achados")
    y -= 0.55*cm
    c.setFont("Helvetica", 10)
    bullet = u"\u2022"
    for item in achados:
        # quebra simples por largura
        max_width = W - 2*margin
        words = item.split()
        row = ""
        for w in words:
            if c.stringWidth((row + " " + w).strip(), "Helvetica", 10) < max_width:
                row = (row + " " + w).strip()
            else:
                c.drawString(margin+10, y, row)
                y -= 0.42*cm
                row = w
        if row:
            c.drawString(margin+10, y, row)
            y -= 0.55*cm

    # Observações
    if y < 3*cm:
        c.showPage()
        y = H - margin
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Observações")
    y -= 0.5*cm
    c.setFont("Helvetica", 10)
    obs = "Export automático gerado pela plataforma DAP ATLAS. Substitua este texto pelas observações do pipeline."
    # wrap simples
    words = obs.split()
    row = ""
    while words:
        w = words.pop(0)
        if c.stringWidth((row + " " + w).strip(), "Helvetica", 10) < (W - 2*margin):
            row = (row + " " + w).strip()
        else:
            c.drawString(margin, y, row)
            y -= 0.42*cm
            row = w
    if row:
        c.drawString(margin, y, row)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

pdf_bytes = build_pdf()
st.download_button(
    label="Exportar PDF",
    data=pdf_bytes,
    file_name=f"SITREP_{AOI_ID}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
    mime="application/pdf",
    type="primary",
    use_container_width=True,
    key="export_pdf_dl",
)

# fecha o div do painel após os componentes Streamlit
st.markdown("</div>", unsafe_allow_html=True)

# ======== DICAS DE INTEGRAÇÃO ========
st.markdown(
    f"""
    <div style="position:fixed; left:14px; bottom:14px; color:{MUTED}; font-size:.86rem;">
      © {datetime.now().year} MAVIPE Sistemas Espaciais — DAP ATLAS
    </div>
    """,
    unsafe_allow_html=True,
)
