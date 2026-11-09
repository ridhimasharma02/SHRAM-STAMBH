from urllib.parse import quote
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + os.sep
VER = "36"  # bump when css/js change so phones fetch fresh copies

S = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
def svg(body): return S + body + '</svg>'

ICONS = {
    # topics
    "rights":  svg('<path d="M24 6v34M14 42h20M8 14h32"/><path d="M12 14L6 27a6 4 0 0 0 12 0z"/><path d="M36 14l-6 13a6 4 0 0 0 12 0z"/>'),
    "money":   svg('<rect x="4" y="12" width="40" height="24"/><path d="M19 18h10M19 22h10M22 18c5 0 5 8 0 8h-3l8 5"/>'),
    "job":     svg('<rect x="10" y="8" width="28" height="34"/><path d="M18 11V5h12v6z"/><path d="M17 26l5 5 9-10"/>'),
    "phone":   svg('<path d="M14 6h-4a4 4 0 0 0-4 4c0 18 14 32 32 32a4 4 0 0 0 4-4v-4l-8-4-4 4c-6-3-9-6-12-12l4-4-4-8z"/>'),
    "home":    svg('<path d="M6 22L24 8l18 14"/><path d="M11 19v21h26V19"/>'),
    "diary":   svg('<rect x="6" y="9" width="36" height="32"/><path d="M6 18h36M15 5v8M33 5v8"/><path d="M15 28l5 5 10-10"/>'),
    "show":    svg('<rect x="13" y="4" width="22" height="40" rx="2"/><path d="M18 13h12M18 19h12M18 25h8M22 38h4"/>'),
    "pictures":svg('<rect x="5" y="9" width="38" height="30"/><circle cx="16" cy="19" r="4"/><path d="M5 34l12-10 9 8 6-5 11 9"/>'),
    "speaker": svg('<path d="M6 18h8l10-8v28l-10-8H6z"/><path d="M31 17a10 10 0 0 1 0 14M36 12a17 17 0 0 1 0 24"/>'),
    "alert":   svg('<path d="M24 5L45 41H3z"/><path d="M24 18v11M24 34v1"/>'),
    "pillar":  svg('<path d="M7 9h34M10 13h28M13 13v25M35 13v25M21 13v25M27 13v25M10 38h28M6 43h36"/><path d="M12 5h24"/>'),
    "thumbup":  svg('<path d="M14 22v20H6V22z"/><path d="M14 22l8-16c3 0 5 2 5 5v7h11a4 4 0 0 1 4 5l-3 14a4 4 0 0 1-4 3H14"/>'),
    "thumbdown":svg('<path d="M14 26V6H6v20z"/><path d="M14 26l8 16c3 0 5-2 5-5v-7h11a4 4 0 0 0 4-5l-3-14a4 4 0 0 0-4-3H14"/>'),
    "mic":      svg('<rect x="17" y="4" width="14" height="25" rx="7"/><path d="M10 22a14 14 0 0 0 28 0M24 36v7M16 43h16"/>'),
    "hospital": svg('<path d="M7 42V15h34v27"/><path d="M24 21v13M17.5 27.5h13"/><path d="M3 42h42M15 15V7h18v8"/>'),
    # login: "this is me" pictures
    "hammer":   svg('<path d="M8 10h20v10H8z"/><path d="M28 13h8l4-4v14l-4-4h-8"/><path d="M17 20v23"/>'),
    "broom":    svg('<path d="M33 4L23 25"/><path d="M15 25h16l5 18H10z"/><path d="M17 33v10M23 33v10M29 33v10"/>'),
    "shovel":   svg('<path d="M24 4v22"/><path d="M18 4h12"/><path d="M15 26h18v7a9 9 0 0 1-18 0z"/>'),
    "scissors": svg('<circle cx="13" cy="36" r="6"/><circle cx="35" cy="36" r="6"/><path d="M17 31L36 6M31 31L12 6"/>'),
    # login: secret pictures
    "sun":      svg('<circle cx="24" cy="24" r="8"/><path d="M24 4v6M24 38v6M4 24h6M38 24h6M10 10l4 4M34 34l4 4M38 10l-4 4M14 34l-4 4"/>'),
    "moon":     svg('<path d="M30 6a18 18 0 1 0 12 26A14 14 0 0 1 30 6z"/>'),
    "star":     svg('<path d="M24 5l5.6 12 13 1.5-9.7 8.8 2.7 12.9L24 33.6 12.4 40.2l2.7-12.9-9.7-8.8 13-1.5z"/>'),
    "tree":     svg('<path d="M24 44V30"/><path d="M24 4L10 24h8L8 34h32L30 24h8z"/>'),
    "flower":   svg('<circle cx="24" cy="18" r="5"/><circle cx="24" cy="8" r="5"/><circle cx="34" cy="16" r="5"/><circle cx="30" cy="27" r="5"/><circle cx="18" cy="27" r="5"/><circle cx="14" cy="16" r="5"/><path d="M24 30v14M24 38c-4-4-9-4-11-2M24 40c4-4 9-4 11-2"/>'),
    "fish":     svg('<path d="M6 24c6-9 18-12 28-4 0 0-4 4 0 8-10 8-22 5-28-4z"/><path d="M34 20l9-6v20l-9-6"/><circle cx="14" cy="23" r="1.5" fill="currentColor"/>'),
    "key":      svg('<circle cx="14" cy="24" r="8"/><circle cx="14" cy="24" r="2.5"/><path d="M22 24h21M37 24v7M43 24v5"/>'),
    "umbrella": svg('<path d="M4 24a20 20 0 0 1 40 0z"/><path d="M24 4v2M24 24v14a4 4 0 0 1-8 0"/>'),
    "cup":      svg('<path d="M8 18h26v14a10 10 0 0 1-10 10h-6A10 10 0 0 1 8 32z"/><path d="M34 22h3a5 5 0 0 1 0 10h-3"/><path d="M16 6c-2 3 2 5 0 8M24 6c-2 3 2 5 0 8"/>'),
    "lock":     svg('<rect x="9" y="21" width="30" height="23"/><path d="M15 21v-6a9 9 0 0 1 18 0v6"/><path d="M24 30v6"/>'),
    "person":   svg('<circle cx="24" cy="15" r="8"/><path d="M8 44c0-9 7-15 16-15s16 6 16 15"/>'),
    "plus":     svg('<path d="M24 8v32M8 24h32"/>'),
    # worker types
    "helmet":  svg('<path d="M8 32a16 15 0 0 1 32 0"/><path d="M4 32h40v5H4z"/><path d="M20 18v-6h8v6"/>'),
    "house":   svg('<path d="M6 22L24 8l18 14"/><path d="M10 19v21h28V19"/><path d="M20 40V28h8v12"/>'),
    "factory": svg('<path d="M4 42V22l10 6v-6l10 6v-6l10 6V8h8v34z"/><path d="M10 35h4M20 35h4M30 35h4"/>'),
    "bus":     svg('<rect x="8" y="6" width="32" height="30"/><path d="M8 22h32M14 36v5M34 36v5"/><path d="M15 29h2M31 29h2"/>'),
    # pictograms
    "coins":   svg('<ellipse cx="24" cy="12" rx="14" ry="5"/><path d="M10 12v8c0 3 6 5 14 5s14-2 14-5v-8"/><path d="M10 20v8c0 3 6 5 14 5s14-2 14-5v-8"/><path d="M10 28v8c0 3 6 5 14 5s14-2 14-5v-8"/>'),
    "calpay":  svg('<rect x="6" y="9" width="36" height="32"/><path d="M6 18h36M15 5v8M33 5v8"/><path d="M19 24h10M19 28h10M22 24c5 0 5 7 0 7h-2l7 5"/>'),
    "clock8":  svg('<circle cx="24" cy="24" r="18"/><path d="M24 11v13l-9 5"/>'),
    "bed":     svg('<path d="M4 38V12M4 30h40v8M44 30v-5a6 6 0 0 0-6-6H22v11"/><circle cx="13" cy="23" r="4"/>'),
    "overtime":svg('<circle cx="16" cy="24" r="12"/><path d="M16 16v8l5 3"/><text x="29" y="31" font-size="15" font-weight="bold" font-family="Arial, sans-serif" fill="currentColor" stroke="none">2×</text>'),
    "equal":   svg('<circle cx="11" cy="11" r="5"/><path d="M4 42V28a7 7 0 0 1 14 0v14"/><circle cx="37" cy="11" r="5"/><path d="M29 42l3-15h10l3 15z"/><path d="M21 22h6M21 28h6"/>'),
    "aid":     svg('<rect x="6" y="13" width="36" height="27"/><path d="M18 13V7h12v6M24 20v13M17.5 26.5h13"/>'),
    "chain":   svg('<path d="M7 31l6-6a5 5 0 0 1 7 7l-6 6a5 5 0 0 1-7-7z"/><path d="M28 16l6-6a5 5 0 0 1 7 7l-6 6a5 5 0 0 1-7-7z"/><path d="M21 21l-3-3M27 27l3 3M24 18v-4M30 24h4"/>'),
    "idcard":  svg('<rect x="4" y="10" width="40" height="28"/><circle cx="15" cy="21" r="4"/><path d="M8 32a7 6 0 0 1 14 0M27 19h11M27 25h8"/>'),
    "slip":    svg('<path d="M12 4h18l8 8v32H12z"/><path d="M30 4v8h8M18 22h14M18 28h14M18 34h8"/>'),
    "hand":    svg('<path d="M16 27V12a3 3 0 0 1 6 0v10M22 22V8a3 3 0 0 1 6 0v14M28 22V10a3 3 0 0 1 6 0v16M34 19a3 3 0 0 1 6 0v9c0 9-6 16-14 16-6 0-10-3-13-9l-4-8a3 3 0 0 1 5-3l2 4"/>'),
    "child":   svg('<circle cx="24" cy="12" r="5"/><path d="M17 42V27a7 7 0 0 1 14 0v15"/><path d="M6 6l36 36"/>'),
    "nothumb": svg('<path d="M10 4h20l8 8v32H10z"/><path d="M30 4v8h8"/><ellipse cx="24" cy="27" rx="6" ry="8"/><path d="M21 24c2-2 4-2 6 0M20 28c3-2 5-2 8 0M8 42L40 10"/>'),
    "ear":     svg('<path d="M14 18a10 10 0 0 1 20 0c0 6-6 8-6 14a6 6 0 0 1-12 0"/><path d="M20 18a4 4 0 0 1 8 0c0 3-3 4-3 6"/>'),
    "people":  svg('<circle cx="12" cy="14" r="4"/><circle cx="24" cy="11" r="5"/><circle cx="36" cy="14" r="4"/><path d="M4 38v-8a8 8 0 0 1 12-6M44 38v-8a8 8 0 0 0-12-6M16 40V28a8 8 0 0 1 16 0v12"/>'),
    "police":  svg('<path d="M24 4l16 6v12c0 10-7 18-16 22C15 40 8 32 8 22V10z"/><path d="M24 15l3 6 6 1-4.5 4 1 6-5.5-3-5.5 3 1-6L15 22l6-1z"/>'),
}

