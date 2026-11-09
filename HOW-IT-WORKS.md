# SHRAM STAMBH: how every feature works

SHRAM STAMBH (श्रम स्तंभ, "pillar of labour") is a free website for construction workers, domestic workers, factory hands and daily-wage labourers in India. It deals with four problems:

1. **Wage theft.** Workers are not paid, or paid less, and have no proof.
2. **Not knowing their rights.**
3. **No way to check an employer before taking a job.**
4. **Language and literacy barriers.** Many users cannot read at all.

The site is plain HTML, CSS and a small amount of JavaScript. There is no server-side code and no database. Every page needs a picture login, and everything a worker saves, including their name and mobile number, stays on their own phone.

---

## 1. Files at a glance

| File | What it is |
|---|---|
| [index.html](index.html) | Home page: listen button, language buttons, ask banner, six picture tiles |
| [rights.html](rights.html) | Rights for every worker, then construction, domestic, factory and migrant sections |
| [pictures.html](pictures.html) | Twelve rights shown as one picture each, with sound |
| [wages.html](wages.html) | Step-by-step guide to recovering unpaid wages, plus a printable work log |
| [diary.html](diary.html) | Tap-to-mark work diary that works out how much is owed |
| [before-job.html](before-job.html) | Questions to ask, job card, warning signs, contractor notebook |
| [show.html](show.html) | Ready-made messages that fill the screen, to show an officer |
| [ask.html](ask.html) | Ask a question by voice in seven languages and hear the answer |
| [help.html](help.html) | Helplines, offices, what to say on the phone |
| [404.html](404.html) | Friendly "page not found" with a home link and the 15100 call button |
| [login.html](login.html) | Picture login: no reading or writing needed |
| [style.css](style.css) | All visual design |
| [speak.js](speak.js) | The voice: plays recordings, falls back to the phone's voice |
| [ask.js](ask.js) | The voice assistant: listens, matches the question, answers |
| [diary.js](diary.js) | Work diary logic |
| [site.js](site.js) | Print buttons and the contractor notebook |
| [account.js](account.js) | Accounts on this phone: create, check, lock out, log out, privacy gates |
| [login.js](login.js) | The login screen's steps |
| `audio/` | 440 recorded voice clips, one folder per language |
| `audio-manifest.js`, `lang-data.js`, `ask-data.js`, `account-data.js` | Generated data files. Don't edit these by hand |
| `tools/` | Python scripts that generate the pages and record the audio. Not uploaded to the web |

The HTML pages are **generated**. To change page text, edit the scripts in `tools/` and rebuild (see section 14). Editing the `.html` files directly works, but the changes are lost on the next rebuild.

---

### Reading the code

Every file starts with a comment that says what it does and how it is laid out. A good order to read them in:

1. **[style.css](style.css)** has 17 numbered sections, listed in a table of contents at the top: colours, base text, header, layout, boxes, voice, home page, call buttons, pictures, diary, notebook, Ask page, login, sidebar and footer, screen sizes, then printing. Each rule appears once, with its final value. Everything that changes on smaller screens is together in section 16, from wide screens down to the smallest phones.
2. **[speak.js](speak.js)** turns a box into words with [`gather()`](speak.js:115), then plays the matching recording with [`speak()`](speak.js:297).
3. **[ask.js](ask.js)** scores a spoken question against the 16 topics with [`match()`](ask.js:66), then shows and speaks the answer.
4. **[account.js](account.js)** holds accounts and the page lock. **[login.js](login.js)** is the login screen, one step at a time.
5. **[diary.js](diary.js)** and **[site.js](site.js)** are the work diary and the contractor notebook.

Names say what things are: `DATA` is the data a script reads from its generated `...-data.js` file, `state` is where the login screen is up to, and `textFor()` gets a line of text in the chosen language.

---

## 2. How the pages are built

**What it does:** all ten pages share the same header, menu, bottom bar and footer, so they stay consistent.

**How it works:** [build_common.py](tools/build_common.py) has one function, [`page()`](tools/build_common.py:137), that wraps any page body in the shared shell. It adds:

- the `<head>`, with the Mukta font, the stylesheet and the scripts;
- the dark strip at the top, with the free legal help number and the voice language picker;
- the header, with the logo (an ochre signboard tile with the word श्रम, "labour"), the seven-item menu ([`NAV`](tools/build_common.py:72)) and the login button;
- the footer, with the disclaimer and the WhatsApp share link;
- the fixed bottom bar, with four buttons.

