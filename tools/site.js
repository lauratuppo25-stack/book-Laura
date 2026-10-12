/* Laura Tuppo — portfolio : interactions communes aux pages. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const lock = on => { document.body.style.overflow = on ? 'hidden' : ''; };

  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();

  // Écran de chargement : compteur réel (images de l'accueil + polices), puis ouverture
  const loader = $('.loader');
  const reveal = () => { root.classList.remove('is-loading'); root.classList.add('loaded'); };
  if (loader && !reduce) {
    const bar = $('.loader-bar', loader), count = $('.loader-count', loader);
    const imgs = $$('img').filter(i => i.loading !== 'lazy');
    const t0 = performance.now(), MIN = 1500;
    let shown = 0, done = false;
    const ready = () => imgs.filter(i => i.complete).length / Math.max(imgs.length, 1);
    let fontsOk = false;
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => { fontsOk = true; });
    const tick = now => {
      const time = Math.min((now - t0) / MIN, 1);
      const real = (ready() + (fontsOk ? 1 : 0)) / 2;
      const target = Math.min(time, real < 1 ? Math.min(real, .92) : 1) ;
      shown += (Math.max(target, shown) - shown) * .12;
      if (target >= 1 && shown > .995) shown = 1;
      bar.style.setProperty('--l', shown.toFixed(3));
      count.textContent = String(Math.round(shown * 100)).padStart(3, '0') + ' %';
      if (shown >= 1 && !done) { done = true; setTimeout(reveal, 250); return; }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    setTimeout(() => { if (!done) { done = true; reveal(); } }, 7000);
  } else reveal();

  // En-tête : fond au défilement, se cache en descendant ; barre de progression
  const top = $('#topbar'), prog = $('#progress');
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    if (top && !top.classList.contains('solid')) top.classList.toggle('scrolled', y > innerHeight * .5);
    if (top) top.classList.toggle('hide', y > lastY && y > innerHeight && !root.classList.contains('menu-open'));
    lastY = y;
    if (prog) {
      const h = document.documentElement.scrollHeight - innerHeight;
      prog.style.setProperty('--p', h > 0 ? (y / h).toFixed(4) : 0);
    }
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Photo : s'ouvre en entrant à l'écran, reste nette, puis se floute pour l'À propos
  const scene = $('#scene');
  if (scene) {
    let ticking = false;
    const clamp = v => Math.min(Math.max(v, 0), 1);
    const update = () => {
      ticking = false;
      const top = scene.getBoundingClientRect().top, h = innerHeight;
      scene.style.setProperty('--e', clamp(1 - top / h).toFixed(3));
      scene.style.setProperty('--p', clamp((-top - h * .45) / (h * .55)).toFixed(3));
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    addEventListener('resize', update);
    update();
  }

  // Apparitions au défilement (titres lettre par lettre, cartes, photos)
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: .08, rootMargin: '0px 0px -40px 0px' });
  $$('.rv').forEach(el => io.observe(el));

  // Menu plein écran
  const menu = $('#menu'), menuBtn = $('#menuBtn'), menuLbl = $('#menuLbl');
  const menuLinks = menu ? $$('ol a', menu) : [];
  const sections = menuLinks.map(a => { const h = a.getAttribute('href'); return h.startsWith('#') ? document.querySelector(h) : null; });
  const markCurrent = () => {
    const mid = innerHeight / 2;
    let i = sections.findIndex(s => s && s.getBoundingClientRect().bottom > mid);
    menuLinks.forEach((a, j) => a.classList.toggle('current', a.dataset.page === 'here' || (i >= 0 && j === i)));
  };
  const setMenu = open => {
    root.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', open);
    menu.setAttribute('aria-hidden', !open);
    menu.inert = !open;
    menuLbl.textContent = open ? 'Fermer' : 'Menu';
    lock(open);
    if (open) { markCurrent(); setTimeout(() => menuLinks[0].focus({ preventScroll: true }), 300); }
  };
  if (menu) {
    menu.inert = true;
    menuBtn.addEventListener('click', () => setMenu(!root.classList.contains('menu-open')));
    $$('a', menu).forEach(a => a.addEventListener('click', () => setMenu(false)));
  }

  // Filtres de projets, avec fondu entre deux sélections
  const grid = $('#grid'), tiles = $('#tiles'), filterBtns = $$('.filters button');
  filterBtns.forEach(b => b.addEventListener('click', () => {
    if (b.getAttribute('aria-pressed') === 'true') return;
    const f = b.dataset.filter, zones = [grid, tiles].filter(Boolean);
    filterBtns.forEach(x => x.setAttribute('aria-pressed', x === b));
    const apply = () => {
      $$('.card').forEach(c => {
        c.hidden = f !== 'all' && c.dataset.cat !== f;
        c.classList.remove('in');
        if (!c.hidden) io.observe(c);
      });
      zones.forEach(z => { z.hidden = !$$('.card', z).some(c => !c.hidden); z.classList.remove('fading'); });
      if (grid) grid.dispatchEvent(new Event('relayout'));
    };
    if (reduce) { apply(); return; }
    zones.forEach(z => z.classList.add('fading'));
    setTimeout(apply, 260);
  }));

  // Fiche projet plein écran
  const panel = $('#panel');
  if (panel) {
    const cards = $$('.card');
    let current = null, opener = null;
    const visible = () => cards.filter(c => !c.hidden);
    const show = (card, swap) => {
      current = card;
      const list = visible(), det = $('.card-detail', card);
      $('#pLabel').textContent = $('.card-meta .label', card).textContent;
      const title = $('#pTitle');
      title.innerHTML = $('.d-title', det).innerHTML;
      title.classList.remove('go'); void title.offsetWidth; title.classList.add('go');
      $('#pType').textContent = $('.card-type', card).textContent;
      const text = $('#pText'); text.innerHTML = '';
      text.append($('.d-text', det).cloneNode(true), $('.d-specs', det).cloneNode(true));
      const imgs = $('#pImgs'); imgs.innerHTML = '';
      const figs = $$('.d-imgs figure', det);
      (figs.length ? figs : [$('.card-img', card)]).forEach((f, k) => {
        const c = f.cloneNode(true);
        $$('img', c).forEach(i => { i.loading = 'eager'; });
        $$('.card-cta', c).forEach(el => el.remove());
        c.style.setProperty('--k', k);
        imgs.append(c);
      });
      $('#pCount').textContent = String(list.indexOf(card) + 1).padStart(2, '0') + ' / ' + String(list.length).padStart(2, '0');
      panel.scrollTop = 0;
      if (swap) { const info = $('.panel-info', panel); info.classList.remove('panel-swap'); void info.offsetWidth; info.classList.add('panel-swap'); }
    };
    const open = card => {
      opener = $('.card-open', card);
      show(card);
      panel.classList.add('open');
      panel.setAttribute('aria-hidden', 'false');
      panel.inert = false;
      lock(true);
      $('#pClose').focus({ preventScroll: true });
    };
    const close = () => {
      panel.classList.remove('open');
      panel.setAttribute('aria-hidden', 'true');
      panel.inert = true;
      lock(false);
      if (opener) opener.focus({ preventScroll: true });
    };
    const step = d => { const l = visible(); show(l[(l.indexOf(current) + d + l.length) % l.length], true); };
    panel.inert = true;
    cards.forEach(c => $('.card-open', c).addEventListener('click', () => open(c)));
    $('#pClose').addEventListener('click', close);
    $('#pPrev').addEventListener('click', () => step(-1));
    $('#pNext').addEventListener('click', () => step(1));
    addEventListener('keydown', e => {
      if (!panel.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    });
  }

  // Grille : projets répartis ligne par ligne (l'ordre se lit de gauche à droite)
  const masonry = $('#grid');
  if (masonry) {
    const items = $$('.card', masonry);
    let cols = 0;
    const layoutGrid = force => {
      const n = innerWidth > 980 ? 3 : innerWidth > 640 ? 2 : 1;
      if (n === cols && !force) return;
      cols = n;
      masonry.classList.add('cols');
      $$('.grid-col', masonry).forEach(c => c.remove());
      const columns = Array.from({ length: n }, () => { const c = document.createElement('div'); c.className = 'grid-col'; masonry.append(c); return c; });
      let k = 0;
      items.forEach(it => { columns[it.hidden ? n - 1 : k++ % n].append(it); });
    };
    layoutGrid();
    addEventListener('resize', () => layoutGrid());
    masonry.addEventListener('relayout', () => layoutGrid(true));
  }

  // CV : agrandir la page du CV
  const sheet = $('#sheet'), zoom = $('#zoom');
  if (sheet && zoom) {
    const openZ = () => { zoom.classList.add('open'); zoom.setAttribute('aria-hidden', 'false'); lock(true); $('button', zoom).focus(); };
    const closeZ = () => { zoom.classList.remove('open'); zoom.setAttribute('aria-hidden', 'true'); lock(false); sheet.focus(); };
    sheet.addEventListener('click', openZ);
    sheet.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openZ(); } });
    zoom.addEventListener('click', closeZ);
    addEventListener('keydown', e => { if (e.key === 'Escape' && zoom.classList.contains('open')) closeZ(); });
  }

  addEventListener('keydown', e => {
    if (e.key === 'Escape' && root.classList.contains('menu-open')) { setMenu(false); menuBtn.focus(); }
  });

  // Copier l'adresse e-mail
  const copy = $('#copyMail');
  if (copy) copy.addEventListener('click', () => {
    const mail = copy.dataset.mail, out = $('#copied');
    const done = () => { out.textContent = 'Adresse copiée : ' + mail; };
    if (navigator.clipboard) navigator.clipboard.writeText(mail).then(done, () => { out.textContent = mail; });
    else out.textContent = mail;
  });

  if (!fine || reduce) return;

  // Curseur rose : devient « Voir » sur les projets
  const cur = $('#cursor');
  let mx = innerWidth / 2, my = innerHeight / 2, cx = mx, cy = my;
  addEventListener('pointermove', e => { mx = e.clientX; my = e.clientY; });
  if (cur) {
    root.classList.add('has-cursor');
    const label = $('span', cur);
    const hover = el => {
      const t = el && el.closest('[data-cursor]');
      cur.classList.toggle('big', !!t);
      if (t) label.textContent = t.dataset.cursor;
    };
    addEventListener('pointerover', e => hover(e.target));
    addEventListener('scroll', () => hover(document.elementFromPoint(mx, my)), { passive: true });
    document.addEventListener('pointerleave', () => { cur.style.opacity = 0; });
    document.addEventListener('pointerenter', () => { cur.style.opacity = 1; });
  }


  // Expertises : un visuel suit la souris
  const peek = $('#peek'), pimg = peek && $('img', peek);
  let px = 0, py = 0, active = null;
  if (peek) {
    $$('.exp-list li').forEach(li => {
      li.addEventListener('pointerenter', () => { active = li; pimg.src = li.dataset.peek; if (!peek.classList.contains('on')) { px = mx + 40; py = my - 120; } peek.classList.add('on'); });
      li.addEventListener('pointerleave', () => { active = null; peek.classList.remove('on'); });
    });
    addEventListener('scroll', () => { if (active && !active.matches(':hover')) { active = null; peek.classList.remove('on'); } }, { passive: true });
  }

  const loop = () => {
    cx += (mx - cx) * .2; cy += (my - cy) * .2;
    if (cur) cur.style.transform = `translate3d(${cx}px,${cy}px,0)`;
    if (peek) {
      const w = peek.offsetWidth, h = peek.offsetHeight;
      const tx = mx > innerWidth * .6 ? mx - w - 40 : mx + 40;
      const ty = Math.min(Math.max(my - h / 2, 80), innerHeight - h - 20);
      px += (tx - px) * .15; py += (ty - py) * .15;
      peek.style.transform = `translate3d(${px}px,${py}px,0) rotate(-3deg) scale(${peek.classList.contains('on') ? 1 : .8})`;
    }
    requestAnimationFrame(loop);
  };
  loop();
})();
