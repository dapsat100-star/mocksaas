# -*- coding: utf-8 -*-
# DAP ATLAS — Sidebar SaaS (mock para screenshot)

from datetime import datetime
from base64 import b64encode
from pathlib import Path
import streamlit as st

# ========= THEME =========
PRIMARY   = "#00E3A5"
BG_DARK   = "#0b1221"
CARD_DARK = "#10182b"
TEXT      = "#FFFFFF"
MUTED     = "#9fb0c9"
BORDER    = "rgba(255,255,255,.10)"

PANEL_W_PX   = 560   # ajuste a largura do painel p/ o seu print
PANEL_GAP_PX = 24    # distância da borda

# ========= PAGE =========
st.set_page_config(page_title="DAP ATLAS — Sidebar SaaS", page_icon="🛰️", layout="wide")

# ========= LOGO =========
def logo_data_uri(path="dapatlas.png"):
    p = Path(path)
    if p.exists() and p.stat().st_size > 0:
        return "data:image/png;base64," + b64encode(p.read_bytes()).decode("ascii")
    return None
LOGO_URI = logo_data_uri()

# ========= CSS (apenas o painel) =========
st.markdown(f"""
<style>
  :root {{
    --panel-w: {PANEL_W_PX}px;
    --panel-gap: {PANEL_GAP_PX}px;
  }}

  .block-container {{ padding: 0; max-width: 100%; }}
  body {{ background:{BG_DARK}; color:{TEXT}; }}

  /* Fundo com leve vinheta para ficar bonito no print */
  .stage {{
    height: 100vh; width: 100%;
    background: radial-gradient(1000px 600px at 70% 40%, rgba(255,255,255,.04), transparent 60%),
                radial-gradient(800px 500px at 30% 70%, rgba(255,255,255,.03), transparent 60%);
    position: relative;
  }}

  .side-panel {{
    position: absolute;
    top: var(--panel-gap);
    right: var(--panel-gap);
    bottom: var(--panel-gap);
    width: var(--panel-w);
    background: {CARD_DARK};
    border: 1px solid {BORDER};
    border-radius: 18px;
    box-shadow: 0 18px 44px rgba(0,0,0,.45);
    padding: 16px;
    color: {TEXT};
    display: flex; flex-direction: column; gap: 10px;
  }}

  .panel-header {{ display:flex; align-items:center; justify-content:space-between; gap:12px; }}
  .brand {{ display:flex; align-items:center; gap:12px; }}
  .logo-wrap {{
    width:42px; height:42px; border-radius:12px; overflow:hidden; background:#0e1628;
    border:1px solid {BORDER}; display:flex; align-items:center; justify-content:center;
  }}
  .logo-wrap img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .name {{ font-weight:800; letter-spacing:.2px; line-height:1.1; }}
  .sub  {{ font-size:.82rem; color:{MUTED}; margin-top:2px; }}

  .badge {{
    background: rgba(0,227,165,.12);
    color:{PRIMARY};
    border: 1px solid rgba(0,227,165,.25);
    padding: 6px 10px; border-radius: 999px; font-weight: 700; font-size:.85rem; white-space:nowrap;
  }}

  .metrics {{
    display:grid; grid-template-columns: repeat(2, minmax(0,1fr));
    gap: 10px; margin-top: 6px;
  }}
  .metric {{
    background: rgba(255,255,255,.04);
    border: 1px solid {BORDER};
    border-radius: 14px; padding: 12px;
  }}
  .metric .k {{ font-size: 1.15rem; font-weight: 800; }}
  .metric .l {{ font-size:.85rem; color:{MUTED}; }}

  .section-title {{ font-weight:800; margin: 8px 0 2px; }}
  .muted {{ color:{MUTED}; }}

  ul.bullets {{ margin: 6px 0 0 0; padding-left: 1.1rem; }}
  ul.bullets li {{ margin: 8px 0; }}

  table.minimal {{ width:100%; border-collapse: collapse; margin-top: 6px; color:{TEXT}; }}
  table.minimal th, table.minimal td {{
    border-bottom: 1px solid {BORDER};
    padding: 9px 6px; text-align: left; font-size: .95rem;
  }}
  table.minimal th {{ color:{MUTED}; font-weight: 600; }}

  /* botão fake só pro look (não funcional) */
  .btn {{
    display:inline-block; background:{PRIMARY}; color:#08121f; font-weight:800;
    padding:10px 14px; border-radius:12px; text-decoration:none; border:none;
  }}

  /* ajuda no print de browser */
  @media print {{
    .stage {{ background: #0b1221 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
</style>
""", unsafe_allow_html=True)