Each page is then written by a small script:

| Script | Pages |
|---|---|
| [build_1.py](tools/build_1.py) | Home and rights |
| [build_2.py](tools/build_2.py) | Not paid, before a job, help |
| [build_3.py](tools/build_3.py) | Pictures, show this screen, diary |
| [build_ask.py](tools/build_ask.py) | Ask page and the two language data files |
| [build_login.py](tools/build_login.py) | Login page and its data file |
| [build_404.py](tools/build_404.py) | The "page not found" page |

All icons are hand-drawn SVG line drawings stored in [`ICONS`](tools/build_common.py:9). They are written straight into the HTML, so no image files need to load.

**Cache busting:** [`VER`](tools/build_common.py:4) is added to every CSS and JS link, for example `speak.js?v=13`. Raising this number after a change makes phones download the new file instead of using an old cached copy.

---

## 3. Visual design and colour coding

**What it does:** a plain, grey, "notice board" look that doesn't feel like a template. Every topic has one fixed colour, so a person who can't read can find things by colour:

| Colour | Meaning | Pages |
|---|---|---|
| Ochre (yellow-brown) | Money | Not paid, work diary |
| Slate blue | Rights | Rights, pictures |
| Moss green | New job | Before a job |
| Brick red | Help and danger | Help, show screen, ask, the 112 button |

**How it works:** colours are CSS variables at the top of the stylesheet, under [`:root`](style.css:32). Topic classes such as [`.t-wages`](style.css:68) just set `--topic`. Every heading band, tile stripe, step number and border then uses `var(--topic)`. That means one class on `<body>` colours a whole page.

Other design points:

- **Square corners and flat greys.** No gradients, rounded "pill" buttons or emoji.
- **Large tap targets.** Every button is at least about 44 to 50 pixels high, for cheap phones and rough hands.
- **Full screen on computers.** The layout stretches across the whole screen, up to 1800px wide. Above 1100px, a sticky **sidebar** on the right holds what every page needs: "Listen to this page", the voice language buttons, the 15100 and 112 call buttons, and Ask. The main column then only shows that page's own content. The fixed bottom bar, and the listen box and ask banner on the home page, are hidden there because the sidebar already has them. The sidebar is built by `sidebar()` in [build_common.py](tools/build_common.py).
- **Less clutter.** There's one header row (logo, voice language, account) above the menu, more space inside and between boxes, and a two-column footer. On tablets, the menu becomes two even rows.
- **Phone first.** Below 1100px there is no sidebar. The bottom bar and the home page listen and ask boxes come back. Below 680px, the menu becomes two columns, grids stack and fonts adjust. Every page was checked at 320, 360, 390, 768, 1024, 1280, 1600 and 1920px with no sideways scrolling.
- **Print layout.** The [`@media print`](style.css:1285) rule hides the header, menu and bottom bar, so only the work log or job card prints, in black on white.
- **Font.** Mukta, loaded from Google Fonts, covers English and Hindi. Bengali, Tamil, Telugu, Kannada and Marathi use the phone's own fonts, which Android already includes.

---

## 4. Built for people who cannot read

These features work together:

- **Every line in two languages.** English, with Hindi underneath, using `<span class="hi" lang="hi">`. The `lang` attribute tells the voice which part is Hindi.
- **Pictures on everything.** Menu items, tiles, steps and buttons all have an icon. The same icon always means the same topic.
- **Colour coding**, as in section 3.
- **Speaker button on every box.** It reads that box aloud (section 5).
- **"Listen" in the bottom bar.** It reads the whole page.
- **Voice questions.** The Ask page answers spoken questions (section 7).
- **Tap-to-call numbers.** Every phone number is a `tel:` link, so tapping it dials.
- **Show this screen.** Full-screen messages to hand to an officer (section 10).
- **No reading needed for the diary.** Tap days, type numbers (section 8).

**Graceful fallback:** the `<html>` tag gets the class `js` as soon as JavaScript runs, and `can-speak` once the voice is ready. CSS uses these to hide or show things ([style.css:153](style.css:153)):

- `.needs-js` only shows when JavaScript works.
- `.needs-speech` only shows when the voice works.
- `.no-js` messages only show when JavaScript is off. They tell the person to use the printable log or call 15100 instead.

