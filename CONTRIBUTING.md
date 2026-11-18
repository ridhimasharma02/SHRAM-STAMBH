# Contributing to SHRAM STAMBH

Thank you for helping. This site is used by people who may not be able to read, on cheap phones with slow data, so every change is judged by one question: **does it still work for them?**

## Ground rules

- **Plain files only.** HTML, CSS and JavaScript that browsers run as they are. No frameworks, no build step, no npm packages, no tracking or analytics.
- **Nothing leaves the phone.** Accounts, the diary and notes are saved only in the browser. Don't add anything that sends them to a server.
- **Everything can be heard.** New text on a page must be readable aloud, and fixed sentences should have a recording (see below).
- **Facts need a source.** Helpline numbers, wage rules and laws must come from an official source. Put it in the commit message.

To report a problem instead of fixing it, use the [issue forms](https://github.com/ridhimasharma02/SHRAM-STAMBH/issues/new/choose). If you are a worker who needs help now, call free legal aid on **15100**.

## Running it on your computer

To test a change before it goes live, run the site on localhost, which browsers treat as secure, so the microphone works too:

- **On a Mac, with nothing to install,** open Terminal in the project folder and run this, then open **http://localhost:8123**. Press `Ctrl + C` to stop it.

  ```bash
  ruby -rwebrick -e 'm = WEBrick::HTTPUtils::DefaultMimeTypes.merge("m4a" => "audio/mp4"); s = WEBrick::HTTPServer.new(Port: 8123, DocumentRoot: ".", MimeTypes: m); trap("INT") { s.shutdown }; s.start'
  ```

  It uses the Ruby that comes with macOS. The `m4a` part makes it send the voice clips as audio, which Safari needs.
- **On any computer with VS Code,** install the "Live Server" extension, right-click `index.html` and choose **Open with Live Server**. It opens at **http://localhost:5500**.

## Changing text on a page

- Each page has English and Hindi side by side. The Hindi is in `<span class="hi" lang="hi">…</span>` right after the English, and the voice uses the `lang` attribute to pick the right part.
- Bengali, Marathi, Tamil, Telugu and Kannada are spoken from `data-say-bn`, `data-say-mr`, `data-say-ta`, `data-say-te` and `data-say-kn` attributes, and from the `*-data.js` files. [docs/TRANSLATING.md](docs/TRANSLATING.md) maps exactly where, for anyone checking a language.
- The header, menu, footer and bottom bar are repeated in all eleven pages. Change all of them the same way.
- After changing `style.css` or any `.js` file, raise the `?v=` number on every link in every page, so phones don't keep an old copy.

## Adding a new page

There is no template engine, so a new page starts as a copy of an existing one. Copy the page closest to what you need (`help.html` is a good plain example), rename it, then:

1. **Keep the `<head>` as it is,** apart from the `<title>`, `description` and `og:` lines. In particular keep the page-lock script at the top and the `?v=` numbers on every link, which must match the other pages.
2. **Set the topic colour** on `<body>`: `t-wages` (money), `t-rights`, `t-job` or `t-help`.
3. **Replace only what is inside `<div class="content">`.** Use `<div class="panel">` boxes with English and Hindi side by side, so each box gets a speaker button and can be read aloud.
4. **Link to the new page** from the footer's list of pages in all eleven existing pages, and from the main menu if it is a main section. Mark the menu item `aria-current="page"` on the new page itself.
5. **Record its spoken lines** (below), then go through the checks at the end of this guide, including print preview and a phone-sized window.

## Recording the voice for a new or changed sentence

Each clip in `audio/` is named after a fingerprint of its exact words, so a changed sentence has no recording until you make one. Until then the phone's own voice reads it, which is silent on many phones. Recording needs a Mac.

1. **Run the site on localhost** (see [Running it on your computer](#running-it-on-your-computer)), log in, and open the page you changed.
2. **List the lines without a recording.** In the browser console:

   ```js
   ssDebug.collect().filter(p => !ssDebug.audioUrl(p))
   ```

   Each result has a `lang`, the exact `text` and its `hash`. Lines spoken from scripts, such as the diary's messages, are included too.
3. **Copy the text exactly.** Retyping Hindi can change invisible characters, and then the fingerprint won't match. In the console, `copy(ssDebug.collect().filter(p => !ssDebug.audioUrl(p))[0].text)` puts the first one on the clipboard. Then in Terminal:

   ```bash
   pbpaste > line.txt
   ```

4. **Record it with the voice for that language,** then compress it. Use the `lang` and `hash` from step 2 in the file name:

   | Language | Command |
   |---|---|
   | Hindi `hi`, Marathi `mr` | `say -v Lekha -f line.txt -o line.aiff` |
   | English `en` | `say -v Tara -r 165 -f line.txt -o line.aiff` |
   | Bengali `bn` | `say -v Piya -f line.txt -o line.aiff` |
   | Tamil `ta` | `say -v Vani -f line.txt -o line.aiff` |
   | Telugu `te` | `say -v Geeta -f line.txt -o line.aiff` |
   | Kannada `kn` | `say -v Soumya -f line.txt -o line.aiff` |

   ```bash
   afconvert -f m4af -d aac -b 32000 -c 1 line.aiff audio/hi/0a1b2c3d.m4a
   ```

5. **Add it to the list** in [audio-manifest.js](audio-manifest.js), keeping the lines in alphabetical order:

   ```js
   "hi:0a1b2c3d": 1,
   ```

6. **Check.** Reload the page and run the console line from step 2 again. It should return an empty list. Then raise the `?v=` number, because `audio-manifest.js` changed.

If you can't record, leave the sentence unrecorded and say so in the commit message. The phone's voice will read it until someone with a Mac records it.

## Checking after a change

Run the site on localhost ([how](#running-it-on-your-computer)) and go through this list. It takes a few minutes.

1. Log out, then open any page. It should go straight to the login page.
2. Make an account and log in. You should come back to the page you opened.
3. Open every page from the menu. Nothing should be cut off, and there should be no sideways scrolling on a phone-sized window.
4. Press a few speaker buttons in two or three languages. Each should speak once, not twice.
5. Open the browser console (`F12`). There should be no red errors.
6. To check that every spoken line still has a recording, run this in the console on each page. It should print `0`:

   ```js
   ssDebug.collect().filter(p => !ssDebug.audioUrl(p)).length
   ```

7. Open print preview (`Ctrl + P`, or `Cmd + P` on a Mac) on the wages page and the diary. Only the content should show: no menus, speaker buttons or print buttons.
8. In the diary, mark a day and press **Send this month on WhatsApp**. The message should match the totals on screen.

Keep each commit to one change, with a message that says what changed and why, in plain words.
