# Checking and improving the translations

SHRAM STAMBH speaks seven languages. The Hindi and English were written for the site. The **Bengali, Marathi, Tamil, Telugu and Kannada have not yet been checked by native speakers**, and that has to happen before the site is used with real workers.

You don't need to know any code to help. You need to read the language well, and ideally to know how workers in that region actually talk.

## What to look for

- **Would a worker say it this way?** Prefer everyday spoken words over formal or official ones. "पैसा नहीं मिला" is better than "पारिश्रमिक प्राप्त नहीं हुआ".
- **Is it short?** Every line is heard, not read. Long sentences are hard to follow by ear.
- **Are the facts the same as the English?** Numbers, amounts and rights must match exactly. If the English seems wrong, report that separately.
- **Does it sound right aloud?** Most lines are recorded. Listen to them on the site, in your language, and note any that sound wrong or are hard to understand.

## Where each language's text is

| What | File | How it looks |
|---|---|---|
| Home page tiles, Rights in pictures, and a few boxes on other pages | the `.html` page itself | `data-say-bn="…"`, `data-say-mr="…"`, `data-say-ta="…"`, `data-say-te="…"`, `data-say-kn="…"` on each box |
| The 16 Ask answers, their button labels and the Ask screen's messages | [ask-data.js](../ask-data.js) | `"answer": { "hi": "…", "bn": "…", … }` under each topic, and the `ui` section |
| Words the Ask page listens for | [ask-data.js](../ask-data.js) | `kw` and `weak` lists in each topic, and the `concepts` word groups |
| The login screen | [account-data.js](../account-data.js) | `text`: every line in all seven languages |
| Language names and lines spoken on every page | [lang-data.js](../lang-data.js) | `langs`, `voiceChosen`, `otherLang`, `chooseLang`, `askTitle` |

The pages show only English and Hindi on screen. The other five languages are spoken, so in those files you are checking what people will **hear**.

## The words the Ask page listens for

These matter as much as the answers. When someone asks a question aloud, the site looks for these words in what they said. If people in your region use a different word for "contractor", "wages" or "injury", add it to that topic's `kw` list. Common spellings that speech-to-text might produce are worth adding too.

## How to send a fix

- **Easiest:** open a [translation issue](https://github.com/ridhimasharma02/SHRAM-STAMBH/issues/new?template=translation.yml) and paste what it says now and your better wording.
- **If you are comfortable editing files:** change the text directly and follow [CONTRIBUTING.md](../CONTRIBUTING.md). Every changed spoken line needs a new recording, and the steps for that are there. If you can't record, say so, and the phone's own voice will read the line until someone records it.