So no one ever sees a button that does nothing.

---

## 5. The voice (read aloud)

**What it does:** every box has a speaker button. Pressing it reads the box aloud in the chosen language. Pressing again stops it. The box gets a yellow outline while it is being read. The "Listen" button in the bottom bar reads the whole page, box by box, and changes to "Stop" while playing.

### Why recordings instead of the phone's voice

The first versions used the browser's built-in voice (the Web Speech API). That proved unreliable. Some browsers never start speaking at all, and many phones have no Hindi, Tamil or Bengali voice installed. So every fixed sentence on the site is now **recorded in advance** on a Mac (section 6), and the browser just plays a small audio file. That works in every browser.

### How a button press becomes sound

All of this is in [speak.js](speak.js).

1. **Pick the text.** [`pieces()`](speak.js:223) turns the box into a list of `{lang, text}` pieces using [`resolve()`](speak.js:179):
   - If the box has a translation stored as `data-say-ta="..."` (for Tamil), it uses that.
   - For Hindi or English, [`gather()`](speak.js:115) walks the HTML of the box. Lines inside `lang="hi"` count as Hindi, everything else as English. Buttons, icons and inputs are skipped. Phone numbers are read digit by digit, so "15100" becomes "1 5 1 0 0".
   - For a language a box isn't translated into, it first plays a short note in the user's language, "this part is only in Hindi and English", then reads the Hindi.
2. **Clean it.** [`finalText()`](speak.js:82) tidies punctuation and spells out helpline numbers, so the text is exactly what was recorded.
3. **Find the recording.** [`hash()`](speak.js:61) turns the text into an 8-character code, an FNV-1a hash. [`audioUrl()`](speak.js:237) looks that code up in `audio-manifest.js`:

   ```js
   function audioUrl(p) {
     var h = hash(p.text);
     return MANIFEST[p.lang + ':' + h] ? 'audio/' + p.lang + '/' + h + '.m4a' : null;
   }
   ```

   Because the file name comes from the text itself, a recording can never play the wrong words. If text changes and isn't re-recorded, the lookup misses and the backup voice is used instead.
4. **Play it.** [`speak()`](speak.js:297) plays each piece in turn. [`playFile()`](speak.js:326) plays the recording. If the file fails to load, or nothing starts within 12 seconds on a slow connection, [`playTts()`](speak.js:353) uses the phone's own voice instead.
5. **The backup voice is protected.** In `playTts()`:
   - text is cut into short sentences, because Chrome cuts off long speech;
   - a watchdog checks that speech actually started within 3.5 seconds. If not, it resets and retries once, then shows a message about volume and silent mode;
   - the watchdog leaves the voice alone if the phone is already speaking. Some phones never report "started", and replaying the line in that case made it heard twice;
   - the backup is only really needed for text that changes, such as diary totals.
6. **Only one thing plays at a time.** Every press increases a `session` number. Any old sound or timer that belongs to an earlier session ignores itself, so tapping a second box cleanly stops the first one.
7. **Each line plays exactly once.** These rules stop the voice repeating:
   - Stopping a clip only pauses it. Emptying the audio source fired late events that could start the backup voice on top of the recording.
   - Every audio event is checked against the clip it belongs to.
   - The backup voice can take over a clip at most once.
   - A shaky double tap on the same button within 0.6 seconds counts as one tap, so it doesn't start and then immediately stop.
   - On the Ask page, phones that send the same recognised sentence twice only get one answer.

**Where the buttons come from:** speaker buttons are not in the HTML. [speak.js:435](speak.js:435) adds one to every `.panel`, tile, picture and show-card when the page loads. If the voice can't work at all, no buttons appear.

**Language picker:** the top strip has a drop-down ([speak.js:477](speak.js:477)), and the home and ask pages have big language buttons ([speak.js:499](speak.js:499)). Both call [`setLang()`](speak.js:465):

- it saves the choice in `localStorage`, so it is remembered next time;
- it speaks a confirmation in the new language, such as "ठीक है, अब हिंदी में सुनाया जाएगा";
- it sends an `ss-lang` event, so the Ask page can relabel itself.

**Seven languages:** Hindi, English, Bengali, Marathi, Tamil, Telugu, Kannada. They are listed in [`LANGS`](tools/i18n.py:10), along with the Mac voice used to record each one.

---

## 6. How the audio is recorded

