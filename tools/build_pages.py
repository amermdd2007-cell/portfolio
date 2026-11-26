"""Builds the project pages in work/ from the content below (python tools/build_pages.py).
Each page: the shared nav, a hero (name, summary, role / year / tools, the cover that carries over
from the home page), the problem and the fix, the work itself, the next project, the shared footer.
Every visible line has its Arabic in data-ar."""
import html, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIL = 'mailto:amer.mdddd.2007@gmail.com'
ARROW = '<svg class="m-arrow" viewBox="0 0 12 12" aria-hidden="true"><path class="m-arrow__stem" d="M1 6h8"/><path class="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5"/></svg>'


def a(s):
    return html.escape(s, quote=True)


def t(tag, en, ar, cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c}{extra} data-ar="{a(ar)}">{en}</{tag}>'


def img(src, en, ar, cls='', extra='', lazy=True):
    c = f' class="{cls}"' if cls else ''
    lz = ' loading="lazy"' if lazy else ''
    w, h = Image.open(os.path.join(ROOT, 'img', src)).size
    sm = src.replace('.jpg', '-800.jpg')
    srcset = f' srcset="../img/{sm} 800w, ../img/{src} {w}w" sizes="(min-width: 1024px) 45vw, 92vw"' if os.path.exists(os.path.join(ROOT, 'img', sm)) else ''
    return f'<img{c} src="../img/{src}"{srcset} width="{w}" height="{h}" alt="{a(en)}" data-ar-alt="{a(ar)}"{lz}{extra}>'


TOOLS = {
    'figma': ('figma.svg', 27, 40, 'Figma'),
    'flutter': ('flutter.svg', 33, 40, 'Flutter'),
    'claude': ('claude.svg', 40, 40, 'Claude'),
    'react': ('react.svg', 40, 36, 'React and Remotion'),
    'play': ('google-play.svg', 36, 40, 'Google Play'),
}


def tools(keys):
    out = []
    for k in keys:
        f, w, h, name = TOOLS[k]
        out.append(f'<li><img src="../assets/icons/{f}" alt="" width="{w}" height="{h}" loading="lazy">{name}</li>')
    return '<ul class="tools">' + ''.join(out) + '</ul>'


HEAD = '''<!doctype html>
<html lang="en" data-type="service" data-radius="soft" data-buttons="pill" data-motion style="--pc: {pc}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-ar-title-text="{title_ar}">{title}</title>
<meta name="description" content="{desc}" data-ar-content="{desc_ar}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="../img/{cover}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0d0e10">
<meta name="site-kind" content="other">
<meta name="page-type" content="service">
<script>
  (function(){{var q=new URLSearchParams(location.search).get('lang');
  if(q==='ar'){{var r=document.documentElement;r.lang='ar';r.dir='rtl';r.classList.add('i18n-wait');setTimeout(function(){{r.classList.remove('i18n-wait')}},900)}}}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Instrument+Serif:ital@1&family=Work+Sans:wght@400..600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/system.css">
<link rel="stylesheet" href="../assets/ui/cards.css">
<link rel="stylesheet" href="../assets/motion/motion.css">
<link rel="stylesheet" href="../assets/layout/layout.css">
<link rel="stylesheet" href="../assets/icons/icon.css">
<style>
:root {{
  --p-bg: #0d0e10; --p-surface: #16181b; --p-ink: #f2efe8; --p-muted: #9a968d;
  --p-accent: {pc}; --p-accent-ink: #111111; --p-action: {pc}; --p-action-ink: #111111;
  --p-inv-bg: #16181b; --p-inv-surface: #1d2024; --p-inv-ink: #f2efe8; --p-inv-muted: #9a968d;
  --p-inv-accent: {pc}; --p-inv-accent-ink: #111111; --p-inv-action: {pc}; --p-inv-action-ink: #111111;
  --font-display: "Bricolage Grotesque", "Work Sans", system-ui, sans-serif;
  --font-text: "Work Sans", system-ui, sans-serif;
  --display-weight: 700; --display-tracking: -0.035em; --display-tracking-xl: -0.045em; --ly-scale: 1.04;
}}
</style>
<link rel="stylesheet" href="../site.css">
<link rel="stylesheet" href="../story3d.css">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
</head>
<body>
<header class="nav nav--split">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top" data-ar="تخطَّ إلى المحتوى">Skip to content</a>
    <nav class="nav__links" aria-label="Main" data-ar-aria="الرئيسية">
      <div class="nav__item"><a class="nav__link" href="../index.html#work" data-ar="الأعمال">Work</a></div>
      <div class="nav__item"><a class="nav__link" href="../index.html#about" data-ar="عنّي">About</a></div>
      <div class="nav__item"><a class="nav__link" href="../index.html#services" data-ar="الخدمات">Services</a></div>
    </nav>
    <a class="nav__logo" href="../index.html"><span class="mark" data-mark="dots" aria-hidden="true"></span><span data-ar="عامر الدلق">Amer AL Dalaq</span></a>
    <div class="nav__actions">
      <button class="lang-toggle nav__link" type="button" data-lang-toggle lang="ar" aria-label="اقرأ الصفحة بالعربية">العربية</button>
      <a class="btn btn--primary" href="{mail}" data-ar="راسل عامر">Email Amer</a>
    </div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="Menu" data-ar-aria="القائمة">
      <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>
<main id="top">
'''

