"""Génère index.html du portfolio (version éditoriale)."""
import html, os, sys

ROOT = sys.argv[1]
os.chdir(ROOT)

DIM = {}
from PIL import Image
for f in os.listdir('images'):
    if f.endswith('.jpg'):
        with Image.open('images/' + f) as im:
            DIM[f[:-4]] = im.size

def img(name, alt, cls='', lazy=True, extra=''):
    w, h = DIM[name]
    c = f' class="{cls}"' if cls else ''
    l = ' loading="lazy"' if lazy else ''
    return f'<img{c} src="images/{name}.jpg" width="{w}" height="{h}"{l} alt="{html.escape(alt)}"{extra}>'


# ─────────────────────────────────────────────── Typo Riesling → tracés SVG
# La police n'est pas publiée : les titres sont convertis en tracés vectoriels.
# Chemin de la police : variable RIESLING ou tools/riesling.ttf (ignoré par git).
import re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
FONT = os.environ.get('RIESLING') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'riesling.ttf')
_f = TTFont(FONT)
_gs, _cmap, _hmtx = _f.getGlyphSet(), _f.getBestCmap(), _f['hmtx']
ASC, DESC = _f['hhea'].ascent, _f['hhea'].descent
BOX = ASC - DESC
_used = {}
SUBST = {'×': 'x'}

