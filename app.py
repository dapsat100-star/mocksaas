# -*- coding: utf-8 -*-
# DAP ATLAS — Sidebar SaaS (logo grande + abas CSS + scroll interno + EXPORT SVG/PDF vetorial)

from datetime import datetime
from base64 import b64encode
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DAP ATLAS — Sidebar SaaS", page_icon="🛰️", layout="wide")

# ======= Tema
PRIMARY   = "#00E3A5"
BG_DARK   = "#0b1221"
CARD_DARK = "#10182b"
TEXT      = "#FFFFFF"
MUTED     = "#9fb0c9"
BORDER    = "rgba(255,255,255,.10)"

PANEL_W_PX   = 560
PANEL_GAP_PX = 24

# ======= Logo (png com fundo branco)
logo_uri = ""
p = Path("dapatlas_fundo_branco.png")
if p.exists() and p.stat().st_size > 0:
    logo_uri = "data:image/png;base64," + b64encode(p.read_bytes()).decode("ascii")

# ======= Dados
AOI_ID       = "BR-PA-2025-01"
confianca    = "92%"
extensao_km  = "5 km"
area_km2     = "25 km²"
resolucao    = "35 cm"
local        = "Cena 5 × 5 km"
data_hora    = "07/06/2025 – 09:25"
sensor       = "BlackSky Global-16 (Sensor: Global-16)"
agora        = datetime.now().strftime("%d/%m %H:%M")

achados = [
    "Vias lineares abertas na vegetação, com características de abertura recente ou uso contínuo — indícios compatíveis com pressão antrópica, como atividade madeireira, garimpo ou ocupação irregular.",
    "Clareiras de diferentes tamanhos, algumas conectadas às vias mencionadas.",
    "Aglomerados habitacionais dispersos, sugerindo presença humana ativa.",
    "Pista de pouso com dimensões estimadas entre 750 e 850 m de comprimento, largura compatível com operação de aeronaves de pequeno porte.",
    "A pista conecta-se a uma rede de vias irregulares e áreas desmatadas, reforçando o caráter logístico da estrutura.",
]

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
  overflow:auto;               /* scroll interno, não corta */
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