FOOT = '''</main>
<footer class="footer closing footer--dark ground-inverse" id="contact" aria-labelledby="close-h">
  <div class="wrap">
    <div class="closing__cta close--word">
      <div class="section-head--split">
        <div><h2 id="close-h" data-ar="راسل عامر بخصوص مشروعك">Email Amer about your project</h2><p class="t-lead" data-ar="اكتب لي بالعربية أو الإنجليزية: ما الفكرة، ولمن، ومتى تحتاجها.">Write in Arabic or English: the idea, who it is for and when you need it.</p></div>
        <a class="btn btn--primary" href="{mail}"><span data-ar="راسل عامر">Email Amer</span>{arrow}</a>
      </div>
    </div>
    <div class="closing__links">
      <div class="grid">
        <div class="span-4 stack-4">
          <a class="nav__logo" href="../index.html"><span class="mark" data-mark="dots" aria-hidden="true"></span><span data-ar="عامر الدلق">Amer AL Dalaq</span></a>
          <p class="footer__lede" data-ar="أصمّم التطبيقات والهويات، وأبنيها.">I design apps and brands, and build them.</p>
        </div>
        <div class="span-2 footer__col"><h3 data-ar="الأعمال">Work</h3><ul>
          <li><a href="bug-hunter.html">Bug Hunter</a></li>
          <li><a href="reels.html" data-ar="الفيديوهات">Reels</a></li>
          <li><a href="wasla.html" data-ar="وَصلة">Wasla</a></li>
          <li><a href="masar.html" data-ar="مسار">Masar</a></li>
          <li><a href="travel-jo.html">Travel JO</a></li>
        </ul></div>
        <div class="span-2 footer__col"><h3 data-ar="عنّي">About</h3><ul>
          <li><a href="../index.html#about" data-ar="قصتي">My story</a></li>
          <li><a href="../index.html#process" data-ar="طريقة عملي">How I work</a></li>
          <li><a href="../index.html#services" data-ar="الخدمات">Services</a></li>
        </ul></div>
        <div class="span-2 footer__col"><h3 data-ar="تواصل">Contact</h3><ul>
          <li><a href="{mail}" data-ar="البريد">Email</a></li>
        </ul></div>
        <div class="span-2 footer__col"><h3 data-ar="اللغة">Language</h3><ul>
          <li><a href="{slug}.html" lang="en">English</a></li>
          <li><a href="{slug}.html?lang=ar" lang="ar">العربية</a></li>
        </ul></div>
      </div>
      <div class="footer__legal">
        <span>&copy; 2026 <span data-ar="عامر الدلق">Amer AL Dalaq</span></span>
        <span data-ar="أسماء المنتجات وشعاراتها علامات تجارية لأصحابها.">Product names and logos are trademarks of their owners.</span>
      </div>
    </div>
  </div>
</footer>
<script type="module" src="../site.js"></script>
<script type="module" src="../story3d.js"></script>
<script type="module" src="../assets/system.js"></script>
<script type="module" src="../assets/motion/motion.js"></script>
<script type="module" src="../assets/layout/layout.js"></script>
</body>
</html>
'''


def hero(p):
    facts = ''.join(
        f'<div><dt data-ar="{a(lab_ar)}">{lab}</dt><dd data-ar="{a(v_ar)}">{v}</dd></div>'
        for lab, lab_ar, v, v_ar in p['facts'])
    return f'''  <section class="hero hero--split" data-enter aria-labelledby="hero-h">
    <div class="wrap">
      <div class="hero-text grid hero-split">
        <div class="hero-copy span-6">
          <h1 id="hero-h" data-ar="{a(p['h1_ar'])}">{p['h1']}</h1>
          <p class="t-lead" data-ar="{a(p['lead_ar'])}">{p['lead']}</p>
          <dl class="facts">{facts}</dl>
          {tools(p['tools']) if p.get('steps') else ''}
        </div>
        <div class="hero-visual frame frame--photo span-6 start-7">
          {img(p['cover'], p['cover_alt'], p['cover_alt_ar'], cls='frame__img', extra=f' style="view-transition-name: p-{p["slug"]}" fetchpriority="high"', lazy=False)}
        </div>
      </div>
    </div>
  </section>
'''


def story(p):
    rows = ''.join(
        f'<div><h3 data-ar="{a(h_ar)}">{h}</h3><p data-ar="{a(b_ar)}">{b}</p></div>'
        for h, h_ar, b, b_ar in p['story'])
    pic = p['story_pic']
    return f'''  <section class="section" id="story" aria-labelledby="story-h" style="height: auto">
    <div class="wrap">
      <div class="grid grid--top">
        <div class="span-5">
          <h2 id="story-h" data-ar="{a(p['story_h_ar'])}">{p['story_h']}</h2>
          <div class="story" data-reveal="stagger">{rows}</div>
          <h3 class="t-label" style="margin-top: var(--s-7); color: var(--muted)" data-ar="الأدوات">Tools</h3>
          {tools(p['tools'])}
        </div>
        <div class="frame frame--photo span-6 start-7" style="aspect-ratio: 4 / 5; max-height: 708px" data-reveal-img>
          {img(pic[0], pic[1], pic[2], cls='frame__img', extra=f' style="object-position: {pic[4]}"')}
        </div>
      </div>
    </div>
  </section>
'''


def story3d(p):
    """The pinned 3D story: screens on a ring that turn with the scroll, an editor that explains each."""
    st = p['steps']
    cards = ''.join(
        f'<figure class="s3__card">{shot(src, e, r, sizes="(min-width: 1024px) 250px, 46vw")}</figure>' for src, e, r, *_ in st)
    steps = ''.join(
        f'<div class="s3__step"><span class="s3__ln">{i * 3 + 1:02d}</span><div>'
        f'<span class="c" data-ar="{a("// " + lab_ar)}">// {lab}</span>'
        f'<h3 data-ar="{a(h_ar)}">{h}</h3><p data-ar="{a(b_ar)}">{b}</p></div></div>'
        for i, (src, e, r, lab, lab_ar, h, h_ar, b, b_ar) in enumerate(st))
    stack = ''.join(
        f'<li><button type="button"><span class="bp" aria-hidden="true"></span><span data-ar="{a(lab_ar)}">{lab}</span></button></li>'
        for src, e, r, lab, lab_ar, *_ in st)
    return f'''  <section class="s3" data-story aria-labelledby="s3-h">
    <div class="s3__pin">
      <div class="wrap">
        <h2 id="s3-h" class="sr-only" data-ar="{a(p['s3_h_ar'])}">{p['s3_h']}</h2>
        <div class="s3__grid">
          <div class="s3__editor">
            <div class="s3__tabs"><span class="dot" aria-hidden="true"></span><b>{p['slug']}.case</b><span>· {len(st)} steps</span></div>
            <p class="s3__cmd" aria-hidden="true"><span class="p">$</span> <span data-type>open {p['slug']} --case-study</span><span class="caret"></span></p>
            <div class="s3__steps">{steps}</div>
            <ol class="s3__stack" aria-label="Steps" data-ar-aria="الخطوات">{stack}</ol>
            <div class="s3__bar" aria-hidden="true"><i></i></div>
          </div>
          <div class="s3__stage">
            <div class="s3__ring">{cards}</div>
            <p class="s3__count" aria-hidden="true"><b>01</b> / {len(st):02d}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
'''


def built(items, pics, h, h_ar, line, line_ar):
    """How it is built: the stack as plain rows beside real code from the project."""
    rows = ''.join(
        f'<li><b data-ar="{a(n_ar)}">{n}</b><span data-ar="{a(d_ar)}">{d}</span></li>' for n, n_ar, d, d_ar in items)
    shots_html = ''.join(f'<figure class="code-shot">{img(s_, e, r)}</figure>' for s_, e, r in pics)
    return f'''  <section class="section built" id="built" aria-labelledby="built-h" style="height: auto">
    <div class="wrap">
      <div class="section-head"><h2 id="built-h" data-ar="{a(h_ar)}">{h}</h2><p data-ar="{a(line_ar)}">{line}</p></div>
      <div class="built__grid">
        <ul class="stack-list" data-reveal="stagger">{rows}</ul>
        <div class="code-shots" data-reveal="stagger">{shots_html}</div>
      </div>
    </div>
  </section>
'''