def _glyph(ch):
    ch = SUBST.get(ch, ch)
    name = _cmap.get(ord(ch))
    if name is None:
        raise SystemExit(f'Caractère absent de Riesling : {ch!r}')
    if name not in _used:
        pen = SVGPathPen(_gs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
        _gs[name].draw(TransformPen(pen, (1, 0, 0, -1, 0, ASC)))
        _used[name] = (f'rg{len(_used)}', pen.getCommands())
    return _used[name][0], _hmtx[name][0]

def _word(chars, start=0):
    """chars : liste de (caractère, accent) → un <svg> pour un mot ; --i numérote les lettres."""
    x, runs, cur, flag = 0, [], [], None
    for k, (ch, em) in enumerate(chars):
        gid, adv = _glyph(ch)
        if em != flag and cur:
            runs.append((flag, cur)); cur = []
        flag = em
        cur.append(f'<use href="#{gid}" x="{x}" style="--i:{start + k}"/>')
        x += adv
    if cur:
        runs.append((flag, cur))
    body = ''.join(('<g class="e">' + ''.join(u) + '</g>') if em else ''.join(u) for em, u in runs)
    return f'<svg class="rs" viewBox="0 0 {x} {BOX}" style="width:{x / BOX:.3f}em">{body}</svg>'

def rsvg(marked):
    """Texte (avec <em> pour la partie rose) → mots en SVG, sans texte alternatif."""
    chars, em = [], False
    for part in re.split(r'(</?em>)', marked):
        if part == '<em>': em = True
        elif part == '</em>': em = False
        else: chars += [(c, em) for c in html.unescape(part)]
    words, cur, n = [], [], 0
    for c in chars + [(' ', False)]:
        if c[0] == ' ':
            if cur: words.append(_word(cur, n)); n += len(cur) + 1; cur = []
        else:
            cur.append(c)
    return ' '.join(words)

def rtext(marked):
    plain = html.unescape(re.sub(r'</?em>', '', marked))
    return f'<span class="sr">{html.escape(plain)}</span><span class="rt" aria-hidden="true">{rsvg(marked)}</span>'

def sprite():
    paths = ''.join(f'<path id="{gid}" d="{d}"/>' for gid, d in _used.values())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{paths}</defs></svg>'

def width_of(text):
    return sum(_glyph(c)[1] for c in text)

# ─────────────────────────────────────────────── Projets
# cat: graphisme | communication | photo
P = [
 dict(id='bistro', cat='graphisme', cadre='Client', type='Identité visuelle', title='Le Bistro <em>des Arènes</em>',
      desc=['Logotype d’un restaurant bistronomique. Arche des Arènes de Nîmes, typographie Art déco.'],
      specs=[('Livrables', 'Logo, charte, mockup'), ('Outils', 'Illustrator, Photoshop')],
      cover='bistro-logo', imgs=[('bistro-logo', 'Logo Le Bistro des Arènes en lettrage blanc sur une vitrine')]),
 dict(id='regina', cat='graphisme', cadre='Client', type='Identité & réseaux sociaux', title='Le <em>Régina</em>',
      desc=['Identité d’un bar-café : serif terracotta, script doré. Stories des soirées de l’été 2025.'],
      specs=[('Livrables', 'Logo, stories, programme'), ('Date', 'Juillet 2025')],
      cover='regina-tropical', imgs=[('regina-logo', 'Logotype Le Régina bar-café'), ('regina-programme', 'Story Instagram, programme de la Saint-Éloi 2025'), ('regina-tropical', 'Story Instagram, Tropical Flower Night')]),
 dict(id='cochonnade', cat='graphisme', cadre='Client', type='Affiche événementielle', title='La Cochonnade <em>des Voiles</em>',
      desc=['Affiche du BBQ du 14 juillet. Titre gravé dans la viande, monochrome bleu.'],
      specs=[('Lieu', 'Les Voiles, Beaucaire'), ('Outils', 'Photoshop, Illustrator')],
      cover='cochonnade-des-voiles', imgs=[('cochonnade-des-voiles', 'Affiche La Cochonnade des Voiles')]),
 dict(id='siroo', cat='graphisme', cadre='École', type='Branding & packaging', title='Siroo, <em>le goût en boucle</em>',
      desc=['Marque fictive de sirops rechargeables. Logo par saveur, étiquettes ovales.'],
      specs=[('Livrables', 'Logo, étiquettes, mockup'), ('Outils', 'Illustrator, Photoshop')],
      cover='siroo-bouteille', imgs=[('siroo-fraise', 'Étiquette Siroo goût fraise'), ('siroo-peche', 'Étiquette Siroo goût pêche'), ('siroo-bouteille', 'Bouteille Siroo framboise')]),
 dict(id='enzo', cat='graphisme', cadre='Client', type='Invitation', title='Enzo’s <em>Birthday</em>',
      desc=['Invitation d’anniversaire. Typo liquide, collage de citrons, dégradé solaire.'],
      specs=[('Lieu', 'L’Antre des Citrons'), ('Format', 'Invitation, réseaux sociaux')],
      cover='enzos-birthday', imgs=[('enzos-birthday', 'Invitation Enzo’s Birthday')]),
 dict(id='kelloggs', cat='graphisme', cadre='École', type='Packaging', title='Kellogg’s <em>× Barbie</em>',
      desc=['Édition limitée fictive. Univers rose, goût framboise.'],
      specs=[('Livrable', 'Boîte et mise en situation'), ('Outils', 'Illustrator, Photoshop')],
      cover='kelloggs-barbie', imgs=[('kelloggs-barbie', 'Boîte de céréales Kellogg’s × Barbie sur une table')]),
 dict(id='aml', cat='graphisme', cadre='Client', type='Affiche événementielle', title='AML Music <em>aux Voiles</em>',
      desc=['Soirée DJ du 22 juillet. Portrait monochrome bleu.'],
      specs=[('Lieu', 'Les Voiles, Beaucaire'), ('Outils', 'Photoshop')],
      cover='voiles-aml-music', imgs=[('voiles-aml-music', 'Affiche AML Music aux Voiles')]),
 dict(id='comptoir', cat='graphisme', cadre='Client', type='Affiche événementielle', title='Un chef <em>en cave</em>',
      desc=['Soirée accords mets et vins. Formes organiques, script manuscrit.'],
      specs=[('Client', 'Comptoir des Vignes'), ('Outils', 'Illustrator, Photoshop')],
      cover='comptoir-chef-en-cave', imgs=[('comptoir-chef-en-cave', 'Affiche Un chef en cave, Comptoir des Vignes')]),
 dict(id='futurs', cat='graphisme', cadre='École', type='Affiche de film', title='Futur<em>(s)</em>',
      desc=['Affiche de film fictif, entre synthwave et cyberpunk.'],
      specs=[('Projet', 'Film fictif'), ('Outil', 'Photoshop')],
      cover='futurs-affiche', imgs=[('futurs-affiche', 'Affiche du film fictif Futur(s)')]),
 dict(id='lowbass', cat='communication', cadre='Client', type='Communication événementielle', title='Low <em>Bass</em>',
      desc=['Château Romanin, 22 novembre. Story teaser, puis invitation exclusive.'],
      specs=[('Lieu', 'Château Romanin, Saint-Rémy-de-Provence'), ('Date', 'Dimanche 22 novembre'), ('Formats', 'Story teaser, invitation')],
      cover='low-bass-invitation', imgs=[('low-bass-invitation', 'Invitation exclusive Low Bass au Château Romanin, dimanche 22 novembre'), ('low-bass-stay-tuned', 'Story teaser Low Bass, Stay tuned')]),
 dict(id='confort', cat='communication', cadre='École', type='Campagne de sensibilisation', title='Notre confort, <em>leur enfer.</em>',
      desc=['Campagne contre la pollution pétrolière. Visuel choc, déclinaison abribus.'],
      specs=[('Livrables', 'Affiche, abribus'), ('Outils', 'Photoshop, Illustrator')],
      cover='confort-enfer-affiche', imgs=[('confort-enfer-affiche', 'Affiche Notre confort, leur enfer'), ('confort-enfer-abribus', 'L’affiche sur un abribus')]),
 dict(id='dondusang', cat='communication', cadre='École', type='Street marketing', title='Don du sang <em>× Marvel</em>',
      desc=['Collaboration imaginaire avec Marvel. « Le vrai héros, c’est celui qui donne. »'],
      specs=[('Support', 'Abribus'), ('Outils', 'Photoshop, Illustrator')],
      cover='don-du-sang-affiche', imgs=[('don-du-sang-affiche', 'Affiche Don du sang avec Captain America'), ('don-du-sang-abribus', 'L’affiche Don du sang sur un abribus')]),
 dict(id='cic', cat='communication', cadre='École', type='Campagne & carte bancaire', title='CIC, <em>le plan Q*</em>',
      desc=['Campagne 18–25 ans autour du « Plan Q ». Abribus et carte Q+.'],
      specs=[('Cible', 'Étudiants 18–25 ans'), ('Livrables', 'Abribus, cartes Q+')],
      cover='cic-cartes', imgs=[('cic-abribus', 'Abribus CIC, le meilleur Plan Q de ta vie'), ('cic-cartes', 'Trois cartes bancaires CIC Q+')]),
 dict(id='gestiboat', cat='communication', cadre='École', type='Identité & affichage', title='GestiBoat, <em>speed boating day</em>',
      desc=['Journée Speed Boating à La Grande-Motte. Affiche et affichage urbain.'],
      specs=[('Livrables', 'Affiche, affichage urbain'), ('Outils', 'Illustrator, Canva')],
      cover='gestiboat-affiche', imgs=[('gestiboat-affiche', 'Affiche GestiBoat Speed Boating Day'), ('gestiboat-mockup', 'Affichage urbain GestiBoat')]),
 dict(id='sorhobis', cat='communication', cadre='Client', type='Bannières web', title='Sorhobis <em>Boissons</em>',
      desc=['Cinq bannières web, une par marque, chartes respectées.'],
      specs=[('Livrables', '5 bannières web'), ('Outils', 'Photoshop, Illustrator')],
      cover='stack', imgs=[('sorhobis-pastis-olive', 'Bannière Pastis Olive'), ('sorhobis-ricard', 'Bannière Ricard'), ('sorhobis-get27', 'Bannière Get 27'), ('sorhobis-citadelle', 'Bannière Citadelle'), ('sorhobis-lillet', 'Bannière Lillet')]),
 dict(id='pallas', cat='communication', cadre='Client', type='SEO / GEO & social media', title='Pallas <em>Cuir</em>',
      desc=['Audit SEO et GEO d’un site PrestaShop. Contenus réseaux sociaux.'],
      specs=[('Plateforme', 'PrestaShop'), ('Missions', 'Audit SEO, GEO, contenus')],
      cover=None, imgs=[]),
 dict(id='bda', cat='photo', cadre='Client', type='Photo food & lifestyle', title='Le Bistro <em>en images</em>',
      desc=['Cafés, cocktails, assiettes, terrasse. Direction artistique, prise de vue, retouche.'],
      specs=[('Sujets', 'Cafés, cocktails, plats'), ('Outils', 'Lightroom, Photoshop')],
      cover='bda-cafe', imgs=[('bda-cafe', 'Expresso posé sur la table'), ('bda-cafe-glace', 'Café glacé servi en terrasse'), ('bda-assiette', 'Assiette de poisson, légumes et œuf'), ('bda-photo-1', 'Bière tenue en terrasse'), ('bda-photo-2', 'Portrait en casquette, lumière naturelle'), ('bda-photo-3', 'Cocktail spritz'), ('bda-photo-4', 'Mule dans une tasse en cuivre'), ('bda-photo-5', 'Assiettes dressées')]),
 dict(id='roumaniere', cat='photo', cadre='Client', type='Photo produit', title='La <em>Roumanière</em>',
      desc=['Confiture de pêche de Provence. Fond rouge, lumière naturelle.'],
      specs=[('Produit', 'Confiture pêche de Provence'), ('Outils', 'Lightroom, Photoshop')],
      cover='roumaniere-1', imgs=[('roumaniere-1', 'Pot de confiture sur des feuilles, fond rouge'), ('roumaniere-2', 'Pot de confiture tenu en main'), ('roumaniere-3', 'Pot de confiture couché sur fond rouge')]),
 dict(id='cherico', cat='photo', cadre='Client', type='Packshot & lifestyle', title='Chérico, <em>chicorée bio</em>',
      desc=['Packshot e-commerce et image lifestyle.'],
      specs=[('Usages', 'E-commerce, réseaux sociaux'), ('Outils', 'Lightroom, Photoshop')],
      cover='cherico-lifestyle', imgs=[('cherico-packshot', 'Boîtes de chicorée Chérico'), ('cherico-lifestyle', 'Chicorée versée dans une tasse')]),
]
CAT = {'graphisme': 'Design graphique', 'communication': 'Communication', 'photo': 'Photographie'}
count = {c: sum(1 for p in P if p['cat'] == c) for c in CAT}

def card(i, p):
    num = f'{i+1:02d}'
    plain = html.unescape(p['title'].replace('<em>', '').replace('</em>', ''))
    if p['cover'] == 'stack':
        cover = '<figure class="card-img card-stack">' + ''.join(img(n, a) for n, a in p['imgs']) + '<span class="card-cta">Voir le projet</span></figure>'
    elif p['cover']:
        cover = f'<figure class="card-img">{img(p["cover"], plain)}<span class="card-cta">Voir le projet</span></figure>'
    else:
        cover = '<figure class="card-img card-text"><span class="ct-big">' + rtext('SEO <em>&amp; GEO</em>') + '</span><span class="ct-small">E-commerce · PrestaShop · réseaux sociaux</span><span class="card-cta">Voir le projet</span></figure>'
    desc = ''.join(f'<p>{d}</p>' for d in p['desc'])
    specs = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [('Discipline', CAT[p['cat']]), ('Cadre', p['cadre'])] + p['specs'])
    imgs = ''.join(f'<figure>{img(n, a)}</figure>' for n, a in p['imgs'])
    return f'''
      <article class="card rv" id="p-{p['id']}" data-cat="{p['cat']}">
        <button class="card-open" data-cursor="Voir" aria-label="Voir le projet {html.escape(plain)}">
          {cover}
          <span class="card-meta"><span class="label">{num} — {CAT[p['cat']]}</span><span class="card-title">{p['title']}</span><span class="card-type">{p['type']} · {p['cadre']}</span></span>
        </button>
        <div class="card-detail" hidden>
          <div class="d-title">{rtext(p['title'])}</div>
          <div class="d-text">{desc}</div>
          <dl class="d-specs">{specs}</dl>
          <div class="d-imgs">{imgs}</div>
        </div>
      </article>'''

