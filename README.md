# SHRAM STAMBH · श्रम स्तंभ

**A free website that helps India's daily-wage, construction, domestic and factory workers get paid fairly and know their rights, even if they cannot read.**

*Shram Stambh* means "pillar of labour".

![SHRAM STAMBH home page on a computer](docs/screenshots/home.jpg)

---

## Contents

- [The problem](#the-problem)
- [Who it is for](#who-it-is-for)
- [What the site does](#what-the-site-does)
- [Screenshots](#screenshots)
- [Languages](#languages)
- [Run it on your computer](#run-it-on-your-computer)
- [Changing the site](#changing-the-site)
- [Putting it online](#putting-it-online)
- [Accessibility](#accessibility)
- [Privacy and security](#privacy-and-security)
- [Known limits](#known-limits)
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

## Who it is for

- **Workers**, including people who have never learnt to read. Everything can be heard, every topic has a picture and a colour, and the login uses pictures instead of a password.
- **Helpers**, such as NGO staff, union volunteers and family members who sit with a worker and go through the site together.
- **Shared phones.** One cheap Android phone is often used by a whole family, so each person gets their own private account, diary and notes on the same phone.

## What the site does

### For people who cannot read
- **Every box can be read aloud.** Each box has a speaker button. A "Listen" button in the bottom bar reads the whole page, box by box.
- **Seven spoken languages.** Every page is written in English and Hindi, and the voice speaks seven Indian languages.
- **Pictures and colours.** Every topic has its own picture and colour: yellow for money, blue for rights, green for a new job, red for help.
- **Picture login.** There is no password. People tap their own picture, then four secret pictures.
- **Call buttons everywhere.** Free legal help (15100) and emergency (112) are one tap away on every page, even before logging in.

### Getting paid
- **Not paid?** ([wages.html](wages.html)) Six steps to recover unpaid wages, a message template to send the employer as written proof, and a printable work log.
- **Work diary.** ([diary.html](diary.html)) Tap the days you worked, add money as you receive it, and the page works out what you are still owed. It can read the total aloud.

### Knowing your rights
- **Your rights.** ([rights.html](rights.html)) Rights for every worker, plus sections for construction, domestic, factory and migrant workers.
- **Rights in pictures.** ([pictures.html](pictures.html)) Twelve rights, one picture each, with sound.

### Before taking a job
- **Before a job.** ([before-job.html](before-job.html)) Questions to ask, a **job card** for both sides to sign, and **warning signs** of bonded labour.
- **Contractor notebook.** On the same page: save notes on whether a contractor paid properly, search them, and send a warning to a WhatsApp group in one tap.

### Getting help
- **Ask a question by voice.** ([ask.html](ask.html)) Press the microphone, ask in your own language, and hear the answer. It covers 16 common problems, from unpaid wages to injuries and harassment. People without a microphone can tap a picture question or type instead.
- **Show this screen.** ([show.html](show.html)) Ready-made messages fill the whole screen, such as "I cannot read, please read this to me", so a worker can hand the phone to an officer or doctor.
- **Helplines.** ([help.html](help.html)) Free numbers, which office to visit for which problem, and what to say on the phone.

## Screenshots

| Ask a question (phone) | Picture login (phone) |
|---|---|
| ![Asking a question and hearing the answer](docs/screenshots/ask-phone.jpg) | ![Logging in by tapping secret pictures](docs/screenshots/login-phone.jpg) |

![Rights shown as pictures, each with a speaker button](docs/screenshots/rights-in-pictures.jpg)

## Languages

| Language | Written on the pages | Spoken | Recorded clips |
|---|---|---|---|
| Hindi · हिंदी | ✓ every page | ✓ everything | 128 |
| English | ✓ every page | ✓ everything | 139 |
| Bengali · বাংলা | – | home page, rights in pictures, Ask, login | 65 |
| Marathi · मराठी | – | home page, rights in pictures, Ask, login | 65 |
| Tamil · தமிழ் | – | home page, rights in pictures, Ask, login | 65 |
| Telugu · తెలుగు | – | home page, rights in pictures, Ask, login | 65 |
| Kannada · ಕನ್ನಡ | – | home page, rights in pictures, Ask, login | 65 |

Where a box has no translation in the chosen language, the voice first says so in that language ("this part is only in Hindi and English"), then reads the Hindi.

## Run it on your computer

There is nothing to install and nothing to build. The site is just HTML, CSS and JavaScript files.

**Double-click `index.html`** to open it in Chrome, Edge or Safari. Make an account with any name and a 10-digit mobile number starting with 6, 7, 8 or 9. The account is saved only in that browser.

Opened this way, everything works except asking questions by microphone. Browsers only allow the microphone on a web address (`https://`, or `http://localhost` from a local web server such as the VS Code "Live Server" extension).

## Changing the site

Edit the files directly. There is no build step.

- **Page text** (English and Hindi) is in each `.html` file.
- **Spoken text in the other five languages** is in `data-say-bn`, `data-say-mr`, `data-say-ta`, `data-say-te` and `data-say-kn` attributes on the boxes, and in the `*-data.js` files.
- **The header, menu, footer and bottom bar** are repeated in every page. Change all eleven pages the same way.
- **New or changed spoken sentences** have no recording yet, because each clip matches its exact words. The phone's own voice reads them instead until they are recorded.
- **After changing `style.css` or a `.js` file**, raise the `?v=36` number on the links in every page, so phones load the new file instead of an old copy.

### Checking after a change

1. Log out, then open any page. It should go straight to the login page.
2. Make an account and log in. You should come back to the page you opened.
3. Open every page from the menu. Nothing should be cut off, and there should be no sideways scrolling on a phone-sized window.
4. Press a few speaker buttons in two or three languages. Each should speak once, not twice.
5. Open the browser console (`F12`). There should be no red errors.
6. To check that every spoken line still has a recording, run this in the console on each page. It should print `0`:

   ```js
   ssDebug.collect().filter(p => !ssDebug.audioUrl(p)).length
   ```

## Putting it online

Upload everything except the `docs/` folder to any static web host, such as GitHub Pages, Netlify or Cloudflare Pages.

- **Use HTTPS.** The microphone only works on secure addresses.
- **Set caching.** Pages, scripts and styles should be re-checked on every visit (`Cache-Control: no-cache`). The `audio/` folder can be cached for a long time, because a clip's name changes whenever its words change.
- `404.html` is used automatically by most hosts for wrong addresses.

## Accessibility

- **Readable text.** Contrast meets WCAG AA: at least 4.5 : 1, or 3 : 1 for large text.
- **Easy to tap.** Every button is at least about 44 pixels tall.
- **Works with assistive tools.** Every button and form field has a name screen readers can announce, and headings are in order.
- **Fits every screen.** It was tested at eight widths, from 320px phones to 1920px monitors, with no sideways scrolling.
- **Prints cleanly.** The work log and job card print in black and white, without the menus.
- **JavaScript turned off.** Content stays hidden behind the login, and a message with the 15100 and 112 call buttons shows instead.

## Privacy and security

- No tracking and no analytics.
- Names, mobile numbers, the diary and notes never leave the phone.
- When the microphone is used, the browser sends the voice to Google (Chrome) or Apple (Safari) to turn it into text. The site says this on the Ask page.
- The only other thing downloaded from outside is the Mukta font, from Google Fonts.
- The site never asks for Aadhaar.
- **How strong the login is.** Four secret pictures out of nine give 6,561 possible codes, and five wrong tries lock the account for a minute. That stops family members or co-workers on a shared phone. It does not stop someone with the phone and technical skill, because a website with no server keeps its data in the browser.

## Known limits

- **Accounts stay on one phone.** They can't be moved to a new phone or reset. That's by design, but tell users about it.
- **Changing text uses the backup voice.** Diary totals and notebook entries use the phone's own voice, which is silent on some phones that have no Hindi voice installed.
- **Marathi voice.** Marathi is read by the Hindi voice, because macOS has no Marathi voice.
- **Microphone.** Voice questions need Chrome, Edge or Safari and an internet connection. Firefox doesn't support speech recognition, so it gets the picture questions and typing instead.
- **Contractor notes are private.** They are only on one phone. Sharing between workers happens through WhatsApp, not through the site.

## Before using it with real workers

- **Translations.** Have a native speaker check each language in the pages and the `*-data.js` files. The Bengali, Marathi, Tamil, Telugu and Kannada text has not been checked yet.
- **Facts.** Check the helpline numbers and legal facts against current government sources. Minimum wages change often and differ by state.
- **Voice input on phones.** Test the microphone on real Android phones and iPhones once the site is on HTTPS.

---

*This site gives general information, not legal advice. For your own case, call free legal aid on **15100** or visit your district labour office.*

No licence has been chosen yet, so by default all rights are reserved by the author.