# ========= DADOS MOCK (edite para o print) =========
AOI_ID = "BR-PA-2025-01"
confianca    = "92%"
extensao_km  = "12.4 km"
area_km2     = "26.8 km²"
resolucao    = "35 cm"
local        = "XPTO"
data_hora    = "07/06/2025 – 09:25"
sensor       = "BlackSky Global-16 (Sensor: Global-16)"
agora        = datetime.now().strftime("%d/%m %H:%M")

achados = [
    "Vias lineares abertas e ramificações não oficiais indicando pressão antrópica.",
    "Clareiras múltiplas conectadas às vias (abertura recente provável).",
    "Aglomerados habitacionais sugerindo presença humana ativa.",
    "Pista de pouso estimada entre 750–850 m (operação de aeronaves leves).",
]

# ========= HTML DO PAINEL =========
panel_html = f"""
<div class="stage">
  <div class="side-panel">
    <div class="panel-header">
      <div class="brand">
        <div class="logo-wrap">
          {"<img src='"+LOGO_URI+"' alt='DAP ATLAS'/>" if LOGO_URI else "<div style='color:#fff;font-weight:900;'>DA</div>"}
        </div>
        <div>
          <div class="name">Relatório de Situação</div>
          <div class="sub">Radar SAR + IA</div>
        </div>
      </div>
      <div class="badge">AOI {AOI_ID} • Live 24/7</div>
    </div>

    <div class="metrics">
      <div class="metric"><div class="k">{confianca}</div><div class="l">Confiança</div></div>
      <div class="metric"><div class="k">{extensao_km}</div><div class="l">Extensão</div></div>
      <div class="metric"><div class="k">{area_km2}</div><div class="l">Área</div></div>
      <div class="metric"><div class="k">{resolucao}</div><div class="l">Resolução</div></div>
    </div>

    <div class="section">
      <div class="muted" style="margin-top:6px;">Resumo</div>
      <p style="margin-top:4px;">
        Detecções sobrepostas à imagem base, com registro geométrico submétrico.
        Pipeline <b>SAR + IA + fusão multi-sensor</b> com atualização em <b>tempo quase-real</b>.
      </p>
    </div>

    <div class="section">
      <div class="section-title">Principais Achados</div>
      <ul class="bullets">
        {"".join(f"<li>{a}</li>" for a in achados)}
      </ul>
    </div>

    <div class="section">
      <div class="section-title">Metadados</div>
      <table class="minimal">
        <tr><th>Local</th><td>{local}</td></tr>
        <tr><th>Data/Hora</th><td>{data_hora}</td></tr>
        <tr><th>Fonte</th><td>{sensor}</td></tr>
        <tr><th>Geração</th><td>{agora}</td></tr>
        <tr><th>Sistema</th><td>DAP ATLAS — SITREP</td></tr>
      </table>
    </div>

    <div style="margin-top:auto; display:flex; justify-content:space-between; align-items:center; gap:10px;">
      <div class="muted" style="font-size:.85rem;">© {datetime.now().year} MAVIPE Sistemas Espaciais</div>
      <a class="btn" href="#">Exportar PDF</a>
    </div>
  </div>
</div>
"""

st.markdown(panel_html, unsafe_allow_html=True)
