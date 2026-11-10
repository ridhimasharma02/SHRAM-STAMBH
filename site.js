/* SHRAM STAMBH - small helpers used on several pages:
   print buttons and the contractor notebook.

   The notebook is stored in localStorage as "shramik-contractors-v1:<account id>",
   newest first: [{id, name, phone, place, note, v: "good" | "late" | "bad", d}]
   Each note can be called, sent to WhatsApp as a warning, or heard aloud. */
(function () {
  'use strict';

  /* ---------------- print buttons ---------------- */
  document.querySelectorAll('.js-print').forEach(function (b) {
    b.addEventListener('click', function () { window.print(); });
  });

  /* ---------------- contractor notebook ---------------- */
  var list = document.getElementById('nb-list');
  if (!list) return;

  var ACC = window.ssAccount;
  if (ACC && ACC.isGated()) { ACC.showGate(); return; }
  var KEY = ACC ? ACC.key('shramik-contractors-v1') : 'shramik-contractors-v1';
  var VERDICT = {
    good: { en: 'Paid fully, on time', hi: 'पूरा पैसा, समय पर दिया' },
    late: { en: 'Paid late or less', hi: 'देर से या कम पैसा दिया' },
    bad:  { en: 'Did not pay', hi: 'पैसा नहीं दिया' }
  };

  function load() {
    try {
      var d = JSON.parse(localStorage.getItem(KEY));
      return Array.isArray(d) ? d : [];
    } catch (e) { return []; }
  }
  window.SS_PHRASES = window.SS_PHRASES || [];
  Object.keys(VERDICT).forEach(function (k) { window.SS_PHRASES.push(VERDICT[k]); });
  window.SS_PHRASES.push(
    { hi: 'पहले ठेकेदार का नाम या फ़ोन नंबर लिखें।', en: 'First write the contractor\u2019s name or phone number.' },
    { hi: 'पैसा ठीक दिया या नहीं, ऊपर के तीन बटनों में से एक दबाएँ।', en: 'Press one of the three buttons to say if they paid properly.' },
    { hi: 'सेव हो गया।', en: 'Saved.' }
  );

  var items = load();
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(items)); return true; }
    catch (e) {
      if (window.ssToast) window.ssToast('This phone is not letting the notebook save.');
      return false;
    }
  }

  function el(id) { return document.getElementById(id); }
  var fName = el('nb-name'), fPhone = el('nb-phone'), fPlace = el('nb-place'), fNote = el('nb-note'), fSearch = el('nb-search');
  var choice = '';

  var vbtns = document.querySelectorAll('.verdict');
  function pick(v) {
    choice = v;
    vbtns.forEach(function (b) { b.setAttribute('aria-checked', b.getAttribute('data-v') === v ? 'true' : 'false'); });
  }
  vbtns.forEach(function (b) {
    b.addEventListener('click', function () {
      pick(b.getAttribute('data-v'));
      var v = VERDICT[choice];
      if (window.ssSpeak) window.ssSpeak({ hi: v.hi, en: v.en });
    });
  });

  function say(hi, en) {
    if (window.ssSpeak) window.ssSpeak({ hi: hi, en: en });
    if (window.ssToast) window.ssToast(en + ' · ' + hi, 4000);
  }

  el('nb-save').addEventListener('click', function () {
    var name = fName.value.trim(), phone = fPhone.value.trim();
    if (!name && !phone) {
      fName.setAttribute('aria-invalid', 'true');
      fName.focus();
      say('पहले ठेकेदार का नाम या फ़ोन नंबर लिखें।', 'First write the contractor’s name or phone number.');
      return;
    }
    if (!choice) {
      say('पैसा ठीक दिया या नहीं, ऊपर के तीन बटनों में से एक दबाएँ।', 'Press one of the three buttons to say if they paid properly.');
      vbtns[0].focus();
      return;
    }
    fName.removeAttribute('aria-invalid');
    items.unshift({ id: Date.now(), name: name, phone: phone, place: fPlace.value.trim(), note: fNote.value.trim(), v: choice, d: new Date().toISOString().slice(0, 10) });
    if (save()) say('सेव हो गया।', 'Saved.');
    fName.value = fPhone.value = fPlace.value = fNote.value = '';
    pick('');
    render();
  });

  fSearch.addEventListener('input', render);

  function shareText(x) {
    var v = VERDICT[x.v] || VERDICT.late;
    var lines = [
      'Contractor note from SHRAM STAMBH / ठेकेदार की जानकारी',
      'Name / नाम: ' + (x.name || '-'),
      'Phone / फ़ोन: ' + (x.phone || '-'),
      'Place / जगह: ' + (x.place || '-'),
      'Payment / पैसा: ' + v.en + ' / ' + v.hi
    ];
    if (x.note) lines.push('Note / टिप्पणी: ' + x.note);
    lines.push('Date / तारीख: ' + x.d);
    return lines.join('\n');
  }

  function render() {
    var q = fSearch.value.trim().toLowerCase();
    var qd = q.replace(/[^0-9]/g, '');
    list.innerHTML = '';
    var shown = items.filter(function (x) {
      if (!q) return true;
      var hay = (x.name + ' ' + x.place + ' ' + x.note).toLowerCase();
      return hay.indexOf(q) !== -1 || (qd.length >= 3 && String(x.phone).replace(/[^0-9]/g, '').indexOf(qd) !== -1);
    });
    shown.forEach(function (x) {
      var v = VERDICT[x.v] || VERDICT.late;
      var li = document.createElement('li');
      li.className = x.v;

      var who = document.createElement('div');
      who.className = 'who';
      who.textContent = x.name || x.phone;
      li.appendChild(who);

      var vt = document.createElement('div');
      vt.className = 'verdict-txt';
      vt.innerHTML = '<strong></strong> · <span lang="hi"></span>';
      vt.querySelector('strong').textContent = v.en;
      vt.querySelector('span').textContent = v.hi;
      li.appendChild(vt);

      var meta = [x.phone && x.name ? x.phone : '', x.place, x.note, x.d].filter(Boolean).join(' · ');
      if (meta) {
        var m = document.createElement('div');
        m.className = 'muted';
        m.textContent = meta;
        li.appendChild(m);
      }

      var acts = document.createElement('div');
      acts.className = 'acts';
      if (x.phone) {
        var call = document.createElement('a');
        call.href = 'tel:' + String(x.phone).replace(/[^0-9+]/g, '');
        call.textContent = 'Call · फ़ोन';
        acts.appendChild(call);
      }
      var wa = document.createElement('a');
      wa.className = 'wa';
      wa.href = 'https://wa.me/?text=' + encodeURIComponent(shareText(x));
      wa.target = '_blank';
      wa.rel = 'noopener';
      wa.textContent = 'Send on WhatsApp · भेजें';
      acts.appendChild(wa);

      var hear = document.createElement('button');
      hear.type = 'button';
      hear.textContent = 'Listen · सुनें';
      hear.className = 'needs-speech-inline';
      hear.addEventListener('click', function () {
        if (!window.ssSpeak) return;
        window.ssSpeak({
          hi: (x.name || 'यह ठेकेदार') + '। ' + v.hi + '।' + (x.place ? ' जगह: ' + x.place + '।' : '') + (x.note ? ' ' + x.note : ''),
          en: (x.name || 'This contractor') + '. ' + v.en + '.' + (x.place ? ' Place: ' + x.place + '.' : '') + (x.note ? ' ' + x.note : '')
        }, hear);
      });
      if (window.ssSpeak) acts.appendChild(hear);

      var del = document.createElement('button');
      del.type = 'button';
      del.textContent = 'Delete · मिटाएँ';
      del.addEventListener('click', function () {
        if (!window.confirm('Delete this note? · यह नोट मिटाएँ?')) return;
        items = items.filter(function (y) { return y.id !== x.id; });
        save();
        render();
      });
      acts.appendChild(del);

      li.appendChild(acts);
      list.appendChild(li);
    });

    if (!shown.length) {
      var none = document.createElement('li');
      none.className = 'muted';
      none.style.borderLeftColor = 'var(--rule)';
      none.innerHTML = q ? 'Nothing found · <span lang="hi">कुछ नहीं मिला</span>' : 'No notes yet · <span lang="hi">अभी कोई नोट नहीं</span>';
      list.appendChild(none);
    }
  }

  render();
})();