**What it does:** produces the 440 `.m4a` clips in `audio/` (about 22 MB). A phone only downloads a clip when someone plays it.

**How it works.** There are three steps, all in `tools/`:

1. **Collect.** [collect.html](tools/collect.html) loads each page in a hidden frame and calls `ssDebug.collect()` in speak.js. That returns every exact sentence each page can speak, in every language, with its hash. Using the real page code guarantees the recordings match what the player will look for.
2. **Save.** The list is sent to [collect_server.py](tools/collect_server.py), a tiny local server on port 8124, which writes it to `tools/collected.json`.
3. **Record.** [make_audio.py](tools/make_audio.py) runs the Mac's `say` command with the right voice for each language:

   | Language | Voice |
   |---|---|
   | Hindi | Lekha |
   | English | Tara |
   | Bengali | Piya |
   | Tamil | Vani |
   | Telugu | Geeta |
   | Kannada | Soumya |
   | Marathi | Lekha (the Hindi voice reading Marathi) |

   `afconvert` then compresses each clip to small AAC audio, about 4 KB per second. The script runs six recordings at once, skips clips that already exist, deletes ones nothing uses any more, and rewrites `audio-manifest.js`.

---

## 7. Ask a question (voice assistant)

**What it does:** on [ask.html](ask.html), the worker:

1. picks a language;
2. presses the big microphone and hears a short beep;
3. asks a question out loud;
4. sees what was heard, and gets a written and spoken answer, with call buttons and a link to the right page.

If the microphone isn't available, they can tap one of 16 picture questions or type instead.

**The 16 topics:** unpaid wages, contractor ran away, when pay is due, minimum wage, hours and overtime, injury at work, PF, ESI, harassment, forced or bonded labour, child labour, domestic work, coming from another state, e-Shram card, taking a new job, and free lawyers. Each topic has a label, an answer, phone numbers and a link, in all seven languages. They live in [`TOPICS`](tools/i18n.py:144).

### How it works

All of this is in [ask.js](ask.js).

1. **Listening** ([ask.js:211](ask.js:211)). Pressing the mic creates the browser's `SpeechRecognition` with the language code, such as `ta-IN` for Tamil. It asks for up to three guesses of what was said. Words appear on screen as they are heard.
2. **Matching.** There is no AI and no server. [`match()`](ask.js:66) scores the sentence against every topic:

   ```js
   function score(q, t) {
     var s = countHits(q, t.kw) * 2 + countHits(q, t.weak || []);
     (t.combos || []).forEach(function (combo) {
       if (combo.every(function (c) { return hasAny(q, D.concepts[c]); })) s += 3;
     });
     return s;
   }
   ```

   - **Strong keywords** score 2 points each, for example "ठेकेदार", "காயம்" or "PF".
   - **Weak words** score 1 point, for example "card" or "help".
   - **Combos** score 3 points when words from two groups both appear. "Money word + negative word" means unpaid, as in "पैसा नहीं मिला". "When + money" means pay day. The word groups (`MONEY`, `NEG`, `WHEN` and so on) are in [`CONCEPTS`](tools/i18n.py:112) and mix all seven languages plus romanised Hindi.
   - The highest score wins. Ties go to the more urgent topic, using [`MATCH_ORDER`](tools/i18n.py:426), so forced labour beats a general answer.
   - Of the recogniser's three guesses, the one that matches best is used.
   - If nothing scores, the worker hears a "didn't understand, call 15100" answer.
3. **Normalising.** [`norm()`](ask.js:39) makes matching forgiving. It lowercases, removes the Hindi and Bengali nukta dot (so ज़ = ज), treats chandrabindu and anusvara the same, and strips punctuation.
4. **Answering.** [`show()`](ask.js:80) writes the answer, adds "Hear again", one call button per helpline and a "More about this" link, then speaks the answer from its recording.
5. **Errors are spoken too** ([ask.js:253](ask.js:253)). A blocked microphone, no speech heard, no internet and an unsupported browser each have a message in all seven languages, which is shown and read aloud.

**Testing:** 35 sample questions across all seven languages all matched the right topic. A weather question correctly got the "didn't understand" answer.

**Privacy:** speech-to-text is done by the browser. Chrome sends the voice to Google and Safari sends it to Apple. The site itself stores nothing, and the Ask page says this.

---

## 8. Work diary

