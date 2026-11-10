/* SHRAM STAMBH - work diary: tap days worked, add money received, see what is owed.

   Parts of this file, in order:
     storage          load and save the diary
     helpers          dates, rupees, element lookup
     fields           daily wage and employer details
     calendar         tap a day: full, then half, then cleared
     totals           days, earned, received, still owed; "hear this month's total"
     WhatsApp         send the month as a plain message, as written proof
     money received   payments, each with a date
     month controls   previous / next month, clear this month

   Stored in localStorage as "shramik-diary-v1:<account id>":
     { rate, emp: {name, phone, site}, days: {"YYYY-MM-DD": "full" | "half"}, pays: [{d, a, id}] }
   Everything stays in this browser's storage on the worker's own phone. */
(function () {
  'use strict';

  var cal = document.getElementById('cal');
  if (!cal) return;

  /* with accounts on this phone, the diary only opens after login, and each account has its own */
  var ACC = window.ssAccount;
  if (ACC && ACC.isGated()) { ACC.showGate(); return; }
  var KEY = ACC ? ACC.key('shramik-diary-v1') : 'shramik-diary-v1';
  var MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var MONTHS_HI = ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'];
  var WD_EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var WD_HI = ['रवि', 'सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि'];

  /* ---------- storage ---------- */

  var storageOk = true;
  function blank() { return { rate: '', emp: { name: '', phone: '', site: '' }, days: {}, pays: [] }; }
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY));
      if (s && typeof s === 'object') {
        var b = blank();
        b.rate = s.rate || '';
        b.emp = Object.assign(b.emp, s.emp || {});
        b.days = s.days && typeof s.days === 'object' ? s.days : {};
        b.pays = Array.isArray(s.pays) ? s.pays : [];
        return b;
      }
    } catch (e) { storageOk = false; }
    return blank();
  }
  var store = load();
  var warned = false;
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(store)); }
    catch (e) {
      if (!warned && window.ssToast) window.ssToast('This phone is not letting the diary save. Take screenshots as your record.');
      warned = true;
    }
  }

  /* ---------- helpers ---------- */

  function pad(n) { return n < 10 ? '0' + n : String(n); }
  function key(y, m, d) { return y + '-' + pad(m + 1) + '-' + pad(d); }
  function rupees(n) { return '₹' + Math.round(n).toLocaleString('en-IN'); }
  function el(id) { return document.getElementById(id); }

  var today = new Date();
  var TY = today.getFullYear(), TM = today.getMonth(), TD = today.getDate();
  var view = { y: TY, m: TM };

  function prefix() { return view.y + '-' + pad(view.m + 1) + '-'; }
  function isCurrentMonth() { return view.y === TY && view.m === TM; }

  /* ---------- fields ---------- */

  var rateIn = el('rate');
  rateIn.value = store.rate;
  rateIn.addEventListener('input', function () {
    store.rate = rateIn.value.replace(/[^0-9]/g, '');
    save();
    totals();
  });
  [['emp-name', 'name'], ['emp-phone', 'phone'], ['emp-site', 'site']].forEach(function (p) {
    var input = el(p[0]);
    input.value = store.emp[p[1]] || '';
    input.addEventListener('input', function () { store.emp[p[1]] = input.value; save(); });
  });

  /* ---------- calendar ---------- */

  var STATE_EN = { full: 'full day', half: 'half day', '': 'no work' };

  function dayLabel(d, st) {
    return d + ' ' + MONTHS_EN[view.m] + ', ' + STATE_EN[st || ''];
  }

  function render() {
    el('mname').innerHTML = MONTHS_EN[view.m] + ' ' + view.y +
      '<br><span lang="hi" style="font-weight:normal">' + MONTHS_HI[view.m] + ' ' + view.y + '</span>';
    el('next').disabled = isCurrentMonth();

    cal.innerHTML = '';
    for (var w = 0; w < 7; w++) {
      var h = document.createElement('div');
      h.className = 'wd';
      h.innerHTML = WD_EN[w] + '<br><span lang="hi">' + WD_HI[w] + '</span>';
      cal.appendChild(h);
    }
    var first = new Date(view.y, view.m, 1).getDay();
    var count = new Date(view.y, view.m + 1, 0).getDate();
    for (var i = 0; i < first; i++) {
      var sp = document.createElement('div');
      sp.setAttribute('aria-hidden', 'true');
      cal.appendChild(sp);
    }
    for (var d = 1; d <= count; d++) cal.appendChild(dayButton(d));

    totals();
    renderPays();
  }

  function dayButton(d) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'daybtn';
    b.textContent = d;
    var k = key(view.y, view.m, d);
    var future = isCurrentMonth() && d > TD;
    if (isCurrentMonth() && d === TD) b.classList.add('today');
    if (future) {
      b.disabled = true;
      b.style.opacity = '0.35';
      b.setAttribute('aria-label', d + ' ' + MONTHS_EN[view.m] + ', not yet');
      return b;
    }
    paint(b, d, store.days[k]);
    b.addEventListener('click', function () {
      var st = store.days[k];
      var next = !st ? 'full' : st === 'full' ? 'half' : '';
      if (next) store.days[k] = next; else delete store.days[k];
      save();
      paint(b, d, next);
      totals();
    });
    return b;
  }

  function paint(b, d, st) {
    b.classList.toggle('full', st === 'full');
    b.classList.toggle('half', st === 'half');
    b.setAttribute('aria-label', dayLabel(d, st));
  }

  /* ---------- totals ---------- */

  function sums() {
    var p = prefix(), full = 0, half = 0, paid = 0;
    Object.keys(store.days).forEach(function (k) {
      if (k.indexOf(p) !== 0) return;
      if (store.days[k] === 'full') full++;
      else if (store.days[k] === 'half') half++;
    });
    store.pays.forEach(function (x) { if (String(x.d).indexOf(p) === 0) paid += Number(x.a) || 0; });
    var rate = Number(store.rate) || 0;
    var days = full + half / 2;
    var earned = days * rate;
    return { full: full, half: half, days: days, rate: rate, earned: earned, paid: paid, owed: Math.max(0, earned - paid), extra: Math.max(0, paid - earned) };
  }

  function totals() {
    var s = sums();
    var whole = Math.floor(s.days);
    el('t-days').textContent = (s.days % 1 ? (whole ? whole : '') + '½' : String(whole));
    el('t-earned').textContent = rupees(s.earned);
    el('t-paid').textContent = rupees(s.paid);
    el('t-owed').textContent = rupees(s.owed);
  }

  window.SS_PHRASES = window.SS_PHRASES || [];
  /* said when the daily wage is still empty */
  var NEED_RATE = { hi: 'पहले ऊपर अपनी रोज़ की मज़दूरी लिखें।', en: 'First, write your daily wage at the top.' };
  window.SS_PHRASES.push(NEED_RATE);
  /* said when there is nothing to send yet for this month */
  var NEED_DAYS = { hi: 'पहले कैलेंडर में वे दिन दबाएँ, जिन दिन आपने काम किया।', en: 'First, tap the days you worked on the calendar.' };
  window.SS_PHRASES.push(NEED_DAYS);

  var sayBtn = el('say-sum');
  if (sayBtn) {
    sayBtn.addEventListener('click', function () {
      if (!window.ssSpeak) return;
      var s = sums();
      var mh = MONTHS_HI[view.m], me = MONTHS_EN[view.m];
      if (!s.rate) {
        window.ssSpeak(NEED_RATE, sayBtn);
        return;
      }
      var dHi = s.full + ' पूरे दिन' + (s.half ? ' और ' + s.half + ' आधे दिन' : '');
      var dEn = s.full + ' full days' + (s.half ? ' and ' + s.half + ' half days' : '');
      var hi = mh + ' में आपने ' + dHi + ' काम किया। रोज़ ' + s.rate + ' रुपये के हिसाब से कुल ' + Math.round(s.earned) + ' रुपये बनते हैं। ' +
        'आपको ' + s.paid + ' रुपये मिल चुके हैं। ' +
        (s.owed > 0 ? 'अभी ' + Math.round(s.owed) + ' रुपये बाकी हैं।' : (s.extra > 0 ? 'आपको ' + Math.round(s.extra) + ' रुपये ज़्यादा मिले हैं, यह एडवांस हो सकता है।' : 'कुछ बाकी नहीं है।'));
      var en = 'In ' + me + ' you worked ' + dEn + '. At ' + s.rate + ' rupees a day, that is ' + Math.round(s.earned) + ' rupees. ' +
        'You have received ' + s.paid + ' rupees. ' +
        (s.owed > 0 ? 'You are still owed ' + Math.round(s.owed) + ' rupees.' : (s.extra > 0 ? 'You have received ' + Math.round(s.extra) + ' rupees more, which may be an advance.' : 'Nothing is owed.'));
      window.ssSpeak({ hi: hi, en: en }, sayBtn);
    });
  }

  /* ---------- send the month on WhatsApp, as written proof ---------- */

  /* the dates of this month marked as worked, as day numbers */
  function workedDates() {
    var p = prefix(), full = [], half = [];
    Object.keys(store.days).sort().forEach(function (k) {
      if (k.indexOf(p) !== 0) return;
      var day = parseInt(k.slice(8), 10);
      if (store.days[k] === 'full') full.push(day);
      else if (store.days[k] === 'half') half.push(day);
    });
    return { full: full, half: half };
  }

  /* a plain message in Hindi and English that an employer, helper or officer can read */
  function summaryText() {
    var s = sums(), dates = workedDates(), e = store.emp, p = prefix();
    var month = MONTHS_HI[view.m] + ' ' + view.y + ' / ' + MONTHS_EN[view.m] + ' ' + view.y;
    var pays = store.pays.filter(function (x) { return String(x.d).indexOf(p) === 0; })
      .sort(function (a, b) { return a.d < b.d ? -1 : 1; })
      .map(function (x) { return parseInt(x.d.slice(8), 10) + ' ' + MONTHS_EN[view.m].slice(0, 3) + ': ' + rupees(x.a); });
    var who = [e.name, e.phone, e.site].filter(Boolean).join(', ');
    var lines = ['SHRAM STAMBH · काम का हिसाब / Work diary', 'महीना / Month: ' + month];
    if (who) lines.push('मालिक / Employer: ' + who);
    lines.push('रोज़ की मज़दूरी / Daily wage: ' + rupees(s.rate));
    lines.push('पूरे दिन / Full days (' + dates.full.length + '): ' + (dates.full.join(', ') || '-'));
    if (dates.half.length) lines.push('आधे दिन / Half days (' + dates.half.length + '): ' + dates.half.join(', '));
    lines.push('कुल कमाई / Earned: ' + rupees(s.earned));
    lines.push('मिला / Received: ' + rupees(s.paid) + (pays.length ? ' (' + pays.join('; ') + ')' : ''));
    if (s.extra > 0) lines.push('ज़्यादा मिला (एडवांस?) / Received extra (advance?): ' + rupees(s.extra));
    else lines.push('बाकी / Still owed: ' + rupees(s.owed));
    return lines.join('\n');
  }

  var sendBtn = el('send-sum');
  if (sendBtn) {
    sendBtn.addEventListener('click', function () {
      if (!(Number(store.rate) > 0)) {
        if (window.ssSpeak) window.ssSpeak(NEED_RATE, sendBtn);
        if (window.ssToast) window.ssToast(NEED_RATE.en + ' · ' + NEED_RATE.hi);
        rateIn.focus();
        return;
      }
      var s = sums();
      if (!s.days && !s.paid) {
        /* an empty record is no proof: ask for the days first */
        if (window.ssSpeak) window.ssSpeak(NEED_DAYS, sendBtn);
        if (window.ssToast) window.ssToast(NEED_DAYS.en + ' · ' + NEED_DAYS.hi);
        var firstDay = el('cal').querySelector('button:not([disabled])');
        if (firstDay) firstDay.focus();
        return;
      }
      /* a link click (not window.open) so WhatsApp opens reliably on phones */
      var a = document.createElement('a');
      a.href = 'https://wa.me/?text=' + encodeURIComponent(summaryText());
      a.target = '_blank';
      a.rel = 'noopener';
      document.body.appendChild(a);
      a.click();
      a.remove();
    });
  }

  /* ---------- money received ---------- */

  var amtIn = el('pay-amt');
  el('pay-add').addEventListener('click', function () {
    var a = parseInt(String(amtIn.value).replace(/[^0-9]/g, ''), 10);
    if (!a || a <= 0) {
      amtIn.setAttribute('aria-invalid', 'true');
      amtIn.focus();
      return;
    }
    amtIn.removeAttribute('aria-invalid');
    var d = isCurrentMonth() ? TD : new Date(view.y, view.m + 1, 0).getDate();
    store.pays.push({ d: key(view.y, view.m, d), a: a, id: Date.now() });
    save();
    amtIn.value = '';
    totals();
    renderPays();
  });

  function renderPays() {
    var list = el('paylist');
    list.innerHTML = '';
    var p = prefix();
    store.pays.filter(function (x) { return String(x.d).indexOf(p) === 0; })
      .sort(function (a, b) { return a.d < b.d ? -1 : 1; })
      .forEach(function (x) {
        var li = document.createElement('li');
        var day = parseInt(x.d.slice(8), 10);
        var span = document.createElement('span');
        span.innerHTML = '<b>' + rupees(x.a) + '</b> &nbsp;' + day + ' ' + MONTHS_EN[view.m].slice(0, 3) + ' · <span lang="hi">' + day + ' ' + MONTHS_HI[view.m] + '</span>';
        var del = document.createElement('button');
        del.type = 'button';
        del.className = 'btn small';
        del.textContent = 'Remove · हटाएँ';
        del.setAttribute('aria-label', 'Remove ' + rupees(x.a));
        del.addEventListener('click', function () {
          if (!window.confirm('Remove ' + rupees(x.a) + '? · ' + rupees(x.a) + ' हटाएँ?')) return;
          store.pays = store.pays.filter(function (y) { return y.id !== x.id; });
          save();
          totals();
          renderPays();
        });
        li.appendChild(span);
        li.appendChild(del);
        list.appendChild(li);
      });
    if (!list.children.length) {
      var none = document.createElement('li');
      none.className = 'muted';
      none.innerHTML = 'Nothing added yet · <span lang="hi">अभी कुछ नहीं जोड़ा</span>';
      list.appendChild(none);
    }
  }

  /* ---------- month controls ---------- */

  el('prev').addEventListener('click', function () {
    view.m--; if (view.m < 0) { view.m = 11; view.y--; }
    render();
  });
  el('next').addEventListener('click', function () {
    if (isCurrentMonth()) return;
    view.m++; if (view.m > 11) { view.m = 0; view.y++; }
    render();
  });
  el('clear-month').addEventListener('click', function () {
    var name = MONTHS_EN[view.m] + ' ' + view.y;
    if (!window.confirm('Delete all days and money for ' + name + '? · ' + MONTHS_HI[view.m] + ' का पूरा हिसाब मिटाएँ?')) return;
    var p = prefix();
    Object.keys(store.days).forEach(function (k) { if (k.indexOf(p) === 0) delete store.days[k]; });
    store.pays = store.pays.filter(function (x) { return String(x.d).indexOf(p) !== 0; });
    save();
    render();
  });

  if (!storageOk && window.ssToast) window.ssToast('This phone is not letting the diary save. Take screenshots as your record.');
  render();
})();
