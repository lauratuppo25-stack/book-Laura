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
M = 64                                         # marge
SITE = 'lauratuppo25-stack.github.io/book-Laura'
GAP = 16


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



proj = {p['id']: p for p in P}
SEL = [  # projets retenus et images montrées (moins chargé que le site)
    ('lowbass', ['low-bass-invitation', 'low-bass-pass']),
    ('voiles', ['cochonnade-des-voiles', 'voiles-aml-music']),
    ('bistro', ['bistro-logo']),
    ('regina', ['regina-logo', 'regina-tropical']),
    ('dondusang', ['don-du-sang-affiche', 'don-du-sang-abribus']),
    ('siroo', ['siroo-bouteille', 'siroo-fraise']),
    ('comptoir', ['comptoir-chef-en-cave', 'comptoir-whisky-sour']),
    ('cic', ['cic-abribus', 'cic-cartes']),
    ('enzo', ['enzos-birthday']),
    ('futurs', ['futurs-affiche', 'futurs-abribus']),
]


def plain(t):
    return html.unescape(t.replace('<em>', '').replace('</em>', ''))


def foot(n):
    return f'<footer class="pf"><span class="wm row">{WM}</span><span class="pn">{n:02d}</span></footer>'


pages = []

# Couverture
pages.append(f"""
<section class="page dark cover bg-aurora">
  <p class="kicker">Portfolio</p>
  <span class="wm big">{WM}</span>
  <div class="cv-b"><span>Communication &amp; Design graphique</span><span>Book 2026</span></div>
</section>""")

# À propos
pages.append(f"""
<section class="page light about bg-mist">
  <figure class="ab-photo"><img src="../images/laura-portrait-rose.jpg" alt=""></figure>
  <div class="ab-t">
    <p class="label">À propos</p>
    <h2 class="t">{rsvg('À <em>propos</em>')}</h2>
    <p class="lead">Étudiante en Master Stratégie Digitale &amp; Innovations à l’IFC Avignon. Communication, direction artistique, création graphique.</p>
    <p class="txt">Alternance en communication chez Sorhobis Boissons, puis chez Pallas Cuir. Identités visuelles, affiches, événements, contenus pour les réseaux sociaux et photographie produit.</p>
    <dl class="facts">
      <div><dt>Basée à</dt><dd>Saint-Rémy-de-Provence</dd></div>
      <div><dt>Expertises</dt><dd>Identité visuelle · Design graphique · Stratégie digitale · Création de contenu · Communication</dd></div>
    </dl>
  </div>
  {foot(2)}
</section>""")

# Projets : une page chacun, texte minimal, images respirantes
n = 3
for i, (pid, imgs) in enumerate(SEL):
    p = proj[pid]
    theme = 'light' if i % 3 == 2 else 'dark'
    bg = ['bg-glow-br', '', 'bg-mist', 'bg-glow-tl', '', 'bg-mist-r', 'bg-glow-br', '', 'bg-mist', 'bg-aurora'][i]
    side = 'left' if i % 2 == 0 else 'right'
    pages.append(f"""
<section class="page {theme} proj {side} {bg}">
  <div class="pj-t">
    <p class="num">{i + 1:02d}</p>
    <h2 class="t">{rsvg(p['title'])}</h2>
    <p class="type">{p['type']} · {p['cadre']}</p>
    <p class="desc">{p['desc'][0]}</p>
  </div>
  <div class="pj-i">{fit(imgs, W - 2 * M - 290 - 56, H - 2 * M - 40)}</div>
  {foot(n)}
</section>""")
    n += 1

# Photographie
cells = ''.join(f'<figure><img src="../images/{x}.jpg" alt=""><figcaption>{c}</figcaption></figure>' for x, c in
                [('roumaniere-3', 'La Roumanière'), ('cherico-verse', 'Chérico'), ('bda-cafe-glace', 'Le Bistro des Arènes')])
pages.append(f"""
<section class="page light photo bg-mist-r">
  <div class="ph-t">
    <p class="num">11</p>
    <h2 class="t">{rsvg('Photo<em>graphie</em>')}</h2>
    <p class="desc">Shootings produit et lifestyle. Direction artistique, prise de vue, retouche.</p>
  </div>
  <div class="ph-g">{cells}</div>
  {foot(n)}
</section>""")