**What it does:** the worker enters their daily wage once. Then they tap each day they worked: once for a full day, twice for a half day, three times to clear. They add money as they receive it. The page shows days worked, total earned, received and **still owed**. One button reads the month's total aloud. Employer name, phone and work place can also be saved.

**How it works** ([diary.js](diary.js)):

- **Storage.** Everything is one object, saved in the browser's `localStorage` under the key `shramik-diary-v1`. It is never sent anywhere. [`load()`](diary.js:22) and [`save()`](diary.js:38) wrap every access in `try/catch`, so a phone that blocks storage still works, it just can't save.
- **Calendar.** [`render()`](diary.js:83) draws the month. [`dayButton()`](diary.js:108) makes each day a button that cycles through states. Future days are greyed out and can't be marked, which keeps the record honest. The "next month" arrow stops at the current month.
- **Maths.** [`sums()`](diary.js:142) works out the totals:

  ```js
  var days = full + half / 2;
  var earned = days * rate;
  ... owed: Math.max(0, earned - paid), extra: Math.max(0, paid - earned)
  ```

  If more was received than earned, the spoken total says it may have been an advance.
- **Half-day style.** A half day is coloured diagonally, half ochre and half white. See [style.css:673](style.css:673).
- **Proof.** The page tells workers to take a screenshot every week, because a screenshot can be shown at the labour office.

---

## 9. Contractor notebook and print buttons

**What it does:** on the "before a job" page, workers save notes about contractors: name, phone, place, a short note, and a picture choice for how they paid. The choices are thumbs up (paid fully, on time), clock (paid late or less) and thumbs down (did not pay). Notes can be searched by name, place or phone number. Each note has buttons to **Call**, **Send on WhatsApp**, **Listen** and **Delete**. Sending to a WhatsApp group warns other workers before they take a job with a bad contractor.

**How it works** ([site.js](site.js)):

- Notes are saved in `localStorage` under `shramik-contractors-v1`.
- [`render()`](site.js:106) filters notes as you type. Phone search ignores spaces, so "43210" finds "98765 43210".
- [`shareText()`](site.js:92) builds a two-language message. It is sent through a `https://wa.me/?text=...` link, which opens WhatsApp with the message ready, and the worker picks who to send it to.
- Saving is refused, with a spoken reason, if there is no name or phone, or no payment choice.
- Notes are built with `textContent`, never `innerHTML`, so anything typed can't break the page.
- **Print buttons** on the work log and job card simply call `window.print()`. The print stylesheet does the rest.

---

## 10. Show this screen

**What it does:** eight ready-made messages in English and Hindi, such as "I cannot read. Please read this to me." or "I am being forced to work. Please call the police on 112." Tapping **Show big** fills the whole screen with the message in large text, so the worker can hand the phone to an officer, doctor or helper. **Close** goes back.

**How it works:** this is pure CSS, with no JavaScript. Each card has an `id` (`c1` to `c8`), and "Show big" is a link to `#c2`, for example. The CSS [`:target`](style.css:592) selector styles whichever card the address points to:

```css
.showcard:target {
  position: fixed;
  inset: 0;
  z-index: 300;
  ...
}
```

It covers the whole screen, including the bottom bar. "Close" links to `#cards`, which un-targets it. Opening or closing a card also stops any speech that is playing.

---

## 11. Rights in pictures

**What it does:** twelve rights, each a big picture plus one short line, such as "Up to 8 hours a day", "Extra hours paid double" and "Children under 14 must not work". Blue pictures are what workers are owed. Red pictures are things nobody may do to them. Each has a speaker button. A big button at the top reads all twelve in a row.

**How it works:** [build_3.py](tools/build_3.py) creates the cards. Each card's spoken text in Bengali, Marathi, Tamil, Telugu and Kannada comes from [`PICTURES`](tools/i18n.py:502) and is stored on the card as `data-say-bn` and similar. The "read all" button has `data-read="#pics"`, which tells speak.js to read the whole list.

---

## 12. The other pages

- **Your rights** ([rights.html](rights.html)). A table of ten rights every worker has, then expandable sections for construction, domestic, factory and migrant workers. The sections use the HTML `<details>` tag, so they open and close with no JavaScript.
- **Not paid?** ([wages.html](wages.html)). Six numbered steps, from collecting proof to getting a free lawyer, plus:
  - a message template to send the employer, in English and Hindi, so there is written proof that the money was asked for;
  - a checklist of what to take to the office;
  - a printable 31-day work log.
