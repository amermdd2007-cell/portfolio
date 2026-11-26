// The project story (story3d.css): the screens on a ring turn with the scroll, the editor beside them
// types each step's title. The page scrolls natively; the section pins with position: sticky and this
// script only reads its progress once a frame. Reduced motion and no script keep the plain list.
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const TYPE_MS = 16;

for (const sec of document.querySelectorAll('[data-story]')) {
  if (still) continue;
  const ring = sec.querySelector('.s3__ring');
  const cards = [...ring.querySelectorAll('.s3__card')];
  const steps = [...sec.querySelectorAll('.s3__step')];
  const stack = [...sec.querySelectorAll('.s3__stack li')];
  const count = sec.querySelector('.s3__count b');
  const cmd = sec.querySelector('.s3__cmd [data-type]');
  const n = cards.length;
  const step = 360 / Math.max(n, 7);                       // degrees between two screens
  sec.style.setProperty('--n', n);
  sec.classList.add('is-live');

  // the ring's radius from the card width, so neighbours never touch
  const layout = () => {
    const w = cards[0].getBoundingClientRect().width || 280;
    const r = Math.round((w / 2) / Math.tan(Math.PI / Math.max(n, 7)) + w * 0.18);
    ring.style.setProperty('--r', r + 'px');
    cards.forEach((c, i) => c.style.setProperty('--a', (i * step) + 'deg'));
  };

  let active = -1, typing = 0;
  const typeTitle = (h) => {
    const full = h.dataset.full ?? (h.dataset.full = h.textContent);
    cancelAnimationFrame(typing);
    const t0 = performance.now();
    const tick = (t) => {
      const k = Math.min(full.length, Math.floor((t - t0) / TYPE_MS));
      h.textContent = full.slice(0, k);
      if (k < full.length) typing = requestAnimationFrame(tick);
    };
    h.textContent = '';
    typing = requestAnimationFrame(tick);
  };
  const setActive = (i) => {
    if (i === active) return;
    active = i;
    steps.forEach((s, k) => s.classList.toggle('is-on', k === i));
    stack.forEach((s, k) => s.classList.toggle('is-on', k === i));
    const h = steps[i]?.querySelector('h3');
    if (h) typeTitle(h);
    const c = cards[i];
    if (c) { c.classList.remove('is-scan'); void c.offsetWidth; c.classList.add('is-scan'); }
    if (count) count.textContent = String(i + 1).padStart(2, '0');
  };

  let queued = false;
  const frame = () => {
    queued = false;
    const r = sec.getBoundingClientRect();
    const span = sec.offsetHeight - innerHeight;
    const p = Math.min(1, Math.max(0, -r.top / Math.max(1, span)));
    sec.style.setProperty('--p', p.toFixed(4));
    const raw = p * (n - 1);                                  // 0 .. n-1 along the scroll
    // each screen rests in front for the middle of its stretch, then the ring turns to the next
    const k0 = Math.floor(raw), f = raw - k0;
    const t = Math.min(1, Math.max(0, (f - 0.3) / 0.4));
    const pos = Math.min(n - 1, k0 + t * t * (3 - 2 * t));
    ring.style.setProperty('--turn', (-pos * step).toFixed(2) + 'deg');
    cards.forEach((c, k) => {
      const d = Math.min(1, Math.abs(k - pos));
      c.style.setProperty('--shade', (Math.min(1, Math.abs(k - pos) / 2) * 0.78).toFixed(3));
      c.style.setProperty('--lift', (1 - d).toFixed(3));        // 1 for the screen in front
    });
    setActive(Math.round(raw));
  };
  const request = () => { if (!queued) { queued = true; requestAnimationFrame(frame); } };

  // a step in the call stack scrolls the page to it
  stack.forEach((li, k) => li.querySelector('button').addEventListener('click', () => {
    const span = sec.offsetHeight - innerHeight;
    const top = sec.getBoundingClientRect().top + scrollY + span * (k / Math.max(1, n - 1));
    scrollTo({ top, behavior: 'smooth' });
  }));

  // the command line types itself once, when the section first comes into view
  if (cmd) {
    const text = cmd.textContent; cmd.textContent = '';
    new IntersectionObserver((es, io) => {
      if (!es.some(e => e.isIntersecting)) return;
      io.disconnect();
      let k = 0;
      const id = setInterval(() => { cmd.textContent = text.slice(0, ++k); if (k >= text.length) clearInterval(id); }, 34);
    }, { rootMargin: '0px 0px -30% 0px' }).observe(sec);
  }

  layout();
  frame();
  addEventListener('scroll', request, { passive: true });
  addEventListener('resize', () => { layout(); request(); });
  // the language switch rewrites the titles: forget the typed copy
  new MutationObserver(() => steps.forEach(s => { const h = s.querySelector('h3'); if (h && h.dataset.ar !== undefined) delete h.dataset.full; }))
    .observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
}
