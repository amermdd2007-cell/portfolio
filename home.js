// Home 2.0 motion: the particle field, the cursor-led 3D screens, the pinned work track with its colour,
// count-ups, the drawn process line, rising sections and the magnetic contact button.
// Reduced motion: none of it runs; the page stands as written.
const root = document.documentElement;
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
const rtl = () => root.dir === 'rtl';
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

// ---- nav: a glass bar once the page has moved
const nav = document.querySelector('.nav');
const onNav = () => nav.classList.toggle('is-solid', scrollY > 40);
addEventListener('scroll', onNav, { passive: true }); onNav();

if (!still) {
  root.classList.add('js-motion');

  // ---- hero entrance: the name rises line by line, then the rest
  const lines = document.querySelectorAll('.hero h1 .ln > span');
  lines.forEach((s, i) => s.animate([{ transform: 'translateY(105%)' }, { transform: 'none' }], { duration: 1100, delay: 120 + i * 110, easing: 'cubic-bezier(.23,1,.32,1)', fill: 'backwards' }));
  document.querySelectorAll('.hero [data-in]').forEach((el, i) => el.animate([{ opacity: 0, transform: 'translateY(18px)' }, { opacity: 1, transform: 'none' }], { duration: 900, delay: 420 + i * 90, easing: 'cubic-bezier(.23,1,.32,1)', fill: 'backwards' }));
  document.querySelectorAll('.scr').forEach((el, i) => el.animate([{ opacity: 0, transform: 'translateZ(-600px) rotate(var(--r)) translateY(80px)' }, { opacity: 1 }], { duration: 1400, delay: 260 + i * 140, easing: 'cubic-bezier(.23,1,.32,1)', fill: 'backwards' }));

  // ---- the particle field: amber dots that drift and part around the cursor
  const cv = document.querySelector('.hero__field');
  if (cv) {
    const ctx = cv.getContext('2d');
    let W = 0, H = 0, dpr = 1, pts = [], mouse = { x: -9999, y: -9999 }, run = true, raf = 0;
    const build = () => {
      dpr = Math.min(2, devicePixelRatio || 1); W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const gap = W < 700 ? 30 : 34; pts = [];
      for (let y = gap / 2; y < H; y += gap) for (let x = gap / 2; x < W; x += gap) pts.push({ x, y, ox: x, oy: y, ph: Math.random() * 6.28 });
    };
    const cx = () => rtl() ? W * 0.28 : W * 0.72;
    const draw = (t) => {
      ctx.clearRect(0, 0, W, H);
      const c = cx(), cy = H * 0.42, R = Math.max(W, H) * 0.62;
      for (const p of pts) {
        const dx = p.ox - mouse.x, dy = p.oy - mouse.y, d = Math.hypot(dx, dy);
        const push = d < 140 ? (140 - d) / 140 : 0;
        const tx = p.ox + (d ? dx / d : 0) * push * 26 + Math.sin(t / 1600 + p.ph) * 2;
        const ty = p.oy + (d ? dy / d : 0) * push * 26 + Math.cos(t / 1900 + p.ph) * 2;
        p.x += (tx - p.x) * 0.12; p.y += (ty - p.y) * 0.12;
        const fall = 1 - Math.min(1, Math.hypot(p.ox - c, p.oy - cy) / R);
        const a = 0.05 + fall * 0.5 + push * 0.5;
        if (a < 0.06) continue;
        ctx.fillStyle = push > 0.05 ? `rgba(255,190,90,${a})` : `rgba(242,169,59,${a})`;
        ctx.beginPath(); ctx.arc(p.x, p.y, 1.2 + push * 1.6, 0, 6.283); ctx.fill();
      }
      if (run && !root.classList.contains('motion-off')) raf = requestAnimationFrame(draw);
    };
    build(); raf = requestAnimationFrame(draw);
    addEventListener('resize', build);
    const hero = document.querySelector('.hero');
    hero.addEventListener('pointermove', (e) => { const r = cv.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
    hero.addEventListener('pointerleave', () => { mouse = { x: -9999, y: -9999 }; });
    // stop drawing while the hero is off screen or the tab is hidden
    new IntersectionObserver(([e]) => { run = e.isIntersecting; if (run) { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); } }).observe(hero);
    window.__resumeField = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); };
  }

  // ---- the cursor leans the screens and the about tiles (-1..1)
  if (fine) {
    let qx = 0, qy = 0, q = false;
    addEventListener('pointermove', (e) => {
      qx = clamp((e.clientX / innerWidth) * 2 - 1, -1, 1); qy = clamp((e.clientY / innerHeight) * 2 - 1, -1, 1);
      if (!q) { q = true; requestAnimationFrame(() => { q = false; root.style.setProperty('--mx', qx.toFixed(3)); root.style.setProperty('--my', qy.toFixed(3)); }); }
    }, { passive: true });
  }

  // ---- work: pinned, the track slides with the scroll, the glow takes each card's colour
  const work = document.querySelector('.work');
  const track = work?.querySelector('.track');
  const cards = track ? [...track.children] : [];
  const dots = [...document.querySelectorAll('.dots i')];
  const wide = matchMedia('(min-width: 900px)');
  const setColour = (i) => { const c = cards[i]; if (!c) return; work.style.setProperty('--pc', getComputedStyle(c).getPropertyValue('--c')); dots.forEach((d, k) => d.classList.toggle('is-on', k === i)); };
  let live = false;
  const layoutWork = () => {
    live = wide.matches && cards.length > 1;
    work.classList.toggle('is-live', live);
    work.style.setProperty('--cards', cards.length);
    if (!live) track.style.transform = '';
    workFrame();
  };
  const workFrame = () => {
    if (!work) return;
    if (!live) {
      // stacked cards: the colour follows the card nearest the middle of the screen
      let best = 0, bd = 1e9; cards.forEach((c, i) => { const r = c.getBoundingClientRect(); const d = Math.abs(r.top + r.height / 2 - innerHeight / 2); if (d < bd) { bd = d; best = i; } });
      setColour(best); return;
    }
    const r = work.getBoundingClientRect(), span = work.offsetHeight - innerHeight;
    const p = clamp(-r.top / Math.max(1, span), 0, 1);
    const max = track.scrollWidth - track.parentElement.clientWidth;
    track.style.transform = `translate3d(${(rtl() ? 1 : -1) * p * max}px,0,0)`;
    setColour(Math.round(p * (cards.length - 1)));
  };
  if (work && track) {
    cards.forEach((c, i) => c.addEventListener('focus', () => {
      if (!live) return;
      const span = work.offsetHeight - innerHeight, top = work.getBoundingClientRect().top + scrollY;
      scrollTo({ top: top + span * (i / Math.max(1, cards.length - 1)), behavior: 'instant' });
    }));
    let q = false;
    addEventListener('scroll', () => { if (!q) { q = true; requestAnimationFrame(() => { q = false; workFrame(); }); } }, { passive: true });
    addEventListener('resize', layoutWork); wide.addEventListener('change', layoutWork);
    new MutationObserver(layoutWork).observe(root, { attributes: true, attributeFilter: ['dir'] });
    layoutWork();
  }

  // ---- rise in once, count up, draw the line
  const counters = [...document.querySelectorAll('[data-count]')];
  const count = (el) => {
    const to = +el.dataset.count, fmt = new Intl.NumberFormat('en-US'), t0 = performance.now(), dur = 1600;
    el.style.display = 'inline-block'; el.style.width = (el.getBoundingClientRect().width + 2) + 'px'; el.style.textAlign = 'end';
    const tick = (t) => { const k = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - k, 4); el.textContent = fmt.format(Math.round(to * e)); if (k < 1) requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
  };
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    const el = e.target; io.unobserve(el);
    el.classList.add('is-in');
    if (el.matches('[data-count]')) count(el);
  }), { rootMargin: '0px 0px -12% 0px' });
  document.querySelectorAll('[data-rise], [data-count]').forEach((el) => io.observe(el));

  const line = document.querySelector('.proc__line');
  if (line) {
    const drawLine = () => { const r = line.getBoundingClientRect(); line.style.setProperty('--draw', clamp((innerHeight * 0.9 - r.top) / (innerHeight * 0.6), 0, 1).toFixed(3)); };
    line.style.setProperty('--draw', 0);
    addEventListener('scroll', () => requestAnimationFrame(drawLine), { passive: true }); drawLine();
  }

  // ---- the contact button leans toward the cursor
  const mag = document.querySelector('.magnet');
  if (mag && fine) {
    const zone = mag.closest('.contact');
    zone.addEventListener('pointermove', (e) => {
      const r = mag.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2), d = Math.hypot(dx, dy);
      const k = d < 320 ? (1 - d / 320) * 0.45 : 0;
      mag.style.setProperty('--tx', (dx * k).toFixed(1) + 'px'); mag.style.setProperty('--ty', (dy * k).toFixed(1) + 'px');
    });
    zone.addEventListener('pointerleave', () => { mag.style.setProperty('--tx', '0px'); mag.style.setProperty('--ty', '0px'); });
  }
}

// ---- one button pauses every moving thing (particles, glows, floating screens, the strip) and plays it again
const toggle = document.querySelector('[data-motion-toggle]');
if (toggle) {
  if (still) toggle.hidden = true;
  toggle.addEventListener('click', () => {
    const off = root.classList.toggle('motion-off');
    toggle.setAttribute('aria-pressed', String(off));
    const label = toggle.querySelector('span[data-ar]');
    const ar = root.lang === 'ar';
    label.dataset.enHtml = off ? 'Play motion' : 'Pause motion';
    label.dataset.ar = off ? 'شغّل الحركة' : 'أوقف الحركة';
    label.textContent = ar ? label.dataset.ar : label.dataset.enHtml;
    if (!off && window.__resumeField) window.__resumeField();
  });
}
