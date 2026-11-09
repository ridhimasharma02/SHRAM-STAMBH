# Changelog

What changed in each version of SHRAM STAMBH. Downloads are on the [releases page](https://github.com/ridhimasharma02/shram-stambh/releases).

## 1.2 — 9 November 2026

### Added
- **Send the diary on WhatsApp.** A button under the diary totals opens WhatsApp with the month's record in Hindi and English: employer, daily wage, each date worked, every payment and the amount still owed. It works as written proof for an employer, union helper or labour officer.
- **Home-screen icon.** `manifest.json` and new icons in `icons/` let people add the site to their phone's home screen and open it by tapping the logo.
- **Hosting files.** `_headers` gives Netlify and Cloudflare Pages long caching for voice clips and standard safety headers. `.nojekyll` makes GitHub Pages serve the files as they are.
- **Issue forms** for wrong facts or helpline numbers, translation and voice fixes, and bugs.
- `.editorconfig`, so every editor uses UTF-8, LF line endings and two-space indents.

### Changed
- Cache number on CSS and JS links raised from 37 to 38.
- README covers the new features, files and hosting.

## 1.1 — 9 November 2026

### Changed
- **New logo:** a raised fist on a pillar over a gear, drawn in each page from simple SVG shapes. It is also the browser tab icon, and the README screenshot shows it.
- **No Python.** The build and recording scripts were removed. The pages, styles, scripts and voice clips are edited directly, and the site opens by double-clicking `index.html`.
- The data files have one entry per line, so they can be read and edited by hand.
- The README was rewritten, with architecture diagrams and a reference section.

## 1.0 — 9 November 2026

First complete version: eleven pages in English and Hindi, recorded voice in seven languages, picture login, work diary, contractor notebook, rights in pictures, "show this screen", helplines, and asking questions by voice.