# the site logo: an ochre tile with the word श्रम (labour), like a signboard
ICONS["pillar"] = '<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><rect width="48" height="48" fill="#b5832a"/><text x="24" y="31.5" text-anchor="middle" font-size="19" font-weight="800" font-family="Mukta, &apos;Noto Sans Devanagari&apos;, &apos;Kohinoor Devanagari&apos;, sans-serif" fill="#1d1f20">श्रम</text></svg>'

# href, english, hindi, icon, topic class
NAV = [
    ("index.html",      "Home",          "मुख्य पन्ना",     "home",   ""),
    ("rights.html",     "Your rights",   "आपके अधिकार",    "rights", "t-rights"),
    ("wages.html",      "Not paid?",     "पैसा नहीं मिला?",  "money",  "t-wages"),
    ("diary.html",      "Work diary",    "काम का हिसाब",    "diary",  "t-wages"),
    ("before-job.html", "Before a job",  "काम से पहले",     "job",    "t-job"),
    ("ask.html",        "Ask",           "सवाल पूछें",       "mic",    "t-help"),
    ("help.html",       "Get help",      "मदद लें",         "phone",  "t-help"),
]
CUR = ' aria-current="page"'

ASK_CELL = '<li><a class="askbtn" href="ask.html">' + ICONS["mic"] + '<span><b>Ask</b>सवाल पूछें</span></a></li>'

