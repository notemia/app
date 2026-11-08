#!/usr/bin/env python3
"""Builds the one-page snowboard site (one page per language) from lang_*.py and docs_*.py.

Run:  python3 snowboard/_src/build.py   (from the notemia-app repo root)
Course names, level names and lesson names come from the app's own string
catalog, so the site always says exactly what the app says.
"""
import html, json, importlib, os, re, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)                    # .../snowboard
ROOT = os.path.dirname(SITE)                    # repo root
CATALOG = os.environ.get('SNOWBOARD_XCSTRINGS',
    '/Users/vladimir/claude/SnowboardFeelTheTurn/SnowboardFeelTheTurn/Localization/Localizable.xcstrings')
sys.path.insert(0, HERE)

# code -> (folder, hreflang, og:locale, app catalog key, native name)
LANGS = [
    ('en', '',     'en',      'en_US', 'en',      'English'),
    ('ru', 'ru/',  'ru',      'ru_RU', 'ru',      'Русский'),
    ('de', 'de/',  'de',      'de_DE', 'de',      'Deutsch'),
    ('es', 'es/',  'es',      'es_ES', 'es',      'Español'),
    ('fr', 'fr/',  'fr',      'fr_FR', 'fr',      'Français'),
    ('it', 'it/',  'it',      'it_IT', 'it',      'Italiano'),
    ('ja', 'ja/',  'ja',      'ja_JP', 'ja',      '日本語'),
    ('ko', 'ko/',  'ko',      'ko_KR', 'ko',      '한국어'),
    ('zh', 'zh/',  'zh-Hans', 'zh_CN', 'zh-Hans', '简体中文'),
]
BASE = 'https://notemia.app/snowboard/'
STR = json.load(open(CATALOG, encoding='utf-8'))['strings']

def app(key, ck):
    return STR[key]['localizations'][ck]['stringUnit']['value']

COURSES = [('longRun', 'course-long-run'), ('pyramid', 'course-pyramid'), ('parkPipe', 'course-park-pipe'),
           ('powderGlades', 'course-powder-glades'), ('couloir', 'course-couloir')]
LEVELS = [('level.safety', [17, 18]), ('level1', [11, 10, 2]), ('level2', [12, 6]), ('level.lifts', [20, 21]),
          ('level3', [1, 13, 4, 8, 19]), ('level4', [5, 14, 7, 15]), ('level5', [3, 9, 22, 23, 16])]
assert sum(len(l) for _, l in LEVELS) == 23

e = lambda s: html.escape(s, quote=False)
a = lambda s: html.escape(s, quote=True)

RANGE = """<svg class="range" viewBox="0 0 900 420" aria-hidden="true">
  <path fill="#a873b9" d="M0 420 120 215l100 85 110-65 100 85h470v100z"/>
  <path fill="#ffe6da" d="m120 215-38 27 24-4 14 22 12-20 26 8z"/>
  <path fill="#6a55b5" d="M190 420 560 24l340 356v40z"/>
  <path fill="#2b2a7c" d="m560 24 66 112-26 96 96 62 204 86v40H470l70-130-16-84z"/>
  <path fill="#9497de" d="m560 24 44 64 16 74 22-36 50 52z" />
  <path fill="#ffe6da" d="m560 24-92 99 36-12 16 60 32-64 24 44 28-66z"/>
</svg>"""

def fit(word, code):
    """Viewport-relative size that makes the product name fill the line, in any script."""
    per_char = 1.02 if code in ('ja', 'ko', 'zh') else 0.385
    return round(92 / (len(word) * per_char), 1)

def details(summary, inner):
    return f'<details><summary>{summary}</summary>{inner}</details>'

