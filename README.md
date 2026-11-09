# SHRAM STAMBH · श्रम स्तंभ

**A free website that helps India's daily-wage, construction, domestic and factory workers get paid fairly and know their rights, even if they cannot read.**

*Shram Stambh* means "pillar of labour".

![SHRAM STAMBH home page on a computer](docs/screenshots/home.jpg)

---

## Contents

- [The problem](#the-problem)
- [What the site does](#what-the-site-does)
- [Screenshots](#screenshots)
- [Languages](#languages)
- [Run it on your computer](#run-it-on-your-computer)
- [Project structure](#project-structure)
- [How it works](#how-it-works)
- [Changing the site](#changing-the-site)
- [Putting it online](#putting-it-online)
- [Accessibility and testing](#accessibility-and-testing)
- [Privacy](#privacy)
- [Before using it with real workers](#before-using-it-with-real-workers)

---

## The problem

Millions of workers in India face the same four problems:

| Problem | What happens |
|---|---|
| **Wage theft** | Workers are paid late, paid less than agreed, or not paid at all, and have no proof of the days they worked. |
| **Not knowing their rights** | Few workers know the minimum wage, pay dates, overtime rules, or that bonded labour is a crime. |
| **No way to check an employer** | There is no easy way to find out whether a contractor pays properly before agreeing to the job. |
| **Language and reading barriers** | Most help is in English, written down, and assumes the reader can read. |

## What the site does

### For people who cannot read
- **Every box can be read aloud.** Press the speaker button on any box to hear it. A "Listen" button reads the whole page.
- **Seven spoken languages.** Every page is written in English and Hindi, and the voice speaks seven Indian languages.
- **Pictures and colours.** Every topic has its own picture and colour: yellow for money, blue for rights, green for a new job, red for help.
- **Picture login.** There is no password. People tap their own picture, then four secret pictures.
- **Call buttons everywhere.** Free legal help (15100) and emergency (112) are one tap away on every page.

### Getting paid
- **Not paid?** Six steps to recover unpaid wages, a message template to send the employer as written proof, and a printable work log.
- **Work diary.** Tap the days you worked, add money as you receive it, and the page works out what you are still owed. It can read the total aloud.

### Knowing your rights
- **Your rights.** Rights for every worker, plus sections for construction, domestic, factory and migrant workers.
- **Rights in pictures.** Twelve rights, one picture each, with sound.

### Before taking a job
- **Questions to ask**, a **job card** for both sides to sign, and **warning signs** of bonded labour.
- **Contractor notebook.** Save notes on whether a contractor paid properly, search them, and send a warning to a WhatsApp group in one tap.

### Getting help
- **Ask a question by voice.** Press the microphone, ask in your own language, and hear the answer. It covers 16 common problems, from unpaid wages to injuries and harassment.
- **Show this screen.** Ready-made messages fill the whole screen, such as "I cannot read, please read this to me", so a worker can hand the phone to an officer or doctor.
- **Helplines.** Free numbers, which office to visit for which problem, and what to say on the phone.

## Screenshots

| Ask a question (phone) | Picture login (phone) |
|---|---|
| ![Asking a question and hearing the answer](docs/screenshots/ask-phone.jpg) | ![Logging in by tapping secret pictures](docs/screenshots/login-phone.jpg) |

![Rights shown as pictures, each with a speaker button](docs/screenshots/rights-in-pictures.jpg)

## Languages

| Language | Written on the pages | Spoken |
|---|---|---|
| Hindi · हिंदी | ✓ every page | ✓ everything |
| English | ✓ every page | ✓ everything |
| Bengali · বাংলা | – | home page, rights in pictures, Ask, login |
| Marathi · मराठी | – | home page, rights in pictures, Ask, login |
| Tamil · தமிழ் | – | home page, rights in pictures, Ask, login |
| Telugu · తెలుగు | – | home page, rights in pictures, Ask, login |
| Kannada · ಕನ್ನಡ | – | home page, rights in pictures, Ask, login |

Where a page has no translation in the chosen language, the voice says so in that language and reads the Hindi.

## Run it on your computer

There is nothing to install and nothing to build. The site is just HTML, CSS and JavaScript files.

**Double-click `index.html`** to open it in Chrome, Edge or Safari. Make an account with any name and a 10-digit mobile number. The account is saved only in that browser.

Opened this way, everything works except asking questions by microphone. Browsers only allow the microphone on a web address (`https://`, or `http://localhost` from a local web server such as the VS Code "Live Server" extension).

## Project structure

```
SHRAM-STAMBH/
├── index.html          Home page
├── rights.html         Your rights
├── pictures.html       Rights in pictures
├── wages.html          Not paid? (steps and printable work log)
├── diary.html          Work diary
├── before-job.html     Before a job, and the contractor notebook
├── show.html           Show this screen
├── ask.html            Ask a question by voice
├── help.html           Helplines and offices
├── login.html          Picture login
├── 404.html            Page not found
│
├── style.css           All styling, in 17 numbered sections
├── speak.js            The voice: plays recordings, reads boxes aloud
├── ask.js              Voice questions: listens, matches, answers
├── account.js          Accounts and the page lock
├── login.js            The login screen
├── diary.js            The work diary
├── site.js             Print buttons and the contractor notebook
├── *-data.js           Text in seven languages, Ask topics, login pictures
│
├── audio/              592 recorded voice clips, one folder per language
└── docs/screenshots/   Images used in this README
```

## How it works

- **No server code and no database.** The site is plain HTML, CSS and JavaScript. Anything a person saves, such as their account, diary and notes, stays in their own browser.
- **Recorded voice.** Every fixed sentence on the site was recorded in advance with the Mac's built-in voices, so it plays on any phone, even one with no Hindi or Tamil voice installed. The phone's own voice is used only for text that changes, like diary totals.
- **Voice questions without AI.** The browser turns speech into text. The site then scores the sentence against 16 topics using keywords in all seven languages, and plays the recorded answer.
- **Picture login.** The four secret pictures are never stored, only a salted SHA-256 fingerprint of them. Five wrong tries lock the account for one minute, and it logs out by itself after 30 minutes unused.

## Changing the site

Edit the files directly. There is no build step.

- **Page text** (English and Hindi) is in each `.html` file.
- **Spoken text in the other five languages** is in `data-say-bn`, `data-say-mr`, `data-say-ta`, `data-say-te` and `data-say-kn` attributes on the boxes, and in the `*-data.js` files.
- **The header, menu, footer and bottom bar** are repeated in every page. Change all eleven pages the same way.
- **New or changed spoken sentences** have no recording yet, because each clip matches its exact words. The phone's own voice reads them instead until they are recorded.
- **After changing `style.css` or a `.js` file**, raise the `?v=36` number on the links in every page, so phones load the new file instead of an old copy.

## Putting it online

Upload everything except the `docs/` folder to any static web host, such as GitHub Pages, Netlify or Cloudflare Pages.

- **Use HTTPS.** The microphone only works on secure addresses.
- **Set caching.** Pages, scripts and styles should be re-checked on every visit (`Cache-Control: no-cache`). The `audio/` folder can be cached for a long time.
- `404.html` is used automatically by most hosts for wrong addresses.

## Accessibility and testing

- **Readable text.** Contrast meets WCAG AA: at least 4.5 : 1, or 3 : 1 for large text.
- **Easy to tap.** Every button is at least about 44 pixels tall.
- **Works with assistive tools.** Every button and form field has a name screen readers can announce, and headings are in order.
- **Fits every screen.** It was tested at eight widths, from 320px phones to 1920px monitors, with no sideways scrolling.
- **Prints cleanly.** The work log and job card print in black and white, without the menus.
- **JavaScript turned off.** Content stays hidden behind the login, and a message with the 15100 and 112 call buttons shows instead.

## Privacy

- No tracking and no analytics.
- Names, mobile numbers, the diary and notes never leave the phone.
- When the microphone is used, the browser sends the voice to Google (Chrome) or Apple (Safari) to turn it into text. The site says this on the Ask page.
- The site never asks for Aadhaar.

## Before using it with real workers

- **Translations.** Have a native speaker check each language in the pages and the `*-data.js` files.
- **Facts.** Check the helpline numbers and legal facts against current government sources. Minimum wages change often and differ by state.
- **Voice input on phones.** Test the microphone on real Android phones and iPhones once the site is on HTTPS.
- **Accounts stay on one phone.** They can't be moved to a new phone or reset. That's by design, but tell users about it.

---

*This site gives general information, not legal advice. For your own case, call free legal aid on **15100** or visit your district labour office.*

No licence has been chosen yet, so by default all rights are reserved by the author.