cards = ''.join(card(i, p) for i, p in enumerate(P))

# ─────────────────────────────────────────────── Expertises
EXP = [
 ('Identité <em>visuelle</em>', 'Logos, chartes, déclinaisons.', 'Le Bistro des Arènes · Le Régina · Siroo', 'bistro-logo'),
 ('Design <em>graphique</em>', 'Affiches, packagings, visuels d’événements.', 'La Cochonnade · Enzo’s Birthday · Kellogg’s × Barbie', 'enzos-birthday'),
 ('Stratégie <em>digitale</em>', 'SEO, GEO, e-commerce.', 'Pallas Cuir · Sorhobis Boissons', 'sorhobis-ricard'),
 ('Création <em>de contenu</em>', 'Photo produit, lifestyle, réseaux sociaux.', 'La Roumanière · Chérico · Le Bistro des Arènes', 'cherico-lifestyle'),
 ('Commu<em>nication</em>', 'Événementiel, campagnes, street marketing.', 'Low Bass · Notre confort, leur enfer · Don du sang × Marvel', 'low-bass-invitation'),
]
exp = ''.join(f'''
        <li class="rv" data-peek="images/{pk}.jpg"><h3>{rtext(t)}</h3><p>{d}<span>{ex}</span></p></li>''' for t, d, ex, pk in EXP)