def section(sid, h, h_ar, line, line_ar, body):
    sub = f'<p data-ar="{a(line_ar)}">{line}</p>' if line else ''
    return f'''  <section class="section" id="{sid}" aria-labelledby="{sid}-h" style="height: auto">
    <div class="wrap">
      <div class="section-head"><h2 id="{sid}-h" data-ar="{a(h_ar)}">{h}</h2>{sub}</div>
      {body}
    </div>
  </section>
'''


def shots(items, five=False):
    cls = 'shots shots--five' if five else 'shots'
    return f'<ul class="{cls}" data-reveal="stagger">' + ''.join(f'<li>{shot(s, e, r)}</li>' for s, e, r in items) + '</ul>'


def shot(src, en, ar, sizes='(min-width: 1024px) 22vw, (min-width: 640px) 30vw, 46vw'):
    # a phone screen: four a row on a desktop, two on a phone, so a 340px copy for small screens
    w, h = Image.open(os.path.join(ROOT, 'img', src)).size
    sm = src.replace('.jpg', '-340.jpg')
    srcset = f' srcset="../img/{sm} 340w, ../img/{src} {w}w" sizes="{sizes}"' if os.path.exists(os.path.join(ROOT, 'img', sm)) else ''
    return f'<img src="../img/{src}"{srcset} width="{w}" height="{h}" alt="{a(en)}" data-ar-alt="{a(ar)}" loading="lazy">'


def wide(items, one=False):
    cls = 'wide wide--one' if one else 'wide'
    return f'<div class="{cls}" data-reveal="stagger">' + ''.join(img(s, e, r) for s, e, r in items) + '</div>'


def nxt(p):
    n = p['next']
    return f'''  <section class="section" aria-label="Next project" data-ar-aria="المشروع التالي" style="height: auto; padding-top: 0">
    <div class="wrap">
      <a class="next" href="{n[0]}.html"><span><span class="t-label" data-ar="المشروع التالي">Next project</span><span class="next__name" data-ar="{a(n[2])}">{n[1]}</span></span><svg class="m-arrow" viewBox="0 0 12 12" aria-hidden="true"><path class="m-arrow__stem" d="M1 6h8"/><path class="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5"/></svg></a>
    </div>
  </section>
'''


# ------------------------------------------------------------------ the projects
P = []