# Runs first on every page except login.html: if nobody is logged in on this
# phone, go to the login page straight away, before anything else shows.
GUARD = """  <script>
  (function () {
    function check() {
      var ok = false;
      try {
        var id = JSON.parse(sessionStorage.getItem('ss-session') || 'null');
        var last = JSON.parse(sessionStorage.getItem('ss-last') || '0');
        var list = JSON.parse(localStorage.getItem('ss-profiles') || '[]');
        var fresh = !last || Date.now() - last < 30 * 60 * 1000;   /* 30 minutes unused logs out */
        ok = !!id && fresh && list.some(function (p) { return p.id === id; });
      } catch (e) {}
      if (!ok) {
        document.documentElement.style.display = 'none';
        var here = location.pathname.split('/').pop() || 'index.html';
        location.replace('login.html?next=' + encodeURIComponent(here + location.hash));
      }
    }
    check();
    /* the Back button can show a saved copy of the page: check again */
    window.addEventListener('pageshow', function (e) { if (e.persisted) check(); });
  })();
  </script>
"""
SHARE_TEXT = "SHRAM STAMBH (श्रम स्तंभ): free information for workers on wages and rights, in English and Hindi, with read-aloud. मज़दूरों के अधिकार और मज़दूरी की जानकारी, सुनने की सुविधा के साथ।"

