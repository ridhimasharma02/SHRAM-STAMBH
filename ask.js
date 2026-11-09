/* SHRAM STAMBH - ask a question by voice, hear the answer.

   1. The user picks a language and presses the microphone.
   2. The browser turns speech into text (Chrome uses Google's service, Safari
      uses Apple's; this site itself stores nothing).
   3. The text is matched against 16 common worker problems using keywords in
      seven languages, and the answer is shown and spoken from a recording.
   If the microphone is not available, the same answers come from tapping a
   picture question or typing. */
(function () {
  'use strict';

  var DATA = window.SS_ASK;
  var rootEl = document.getElementById('ask-root');
  if (!DATA || !rootEl) return;

  var $ = function (id) { return document.getElementById(id); };
  var micBtn = $('mic'), micLabel = $('mic-label'), msgEl = $('ask-msg');
  var heardBox = $('heard'), heardText = $('heard-text');
  var answerBox = $('answer'), answerText = $('answer-text'), answerActs = $('answer-actions');
  var typeInput = $('type-input');
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var byId = {};
  DATA.topics.forEach(function (t) { byId[t.id] = t; });
  var FALLBACK = { id: 'fallback', answer: DATA.ui.fallback, calls: ['15100'], link: 'help.html' };

  /* phrases spoken by this page, so tools/make_audio.py records them */
  window.SS_PHRASES = window.SS_PHRASES || [];
  ['noMic', 'micBlocked', 'noSpeech', 'network', 'howTo', 'fallback'].forEach(function (k) { window.SS_PHRASES.push(DATA.ui[k]); });
  DATA.topics.forEach(function (t) { window.SS_PHRASES.push(t.answer); });

  function lang() { return window.ssLang ? window.ssLang() : 'hi'; }
  function ui(key) { var l = lang(); return (DATA.ui[key] && (DATA.ui[key][l] || DATA.ui[key].en)) || ''; }
  function langInfo() { var l = lang(); for (var i = 0; i < DATA.langs.length; i++) if (DATA.langs[i].code === l) return DATA.langs[i]; return DATA.langs[0]; }
  function speak(obj, btn) { if (window.ssSpeak) window.ssSpeak(obj, btn); }

  /* ---------------- matching ---------------- */

  function norm(s) {
    return (' ' + String(s || '') + ' ')
      .normalize('NFC')
      .toLowerCase()
      .replace(/[़়‌‍]/g, '')   /* nukta dots, zero-width joiners */
      .replace(/ँ/g, 'ं')                 /* chandrabindu -> anusvara */
      .replace(/[.,!?;:'"“”‘’()।॥-]/g, ' ')
      .replace(/\s+/g, ' ');
  }
  var normCache = {};
  function normalised(s) { return normCache[s] || (normCache[s] = norm(s).trim()); }
  function hasAny(q, list) {
    for (var i = 0; i < list.length; i++) { var k = normalised(list[i]); if (k && q.indexOf(k) !== -1) return true; }
    return false;
  }
  function countHits(q, list) {
    var c = 0;
    for (var i = 0; i < list.length; i++) { var k = normalised(list[i]); if (k && q.indexOf(k) !== -1) c++; }
    return c;
  }
  function score(q, t) {
    var s = countHits(q, t.kw) * 2 + countHits(q, t.weak || []);
    (t.combos || []).forEach(function (combo) {
      if (combo.every(function (c) { return hasAny(q, DATA.concepts[c]); })) s += 3;
    });
    return s;
  }
  function match(text) {
    var q = norm(text);
    var best = null, bestScore = 0;
    DATA.matchOrder.forEach(function (id) {
      var s = score(q, byId[id]);
      if (s > bestScore) { best = byId[id]; bestScore = s; }
    });
    return { topic: best, score: bestScore };
  }

  /* ---------------- showing an answer ---------------- */

  var current = null;   /* {topic, asked} so a language change can re-show it */

  function show(topic, asked, speakNow) {
    current = { topic: topic, asked: asked };
    var t = topic || FALLBACK;
    var l = lang();

    if (asked) {
      heardBox.hidden = false;
      heardBox.querySelector('.lbl').textContent = ui('youAsked');
      heardText.textContent = asked;
    } else {
      heardBox.hidden = true;
    }

    answerBox.hidden = false;
    answerBox.className = 'answerbox' + (topic ? '' : ' unknown');
    answerBox.querySelector('.lbl').textContent = ui('answer') + (topic && topic.label ? ' · ' + (topic.label[l] || topic.label.en) : '');
    answerText.textContent = t.answer[l] || t.answer.hi;
    answerText.lang = t.answer[l] ? l : 'hi';

    answerActs.innerHTML = '';
    var again = document.createElement('button');
    again.type = 'button';
    again.className = 'btn dark';
    again.textContent = ui('hearAgain');
    again.addEventListener('click', function () { speak(t.answer, again); });
    answerActs.appendChild(again);
    (t.calls || []).forEach(function (num) {
      var a = document.createElement('a');
      a.className = 'callbtn slim' + (num === '112' ? ' red' : '');
      a.href = 'tel:' + num;
      a.textContent = ui('call') + ' ' + num;
      answerActs.appendChild(a);
    });
    if (t.link) {
      var more = document.createElement('a');
      more.className = 'btn';
      more.href = t.link;
      more.textContent = ui('openPage');
      answerActs.appendChild(more);
    }
    if (speakNow) speak(t.answer, again);
    answerBox.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  function message(key, speakNow) {
    msgEl.setAttribute('data-key', key || '');
    msgEl.hidden = !key;
    if (!key) return;
    msgEl.textContent = ui(key);
    if (speakNow) speak(DATA.ui[key]);
  }

  /* ---------------- labels in the chosen language ---------------- */

  function relabel() {
    var l = lang();
    rootEl.setAttribute('data-lang', l);
    document.querySelectorAll('[data-ui]').forEach(function (el) { el.textContent = ui(el.getAttribute('data-ui')); });
    micLabel.textContent = listening ? ui('listening') : ui('micIdle');
    typeInput.placeholder = ui('typeHere');
    document.querySelectorAll('.qbtn').forEach(function (b) {
      var t = byId[b.getAttribute('data-topic')];
      var lab = b.querySelector('.qlabel');
      lab.textContent = t.label[l] || t.label.en;
      lab.lang = l;
    });
    var how = $('how-say');
    if (how) DATA.langs.forEach(function (x) { how.setAttribute('data-say-' + x.code, DATA.ui.howTo[x.code]); });
    if (current) show(current.topic, current.asked, false);
    if (!msgEl.hidden && msgEl.getAttribute('data-key')) message(msgEl.getAttribute('data-key'), false);
  }
  document.addEventListener('ss-lang', relabel);

  /* ---------------- picture questions and typing ---------------- */

  document.querySelectorAll('.qbtn').forEach(function (b) {
    b.addEventListener('click', function () {
      stopListening();
      message(null);
      var t = byId[b.getAttribute('data-topic')];
      show(t, null, true);
    });
  });

  $('type-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var q = typeInput.value.trim();
    if (!q) { typeInput.focus(); return; }
    stopListening();
    message(null);
    var m = match(q);
    show(m.topic, q, true);
  });

  /* ---------------- microphone ---------------- */

  var rec = null, listening = false, gotResult = false, failed = false;

  function beep() {
    try {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      var ctx = beep.ctx || (beep.ctx = new AC());
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.value = 880;
      g.gain.setValueAtTime(0.15, ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);
      o.connect(g); g.connect(ctx.destination);
      o.start(); o.stop(ctx.currentTime + 0.2);
    } catch (e) { /* no sound is fine */ }
  }

  function setListening(on) {
    listening = on;
    micBtn.classList.toggle('listening', on);
    micBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    micLabel.textContent = on ? ui('listening') : ui('micIdle');
  }

  function stopListening() {
    if (rec && listening) { try { rec.abort(); } catch (e) {} }
    setListening(false);
  }

  function fail(key) {
    failed = true;
    setListening(false);
    msgEl.setAttribute('data-key', key);
    message(key, true);
  }

  micBtn.addEventListener('click', function () {
    if (listening) { stopListening(); return; }
    if (window.ssStop) window.ssStop();
    message(null);
    var SRnow = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SRnow) { fail('noMic'); $('qgrid').scrollIntoView({ block: 'nearest', behavior: 'smooth' }); return; }

    rec = new SRnow();
    rec.lang = langInfo().rec;
    rec.interimResults = true;
    rec.maxAlternatives = 3;
    rec.continuous = false;
    gotResult = false;
    failed = false;

    rec.onresult = function (ev) {
      if (gotResult) return;   /* some phones send the final result twice */
      var finalAlts = null, interim = '';
      for (var i = ev.resultIndex; i < ev.results.length; i++) {
        var r = ev.results[i];
        if (r.isFinal) {
          finalAlts = [];
          for (var a = 0; a < r.length; a++) finalAlts.push(r[a].transcript);
        } else interim += r[0].transcript;
      }
      if (interim) {
        heardBox.hidden = false;
        heardBox.querySelector('.lbl').textContent = ui('youAsked');
        heardText.textContent = interim + '…';
      }
      if (finalAlts && finalAlts.length) {
        gotResult = true;
        /* pick whichever of the recogniser's guesses matches a topic best */
        var best = { topic: null, score: 0 }, said = finalAlts[0];
        finalAlts.forEach(function (alt) {
          var m = match(alt);
          if (m.score > best.score) { best = m; said = alt; }
        });
        setListening(false);
        show(best.topic, said, true);
      }
    };
    rec.onerror = function (ev) {
      var e = ev && ev.error;
      if (e === 'aborted') return;
      if (e === 'not-allowed' || e === 'service-not-allowed' || e === 'audio-capture') fail('micBlocked');
      else if (e === 'network') fail('network');
      else if (e === 'no-speech') fail('noSpeech');
      else if (e === 'language-not-supported') fail('noMic');
      else fail('noSpeech');
    };
    rec.onend = function () {
      if (listening && !gotResult && !failed) fail('noSpeech');
      setListening(false);
    };

    try {
      rec.start();
      setListening(true);
      beep();
    } catch (e) {
      fail('noMic');
    }
  });

  if (!SR) rootEl.classList.add('no-sr');
  relabel();

  /* for testing */
  window.ssAsk = { match: match, norm: norm };
})();