P.append(dict(
    slug='bug-hunter', pc='#f2a93b', cover='cover-bug-hunter.jpg',
    title='Bug Hunter: a programming game, designed and built by Amer AL Dalaq',
    title_ar='Bug Hunter: لعبة برمجة صمّمها وبناها عامر الدلق',
    desc='How Bug Hunter 3.0 was redesigned in Figma to look like a real debugger, then rebuilt in Flutter and published on Google Play.',
    desc_ar='كيف أُعيد تصميم Bug Hunter 3.0 في Figma ليشبه أداة تصحيح حقيقية، ثم بُني بـ Flutter ونُشر على Google Play.',
    tag='Solo project · Design and Flutter · 2026', tag_ar='مشروع فردي · تصميم وبرمجة · 2026',
    h1='Bug Hunter, a game for learning to code', h1_ar='Bug Hunter، لعبة لتعلّم البرمجة',
    lead='Players fix one bug a level in real code, in C++, Python, Java and more. I designed three versions of it and built every one in Flutter; it is live on Google Play.',
    lead_ar='يصلّح اللاعب خطأً واحداً في كل مرحلة داخل كود حقيقي، بلغات مثل C++ وPython وJava. صمّمت منها ثلاث نسخ وبنيت كل نسخة بـ Flutter، وهي منشورة على Google Play.',
    facts=[('My role', 'دوري', 'Design, Flutter, store page', 'التصميم والبرمجة وصفحة المتجر'),
           ('Year', 'السنة', '2026', '2026'),
           ('Screens', 'الشاشات', '25 phone, 3 tablet', '25 للجوال و3 للتابلت')],
    cover_alt='Home, game and result screens of Bug Hunter 3.0', cover_alt_ar='شاشات الرئيسية واللعب والنتيجة في Bug Hunter 3.0',
    story_h='The problem and the fix', story_h_ar='المشكلة والحل',
    story=[('The problem', 'المشكلة',
            'Version 2.0 had neon gradients, glowing cards and emoji everywhere. Players told me it looked AI-made, and some did not believe a student had built it.',
            'كانت النسخة 2.0 مليئة بالتدرّجات اللامعة والبطاقات المضيئة والإيموجي. قال لي اللاعبون إنها تبدو مصنوعة بالذكاء الاصطناعي، وبعضهم لم يصدّق أن طالباً بناها.'),
           ('The fix', 'الحل',
            'Version 3.0 copies the tools programmers already trust: line numbers, a red squiggle under the bug, breakpoint dots, 4px corners and amber only for warnings. I built the system first, then 25 phone and 3 tablet screens, then the app.',
            'النسخة 3.0 تأخذ من الأدوات التي يثق بها المبرمجون: أرقام الأسطر، وخط أحمر متموّج تحت الخطأ، ونقاط التوقف، وزوايا 4px، والكهرماني للتحذير فقط. بنيت النظام أولاً، ثم 25 شاشة للجوال و3 للتابلت، ثم التطبيق.'),
           ('What came out', 'النتيجة',
            'The redesign shipped as version 3.0 on Google Play in November 2026, with new store screenshots and a store banner in the same style.',
            'نُشرت النسخة 3.0 على Google Play في نوفمبر 2026، مع صور متجر جديدة وبانر بالأسلوب نفسه.')],
    story_pic=('bug-hunter/design-system.jpg', 'The Bug Hunter 3.0 design system board: logo, colours, type and components',
               'لوحة نظام تصميم Bug Hunter 3.0: الشعار والألوان والخطوط والمكوّنات', '4 / 5', '50% 0%'),
    tools=['figma', 'flutter', 'play', 'claude'],
    s3_h='Bug Hunter, screen by screen', s3_h_ar='Bug Hunter، شاشة شاشة',
    steps=[
        ('bug-hunter/v2-home.jpg', 'Version 2.0 home screen with neon gradients', 'الرئيسية في النسخة 2.0 بالتدرّجات اللامعة',
         'before: v2.0', 'قبل: النسخة 2.0',
         'Players said it looked AI-made', 'قال اللاعبون إنها تبدو مصنوعة بالذكاء الاصطناعي',
         'Neon gradients, glowing cards and emoji everywhere. Some players did not believe a student had built it, so the look had to change, not the game.',
         'تدرّجات لامعة وبطاقات مضيئة وإيموجي في كل مكان. بعض اللاعبين لم يصدّقوا أن طالباً بناها، فكان لا بد أن يتغيّر الشكل لا اللعبة.'),
        ('bug-hunter/home.jpg', 'Version 3.0 home: the next level shown as a code editor', 'رئيسية النسخة 3.0: المرحلة التالية كمحرّر كود',
         'home', 'الرئيسية',
         'Home opens like a code editor', 'الرئيسية تُفتح كمحرّر كود',
         'The next level waits in an editor tab with line numbers and the bug already marked. Players see code before they see a menu.',
         'المرحلة التالية تنتظر في تبويب محرّر بأرقام أسطر والخطأ معلَّم مسبقاً. يرى اللاعب الكود قبل أن يرى أي قائمة.'),
        ('bug-hunter/paths.jpg', 'Paths: the languages listed like a file explorer', 'المسارات: اللغات كمستكشف ملفات',
         'paths', 'المسارات',
         'Languages as a file explorer', 'اللغات كمستكشف ملفات',
         'C++, Python, Java and the rest sit in an explorer tree with their progress, the way a programmer browses a project.',
         'C++ وPython وJava وباقي اللغات في شجرة ملفات مع تقدّم كل منها، كما يتصفح المبرمج مشروعه.'),
        ('bug-hunter/game.jpg', 'The game screen: the bug line underlined in red', 'شاشة اللعب: سطر الخطأ وتحته خط أحمر',
         'game', 'اللعب',
         'The bug gets a red squiggle', 'الخطأ تحته خط أحمر متموّج',
         'The broken line has a <b>breakpoint dot</b> and a red squiggle, like a compiler warning. The output panel shows the real runtime error.',
         'السطر الخاطئ عليه <b>نقطة توقف</b> وخط أحمر متموّج، كتحذير المترجم. ولوحة المخرجات تعرض خطأ التشغيل الحقيقي.'),
        ('bug-hunter/result.jpg', 'Result: build passed, with the diff of the fix', 'النتيجة: نجح البناء مع الفرق بين السطرين',
         'result', 'النتيجة',
         'Build passed, with the diff', 'نجح البناء، مع الفرق',
         'Instead of confetti, the player gets what a developer gets: <b>BUILD PASSED</b>, the time, the points and the red and green diff of the fixed line.',
         'بدل الاحتفالات، يحصل اللاعب على ما يحصل عليه المطوّر: <b>BUILD PASSED</b>، والوقت، والنقاط، والفرق الأحمر والأخضر للسطر الذي أصلحه.'),
        ('bug-hunter/daily-bug.jpg', 'The daily bug with a contribution graph', 'خطأ اليوم مع مخطط المساهمات',
         'daily', 'اليومي',
         'A contribution graph for streaks', 'مخطط مساهمات للأيام المتتالية',
         'The daily bug keeps a grid of solved days in amber, the same graph programmers know from their code history.',
         'خطأ اليوم يحفظ شبكة الأيام المحلولة باللون الكهرماني، المخطط نفسه الذي يعرفه المبرمجون من سجل أكوادهم.'),
        ('bug-hunter/season.jpg', 'The season as a list of passed and failed tests', 'الموسم كقائمة اختبارات ناجحة وفاشلة',
         'season', 'الموسم',
         'The season as a test run', 'الموسم كتشغيل اختبارات',
         'Each week is a test: PASS in green, FAIL in red. 25 phone and 3 tablet screens, all built from the same 10 components.',
         'كل أسبوع اختبار: PASS بالأخضر وFAIL بالأحمر. 25 شاشة للجوال و3 للتابلت، كلها مبنية من المكوّنات العشرة نفسها.'),
    ],

    body=lambda: (
        built([
            ('Flutter and Dart', 'Flutter وDart', 'The whole app, Arabic and English, phone and tablet, from my own designs.', 'التطبيق كاملاً بالعربية والإنجليزية، للجوال والتابلت، من تصاميمي.'),
            ('A Dart server in Docker', 'سيرفر Dart داخل Docker', 'shelf and SQLite for accounts, seasons, contests and duels, running on a server at home.', 'shelf وSQLite للحسابات والمواسم والمسابقات والمبارزات، يعمل على سيرفر في البيت.'),
            ('Judge0 for the code lab', 'Judge0 لمختبر الكود', 'Players write and run real code; Judge0 runs it safely, away from the app.', 'يكتب اللاعب كوداً حقيقياً ويشغّله؛ وJudge0 يشغّله بأمان بعيداً عن التطبيق.'),
            ('A fair contest', 'مسابقة عادلة', 'Google Sign-In and Play Integrity, so every score comes from a real install.', 'تسجيل دخول Google وPlay Integrity، لتأتي كل نتيجة من تطبيق حقيقي.'),
            ('An admin dashboard', 'لوحة تحكم', 'New levels, lessons and contests go live without a new app version.', 'مراحل ودروس ومسابقات جديدة تُنشر دون إصدار نسخة جديدة من التطبيق.'),
            ('AdMob and a Pro plan', 'AdMob واشتراك Pro', 'Ads, plus a subscription through Google Play billing.', 'إعلانات، واشتراك عبر الدفع في Google Play.'),
            ('Close to 300 automated tests', 'قرابة 300 اختبار تلقائي', 'So more than 30 updates shipped without breaking what already worked.', 'لتخرج أكثر من 30 تحديثاً دون أن ينكسر ما كان يعمل.'),
        ], [
            ('bug-hunter/code-daily.jpg', 'Dart code in VS Code that picks each player a daily bug for their level', 'كود Dart في VS Code يختار لكل لاعب خطأ اليوم على قدّ مستواه'),
            ('bug-hunter/code-ui.jpg', 'Flutter code in VS Code for the home screen card', 'كود Flutter في VS Code لبطاقة الشاشة الرئيسية'),
        ], 'How I built it', 'كيف بنيتها',
           '400+ levels, 200+ lessons and 13 paths, from C++ and Python to SQL, Linux and cyber security, all in one app I code myself.',
           'أكثر من 400 مرحلة و200 درس و13 مساراً، من C++ وPython إلى SQL وLinux والأمن السيبراني، في تطبيق واحد أبرمجه بنفسي.')
        + section('tablet', 'Tablet and brand', 'التابلت والهوية',
                'The tablet splits the code and the task side by side. The logo is two code braces holding a bug.',
                'في التابلت يظهر الكود والمهمة جنباً إلى جنب. والشعار قوسا كود يحتضنان حشرة.',
                wide([('bug-hunter/t2.jpg', 'The game on an iPad: code on one side, the task on the other', 'اللعب على الآيباد: الكود في جهة والمهمة في الأخرى'),
                      ('bug-hunter/logo.jpg', 'The Bug Hunter logo: braces around a bug on amber', 'شعار Bug Hunter: قوسان حول حشرة على الكهرماني')]))
    ),
    next=('reels', 'Reels for @bughunter_code', 'فيديوهات @bughunter_code'),
))

