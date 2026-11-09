# -*- coding: utf-8 -*-
"""Builds ask.html, ask-data.js and lang-data.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_common import page, pagehead, hi, ICONS as I, OUT
import i18n

def write(name, text):
    with open(OUT + name, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", name)

write("ask-data.js", i18n.ask_data_js())
write("lang-data.js", i18n.lang_data_js())

by_id = {t["id"]: t for t in i18n.TOPICS}
qbtns = "\n          ".join(
    f'<button type="button" class="qbtn" data-topic="{tid}">{I[by_id[tid]["icon"]]}<span class="qlabel" lang="hi">{by_id[tid]["label"]["hi"]}</span></button>'
    for tid in i18n.BUTTON_ORDER
)

body = f'''
{pagehead("mic", "t-help", "Ask a question", "सवाल पूछें", "Ask")}

    <div class="panel no-js">
      <p>Asking by voice needs a newer phone browser. Call <a href="tel:15100">15100</a> to ask a person, for free, in your language.{hi("बोलकर पूछने के लिए नया ब्राउज़र चाहिए। किसी इंसान से पूछने के लिए 15100 पर मुफ़्त फ़ोन करें।")}</p>
    </div>

    <div id="ask-root" class="needs-js" {i18n.say_attrs(i18n.UI["howTo"])}>
      <div class="panel askpanel" data-no-say>
        <h2 data-ui="chooseLang">Choose your language</h2>
        <div class="langrow" aria-label="Choose your language"></div>

        <div class="askmain">
          <button type="button" id="mic" class="mic" aria-pressed="false">{I["mic"]}<span id="mic-label">Press and ask your question</span></button>
          <div class="askhelp">
            <button type="button" id="how-say" class="bigsay" {i18n.say_attrs(i18n.UI["howTo"])} aria-label="How to ask">{I["speaker"]}</button>
            <p class="muted" style="margin:0">How to ask · कैसे पूछें</p>
          </div>
        </div>

        <p id="ask-msg" class="warn" role="status" hidden></p>
        <div id="heard" class="heardbox" hidden><span class="lbl"></span><p id="heard-text"></p></div>
        <div id="answer" class="answerbox" aria-live="polite" hidden><span class="lbl"></span><p id="answer-text"></p><div id="answer-actions" class="acts"></div></div>
      </div>

      <div class="panel" id="qgrid" data-no-say>
        <h2 data-ui="orTap">Or tap a question</h2>
        <div class="qgrid">
          {qbtns}
        </div>
      </div>

      <form id="type-form" class="panel typeform" data-no-say autocomplete="off">
        <label for="type-input" data-ui="typeHere">Or type your question</label>
        <div class="payrow">
          <input id="type-input" type="text" enterkeyhint="send">
          <button type="submit" class="btn dark" data-ui="askBtn">Ask</button>
        </div>
      </form>

      <p class="muted">When you press the microphone, your browser sends your voice to Google (in Chrome) or Apple (in Safari) to turn it into words. SHRAM STAMBH does not keep it. The answers are general information. For your own case, call 15100.{hi("माइक्रोफ़ोन दबाने पर आपका ब्राउज़र आपकी आवाज़ को शब्दों में बदलने के लिए Google या Apple को भेजता है। श्रम स्तंभ उसे नहीं रखता। अपने मामले के लिए 15100 पर फ़ोन करें।")}</p>
    </div>
'''
page("ask.html", "Ask a question", body, "Ask a question about wages and workers' rights by speaking in Hindi, English, Bengali, Marathi, Tamil, Telugu or Kannada, and hear the answer.", topic="t-help", extra_js=["ask-data.js", "ask.js"])
