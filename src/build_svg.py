import base64
import math
from logo_svg import LOGO_VIEWBOX, LOGO_ASPECT, LOGO_COLORED_INNER

FONT_DIR = "fonts/beaufort"

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

# Official Legend in the Mist press-kit font: Beaufort for LOL (Riot Games' display
# serif). Only the weight actually used stays embedded. The logo is fixed vector
# artwork, so the only text left in the banner is the user's campaign/one-shot name,
# which uses Medium Italic.
BEAUFORT_MEDIUM_ITALIC = b64(f"{FONT_DIR}/medium_italic.woff2")

FONT_FACES = f"""
    <style>
      @font-face {{
        font-family: 'Beaufort LitM';
        font-weight: 500;
        font-style: italic;
        src: url(data:font/woff2;base64,{BEAUFORT_MEDIUM_ITALIC}) format('woff2');
      }}
      .bodyface {{ font-family: 'Beaufort LitM', Georgia, 'Times New Roman', serif; }}
    </style>
"""

# ---- palette ----
PARCHMENT      = "#EFE3C6"
PARCHMENT_LT   = "#F7EFDA"
PARCHMENT_DK   = "#C9B78E"
INK            = "#2A2018"
AMBER          = "#B5792E"
AMBER_LT       = "#D9A653"

W, H = 1920, 1080

# Outer frame margin / corner radius. Both frame lines are plain, straight rounded
# rects (no notch): the dark ink line and the gold amber accent line each run
# uninterrupted all the way around.
MARGIN = 44
CORNER_R = 10
INNER_MARGIN = MARGIN + 13
INNER_R = 6

# --- logo medallion: the logo sits inside an elongated hexagon (flat top/bottom
# edges, pointy left/right "shoulders") that pokes up through the top of the
# frame. The shoulders sit exactly on the main dark line (HEX_MID_Y == MARGIN).
# The box has its own parchment fill (see _hex_closed_path / #logoBoxFill), just
# like the campaign-name plaque, with its own opacity slider.
#
# The hexagon's upper half (shoulders -> top edge) is a separate open stroke, the
# cap, poking up above the line (see _hex_cap_path). It has to be a separate
# stroke since it goes outside the rect's own boundary. Its lower half (shoulders
# -> bottom edge), the notch, is cut directly into the main dark <rect>'s top
# edge (see _rect_with_hex_gap), so there's no redundant straight segment of the
# rect still running underneath/through the medallion. The rect's own outline
# *is* the notch there.
#
# The gold amber line no longer follows the box at all. It's a plain, ordinary
# straight cornice everywhere, exactly like the rest of the inner accent, except
# for one plain flat gap over the box's widest extent (see _rect_with_flat_gap)
# so it's simply never drawn inside the box. Since gold never enters the box, it
# can never clash with the logo or with dark's line there, no matter how
# transparent the box's own fill is set. ---
LOGO_W = 255
LOGO_H = LOGO_W * LOGO_ASPECT
LOGO_X = W / 2 - LOGO_W / 2

HEX_CX = W / 2
HEX_HALF_TOP = LOGO_W / 2 + 18   # half-width of the flat top + bottom edges (narrow)
HEX_HALF_MID = LOGO_W / 2 + 53   # half-width at the shoulders, the widest point
HEX_TOP_Y = 20                     # flat top edge, pokes ~24px above MARGIN
HEX_MID_Y = MARGIN                 # shoulders sit exactly on the main dark line

LOGO_BOX_PAD = 20  # vertical clearance between the logo and the box's top/bottom
                    # edges, equal on both sides, so the logo sits vertically
                    # centered in the box
LOGO_Y = HEX_TOP_Y + LOGO_BOX_PAD
NOTCH_BOTTOM_Y = LOGO_Y + LOGO_H + LOGO_BOX_PAD  # flat bottom edge

LOGO_FILL_OPACITY = 0.88   # default parchment-fill opacity for the logo box
TITLE_FILL_OPACITY = 1.0   # default parchment-fill opacity for the title plaque