P.append(dict(
    slug='reels', pc='#8b6cff', cover='cover-reels.jpg',
    title='Reels for @bughunter_code by Amer AL Dalaq',
    title_ar='فيديوهات @bughunter_code من عامر الدلق',
    desc='Short animated videos for programming students, built in code with Remotion. One reached 112,700 views and 3,616 saves.',
    desc_ar='فيديوهات قصيرة متحركة لطلاب البرمجة، مبنية بالكود عبر Remotion. أحدها وصل إلى 112,700 مشاهدة و3,616 حفظ.',
    tag='Solo project · Motion and social · 2026', tag_ar='مشروع فردي · موشن وتواصل اجتماعي · 2026',
    h1='Reels for programming students', h1_ar='فيديوهات قصيرة لطلاب البرمجة',
    lead='Short videos for the Bug Hunter Instagram page, made in code with Remotion: one idea per scene, captions word by word, Arabic voice-over. "C++ in a minute" reached 112,700 views.',
    lead_ar='فيديوهات قصيرة لصفحة Bug Hunter على إنستغرام، مصنوعة بالكود عبر Remotion: فكرة واحدة في كل مشهد، وترجمة كلمة بكلمة، وتعليق صوتي بالعربية. فيديو «C++ بدقيقة» وصل إلى 112,700 مشاهدة.',
    facts=[('My role', 'دوري', 'Idea, script, motion, posting', 'الفكرة والنص والحركة والنشر'),
           ('Year', 'السنة', '2026', '2026'),
           ('Videos', 'الفيديوهات', 'More than 20 published', 'أكثر من 20 فيديو منشور')],
    cover_alt='Frames from the C++ in a minute reel and a bug-fix reel', cover_alt_ar='لقطات من فيديو C++ بدقيقة وفيديو تصحيح خطأ',
    story_h='The problem and the fix', story_h_ar='المشكلة والحل',
    story=[('The problem', 'المشكلة',
            'A new page with no budget. My first quiz reels reached 250 to 600 people and brought almost no followers.',
            'صفحة جديدة بلا ميزانية. أول فيديوهات الأسئلة وصلت إلى 250 حتى 600 شخص، ولم تجلب متابعين تقريباً.'),
           ('The fix', 'الحل',
            'I read the numbers after each post. Videos that students save before an exam spread; definitions did not. So every reel became a fast summary or a trap that shows a surprising output.',
            'كنت أقرأ الأرقام بعد كل منشور. الفيديوهات التي يحفظها الطلاب قبل الامتحان انتشرت، والتعريفات لم تنتشر. فصار كل فيديو ملخصاً سريعاً أو فخاً يُظهر نتيجة غير متوقعة.'),
           ('What came out', 'النتيجة',
            '"C++ in a minute" reached 112,700 views, 3,616 saves and 2,557 shares, and the page grew from 564 to 1,873 followers in a day and a half.',
            'فيديو «C++ بدقيقة» وصل إلى 112,700 مشاهدة و3,616 حفظ و2,557 مشاركة، وكبرت الصفحة من 564 إلى 1,873 متابعاً خلال يوم ونصف.')],
    story_pic=('reels/r1_2.jpg', 'The opening frame of C++ in a minute: the glowing C++ letters over a grid floor',
               'اللقطة الأولى من فيديو C++ بدقيقة: حروف C++ المضيئة فوق أرضية شبكية', '9 / 16', '50% 50%'),
    tools=['react', 'claude'],
    s3_h='The reels, one by one', s3_h_ar='الفيديوهات، واحداً واحداً',
    steps=[
        ('reels/r3_2.jpg', 'The i++ vs ++i quiz reel', 'فيديو سؤال i++ أم ++i',
         'quiz reels', 'فيديوهات الأسئلة', 'Quizzes reached few people', 'الأسئلة وصلت لعدد قليل',
         'The first quiz reels reached 250 to 600 people and almost nobody followed. The page needed a format students keep.',
         'أول فيديوهات الأسئلة وصلت إلى 250 حتى 600 شخص، وتقريباً لم يتابع أحد. احتاجت الصفحة شكلاً يحتفظ به الطلاب.'),
        ('reels/r4_20.jpg', 'A bug and its fix in the exam reel', 'خطأ وتصحيحه في فيديو الامتحان',
         'exam bugs', 'أخطاء الامتحان', 'Bugs that cost exam marks', 'أخطاء تكلّف علامات بالامتحان',
         'Three common bugs with the red line and its fix. Students saved it to revise later.',
         'ثلاثة أخطاء شائعة مع السطر الأحمر وتصحيحه. حفظه الطلاب ليراجعوه لاحقاً.'),
        ('reels/r2_2.jpg', 'The C++ cheat sheet reel', 'فيديو ملخص C++',
         'cheat sheet', 'الملخص', 'A cheat sheet took off', 'ملخص انتشر',
         '<b>40,100 views and 1,170 saves</b>: six rules of C++ in 30 seconds, right before exams.',
         '<b>40,100 مشاهدة و1,170 حفظ</b>: ست قواعد في C++ خلال 30 ثانية، قبل الامتحانات مباشرة.'),
        ('reels/r1_2.jpg', 'The opening of C++ in a minute', 'افتتاحية فيديو C++ بدقيقة',
         'c++ in a minute', 'C++ بدقيقة', 'One hook, fast scenes', 'افتتاحية واحدة ومشاهد سريعة',
         'An animated picture for each idea and captions word by word. <b>112,700 views and 3,616 saves.</b>',
         'صورة متحركة لكل فكرة وترجمة كلمة بكلمة. <b>112,700 مشاهدة و3,616 حفظ.</b>'),
        ('reels/r1_8.jpg', 'A scene about cout and cin', 'مشهد عن cout و cin',
         'two voices', 'صوتان', 'Two voices, one for code', 'صوتان، أحدهما للكود',
         'The first cut read code words badly. The fix: Arabic voice for the idea, an English voice for each code word.',
         'النسخة الأولى نطقت كلمات الكود بشكل سيئ. الحل: صوت عربي للفكرة، وصوت إنجليزي لكل كلمة كود.'),
    ],
    body=lambda: (
        section('films', 'Three reels to watch', 'ثلاثة فيديوهات للمشاهدة',
                'Sound on: the voice is Arabic, the code words in English.',
                'شغّل الصوت: التعليق بالعربية وكلمات الكود بالإنجليزية.',
                '<ul class="films" data-reveal="stagger">'
                + ''.join(
                    f'<li><video controls preload="none" playsinline poster="../img/reels/{poster}" aria-label="{a(en)}" data-ar-aria="{a(ar)}"><source src="../media/{src}" type="video/mp4"></video>'
                    f'<h3 data-ar="{a(ar)}">{en}</h3><p data-ar="{a(n_ar)}">{n}</p></li>'
                    for src, poster, en, ar, n, n_ar in [
                        ('cpp-in-a-minute.mp4', 'r1_2.jpg', 'C++ in a minute', 'C++ بدقيقة', '112,700 views · 3,616 saves', '112,700 مشاهدة · 3,616 حفظ'),
                        ('cpp-cheat-sheet.mp4', 'r2_2.jpg', 'C++ cheat sheet in 30 seconds', 'ملخص C++ بـ 30 ثانية', '40,100 views · 1,170 saves', '40,100 مشاهدة · 1,170 حفظ'),
                        ('i-plus-plus.mp4', 'r3_2.jpg', 'i++ or ++i', 'i++ أم ++i', '6,300 views · 131 shares', '6,300 مشاهدة · 131 مشاركة')])
                + '</ul>')
        + section('numbers', 'The numbers on the page', 'أرقام الصفحة',
                  'From Instagram insights on 25 November 2026.', 'من إحصائيات إنستغرام في 25 نوفمبر 2026.',
                  '<dl class="numbers" data-reveal="stagger">'
                  + ''.join(f'<div><dt data-ar="{a(l_ar)}">{l}</dt><dd>{v}</dd></div>' for l, l_ar, v in [
                      ('Best reel, views', 'أفضل فيديو، مشاهدات', '112,700'),
                      ('Saves on it', 'الحفظ عليه', '3,616'),
                      ('Follows from it', 'المتابعات منه', '1,245'),
                      ('Followers now', 'المتابعون الآن', '1,955')])
                  + '</dl>')
    ),
    next=('wasla', 'Wasla', 'وَصلة'),
))

