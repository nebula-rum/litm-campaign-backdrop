from build_svg import (
    build_svg, INK, AMBER, AMBER_LT, PARCHMENT, PARCHMENT_LT, PARCHMENT_DK, FIT,
    PLAQUE_CX, PLAQUE_W, PLAQUE_H, CORNER_R_PLAQUE, PAD_TOP, GAP_FLOURISH_NAME, PAD_BOTTOM,
    PLAQUE_TOP_MIN, PLAQUE_BOTTOM_MAX, PLAQUE_POS_DEFAULT_PCT, PLAQUE_MIN_W, PLAQUE_MAX_W,
    FLOURISH_HALF_OUTER, FLOURISH_GAP_INNER,
    DIAMOND_HALF_X, DIAMOND_HALF_Y, LOGO_FILL_OPACITY, TITLE_FILL_OPACITY,
)
import json
import datetime

SAGE = "#6E8062"  # kept for the UI's success/status color, no longer used in the artwork itself

DEFAULT_NAME = "TALES OF THE DALES"

CURRENT_YEAR = datetime.date.today().year
NEBULARUM_URL = "https://github.com/nebula-rum/litm-campaign-backdrop"

svg_markup = build_svg(DEFAULT_NAME)

# Base (100% size, 0% position) plaque geometry, handed to the page's JS so the
# title-box size/position sliders can rebuild the plaque's path/flourish/text
# coordinates live without needing a server round-trip. All of this matches the
# constants build_svg.py used to render the initial markup above.
PLAQUE_BASE = {
    "cx": PLAQUE_CX,
    "w": PLAQUE_W,
    "padTop": PAD_TOP,
    "gapFlourishName": GAP_FLOURISH_NAME,
    "padBottom": PAD_BOTTOM,
    "cornerR": CORNER_R_PLAQUE,
    "flourishHalfOuter": FLOURISH_HALF_OUTER,
    "flourishGapInner": FLOURISH_GAP_INNER,
    "diamondHalfX": DIAMOND_HALF_X,
    "diamondHalfY": DIAMOND_HALF_Y,
    "topMin": PLAQUE_TOP_MIN,
    "bottomMax": PLAQUE_BOTTOM_MAX,
    "minW": PLAQUE_MIN_W,
    "maxW": PLAQUE_MAX_W,
    "fontBase": FIT["name"]["base"],
    "fontMin": FIT["name"]["min"],
    "maxWidthRatio": FIT["name"]["maxWidth"] / PLAQUE_W,
    "spacingBase": FIT["name"]["baseSpacing"],
}

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Legend in the Mist Backdrop Generator</title>
<style>
  :root {{
    --ground:      #17130f;
    --panel:       #211b15;
    --panel-line:  #3a3025;
    --ink:         #ede4d0;
    --ink-dim:     #a89a80;
    --amber:       {AMBER};
    --amber-lt:    {AMBER_LT};
    --sage:        {SAGE};
    --danger:      #b3453a;
    --focus:       #d9a653;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0; padding: 0;
    background: var(--ground);
    color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }}
  body {{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
    padding: 40px 20px 56px;
  }}
  @media (prefers-reduced-motion: no-preference) {{
    .btn, input[type="text"] {{ transition: background-color .15s ease, border-color .15s ease, transform .1s ease; }}
  }}

  header {{
    text-align: center;
    max-width: 1352px;
  }}
  header .eyebrow {{
    font-size: 12px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--amber-lt);
    margin: 0 0 8px;
    font-weight: 600;
  }}
  header h1 {{
    font-size: 22px;
    margin: 0 0 8px;
    font-weight: 600;
    letter-spacing: .01em;
  }}
  header p {{
    margin: 0;
    font-size: 14px;
    line-height: 1.55;
    color: var(--ink-dim);
    text-align: justify;
  }}

  .stage {{
    width: 100%;
    max-width: 1400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 22px;
  }}

  .frame {{
    width: 100%;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 30px 70px -25px rgba(0,0,0,.75), 0 0 0 1px var(--panel-line);
    background: {PARCHMENT};
    line-height: 0;
  }}
  .frame > svg {{ display: block; width: 100%; height: auto; }}

  .panel {{
    width: 100%;
    background: var(--panel);
    border: 1px solid var(--panel-line);
    border-radius: 10px;
    padding: 22px 24px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px 20px;
  }}
  .field {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .field.full {{ grid-column: 1 / -1; }}
  .checkbox-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    font-size: 14px;
    color: var(--ink);
    font-weight: 500;
    letter-spacing: normal;
    text-transform: none;
  }}
  .checkbox-row input[type="checkbox"] {{
    width: 17px; height: 17px;
    accent-color: var(--amber);
    cursor: pointer;
    flex: none;
  }}
  label {{
    font-size: 11px;
    letter-spacing: .09em;
    text-transform: uppercase;
    color: var(--ink-dim);
    font-weight: 600;
  }}
  input[type="text"], select {{
    background: #171310;
    border: 1px solid var(--panel-line);
    color: var(--ink);
    border-radius: 6px;
    padding: 10px 12px;
    font-size: 15px;
    font-family: inherit;
    width: 100%;
  }}
  input[type="text"]:focus, select:focus, .btn:focus-visible {{
    outline: 2px solid var(--focus);
    outline-offset: 1px;
    border-color: var(--focus);
  }}

  .actions {{
    grid-column: 1 / -1;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    align-items: center;
    margin-top: 4px;
  }}
  .btn {{
    appearance: none;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 11px 18px;
    font-size: 14px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }}
  .btn-primary {{
    background: var(--amber);
    color: #1a1108;
  }}
  .btn-primary:hover {{ background: var(--amber-lt); }}
  .btn-secondary {{
    background: transparent;
    border-color: var(--panel-line);
    color: var(--ink);
  }}
  .btn-secondary:hover {{ border-color: var(--amber); color: var(--amber-lt); }}
  .btn:active {{ transform: translateY(1px); }}
  .btn svg {{ width: 15px; height: 15px; flex: none; }}

  .visually-hidden {{
    position: absolute;
    width: 1px; height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    white-space: nowrap;
  }}
  .upload-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }}
  .filename {{
    font-size: 13px;
    color: var(--ink-dim);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 260px;
  }}
  .filename.empty {{ font-style: italic; }}
  .icon-btn {{
    background: transparent;
    border: 1px solid var(--panel-line);
    color: var(--ink-dim);
    border-radius: 6px;
    width: 30px; height: 30px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex: none;
  }}
  .icon-btn:hover {{ border-color: var(--danger); color: var(--danger); }}
  .icon-btn svg {{ width: 15px; height: 15px; }}
  .icon-btn[hidden] {{ display: none; }}

  .slider-row {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .slider-row input[type="range"] {{
    flex: 1;
    -webkit-appearance: none;
    appearance: none;
    height: 4px;
    border-radius: 999px;
    background: var(--panel-line);
    outline: none;
  }}
  .slider-row input[type="range"]::-webkit-slider-thumb {{
    -webkit-appearance: none;
    width: 17px; height: 17px;
    border-radius: 50%;
    background: var(--amber);
    border: 2px solid #171310;
    cursor: pointer;
  }}
  .slider-row input[type="range"]::-moz-range-thumb {{
    width: 17px; height: 17px;
    border-radius: 50%;
    background: var(--amber);
    border: 2px solid #171310;
    cursor: pointer;
  }}
  .slider-row input[type="range"]:disabled {{ opacity: 0.4; }}
  .slider-value {{
    font-size: 13px;
    color: var(--ink-dim);
    width: 3.2em;
    text-align: right;
    font-variant-numeric: tabular-nums;
    flex: none;
  }}

  .hint {{
    grid-column: 1 / -1;
    font-size: 12.5px;
    color: var(--ink-dim);
    line-height: 1.5;
    border-top: 1px solid var(--panel-line);
    padding-top: 14px;
    margin-top: 2px;
  }}
  .hint strong {{ color: var(--ink); font-weight: 600; }}
  .site-footer {{
    width: 100%;
    max-width: 1352px;
    text-align: center;
  }}
  .site-footer p {{
    margin: 0;
    font-size: 11.5px;
    line-height: 1.6;
    color: var(--ink-dim);
    opacity: 0.75;
  }}
  .site-footer a {{
    color: var(--amber-lt);
    text-decoration: none;
  }}
  .site-footer a:hover {{ text-decoration: underline; }}
  .status {{
    font-size: 12.5px;
    color: var(--sage);
    min-height: 1em;
  }}

  @media (max-width: 640px) {{
    .panel {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<header>
  <p class="eyebrow">Legend in the Mist</p>
  <h1>Campaign Backdrop Generator</h1>
  <p>A vector frame for your VTT table. The Legend in the Mist logo is built into the top edge, and your
     campaign or one-shot name goes in a plaque below it that you can move, resize, or hide entirely. Drop
     in your own background art (most official pieces are already 16:9) and blend it with the parchment
     using the slider below, then export a PNG sized for Owlbear Rodeo or any other VTT, or grab the SVG
     if you want it to stay sharp no matter how far your players zoom in.</p>
</header>

<div class="stage">
  <div class="frame">
    {svg_markup}
  </div>

  <div class="panel">
    <div class="field full">
      <label for="nameInput">Campaign / one-shot name</label>
      <input type="text" id="nameInput" value="{DEFAULT_NAME}" maxlength="70" autocomplete="off">
    </div>

    <div class="field full">
      <label class="checkbox-row" for="allCapsToggle">
        <input type="checkbox" id="allCapsToggle" checked>
        <span>ALL CAPS title text</span>
      </label>
    </div>

    <div class="field full">
      <label class="checkbox-row" for="titleBoxToggle">
        <input type="checkbox" id="titleBoxToggle" checked>
        <span>Show title box</span>
      </label>
    </div>

    <div class="field">
      <label for="titleSizeSlider">Title box size</label>
      <div class="slider-row">
        <input type="range" id="titleSizeSlider" min="70" max="130" value="100">
        <span class="slider-value" id="titleSizeValue">100%</span>
      </div>
    </div>

    <div class="field">
      <label for="titleWidthSlider">Title box width</label>
      <div class="slider-row">
        <input type="range" id="titleWidthSlider" min="50" max="160" value="100">
        <span class="slider-value" id="titleWidthValue">100%</span>
      </div>
    </div>

    <div class="field">
      <label for="titlePosSlider">Title box position</label>
      <div class="slider-row">
        <input type="range" id="titlePosSlider" min="0" max="100" value="{PLAQUE_POS_DEFAULT_PCT}">
        <span class="slider-value" id="titlePosValue">{PLAQUE_POS_DEFAULT_PCT}%</span>
      </div>
    </div>

    <div class="field">
      <label for="titleFontSizeSlider">Title font size</label>
      <div class="slider-row">
        <input type="range" id="titleFontSizeSlider" min="30" max="100" value="{FIT['name']['base']}">
        <span class="slider-value" id="titleFontSizeValue">{FIT['name']['base']}px</span>
      </div>
    </div>

    <div class="field">
      <label for="titleFillOpacitySlider">Title box background</label>
      <div class="slider-row">
        <input type="range" id="titleFillOpacitySlider" min="0" max="100" value="{round(TITLE_FILL_OPACITY*100)}">
        <span class="slider-value" id="titleFillOpacityValue">{round(TITLE_FILL_OPACITY*100)}%</span>
      </div>
    </div>

    <div class="field">
      <label for="logoFillOpacitySlider">Logo box background</label>
      <div class="slider-row">
        <input type="range" id="logoFillOpacitySlider" min="0" max="100" value="{round(LOGO_FILL_OPACITY*100)}">
        <span class="slider-value" id="logoFillOpacityValue">{round(LOGO_FILL_OPACITY*100)}%</span>
      </div>
    </div>

    <div class="field full">
      <label for="bgFileInput">Background image</label>
      <div class="upload-row">
        <label class="btn btn-secondary" for="bgFileInput" style="cursor:pointer;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/><path d="M7 9l5-5 5 5"/><path d="M12 4v13"/></svg>
          Upload image
        </label>
        <input type="file" id="bgFileInput" accept="image/*" class="visually-hidden">
        <span class="filename empty" id="bgFileName">No image uploaded yet, showing plain parchment</span>
        <button class="icon-btn" id="bgRemoveBtn" type="button" title="Remove image" hidden>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>
    </div>

    <div class="field full">
      <label for="blendSlider">Image blend (parchment ↔ your image)</label>
      <div class="slider-row">
        <input type="range" id="blendSlider" min="0" max="100" value="100" disabled>
        <span class="slider-value" id="blendValue">100%</span>
      </div>
    </div>

    <div class="field full">
      <label for="resSelect">Export resolution (PNG)</label>
      <select id="resSelect">
        <option value="1920x1080">Standard · 1920 × 1080</option>
        <option value="3840x2160" selected>High · 3840 × 2160 (recommended for VTT zoom)</option>
        <option value="7680x4320">Ultra · 7680 × 4320</option>
      </select>
    </div>

    <div class="actions">
      <button class="btn btn-primary" id="pngBtn" type="button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v13"/><path d="M7 11l5 5 5-5"/><path d="M4 19h16"/></svg>
        Download PNG
      </button>
      <button class="btn btn-secondary" id="svgBtn" type="button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v13"/><path d="M7 11l5 5 5-5"/><path d="M4 19h16"/></svg>
        Download SVG (vector)
      </button>
      <span class="status" id="statusMsg" aria-live="polite"></span>
    </div>

    <p class="hint">
      <strong>How this works:</strong> the frame, the logo, and the campaign name are all vector, so they
      stay sharp at any size. Your background image sits underneath as a plain layer, cropped to fill the
      frame, and the slider fades it against the parchment. The SVG export keeps your image embedded in the
      file (so it can get large), while the PNG export renders at whatever resolution you pick above,
      regardless of your original image's size.
    </p>
  </div>

  <footer class="site-footer">
    <p>&copy; {CURRENT_YEAR} Nebularum. Source and updates: <a href="{NEBULARUM_URL}" target="_blank" rel="noopener">{NEBULARUM_URL.replace('https://', '')}</a>.
       Legend in the Mist is a trademark of Son of Oak Game Studio; this is an unofficial fan-made tool, not affiliated with or endorsed by them.</p>
  </footer>
</div>

<script>
(function() {{
  const svg = document.getElementById('litmBackdrop');
  const nameEl = document.getElementById('nameText');
  const nameInput = document.getElementById('nameInput');
  const statusMsg = document.getElementById('statusMsg');

  function autoFit(el, cfg) {{
    el.setAttribute('font-size', cfg.base);
    el.setAttribute('letter-spacing', cfg.baseSpacing);
    let bbox;
    try {{ bbox = el.getBBox(); }} catch (e) {{ return; }}
    if (!bbox || bbox.width === 0) return;
    const scale = Math.min(1, cfg.maxWidth / bbox.width);
    const size = Math.max(cfg.min, cfg.base * scale);
    el.setAttribute('font-size', size.toFixed(1));
    el.setAttribute('letter-spacing', (cfg.baseSpacing * (size / cfg.base)).toFixed(2));
  }}

  const dividerGroup = document.getElementById('nameDivider');

  // --- title box: optional (checkbox), with size + position sliders that rebuild
  // the plaque's rounded-rect path, flourish, and text position live ---
  const PLAQUE_BASE = {json.dumps(PLAQUE_BASE)};
  const plaqueGroup = document.getElementById('plaqueGroup');
  const plaqueFillEl = document.getElementById('plaqueFill');
  const plaqueOutlineEl = document.getElementById('plaqueOutline');
  const flourishLeftEl = document.getElementById('flourishLeft');
  const flourishRightEl = document.getElementById('flourishRight');
  const flourishDiamondEl = document.getElementById('flourishDiamond');
  const titleBoxToggle = document.getElementById('titleBoxToggle');
  const titleSizeSlider = document.getElementById('titleSizeSlider');
  const titleSizeValue = document.getElementById('titleSizeValue');
  const titleWidthSlider = document.getElementById('titleWidthSlider');
  const titleWidthValue = document.getElementById('titleWidthValue');
  const titlePosSlider = document.getElementById('titlePosSlider');
  const titlePosValue = document.getElementById('titlePosValue');
  const titleFontSizeSlider = document.getElementById('titleFontSizeSlider');
  const titleFontSizeValue = document.getElementById('titleFontSizeValue');
  const allCapsToggle = document.getElementById('allCapsToggle');

  function roundedRectPath(cx, cy, w, h, r) {{
    const x0 = cx - w / 2, y0 = cy - h / 2;
    return 'M ' + (x0+r).toFixed(1) + ',' + y0.toFixed(1) +
      ' L ' + (x0+w-r).toFixed(1) + ',' + y0.toFixed(1) +
      ' Q ' + (x0+w).toFixed(1) + ',' + y0.toFixed(1) + ' ' + (x0+w).toFixed(1) + ',' + (y0+r).toFixed(1) +
      ' L ' + (x0+w).toFixed(1) + ',' + (y0+h-r).toFixed(1) +
      ' Q ' + (x0+w).toFixed(1) + ',' + (y0+h).toFixed(1) + ' ' + (x0+w-r).toFixed(1) + ',' + (y0+h).toFixed(1) +
      ' L ' + (x0+r).toFixed(1) + ',' + (y0+h).toFixed(1) +
      ' Q ' + x0.toFixed(1) + ',' + (y0+h).toFixed(1) + ' ' + x0.toFixed(1) + ',' + (y0+h-r).toFixed(1) +
      ' L ' + x0.toFixed(1) + ',' + (y0+r).toFixed(1) +
      ' Q ' + x0.toFixed(1) + ',' + y0.toFixed(1) + ' ' + (x0+r).toFixed(1) + ',' + y0.toFixed(1) + ' Z';
  }}

  function clamp(v, lo, hi) {{ return Math.min(hi, Math.max(lo, v)); }}

  function updatePlaque() {{
    const show = titleBoxToggle.checked;
    plaqueGroup.style.display = show ? '' : 'none';
    titleSizeSlider.disabled = !show;
    titleWidthSlider.disabled = !show;
    titlePosSlider.disabled = !show;
    if (!show) return;

    const s = Number(titleSizeSlider.value) / 100;
    const widthScale = Number(titleWidthSlider.value) / 100;
    const p = Number(titlePosSlider.value);
    const fontBaseLive = Number(titleFontSizeSlider.value);
    titleSizeValue.textContent = titleSizeSlider.value + '%';
    titleWidthValue.textContent = titleWidthSlider.value + '%';
    titlePosValue.textContent = titlePosSlider.value + '%';
    titleFontSizeValue.textContent = titleFontSizeSlider.value + 'px';

    const b = PLAQUE_BASE;
    // Width composes the box-size slider with its own, independent width slider
    // (same pattern as the font-size slider composing with box size), then gets
    // clamped so no combination can ever push the plaque wider than the frame or
    // squeeze it into an unreadable sliver.
    const w = clamp(b.w * s * widthScale, b.minW, b.maxW);
    const padTop = b.padTop * s;
    const gapFn = b.gapFlourishName * s;
    const padBottom = b.padBottom * s;
    const h = padTop + gapFn + padBottom;
    const r = b.cornerR * s;
    const py0 = b.topMin + (p / 100) * (b.bottomMax - h - b.topMin);
    const cy = py0 + h / 2;
    const flourishY = py0 + padTop;
    const nameY = flourishY + gapFn;

    const d = roundedRectPath(b.cx, cy, w, h, r);
    plaqueFillEl.setAttribute('d', d);
    plaqueOutlineEl.setAttribute('d', d);

    // Flourish follows the box's actual rendered width (not just the size
    // slider) so it stays in proportion whether the box has been stretched wide
    // or narrowed down, and never overhangs a narrow box's edges.
    const foHalf = Math.min(b.flourishHalfOuter * s * widthScale, w * 0.42), giHalf = b.flourishGapInner * s;
    flourishLeftEl.setAttribute('d', 'M ' + (b.cx - foHalf).toFixed(1) + ',' + flourishY.toFixed(1) + ' L ' + (b.cx - giHalf).toFixed(1) + ',' + flourishY.toFixed(1));
    flourishRightEl.setAttribute('d', 'M ' + (b.cx + giHalf).toFixed(1) + ',' + flourishY.toFixed(1) + ' L ' + (b.cx + foHalf).toFixed(1) + ',' + flourishY.toFixed(1));
    const dxHalf = b.diamondHalfX * s, dyHalf = b.diamondHalfY * s;
    flourishDiamondEl.setAttribute('d',
      'M ' + (b.cx - dxHalf).toFixed(1) + ',' + (flourishY - dyHalf).toFixed(1) +
      ' L ' + b.cx.toFixed(1) + ',' + (flourishY + dyHalf).toFixed(1) +
      ' L ' + (b.cx + dxHalf).toFixed(1) + ',' + (flourishY - dyHalf).toFixed(1) +
      ' L ' + b.cx.toFixed(1) + ',' + flourishY.toFixed(1) + ' Z');

    nameEl.setAttribute('y', nameY.toFixed(1));

    autoFit(nameEl, {{
      base: fontBaseLive * s,
      min: b.fontMin * s,
      maxWidth: w * b.maxWidthRatio,
      baseSpacing: b.spacingBase * s,
    }});
  }}

  function updateName() {{
    const has = nameInput.value.trim().length > 0;
    const raw = nameInput.value.trim();
    nameEl.textContent = has ? (allCapsToggle.checked ? raw.toUpperCase() : raw) : '';
    dividerGroup.style.display = has ? '' : 'none';
    updatePlaque();
  }}

  nameInput.addEventListener('input', updateName);
  allCapsToggle.addEventListener('change', updateName);
  titleBoxToggle.addEventListener('change', updatePlaque);
  titleSizeSlider.addEventListener('input', updatePlaque);
  titleWidthSlider.addEventListener('input', updatePlaque);
  titlePosSlider.addEventListener('input', updatePlaque);
  titleFontSizeSlider.addEventListener('input', updatePlaque);
  updateName();

  // --- parchment-fill opacity sliders: the title plaque and the logo box each
  // have their own independent transparency control over their fill only (the
  // ink border / amber outline / dark hexagon outline stay fully opaque) ---
  const logoBoxFillEl = document.getElementById('logoBoxFill');
  const titleFillOpacitySlider = document.getElementById('titleFillOpacitySlider');
  const titleFillOpacityValue = document.getElementById('titleFillOpacityValue');
  const logoFillOpacitySlider = document.getElementById('logoFillOpacitySlider');
  const logoFillOpacityValue = document.getElementById('logoFillOpacityValue');

  function updateTitleFillOpacity() {{
    const v = Number(titleFillOpacitySlider.value);
    plaqueFillEl.setAttribute('fill-opacity', (v / 100).toFixed(2));
    titleFillOpacityValue.textContent = v + '%';
  }}
  function updateLogoFillOpacity() {{
    const v = Number(logoFillOpacitySlider.value);
    logoBoxFillEl.setAttribute('fill-opacity', (v / 100).toFixed(2));
    logoFillOpacityValue.textContent = v + '%';
  }}
  titleFillOpacitySlider.addEventListener('input', updateTitleFillOpacity);
  logoFillOpacitySlider.addEventListener('input', updateLogoFillOpacity);
  updateTitleFillOpacity();
  updateLogoFillOpacity();

  // --- background image upload + blend slider ---
  const bgImage = document.getElementById('bgImage');
  const bgFileInput = document.getElementById('bgFileInput');
  const bgFileName = document.getElementById('bgFileName');
  const bgRemoveBtn = document.getElementById('bgRemoveBtn');
  const blendSlider = document.getElementById('blendSlider');
  const blendValue = document.getElementById('blendValue');
  const XLINK = 'http://www.w3.org/1999/xlink';

  function setBgOpacity(pct) {{
    bgImage.setAttribute('opacity', (pct / 100).toFixed(2));
    blendValue.textContent = pct + '%';
  }}

  function clearBgImage() {{
    bgImage.removeAttribute('href');
    bgImage.removeAttributeNS(XLINK, 'href');
    bgImage.setAttribute('opacity', '0');
    blendSlider.disabled = true;
    bgFileName.textContent = 'No image uploaded yet, showing plain parchment';
    bgFileName.classList.add('empty');
    bgRemoveBtn.hidden = true;
    bgFileInput.value = '';
  }}

  bgFileInput.addEventListener('change', function() {{
    const file = bgFileInput.files && bgFileInput.files[0];
    if (!file) return;
    if (file.size > 20 * 1024 * 1024) {{
      flash('That image is over 20MB. Try a smaller export from the press kit.');
      bgFileInput.value = '';
      return;
    }}
    const reader = new FileReader();
    reader.onload = function(e) {{
      const dataUrl = e.target.result;
      bgImage.setAttribute('href', dataUrl);
      bgImage.setAttributeNS(XLINK, 'href', dataUrl);
      blendSlider.disabled = false;
      blendSlider.value = 100;
      setBgOpacity(100);
      bgFileName.textContent = file.name;
      bgFileName.classList.remove('empty');
      bgRemoveBtn.hidden = false;
      flash('Image loaded. Use the slider to blend it with the parchment.');
    }};
    reader.onerror = function() {{
      flash('Could not read that file. Try a different image.');
    }};
    reader.readAsDataURL(file);
  }});

  bgRemoveBtn.addEventListener('click', clearBgImage);
  blendSlider.addEventListener('input', function() {{ setBgOpacity(Number(blendSlider.value)); }});

  function slug(s) {{
    return (s || 'legend-in-the-mist-backdrop')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '')
      .slice(0, 60) || 'legend-in-the-mist-backdrop';
  }}

  function flash(msg) {{
    statusMsg.textContent = msg;
    setTimeout(() => {{ if (statusMsg.textContent === msg) statusMsg.textContent = ''; }}, 3200);
  }}

  function serializeSVG() {{
    const clone = svg.cloneNode(true);
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
    return '<?xml version="1.0" encoding="UTF-8"?>\\n' + new XMLSerializer().serializeToString(clone);
  }}

  document.getElementById('svgBtn').addEventListener('click', function() {{
    const blob = new Blob([serializeSVG()], {{ type: 'image/svg+xml;charset=utf-8' }});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = slug(nameInput.value) + '.svg';
    document.body.appendChild(a);
    a.click();
    a.remove();
    flash('Vector SVG downloaded.');
  }});

  document.getElementById('pngBtn').addEventListener('click', function() {{
    const btn = this;
    btn.disabled = true;
    flash('Rendering PNG…');
    const [w, h] = document.getElementById('resSelect').value.split('x').map(Number);
    const svgStr = serializeSVG();
    const blob = new Blob([svgStr], {{ type: 'image/svg+xml;charset=utf-8' }});
    const url = URL.createObjectURL(blob);
    const img = new Image();
    img.onload = function() {{
      const canvas = document.createElement('canvas');
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, w, h);
      URL.revokeObjectURL(url);
      canvas.toBlob(function(pngBlob) {{
        const a = document.createElement('a');
        a.href = URL.createObjectURL(pngBlob);
        a.download = slug(nameInput.value) + '-' + w + 'x' + h + '.png';
        document.body.appendChild(a);
        a.click();
        a.remove();
        btn.disabled = false;
        flash('PNG downloaded (' + w + '\\u00d7' + h + ').');
      }}, 'image/png');
    }};
    img.onerror = function() {{
      URL.revokeObjectURL(url);
      btn.disabled = false;
      flash('Could not render the PNG. Try the SVG download instead.');
    }};
    img.src = url;
  }});
}})();
</script>
</body>
</html>
"""

with open("litm-campaign-backdrop.html", "w") as f:
    f.write(HTML)
print("wrote litm-campaign-backdrop.html", len(HTML), "bytes")
