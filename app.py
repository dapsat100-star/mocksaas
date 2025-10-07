# -*- coding: utf-8 -*-
# Sidebar SaaS (render via components.html para não virar texto cru)

from datetime import datetime
from base64 import b64encode
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ------- CONFIG -------
st.set_page_config(page_title="DAP ATLAS — Sidebar SaaS", page_icon="🛰️", layout="wide")

PRIMARY   = "#00E3A5"
BG_DARK   = "#0b1221"
CARD_DARK = "#10182b"
TEXT      = "#FFFFFF"
MUTED     = "#9fb0c9"
BORDER    = "rgba(255,255,255,.10)"

PANEL_W_PX   = 560   # largura do painel para o seu print
PANEL_GAP_PX = 24    # distância das bordas

# ------- LOGO -> base64 -------
logo_uri = ""
p = Path("dapatlas.png")
if p.exists() and p.stat().st_size > 0:
    logo_uri = "data:image/png;base64," + b64encode(p.read_bytes()).decode("ascii")

# ------- DADOS MOCK (mude para o print) -------
AOI_ID       = "BR-PA-2025-01"
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

# ------- HTML + CSS standalone (no markdown) -------
html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  :root {{
    --panel-w: {PANEL_W_PX}px;
    --panel-gap: {PANEL_GAP_PX}px;
    --primary: {PRIMARY};
    --bg: {BG_DARK};
    --card: {CARD_DARK};
    --text: {TEXT};
    --muted: {MUTED};
    --border: {BORDER};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; height: 100vh; width: 100vw;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
  }}
  /* fundo bonito p/ o print */
  .stage {{
    height: 100vh; width: 100vw; position: relative;
    background: radial-gradient(1000px 600px at 70% 40%, rgba(255,255,255,.04), transparent 60%),
                radial-gradient(800px 500px at 30% 70%, rgba(255,255,255,.03), transparent 60%);
  }}
  .side-panel {{
    position: absolute;
    top: var(--panel-gap); right: var(--panel-gap); bottom: var(--panel-gap);
    width: var(--panel-w);
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 18px 44px rgba(0,0,0,.45);
    padding: 16px;
    display: flex; flex-direction: column; gap: 10px;
  }}
  .panel-header {{ display:flex; align-items:center; justify-content:space-between; gap:12px; }}
  .brand {{ display:flex; align-items:center; gap:12px; }}
  .logo-wrap {{
    width:42px; height:42px; border-radius:12px; overflow:hidden; background:#0e1628;
    border:1px solid var(--border); display:flex; align-items:center; justify-content:center;
  }}
  .logo-wrap img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .name {{ font-weight:800; letter-spacing:.2px; line-height:1.1; }}
  .sub  {{ font-size:.82rem; color:var(--muted); margin-top:2px; }}
  .badge {{
    background: rgba(0,227,165,.12); color: var(--primary);
    border: 1px solid rgba(0,227,165,.25);
    padding: 6px 10px; border-radius: 999px; font-weight:700; font-size:.85rem; white-space:nowrap;
  }}

  .metrics {{
    display:grid; grid-template-columns: repeat(2, minmax(0,1fr));
    gap: 10px; margin-top: 6px;
  }}
  .metric {{
    background: rgba(255,255,255,.04); border:1px solid var(--border);
    border-radius:14px; padding:12px;
  }}
  .metric .k {{ font-size:1.15rem; font-weight:800; }}
  .metric .l {{ font-size:.85rem; color:var(--muted); }}

  .section-title {{ font-weight:800; margin: 8px 0 2px; }}
  .muted {{ color: var(--muted); }}

  ul.bullets {{ margin:6px 0 0 0; padding-left:1.1rem; }}
  ul.bullets li {{ margin:8px 0; }}

  table.minimal {{ width:100%; border-collapse:collapse; margin-top:6px; }}
  table.minimal th, table.minimal td {{
    border-bottom:1px solid var(--border); padding:9px 6px; text-align:left; font-size:.95rem;
  }}
  table.minimal th {{ color:var(--muted); font-weight:600; }}

  .btn {{
    display:inline-block; background: var(--primary); color:#08121f; font-weight:800;
    padding:10px 14px; border-radius:12px; text-decoration:none; border:none;
  }}

  @media (max-width: 820px) {{
    :root {{ --panel-w: 92vw; }}
  }}
</style>
</head>
<body>
  <div class="stage">
    <div class="side-panel">
      <div class="panel-header">
        <div class="brand">
          <div class="logo-wrap">
            {"<img src='"+logo_uri+"' alt='DAP ATLAS'/>" if logo_uri else "<div style='color:#fff;font-weight:900'>DA</div>"}
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

      <div>
        <div class="muted" style="margin-top:6px;">Resumo</div>
        <p style="margin-top:4px;">
          Detecções sobrepostas à imagem base, com registro geométrico submétrico.
          Pipeline <b>SAR + IA + fusão multi-sensor</b> com atualização em <b>tempo quase-real</b>.
        </p>
      </div>

      <div>
        <div class="section-title">Principais Achados</div>
        <ul class="bullets">
          {''.join(f'<li>{a}</li>' for a in achados)}
        </ul>
      </div>

      <div>
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
</body>
</html>
"""

# render (sem markdown, sem risco de escapar HTML)
components.html(html, height=900, scrolling=False)