P.append(dict(
    slug='wasla', pc='#c8f560', cover='cover-wasla.jpg',
    title='Wasla: brand identity for a design and app studio, by Amer AL Dalaq',
    title_ar='وَصلة: هوية بصرية لاستوديو تصميم وتطبيقات، من عامر الدلق',
    desc='Name, mark, colours and type for wasla, the studio Amer AL Dalaq sells design, apps and websites through.',
    desc_ar='الاسم والعلامة والألوان والخطوط لوَصلة، الاستوديو الذي يقدّم عبره عامر الدلق خدمات التصميم والتطبيقات والمواقع.',
    tag='Solo project · Brand identity · 2026', tag_ar='مشروع فردي · هوية بصرية · 2026',
    h1='Wasla, a brand for my design studio', h1_ar='وَصلة، هوية لاستوديو التصميم الخاص بي',
    lead='One name and one mark for selling design, apps and websites, in Arabic and English. Wasla means "a link": from the idea to a product that works.',
    lead_ar='اسم واحد وعلامة واحدة لبيع التصميم والتطبيقات والمواقع، بالعربية والإنجليزية. وَصلة تعني الرابط: من الفكرة إلى منتج يعمل.',
    facts=[('My role', 'دوري', 'Name, logo, colours, first reel', 'الاسم والشعار والألوان وأول فيديو'),
           ('Year', 'السنة', '2026', '2026'),
           ('Page', 'الصفحة', 'Instagram @wasla.j', 'إنستغرام @wasla.j')],
    cover_alt='The wasla mark: a hollow dot joined by a curve to a full dot', cover_alt_ar='علامة وَصلة: نقطة مفرغة يصلها منحنى بنقطة ممتلئة',
    story_h='The idea behind the mark', story_h_ar='الفكرة خلف العلامة',
    story=[('The problem', 'المشكلة',
            'I needed a name clients could say in Arabic and English, and a mark that still reads at the size of an Instagram profile picture.',
            'احتجت اسماً يقوله العميل بالعربية والإنجليزية، وعلامة تبقى واضحة بحجم صورة الملف الشخصي في إنستغرام.'),
           ('The fix', 'الحل',
            'The mark is a hollow dot, the idea, joined by one curve to a full dot, the finished product. Ink #0E1116, paper #F4F2EC and one lime, #C8F560. IBM Plex Mono for English, Noto Sans Arabic for Arabic.',
            'العلامة نقطة مفرغة هي الفكرة، يصلها منحنى واحد بنقطة ممتلئة هي المنتج النهائي. الحبر ‎#0E1116 والورق ‎#F4F2EC ولون ليموني واحد ‎#C8F560. خط IBM Plex Mono للإنجليزية وNoto Sans Arabic للعربية.')],
    story_pic=('wasla/wasla-profile.jpg', 'The wasla profile picture: the mark in lime on ink', 'صورة ملف وَصلة: العلامة باللون الليموني على الحبر', '1 / 1', '50% 50%'),
    tools=['react', 'claude'],
    body=lambda: (
        section('logo', 'The logo on dark and light', 'الشعار على الداكن والفاتح', '', '',
                wide([('wasla/wasla-logo-dark.jpg', 'The wasla logo on ink with the line design, apps, web', 'شعار وَصلة على الحبر مع سطر تصميم وتطبيقات وويب'),
                      ('wasla/wasla-logo-light.jpg', 'The wasla logo on paper', 'شعار وَصلة على الورق')]))
        + section('reel', 'The first reel', 'أول فيديو',
                  'A 17-second reel for the launch, with Bug Hunter as the proof project.',
                  'فيديو من 17 ثانية للإطلاق، وBug Hunter فيه مثال على شغلي.',
                  '<ul class="films"><li><video controls preload="none" playsinline poster="../img/wasla/wasla-profile.jpg" aria-label="The first wasla reel" data-ar-aria="أول فيديو لوَصلة"><source src="../media/wasla-reel-1.mp4" type="video/mp4"></video></li></ul>')
    ),
    next=('masar', 'Masar', 'مسار'),
))

