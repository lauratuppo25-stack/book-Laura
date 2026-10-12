"""Carrousel LinkedIn (PDF 1080 × 1350) dans la DA du portfolio.

Génère carousel/carrousel.html ; le PDF est imprimé ensuite avec Chromium.
Usage : python3 tools/carousel.py .
"""
import html, os, runpy, sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
os.chdir(root)
sys.argv = [os.path.join(root, 'tools', 'build.py'), root]
B = runpy.run_path(sys.argv[0])          # réutilise les outils du site (Riesling, images, projets)
rtext, rsvg, sprite, DIM, WM_IN, P = B['rtext'], B['rsvg'], B['sprite'], B['DIM'], B['WM_IN'], B['P']
K_L, K_T = B['BOX'] / B['width_of']('LAURA'), .63 * B['width_of']('LAURA') / B['width_of']('TUPPO')

W, H = 1080, 1350
PAD = 84
SITE = 'lauratuppo25-stack.github.io/book-Laura'
proj = {p['id']: p for p in P}


def photo_rows(rows, box_w, box_h, gap=18):
    """Rangées d'images entières (sans recadrage), mises à l'échelle pour tenir dans la zone."""
    out, heights = [], []
    for row in rows:
        ratios = [DIM[n][0] / DIM[n][1] for n in row]
        heights.append((box_w - gap * (len(row) - 1)) / sum(ratios))
    scale = min(1, (box_h - gap * (len(rows) - 1)) / sum(heights))
    for row, h in zip(rows, heights):
        h *= scale
        cells = ''.join(f'<img src="../images/{n}.jpg" style="height:{h:.0f}px;width:{h * DIM[n][0] / DIM[n][1]:.0f}px" alt="">' for n in row)
        out.append(f'<div class="row">{cells}</div>')
    return f'<div class="photos" style="gap:{gap}px">{"".join(out)}</div>'


def project_slide(n, pid, rows, title=None, desc=None, theme='dark'):
    p = proj[pid]
    cat = B['CAT'][p['cat']]
    d = desc or p['desc'][0]
    return f'''
<section class="slide {theme}">
  <header class="ph">
    <span class="pill {'pill-white' if theme == 'dark' else 'pill-black'}">{n:02d} — {cat}</span>
    <h2 class="t">{rsvg(title or p['title'])}</h2>
    <p class="type">{p['type']} · {p['cadre']}</p>
    <p class="desc">{d}</p>
  </header>
  {photo_rows(rows, W - 2 * PAD, 780)}
  <footer class="sf"><span class="wm row">{WM_IN}</span><span>{SITE}</span></footer>
</section>'''


slides = []

# 1. Couverture
slides.append(f'''
<section class="slide dark cover">
  <p class="kicker"><span class="pill pill-pink">Portfolio</span>Communication &amp; Design graphique</p>
  <span class="wm big">{WM_IN}</span>
  <div class="cover-strip">
    <img src="../images/low-bass-invitation.jpg" alt=""><img src="../images/cochonnade-des-voiles.jpg" alt=""><img src="../images/regina-tropical.jpg" alt=""><img src="../images/siroo-bouteille.jpg" alt="">
  </div>
  <p class="swipe">Projets sélectionnés <span>→</span></p>
</section>''')

# 2. À propos
slides.append(f'''
<section class="slide light about">
  <span class="pill pill-black">À propos</span>
  <h2 class="t big">{rsvg('À <em>propos</em>')}</h2>
  <p class="lead">Étudiante en <strong>Master Stratégie Digitale &amp; Innovations</strong>.<br>Communication, direction artistique, création graphique.</p>
  <ul class="skills">
    <li>{rsvg('Identité <em>visuelle</em>')}</li>
    <li>{rsvg('Design <em>graphique</em>')}</li>
    <li>{rsvg('Stratégie <em>digitale</em>')}</li>
    <li>{rsvg('Création <em>de contenu</em>')}</li>
    <li>{rsvg('Commu<em>nication</em>')}</li>
  </ul>
  <footer class="sf"><span class="wm row">{WM_IN}</span><span>{SITE}</span></footer>
</section>''')

