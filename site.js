// Language switch (English / Arabic) and the work reveal. No library.
// Every translatable element carries its Arabic in data-ar (HTML allowed); the English stays in the markup,
// so the page reads in full without script. data-ar-alt / data-ar-aria / data-ar-href swap attributes.
const root = document.documentElement;

// the language lives in the address (?lang=ar), so a shared link opens in the language it was sent in
function readLang() {
  return new URLSearchParams(location.search).get('lang') === 'ar' ? 'ar' : 'en';
}

function loadArabicFont() {
  if (document.getElementById('font-ar')) return;
  const l = document.createElement('link');
  l.id = 'font-ar'; l.rel = 'stylesheet';
  l.href = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500&display=swap';
  document.head.appendChild(l);
}

function swap(el, attr, key) {
  const enKey = 'en' + key;
  if (el.dataset[enKey] === undefined) el.dataset[enKey] = attr ? (el.getAttribute(attr) ?? '') : el.innerHTML;
  return el.dataset[enKey];
}

function apply(lang) {
  const ar = lang === 'ar';
  if (ar) loadArabicFont();
  root.lang = ar ? 'ar' : 'en';
  root.dir = ar ? 'rtl' : 'ltr';
  document.querySelectorAll('[data-ar]').forEach(el => {
    const en = swap(el, null, 'Html');
    el.innerHTML = ar ? el.dataset.ar : en;
  });
  for (const [data, attr] of [['arAlt', 'alt'], ['arAria', 'aria-label'], ['arContent', 'content'], ['arTitle', 'title']]) {
    document.querySelectorAll(`[data-${data.replace(/[A-Z]/g, c => '-' + c.toLowerCase())}]`).forEach(el => {
      const en = swap(el, attr, data);
      el.setAttribute(attr, ar ? el.dataset[data] : en);
    });
  }
  const t = document.querySelector('title');
  if (t && t.dataset.arTitleText) {
    if (t.dataset.enTitleText === undefined) t.dataset.enTitleText = t.textContent;
    t.textContent = ar ? t.dataset.arTitleText : t.dataset.enTitleText;
  }
  document.querySelectorAll('[data-lang-toggle]').forEach(b => {
    b.textContent = ar ? 'English' : 'العربية';
    b.lang = ar ? 'en' : 'ar';
    b.setAttribute('aria-label', ar ? 'Read this page in English' : 'اقرأ الصفحة بالعربية');
  });
  // keep the language when moving between pages
  document.querySelectorAll('a[href]:not([lang])').forEach(a => {
    const h = a.getAttribute('href');
    if (!h || /^(https?:|mailto:|#)/.test(h)) return;
    const m = h.match(/^([^?#]*)(\?[^#]*)?(#.*)?$/);
    a.setAttribute('href', m[1] + (ar ? '?lang=ar' : '') + (m[3] || ''));
  });
  root.classList.remove('i18n-wait');
}

let lang = readLang();
apply(lang);
document.querySelectorAll('[data-lang-toggle]').forEach(b => b.addEventListener('click', () => {
  lang = lang === 'ar' ? 'en' : 'ar';
  const u = new URL(location.href);
  if (lang === 'ar') u.searchParams.set('lang', 'ar'); else u.searchParams.delete('lang');
  history.replaceState(null, '', u);
  apply(lang);
}));

// Motion on scroll, asked for in the brief: once per element, started on its first visible pixel, so
// nothing is ever hidden before (no script, no IntersectionObserver or reduced motion: everything stands).
//  [data-reveal="stagger"]  its children rise 28px and fade in, 90ms apart
//  [data-reveal]            the element itself
//  [data-reveal-img]        a picture uncovers from the bottom while it settles from 1.06
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
const OUT = 'cubic-bezier(.23,1,.32,1)', INOUT = 'cubic-bezier(.77,0,.175,1)';
const rise = (el, delay) => el.animate(
  [{ opacity: 0, transform: 'translateY(28px)' }, { opacity: 1, transform: 'none' }],
  { duration: 760, delay, easing: OUT, fill: 'backwards' });
function play(el) {
  if (el.matches('[data-reveal-img]')) {
    el.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }], { duration: 1100, easing: INOUT, fill: 'backwards' });
    const img = el.querySelector('img');
    if (img) img.animate([{ transform: 'scale(1.06)' }, { transform: 'scale(1)' }], { duration: 1400, easing: OUT, fill: 'backwards' });
  } else if (el.dataset.reveal === 'stagger') {
    [...el.children].forEach((c, i) => rise(c, i * 90));
  } else {
    rise(el, 0);
  }
}
const items = [...document.querySelectorAll('[data-reveal], [data-reveal-img]')];
if (!still && 'IntersectionObserver' in window && items.length) {
  root.classList.add('reveal-on');
  const io = new IntersectionObserver(entries => {
    entries.filter(e => e.isIntersecting).forEach(e => { play(e.target); io.unobserve(e.target); });
  }, { rootMargin: '0px', threshold: 0 });
  // what is already on screen at load is part of the page's first paint: it stands
  requestAnimationFrame(() => items.forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.top < innerHeight && r.bottom > 0) return;
    io.observe(el);
  }));
}
