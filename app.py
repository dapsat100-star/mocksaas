# -*- coding: utf-8 -*-
# DAP ATLAS — Sidebar SaaS (large logo + CSS tabs + internal scroll + EXPORT SVG/PDF via shortcuts)

from datetime import datetime
from base64 import b64encode
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — Sidebar SaaS", page_icon="🛰️", layout="wide")

# ======= Theme
PRIMARY   = "#00E3A5"
BG_DARK   = "#0b1221"
CARD_DARK = "#10182b"
TEXT      = "#FFFFFF"
MUTED     = "#9fb0c9"
BORDER    = "rgba(255,255,255,.10)"

PANEL_W_PX   = 560
PANEL_GAP_PX = 24

# ======= Logo (png with white background)
logo_uri = ""
p = Path("dapatlas_fundo_branco.png")
if p.exists() and p.stat().st_size > 0:
    logo_uri = "data:image/png;base64," + b64encode(p.read_bytes()).decode("ascii")

# ======= Data
AOI_ID       = "BR-PA-2025-01"
confidence   = "95%"
extent_km    = "5 km"
area_km2     = "25 km²"
resolution   = "35 cm"
location     = "Scene 5 × 5 km"
acq_datetime = "2025-06-07 – 09:25"
sensor       = "BlackSky Global-16 (Sensor: Global-16)"
now_label    = datetime.now().strftime("%d/%m %H:%M")

# ======= Findings (suited to roads/clearings/settlements/airstrip case)
findings = [
    "Linear roads opened through vegetation, with signs of recent opening or continuous use — consistent with anthropic pressure (logging, mining, or irregular occupation).",
    "Clearings of different sizes, some connected to the aforementioned roads.",
    "Dispersed residential clusters, suggesting active human presence.",
    "Airstrip with estimated length between ~750 and 850 m; width compatible with small aircraft operations.",
    "The airstrip connects to an irregular road network and deforested areas, reinforcing the structure’s logistical character."
]

# ======= HTML/JS (with export via S and P shortcuts)
html = f"""
<!doctype html>
<html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
:root {{
  --panel-w:{PANEL_W_PX}px; --gap:{PANEL_GAP_PX}px;
  --primary:{PRIMARY}; --bg:{BG_DARK}; --card:{CARD_DARK};
  --text:{TEXT}; --muted:{MUTED}; --border:{BORDER};
}}
*{{box-sizing:border-box}}
body{{margin:0;height:100vh;width:100vw;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Inter,Helvetica Neue,Arial,Noto Sans,sans-serif}}
.stage{{height:100vh;width:100vw;position:relative;
  background:radial-gradient(1000px 600px at 70% 40%,rgba(255,255,255,.04),transparent 60%),
             radial-gradient(800px 500px at 30% 70%,rgba(255,255,255,.03),transparent 60%)}}
.side-panel{{
  position:absolute; top:var(--gap); right:var(--gap); bottom:var(--gap);
  width:var(--panel-w); background:var(--card); border:1px solid var(--border);
  border-radius:18px; box-shadow:0 18px 44px rgba(0,0,0,.45);
  padding:16px; display:flex; flex-direction:column; gap:12px;
  overflow:auto;               /* internal scroll, no clipping */
}}
.panel-header{{display:flex;align-items:center;justify-content:space-between;gap:18px}}
.brand{{display:flex;align-items:center;gap:18px}}
.logo-wrap{{width:80px;height:80px;border-radius:18px;overflow:hidden;background:#fff;
  border:1px solid var(--border);display:flex;align-items:center;justify-content:center}}
.logo-wrap img{{width:100%;height:100%;object-fit:contain;display:block}}
.name{{font-weight:800;letter-spacing:.2px;line-height:1.1;font-size:1.1rem}}
.sub{{font-size:.82rem;color:var(--muted);margin-top:2px}}
.badge{{background:rgba(0,227,165,.12);color:var(--primary);border:1px solid rgba(0,227,165,.25);
  padding:6px 10px;border-radius:999px;font-weight:700;font-size:.85rem;white-space:nowrap}}
.metrics{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:6px}}
.metric{{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:14px;padding:12px}}
.metric .k{{font-size:1.15rem;font-weight:800}}
.metric .l{{font-size:.85rem;color:var(--muted)}}

/* ======= Tabs (CSS-only) ======= */
.tabs{{margin-top:6px}}
.tabs input{{display:none}}
.tabs label{{
  display:i
