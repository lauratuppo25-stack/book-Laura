"""Book PDF (A4 paysage) dans la DA du portfolio, sans effet interactif.

Usage : python3 tools/book_pdf.py .   → pdf/book.html (à imprimer en PDF avec Chromium)
Le site (index.html, cv.html) n'est pas modifié.
"""
import html, os, runpy, sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
os.chdir(root)
build = os.path.join(root, 'tools', 'build.py')
saved = {f: open(f, 'rb').read() for f in ('index.html', 'cv.html', 'assets/site.css', 'assets/site.js') if os.path.exists(f)}
sys.argv = [build, root]
B = runpy.run_path(build)                     # outils du site : Riesling, dimensions, projets
for f, data in saved.items():                 # le site reste strictement identique
    open(f, 'wb').write(data)

rsvg, sprite, DIM, P, CAT = B['rsvg'], B['sprite'], B['DIM'], B['P'], B['CAT']
wl, wt = B['width_of']('LAURA'), B['width_of']('TUPPO')
K_L, K_T = B['BOX'] / wl, .63 * wl / wt
WM = f'<span class="wm-l">{rsvg("LAURA")}</span><span class="wm-t">{rsvg("TUPPO")}</span>'

W, H = 1123, 794                               # A4 paysage à 96 dpi
M = 56                                         # marge
SITE = 'lauratuppo25-stack.github.io/book-Laura'
GAP = 14


def fit(names, bw, bh):
    """Images entières (aucun recadrage) en rangées justifiées, sans chevauchement.
    Essaie les découpages en rangées (et l'ordre des images si peu nombreuses) et garde le plus grand rendu."""
    from itertools import permutations
    n = len(names)
    orders = list(dict.fromkeys(permutations(names))) if n <= 5 else [tuple(names)]
    best = None
    for order in orders:
        for mask in range(1 << (n - 1)):
            rows, cur = [], [order[0]]
            for i in range(1, n):
                if mask >> (i - 1) & 1:
                    rows.append(cur); cur = []
                cur.append(order[i])
            rows.append(cur)
            wide = any(len(r) > 1 and any(DIM[x][0] / DIM[x][1] > 3 for x in r) for r in rows)
            if wide or len(rows) > (5 if any(DIM[x][0] / DIM[x][1] > 3 for x in order) else 3) or max(len(r) for r in rows) > 4:
                continue
            hs = [(bw - GAP * (len(r) - 1)) / sum(DIM[x][0] / DIM[x][1] for x in r) for r in rows]
            s = min(1, (bh - GAP * (len(rows) - 1)) / sum(hs))
            area = sum(h * s * (bw - GAP * (len(r) - 1)) * s for r, h in zip(rows, hs))
            area *= 1 - .04 * abs(order.index(names[0]))      # la 1re image reste de préférence en tête
            if best is None or area > best[0] + 1:
                best = (area, rows, [h * s for h in hs])
    _, rows, hs = best
    out = []
    for r, h in zip(rows, hs):
        cells = ''.join(f'<img src="../images/{x}.jpg" style="height:{h:.1f}px;width:{h * DIM[x][0] / DIM[x][1]:.1f}px" alt="">' for x in r)
        out.append(f'<div class="row">{cells}</div>')
    return ''.join(out)


def foot(n, theme):
    return f'<footer class="pf"><span class="wm row">{WM}</span><span>{SITE}</span><span class="pn">{n:02d}</span></footer>'


pages = []

# 1. Couverture
pages.append(f'''
<section class="page dark cover">
  <div class="cv-l">
    <p class="kicker"><span class="pill pill-pink">Portfolio</span>Communication &amp; Design graphique</p>
    <span class="wm big">{WM}</span>
    <p class="cv-sub">Identité visuelle · Affiches · Communication événementielle · Photographie</p>
    <p class="cv-year">Book 2026</p>
  </div>
  <div class="cv-r">{fit(['low-bass-invitation', 'cochonnade-des-voiles'], 470, 600)}</div>
</section>''')

# 2. À propos + sommaire
proj_pages = {}
num = 3
for p in P:
    proj_pages[p['id']] = num
    num += 1
