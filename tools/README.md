# SHRAM STAMBH build tools

The site is plain HTML, CSS and a little JavaScript. These scripts generate the pages and the recorded voice.

## Run the site

```bash
python3 tools/serve.py
```

Then open http://localhost:8123. This server stops browsers showing old cached copies and fixes links pasted with a stray comma.

## Rebuild the pages

```bash
cd tools
python3 build_1.py && python3 build_2.py && python3 build_3.py && python3 build_ask.py && python3 build_login.py && python3 build_404.py
```

- `build_common.py` holds the shared header, menu, footer, bottom bar and icons. Bump `VER` after changing CSS or JS so phones fetch fresh copies.
- `i18n.py` holds every translation, the 16 assistant answers and the keywords used to match spoken questions.

## Refresh the recorded voice

The voice plays recorded `.m4a` files from `audio/`, so it works even on phones without a Hindi or Tamil voice. After changing any text:

1. Log out of any account on the site. Then run the site on port 8123 and `python3 tools/collect_server.py` (port 8124).
2. Open `http://localhost:8123/tools/collect.html` and wait for "Saved … lines".
3. Run `python3 tools/make_audio.py`. It records new lines with the Mac voices, deletes unused ones and rewrites `audio-manifest.js`.

Text with no recording, such as diary totals, falls back to the phone's own text-to-speech.

## Before going live

- Have a native speaker check each language in `i18n.py`.
- Check the helpline numbers and legal facts against current government sources.
- The `tools/` and `docs/` folders do not need to be uploaded to the web server.