# 3 → 10. Projets phares
slides += [
    project_slide(1, 'lowbass', [['low-bass-invitation', 'low-bass-stay-tuned'], ['low-bass-pass', 'low-bass-dashboard']],
                  desc='Château Romanin, 22 novembre. Teaser, invitation exclusive et mini-site de réservation avec billet QR.'),
    project_slide(2, 'voiles', [['cochonnade-des-voiles', 'voiles-aml-music']]),
    project_slide(3, 'bistro', [['bistro-logo'], ['bda-cafe', 'bda-cafe-glace', 'bda-assiette']], theme='light',
                  desc='Logotype inspiré de la porte des Arènes de Beaucaire, puis shooting photo du restaurant.'),
    project_slide(4, 'regina', [['regina-logo', 'regina-programme', 'regina-tropical']]),
    project_slide(5, 'dondusang', [['don-du-sang-affiche', 'don-du-sang-abribus']]),
    project_slide(6, 'siroo', [['siroo-bouteille'], ['siroo-fraise', 'siroo-peche']], theme='light'),
    project_slide(7, 'comptoir', [['comptoir-chef-en-cave', 'comptoir-whisky-sour'], ['comptoir-plv-futs', 'comptoir-rayon']]),
    project_slide(8, 'cic', [['cic-abribus'], ['cic-app', 'cic-cartes']], theme='light'),
]

# 11. Photographie
tiles = [('roumaniere-3', 'La <em>Roumanière</em>'), ('cherico-verse', 'Chérico'), ('bda-cafe-glace', 'Le Bistro <em>des Arènes</em>'),
         ('roumaniere-1', ''), ('cherico-duo', ''), ('bda-photo-3', '')]
cells = ''.join(f'<figure><img src="../images/{n}.jpg" alt=""></figure>' for n, _ in tiles)
slides.append(f'''
<section class="slide dark">
  <header class="ph">
    <span class="pill pill-pink">Photographie</span>
    <h2 class="t">{rsvg('Shootings <em>produit</em>')}</h2>
    <p class="desc">La Roumanière, Chérico, Le Bistro des Arènes. Direction artistique, prise de vue, retouche.</p>
  </header>
  <div class="tiles">{cells}</div>
  <footer class="sf"><span class="wm row">{WM_IN}</span><span>{SITE}</span></footer>
</section>''')

# 12. Contact
slides.append(f'''
<section class="slide rose contact">
  <span class="pill pill-black">Portfolio complet</span>
  <h2 class="t big">{rsvg('Tous les <em>projets</em>')}</h2>
  <p class="url">{SITE}</p>
  <ul class="links">
    <li><b>E-mail</b>laura.tuppo25@gmail.com</li>
    <li><b>LinkedIn</b>Laura Tuppo</li>
    <li><b>CV</b>à télécharger sur le site</li>
  </ul>
  <span class="wm end">{WM_IN}</span>
</section>''')

page = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Laura Tuppo — Portfolio (carrousel)</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600&family=Raleway:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="../assets/site.css">
<style>
@page{{size:{W}px {H}px;margin:0}}
html,body{{margin:0;background:#141414;overflow:visible}}
.slide{{position:relative;width:{W}px;height:{H}px;overflow:hidden;box-sizing:border-box;padding:{PAD}px {PAD}px 0;display:flex;flex-direction:column;gap:30px;page-break-after:always;break-after:page}}
.slide.light{{background:#fff;color:#141414}}
.slide.dark{{background:#141414;color:#fff}}
.slide.rose{{background:#dfa0be;color:#141414}}
.pill{{font-size:22px;align-self:flex-start}}
.t{{font-size:118px;line-height:.95;margin:0}}
.t.big{{font-size:170px}}
.rose .rs .e{{fill:#fff}}
.light .rs .e{{fill:#c9799f}}
.ph{{display:flex;flex-direction:column;gap:16px}}
.type{{margin:0;font-family:var(--title);font-size:24px;color:#dfa0be}}
.light .type{{color:#b0678b}}
.desc{{margin:0;font-size:27px;line-height:1.45;max-width:30em;font-weight:300}}
.photos{{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;padding-bottom:120px}}
.photos .row{{display:flex;gap:18px;justify-content:center}}
.photos img{{display:block;border-radius:20px;object-fit:cover;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
.light .photos img{{box-shadow:0 18px 40px rgba(20,20,20,.16)}}
.sf{{position:absolute;left:{PAD}px;right:{PAD}px;bottom:44px;display:flex;justify-content:space-between;align-items:center;font-family:var(--title);font-size:19px;color:#a8a8a8}}
.light .sf{{color:#6b6b6b}}
.sf .wm{{--h:34px;--wm-l:currentColor}}
.dark .sf .wm{{--wm-l:#fff}}
.light .sf .wm{{--wm-l:#141414}}
.wm{{font-size:calc(var(--w,320px) * {K_L:.4f})}}
.wm-t{{font-size:{K_T:.4f}em}}
/* couverture */
.cover{{justify-content:center;gap:40px;padding-top:70px;padding-bottom:70px}}
.cover::after{{content:"";position:absolute;right:-220px;top:-160px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(223,160,190,.22),transparent 64%)}}
.kicker{{display:flex;align-items:center;gap:20px;font-family:var(--title);font-weight:500;font-size:28px;margin:0;position:relative;z-index:1}}
.wm.big{{--w:700px;--wm-l:#fff;position:relative;z-index:1}}
.cover-strip{{display:flex;gap:18px;position:relative;z-index:1;margin-top:12px}}
.cover-strip img{{width:196px;height:270px;object-fit:cover;border-radius:18px;box-shadow:0 20px 50px rgba(0,0,0,.5)}}
.cover-strip img:nth-child(odd){{transform:rotate(-3deg)}}
.cover-strip img:nth-child(even){{transform:rotate(3deg) translateY(16px)}}
.swipe{{margin:0;font-family:var(--title);font-size:26px;color:#dfa0be;position:relative;z-index:1}}
.swipe span{{display:inline-block;margin-left:10px}}
/* à propos */
.about{{justify-content:center;gap:34px;padding-bottom:120px}}
.lead{{margin:0;font-size:40px;line-height:1.35;font-weight:300}}
.lead strong{{font-weight:500}}
.skills{{list-style:none;margin:20px 0 0;padding:0;border-top:1px solid rgba(20,20,20,.14)}}
.skills li{{font-size:70px;line-height:1;padding:18px 0;border-bottom:1px solid rgba(20,20,20,.14)}}
/* photographie */
.tiles{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:20px}}
.tiles figure{{margin:0;aspect-ratio:1;border-radius:24px;overflow:hidden}}
.tiles img{{width:100%;height:100%;object-fit:cover;display:block}}
/* contact */
.contact{{justify-content:center;gap:36px;padding-bottom:84px}}
.url{{margin:0;font-family:var(--title);font-weight:600;font-size:40px;background:#141414;color:#fff;border-radius:999px;padding:22px 36px;align-self:flex-start}}
.links{{list-style:none;margin:10px 0 0;padding:0;font-size:32px;border-top:1px solid rgba(20,20,20,.2)}}
.links li{{display:grid;grid-template-columns:200px 1fr;padding:20px 0;border-bottom:1px solid rgba(20,20,20,.2)}}
.links b{{font-family:var(--title);font-weight:600;font-size:24px;align-self:center}}
.wm.end{{--w:520px;--wm-t:#fff;margin-top:30px}}
</style></head>
<body>
{sprite()}
{''.join(slides)}
</body></html>'''

os.makedirs('carousel', exist_ok=True)
open('carousel/carrousel.html', 'w', encoding='utf-8').write(page)
print('carousel/carrousel.html', len(slides), 'pages')