/* ======= Abas (CSS-only) ======= */
.tabs{{margin-top:6px}}
.tabs input{{display:none}}
.tabs label{{
  display:inline-block; padding:8px 12px; margin-right:8px; border:1px solid var(--border);
  border-bottom:none; border-top-left-radius:10px; border-top-right-radius:10px;
  color:var(--muted); background:rgba(255,255,255,.02); cursor:pointer; font-weight:700; font-size:.92rem
}}
.tabs input:checked + label{{color:#08121f; background:var(--primary); border-color:var(--primary)}}
.tab-content{{border:1px solid var(--border); border-radius:0 12px 12px 12px; padding:12px; margin-top:-1px}}

ul.bullets{{margin:6px 0 0 0; padding-left:1.1rem}}
ul.bullets li{{margin:8px 0}}
.section-title{{font-weight:800; margin: 2px 0 8px}}

table.minimal{{width:100%;border-collapse:collapse;margin-top:2px}}
table.minimal th, table.minimal td{{border-bottom:1px solid var(--border);padding:9px 6px;text-align:left;font-size:.95rem}}
table.minimal th{{color:var(--muted);font-weight:600}}

.footer{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:10px}}
.btn{{display:inline-block;background:var(--primary);color:#08121f;font-weight:800;padding:10px 14px;border-radius:12px;text-decoration:none;border:none}}
.small{{font-size:.85rem}}
.hidden{{display:none}}
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
            <div class="name">Relatório de Situação</div>
            <div class="sub">Imagem Óptica + IA</div>
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

      <!-- Abas: Achados (default), Metadados, Resumo -->
      <div class="tabs">
        <input type="radio" name="tab" id="tab-achados" checked>
        <label for="tab-achados">Principais Achados</label>

        <input type="radio" name="tab" id="tab-meta">
        <label for="tab-meta">Metadados</label>

        <input type="radio" name="tab" id="tab-resumo">
        <label for="tab-resumo">Resumo</label>

        <div class="tab-content" id="content-achados">
          <ul class="bullets">
            {''.join(f'<li>{a}</li>' for a in achados)}
          </ul>
        </div>

        <div class="tab-content" id="content-meta" style="display:none"></div>
        <div class="tab-content" id="content-resumo" style="display:none"></div>
      </div>

      <div class="footer">
        <div class="muted small">© {datetime.now().year} MAVIPE Sistemas Espaciais</div>
        <!-- sem botão visível; exporto por atalho/URL -->
        <div id="export-controls" class="hidden">
          <a class="btn" id="btn-svg">Exportar SVG</a>
          <a class="btn" id="btn-pdf">Exportar PDF</a>
        </div>
      </div>
    </div>
  </div>

  <!-- libs: dom-to-image-more (SVG) + jsPDF + svg2pdf -->
  <script src="https://cdn.jsdelivr.net/npm/dom-to-image-more@2.8.0/dist/dom-to-image-more.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/svg2pdf.js@2.2.3/dist/svg2pdf.umd.min.js"></script>

  <script>
    // Troca das abas
    const achados = document.getElementById('content-achados');
    const meta    = document.getElementById('content-meta');
    const resumo  = document.getElementById('content-resumo');
    function show(which) {{
      achados.style.display = (which==='a')?'block':'none';
      meta.style.display    = (which==='m')?'block':'none';
      resumo.style.display  = (which==='r')?'block':'none';
    }}
    document.getElementById('tab-achados').onchange = ()=>show('a');
    document.getElementById('tab-meta').onchange    = ()=>show('m');
    document.getElementById('tab-resumo').onchange  = ()=>show('r');

    // Preenche conteúdo das abas Meta/Resumo
    meta.innerHTML = `
      <div class="section-title">Metadados</div>
      <table class="minimal">
        <tr><th>Local</th><td>{local}</td></tr>
        <tr><th>Data/Hora</th><td>{data_hora}</td></tr>
        <tr><th>Fonte</th><td>{sensor}</td></tr>
        <tr><th>Geração</th><td>{agora}</td></tr>
        <tr><th>Sistema</th><td>DAP ATLAS — SITREP</td></tr>
      </table>
    `;
    resumo.innerHTML = `
      <div class="section-title">Resumo</div>
      <p>
        Detecções sobrepostas à imagem base, com registro geométrico submétrico.
        Pipeline <b>Imagem Óptica + IA + fusão multi-sensor</b> com atualização em <b>tempo quase-real</b>.
      </p>
    `;

    // ===== Exportação Vetorial =====
    const PANEL = document.getElementById('panel');

    async function exportSVG() {{
      // Converte o painel para SVG via foreignObject (mantém textos como texto)
      const dataUrl = await domtoimage.toSvg(PANEL, {{
        bgcolor: '{CARD_DARK}',
        filter: (node) => true,
        style: {{
          // Garante background e fontes
          'background': '{CARD_DARK}',
          'color': '{TEXT}'
        }},
        quality: 1
      }});
      triggerDownload(dataUrl, 'SITREP_Painel.svg');
    }}

    async function exportPDF() {{
      // 1) Gera SVG
      const svgUrl = await domtoimage.toSvg(PANEL, {{
        bgcolor: '{CARD_DARK}',
        quality: 1
      }});
      const svgText = await (await fetch(svgUrl)).text();

      // 2) Converte SVG -> PDF (A4 portrait)
      const {{ jsPDF }} = window.jspdf;
      const pdf = new jsPDF({{ unit: 'pt', format: 'a4', orientation: 'p' }});

      // Ajuste de escala para caber na página mantendo proporção
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');
      const svgEl  = svgDoc.documentElement;
      const width  = parseFloat(svgEl.getAttribute('width'))  || PANEL.offsetWidth;
      const height = parseFloat(svgEl.getAttribute('height')) || PANEL.offsetHeight;

      const pageW = pdf.internal.pageSize.getWidth();
      const pageH = pdf.internal.pageSize.getHeight();
      const scale = Math.min(pageW / width, pageH / height);

      // Renderiza o SVG no PDF
      window.svg2pdf(svgEl, pdf, {{
        x: (pageW - width * scale) / 2,
        y: (pageH - height * scale) / 2,
        scale: scale
      }});

      pdf.save('SITREP_Painel.pdf');
    }}

    function triggerDownload(dataUrl, filename) {{
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }}

    // Atalhos: S (SVG), P (PDF)
    document.addEventListener('keydown', (e) => {{
      if (e.key === 's' || e.key === 'S') exportSVG();
      if (e.key === 'p' || e.key === 'P') exportPDF();
    }});

    // Auto-export por querystring (?export=svg | ?export=pdf)
    const params = new URLSearchParams(location.search);
    const exp = params.get('export');
    if (exp === 'svg') exportSVG();
    if (exp === 'pdf') exportPDF();
  </script>
</body></html>
"""

components.html(html, height=900, scrolling=False)


