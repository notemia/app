#!/usr/bin/env python3
"""Builds the snowboard landing pages (one per language) from lang_*.py content.

Run:  python3 snowboard/_src/build.py   (from the notemia-app repo root)
Course names, level names and lesson names come from the app's own string
catalog, so the site always says exactly what the app says.
"""
import html, json, importlib, os, sys, urllib.parse

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

def build(code, folder, hl, ogl, ck, native, d):
    url = BASE + folder
    alt = ''.join(f'<link rel="alternate" hreflang="{h}" href="{BASE}{f}">\n' for _, f, h, *_ in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{BASE}">\n'
    og_img = BASE + f'assets/og-{code}.jpg'
    mail = 'mailto:helpyoutofeel@gmail.com?subject=' + urllib.parse.quote(d['notify_subject'], safe='')
    ru = code == 'ru'
    shot = lambda n: f'/snowboard/assets/shots/{code}/{n:02d}.webp'
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": hl, "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in d['faq']]}
    app_ld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": "Snowboarding",
              "alternateName": "Snowboarding: Lessons & Game",
              "url": url, "inLanguage": hl, "description": d['desc'],
              "applicationSubCategory": "Snowboarding lessons and riding game", "operatingSystem": "iOS 18 or later",
              "applicationCategory": "SportsApplication", "image": BASE + "assets/icon.png",
              "screenshot": [BASE + "assets/game.jpg", BASE + f"assets/shots/{code}/01.webp"],
              "author": {"@type": "Person", "name": "Vladimir Dyagay"}}
    ld = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
    P = []
    w = P.append
    w(f'''<!doctype html>
<html lang="{hl}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(d['title'])}</title>
<meta name="description" content="{a(d['desc'])}">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#17243d">
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
<header class="top"><div class="wrap">
  <a class="brand" href="/snowboard/{folder}"><img src="/snowboard/assets/icon-64.png" alt="" width="36" height="36">Snowboarding</a>
  <nav><a href="#mountain">{e(d['nav_game'])}</a><a href="#lessons">{e(d['nav_lessons'])}</a><a href="#faq">{e(d['nav_faq'])}</a>
  <details class="langs"><summary class="lang" aria-label="{a(d['lang_label'])}">{e(native)}</summary><div class="langs-list">{lang_menu(code, '')}</div></details></nav>
</div></header>

<main>
<div class="hero">
  <svg class="track" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" fill="none">
  <path d="M1180 -40 C 1460 120 1500 250 1180 330 C 820 420 820 520 1100 610 C 1340 690 1270 830 1010 960" stroke="#fff" stroke-opacity=".09" stroke-width="58" stroke-linecap="round"/>
  <path d="M1180 -40 C 1460 120 1500 250 1180 330 C 820 420 820 520 1100 610 C 1340 690 1270 830 1010 960" stroke="#fff" stroke-opacity=".2" stroke-width="2"/>
</svg>
  <div class="wrap hero-grid">
    <div>
      <h1>{e(d['h1a'])}<br><em>{e(d['h1b'])}</em></h1>
      <p class="sub">{e(d['sub'])}</p>
      <div class="cta"><a class="btn btn-primary" href="#mountain">{e(d['cta1'])}</a><a class="btn btn-ghost" href="{a(mail)}">{e(d['cta2'])}</a></div>
      <p class="soon">{e(d['soon'])}</p>
      <ul class="facts">{''.join(f'<li><b>{e(b)}</b><span>{e(s)}</span></li>' for b, s in d['facts'])}</ul>
    </div>
    <div class="phone-col">
      <div class="phone"><video data-loop muted loop playsinline preload="metadata" poster="/snowboard/assets/game.jpg" aria-label="{a(d['hero_aria'])}" width="640" height="1390"><source src="/snowboard/assets/game.mp4" type="video/mp4"></video></div>
    </div>
  </div>
</div>

<section class="mountain" id="mountain">
  <div class="wrap">
    <p class="eyebrow">{e(d['m_eyebrow'])}</p>
    <h2>{e(d['m_h2'])}</h2>
    <p class="lead">{e(d['m_lead'])}</p>
  </div>
  <div class="courses" tabindex="0">''')
    figs = []
    for (key, img), alt_t in zip(COURSES, d['courses_alt']):
        figs.append(f'<figure class="course"><img src="/snowboard/assets/{img}.jpg" alt="{a(alt_t)}" width="720" height="1080" loading="lazy">\n'
                    f'        <figcaption><span>{e(app(f"mountain.{key}.place", ck))}</span><strong>{e(app(f"mountain.{key}.run", ck))}</strong><em>{e(app(f"mountain.{key}.focus", ck))}</em></figcaption></figure>')
    w(''.join(figs) + '</div>')
    w(f'''
  <div class="wrap">
    <ul class="moves">{''.join(f'<li><h3>{e(h)}</h3><p>{e(p)}</p></li>' for h, p in d['moves'])}</ul>
    <p class="note">{e(d['m_note'])}</p>
  </div>
</section>

<section><div class="wrap">
  <p class="eyebrow">{e(d['l_eyebrow'])}</p>
  <h2>{e(d['l_h2'])}</h2>
  <p class="lead">{e(d['l_lead'])}</p>
  <ol class="loop">{''.join(f'<li class="rise"><span class="k">{e(k)}</span><h3>{e(h)}</h3><p>{e(p)}</p></li>' for k, h, p in d['loop'])}</ol>
</div></section>

<section style="padding-top:0"><div class="wrap split">
  <div class="rise">
    <p class="eyebrow">{e(d['s_eyebrow'])}</p>
    <h2>{e(d['s_h2'])}</h2>
    <p class="lead">{e(d['s_lead'])}</p>
    <ol class="steps">{''.join(f'<li>{e(s)}</li>' for s in d['steps'])}</ol>
  </div>
  <div class="media rise"><figure class="shot"><img src="{shot(1)}" alt="{a(d['watch_aria'])}" width="660" height="1434" loading="lazy"></figure></div>
</div></section>

<section class="dark"><div class="wrap split">
  <div class="media rise"><figure class="shot"><img src="{shot(6)}" alt="{a(d['early_alt'])}" width="660" height="1434" loading="lazy"></figure></div>
  <div class="rise">
    <p class="eyebrow">{e(d['e_eyebrow'])}</p>
    <h2>{e(d['e_h2'])}</h2>
    <p class="lead">{e(d['e_lead'])}</p>
    <ul class="mistakes">{''.join(f'<li><b>{e(b)}</b>{e(t)}</li>' for b, t in d['mistakes'])}</ul>
  </div>
</div></section>

<section class="ride"><div class="wrap split">
  <div class="rise">
    <p class="eyebrow">{e(d['t_eyebrow'])}</p>
    <h2>{e(d['t_h2'])}</h2>
    <p class="lead">{e(d['t_lead'])}</p>
    <div class="pad-card">
      <p class="pad-label" style="color:var(--ink);font-size:15px;margin-bottom:6px">{e(d['t_try'])}</p>
      <p class="pad-label">{e(d['t_toes'])}</p>
      <div class="pad-stage">
        <div class="board">
          <span class="edge toes"></span><span class="edge heels"></span>
          <span class="end nose">{e(d['t_nose'])}</span><span class="end tail">{e(d['t_tail'])}</span>
          <span class="foot lead-foot"></span><span class="foot rear-foot"></span>
          <span class="ball" role="slider" tabindex="0" aria-label="{a(d['t_ball'])}" aria-valuemin="-1" aria-valuemax="1" aria-valuenow="0"></span>
        </div>
      </div>
      <p class="pad-label">{e(d['t_heels'])}</p>
      <p class="readout" aria-live="polite"></p>
      <p class="pad-hint">{e(d['t_hint'])}</p>
    </div>
    <script type="application/json" id="pad-messages">{ld(d['pad'])}</script>
  </div>
  <div class="media rise"><figure class="shot"><img src="{shot(5)}" alt="{a(d['ride_aria'])}" width="660" height="1434" loading="lazy"></figure></div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow">{e(d['f_eyebrow'])}</p>
  <h2>{e(d['f_h2'])}</h2>
  <div class="trio">''')
    imgs = [7, 8, 9]
    arts = []
    for (h, p, lis, alt_t), im in zip(d['trio'], imgs):
        arts.append(f'<article class="rise"><h3>{e(h)}</h3><p>{e(p)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in lis)}</ul>\n'
                    f'        <figure class="shot sm"><img src="{shot(im)}" alt="{a(alt_t)}" width="660" height="1434" loading="lazy"></figure></article>')
    w(''.join(arts) + '</div>\n</div></section>\n')
    lv = []
    for i, ((stem, lessons), (g)) in enumerate(zip(LEVELS, [0] * 7), 1):
        lv.append(f'<div class="level rise"><span class="n">{e(d["level_label"].replace("%d", str(i)))}</span><h3>{e(app(stem + ".title", ck))}</h3>'
                  f'<p>{e(app(stem + ".goal", ck))}</p><ol>{"".join(f"<li>{e(app(f"lesson{n}.skill", ck))}</li>" for n in lessons)}</ol></div>')
    w(f'''<section id="lessons" style="padding-top:0"><div class="wrap">
  <p class="eyebrow">{e(d['c_eyebrow'])}</p>
  <h2>{e(d['c_h2'])}</h2>
  <p class="lead">{e(d['c_lead'])}</p>
  <div class="levels">{''.join(lv)}</div>
</div></section>

<section class="gallery" style="padding-top:0"><div class="wrap">
  <p class="eyebrow">{e(d['g_eyebrow'])}</p>
  <h2>{e(d['g_h2'])}</h2>
</div>
  <div class="shots" tabindex="0">{''.join(f'<figure class="shot"><img src="{shot(n)}" alt="" width="660" height="1434" loading="lazy"></figure>' for n in (2, 3, 4, 10))}</div>
</section>

<section style="padding-top:0"><div class="wrap pair">
  <div class="panel a rise"><h2>{e(d['pa'][0])}</h2><p>{e(d['pa'][1])}</p><p>{e(d['pa'][2])}</p></div>
  <div class="panel b rise"><h2>{e(d['pb'][0])}</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in d['pb'][1])}</ul></div>
</div></section>

<section id="faq" style="padding-top:0"><div class="wrap">
  <p class="eyebrow">{e(d['q_eyebrow'])}</p>
  <h2>{e(d['q_h2'])}</h2>
  <div class="faq">{''.join(f'<details><summary>{e(q)}</summary><p>{e(t)}</p></details>' for q, t in d['faq'])}</div>
</div></section>

<section class="end-cta"><div class="wrap">
  <img src="/snowboard/assets/icon.png" alt="" width="96" height="96" loading="lazy">
  <h2>{e(d['end_h2'])}</h2>
  <p>{e(d['end_p'])}</p>
  <div class="cta"><a class="btn btn-primary" href="{a(mail)}">{e(d['cta2'])}</a></div>
</div></section>
</main>

<footer><div class="wrap">
  <small>{e(d['foot'])}<br>© 2026 Vladimir Dyagay</small>
  <nav><a href="/snowboard/{folder}support.html">{e(d['foot_support'])}</a><a href="/snowboard/{folder}privacy.html">{e(d['foot_privacy'])}</a><a href="/">Notemia apps</a><a href="mailto:helpyoutofeel@gmail.com">helpyoutofeel@gmail.com</a></nav>
</div></footer>
<script src="/snowboard/app.js"></script>
</body>
</html>
''')
    return ''.join(P)