def hi(t): return f'<span class="hi" lang="hi">{t}</span>'

def pagehead(icon, topic, en, h, crumb):
    return f'''    <p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>
    <div class="pagehead {topic}">{ICONS[icon]}<h1>{en}{hi(h)}</h1></div>'''

def sidebar(filename, guard):
    """Right-hand column on wide screens: listen, language, help numbers, ask.
    Phones don't show it; they have the bottom bar and the boxes on the home page instead."""
    ask = "" if (not guard or filename == "ask.html") else f'''
      <a class="side-card side-ask" href="ask.html">{ICONS["mic"]}<span><strong>Ask a question</strong>{hi("बोलकर सवाल पूछें")}<span class="desc">Speak in your language and hear the answer.</span></span></a>'''
    return f'''    <aside class="sidebar noprint" aria-label="Listen and get help">
      <div class="side-card side-listen">
        <button type="button" class="bigsay side-say" data-read="page" aria-label="Listen to this page">{ICONS["speaker"]}<span>Listen to this page{hi("यह पन्ना सुनें")}</span></button>
        <p class="side-label">Voice language · आवाज़ की भाषा</p>
        <div class="langrow" aria-label="Choose your language"></div>
      </div>
      <div class="side-card side-help">
        <p class="side-title"><strong>Need help now?</strong>{hi("अभी मदद चाहिए?")}</p>
        <a class="callbtn" href="tel:15100">{ICONS["phone"]}<span>15100<small>Free legal help · मुफ़्त कानूनी मदद</small></span></a>
        <a class="callbtn red" href="tel:112">{ICONS["alert"]}<span>112<small>Danger · खतरा</small></span></a>
      </div>{ask}
    </aside>'''


def page(filename, title, body, desc, topic="", extra_js="", guard=True):
    nav = "\n".join(
        f'        <li class="{t}"><a href="{href}"{CUR if href == filename else ""}>{ICONS[ic]}<span>{en}<span class="hi" lang="hi">{h}</span></span></a></li>'
        for href, en, h, ic, t in NAV
    )
    share = "https://wa.me/?text=" + quote(SHARE_TEXT)
    extra = extra_js if isinstance(extra_js, (list, tuple)) else ([extra_js] if extra_js else [])
    js = "".join(f'  <script src="{f}?v={VER}" defer></script>\n' for f in ["audio-manifest.js", "lang-data.js", "account-data.js", "speak.js", "account.js", "site.js"] + list(extra))
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | SHRAM STAMBH</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#2e3336">
  <meta property="og:site_name" content="SHRAM STAMBH · श्रम स्तंभ">
  <meta property="og:title" content="{title} | SHRAM STAMBH">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="style.css?v={VER}">
{GUARD if guard else ''}  <script>document.documentElement.classList.add('js')</script>
{js}</head>
<body class="{topic}">
<a class="skip" href="#content">Skip to content</a>
<noscript>
  <div class="nojs-box">
    <p><strong>This site needs JavaScript to log in and to speak.</strong> Please turn JavaScript on, or open the site in Chrome.</p>
    <p lang="hi">लॉग इन और आवाज़ के लिए JavaScript चाहिए। कृपया उसे चालू करें या Chrome में खोलें।</p>
    <p>For help now · अभी मदद के लिए:</p>
    <a class="callbtn" href="tel:15100">15100<small>Free legal help · मुफ़्त कानूनी मदद</small></a>
    <a class="callbtn red" href="tel:112">112<small>Danger · खतरा</small></a>
  </div>