# ─────────────────────────────────────────────── Carnet d'images (bandeau défilant)
STRIP = ['roumaniere-2', 'bda-cafe-glace', 'low-bass-invitation', 'regina-tropical', 'bda-photo-3', 'cochonnade-des-voiles', 'cherico-packshot', 'enzos-birthday', 'bda-photo-5', 'siroo-fraise', 'roumaniere-1', 'voiles-aml-music', 'kelloggs-barbie', 'bda-photo-4']
strip_imgs = ''.join(img(n, '', extra=' aria-hidden="true"') for n in STRIP)

TOOLS = os.path.dirname(os.path.abspath(__file__))
MAIL, LINKEDIN = 'laura.tuppo25@gmail.com', 'https://www.linkedin.com/in/profil-de-laura-tuppo'
wl, wt = width_of('LAURA'), width_of('TUPPO')
WM_IN = f'<span class="wm-l">{rsvg("LAURA")}</span><span class="wm-t">{rsvg("TUPPO")}</span>'
HEAD = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='16' fill='%23dfa0be'/%3E%3Ctext x='16' y='21' font-family='Arial' font-weight='700' font-size='13' fill='%23141414' text-anchor='middle'%3ELT%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600&family=Raleway:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">"""
ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-mail" viewBox="0 0 24 24"><path fill="currentColor" d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 7.2L4.4 7H19.6L12 12.2ZM4 8.6V17h16V8.6l-8 5.4-8-5.4Z"/></symbol>
  <symbol id="i-in" viewBox="0 0 24 24"><path fill="currentColor" d="M4.5 9h3v11h-3V9Zm1.5-5a1.75 1.75 0 1 1 0 3.5A1.75 1.75 0 0 1 6 4Zm4 5h2.9v1.5h.04c.4-.76 1.38-1.56 2.85-1.56 3.05 0 3.61 2 3.61 4.6V20h-3v-5.4c0-1.29-.02-2.95-1.8-2.95-1.8 0-2.07 1.4-2.07 2.86V20H10V9Z"/></symbol>