def check(code, d):
    need = ['title','desc','lang_label','nav_game','nav_lessons','nav_faq','h1a','h1b','sub','cta1','cta2','notify_subject','soon','facts','hero_aria',
            'm_eyebrow','m_h2','m_lead','courses_alt','moves','m_note','l_eyebrow','l_h2','l_lead','loop','s_eyebrow','s_h2','s_lead','steps','watch_aria',
            'early_alt','e_eyebrow','e_h2','e_lead','mistakes','t_eyebrow','t_h2','t_lead','t_try','t_toes','t_heels','t_nose','t_tail','t_ball','t_hint','pad','ride_aria',
            'f_eyebrow','f_h2','trio','level_label','c_eyebrow','c_h2','c_lead','pa','pb','q_eyebrow','q_h2','faq','end_h2','end_p','foot','foot_support','foot_privacy','g_eyebrow','g_h2']
    miss = [k for k in need if k not in d]
    assert not miss, (code, miss)
    assert len(d['facts']) == 4 and len(d['courses_alt']) == 5 and len(d['moves']) == 6 and len(d['loop']) == 4
    assert len(d['steps']) == 8 and len(d['mistakes']) == 2 and len(d['trio']) == 3 and len(d['faq']) == 12
    assert set(d['pad']) == {'flat','nose','toes','heels','back'} and len(d['pb'][1]) == 5