</noscript>

<header class="site">
  <div class="wrap">
    <div class="brandrow">
      <p class="site-name"><a href="index.html">{ICONS["pillar"]}<span>SHRAM STAMBH <small lang="hi">श्रम स्तंभ</small></span></a></p>
      <div class="head-tools">
        <span id="voice-slot"></span>
        <div class="account" id="account-slot"><a class="account-link" href="login.html">{ICONS["lock"]}<span>Log in<span class="hi" lang="hi">लॉग इन</span></span></a></div>
      </div>
    </div>
    <nav class="main" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>

<main id="content">
  <div class="wrap layout">
    <div class="content">
{body}
    </div>
{sidebar(filename, guard)}
  </div>
</main>

<footer class="site">
  <div class="wrap foot-grid">
    <div>
      <p class="foot-name">{ICONS["pillar"]}<span>SHRAM STAMBH <small lang="hi">श्रम स्तंभ</small></span></p>
      <p>Information for daily-wage, construction, domestic and factory workers in India.</p>
      <p class="muted">This site gives general information, not legal advice. Rules and minimum wages are different in every state. Use it to know what to ask, then confirm with your district labour office or free legal aid on 15100.</p>
      <p class="muted" lang="hi">यह सामान्य जानकारी है, कानूनी सलाह नहीं। हर राज्य के नियम और न्यूनतम मज़दूरी अलग हैं। पक्की जानकारी के लिए ज़िला श्रम कार्यालय या 15100 पर बात करें।</p>
    </div>
    <ul class="foot-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="rights.html">Your rights</a></li>
      <li><a href="pictures.html">Rights in pictures</a></li>
      <li><a href="wages.html">Not paid?</a></li>
      <li><a href="diary.html">Work diary</a></li>
      <li><a href="before-job.html">Before a job</a></li>
      <li><a href="show.html">Show this screen</a></li>
      <li><a href="ask.html">Ask a question</a></li>
      <li><a href="help.html">Helplines</a></li>
      <li><a href="login.html">Log in</a></li>
      <li><a href="{share}">Send this site on WhatsApp</a></li>
    </ul>
    <p class="foot-small">No tracking. Your account, name and mobile number stay on this phone and are never sent anywhere. We never ask for Aadhaar. &nbsp;·&nbsp; Last checked: November 2026</p>
  </div>
</footer>

<nav class="bottombar noprint{'' if guard else ' three'}" aria-label="Quick help">
  <ul>
    <li><a href="tel:15100">{ICONS["phone"]}<span><b>15100</b>Free help · मदद</span></a></li>
    <li><a class="sos" href="tel:112">{ICONS["alert"]}<span><b>112</b>Danger · खतरा</span></a></li>
    {ASK_CELL if guard else ''}
    <li id="listen-slot"><a href="help.html">{ICONS["people"]}<span><b>Help</b>मदद लें</span></a></li>
  </ul>
</nav>

</body>
</html>
'''
    with open(OUT + filename, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


def login_gate(next_page, panel=True):
    """'Log in to see your diary' box. Hidden until account.js finds this phone has accounts."""
    import i18n
    cls = "panel t-help login-gate" if panel else "login-gate"
    return (f'<div class="{cls}" hidden {i18n.say_attrs(i18n.LOGIN["needLogin"])}>'
            f'{ICONS["lock"]}<p><strong>Log in to see your saved diary and notes.</strong>{hi("अपना हिसाब और डायरी देखने के लिए लॉग इन करें।")}</p>'
            f'<a class="btn dark" href="login.html?next={next_page}">Log in · लॉग इन</a></div>')
