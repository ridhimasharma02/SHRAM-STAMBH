/* SHRAM STAMBH - the login screen. Every page needs a login.

   Steps (only one shows at a time):
     s-who      "Who are you?"  tap your picture, or make a new account
     s-avatar   new account: pick a picture
     s-details  name and mobile number (both required). The name can be
                spoken into the microphone instead of typed.
     s-secret   tap four secret pictures (twice when creating)
     s-in       logged in: continue, go to the diary or notebook, log out
   Every step speaks its instruction in the chosen language. Secret taps are
   never spoken aloud, so someone standing nearby cannot hear the code. */
(function () {
  'use strict';

  var DATA = window.SS_ACCOUNT, ACC = window.ssAccount;
  var $ = function (id) { return document.getElementById(id); };
  var root = $('login-root');
  if (!DATA || !ACC || !root) return;

  var STEPS = ['s-who', 's-avatar', 's-details', 's-secret', 's-in'];
  var state;
  var lockTimer = null;

  /* where to go after logging in: only one of our own pages */
  var next = (new URLSearchParams(location.search).get('next') || '');
  if (!/^[a-z-]+\.html(#[a-z-]+)?$/.test(next) || next === 'login.html') next = '';

  function textFor(key) { return ACC.text(key); }
  function say(keys) {
    if (!window.ssSpeak) return;
    var list = (Array.isArray(keys) ? keys : [keys]).map(function (k) { return DATA.text[k]; });
    window.ssSpeak(list.length === 1 ? list[0] : list);
  }
  function show(step) {
    STEPS.forEach(function (id) { $(id).hidden = id !== step; });
    root.setAttribute('data-step', step);
    var top = root.getBoundingClientRect().top + window.scrollY - 12;
    if (window.scrollY > top) window.scrollTo(0, top);
  }
  function relabel() {
    root.querySelectorAll('[data-t]').forEach(function (el) { el.textContent = textFor(el.getAttribute('data-t')); });
    if (state) $('secret-title').textContent = textFor(state.titleKey);
    var msg = $('det-msg');
    if (!msg.hidden && msg.getAttribute('data-key')) msg.textContent = textFor(msg.getAttribute('data-key'));
  }
  document.addEventListener('ss-lang', relabel);

  /* ---------------- step 1: who are you ---------------- */

  function renderWho() {
    var list = $('who-list');
    list.innerHTML = '';
    ACC.profiles().forEach(function (p) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'who-btn';
      b.innerHTML = ACC.avatarHtml(p.avatar) + '<span class="who-label"></span>';
      b.querySelector('.who-label').textContent = p.name || '';
      b.setAttribute('aria-label', p.name || 'Account');
      b.addEventListener('click', function () {
        state.mode = 'login';
        state.profile = p.id;
        state.avatar = p.avatar;
        startSecret('enterSecret');
      });
      list.appendChild(b);
    });
  }

  $('btn-new').addEventListener('click', function () { startCreate(true); });

  /* ---------------- step 2: new account picture ---------------- */

  function startCreate(speak) {
    state.mode = 'create';
    state.avatar = null;
    state.first = null;
    state.name = '';
    state.mobile = '';
    renderAvatars();
    $('av-next').disabled = true;
    $('av-back').hidden = ACC.profiles().length === 0;
    show('s-avatar');
    if (speak) say('choosePic');
  }

  function renderAvatars() {
    var used = ACC.profiles().map(function (p) { return p.avatar; });
    var grid = $('avatar-grid');
    grid.innerHTML = '';
    DATA.avatars.forEach(function (a) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pick-btn';
      b.setAttribute('aria-pressed', 'false');
      b.setAttribute('aria-label', a.name);
      b.innerHTML = ACC.avatarHtml(a.id, 'lg');
      /* pictures already taken on this phone are dimmed so people stay easy to tell apart */
      if (used.indexOf(a.id) !== -1 && used.length < DATA.avatars.length) { b.disabled = true; b.classList.add('taken'); }
      b.addEventListener('click', function () {
        state.avatar = a.id;
        grid.querySelectorAll('.pick-btn').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        $('av-next').disabled = false;
      });
      grid.appendChild(b);
    });
  }

  $('av-back').addEventListener('click', function () { init(false); });
  $('av-next').addEventListener('click', function () {
    if (!state.avatar) return;
    startDetails(true);
  });

  /* ---------------- step 3: name and mobile number ---------------- */

  function startDetails(speak) {
    var p = state.mode === 'complete' ? ACC.current() : null;
    $('name').value = state.name || (p && p.name) || '';
    $('mobile').value = state.mobile || (p && p.mobile) || '';
    $('det-avatar').innerHTML = ACC.avatarHtml(state.avatar, 'md');
    $('det-back').hidden = state.mode === 'complete';
    detMessage(null);
    stopNameMic();
    show('s-details');
    if (speak) say('detailsPrompt');
  }

  function detMessage(key) {
    var msg = $('det-msg');
    msg.setAttribute('data-key', key || '');
    msg.hidden = !key;
    if (key) msg.textContent = textFor(key);
  }

  $('det-back').addEventListener('click', function () {
    stopNameMic();
    state.name = $('name').value;
    state.mobile = $('mobile').value;
    show('s-avatar');
  });

  $('details-form').addEventListener('submit', function (e) {
    e.preventDefault();
    stopNameMic();
    var name = $('name').value, mobile = $('mobile').value;
    var ownId = state.mode === 'complete' ? state.profile : null;
    var problem = !ACC.validName(name) ? 'nameNeeded'
      : !ACC.cleanMobile(mobile) ? 'mobileNeeded'
      : ACC.mobileTaken(mobile, ownId) ? 'mobileTaken' : null;
    $('name').classList.toggle('bad', problem === 'nameNeeded');
    $('mobile').classList.toggle('bad', problem === 'mobileNeeded' || problem === 'mobileTaken');
    if (problem) {
      detMessage(problem);
      say(problem);
      (problem === 'nameNeeded' ? $('name') : $('mobile')).focus();
      return;
    }
    state.name = name;
    state.mobile = mobile;
    if (state.mode === 'complete') {
      ACC.update(state.profile, { name: name, mobile: mobile });
      say('welcome');
      goIn();
      return;
    }
    state.first = null;
    startSecret('chooseSecret');
  });

  /* say your name instead of typing it */
  var nameRec = null, nameListening = false;
  function stopNameMic() {
    if (nameRec && nameListening) { try { nameRec.abort(); } catch (e) {} }
    setNameMic(false);
  }
  function setNameMic(on) {
    nameListening = on;
    var b = $('name-mic');
    b.classList.toggle('listening', on);
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    b.querySelector('[data-t]').textContent = on ? textFor('listeningShort') : textFor('sayName');
  }
  $('name-mic').addEventListener('click', function () {
    if (nameListening) { stopNameMic(); return; }
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { detMessage('micUnavailable'); say('micUnavailable'); return; }
    if (window.ssStop) window.ssStop();
    var code = window.ssLang ? window.ssLang() : 'hi';
    var info = (window.SS_LANG && window.SS_LANG.langs || []).filter(function (x) { return x.code === code; })[0];
    nameRec = new SR();
    nameRec.lang = info ? info.rec : 'hi-IN';
    nameRec.interimResults = true;
    nameRec.maxAlternatives = 1;
    nameRec.onresult = function (ev) {
      var text = '';
      for (var i = 0; i < ev.results.length; i++) text += ev.results[i][0].transcript;
      $('name').value = text.replace(/[.,!?।]/g, '').trim().slice(0, 40);
      $('name').classList.remove('bad');
      if (ev.results[ev.results.length - 1].isFinal) { setNameMic(false); detMessage(null); }
    };
    nameRec.onerror = function (ev) {
      setNameMic(false);
      if (ev && ev.error === 'aborted') return;
      detMessage('micUnavailable');
      say('micUnavailable');
    };
    nameRec.onend = function () { setNameMic(false); };
    try { nameRec.start(); setNameMic(true); }
    catch (e) { setNameMic(false); detMessage('micUnavailable'); say('micUnavailable'); }
  });

  /* ---------------- step 4: secret pictures ---------------- */

  function startSecret(titleKey) {
    state.entry = [];
    state.busy = false;
    state.titleKey = titleKey;
    $('secret-title').textContent = textFor(titleKey);
    $('secret-avatar').innerHTML = ACC.avatarHtml(state.avatar, 'md');
    $('forgot-wrap').hidden = state.mode !== 'login';
    $('forgot-box').hidden = true;
    $('forgot-yes').hidden = true;
    drawDots();
    show('s-secret');
    if (state.mode === 'login' && ACC.lockedFor(state.profile)) { startLock(); say('locked'); return; }
    stopLock();
    say(titleKey);
  }

  function drawDots() {
    var dots = $('dots').children;
    for (var i = 0; i < dots.length; i++) dots[i].classList.toggle('filled', i < state.entry.length);
    $('dots-live').textContent = state.entry.length + ' / 4';
  }

  function buildSecretGrid() {
    var grid = $('secret-grid');
    DATA.secrets.forEach(function (s) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'secret-btn c-' + s.color;
      b.setAttribute('aria-label', s.name);
      b.innerHTML = s.svg;
      b.addEventListener('click', function () { tapSecret(s.id, b); });
      grid.appendChild(b);
    });
  }

  function vibrate(p) { if (navigator.vibrate && navigator.userActivation && navigator.userActivation.isActive) { try { navigator.vibrate(p); } catch (e) {} } }

  function tapSecret(id, btn) {
    if (state.busy || state.entry.length >= 4) return;
    state.entry.push(id);
    btn.classList.add('flash');
    setTimeout(function () { btn.classList.remove('flash'); }, 180);
    vibrate(25);
    drawDots();
    if (state.entry.length === 4) { state.busy = true; setTimeout(evaluate, 250); }
  }

  function shake() {
    var g = $('secret-grid');
    g.classList.remove('wrong');
    void g.offsetWidth;
    g.classList.add('wrong');
    vibrate([60, 40, 60]);
  }

  function evaluate() {
    var seq = state.entry.slice();
    if (state.mode === 'create') {
      if (!state.first) {
        state.first = seq;
        startSecret('repeatSecret');
        return;
      }
      if (state.first.join() !== seq.join()) {
        state.first = null;
        shake();
        state.titleKey = 'chooseSecret';
        state.entry = [];
        state.busy = false;
        $('secret-title').textContent = textFor('chooseSecret');
        drawDots();
        say('mismatch');
        return;
      }
      ACC.create(state.avatar, state.name, state.mobile, seq).then(function (r) {
        say(r.moved ? ['created', 'movedGuest'] : 'created');
        goIn();
      }).catch(function (err) {
        state.busy = false;
        if (err && err.message === 'taken') { startDetails(false); detMessage('mobileTaken'); say('mobileTaken'); return; }
        if (err && err.message === 'details') { startDetails(false); say('detailsPrompt'); return; }
        if (window.ssToast) window.ssToast('This phone is not letting the site save. Check that private browsing is off.');
      });
      return;
    }
    ACC.verify(state.profile, seq).then(function (res) {
      if (res === 'ok') {
        /* accounts from before details were required must add them now */
        if (!ACC.isComplete(ACC.current())) { state.mode = 'complete'; startDetails(true); return; }
        say('welcome');
        goIn();
        return;
      }
      state.entry = [];
      state.busy = false;
      drawDots();
      shake();
      if (res === 'locked') { startLock(); say('locked'); }
      else say('wrong');
    });
  }

  function startLock() {
    stopLock();
    $('secret-grid').classList.add('locked');
    var msg = $('lock-msg');
    msg.hidden = false;
    (function tick() {
      var s = ACC.lockedFor(state.profile);
      if (!s) { stopLock(); return; }
      msg.textContent = textFor('locked') + '  ' + s;
      lockTimer = setTimeout(tick, 1000);
    })();
  }
  function stopLock() {
    clearTimeout(lockTimer);
    $('secret-grid').classList.remove('locked');
    $('lock-msg').hidden = true;
  }

  $('sec-clear').addEventListener('click', function () {
    if (state.busy) return;
    state.entry = [];
    drawDots();
  });
  $('sec-back').addEventListener('click', function () {
    stopLock();
    if (state.mode === 'create') {
      if (state.first) { state.first = null; startSecret('chooseSecret'); }
      else startDetails(false);
    } else init(false);
  });

  /* forgot the pictures: the only way out is to remove that account */
  $('forgot-link').addEventListener('click', function () {
    var box = $('forgot-box');
    box.hidden = !box.hidden;
    $('forgot-yes').hidden = true;
    if (!box.hidden) say('forgotInfo');
  });
  $('forgot-remove').addEventListener('click', function () { $('forgot-yes').hidden = false; });
  $('forgot-yes').addEventListener('click', function () {
    ACC.remove(state.profile);
    say('removed');
    init(false);
  });

  /* ---------------- step 5: logged in ---------------- */

  function maskMobile(m) { return m ? m.slice(0, 2) + '••••••' + m.slice(-2) : ''; }

  function goIn() {
    var c = ACC.current();
    if (!c) { init(false); return; }
    stopLock();
    $('in-avatar').innerHTML = ACC.avatarHtml(c.avatar, 'xl');
    $('in-name').textContent = c.name || '';
    $('in-mobile').textContent = maskMobile(c.mobile);
    var cont = $('in-continue');
    cont.href = next || 'index.html';
    $('in-remove-yes').hidden = true;
    show('s-in');
  }

  $('in-logout').addEventListener('click', function () {
    ACC.logout();
    say('loggedOut');
    init(false);
  });
  $('in-remove').addEventListener('click', function () { $('in-remove-yes').hidden = false; say('forgotInfo'); });
  $('in-remove-yes').addEventListener('click', function () {
    var c = ACC.current();
    if (c) ACC.remove(c.id);
    say('removed');
    init(false);
  });

  /* ---------------- start ---------------- */

  function init(speak) {
    state = { mode: null, profile: null, avatar: null, name: '', mobile: '', first: null, entry: [], busy: false, titleKey: 'enterSecret' };
    var c = ACC.current();
    if (c) {
      if (!ACC.isComplete(c)) { state.mode = 'complete'; state.profile = c.id; state.avatar = c.avatar; startDetails(speak); return; }
      goIn();
      return;
    }
    if (ACC.profiles().length) {
      renderWho();
      show('s-who');
      if (speak) say('whoAreYou');
    } else startCreate(speak);
  }

  buildSecretGrid();
  init(false);
  relabel();

  /* for testing */
  window.ssLogin = { state: function () { return state; } };
})();