# --- campaign-name plaque: framed, centered, sitting below the medallion. Its size
# and vertical position are also adjustable live in the page (a checkbox to show/
# hide it, plus size/position sliders). The numbers below are just the defaults
# used for the initial server-rendered markup; build_html.py's JS recomputes the
# same geometry (see BASE_* there) whenever the controls change. ---
PLAQUE_CX = W / 2
PLAQUE_W = 1000
CORNER_R_PLAQUE = 22

PAD_TOP = 18               # plaque top -> flourish ornament (kept tight to the box)
GAP_FLOURISH_NAME = 58     # flourish -> campaign-name baseline
PAD_BOTTOM = 30            # campaign-name baseline -> plaque bottom (room for descenders)

PLAQUE_H = PAD_TOP + GAP_FLOURISH_NAME + PAD_BOTTOM

# Position-slider range: the plaque's top edge can now move through virtually the
# whole picture, from just inside the top dark line down to just above the
# bottom one, instead of the narrower band below the logo notch it used to be
# confined to. The user can push it up to overlap the medallion, or all the way
# down near the bottom margin, if that's the look they want.
PLAQUE_TOP_MIN = MARGIN + 20
PLAQUE_BOTTOM_MAX = H - MARGIN - 20  # = 1016

# Default position (used for the server-rendered initial markup, and as the
# position slider's starting value) stays exactly where it's always been, right
# below the logo notch, even though the slider's own range is now much wider.
PLAQUE_DEFAULT_TOP = NOTCH_BOTTOM_Y + 40
PLAQUE_PY0 = PLAQUE_DEFAULT_TOP
PLAQUE_CY = PLAQUE_PY0 + PLAQUE_H / 2

PLAQUE_POS_DEFAULT_PCT = round(
    (PLAQUE_DEFAULT_TOP - PLAQUE_TOP_MIN)
    / (PLAQUE_BOTTOM_MAX - PLAQUE_H - PLAQUE_TOP_MIN) * 100
)

# Width-slider safety clamp, in raw pixels. Applied in the page's JS so no
# combination of the (independent) width slider and the box-size slider can ever
# push the plaque wider than the frame or shrink it into an unreadable sliver.
PLAQUE_MIN_W = 300
PLAQUE_MAX_W = W - 2 * (INNER_MARGIN + 40)  # 40px clearance inside gold on each side

FLOURISH_HALF_OUTER = 160
FLOURISH_GAP_INNER = 24
DIAMOND_HALF_X = 9
DIAMOND_HALF_Y = 6

FLOURISH_Y = PLAQUE_PY0 + PAD_TOP
NAME_Y = FLOURISH_Y + GAP_FLOURISH_NAME

FIT = {
    "name": {"base": 68, "min": 28, "maxWidth": PLAQUE_W * 0.9, "baseSpacing": 2.8},
}


def _hex_points(cx, half_top, half_mid, top_y, mid_y, bottom_y):
    """The six vertices of an elongated hexagon: flat top/bottom edges, pointy
    left/right shoulders at mid_y (the widest point), going clockwise from the
    top-left corner: top-left, top-right, right shoulder, bottom-right,
    bottom-left, left shoulder."""
    return [
        (cx - half_top, top_y),
        (cx + half_top, top_y),
        (cx + half_mid, mid_y),
        (cx + half_top, bottom_y),
        (cx - half_top, bottom_y),
        (cx - half_mid, mid_y),
    ]


def _hex_cap_path(pts):
    """Open stroke for the hexagon's upper half only: left shoulder up to the
    top-left corner, across the flat top, down to the right shoulder. Both
    ends land exactly on the main straight <rect> line at the shoulder points, so
    this is the part that pokes up above it into the outer margin."""
    top_left, top_right, right_shoulder, _, _, left_shoulder = pts
    return (
        f"M {left_shoulder[0]:.1f},{left_shoulder[1]:.1f} "
        f"L {top_left[0]:.1f},{top_left[1]:.1f} "
        f"L {top_right[0]:.1f},{top_right[1]:.1f} "
        f"L {right_shoulder[0]:.1f},{right_shoulder[1]:.1f}"
    )


