# -*- coding: utf-8 -*-
"""Builds login.html and account-data.js."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_common import page, pagehead, hi, ICONS as I, OUT
import i18n

with open(OUT + "account-data.js", "w", encoding="utf-8") as f:
    f.write(i18n.account_data_js(I))
print("wrote account-data.js")

T = i18n.LOGIN
def t(key, tag="span", cls=""):
    """English text in the HTML; login.js swaps in the chosen language."""
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-t="{key}">{T[key]["en"]}</{tag}>'

body = f'''
{pagehead("lock", "t-rights", "Log in", "लॉग इन", "Log in")}

    <div class="panel no-js">
      <p>Logging in needs a newer phone browser. For help now, call <a href="tel:15100">15100</a> (free legal help) or <a href="tel:112">112</a> (emergency).{hi("लॉग इन के लिए नया ब्राउज़र चाहिए। अभी मदद के लिए 15100 या 112 पर फ़ोन करें।")}</p>
    </div>

    <div id="login-root" class="needs-js" {i18n.say_attrs(T["intro"])}>
      <div class="panel login-top" data-no-say>
        <div class="login-intro">
          <button type="button" class="bigsay" {i18n.say_attrs(T["intro"])} aria-label="Listen: how to log in">{I["speaker"]}</button>
          <div>
            <p><strong>Log in to use SHRAM STAMBH.</strong> No reading needed: tap your picture, then your four secret pictures. New here? Make an account with your name and mobile number.{hi("श्रम स्तंभ इस्तेमाल करने के लिए लॉग इन करें। अपनी तस्वीर दबाएँ, फिर चार गुप्त तस्वीरें। नए हैं? नाम और मोबाइल नंबर से खाता बनाएँ।")}</p>
            <div class="langrow" aria-label="Choose your language"></div>
          </div>
        </div>
      </div>

      <section class="panel login-step" id="s-who" hidden data-no-say>
        {t("whoAreYou", "h2")}
        <div class="who-list" id="who-list"></div>
        <button type="button" class="new-btn" id="btn-new">{I["plus"]}{t("newUser")}</button>
      </section>

      <section class="panel login-step" id="s-avatar" hidden data-no-say>
        {t("choosePic", "h2")}
        <div class="pick-grid" id="avatar-grid"></div>
        <div class="step-actions">
          <button type="button" class="btn" id="av-back">{t("back")}</button>
          <button type="button" class="btn dark" id="av-next" disabled>{t("next")} &rsaquo;</button>
        </div>
      </section>

      <section class="panel login-step" id="s-details" hidden data-no-say>
        <div class="secret-head">
          <span id="det-avatar"></span>
          {t("detailsPrompt", "h2")}
        </div>
        <form id="details-form" class="details-form" novalidate>
          <label class="name-label" for="name">{I["person"]}{t("nameLabel")}</label>
          <div class="name-row">
            <input id="name" type="text" maxlength="40" autocomplete="name" enterkeyhint="next" required>
            <button type="button" class="btn mic-mini" id="name-mic" aria-pressed="false">{I["mic"]}{t("sayName")}</button>
          </div>
          <label class="name-label" for="mobile">{I["phone"]}{t("mobileLabel")}</label>
          <input id="mobile" type="tel" inputmode="numeric" maxlength="14" autocomplete="tel-national" enterkeyhint="done" placeholder="98765 43210" required>
          <p class="warn" id="det-msg" role="alert" hidden></p>
          <div class="step-actions">
            <button type="button" class="btn" id="det-back">{t("back")}</button>
            <button type="submit" class="btn dark" id="det-next">{t("next")} &rsaquo;</button>
          </div>
        </form>
      </section>

      <section class="panel login-step" id="s-secret" hidden data-no-say>
        <div class="secret-head">
          <span id="secret-avatar"></span>
          <h2 id="secret-title">{T["enterSecret"]["en"]}</h2>
        </div>
        <div class="dots" id="dots" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
        <p class="sr-only" id="dots-live" aria-live="polite"></p>
        <p class="warn" id="lock-msg" role="status" hidden></p>
        <div class="secret-grid" id="secret-grid"></div>
        <div class="step-actions">
          <button type="button" class="btn" id="sec-back">{t("back")}</button>
          <button type="button" class="btn" id="sec-clear">{t("clear")}</button>
        </div>
        <div id="forgot-wrap" hidden>
          <button type="button" class="linkbtn" id="forgot-link">{t("forgot")}</button>
          <div class="forgot-box" id="forgot-box" hidden>
            {t("forgotInfo", "p")}
            <button type="button" class="btn" id="forgot-remove">{t("removeAccount")}</button>
            <button type="button" class="btn red" id="forgot-yes" hidden>{t("confirmRemove")}</button>
          </div>
        </div>
      </section>

      <section class="panel login-step" id="s-in" hidden data-no-say>
        <div class="in-head">
          <span id="in-avatar"></span>
          <div>{t("loggedInAs", "h2")}<p class="in-name" id="in-name"></p><p class="in-mobile" id="in-mobile"></p></div>
        </div>
        <a class="btn dark in-continue" id="in-continue" href="index.html">{t("next")} &rsaquo;</a>
        <div class="in-links">
          <a href="diary.html" class="in-link t-wages">{I["diary"]}<span>My work diary{hi("मेरा काम का हिसाब")}</span></a>
          <a href="before-job.html#notebook" class="in-link t-job">{I["job"]}<span>Contractor notebook{hi("ठेकेदार की डायरी")}</span></a>
          <a href="ask.html" class="in-link t-help">{I["mic"]}<span>Ask a question{hi("सवाल पूछें")}</span></a>
          <a href="index.html" class="in-link">{I["home"]}<span>Home{hi("मुख्य पन्ना")}</span></a>
        </div>
        <div class="step-actions">
          <button type="button" class="btn dark" id="in-logout">{t("logout")}</button>
          <button type="button" class="btn" id="in-remove">{t("removeAccount")}</button>
          <button type="button" class="btn red" id="in-remove-yes" hidden>{t("confirmRemove")}</button>
        </div>
      </section>

      <p class="muted login-note">{I["lock"]}{t("onThisPhone")}</p>
    </div>
'''
page("login.html", "Log in", body, "Log in to SHRAM STAMBH with pictures: no reading needed. New users make an account with their name and mobile number.", topic="t-rights", extra_js=["login.js"], guard=False)