M = lambda n, e, r: (f'masar/{n}.jpg', e, r)
P.append(dict(
    slug='masar', pc='#44bfb7', cover='cover-masar.jpg',
    title='Masar: a study app from the JORDAN.NEXT() hackathon, with Amer AL Dalaq',
    title_ar='مسار: تطبيق مذاكرة من هاكاثون JORDAN.NEXT()، بمشاركة عامر الدلق',
    desc='A team of three built Masar, an adaptive study app for university students. Amer made its colour system, dark mode, mentor welcome and profile screens.',
    desc_ar='بنى فريق من ثلاثة تطبيق مسار للمذاكرة التكيّفية لطلاب الجامعات. صمّم عامر نظام الألوان والوضع الداكن وشاشة ترحيب المرشد والملف الشخصي.',
    tag='Team of 3 · Hackathon · 2026', tag_ar='فريق من 3 · هاكاثون · 2026',
    h1='Masar, a study app for university exams', h1_ar='مسار، تطبيق مذاكرة لامتحانات الجامعة',
    lead='Built with two teammates for the JORDAN.NEXT() hackathon, Education track. A short test maps what a student knows, and a daily plan targets the topics that appear most in real past exams.',
    lead_ar='بنيته مع زميلين في هاكاثون JORDAN.NEXT() ضمن مسار التعليم. اختبار قصير يرسم ما يعرفه الطالب، وخطة يومية تركّز على المواضيع الأكثر تكراراً في امتحانات سابقة حقيقية.',
    facts=[('My part', 'دوري', 'Colours, dark mode, mentor and profile screens', 'الألوان والوضع الداكن وشاشتا المرشد والملف الشخصي'),
           ('Year', 'السنة', '2026', '2026'),
           ('Team', 'الفريق', 'Three students', 'ثلاثة طلاب')],
    cover_alt='Masar home, mentor and profile screens', cover_alt_ar='شاشات الرئيسية والمرشد والملف الشخصي في مسار',
    story_h='The problem and my part', story_h_ar='المشكلة ودوري',
    story=[('The problem', 'المشكلة',
            'Students revise everything the same way, without knowing which topics their exam really asks about.',
            'يراجع الطلاب كل شيء بالطريقة نفسها، دون أن يعرفوا أي المواضيع يسأل عنها امتحانهم فعلاً.'),
           ('The team’s answer', 'حل الفريق',
            'A readiness score per topic, a daily plan weighted by real past papers, and Rafeeq, a mentor who explains a concept after two wrong answers.',
            'نسبة جاهزية لكل موضوع، وخطة يومية مبنية على امتحانات سابقة حقيقية، ورفيق: مرشد يشرح المفهوم بعد خطأين.'),
           ('What I made', 'ما صمّمته',
            'The colour system, navy #24477B and teal #44BFB7, with a full dark mode; Rafeeq’s welcome screen with four suggested questions; and the profile with stats, mastery and the appearance setting.',
            'نظام الألوان، الكحلي ‎#24477B والتركوازي ‎#44BFB7، مع وضع داكن كامل؛ وشاشة ترحيب رفيق مع أربعة أسئلة مقترحة؛ والملف الشخصي بالإحصائيات والإتقان وإعداد المظهر.')],
    story_pic=('masar/08.jpg', 'Rafeeq’s welcome screen in dark mode', 'شاشة ترحيب رفيق في الوضع الداكن', '9 / 19.5', '50% 0%'),
    tools=['flutter', 'figma', 'claude'],
    s3_h='Masar, screen by screen', s3_h_ar='مسار، شاشة شاشة',
    steps=[
        ('masar/02.jpg', 'Onboarding: name, subject and exam date', 'البداية: الاسم والمادة وموعد الامتحان',
         'onboarding', 'البداية', 'Three questions to start', 'ثلاثة أسئلة للبداية',
         'Name, subject and exam date. Then eight short questions find where the student stands.',
         'الاسم والمادة وموعد الامتحان. ثم ثمانية أسئلة قصيرة تحدد أين يقف الطالب.'),
        ('masar/04.jpg', 'The diagnostic with instant feedback', 'التشخيص مع تصحيح فوري',
         'diagnostic', 'التشخيص', 'Feedback on every answer', 'تصحيح فوري لكل إجابة',
         'Wrong in red, right in green, and the readiness score moves at once: <b>+4%</b>.',
         'الخطأ بالأحمر والصح بالأخضر، ونسبة الجاهزية تتحرك فوراً: <b>+4%</b>.'),
        ('masar/05.jpg', 'The concept map with readiness per topic', 'خريطة المفاهيم مع الجاهزية لكل موضوع',
         'map', 'الخريطة', 'Topics weighted by real exams', 'مواضيع مرتّبة حسب الامتحانات الحقيقية',
         'Each topic shows how often it appears in past papers, so the weak and frequent ones come first.',
         'كل موضوع يُظهر كم يتكرر في الامتحانات السابقة، فتأتي المواضيع الضعيفة والمتكررة أولاً.'),
        ('masar/06.jpg', 'Home: today’s plan', 'الرئيسية: خطة اليوم',
         'home', 'الرئيسية', 'A plan for today', 'خطة لليوم',
         '16 minutes, 12 questions, on the three topics that matter most before the exam.',
         '16 دقيقة و12 سؤالاً، على المواضيع الثلاثة الأهم قبل الامتحان.'),
        ('masar/08.jpg', 'Rafeeq welcome, dark', 'ترحيب رفيق، داكن',
         'rafeeq · my screen', 'رفيق · من تصميمي', 'Rafeeq says hello', 'رفيق يرحّب',
         'I designed the mentor’s welcome: a big avatar over a teal glow and <b>four suggested questions</b> to start a chat.',
         'صمّمت ترحيب المرشد: صورة كبيرة فوق توهّج تركوازي و<b>أربعة أسئلة مقترحة</b> لبدء المحادثة.'),
        ('masar/10.jpg', 'Profile stats, dark', 'إحصائيات الملف، داكن',
         'profile · my screen', 'الملف · من تصميمي', 'The profile in numbers', 'الملف الشخصي بالأرقام',
         'Readiness, strong topics, answers so far and days to the exam, with a mastery bar from weak to strong.',
         'الجاهزية والمواضيع القوية والإجابات حتى الآن والأيام حتى الامتحان، مع شريط إتقان من الضعيف للقوي.'),
        ('masar/12.jpg', 'Profile, light', 'الملف الشخصي، فاتح',
         'colours · my system', 'الألوان · من تصميمي', 'Dark and light, one system', 'داكن وفاتح بنظام واحد',
         'Navy <b>#24477B</b> and teal <b>#44BFB7</b>, with a full dark mode that switches every screen at once.',
         'كحلي <b>#24477B</b> وتركوازي <b>#44BFB7</b>، مع وضع داكن كامل يبدّل كل الشاشات مرة واحدة.'),
    ],
    body=lambda: '',
    next=('travel-jo', 'Travel JO', 'Travel JO'),
))