def _hex_closed_path(pts):
    """The hexagon's own closed silhouette (all six vertices): the logo box's
    filled shape, matching the union of the cap and notch outline exactly, so the
    fill sits precisely up to (and never past) dark's stroke on every side."""
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def _rect_with_flat_gap(x0, y0, x1, y1, r, gap_left_x, gap_right_x):
    """Same rounded-rect silhouette as _rounded_rect_path, but with a plain flat
    gap left open in the top edge between gap_left_x and gap_right_x. No detour,
    the line is simply absent there. This is gold's frame line: one open path,
    starting just right of the gap and running clockwise all the way around back
    to just left of it, so gold is never drawn inside the logo box at all
    (rather than routed around it)."""
    return (
        f"M {gap_right_x:.1f},{y0:.1f} "
        f"L {x1-r:.1f},{y0:.1f} "
        f"Q {x1:.1f},{y0:.1f} {x1:.1f},{y0+r:.1f} "
        f"L {x1:.1f},{y1-r:.1f} "
        f"Q {x1:.1f},{y1:.1f} {x1-r:.1f},{y1:.1f} "
        f"L {x0+r:.1f},{y1:.1f} "
        f"Q {x0:.1f},{y1:.1f} {x0:.1f},{y1-r:.1f} "
        f"L {x0:.1f},{y0+r:.1f} "
        f"Q {x0:.1f},{y0:.1f} {x0+r:.1f},{y0:.1f} "
        f"L {gap_left_x:.1f},{y0:.1f}"
    )


def _rect_with_hex_gap(x0, y0, x1, y1, r, gap_pts):
    """A single closed rounded-rect path, same silhouette as _rounded_rect_path,
    except the top edge is interrupted by a notch that tapers out to the
    hexagon's shoulders and back in to its bottom edge (gap_pts = left-shoulder,
    bottom-left, bottom-right, right-shoulder points, from _hex_points) instead
    of running straight across. This is dark's frame line: the notch is baked
    directly into the one path, so there's no redundant straight segment of the
    rect still running underneath the logo box. This outline *is* the notch."""
    ls, bl, br, rs = gap_pts
    return (
        f"M {x0+r:.1f},{y0:.1f} "
        f"L {ls[0]:.1f},{y0:.1f} "
        f"L {bl[0]:.1f},{bl[1]:.1f} "
        f"L {br[0]:.1f},{br[1]:.1f} "
        f"L {rs[0]:.1f},{y0:.1f} "
        f"L {x1-r:.1f},{y0:.1f} "
        f"Q {x1:.1f},{y0:.1f} {x1:.1f},{y0+r:.1f} "
        f"L {x1:.1f},{y1-r:.1f} "
        f"Q {x1:.1f},{y1:.1f} {x1-r:.1f},{y1:.1f} "
        f"L {x0+r:.1f},{y1:.1f} "
        f"Q {x0:.1f},{y1:.1f} {x0:.1f},{y1-r:.1f} "
        f"L {x0:.1f},{y0+r:.1f} "
        f"Q {x0:.1f},{y0:.1f} {x0+r:.1f},{y0:.1f} Z"
    )


def _rounded_rect_path(cx, cy, w, h, r):
    x0, y0 = cx - w / 2, cy - h / 2
    return (
        f"M {x0+r:.1f},{y0:.1f} "
        f"L {x0+w-r:.1f},{y0:.1f} "
        f"Q {x0+w:.1f},{y0:.1f} {x0+w:.1f},{y0+r:.1f} "
        f"L {x0+w:.1f},{y0+h-r:.1f} "
        f"Q {x0+w:.1f},{y0+h:.1f} {x0+w-r:.1f},{y0+h:.1f} "
        f"L {x0+r:.1f},{y0+h:.1f} "
        f"Q {x0:.1f},{y0+h:.1f} {x0:.1f},{y0+h-r:.1f} "
        f"L {x0:.1f},{y0+r:.1f} "
        f"Q {x0:.1f},{y0:.1f} {x0+r:.1f},{y0:.1f} Z"
    )