- **Before a job** ([before-job.html](before-job.html)). Questions to ask, a printable job card that both sides sign, warning signs of bonded labour, a "before you leave home" checklist, and the contractor notebook.
- **Get help** ([help.html](help.html)). A helpline table where every number is a call button. Each row also has a spoken version ("खतरे में हों तो 1 1 2 पर फ़ोन करें"). There is a five-line script for what to say on a call, a list of which office to visit for which problem, and advice for people who can't read, including "never put your thumbprint on a blank paper".

---

## 13. Login (required)

**What it does:** every page needs a login. A visitor who isn't logged in is sent to the login page first and never sees the content. After logging in, they land back on the page they were trying to open. The emergency buttons for **15100 and 112 stay on the login page**, so nobody is ever blocked from calling for help.

**Making an account** needs real details:

1. **A picture for yourself:** a helmet, house, factory, bus, hammer, broom, shovel or scissors.
2. **Name (required).** People who can't write press **Say your name** and speak it. The browser turns speech into text in the chosen language.
3. **Mobile number (required).** It must be a 10-digit Indian mobile number starting with 6 to 9. "+91 98765 43210" and "098765…" are also accepted. The same number can't be used for two accounts on one phone.
4. **Four secret pictures,** tapped twice to confirm. They come from a grid of nine everyday things: sun, moon, star, tree, flower, fish, key, umbrella and cup.

If a detail is missing or wrong, the box turns red and the reason is shown and spoken, for example "Please type your ten-digit mobile number". Accounts made before details were required are asked to add them on their next login.

**Logging in** is just: tap your picture, then your four secret pictures. Every instruction is spoken in the chosen language. The secret taps are **never spoken aloud**.

**Important:** there is no server, so accounts and details live only on this phone. Nobody can reset a forgotten code. "Forgot your pictures?" removes that account and its diary, after a spoken warning and a second "Yes, remove it" tap.

### How it works

- **The lock on every page.** Every page except login has a tiny script at the very top of its `<head>`, called `GUARD` in [build_common.py](tools/build_common.py). It runs before anything else, checks for a logged-in account, and if there isn't one hides the page and jumps to `login.html?next=<this page>`. It runs again when the browser's Back button shows a saved copy of a page, so logging out and pressing Back doesn't reveal anything.
- **Storing accounts.** [account.js](account.js) saves accounts in `localStorage` under `ss-profiles`. Each one has an id, picture, name, mobile number, a random salt and a hash. The secret code itself is **never stored**. [`digest()`](account.js:83) makes a SHA-256 fingerprint of the salt plus the four picture ids, and [`verify()`](account.js:141) recomputes and compares it.
- **Checking details.** [`cleanMobile()`](account.js:96) accepts only valid Indian mobile numbers. [`validName()`](account.js:103) needs at least two letters in any script, so "7" is refused but "मुरुगन" or "முருகன்" is fine. [`mobileTaken()`](account.js:104) blocks duplicates. [`create()`](account.js:110) refuses to save without them, even if the screen were skipped.
- **Lockout.** Five wrong codes lock that account for one minute (`ss-locks`). During the lock the right code is refused too.
- **Staying logged in.** The account id lives in `sessionStorage`, so closing the browser logs out. Because shared phones rarely get their browser closed, the site also **logs out by itself after 30 minutes without use**: every tap, key press or scroll updates a timestamp, and both the page lock and [account.js](account.js) refuse a session that is older than that. Logging out from the header says goodbye and returns to the login page. On the login page the bottom bar keeps 15100, 112 and Listen, but not Ask, since Ask needs a login.
- **Private data per person.** [`key()`](account.js:62) adds the account id to storage names, so each person has their own diary and contractor notebook.
- **Moving old data in.** The first account created takes over any diary or notes saved before accounts existed.
- **The screen.** [login.js](login.js) shows one step at a time:
  - "Who are you?";
  - picking a picture ([`renderAvatars()`](login.js:87));
  - name and mobile ([`startDetails()`](login.js:117)), with the say-your-name microphone;
  - the secret pictures ([`tapSecret()`](login.js:252), [`evaluate()`](login.js:270));
  - the logged-in view, with a Continue button back to the page the person wanted.
