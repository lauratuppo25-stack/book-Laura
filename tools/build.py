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

# ─────────────────────────────────────────────── Projets
# cat: graphisme | communication | photo
P = [
 dict(id='bistro', cat='graphisme', cadre='Client', type='Identité visuelle', title='Le Bistro <em>des Arènes</em>',
      desc=['Logotype d’un restaurant bistronomique provençal. Une arche inspirée des Arènes de Nîmes et une typographie Art déco, posée en lettrage blanc sur la vitrine.'],
      specs=[('Livrables', 'Logo, charte, mockup'), ('Outils', 'Illustrator, Photoshop')],
      cover='bistro-logo', imgs=[('bistro-logo', 'Logo Le Bistro des Arènes en lettrage blanc sur une vitrine')]),
 dict(id='regina', cat='graphisme', cadre='Client', type='Identité & réseaux sociaux', title='Le <em>Régina</em>',
      desc=['Identité du Régina, bar-café à Châteaurenard : un serif terracotta et un script doré.', 'L’univers se décline en stories pour les soirées de l’été 2025, du programme de la Saint-Éloi à la Tropical Flower Night.'],
      specs=[('Livrables', 'Logo, stories, programme'), ('Date', 'Juillet 2025')],
      cover='regina-tropical', imgs=[('regina-logo', 'Logotype Le Régina bar-café'), ('regina-programme', 'Story Instagram, programme de la Saint-Éloi 2025'), ('regina-tropical', 'Story Instagram, Tropical Flower Night')]),
 dict(id='cochonnade', cat='graphisme', cadre='Client', type='Affiche événementielle', title='La Cochonnade <em>des Voiles</em>',
      desc=['Affiche du BBQ du 14 juillet aux Voiles, à Beaucaire, avec AML Music. Le titre est gravé dans la viande, piquée sur une fourchette à découper, en monochrome bleu électrique.'],
      specs=[('Lieu', 'Les Voiles, Beaucaire'), ('Outils', 'Photoshop, Illustrator')],
      cover='cochonnade-des-voiles', imgs=[('cochonnade-des-voiles', 'Affiche La Cochonnade des Voiles')]),
 dict(id='siroo', cat='graphisme', cadre='École', type='Branding & packaging', title='Siroo, <em>le goût en boucle</em>',
      desc=['Marque fictive de sirops naturels et rechargeables. Un logo décliné par saveur, des étiquettes ovales et une bouteille d’apothicaire.'],
      specs=[('Livrables', 'Logo, étiquettes, mockup'), ('Outils', 'Illustrator, Photoshop')],
      cover='siroo-bouteille', imgs=[('siroo-fraise', 'Étiquette Siroo goût fraise'), ('siroo-peche', 'Étiquette Siroo goût pêche'), ('siroo-bouteille', 'Bouteille Siroo framboise')]),
 dict(id='enzo', cat='graphisme', cadre='Client', type='Invitation', title='Enzo’s <em>Birthday</em>',
      desc=['Invitation pour les 35 ans du « Citron » à L’Antre des Citrons : typographie liquide, collage de citrons tramés et dégradé solaire. Dress code : venez comme vous zestes.'],
      specs=[('Lieu', 'L’Antre des Citrons'), ('Format', 'Invitation, réseaux sociaux')],
      cover='enzos-birthday', imgs=[('enzos-birthday', 'Invitation Enzo’s Birthday')]),
 dict(id='kelloggs', cat='graphisme', cadre='École', type='Packaging', title='Kellogg’s <em>× Barbie</em>',
      desc=['Refonte fictive d’une boîte de céréales en édition limitée : univers rose, typographie script, goût framboise.'],
      specs=[('Livrable', 'Boîte et mise en situation'), ('Outils', 'Illustrator, Photoshop')],
      cover='kelloggs-barbie', imgs=[('kelloggs-barbie', 'Boîte de céréales Kellogg’s × Barbie sur une table')]),
 dict(id='aml', cat='graphisme', cadre='Client', type='Affiche événementielle', title='AML Music <em>aux Voiles</em>',
      desc=['Soirée DJ du 22 juillet, de 17 h à 2 h : un portrait en monochrome bleu fondu dans la façade du bar, dans la continuité de la Cochonnade.'],
      specs=[('Lieu', 'Les Voiles, Beaucaire'), ('Outils', 'Photoshop')],
      cover='voiles-aml-music', imgs=[('voiles-aml-music', 'Affiche AML Music aux Voiles')]),
 dict(id='comptoir', cat='graphisme', cadre='Client', type='Affiche événementielle', title='Un chef <em>en cave</em>',
      desc=['Soirée accords mets et vins dans les chais du Comptoir des Vignes, à Châteaurenard : formes organiques, script manuscrit et palette chaude.'],
      specs=[('Client', 'Comptoir des Vignes'), ('Outils', 'Illustrator, Photoshop')],
      cover='comptoir-chef-en-cave', imgs=[('comptoir-chef-en-cave', 'Affiche Un chef en cave, Comptoir des Vignes')]),
 dict(id='futurs', cat='graphisme', cadre='École', type='Affiche de film', title='Futur<em>(s)</em>',
      desc=['Affiche d’un film fictif. Direction artistique cinématographique, entre synthwave et cyberpunk, entièrement composée sous Photoshop.'],
      specs=[('Projet', 'Film fictif'), ('Outil', 'Photoshop')],
      cover='futurs-affiche', imgs=[('futurs-affiche', 'Affiche du film fictif Futur(s)')]),
 dict(id='lowbass', cat='communication', cadre='Client', type='Communication événementielle', title='Low <em>Bass</em>',
      desc=['Communication de l’événement Low Bass au Château Romanin, à Saint-Rémy-de-Provence : dimanche 22 novembre, de 14 h à 21 h, food & drink.', 'Une story teaser « Stay tuned » pour créer l’attente, puis l’invitation exclusive. Dégradé rouge et noir granuleux, titres flous en mouvement et logo circulaire.'],
      specs=[('Lieu', 'Château Romanin, Saint-Rémy-de-Provence'), ('Date', 'Dimanche 22 novembre'), ('Formats', 'Story teaser, invitation')],
      cover='low-bass-invitation', imgs=[('low-bass-invitation', 'Invitation exclusive Low Bass au Château Romanin, dimanche 22 novembre'), ('low-bass-stay-tuned', 'Story teaser Low Bass, Stay tuned')]),
 dict(id='confort', cat='communication', cadre='École', type='Campagne de sensibilisation', title='Notre confort, <em>leur enfer.</em>',
      desc=['Campagne fictive contre la pollution pétrolière et ses effets sur la faune marine : un manchot couvert de pétrole et une accroche directe, déclinée en abribus.'],
      specs=[('Livrables', 'Affiche, abribus'), ('Outils', 'Photoshop, Illustrator')],
      cover='confort-enfer-affiche', imgs=[('confort-enfer-affiche', 'Affiche Notre confort, leur enfer'), ('confort-enfer-abribus', 'L’affiche sur un abribus')]),
 dict(id='dondusang', cat='communication', cadre='École', type='Street marketing', title='Don du sang <em>× Marvel</em>',
      desc=['Collaboration imaginaire pour le don du sang : Captain America en héros du quotidien. « Le vrai héros, c’est celui qui donne. »'],
      specs=[('Support', 'Abribus'), ('Outils', 'Photoshop, Illustrator')],
      cover='don-du-sang-affiche', imgs=[('don-du-sang-affiche', 'Affiche Don du sang avec Captain America'), ('don-du-sang-abribus', 'L’affiche Don du sang sur un abribus')]),
 dict(id='cic', cat='communication', cadre='École', type='Campagne & carte bancaire', title='CIC, <em>le plan Q*</em>',
      desc=['Campagne pour les 18–25 ans qui joue sur le double sens du « Plan Q » (*plan quotidien), déclinée en abribus et en carte étudiante Q+ en trois versions.'],
      specs=[('Cible', 'Étudiants 18–25 ans'), ('Livrables', 'Abribus, cartes Q+')],
      cover='cic-cartes', imgs=[('cic-abribus', 'Abribus CIC, le meilleur Plan Q de ta vie'), ('cic-cartes', 'Trois cartes bancaires CIC Q+')]),
 dict(id='gestiboat', cat='communication', cadre='École', type='Identité & affichage', title='GestiBoat, <em>speed boating day</em>',
      desc=['Supports de communication pour une startup de gestion nautique : la journée spéciale propriétaires au port de La Grande-Motte, en affiche et en affichage urbain.'],
      specs=[('Livrables', 'Affiche, affichage urbain'), ('Outils', 'Illustrator, Canva')],
      cover='gestiboat-affiche', imgs=[('gestiboat-affiche', 'Affiche GestiBoat Speed Boating Day'), ('gestiboat-mockup', 'Affichage urbain GestiBoat')]),
 dict(id='sorhobis', cat='communication', cadre='Client', type='Bannières web', title='Sorhobis <em>Boissons</em>',
      desc=['Cinq bannières promotionnelles pour l’intranet du distributeur, dans le respect des chartes de chaque marque : Pastis Olive, Ricard, Get 27, Citadelle et Lillet.'],
      specs=[('Livrables', '5 bannières web'), ('Outils', 'Photoshop, Illustrator')],
      cover='stack', imgs=[('sorhobis-pastis-olive', 'Bannière Pastis Olive'), ('sorhobis-ricard', 'Bannière Ricard'), ('sorhobis-get27', 'Bannière Get 27'), ('sorhobis-citadelle', 'Bannière Citadelle'), ('sorhobis-lillet', 'Bannière Lillet')]),
 dict(id='pallas', cat='communication', cadre='Client', type='SEO / GEO & social media', title='Pallas <em>Cuir</em>',
      desc=['Audit SEO et GEO du site e-commerce multimarque sous PrestaShop, et optimisation des fiches produit pour gagner en visibilité en Provence.', 'En parallèle, création de contenus pour les réseaux sociaux.'],
      specs=[('Plateforme', 'PrestaShop'), ('Missions', 'Audit SEO, GEO, contenus')],
      cover=None, imgs=[]),
 dict(id='bda', cat='photo', cadre='Client', type='Photo food & lifestyle', title='Le Bistro des Arènes, <em>en images</em>',
      desc=['Shooting pour le restaurant : cocktails, assiettes et terrasse. Direction artistique, prise de vue et retouche.'],
      specs=[('Sujets', 'Cocktails, plats, terrasse'), ('Outils', 'Lightroom, Photoshop')],
      cover='bda-photo-3', imgs=[('bda-photo-1', 'Bière tenue en terrasse'), ('bda-photo-2', 'Portrait en casquette, lumière naturelle'), ('bda-photo-3', 'Cocktail spritz'), ('bda-photo-4', 'Mule dans une tasse en cuivre'), ('bda-photo-5', 'Assiettes dressées')]),
 dict(id='roumaniere', cat='photo', cadre='Client', type='Photo produit', title='La <em>Roumanière</em>',
      desc=['Confiture de pêche de Provence : fond rouge, lumière naturelle et mise en scène végétale. Direction artistique et retouche.'],
      specs=[('Produit', 'Confiture pêche de Provence'), ('Outils', 'Lightroom, Photoshop')],
      cover='roumaniere-1', imgs=[('roumaniere-1', 'Pot de confiture sur des feuilles, fond rouge'), ('roumaniere-2', 'Pot de confiture tenu en main'), ('roumaniere-3', 'Pot de confiture couché sur fond rouge')]),
 dict(id='cherico', cat='photo', cadre='Client', type='Packshot & lifestyle', title='Chérico, <em>chicorée bio</em>',
      desc=['Packshot pour la fiche produit e-commerce et image lifestyle en lumière naturelle pour les réseaux sociaux.'],
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
        cover = '<figure class="card-img card-text"><span class="ct-big">SEO <em>&amp; GEO</em></span><span class="ct-small">E-commerce · PrestaShop · réseaux sociaux</span><span class="card-cta">Voir le projet</span></figure>'
    desc = ''.join(f'<p>{d}</p>' for d in p['desc'])
    specs = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [('Discipline', CAT[p['cat']]), ('Cadre', p['cadre'])] + p['specs'])
    imgs = ''.join(f'<figure>{img(n, a)}</figure>' for n, a in p['imgs'])
    return f'''
      <article class="card rv" id="p-{p['id']}" data-cat="{p['cat']}">
        <button class="card-open" aria-label="Voir le projet {html.escape(plain)}">
          {cover}
          <span class="card-meta"><span class="label">{num} — {CAT[p['cat']]}</span><span class="card-title">{p['title']}</span><span class="card-type">{p['type']} · {p['cadre']}</span></span>
        </button>
        <div class="card-detail" hidden>
          <div class="d-text">{desc}</div>
          <dl class="d-specs">{specs}</dl>
          <div class="d-imgs">{imgs}</div>
        </div>
      </article>'''

cards = ''.join(card(i, p) for i, p in enumerate(P))

# ─────────────────────────────────────────────── Expertises
EXP = [
 ('Identité <em>visuelle</em>', 'Logos, chartes et déclinaisons qui donnent une voix visuelle à une marque.', 'Le Bistro des Arènes · Le Régina · Siroo', 'bistro-logo'),
 ('Design <em>graphique</em>', 'Affiches, packagings et visuels d’événements, du print aux stories.', 'La Cochonnade · Enzo’s Birthday · Kellogg’s × Barbie', 'enzos-birthday'),
 ('Stratégie <em>digitale</em>', 'Audit SEO et GEO, e-commerce et visibilité en ligne.', 'Pallas Cuir · Sorhobis Boissons', 'sorhobis-ricard'),
 ('Création <em>de contenu</em>', 'Photographie produit, lifestyle et contenus pour les réseaux sociaux.', 'La Roumanière · Chérico · Le Bistro des Arènes', 'cherico-lifestyle'),
 ('Commu<em>nication</em>', 'Communication événementielle, campagnes de sensibilisation et street marketing.', 'Low Bass · Notre confort, leur enfer · Don du sang × Marvel', 'low-bass-invitation'),
]
exp = ''.join(f'''
        <li class="rv" data-peek="images/{pk}.jpg"><h3>{t}</h3><p>{d}<span>{ex}</span></p></li>''' for t, d, ex, pk in EXP)

# ─────────────────────────────────────────────── Carnet d'images (bandeau défilant)
STRIP = ['roumaniere-2', 'low-bass-invitation', 'regina-tropical', 'bda-photo-3', 'cochonnade-des-voiles', 'cherico-packshot', 'enzos-birthday', 'bda-photo-5', 'siroo-fraise', 'roumaniere-1', 'voiles-aml-music', 'kelloggs-barbie', 'bda-photo-4']
strip_imgs = ''.join(img(n, '', extra=' aria-hidden="true"') for n in STRIP)

page = open(os.path.join(os.path.dirname(__file__), 'template.html'), encoding='utf-8').read()
page = (page.replace('{{CARDS}}', cards).replace('{{EXP}}', exp).replace('{{STRIP}}', strip_imgs + strip_imgs)
        .replace('{{N_ALL}}', str(len(P))).replace('{{N_G}}', str(count['graphisme']))
        .replace('{{N_C}}', str(count['communication'])).replace('{{N_P}}', str(count['photo'])))
for key, (name, alt) in {'H1': ('low-bass-invitation', 'Invitation Low Bass'), 'H2': ('kelloggs-barbie', 'Packaging Kellogg’s × Barbie'),
                         'H3': ('cochonnade-des-voiles', 'Affiche La Cochonnade des Voiles'), 'H4': ('enzos-birthday', 'Invitation Enzo’s Birthday'),
                         'PORTRAIT': ('laura-portrait', 'Portrait de Laura Tuppo')}.items():
    page = page.replace('{{' + key + '}}', img(name, alt, lazy=(key == 'PORTRAIT')))
assert '{{' not in page, page[page.index('{{'):page.index('{{') + 40]
open('index.html', 'w', encoding='utf-8').write(page)
print('ok', len(page))