def build(code, folder, hl, ogl, ck, native, d, P, S):
    url = BASE + folder
    alt = ''.join(f'<link rel="alternate" hreflang="{h}" href="{BASE}{f}">\n' for _, f, h, *_ in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{BASE}">\n'
    og_img = BASE + f'assets/og-{code}.jpg'
    MAIL = 'mailto:helpyoutofeel@gmail.com'
    mail = MAIL + '?subject=' + urllib.parse.quote(d['notify_subject'], safe='')
    shot = lambda n: f'/snowboard/assets/shots/{code}/{n:02d}.webp'
    name = re.sub(r'[\s:：]+$', '', d['h1a'])
    ld = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": hl, "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in S['faq']]}
    app_ld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": "Snowboarding",
              "alternateName": "Snowboarding: Lessons & Game", "url": url, "inLanguage": hl, "description": d['desc'],
              "applicationSubCategory": "Snowboarding lessons and riding game", "operatingSystem": "iOS 18 or later",
              "applicationCategory": "SportsApplication", "image": BASE + "assets/icon.png",
              "screenshot": [BASE + "assets/game.jpg", BASE + f"assets/shots/{code}/01.webp"],
              "author": {"@type": "Person", "name": "Vladimir Dyagay"}}
    courses = ''.join(
        f'<figure><img src="/snowboard/assets/{img}.jpg" alt="{a(t)}" width="720" height="1080" loading="lazy">'
        f'<figcaption><span>{e(app(f"mountain.{key}.place", ck))}</span><strong>{e(app(f"mountain.{key}.run", ck))}</strong>'
        f'{e(app(f"mountain.{key}.focus", ck))}</figcaption></figure>'
        for (key, img), t in zip(COURSES, d['courses_alt']))
    levels = ''.join(
        details(f'<b class="pole">{i}</b><span><strong>{e(app(stem + ".title", ck))}</strong>{e(app(stem + ".goal", ck))}</span>',
                '<ol>' + ''.join(f'<li>{e(app(f"lesson{n}.skill", ck))}</li>' for n in lessons) + '</ol>')
        for i, (stem, lessons) in enumerate(LEVELS, 1))
    contact = ''.join(
        f'<p><strong>{e(h)}</strong>{e(p)}</p><a class="btn {c}" href="{a(MAIL + "?subject=" + urllib.parse.quote(sub, safe=""))}">{e(b)}</a>'
        for (h, p, b, sub), c in zip(S['cards'], ('', 'line')))
    faq = ''.join(details(e(q), f'<p>{e(t)}</p>') for q, t in S['faq'])
    policy = ''.join(details(e(h), f'<p>{e(p)}</p>') for h, p in P['sections'])
    return f"""<!doctype html>
<html lang="{hl}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(d['title'])}</title>
<meta name="description" content="{a(d['desc'])}">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#141a5e">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Snowboarding">
<meta property="og:title" content="{a(d['title'])}">
<meta property="og:description" content="{a(d['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{ogl}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/snowboard/assets/icon-64.png" type="image/png">
<link rel="apple-touch-icon" href="/snowboard/assets/icon-180.png">
<link rel="stylesheet" href="/snowboard/style.css">
<script type="application/ld+json">{ld(app_ld)}</script>
<script type="application/ld+json">{ld(faq_ld)}</script>
</head>
<body>
<header class="top">
  <a class="brand" href="/snowboard/{folder}"><img src="/snowboard/assets/icon-64.png" alt="" width="32" height="32">Snowboarding</a>
  <nav><a href="#game">{e(d['nav_game'])}</a><a href="#lessons">{e(d['nav_lessons'])}</a><a href="#support">{e(d['foot_support'])}</a><a href="#privacy">{e(d['foot_privacy'])}</a>
  <details class="langs"><summary aria-label="{a(d['lang_label'])}">{e(native)}</summary><div>{lang_menu(code)}</div></details></nav>
</header>

<main>
<div class="hero">
  <h1><span style="--fit:{fit(name, code)}vw">{e(name)}</span>{e(d['h1b'])}</h1>
  <div class="pitch">
    <p>{e(d['sub'])}</p>
    <a class="btn" href="{a(mail)}">{e(d['cta2'])}</a>
    <p class="soon">{e(d['soon'])}</p>
  </div>
  {RANGE}
  <svg class="hill" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 80V44C260-6 520 4 760 26s460 34 680-8v62z"/></svg>
</div>

<div class="run" id="run">
<section class="gate r" id="game"><div class="in play">
  <div><h2>{e(d['m_h2'])}</h2><p>{e(d['m_lead'])}</p><p class="quiet">{e(d['m_note'])}</p></div>
  <video data-loop muted loop playsinline preload="metadata" poster="/snowboard/assets/game.jpg" aria-label="{a(d['hero_aria'])}" width="640" height="1390"><source src="/snowboard/assets/game.mp4" type="video/mp4"></video>
</div></section>
<div class="courses" tabindex="0" aria-label="{a(d['m_h2'])}">{courses}</div>

<section class="gate l" id="lessons"><div class="in">
  <h2>{e(d['l_h2'])}</h2><p>{e(d['l_lead'])}</p>
  <div class="shots"><img src="{shot(1)}" alt="{a(d['watch_aria'])}" width="660" height="1434" loading="lazy"><img src="{shot(6)}" alt="{a(d['early_alt'])}" width="660" height="1434" loading="lazy"></div>
</div></section>

<section class="gate r"><div class="in">
  <h2>{e(d['c_h2'])}</h2><p>{e(d['c_lead'])}</p>
  <div class="levels">{levels}</div>
</div></section>

<section class="gate l"><div class="in">
  <h2>{e(d['pb'][0])}</h2>
  <ul class="limits">{''.join(f'<li>{e(x)}</li>' for x in d['pb'][1])}</ul>
</div></section>

<section class="gate r finish"><div class="in">
  <h2>{e(d['end_h2'])}</h2><p>{e(d['end_p'])}</p>
  <a class="btn" href="{a(mail)}">{e(d['cta2'])}</a>
</div></section>
</div>

<div class="base">
  <section id="support">
    <h2>{e(d['foot_support'])}</h2><p class="quiet">{e(S['sub'])}</p>
    <div class="contact">{contact}</div>
    <div class="rows">{faq}</div>
  </section>
  <section id="privacy">
    <h2>{e(P['h1'])}</h2><p class="quiet">{e(P['sub'])}</p>
    <p class="short"><strong>{e(P['short_label'])}</strong> {e(P['short'])}</p>
    <div class="rows">{policy}{details(e(P['contact_h']), f'<p><a href="{MAIL}">helpyoutofeel@gmail.com</a></p>')}</div>
  </section>
</div>
</main>

<footer>
  <small>{e(d['foot'])}<br>© 2026 Vladimir Dyagay</small>
  <nav><a href="/">Notemia apps</a><a href="{MAIL}">helpyoutofeel@gmail.com</a></nav>
</footer>
<script src="/snowboard/app.js"></script>
</body>
</html>
"""

