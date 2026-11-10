# Contributing to SHRAM STAMBH

Thank you for helping. This site is used by people who may not be able to read, on cheap phones with slow data, so every change is judged by one question: **does it still work for them?**

## Ground rules

- **Plain files only.** HTML, CSS and JavaScript that browsers run as they are. No frameworks, no build step, no npm packages, no tracking or analytics.
- **Nothing leaves the phone.** Accounts, the diary and notes are saved only in the browser. Don't add anything that sends them to a server.
- **Everything can be heard.** New text on a page must be readable aloud, and fixed sentences should have a recording (see below).
- **Facts need a source.** Helpline numbers, wage rules and laws must come from an official source. Put it in the commit message.

To report a problem instead of fixing it, use the [issue forms](https://github.com/ridhimasharma02/SHRAM-STAMBH/issues/new/choose). If you are a worker who needs help now, call free legal aid on **15100**.

## Changing text on a page

- Each page has English and Hindi side by side. The Hindi is in `<span class="hi" lang="hi">…</span>` right after the English, and the voice uses the `lang` attribute to pick the right part.
- Bengali, Marathi, Tamil, Telugu and Kannada are spoken from `data-say-bn`, `data-say-mr`, `data-say-ta`, `data-say-te` and `data-say-kn` attributes, and from the `*-data.js` files.
- The header, menu, footer and bottom bar are repeated in all eleven pages. Change all of them the same way.
- After changing `style.css` or any `.js` file, raise the `?v=` number on every link in every page, so phones don't keep an old copy.

## Recording the voice for a new or changed sentence

Each clip in `audio/` is named after a fingerprint of its exact words, so a changed sentence has no recording until you make one. Until then the phone's own voice reads it, which is silent on many phones. Recording needs a Mac.

1. **Run the site on localhost** (see the README), log in, and open the page you changed.
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

## Before you commit

Go through the README's [checking after a change](README.md#checking-after-a-change) list. It takes a few minutes and covers the login, every page, the voice and the console.

Keep each commit to one change, with a message that says what changed and why, in plain words.