- **Text.** All login text in seven languages is in [`LOGIN`](tools/i18n.py:553). The pictures are in [`AVATARS`](tools/i18n.py:738) and [`SECRETS`](tools/i18n.py:740). Every spoken line is recorded.
- **Recording audio while logged out.** [collect.html](tools/collect.html) makes a temporary account while it gathers lines, then puts things back.

**How strong it is:** four pictures out of nine gives 6,561 codes, and the lockout makes guessing take many hours. The lock on every page and the code stop casual access by family or co-workers. They do not stop someone with the phone and technical skill, because a website with no server keeps its data in the browser. A server-backed login would be needed for that.

---

## 14. Final quality checks

These are built in and were checked on every page:

- **Readable contrast.** All text is at least 4.5 : 1 against its background, or 3 : 1 for large text, which is the WCAG AA standard.
- **Finger-sized buttons.** Every button and call link is at least about 44px tall.
- **Named controls.** Every button and link can be named by a screen reader, every form box has a label, and each page has one main heading with no skipped levels.
- **Fits every screen.** There is no sideways scrolling on any page, from 320px phones to 1920px monitors.
- **Printing.** Printouts drop the sidebar, header and buttons, so the work log and job card print cleanly.
- **JavaScript turned off.** The login lock can't run without JavaScript, so the content is hidden and a message with the 15100 and 112 call buttons shows instead.
- **Sharing.** Every page has title and description tags, so a link shared on WhatsApp shows a proper preview.
- **Wrong addresses.** A mistyped address shows [404.html](404.html) instead of a bare error. Most web hosts use this file automatically, and `tools/serve.py` does too.

---

## 15. Privacy and safety

- No tracking scripts and no analytics.
- Login is required. Names, mobile numbers, the diary, contractor notes and the language choice stay in the phone's `localStorage` and are never sent anywhere. Secret codes are stored only as salted fingerprints.
- The only data that leaves the phone is:
  - the microphone recording, sent to Google or Apple only when the mic is pressed, and the page says so;
  - the font, downloaded once from Google Fonts.
- Helpline numbers and legal facts are general information. The footer says so and points to 15100 and the district labour office.

---

## 16. Running and rebuilding

**View the site on this Mac:**

```bash
cd "/Users/ridhimasharma/Desktop/HTML PROJECT"
```

```bash
python3 tools/serve.py
```

Then open `http://localhost:8123`.

[serve.py](tools/serve.py) is better than Python's built-in server for this site:
- It tells the browser to re-check pages, scripts and styles every time, so you never see an old cached copy after a change.
- It lets the voice clips cache for good, because their names change whenever their words change.
- It fixes addresses pasted with punctuation stuck on the end, like `login.html,`.

**After changing page text** (in the `tools/build_*.py` files or `tools/i18n.py`):

```bash
cd tools && python3 build_1.py && python3 build_2.py && python3 build_3.py && python3 build_ask.py && python3 build_login.py && python3 build_404.py
```

**After changing spoken text**, re-record. The full steps are in [tools/README.md](tools/README.md):

1. Log out and start the site and `tools/collect_server.py`.
2. Open `http://localhost:8123/tools/collect.html`.
3. Run `python3 tools/make_audio.py`.

**After changing CSS or JS:** raise `VER` in [build_common.py](tools/build_common.py:4) and rebuild, so phones load the new files.

**Publishing:** upload everything except the `tools/` and `docs/` folders to any static web host. HTTPS is needed for the microphone to work. Set the host to send `Cache-Control: no-cache` for `.html`, `.js` and `.css` files, and to cache `audio/` for a long time, the same as `serve.py` does.

---

## 17. Known limits

- **Translations need review.** The Bengali, Marathi, Tamil, Telugu and Kannada text was written for this project and has not been checked by native speakers.
- **Marathi voice.** Marathi is read by the Hindi voice, because macOS has no Marathi voice.
- **Changing text uses the backup voice.** Diary totals and notebook entries use the phone's own voice, which is silent on some browsers and phones.
- **Microphone.** Voice questions need Chrome or Safari and an internet connection. Firefox doesn't support speech recognition, so it gets the picture questions and typing instead.
- **Contractor notes are private.** They are only on one phone. Sharing between workers happens through WhatsApp, not through the site.
- **Accounts can't move.** Accounts are only on one phone and can't be reset or moved to a new phone.
- **Facts change.** Minimum wage amounts change often and differ by state, so the site tells people to ask 14434 or the labour office. Helpline numbers should be re-checked before launch.