</svg>"""
CONTACT_LIST = f"""<ul class="contact-list">
        <li><span class="ic"><svg aria-hidden="true"><use href="#i-mail"/></svg></span><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><span class="ic"><svg aria-hidden="true"><use href="#i-in"/></svg></span><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn · Laura Tuppo</a></li>
      </ul>"""

def footer(base):
    return f"""<footer class="wrap dark">
  <a href="{base}#accueil" aria-label="Laura Tuppo, accueil"><span class="wm row" aria-hidden="true">{WM_IN}</span></a>
  <nav aria-label="Pied de page"><a href="{base}#a-propos">À propos</a><a href="{base}#projets">Projets</a><a href="{base}#competences">Compétences</a><a href="{base}#contact">Contact</a><a href="cv.html">CV</a></nav>
  <div class="foot-contact"><a href="mailto:{MAIL}">{MAIL}</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a></div>
  <small>© <span id="year">2026</span> Laura Tuppo · Communication &amp; Design graphique</small>
</footer>"""

def render(name, base, extra):
    page = open(os.path.join(TOOLS, name), encoding='utf-8').read()
    for k, v in extra.items():
        page = page.replace('{{' + k + '}}', v)
    page = page.replace('{{FOOTER}}', footer(base)).replace('{{HEAD}}', HEAD).replace('{{ICONS}}', ICONS).replace('{{CONTACT_LIST}}', CONTACT_LIST)
    page = re.sub(r'\[\[r:(.+?)\]\]', lambda m: rtext(m.group(1)), page)
    page = page.replace('{{WM_ROW}}', f'<span class="wm row" aria-hidden="true">{WM_IN}</span>').replace('{{WM_IN}}', WM_IN)
    return page

pages = {}
extra = {'CARDS': cards, 'EXP': exp, 'STRIP': strip_imgs + strip_imgs, 'N_ALL': str(len(P)), 'N_G': str(count['graphisme']),
         'N_C': str(count['communication']), 'N_P': str(count['photo'])}
for key, (name, alt) in {'H1': ('low-bass-invitation', 'Invitation Low Bass'), 'H3': ('cochonnade-des-voiles', 'Affiche La Cochonnade des Voiles'),
                         'H4': ('enzos-birthday', 'Invitation Enzo’s Birthday'), 'CAFE': ('laura-cafe', 'Laura Tuppo en terrasse d’un café parisien')}.items():
    extra[key] = img(name, alt, lazy=(key == 'CAFE'))
pages['index.html'] = render('template.html', '', extra)
pages['cv.html'] = render('cv.html', 'index.html', {})
for out, page in pages.items():          # le sprite est complet une fois toutes les pages rendues
    page = page.replace('{{SPRITE}}', sprite())
    assert '{{' not in page, (out, page[page.index('{{'):page.index('{{') + 40])
    open(out, 'w', encoding='utf-8').write(page)
    print(out, len(page))

os.makedirs('assets', exist_ok=True)
css = open(os.path.join(TOOLS, 'site.css'), encoding='utf-8').read()
css = css.replace('{{K_L}}', f'{BOX / wl:.4f}').replace('{{K_T}}', f'{.63 * wl / wt:.4f}')
assert '{{' not in css
open('assets/site.css', 'w', encoding='utf-8').write(css)
open('assets/site.js', 'w', encoding='utf-8').write(open(os.path.join(TOOLS, 'site.js'), encoding='utf-8').read())
print('assets ok')