def check(code, d):
    need = ['title','desc','lang_label','nav_game','nav_lessons','h1a','h1b','sub','cta2','notify_subject','soon','hero_aria',
            'm_h2','m_lead','courses_alt','m_note','l_h2','l_lead','watch_aria','early_alt','c_h2','c_lead','pb','end_h2','end_p','foot','foot_support','foot_privacy']
    miss = [k for k in need if k not in d]
    assert not miss, (code, miss)
    assert len(d['courses_alt']) == 5 and len(d['pb'][1]) == 5

def lang_menu(code):
    return ''.join(f'<a href="/snowboard/{f2}" hreflang="{h2}" lang="{h2}"' + (' aria-current="true"' if c2 == code else '') + f'>{n2}</a>'
                   for c2, f2, h2, _o, _k, n2 in LANGS)

def stub(folder, anchor):
    """Old privacy.html / support.html addresses stay valid: App Store Connect links to them."""
    target = f'/snowboard/{folder}#{anchor}'
    return f"""<!doctype html>
<meta charset="utf-8">
<title>Snowboarding</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}{folder}">
<meta http-equiv="refresh" content="0; url={target}">
<a href="{target}">Snowboarding: {anchor}</a>
"""

def check_doc(code, P, S):
    for k in ['h1','sub','short_label','short','sections','contact_h']:
        assert k in P, (code, 'P', k)
    assert len(P['sections']) == 7, (code, len(P['sections']))
    for k in ['sub','cards','faq']:
        assert k in S, (code, 'S', k)
    assert len(S['cards']) == 2 and len(S['faq']) == 13, (code, len(S['faq']))

def main():
    for code, folder, hl, ogl, ck, native in LANGS:
        d = importlib.import_module('lang_' + code).D
        dm = importlib.import_module('docs_' + code)
        check(code, d)
        check_doc(code, dm.P, dm.S)
        out = os.path.join(SITE, folder, 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(build(code, folder, hl, ogl, ck, native, d, dm.P, dm.S))
        for anchor in ('privacy', 'support'):
            open(os.path.join(SITE, folder, anchor + '.html'), 'w', encoding='utf-8').write(stub(folder, anchor))
        print('wrote', os.path.relpath(out, ROOT))
    alts = ''.join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{BASE}{f}"/>\n' for _, f, h, *_ in LANGS) + f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>\n'
    blocks = ''.join(f'  <url><loc>{BASE}{f}</loc>\n{alts}  </url>\n' for _, f, *_ in LANGS)
    p = os.path.join(ROOT, 'sitemap.xml')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'  <url><loc>https://notemia.app/snowboard/(?:[a-z]{2}/)?(?:privacy\.html|support\.html)?</loc>.*?</url>\n', '', s, flags=re.S)
    s = s.replace('  <url><loc>https://notemia.app/support.html</loc></url>\n', blocks + '  <url><loc>https://notemia.app/support.html</loc></url>\n')
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    main()
