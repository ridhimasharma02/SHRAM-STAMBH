# Changelog

What changed in each version of SHRAM STAMBH. Downloads are on the [releases page](https://github.com/ridhimasharma02/SHRAM-STAMBH/releases).

## Not released yet

### Added
- **CONTRIBUTING.md**, with the ground rules and the steps to record a new voice line on a Mac.
- The "New issue" page links people with their own legal case to NALSA, and tells them to call 15100 instead of posting their details.

### Fixed
- **Printouts.** "Print this log" and "Print the job card" no longer appear on their own printouts, and neither do the listen box or the diary's buttons. The print rules were weaker than the screen rules that show those elements.
- **Diary on WhatsApp** no longer sends an empty month. With no days marked and nothing received, it asks (in recorded Hindi and English) for the days first.
- **Footer share link** opens WhatsApp in a new tab instead of leaving the site.

### Changed
- The README explains how to run the site on localhost, with a Mac command that serves the voice clips as audio.
- Two new voice clips (594 in all). Cache number raised to 40.
- The comments at the top of `speak.js`, `account.js`, `diary.js` and `site.js` describe the code as it is now. The test checklist (now in `CONTRIBUTING.md`) covers printing and the diary's WhatsApp message.

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