def lang_menu(code, page):
    """Language dropdown; `page` is '' for the landing or 'privacy.html' / 'support.html'."""
    items = ''.join(f'<a href="/snowboard/{f2}{page}" hreflang="{h2}" lang="{h2}"' + (' aria-current="true"' if c2 == code else '') + f'>{n2}</a>'
                    for c2, f2, h2, _o, _k, n2 in LANGS)
    return items

def build_doc(kind, code, folder, hl, ogl, ck, native, d, X):
    """kind: 'privacy' or 'support'. X is the dict P or S from docs_<code>.py."""
    page = kind + '.html'
    url = BASE + folder + page
    alt = ''.join(f'<link rel="alternate" hreflang="{h}" href="{BASE}{f}{page}">\n' for _, f, h, *_ in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{BASE}{page}">\n'
    mail = 'mailto:helpyoutofeel@gmail.com'
    body = []
    if kind == 'privacy':
        body.append(f'<div class="summary"><strong>{e(X["short_label"])}</strong> {e(X["short"])}</div>')
        for h, p in X['sections']:
            body.append(f'<h2>{e(h)}</h2><p>{e(p)}</p>')
        body.append(f'<h2>{e(X["contact_h"])}</h2><p><a href="{mail}">helpyoutofeel@gmail.com</a></p>')
    else:
        cards = ''.join(
            f'<div class="support-card"><h3>{e(h)}</h3><p>{e(p)}</p><a class="btn {c}" href="{a(mail + "?subject=" + urllib.parse.quote(sub, safe=""))}">{e(b)}</a></div>'
            for (h, p, b, sub), c in zip(X['cards'], ('btn-primary', 'btn-ink')))
        body.append(f'<div class="support-cards">{cards}</div>')
        body.append(f'<h2>{e(X["faq_h"])}</h2><div class="faq">' + ''.join(f'<details><summary>{e(q)}</summary><p>{e(t)}</p></details>' for q, t in X['faq']) + '</div>')
    other = 'support' if kind == 'privacy' else 'privacy'
    return f"""<!doctype html>
<html lang="{hl}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(X['title'])}</title>
<meta name="description" content="{a(X['desc'])}">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#17243d">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Snowboarding">
<meta property="og:title" content="{a(X['title'])}">
<meta property="og:description" content="{a(X['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{ogl}">
<link rel="icon" href="/snowboard/assets/icon-64.png" type="image/png">
<link rel="apple-touch-icon" href="/snowboard/assets/icon-180.png">
<link rel="stylesheet" href="/snowboard/style.css">
</head>
<body class="doc">
<header class="top solid"><div class="wrap">
  <a class="brand" href="/snowboard/{folder}"><img src="/snowboard/assets/icon-64.png" alt="" width="36" height="36">Snowboarding</a>
  <nav><a href="/snowboard/{folder}support.html">{e(d['foot_support'])}</a><a href="/snowboard/{folder}privacy.html">{e(d['foot_privacy'])}</a>
  <details class="langs"><summary class="lang" aria-label="{a(d['lang_label'])}">{e(native)}</summary><div class="langs-list">{lang_menu(code, page)}</div></details></nav>
</div></header>
<main>
<div class="doc-hero"><div class="wrap narrow">
  <h1>{e(X['h1'])}</h1>
  <p class="sub">{e(X['sub'])}</p>
</div></div>
<div class="doc-body"><div class="wrap narrow">
{chr(10).join(body)}
</div></div>
</main>
<footer><div class="wrap">
  <small>{e(d['foot'])}<br>© 2026 Vladimir Dyagay</small>
  <nav><a href="/snowboard/{folder}">Snowboarding</a><a href="/snowboard/{folder}support.html">{e(d['foot_support'])}</a><a href="/snowboard/{folder}privacy.html">{e(d['foot_privacy'])}</a><a href="/">Notemia apps</a><a href="mailto:helpyoutofeel@gmail.com">helpyoutofeel@gmail.com</a></nav>
</div></footer>
<script src="/snowboard/app.js"></script>
</body>
</html>
"""

def check_doc(code, P, S):
    for k in ['title','desc','h1','sub','short_label','short','sections','contact_h']:
        assert k in P, (code, 'P', k)
    assert len(P['sections']) == 7, (code, len(P['sections']))
    for k in ['title','desc','h1','sub','cards','faq_h','faq']:
        assert k in S, (code, 'S', k)
    assert len(S['cards']) == 2 and len(S['faq']) == 13, (code, len(S['faq']))

def main():
    only = sys.argv[1:] 
    sm = []
    for code, folder, hl, ogl, ck, native in LANGS:
        try:
            d = importlib.import_module('lang_' + code).D
        except ModuleNotFoundError:
            print('skip', code); continue
        check(code, d)
        out = os.path.join(SITE, folder, 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(build(code, folder, hl, ogl, ck, native, d))
        print('wrote', os.path.relpath(out, ROOT), len(d['title']), len(d['desc']))
        sm.append(folder)
        try:
            dm = importlib.import_module('docs_' + code)
        except ModuleNotFoundError:
            print('  no docs for', code); continue
        check_doc(code, dm.P, dm.S)
        for kind, X in (('privacy', dm.P), ('support', dm.S)):
            o2 = os.path.join(SITE, folder, kind + '.html')
            open(o2, 'w', encoding='utf-8').write(build_doc(kind, code, folder, hl, ogl, ck, native, d, X))
            print('wrote', os.path.relpath(o2, ROOT))
    # sitemap block for the language pages
    alts = ''.join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{BASE}{f}"/>\n' for _, f, h, *_ in LANGS) + f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>\n'
    blocks = ''.join(f'  <url><loc>{BASE}{f}</loc>\n{alts}  </url>\n' for _, f, *_ in LANGS)
    for pg in ('privacy.html', 'support.html'):
        alts2 = ''.join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{BASE}{f}{pg}"/>\n' for _, f, h, *_ in LANGS) + f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{pg}"/>\n'
        blocks += ''.join(f'  <url><loc>{BASE}{f}{pg}</loc>\n{alts2}  </url>\n' for _, f, *_ in LANGS)
    p = os.path.join(ROOT, 'sitemap.xml')
    s = open(p, encoding='utf-8').read()
    import re
    s = re.sub(r'  <url><loc>https://notemia.app/snowboard/(?:[a-z]{2}/)?(?:privacy\.html|support\.html)?</loc>.*?</url>\n', '', s, flags=re.S)
    s = s.replace('  <url><loc>https://notemia.app/support.html</loc></url>\n', blocks + '  <url><loc>https://notemia.app/support.html</loc></url>\n')
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    main()