T = lambda n, e, r: (f'travel-jo/{n}.jpg', e, r)
P.append(dict(
    slug='travel-jo', pc='#2ec4c9', cover='cover-travel-jo.jpg',
    title='Travel JO: a tourism app for Jordan, designed by Amer AL Dalaq',
    title_ar='Travel JO: تطبيق سياحي للأردن صمّمه عامر الدلق',
    desc='A learning project in Figma: a tourism app for Jordan in Arabic, English and French, with places, car rental, tour guides and payment.',
    desc_ar='مشروع تعلّم في Figma: تطبيق سياحي للأردن بالعربية والإنجليزية والفرنسية، فيه الأماكن وتأجير السيارات والمرشدون والدفع.',
    tag='Solo learning project · Figma', tag_ar='مشروع تعلّم فردي · Figma',
    h1='Travel JO, a tourism app for Jordan', h1_ar='Travel JO، تطبيق سياحي للأردن',
    lead='My first big Figma file, designed over eight months: places like Petra and Wadi Mujib, car rental offices, tour guides and payment, in Arabic, English and French.',
    lead_ar='أول ملف كبير لي في Figma، صمّمته على مدى ثمانية أشهر: أماكن مثل البتراء ووادي الموجب، ومكاتب تأجير السيارات، والمرشدون، والدفع، بالعربية والإنجليزية والفرنسية.',
    facts=[('My role', 'دوري', 'Every screen', 'كل الشاشات'),
           ('Length', 'المدة', 'About eight months', 'نحو ثمانية أشهر'),
           ('Frames', 'الإطارات', '221 in one file', '221 في ملف واحد')],
    cover_alt='Travel JO welcome screen over Petra, the Petra page and a list of places', cover_alt_ar='شاشة ترحيب Travel JO فوق البتراء، وصفحة البتراء، وقائمة أماكن',
    story_h='What I was trying to solve', story_h_ar='ما حاولت حلّه',
    story=[('The problem', 'المشكلة',
            'A visitor to Jordan jumps between sites to read about a place, rent a car and find a guide.',
            'زائر الأردن يتنقّل بين مواقع كثيرة ليقرأ عن مكان ويستأجر سيارة ويجد مرشداً.'),
           ('The idea', 'الفكرة',
            'One app for all three, in the visitor’s language: each place with its story and photographs, rental offices with their cars, guides, saved trips and payment.',
            'تطبيق واحد للثلاثة، بلغة الزائر: كل مكان بقصته وصوره، ومكاتب التأجير بسياراتها، والمرشدون، والرحلات المحفوظة، والدفع.'),
           ('What I learned', 'ما تعلّمته',
            'It is an early style, teal and busy. Working on it taught me frames, components and three-language layouts, and why a design system has to come first.',
            'أسلوبه مبكر، تركوازي ومزدحم. لكنه علّمني الإطارات والمكوّنات وتخطيط ثلاث لغات، ولماذا يجب أن يأتي نظام التصميم أولاً.')],
    story_pic=('travel-jo/board.jpg', 'The whole Travel JO Figma board with all 221 frames', 'لوحة Travel JO كاملة في Figma بإطاراتها الـ 221', '1 / 2', '50% 30%'),
    tools=['figma'],
    s3_h='Travel JO, screen by screen', s3_h_ar='Travel JO، شاشة شاشة',
    steps=[
        ('travel-jo/001.jpg', 'Welcome screen over Petra', 'شاشة الترحيب فوق البتراء',
         'welcome', 'الترحيب', 'Petra as the front door', 'البتراء كباب الدخول',
         'The app opens on the Treasury with the Jordanian flag in the logo, then sign in or sign up.',
         'يفتح التطبيق على الخزنة مع علم الأردن في الشعار، ثم تسجيل الدخول أو إنشاء حساب.'),
        ('travel-jo/012.jpg', 'The Petra page in Arabic', 'صفحة البتراء بالعربية',
         'place · ar', 'مكان · عربي', 'Every place tells its story', 'كل مكان يحكي قصته',
         'Photographs, history and reviews for each place, here Petra in Arabic.',
         'صور وتاريخ ومراجعات لكل مكان، وهنا البتراء بالعربية.'),
        ('travel-jo/017.jpg', 'The Petra page in French', 'صفحة البتراء بالفرنسية',
         'place · fr', 'مكان · فرنسي', 'The same page in French', 'الصفحة نفسها بالفرنسية',
         'Three languages, Arabic, English and French, each laid out for its own direction and length.',
         'ثلاث لغات، العربية والإنجليزية والفرنسية، لكل منها تخطيط يناسب اتجاهها وطولها.'),
        ('travel-jo/038.jpg', 'Places in virtual reality', 'الأماكن بالواقع الافتراضي',
         'places', 'الأماكن', 'Places to visit', 'أماكن للزيارة',
         'Umm Qais, Downtown Amman, Mount Nebo, Ma’in, Wadi Mujib: a list to explore before the trip.',
         'أم قيس ووسط عمّان وجبل نيبو وماعين ووادي الموجب: قائمة لاستكشافها قبل الرحلة.'),
        ('travel-jo/013.jpg', 'A car rental office', 'مكتب تأجير سيارات',
         'cars', 'السيارات', 'Rent a car in the same app', 'استأجر سيارة من التطبيق نفسه',
         'Rental offices with their photographs, cars and location, without leaving the trip.',
         'مكاتب التأجير بصورها وسياراتها وموقعها، دون أن تترك رحلتك.'),
        ('travel-jo/049.jpg', 'Tour guides', 'المرشدون السياحيون',
         'guides', 'المرشدون', 'Find a tour guide', 'جد مرشداً سياحياً',
         'A list of guides with the places they cover, ready to book.',
         'قائمة مرشدين مع الأماكن التي يغطونها، جاهزة للحجز.'),
        ('travel-jo/069.jpg', 'Settings and help', 'الإعدادات والمساعدة',
         'settings', 'الإعدادات', 'Settings, language and help', 'الإعدادات واللغة والمساعدة',
         'Saved trips, bookings, the language switch and a help centre with chat and WhatsApp.',
         'الرحلات المحفوظة والحجوزات وتبديل اللغة ومركز مساعدة بالمحادثة وواتساب.'),
    ],
    body=lambda: (
        section('board', 'The whole file', 'الملف كاملاً',
                'All 221 frames in one Figma page.', 'كل الإطارات الـ 221 في صفحة واحدة في Figma.',
                wide([('travel-jo/board.jpg', 'The whole Travel JO Figma board with all 221 frames', 'لوحة Travel JO كاملة في Figma بإطاراتها الـ 221')], one=True))
    ),
    next=('bug-hunter', 'Bug Hunter', 'Bug Hunter'),
))


def build(p):
    out = HEAD.format(pc=p.get('pc', '#f2a93b'), title=a(p['title']), title_ar=a(p['title_ar']), desc=a(p['desc']), desc_ar=a(p['desc_ar']),
                      cover=p['cover'], mail=MAIL)
    out += hero(p) + (story3d(p) if p.get('steps') else story(p)) + p['body']() + nxt(p)
    out += FOOT.format(mail=MAIL, arrow=ARROW, slug=p['slug'])
    os.makedirs(os.path.join(ROOT, 'work'), exist_ok=True)
    # Latin code words inside Arabic text keep their own direction (C++ never shows as ++C)
    out = re.sub(r'(data-ar(?:-[a-z]+)?="[^"]*")', lambda m: m.group(1).replace('C++', '⁦C++⁩'), out)
    with open(os.path.join(ROOT, 'work', p['slug'] + '.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)


for p in P:
    build(p)
print('built', len(P), 'pages')