toc = ''.join(f'<li><span class="n">{proj_pages[p["id"]]:02d}</span><span class="tt">{html.unescape(p["title"].replace("<em>", "").replace("</em>", ""))}</span><span class="c">{CAT[p["cat"]]}</span></li>' for p in P)
pages.append(f'''
<section class="page light about">
  <div class="ab-l">
    <span class="pill pill-black">À propos</span>
    <h2 class="t">{rsvg('À <em>propos</em>')}</h2>
    <p class="lead">Étudiante en <strong>Master Stratégie Digitale &amp; Innovations</strong>.<br>Communication, direction artistique, création graphique.</p>
    <ul class="exp">
      <li>Identité visuelle</li><li>Design graphique</li><li>Stratégie digitale</li><li>Création de contenu</li><li>Communication</li>
    </ul>
  </div>
  <div class="ab-r">
    <span class="pill pill-pink">Sommaire</span>
    <ol class="toc">{toc}</ol>
  </div>
  {foot(2, 'light')}
</section>''')

# Pages projets
for i, p in enumerate(P):
    n = proj_pages[p['id']]
    theme = 'light' if p['cat'] == 'photo' or i % 4 == 3 else 'dark'
    specs = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [('Cadre', p['cadre'])] + p['specs'])
    desc = ''.join(f'<p>{d}</p>' for d in p['desc'])
    names = [x for x, _ in p['imgs']]
    if names:
        visual = fit(names, W - 2 * M - 330 - 44, H - 2 * M - 46)
    else:
        visual = f'<div class="txtcard"><span class="big">{rsvg("SEO <em>&amp; GEO</em>")}</span><span>E-commerce · PrestaShop · réseaux sociaux</span></div>'
    pages.append(f'''
<section class="page {theme} proj">
  <div class="pj-l">
    <span class="pill {'pill-white' if theme == 'dark' else 'pill-black'}">{i + 1:02d} — {CAT[p['cat']]}</span>
    <h2 class="t">{rsvg(p['title'])}</h2>
    <p class="type">{p['type']}</p>
    <div class="desc">{desc}</div>
    <dl class="specs">{specs}</dl>
  </div>
  <div class="pj-r">{visual}</div>
  {foot(n, theme)}
</section>''')

# Contact
pages.append(f'''
<section class="page rose contact">
  <div class="ct-l">
    <span class="pill pill-black">Contact</span>
    <h2 class="t big">{rsvg('Con<em>tact</em>')}</h2>
    <p class="lead">Pour toute demande ou collaboration.</p>
    <ul class="links">
      <li><b>E-mail</b>laura.tuppo25@gmail.com</li>
      <li><b>LinkedIn</b>linkedin.com/in/profil-de-laura-tuppo</li>
      <li><b>Site</b>{SITE}</li>
    </ul>
  </div>
  <span class="wm end">{WM}</span>
</section>''')

