/* SHRAM STAMBH - voice for people who can't read.

   How it speaks, in order of preference:
   1. Recorded audio. Every fixed piece of text on the site was recorded on a Mac
      in seven languages (the audio/ folder). These are small .m4a files that
      play in any browser, so they do not depend on the phone having a voice.
   2. The phone's own text-to-speech, only for text that changes (the diary
      totals, notebook entries). A watchdog resets it if it gets stuck.

   Nothing the user does here is sent anywhere. */
(function () {
  'use strict';

  var root = document.documentElement;
  var L = window.SS_LANG || { langs: [{ code: 'hi', name: 'हिंदी' }, { code: 'en', name: 'English' }], voiceChosen: {}, otherLang: {} };
  var MANIFEST = window.SS_AUDIO || {};
  var CODES = L.langs.map(function (x) { return x.code; });
  var synth = window.speechSynthesis || null;
  var HAS_TTS = !!(synth && window.SpeechSynthesisUtterance);
  var player = typeof Audio !== 'undefined' ? new Audio() : null;
  if (player) player.preload = 'auto';

  if (!player && !HAS_TTS) return;
  root.classList.add('can-speak');

  var SVG = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">';
  var ICON_SPEAK = SVG + '<path d="M6 18h8l10-8v28l-10-8H6z"/><path d="M31 17a10 10 0 0 1 0 14M36 12a17 17 0 0 1 0 24"/></svg>';
  var ICON_STOP = SVG + '<rect x="13" y="13" width="22" height="22" fill="currentColor"/></svg>';
  var IS_ANDROID = /Android/i.test(navigator.userAgent);
  var KNOWN_NUMBERS = /(^|[^0-9])(1800118005|1800112526|9966044425|15100|14434|1098|112|181)(?![0-9])/g;

  /* ---------------- language ---------------- */

  var lang = 'hi';
  try {
    var saved = localStorage.getItem('ss-voice');
    if (CODES.indexOf(saved) !== -1) lang = saved;
  } catch (e) { /* storage blocked */ }

  var voices = [];
  function loadVoices() { if (!HAS_TTS) return; try { voices = synth.getVoices() || []; } catch (e) { voices = []; } }
  loadVoices();
  if (HAS_TTS) {
    if (synth.addEventListener) synth.addEventListener('voiceschanged', loadVoices);
    else synth.onvoiceschanged = loadVoices;
  }
  function findVoice(l) {
    var best = null;
    for (var v = 0; v < voices.length; v++) {
      var vl = String(voices[v].lang || '').toLowerCase().replace('_', '-');
      if (vl.indexOf(l + '-in') === 0 || (vl.indexOf(l) === 0 && !best)) {
        if (voices[v].localService && vl.indexOf(l + '-in') === 0) return voices[v];
        best = voices[v];
      }
    }
    return best;
  }

  /* ---------------- text helpers ---------------- */

  function hash(s) {
    var h = 0x811c9dc5;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
    return ('0000000' + h.toString(16)).slice(-8);
  }
  function spellDigits(s) { return String(s).replace(/[^0-9]/g, '').split('').join(' '); }
  function spellPhones(t) {
    return String(t).replace(KNOWN_NUMBERS, function (m, pre, num) { return pre + spellDigits(num); });
  }
  function clean(t) {
    return String(t)
      .replace(/_{2,}/g, ' ... ')
      .replace(/\s*\/\s*/g, ', ')
      .replace(/[·|›‹—–]/g, ' ')
      .replace(/₹\s*/g, '₹')
      .replace(/\s+/g, ' ')
      .replace(/\s+([.।?!,:])/g, '$1')
      .replace(/([.।?!:,])(\s*[.।])+/g, '$1')
      .replace(/^[\s.।,]+/, '')
      .trim();
  }
  function finalText(t) { return clean(spellPhones(t)); }

  /* ---------------- reading the page ---------------- */

  var SKIP = 'svg,button,script,style,input,textarea,select,noscript,thead,.noread,.cal,[data-no-say],.no-js,.skip,[hidden]';
  var BLOCK_TAGS = /^(P|LI|H1|H2|H3|H4|TD|TH|TR|SUMMARY|LABEL|DT|DD|DIV|UL|OL|TABLE|DETAILS|SECTION|FIELDSET|LEGEND)$/;
  var SPEAKABLE = '.panel, .tiles > li, .pics > li, .showcard, .askwrap';

  function shown(el) {
    var cs = window.getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden';
  }
  function isBlock(el) { return BLOCK_TAGS.test(el.tagName) || el.classList.contains('desc') || el.classList.contains('big'); }
  /* All the numbers written in the Hindi lines of an element, joined like
     "|15100|112|". Used so a phone number that the Hindi line already says
     is not read out a second time. */
  function hindiNumbersIn(el) {
    var text = el.getAttribute && el.getAttribute('lang') === 'hi' ? el.textContent : '';
    el.querySelectorAll('[lang="hi"]').forEach(function (n) { text += ' ' + n.textContent; });
    var numbers = text.match(/[0-9][0-9-]*/g) || [];
    return '|' + numbers.map(function (x) { return x.replace(/-/g, ''); }).join('|') + '|';
  }

  /* Get the words of a box, in Hindi ('hi') or English ('en').

     It walks through the box's HTML, one piece at a time:
       - text inside lang="hi" counts as Hindi; everything else is English
       - buttons, pictures, inputs and hidden things are skipped
       - an element with data-say-hi / data-say-en is read as that text instead
       - phone numbers are read digit by digit ("1 5 1 0 0")
       - " . " is added between lines so the voice pauses
     In Hindi, a line that has no Hindi translation is skipped, except for
     any numbers in it, which are still worth hearing. */
  function gather(box, language) {
    var parts = [];

    function visit(node, insideHindi, lineNumbers) {
      /* plain text: keep it if it is in the language we want */
      if (node.nodeType === 3) {
        var isWanted = language === 'en' ? !insideHindi : insideHindi;
        if (isWanted) parts.push(node.nodeValue);
        return;
      }
      if (node.nodeType !== 1) return;
      var el = node;
      if (el.matches(SKIP) || !shown(el)) return;

      /* a ready-made spoken version replaces the element's own text */
      var spoken = el.getAttribute('data-say-' + language);
      if (spoken) { parts.push(' . ' + spoken + ' . '); return; }

      var hindiHere = insideHindi || el.getAttribute('lang') === 'hi';

      /* a phone number link */
      if (el.matches('a[href^="tel:"]')) {
        var number = String(el.getAttribute('href')).replace(/[^0-9]/g, '');
        var alreadySaid = lineNumbers.indexOf('|' + number + '|') !== -1;
        var readIt = language === 'en' ? !hindiHere : (hindiHere || !alreadySaid);
        if (readIt) {
          var words = spellDigits(number);
          if (el.classList.contains('callbtn')) words = language === 'hi' ? words + ' पर फ़ोन करें' : 'Call ' + words;
          parts.push(' . ' + words + ' . ');
        }
        return;
      }

      /* a new line (paragraph, list item, table cell...) */
      var isLine = isBlock(el);
      if (isLine) {
        var lineHasHindi = hindiHere || !!el.querySelector('[lang="hi"]');
        lineNumbers = hindiNumbersIn(el);
        parts.push(' . ');
        if (language === 'hi' && !lineHasHindi) {
          /* no Hindi version of this line: only read its numbers */
          var phoneLinks = el.querySelectorAll('a[href^="tel:"]');
          if (phoneLinks.length) {
            phoneLinks.forEach(function (a) { parts.push(' ' + spellDigits(a.getAttribute('href')) + ' . '); });
          } else {
            var shortText = el.textContent.replace(/\s+/g, ' ').trim();
            if (/\d/.test(shortText) && shortText.length < 40) parts.push(' ' + shortText + ' . ');
          }
          return;
        }
      }

      for (var child = el.firstChild; child; child = child.nextSibling) visit(child, hindiHere, lineNumbers);
      if (isLine) parts.push(' . ');
    }

    var startsInHindi = !!(box.closest && box.closest('[lang="hi"]'));
    var boxNumbers = hindiNumbersIn(box);
    for (var c = box.firstChild; c; c = c.nextSibling) visit(c, startsInHindi, boxNumbers);
    return clean(parts.join(''));
  }

  /* Turn anything into a list of {lang, text} pieces to speak.
     ctx.noticed stops the "this part is only in Hindi" notice repeating. */
  function resolve(source, l, ctx) {
    ctx = ctx || {};
    var out = [];
    function notice() {
      if (ctx.noticed || !L.otherLang[l]) return;
      ctx.noticed = true;
      out.push({ lang: l, text: finalText(L.otherLang[l]) });
    }
    if (source == null) return out;
    if (typeof source === 'string') { out.push({ lang: l, text: finalText(source) }); return out; }
    if (source.nodeType === 1) {
      var own = source.getAttribute('data-say-' + l);
      if (own) { out.push({ lang: l, text: finalText(own) }); return out; }
      if (l === 'hi' || l === 'en') {
        var t = gather(source, l);
        if (!t && l === 'hi') { t = gather(source, 'en'); if (t) out.push({ lang: 'en', text: finalText(t) }); return out; }
        if (t) out.push({ lang: l, text: finalText(t) });
        return out;
      }
      var hiOwn = source.getAttribute('data-say-hi');
      var th = hiOwn || gather(source, 'hi');
      if (th) { notice(); out.push({ lang: 'hi', text: finalText(th) }); }
      return out;
    }
    /* an object like {hi: '...', en: '...', bn: '...'} */
    if (source[l]) out.push({ lang: l, text: finalText(source[l]) });
    else if (source.hi) out.push({ lang: 'hi', text: finalText(source.hi) });
    else if (source.en) out.push({ lang: 'en', text: finalText(source.en) });
    return out;
  }

  /* what the bottom-bar Listen button reads: each box on the page in turn */
  function pageParts() {
    var main = (document.querySelector('main .content') || document.querySelector('main .wrap'));
    if (!main) return [];
    var list = [];
    Array.prototype.forEach.call(main.children, function (ch) {
      if (ch.matches(SKIP) || !shown(ch)) return;
      if (ch.matches('.tiles, .pics, .showcards, .split')) {
        ch.querySelectorAll(SPEAKABLE).forEach(function (x) { if (shown(x)) list.push(x); });
      } else list.push(ch);
    });
    return list;
  }
  function pieces(source, l) {
    if (Array.isArray(source)) {
      var many = [];
      source.forEach(function (one) { many = many.concat(pieces(one, l)); });
      return many;
    }
    if (source === 'page') {
      var ctx = {}, all = [];
      pageParts().forEach(function (el) { all = all.concat(resolve(el, l, ctx)); });
      return all.filter(function (p) { return p.text; });
    }
    return resolve(source, l, {}).filter(function (p) { return p.text; });
  }

  function audioUrl(p) {
    var h = hash(p.text);
    return MANIFEST[p.lang + ':' + h] ? 'audio/' + p.lang + '/' + h + '.m4a' : null;
  }

  /* ---------------- toast ---------------- */

  var toastTimer;
  function toast(msg, ms) {
    var t = document.querySelector('.toast');
    if (!t) {
      t = document.createElement('div');
      t.className = 'toast';
      t.setAttribute('role', 'status');
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.hidden = true; }, ms || 7000);
  }

  /* ---------------- player ---------------- */

  var session = 0;
  var cur = { btn: null, el: null };
  var timers = [];
  var live = [];
  function later(fn, ms) { var id = setTimeout(fn, ms); timers.push(id); return id; }
  function clearTimers() { timers.forEach(clearTimeout); timers = []; }

  function setOn(btn, on) {
    if (!btn) return;
    btn.classList.toggle('on', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    var icon = btn.querySelector('svg');
    if (icon && !btn.hasAttribute('data-keep-icon')) icon.outerHTML = on ? ICON_STOP : ICON_SPEAK;
    var lbl = btn.querySelector('.say-label');
    if (lbl) lbl.innerHTML = on ? '<b>Stop</b>रोकें' : lbl.getAttribute('data-idle');
  }
  function clearState() {
    if (cur.el) cur.el.classList.remove('reading');
    setOn(cur.btn, false);
    cur = { btn: null, el: null };
  }
  function stop() {
    session++;
    clearTimers();
    if (player) {
      /* only pause: emptying the source fires late events that could start a second voice */
      player.onplaying = player.onended = player.onerror = null;
      try { player.pause(); } catch (e) {}
    }
    if (HAS_TTS) { try { synth.cancel(); } catch (e) {} }
    live = [];
    clearState();
  }

  var lastPress = { btn: null, at: 0 };

  function speak(source, btn, highlight) {
    btn = btn || null;
    var now = Date.now();
    /* a shaky double tap on the same button counts as one tap */
    if (btn && lastPress.btn === btn && now - lastPress.at < 600) return;
    lastPress = { btn: btn, at: now };
    var wasSame = btn && cur.btn === btn;
    var ttsBusy = HAS_TTS && (synth.speaking || synth.pending);
    stop();
    if (wasSame) return;

    var list = pieces(source, lang);
    if (!list.length) return;

    var my = session;
    cur = { btn: btn, el: highlight || null };
    setOn(btn, true);
    if (highlight) highlight.classList.add('reading');

    var idx = 0;
    function done() { if (my !== session) return; clearTimers(); live = []; clearState(); }
    function next() {
      if (my !== session) return;
      if (idx >= list.length) { done(); return; }
      var p = list[idx++];
      var url = player ? audioUrl(p) : null;
      if (url) playFile(url, p); else playTts(p);
    }

    function playFile(url, p) {
      var started = false, fell = false;
      function mine() { return my === session && player.src && player.src.indexOf(url) !== -1; }
      function fallBack() {
        if (fell || started || my !== session) return;
        fell = true;
        player.onplaying = player.onended = player.onerror = null;
        try { player.pause(); } catch (e) {}
        playTts(p);
      }
      player.onplaying = function () { if (mine()) started = true; };
      player.onended = function () { if (mine()) { player.onended = null; next(); } };
      player.onerror = function () { if (mine()) fallBack(); };
      player.src = url;
      var pr;
      try { pr = player.play(); } catch (e) { pr = null; }
      if (pr && pr.catch) {
        pr.catch(function (err) {
          if (my !== session) return;
          if (err && err.name === 'NotAllowedError') { stop(); toast('Tap the speaker button again to play. · सुनने के लिए बटन फिर से दबाएँ।'); }
          else if (err && err.name !== 'AbortError') fallBack();
        });
      }
      /* slow network: if nothing has started after 12 seconds, use the phone's voice instead */
      later(function () { if (!started && player.paused && player.currentTime === 0) fallBack(); }, 12000);
    }

    function playTts(p) {
      if (my !== session) return;
      if (!HAS_TTS) { next(); return; }
      loadVoices();
      var voice = findVoice(p.lang);
      if (!voice && voices.length && p.lang !== 'en') {
        toast('This phone has no voice for this language, and this line has no recording. Add the language in phone Settings › Text-to-speech.', 9000);
      }
      var chunks = [];
      p.text.replace(/([.।?!])\s+/g, '$1\u0001').split('\u0001').forEach(function (s) {
        s = s.trim();
        while (s.length > 160) { var cut = s.lastIndexOf(' ', 150); if (cut < 50) cut = 150; chunks.push(s.slice(0, cut)); s = s.slice(cut).trim(); }
        if (s) chunks.push(s);
      });
      var i = 0, started = false, retried = false;
      function say1() {
        if (my !== session) return;
        if (i >= chunks.length) { next(); return; }
        var u = new SpeechSynthesisUtterance(chunks[i++]);
        u.lang = p.lang + '-IN';
        if (voice) u.voice = voice;
        u.rate = 0.9;
        u.onstart = function () { started = true; };
        u.onboundary = function () { started = true; };
        u.onend = function () { if (my === session) later(say1, 60); };
        u.onerror = function (e) {
          if (my !== session || (e && (e.error === 'interrupted' || e.error === 'canceled'))) return;
          later(say1, 60);
        };
        live.push(u);
        try { synth.resume(); } catch (e) {}
        synth.speak(u);
      }
      (function watch() {
        later(function () {
          /* some phones speak without reporting "start": if it is speaking, leave it alone */
          if (my !== session || started || synth.speaking) return;
          if (!retried) {
            retried = true;
            try { synth.cancel(); } catch (e) {}
            i = Math.max(0, i - 1);
            later(say1, 250);
            watch();
          } else {
            stop();
            toast('The voice is not starting on this browser. Check the volume and silent mode, or open the site in Chrome.', 9000);
          }
        }, 3500);
      })();
      if (voice && voice.localService === false && !IS_ANDROID) {
        (function keepAlive() {
          later(function () {
            if (my !== session) return;
            if (synth.speaking && !synth.paused) { synth.pause(); synth.resume(); }
            keepAlive();
          }, 9000);
        })();
      }
      if (ttsBusy) { ttsBusy = false; later(say1, 180); } else say1();
    }

    next();
  }

  /* ---------------- buttons ---------------- */

  function makeSay(target) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'say';
    b.setAttribute('aria-label', 'Listen · सुनें');
    b.setAttribute('aria-pressed', 'false');
    b.title = 'Listen · सुनें';
    b.innerHTML = ICON_SPEAK;
    b.addEventListener('click', function (ev) {
      ev.preventDefault();
      ev.stopPropagation();
      speak(target, b, target);
    });
    return b;
  }

  document.querySelectorAll(SPEAKABLE).forEach(function (el) {
    if (el.hasAttribute('data-no-say') || el.classList.contains('no-js')) return;
    el.insertBefore(makeSay(el), el.firstChild);
  });

  document.querySelectorAll('.bigsay').forEach(function (b) {
    b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', function () {
      var sel = b.getAttribute('data-read');
      if (sel === 'page') { speak('page', b, null); return; }
      var target = sel ? document.querySelector(sel) : b;
      speak(target, b, sel ? target : null);
    });
  });

  /* bottom bar: read the whole page */
  var slot = document.getElementById('listen-slot');
  if (slot) {
    slot.innerHTML = '';
    var lb = document.createElement('button');
    lb.type = 'button';
    lb.setAttribute('aria-pressed', 'false');
    var idle = '<b>Listen</b>पन्ना सुनें';
    lb.innerHTML = ICON_SPEAK + '<span class="say-label" data-idle="' + idle.replace(/"/g, '&quot;') + '">' + idle + '</span>';
    lb.addEventListener('click', function () { speak('page', lb, null); });
    slot.appendChild(lb);
  }

  /* ---------------- language choice ---------------- */

  function setLang(code, announce) {
    if (CODES.indexOf(code) === -1) return;
    lang = code;
    try { localStorage.setItem('ss-voice', lang); } catch (e) {}
    document.querySelectorAll('select.voice-select').forEach(function (s) { s.value = lang; });
    document.querySelectorAll('.langrow button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-l') === lang ? 'true' : 'false');
    });
    if (announce) speak(L.voiceChosen, null, null);
    try { document.dispatchEvent(new CustomEvent('ss-lang', { detail: lang })); } catch (e) {}
  }

  var vslot = document.getElementById('voice-slot');
  if (vslot) {
    vslot.className = 'voicepick';
    var sel = document.createElement('select');
    sel.className = 'voice-select';
    sel.setAttribute('aria-label', 'Voice language · आवाज़ की भाषा');
    L.langs.forEach(function (x) {
      var o = document.createElement('option');
      o.value = x.code;
      o.textContent = x.name;
      o.lang = x.code;
      sel.appendChild(o);
    });
    sel.value = lang;
    sel.addEventListener('change', function () { setLang(sel.value, true); });
    var lab = document.createElement('span');
    lab.textContent = 'Voice · आवाज़:';
    vslot.appendChild(lab);
    vslot.appendChild(sel);
  }

  /* big language buttons (home page and ask page) */
  document.querySelectorAll('.langrow').forEach(function (row) {
    L.langs.forEach(function (x) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('data-l', x.code);
      b.lang = x.code;
      b.textContent = x.name;
      b.setAttribute('aria-pressed', x.code === lang ? 'true' : 'false');
      b.addEventListener('click', function () { setLang(x.code, true); });
      row.appendChild(b);
    });
  });

  window.addEventListener('pagehide', stop);
  document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); });
  window.addEventListener('hashchange', stop);

  /* ---------------- shared with other scripts ---------------- */

  window.ssSpeak = function (obj, btn) { speak(obj, btn || null, null); };
  window.ssStop = stop;
  window.ssLang = function () { return lang; };
  window.ssSetLang = setLang;
  window.ssToast = toast;
  window.SS_PHRASES = window.SS_PHRASES || [];

  /* lists every sentence a page can speak and where its recording is; useful for testing */
  window.ssDebug = {
    hash: hash,
    pieces: pieces,
    audioUrl: audioUrl,
    collect: function () {
      var out = [];
      function add(list) { list.forEach(function (p) { if (p.text) out.push({ lang: p.lang, text: p.text, hash: hash(p.text) }); }); }
      CODES.forEach(function (l) {
        document.querySelectorAll(SPEAKABLE).forEach(function (el) {
          if (el.hasAttribute('data-no-say') || el.classList.contains('no-js')) return;
          add(resolve(el, l, { noticed: true }));
        });
        document.querySelectorAll('.bigsay').forEach(function (b) {
          var s = b.getAttribute('data-read');
          if (s === 'page') return;   /* the whole page is collected just below */
          add(resolve(s ? document.querySelector(s) : b, l, { noticed: true }));
        });
        add(pieces('page', l));
        add(resolve(L.voiceChosen, l));
        if (L.otherLang[l]) add([{ lang: l, text: finalText(L.otherLang[l]) }]);
        (window.SS_PHRASES || []).forEach(function (ph) { add(resolve(ph, l)); });
      });
      return out;
    }
  };
})();
