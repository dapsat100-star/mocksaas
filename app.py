# -*- coding: utf-8 -*-
# DAP ATLAS — Sidebar SaaS (large logo + CSS tabs + internal scroll + EXPORT SVG/PDF/PNG via shortcuts)

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

# ======= Findings
findings = [
    "Linear roads opened through vegetation, with signs of recent opening or continuous use — consistent with anthropic pressure (logging, mining, or irregular occupation).",
    "Clearings of different sizes, some connected to the aforementioned roads.",
    "Dispersed residential clusters, suggesting active human presence.",
    "Airstrip with estimated length between ~750 and 850 m; width compatible with small aircraft operations.",
    "The airstrip connects to an irregular road network and deforested areas, reinforcing the structure’s logistical character."
]

# ======= HTML
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
  overflow:auto;
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
.tabs{{margin-top:6px}}
.tabs input{{display:none}}
.tabs label{{
  display:inline-block; padding:8px 12px; margin-right:8px; border:1px solid var(--border);
  border-bottom:none; border-top-left-radius:10px; border-top-right-radius:10px;
  color:var(--muted); background:rgba(255,255,255,.02); cursor:pointer; font-weight:700; font-size:.92rem
}}
.tabs input:checked + label{{color:#08121f; background:var(--primary); border-color:var(--primary)}}
.tab-content{{border:1px solid var(--border); border-radius:0 12px 12px 12px; padding:12px; margin-top:-1px}}
ul.bullets{{margin:6px 0 0 0; padding-left:1.1rem}} ul.bullets li{{margin:8px 0}}
.section-title{{font-weight:800; margin: 2px 0 8px}}
table.minimal{{width:100%;border-collapse:collapse;margin-top:2px}}
table.minimal th, table.minimal td{{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:.95rem}}
table.minimal th{{color:var(--muted);font-weight:600}}
.footer{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:10px}}
.small{{font-size:.85rem}}
</style>
</head>
<body>
  <div class="stage">
    <div class="side-panel" id="panel">
      <div class="panel-header">
        <div class="brand">
          <div class="logo-wrap">
            {"<img src='"+logo_uri+"' alt='DAP ATLAS'/>" if logo_uri else "<div style='color:#000;font-weight:900'>DA</div>"}
          </div>
          <div>
            <div class="name">Situation Report</div>
            <div class="sub">Optical Imagery + AI</div>
          </div>
        </div>
        <div class="badge">AOI {AOI_ID} • Live 24/7</div>
      </div>

      <div class="metrics">
        <div class="metric"><div class="k">{confidence}</div><div class="l">Confidence</div></div>
        <div class="metric"><div class="k">{extent_km}</div><div class="l">Extent</div></div>
        <div class="metric"><div class="k">{area_km2}</div><div class="l">Area</div></div>
        <div class="metric"><div class="k">{resolution}</div><div class="l">Resolution</div></div>
      </div>

      <div class="tabs">
        <input type="radio" name="tab" id="tab-findings" checked>
        <label for="tab-findings">Key Findings</label>
        <input type="radio" name="tab" id="tab-meta">
        <label for="tab-meta">Metadata</label>
        <input type="radio" name="tab" id="tab-summary">
        <label for="tab-summary">Summary</label>

        <div class="tab-content" id="content-findings">
          <ul class="bullets">{''.join(f'<li>{a}</li>' for a in findings)}</ul>
        </div>
        <div class="tab-content" id="content-meta" style="display:none"></div>
        <div class="tab-content" id="content-summary" style="display:none"></div>
      </div>

      <div class="footer">
        <div class="muted small">© {datetime.now().year} MAVIPE Space Systems</div>
        <div class="muted small">Shortcuts: S (SVG) • P (PDF) • G (PNG)</div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/dom-to-image-more@2.8.0/dist/dom-to-image-more.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/svg2pdf.js@2.2.3/dist/svg2pdf.umd.min.js"></script>

  <script>
    const findingsEl = document.getElementById('content-findings');
    const metaEl     = document.getElementById('content-meta');
    const summaryEl  = document.getElementById('content-summary');
    function show(which){{
      findingsEl.style.display=(which==='f')?'block':'none';
      metaEl.style.display=(which==='m')?'block':'none';
      summaryEl.style.display=(which==='s')?'block':'none';
    }}
    document.getElementById('tab-findings').onchange=()=>show('f');
    document.getElementById('tab-meta').onchange=()=>show('m');
    document.getElementById('tab-summary').onchange=()=>show('s');

    metaEl.innerHTML=`<div class="section-title">Metadata</div>
      <table class="minimal">
        <tr><th>Location</th><td>{location}</td></tr>
        <tr><th>Acquisition Time</th><td>{acq_datetime}</td></tr>
        <tr><th>Source</th><td>{sensor}</td></tr>
        <tr><th>Generated</th><td>{now_label}</td></tr>
        <tr><th>System</th><td>DAP ATLAS — SITREP</td></tr>
      </table>`;
    summaryEl.innerHTML=`<div class="section-title">Summary</div>
      <p>Evidence of <b>anthropic pressure</b> and related logistics: recent road openings,
      <b>connected clearings</b>, <b>residential clusters</b>, and an <b>airstrip (~750–850 m)</b>
      linked through an irregular road network. <b>Optical Imagery + AI</b> pipeline with
      <b>near-real-time</b> updates.</p>`;

    const PANEL=document.getElementById('panel');

    async function exportSVG() {{
      const dataUrl=await domtoimage.toSvg(PANEL,{{bgcolor:'{CARD_DARK}',quality:1}});
      triggerDownload(dataUrl,'SITREP_Panel.svg');
    }}
    async function exportPDF() {{
      const svgUrl=await domtoimage.toSvg(PANEL,{{bgcolor:'{CARD_DARK}',quality:1}});
      const svgText=await (await fetch(svgUrl)).text();
      const {{jsPDF}}=window.jspdf;
      const pdf=new jsPDF({{unit:'pt',format:'a4',orientation:'p'}});
      const parser=new DOMParser();
      const svgDoc=parser.parseFromString(svgText,'image/svg+xml');
      const svgEl=svgDoc.documentElement;
      const width=parseFloat(svgEl.getAttribute('width'))||PANEL.offsetWidth;
      const height=parseFloat(svgEl.getAttribute('height'))||PANEL.offsetHeight;
      const pageW=pdf.internal.pageSize.getWidth();
      const pageH=pdf.internal.pageSize.getHeight();
      const scale=Math.min(pageW/width,pageH/height);
      window.svg2pdf(svgEl,pdf,{{x:(pageW-width*scale)/2,y:(pageH-height*scale)/2,scale}});
      const blob=pdf.output('blob');
      const url=URL.createObjectURL(blob);
      triggerDownload(url,'SITREP_Panel.pdf');
    }}
    async function exportPNG() {{
      const dataUrl=await domtoimage.toPng(PANEL,{{bgcolor:'{CARD_DARK}',quality:1}});
      triggerDownload(dataUrl,'SITREP_Panel.png');
    }}
    function triggerDownload(url,filename){{
      try{{
        const a=document.createElement('a');
        a.href=url; a.download=filename; a.rel='noopener'; a.target='_blank';
        document.body.appendChild(a); a.click(); a.remove();
      }}catch(e){{window.open(url,'_blank','noopener');}}
    }}
    document.addEventListener('keydown',e=>{{
      if(e.key==='s'||e.key==='S')exportSVG();
      if(e.key==='p'||e.key==='P')exportPDF();
      if(e.key==='g'||e.key==='G')exportPNG();
    }});
  </script>
</body></html>
"""

components.html(html, height=900, scrolling=False)