def build_svg(campaign_name="TALES OF THE DALES"):
    """A frame + title "mask" over a plain parchment ground. The logo sits inside a
    hexagonal medallion box that pokes up through the top of the frame, with its
    own parchment fill (like the plaque's) behind the logo art. Dark's main frame
    line is a single path (see _rect_with_hex_gap) with the hexagon's lower-half
    taper (shoulders -> bottom edge) cut directly into its top edge. No redundant
    straight segment runs underneath the box; the notch *is* the rect's own
    outline there. Dark's cap (shoulders -> top edge) is a separate open stroke
    (see _hex_cap_path), since it pokes up outside the rect's own boundary. It
    meets the rect exactly at the shoulder points, so the join is seamless.
    Gold's line doesn't follow the box's shape at all: it's a plain straight
    cornice everywhere (see _rect_with_flat_gap), just with a flat gap left open
    over the box's widest extent, so it's simply never drawn inside the box. It
    can't clash with the logo or dark's line there no matter how transparent the
    box's own fill is. The campaign/one-shot name sits below in its own framed,
    boxed, optional plaque. The page's JS can show/hide it and adjust its
    size/position/font size live, and both the plaque's and the logo box's
    parchment fills have their own opacity sliders. A background <image> layer
    (id=bgImage, initially empty) sits between the parchment and the frame; the
    page's JS sets its href from an uploaded file and controls its opacity with
    the blend slider."""

    plaque_cx, plaque_cy = PLAQUE_CX, PLAQUE_CY
    plaque_d = _rounded_rect_path(plaque_cx, plaque_cy, PLAQUE_W, PLAQUE_H, CORNER_R_PLAQUE)

    dark_hex_pts = _hex_points(HEX_CX, HEX_HALF_TOP, HEX_HALF_MID, HEX_TOP_Y, HEX_MID_Y, NOTCH_BOTTOM_Y)
    dark_cap_d = _hex_cap_path(dark_hex_pts)
    logo_box_fill_d = _hex_closed_path(dark_hex_pts)

    # dark_hex_pts order is [top_left, top_right, right_shoulder, bottom_right,
    # bottom_left, left_shoulder]; the notch gap needs (left_shoulder, bottom_left,
    # bottom_right, right_shoulder), left-to-right.
    dark_notch_pts = (dark_hex_pts[5], dark_hex_pts[4], dark_hex_pts[3], dark_hex_pts[2])
    dark_frame_d = _rect_with_hex_gap(MARGIN, MARGIN, W - MARGIN, H - MARGIN, CORNER_R, gap_pts=dark_notch_pts)

    gold_frame_d = _rect_with_flat_gap(
        INNER_MARGIN, INNER_MARGIN, W - INNER_MARGIN, H - INNER_MARGIN, INNER_R,
        gap_left_x=HEX_CX - HEX_HALF_MID, gap_right_x=HEX_CX + HEX_HALF_MID,
    )

    svg = f"""<svg id="litmBackdrop" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
{FONT_FACES}
    <radialGradient id="groundGrad" cx="50%" cy="30%" r="80%">
      <stop offset="0%" stop-color="{PARCHMENT_LT}"/>
      <stop offset="60%" stop-color="{PARCHMENT}"/>
      <stop offset="100%" stop-color="{PARCHMENT_DK}"/>
    </radialGradient>
    <linearGradient id="plaqueGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{PARCHMENT_LT}"/>
      <stop offset="100%" stop-color="{PARCHMENT}"/>
    </linearGradient>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" result="noise"/>
      <feColorMatrix in="noise" type="matrix"
        values="0 0 0 0 0.16  0 0 0 0 0.12  0 0 0 0 0.08  0 0 0 0.05 0"/>
    </filter>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="{INK}" flood-opacity="0.32"/>
    </filter>
    <filter id="logoShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="{INK}" flood-opacity="0.45"/>
    </filter>
  </defs>

  <!-- parchment ground (shows through whenever no image is uploaded, or the blend slider is pulled down) -->
  <rect id="bgParchment" x="0" y="0" width="{W}" height="{H}" fill="url(#groundGrad)"/>
  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#grain)"/>

  <!-- uploaded background image: JS sets href on file select, and opacity from the blend slider -->
  <image id="bgImage" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" opacity="0"/>

  <!-- logo box parchment fill: same treatment as the plaque, own opacity slider.
       Drawn before the frame lines/cap so they stay crisp on top of it. -->
  <g filter="url(#softShadow)">
    <path id="logoBoxFill" d="{logo_box_fill_d}" fill="url(#plaqueGrad)" fill-opacity="{LOGO_FILL_OPACITY}"/>
  </g>

  <!-- outer (dark) frame: a single path with the hexagon's lower-half taper cut
       directly into the top edge. No redundant straight segment runs under the
       box; this outline *is* the notch there. The cap (poking above the line)
       is a separate stroke added below, meeting this path at the shoulders. -->
  <path d="{dark_frame_d}" fill="none" stroke="{INK}" stroke-width="3.5"/>

  <!-- inner (gold) frame: a plain straight cornice everywhere, with one flat gap
       left open over the logo box, so gold is simply never drawn inside the box
       at all and can't clash with the logo or dark's line there. -->
  <path d="{gold_frame_d}" fill="none" stroke="{AMBER}" stroke-width="1.4" opacity="0.75"/>

  <!-- hexagon cap: the box's upper half, poking above the main dark line -->
  <path d="{dark_cap_d}" fill="none" stroke="{INK}" stroke-width="3.5"/>

  <!-- official Legend in the Mist logo lockup: fixed brand mark, centered in its box -->
  <g filter="url(#logoShadow)">
    <svg x="{LOGO_X:.1f}" y="{LOGO_Y:.1f}" width="{LOGO_W:.1f}" height="{LOGO_H:.1f}" viewBox="{LOGO_VIEWBOX}">{LOGO_COLORED_INNER}</svg>
  </g>

  <!-- campaign-name plaque: framed, centered, below the medallion. Optional, JS
       toggles #plaqueGroup's visibility and rewrites the geometry below live. -->
  <g id="plaqueGroup">
    <g filter="url(#softShadow)">
      <path id="plaqueFill" d="{plaque_d}" fill="url(#plaqueGrad)" fill-opacity="{TITLE_FILL_OPACITY}" stroke="{INK}" stroke-width="2.5"/>
      <path id="plaqueOutline" d="{plaque_d}" fill="none" stroke="{AMBER}" stroke-width="1" opacity="0.7"/>
    </g>

    <g id="nameDivider">
      <path id="flourishLeft" d="M {plaque_cx-FLOURISH_HALF_OUTER},{FLOURISH_Y:.1f} L {plaque_cx-FLOURISH_GAP_INNER},{FLOURISH_Y:.1f}" stroke="{AMBER}" stroke-width="1.6"/>
      <path id="flourishRight" d="M {plaque_cx+FLOURISH_GAP_INNER},{FLOURISH_Y:.1f} L {plaque_cx+FLOURISH_HALF_OUTER},{FLOURISH_Y:.1f}" stroke="{AMBER}" stroke-width="1.6"/>
      <path id="flourishDiamond" d="M {plaque_cx-DIAMOND_HALF_X},{FLOURISH_Y-DIAMOND_HALF_Y:.1f} L {plaque_cx},{FLOURISH_Y+DIAMOND_HALF_Y:.1f} L {plaque_cx+DIAMOND_HALF_X},{FLOURISH_Y-DIAMOND_HALF_Y:.1f} L {plaque_cx},{FLOURISH_Y:.1f} Z" fill="{AMBER}"/>
    </g>

    <text id="nameText" class="bodyface" x="{plaque_cx}" y="{NAME_Y:.1f}" text-anchor="middle"
          font-size="{FIT['name']['base']}" font-style="italic" font-weight="500" letter-spacing="{FIT['name']['baseSpacing']}" fill="{INK}" opacity="0.85">{campaign_name}</text>
  </g>
</svg>"""
    return svg


if __name__ == "__main__":
    svg = build_svg()
    with open("backdrop.svg", "w") as f:
        f.write(svg)
    print("wrote backdrop.svg", len(svg), "bytes")