# Contact
pages.append(f"""
<section class="page rose contact bg-rose">
  <p class="label">Contact</p>
  <h2 class="t big">{rsvg('Con<em>tact</em>')}</h2>
  <ul class="links">
    <li>laura.tuppo25@gmail.com</li>
    <li>linkedin.com/in/profil-de-laura-tuppo</li>
    <li>{SITE}</li>
  </ul>
  <span class="wm end">{WM}</span>
</section>""")

css = f"""
@page{{size:{W}px {H}px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#141414}}
body{{font-family:'Raleway','Helvetica Neue',Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
ul{{list-style:none}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;padding:{M}px;break-after:page;page-break-after:always}}
.dark{{background:#141414;color:#fff}}
.light{{background:#fff;color:#141414}}
.rose{{background:#dfa0be;color:#141414}}
.rs{{display:inline-block;height:1em;vertical-align:-.264em;fill:currentColor;overflow:visible}}
.rs .e{{fill:#dfa0be}}
.light .rs .e{{fill:#c27597}}
.rose .rs .e{{fill:#fff}}
.t{{font-weight:400;font-size:52px;line-height:1.05}}
.t.big{{font-size:150px}}
.label,.kicker{{font-family:'Lexend',Arial,sans-serif;font-size:11px;letter-spacing:.28em;text-transform:uppercase}}
.wm{{display:inline-grid;justify-items:start;gap:.04em;font-size:calc(var(--w,320px) * {K_L:.4f});line-height:0}}
.wm .rs{{display:block}}
.wm-l{{color:var(--wl,#fff)}}
.wm-t{{color:var(--wt,#dfa0be);font-size:{K_T:.4f}em;margin-top:-.45em}}
.wm.row{{display:inline-flex;align-items:flex-end;gap:.25em;font-size:15px}}
.wm.row .wm-t{{margin:0 0 .12em}}
.light .wm,.rose .wm{{--wl:#141414}}
.pf{{position:absolute;left:{M}px;right:{M}px;bottom:26px;display:flex;justify-content:space-between;align-items:center;font-family:'Lexend',Arial,sans-serif;font-size:10px;color:#9a9a9a}}
/* fonds en dégradé et halos flous (palette noir, blanc, rose) */
.bg-aurora{{background:
  radial-gradient(ellipse 620px 520px at 88% 18%,rgba(223,160,190,.42),rgba(223,160,190,0) 70%),
  radial-gradient(ellipse 520px 460px at 72% 92%,rgba(194,117,151,.30),rgba(194,117,151,0) 70%),
  radial-gradient(ellipse 480px 420px at 6% 100%,rgba(255,255,255,.07),rgba(255,255,255,0) 70%),
  linear-gradient(160deg,#1c1719 0%,#141414 55%,#0f0d0e 100%)}}
.bg-glow-br{{background:radial-gradient(ellipse 560px 460px at 95% 105%,rgba(223,160,190,.32),rgba(223,160,190,0) 70%),linear-gradient(180deg,#161415,#121112)}}
.bg-glow-tl{{background:radial-gradient(ellipse 600px 480px at -5% -8%,rgba(223,160,190,.30),rgba(223,160,190,0) 70%),linear-gradient(0deg,#141414,#181516)}}
.bg-mist{{background:radial-gradient(ellipse 640px 520px at 100% 0%,rgba(223,160,190,.38),rgba(223,160,190,0) 72%),radial-gradient(ellipse 520px 420px at 0% 100%,rgba(223,160,190,.18),rgba(223,160,190,0) 72%),#fff}}
.bg-mist-r{{background:radial-gradient(ellipse 700px 560px at 0% 0%,rgba(223,160,190,.34),rgba(223,160,190,0) 72%),linear-gradient(135deg,#fff 40%,#fbeef4 100%)}}
.bg-rose{{background:radial-gradient(ellipse 620px 520px at 85% 20%,rgba(255,255,255,.55),rgba(255,255,255,0) 70%),radial-gradient(ellipse 560px 480px at 10% 95%,rgba(150,80,112,.35),rgba(150,80,112,0) 70%),linear-gradient(140deg,#e9b6cd 0%,#dfa0be 50%,#cf8aab 100%)}}
/* couverture */
.cover{{display:flex;flex-direction:column;justify-content:center;gap:40px;padding:{M + 30}px}}
.cover .kicker{{color:#dfa0be}}
.wm.big{{--w:520px}}
.cv-b{{position:absolute;left:{M + 30}px;right:{M + 30}px;bottom:{M}px;display:flex;justify-content:space-between;font-family:'Lexend',Arial,sans-serif;font-size:12px;color:#9a9a9a;letter-spacing:.06em}}
/* à propos */
.about{{display:grid;grid-template-columns:440px 1fr;gap:72px;align-items:center;padding-bottom:{M + 20}px}}
.ab-photo{{margin:0;width:440px;aspect-ratio:1122/1402;align-self:center;border-radius:220px 220px 18px 18px;overflow:hidden}}
.ab-photo img{{width:100%;height:100%;object-fit:cover;object-position:50% 50%;display:block}}
.ab-t{{display:flex;flex-direction:column;gap:22px;max-width:470px}}
.ab-t .label{{color:#c27597}}
.lead{{font-size:21px;line-height:1.5;font-weight:300}}
.txt{{font-size:14px;line-height:1.75;color:#555}}
.facts{{border-top:1px solid #e6e6e6;margin-top:6px}}
.facts div{{display:grid;grid-template-columns:100px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid #e6e6e6;font-size:13px;line-height:1.5}}
.facts dt{{color:#9a9a9a}}
/* projets */
.proj{{display:grid;grid-template-columns:290px 1fr;gap:56px;padding-bottom:{M + 40}px}}
.proj.right{{grid-template-columns:1fr 290px}}
.proj.right .pj-t{{order:2}}
.pj-t{{align-self:end;display:flex;flex-direction:column;gap:12px}}
.num{{font-family:'Lexend',Arial,sans-serif;font-size:12px;letter-spacing:.2em;color:#dfa0be}}
.light .num{{color:#c27597}}
.type{{font-family:'Lexend',Arial,sans-serif;font-size:11px;letter-spacing:.06em;color:#9a9a9a;text-transform:uppercase}}
.desc{{font-size:14px;line-height:1.7;font-weight:300;max-width:26em}}
.pj-i{{display:flex;flex-direction:column;gap:{GAP}px;justify-content:center;align-items:center}}
.row{{display:flex;gap:{GAP}px;justify-content:center}}
.row img{{display:block;border-radius:10px;object-fit:cover}}
/* photographie */
.photo{{display:grid;grid-template-rows:auto 1fr;gap:34px;padding-bottom:{M + 40}px}}
.ph-t{{display:grid;grid-template-columns:auto 1fr;align-items:end;gap:6px 40px}}
.ph-t .num{{grid-column:1 / -1}}
.ph-t .desc{{justify-self:end;text-align:right}}
.ph-g{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;min-height:0}}
.ph-g figure{{margin:0;display:flex;flex-direction:column;gap:10px;min-height:0}}
.ph-g img{{flex:1;min-height:0;width:100%;object-fit:cover;border-radius:10px;display:block}}
.ph-g figcaption{{font-family:'Lexend',Arial,sans-serif;font-size:11px;color:#9a9a9a}}
/* contact */
.contact{{display:flex;flex-direction:column;justify-content:center;gap:26px;padding:{M + 30}px}}
.links li{{font-size:19px;padding:10px 0;border-bottom:1px solid rgba(20,20,20,.2);max-width:520px}}
.wm.end{{position:absolute;right:{M + 30}px;bottom:{M}px;--w:300px;--wt:#fff}}
"""

page = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Laura Tuppo — Book</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600&family=Raleway:wght@300;400;500;600&display=swap">
<style>{css}</style></head>
<body>{sprite()}{''.join(pages)}</body></html>"""

os.makedirs('pdf', exist_ok=True)
open('pdf/book.html', 'w', encoding='utf-8').write(page)
print('pdf/book.html', len(pages), 'pages')