css = f'''
@page{{size:{W}px {H}px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#141414}}
body{{font-family:'Raleway','Helvetica Neue',Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
ul,ol{{list-style:none}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;padding:{M}px;break-after:page;page-break-after:always}}
.dark{{background:#141414;color:#fff}}
.light{{background:#fff;color:#141414}}
.rose{{background:#dfa0be;color:#141414}}
.pill{{display:inline-block;align-self:flex-start;justify-self:start;border-radius:999px;padding:6px 16px;font-family:'Lexend',Arial,sans-serif;font-weight:600;font-size:13px;line-height:1.3}}
.pill-black{{background:#141414;color:#fff}}.pill-white{{background:#fff;color:#141414}}.pill-pink{{background:#dfa0be;color:#141414}}
.rs{{display:inline-block;height:1em;vertical-align:-.264em;fill:currentColor;overflow:visible}}
.rs .e{{fill:#dfa0be}}
.light .rs .e{{fill:#c27597}}
.rose .rs .e{{fill:#fff}}
.t{{font-weight:400;font-size:66px;line-height:1.02}}
.t.big{{font-size:120px}}
.wm{{display:inline-grid;justify-items:start;gap:.04em;font-size:calc(var(--w,320px) * {K_L:.4f});line-height:0}}
.wm .rs{{display:block}}
.wm-l{{color:var(--wl,#fff)}}
.wm-t{{color:var(--wt,#dfa0be);font-size:{K_T:.4f}em;margin-top:-.45em}}
.wm.row{{display:inline-flex;align-items:flex-end;gap:.25em;font-size:18px}}
.wm.row .wm-t{{margin:0 0 .12em}}
.light .wm,.rose .wm{{--wl:#141414}}
/* pied de page */
.pf{{position:absolute;left:{M}px;right:{M}px;bottom:24px;display:flex;align-items:center;gap:24px;font-family:'Lexend',Arial,sans-serif;font-size:11px;color:#a8a8a8}}
.light .pf{{color:#8a8a8a}}
.pf span:nth-child(2){{flex:1;text-align:right}}
.pn{{font-weight:600;color:inherit}}
/* couverture */
.cover{{display:grid;grid-template-columns:1fr 470px;gap:48px;align-items:center}}
.cv-l{{display:flex;flex-direction:column;gap:34px}}
.kicker{{display:flex;align-items:center;gap:14px;font-family:'Lexend',Arial,sans-serif;font-weight:500;font-size:16px}}
.wm.big{{--w:440px}}
.cv-sub{{font-size:16px;color:#bdbdbd;line-height:1.6;max-width:30em}}
.cv-year{{font-family:'Lexend',Arial,sans-serif;font-size:13px;color:#dfa0be;letter-spacing:.2em;text-transform:uppercase}}
.cv-r{{display:flex;flex-direction:column;gap:{GAP}px;align-items:center}}
/* images */
.row{{display:flex;gap:{GAP}px;justify-content:center}}
.row img{{display:block;border-radius:12px;object-fit:cover}}
.cv-r .row img{{border-radius:16px}}
/* à propos */
.about{{display:grid;grid-template-columns:1fr 1fr;gap:64px}}
.ab-l,.ab-r{{display:flex;flex-direction:column;gap:22px}}
.lead{{font-size:21px;line-height:1.5;font-weight:300}}
.lead strong{{font-weight:500}}
.exp{{border-top:1px solid rgba(20,20,20,.14);margin-top:6px}}
.exp li{{padding:11px 0;border-bottom:1px solid rgba(20,20,20,.14);font-family:'Lexend',Arial,sans-serif;font-size:16px}}
.toc{{border-top:1px solid rgba(20,20,20,.14)}}
.toc li{{display:grid;grid-template-columns:34px 1fr auto;gap:10px;padding:6.5px 0;border-bottom:1px solid rgba(20,20,20,.1);font-size:13px;align-items:baseline}}
.toc .n{{font-family:'Lexend',Arial,sans-serif;font-weight:600;color:#c27597}}
.toc .c{{color:#8a8a8a;font-size:11px}}
/* projets */
.proj{{display:grid;grid-template-columns:330px 1fr;gap:44px;padding-bottom:{M + 46 - 10}px}}
.pj-l{{display:flex;flex-direction:column;gap:16px;align-self:start}}
.type{{font-family:'Lexend',Arial,sans-serif;font-size:14px;color:#dfa0be}}
.light .type{{color:#b0678b}}
.desc{{display:flex;flex-direction:column;gap:8px;font-size:15px;line-height:1.6;font-weight:300}}
.specs{{border-top:1px solid rgba(255,255,255,.16);margin-top:6px}}
.light .specs{{border-color:rgba(20,20,20,.14)}}
.specs div{{display:grid;grid-template-columns:96px 1fr;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:12.5px}}
.light .specs div{{border-color:rgba(20,20,20,.1)}}
.specs dt{{color:#a8a8a8}}
.pj-r{{display:flex;flex-direction:column;gap:{GAP}px;justify-content:center;align-items:center;height:100%}}
.txtcard{{width:100%;height:100%;border-radius:16px;background:#dfa0be;color:#141414;display:flex;flex-direction:column;justify-content:center;gap:18px;padding:60px;font-family:'Lexend',Arial,sans-serif}}
.txtcard .big{{font-size:110px;line-height:.95}}
.txtcard .rs .e{{fill:#fff}}
/* contact */
.contact{{display:grid;grid-template-columns:1fr auto;align-items:center;gap:48px}}
.ct-l{{display:flex;flex-direction:column;gap:24px}}
.links{{border-top:1px solid rgba(20,20,20,.2);margin-top:8px}}
.links li{{display:grid;grid-template-columns:110px 1fr;padding:13px 0;border-bottom:1px solid rgba(20,20,20,.2);font-size:17px}}
.links b{{font-family:'Lexend',Arial,sans-serif;font-weight:600;font-size:13px;align-self:center}}
.wm.end{{--w:380px;--wt:#fff}}
'''

page = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Laura Tuppo — Book</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600&family=Raleway:wght@300;400;500;600&display=swap">
<style>{css}</style></head>
<body>{sprite()}{''.join(pages)}</body></html>'''

os.makedirs('pdf', exist_ok=True)
open('pdf/book.html', 'w', encoding='utf-8').write(page)
print('pdf/book.html', len(pages), 'pages')
