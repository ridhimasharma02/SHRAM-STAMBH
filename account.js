/* SHRAM STAMBH - picture login that lives only on this phone.

   Why: workers often share one phone. An account keeps each person's work
   diary and contractor notes separate and private. There is no server, so
   accounts never leave the phone and cannot be reset by anyone.

   How it is stored (localStorage):
     ss-profiles  [{id, avatar, name, mobile, salt, hash, created}]
                  name and a 10-digit mobile number are required to make an account
                  hash = SHA-256(salt + ":" + the four secret picture ids)
                  The secret pictures themselves are never stored.
     ss-locks     wrong-try counters, for the one-minute lockout
   The logged-in account is kept in sessionStorage, so closing the browser
   logs the person out. It also logs out by itself after 30 minutes unused. */
(function () {
  'use strict';

  var DATA = window.SS_ACCOUNT;
  if (!DATA) return;

  var PKEY = 'ss-profiles', SKEY = 'ss-session', LKEY = 'ss-locks';
  var PERSONAL = ['shramik-diary-v1', 'shramik-contractors-v1'];
  var MAX_TRIES = 5, LOCK_MS = 60000;

  /* every fixed sentence the login speaks, so tools/make_audio.py records it */
  window.SS_PHRASES = window.SS_PHRASES || [];
  ['whoAreYou', 'choosePic', 'detailsPrompt', 'nameNeeded', 'mobileNeeded', 'mobileTaken', 'micUnavailable', 'chooseSecret', 'repeatSecret', 'mismatch', 'created', 'movedGuest',
   'enterSecret', 'wrong', 'locked', 'welcome', 'loggedOut', 'forgotInfo', 'removed', 'needLogin', 'intro']
    .forEach(function (k) { window.SS_PHRASES.push(DATA.text[k]); });

  /* ---------------- storage helpers ---------------- */

  function read(k, store) {
    try { return JSON.parse((store || localStorage).getItem(k)); } catch (e) { return null; }
  }
  function write(k, v, store) {
    try { (store || localStorage).setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; }
  }
  function drop(k, store) { try { (store || localStorage).removeItem(k); } catch (e) {} }

  function profiles() { var p = read(PKEY); return Array.isArray(p) ? p : []; }
  function byId(id) { return profiles().filter(function (x) { return x.id === id; })[0] || null; }
  /* shared phones: log out by itself after 30 minutes without use */
  var IDLE_MS = 30 * 60 * 1000, TKEY = 'ss-last';
  function current() {
    var id = read(SKEY, sessionStorage);
    if (!id) return null;
    var last = read(TKEY, sessionStorage);
    if (last && Date.now() - last > IDLE_MS) { drop(SKEY, sessionStorage); drop(TKEY, sessionStorage); return null; }
    return byId(id);
  }
  var touched = 0;
  function touch() {
    var now = Date.now();
    if (now - touched < 15000 || !read(SKEY, sessionStorage)) return;
    touched = now;
    write(TKEY, now, sessionStorage);
  }
  ['pointerdown', 'keydown', 'scroll'].forEach(function (ev) { window.addEventListener(ev, touch, { passive: true }); });

  /* personal data is saved under "name:accountid" once someone logs in */
  function key(base) { var c = current(); return c ? base + ':' + c.id : base; }
  function isGated() { return profiles().length > 0 && !current(); }

  /* ---------------- secret code checking ---------------- */

  function hex(bytes) {
    var out = '';
    for (var i = 0; i < bytes.length; i++) out += ('0' + bytes[i].toString(16)).slice(-2);
    return out;
  }
  function randomHex(n) {
    var a = new Uint8Array(n);
    if (window.crypto && crypto.getRandomValues) crypto.getRandomValues(a);
    else for (var i = 0; i < n; i++) a[i] = Math.floor(Math.random() * 256);
    return hex(a);
  }
  function fnv(s) {
    var h = 0x811c9dc5;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
    return h.toString(16);
  }
  function digest(salt, seq) {
    var msg = salt + ':' + seq.join(',');
    if (window.crypto && crypto.subtle && window.TextEncoder) {
      return crypto.subtle.digest('SHA-256', new TextEncoder().encode(msg))
        .then(function (buf) { return hex(new Uint8Array(buf)); });
    }
    /* older browsers without crypto.subtle: weaker, but still not the plain code */
    return Promise.resolve('fnv:' + fnv(msg) + fnv(msg + salt));
  }

  /* ---------------- account actions ---------------- */

  /* Indian mobile numbers: 10 digits starting 6-9. "+91 98765 43210" and "098765..." are accepted. */
  function cleanMobile(v) {
    var d = String(v || '').replace(/[^0-9]/g, '');
    if (d.length === 12 && d.indexOf('91') === 0) d = d.slice(2);
    if (d.length === 11 && d.charAt(0) === '0') d = d.slice(1);
    return /^[6-9][0-9]{9}$/.test(d) ? d : '';
  }
  function cleanName(v) { return String(v || '').replace(/\s+/g, ' ').trim().slice(0, 40); }
  function validName(v) { return cleanName(v).replace(/[^\p{L}\p{M}]/gu, '').length >= 2; }
  function mobileTaken(mobile, exceptId) {
    var m = cleanMobile(mobile);
    return !!m && profiles().some(function (p) { return p.mobile === m && p.id !== exceptId; });
  }
  function isComplete(p) { return !!(p && validName(p.name) && cleanMobile(p.mobile)); }

  function create(avatar, name, mobile, seq) {
    var before = profiles();
    var id = 'u' + randomHex(6);
    var salt = randomHex(16);
    if (!validName(name) || !cleanMobile(mobile)) return Promise.reject(new Error('details'));
    if (mobileTaken(mobile)) return Promise.reject(new Error('taken'));
    return digest(salt, seq).then(function (h) {
      var list = profiles();
      list.push({ id: id, avatar: avatar, name: cleanName(name), mobile: cleanMobile(mobile), salt: salt, hash: h, created: Date.now() });
      if (!write(PKEY, list)) throw new Error('storage');
      /* the very first account takes over any diary or notes saved before accounts existed */
      var moved = false;
      if (before.length === 0) {
        PERSONAL.forEach(function (base) {
          try {
            var v = localStorage.getItem(base);
            if (v != null) { localStorage.setItem(base + ':' + id, v); localStorage.removeItem(base); moved = true; }
          } catch (e) {}
        });
      }
      login(id);
      return { id: id, moved: moved };
    });
  }

  function lockedFor(id) {
    var l = (read(LKEY) || {})[id];
    return l && l.until > Date.now() ? Math.ceil((l.until - Date.now()) / 1000) : 0;
  }

  /* resolves to 'ok', 'wrong' or 'locked' */
  function verify(id, seq) {
    var p = byId(id);
    if (!p) return Promise.resolve('wrong');
    if (lockedFor(id)) return Promise.resolve('locked');
    return digest(p.salt, seq).then(function (h) {
      var locks = read(LKEY) || {};
      if (h === p.hash) {
        delete locks[id];
        write(LKEY, locks);
        login(id);
        return 'ok';
      }
      var l = locks[id] || { fails: 0, until: 0 };
      l.fails += 1;
      var res = 'wrong';
      if (l.fails >= MAX_TRIES) { l.fails = 0; l.until = Date.now() + LOCK_MS; res = 'locked'; }
      locks[id] = l;
      write(LKEY, locks);
      return res;
    });
  }

  /* accounts made before details were required add them on next login */
  function update(id, fields) {
    var list = profiles();
    list.forEach(function (p) {
      if (p.id !== id) return;
      if (fields.name != null) p.name = cleanName(fields.name);
      if (fields.mobile != null) p.mobile = cleanMobile(fields.mobile);
    });
    var ok = write(PKEY, list);
    renderHeader();
    return ok;
  }

  function login(id) {
    write(SKEY, id, sessionStorage);
    write(TKEY, Date.now(), sessionStorage);
    renderHeader();
    announce();
  }
  function logout() {
    drop(SKEY, sessionStorage);
    drop(TKEY, sessionStorage);
    renderHeader();
    announce();
  }
  function remove(id) {
    write(PKEY, profiles().filter(function (x) { return x.id !== id; }));
    PERSONAL.forEach(function (base) { drop(base + ':' + id); });
    var locks = read(LKEY) || {};
    delete locks[id];
    write(LKEY, locks);
    if (read(SKEY, sessionStorage) === id) drop(SKEY, sessionStorage);
    renderHeader();
    announce();
  }
  function announce() {
    try { document.dispatchEvent(new CustomEvent('ss-account')); } catch (e) {}
  }

  /* ---------------- pictures ---------------- */

  function avatarInfo(id) { return DATA.avatars.filter(function (a) { return a.id === id; })[0] || DATA.avatars[0]; }
  function avatarHtml(id, cls) {
    var a = avatarInfo(id);
    return '<span class="avatar c-' + a.color + (cls ? ' ' + cls : '') + '" aria-hidden="true">' + a.svg + '</span>';
  }

  /* ---------------- header button ---------------- */

  function t(k) {
    var l = window.ssLang ? window.ssLang() : 'hi';
    return DATA.text[k][l] || DATA.text[k].en;
  }

  function renderHeader() {
    var slot = document.getElementById('account-slot');
    if (!slot) return;
    var c = current();
    slot.innerHTML = '';
    if (!c) {
      var a = document.createElement('a');
      a.className = 'account-link';
      a.href = 'login.html';
      a.innerHTML = DATA.lockSvg + '<span>Log in<span class="hi" lang="hi">लॉग इन</span></span>';
      slot.appendChild(a);
      return;
    }
    var who = document.createElement('a');
    who.className = 'account-who';
    who.href = 'login.html';
    who.innerHTML = avatarHtml(c.avatar, 'sm') + '<span class="who-name"></span>';
    who.querySelector('.who-name').textContent = c.name || '';
    who.setAttribute('aria-label', 'Your account' + (c.name ? ': ' + c.name : ''));
    var out = document.createElement('button');
    out.type = 'button';
    out.className = 'account-out';
    out.innerHTML = 'Log out<span class="hi" lang="hi">लॉग आउट</span>';
    out.addEventListener('click', function () {
      logout();
      if (window.ssSpeak) window.ssSpeak(DATA.text.loggedOut);
      /* every page needs a login, so go back to the login page after saying goodbye */
      if (!document.getElementById('login-root')) setTimeout(function () { location.replace('login.html'); }, 1500);
    });
    slot.appendChild(who);
    slot.appendChild(out);
  }

  /* on the diary and notebook: hide private parts, show "log in to see" */
  function showGate() {
    document.querySelectorAll('[data-private]').forEach(function (el) { el.hidden = true; });
    document.querySelectorAll('.login-gate').forEach(function (el) { el.hidden = false; });
  }

  window.ssAccount = {
    profiles: profiles, current: current, key: key, isGated: isGated,
    create: create, verify: verify, lockedFor: lockedFor, login: login, logout: logout, remove: remove,
    update: update, cleanMobile: cleanMobile, validName: validName, mobileTaken: mobileTaken, isComplete: isComplete,
    avatarHtml: avatarHtml, showGate: showGate, text: t
  };

  renderHeader();
  document.addEventListener('ss-lang', renderHeader);
})();
