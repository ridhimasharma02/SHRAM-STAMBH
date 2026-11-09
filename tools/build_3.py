import sys; sys.path.insert(0, sys.path[0])
from build_common import page, pagehead, hi, login_gate, ICONS as I
import i18n

# ---------------- RIGHTS IN PICTURES ----------------
_pic_n = [0]
def pic(icon, en, h, more, bad=False):
    others = i18n.say_attrs(i18n.PICTURES[_pic_n[0]]); _pic_n[0] += 1
    return (f'<li{" class=\"no\"" if bad else ""} {others}><div class="pic">{I[icon]}</div>'
            f'<strong>{en}{hi(h)}</strong><a class="more noread" href="{more}">More</a></li>')

pics = "\n      ".join([
    pic("coins", "At least the minimum wage, for every job", "हर काम में कम से कम न्यूनतम मज़दूरी", "rights.html"),
    pic("calpay", "Paid on time. Daily wage the same day, monthly pay by the 7th", "समय पर पैसा। दिहाड़ी उसी दिन, महीने का पैसा 7 तारीख तक", "rights.html"),
    pic("clock8", "Up to 8 hours of work a day", "दिन में 8 घंटे तक काम", "rights.html"),
    pic("bed", "One day off every week", "हफ़्ते में एक दिन छुट्टी", "rights.html"),
    pic("overtime", "Extra hours are paid double", "ज़्यादा घंटों का दोगुना पैसा", "rights.html"),
    pic("equal", "Same work, same pay for women and men", "एक जैसा काम, औरत और आदमी को बराबर पैसा", "rights.html"),
    pic("helmet", "Helmet, gloves and safety belt are free", "हेलमेट, दस्ताने और सेफ़्टी बेल्ट मुफ़्त", "rights.html#construction"),
    pic("aid", "Hurt at work? The employer must pay compensation", "काम पर चोट लगी? मुआवज़ा मालिक देगा", "rights.html#construction"),
    pic("hand", "Harassment at work can be reported, even inside a home", "काम पर उत्पीड़न की शिकायत हो सकती है, घर के अंदर भी", "rights.html#domestic"),
    pic("chain", "No one can force you to work to pay off a loan", "कर्ज़ के बदले कोई ज़बरदस्ती काम नहीं करवा सकता", "help.html", True),
    pic("idcard", "Never give your original Aadhaar or documents to the employer", "अपना असली आधार या कागज़ मालिक को न दें", "before-job.html", True),
    pic("child", "Children under 14 must not be made to work", "14 साल से कम उम्र के बच्चे से काम करवाना मना है", "help.html", True),
])

pictures = f'''
{pagehead("pictures", "t-rights", "Your rights in pictures", "तस्वीरों में आपके अधिकार", "Rights in pictures")}

    <div class="listen-intro needs-speech">
      <button type="button" class="bigsay" data-read="#pics" aria-label="Listen to all the pictures">{I["speaker"]}</button>
      <p><strong>Press to hear all of them, one by one.</strong>{hi("सब एक-एक करके सुनने के लिए दबाएँ।")}
      <span class="muted">Or press the small speaker on one picture.</span></p>
    </div>

    <p class="muted">Blue pictures are what you are owed. Red pictures are things nobody is allowed to do to you.{hi("नीली तस्वीरें आपके हक़ हैं। लाल तस्वीरें वो हैं जो कोई आपके साथ नहीं कर सकता।")}</p>

    <ul class="pics" id="pics">
      {pics}
    </ul>

    <p><a href="rights.html">Read the full rights page</a> &nbsp;·&nbsp; <a href="show.html">Show a message to an officer</a></p>
'''
page("pictures.html", "Rights in pictures", pictures, "Workers' rights in India shown as simple pictures with read-aloud in Hindi and English.", topic="t-rights")

# ---------------- SHOW THIS SCREEN ----------------
def card(i, topic, icon, en, h):
    return f'''<li class="showcard {topic}" id="c{i}">{I[icon]}
        <p class="big">{en}{hi(h)}</p>
        <a class="open noread" href="#c{i}">Show big · बड़ा करके दिखाएँ</a>
        <a class="close noread" href="#cards">Close · बंद करें</a>
      </li>'''

cards = "\n      ".join([
    card(1, "t-help", "ear", "I cannot read. Please read this to me.", "मैं पढ़ नहीं सकता/सकती। कृपया यह मुझे पढ़कर सुनाइए।"),
    card(2, "t-wages", "money", "I have not been paid for my work. Please help me write a complaint.", "मुझे मेरे काम का पैसा नहीं मिला है। कृपया शिकायत लिखने में मेरी मदद कीजिए।"),
    card(3, "t-rights", "rights", "I need free legal help. Please connect me to legal aid, or call 15100.", "मुझे मुफ़्त कानूनी मदद चाहिए। कृपया मुझे कानूनी सहायता से जोड़िए या 15100 पर फ़ोन कीजिए।"),
    card(4, "t-help", "phone", "Please call this number for me: 15100", "कृपया मेरे लिए इस नंबर पर फ़ोन कीजिए: 15100"),
    card(5, "t-help", "police", "I am being forced to work and I cannot leave. Please call the police on 112.", "मुझसे ज़बरदस्ती काम करवाया जा रहा है और मुझे जाने नहीं दिया जा रहा। कृपया 112 पर पुलिस को बुलाइए।"),
    card(6, "t-job", "nothumb", "Please read this paper to me before I sign or give my thumbprint.", "साइन या अंगूठा लगाने से पहले कृपया यह कागज़ मुझे पढ़कर सुनाइए।"),
    card(7, "t-help", "aid", "I was hurt at work. Please help me get treatment, and keep the bills.", "मुझे काम पर चोट लगी है। कृपया इलाज में मदद कीजिए और बिल संभालकर रखिए।"),
    card(8, "t-wages", "idcard", "Please give my documents back to me. You cannot keep them.", "कृपया मेरे कागज़ मुझे वापस दीजिए। आप इन्हें अपने पास नहीं रख सकते।"),
])

show = f'''
{pagehead("show", "t-help", "Show this screen to someone", "यह स्क्रीन किसी को दिखाएँ", "Show this screen")}
    <p class="lead">Choose a message and press <strong>Show big</strong>. Then hand your phone to the officer, doctor or helper. The message fills the whole screen.{hi("संदेश चुनें और ‘बड़ा करके दिखाएँ’ दबाएँ। फिर फ़ोन अधिकारी, डॉक्टर या मददगार को दें। संदेश पूरी स्क्रीन पर दिखेगा।")}</p>
    <p class="muted needs-speech">The speaker button plays the message out loud, so you can check it is the right one before showing it.</p>

    <ul class="showcards" id="cards">
      {cards}
    </ul>
'''
page("show.html", "Show this screen", show, "Ready-made messages in English and Hindi that a worker can show to an officer, doctor or helper.", topic="t-help")

# ---------------- WORK DIARY ----------------
diary = f'''
{pagehead("diary", "t-wages", "My work diary", "मेरा काम का हिसाब", "Work diary")}

    <div class="panel no-js">
      <p>This diary needs a newer phone browser. Use the <a href="wages.html">printable work log</a> instead, or any notebook.{hi("यह डायरी आपके ब्राउज़र में नहीं चलेगी। ‘पैसा नहीं मिला?’ पन्ने वाली कॉपी इस्तेमाल करें।")}</p>
    </div>

    {login_gate("diary.html")}

    <div class="needs-js" data-private>
      <div class="panel t-wages" id="how">
        <h2>How to use it{hi("कैसे इस्तेमाल करें")}</h2>
        <ol class="steps">
          <li><h3>Write your daily wage{hi("अपनी रोज़ की मज़दूरी लिखें")}</h3></li>
          <li><h3>Tap every day you worked{hi("जिस दिन काम किया, उस दिन पर दबाएँ")}</h3>
            <p>Tap once for a full day. Tap again for half a day. Tap a third time to clear.{hi("एक बार दबाएँ: पूरा दिन। दोबारा: आधा दिन। तीसरी बार: हटाएँ।")}</p></li>
          <li><h3>When you get money, add it{hi("जब पैसा मिले, उसे जोड़ें")}</h3></li>
          <li><h3>Take a screenshot every week{hi("हर हफ़्ते स्क्रीनशॉट लें")}</h3>
            <p>The diary is saved only on this phone. A screenshot is proof you can show the labour office.{hi("यह हिसाब सिर्फ़ इसी फ़ोन में है। स्क्रीनशॉट श्रम कार्यालय में सबूत बनेगा।")}</p></li>
        </ol>
      </div>

      <div class="panel" id="employer">
        <h2>Employer and wage{hi("मालिक और मज़दूरी")}</h2>
        <div class="diary-top">
          <div class="field">{I["money"]}<label for="rate">Daily wage ₹{hi("रोज़ की मज़दूरी ₹")}</label><input id="rate" type="number" inputmode="numeric" min="0" step="1" placeholder="600"></div>
          <div class="field">{I["people"]}<label for="emp-name">Employer or contractor{hi("मालिक या ठेकेदार")}</label><input id="emp-name" type="text" autocomplete="off"></div>
          <div class="field">{I["phone"]}<label for="emp-phone">Their phone number{hi("उनका फ़ोन नंबर")}</label><input id="emp-phone" type="tel" inputmode="tel" autocomplete="off"></div>
          <div class="field">{I["house"]}<label for="emp-site">Work place{hi("काम की जगह")}</label><input id="emp-site" type="text" autocomplete="off"></div>
        </div>
      </div>

      <div class="panel t-wages" id="month" data-no-say>
        <h2>Days worked{hi("काम के दिन")}</h2>
        <div class="monthbar">
          <button type="button" id="prev" aria-label="Previous month">&lsaquo;</button>
          <div class="mname" id="mname" aria-live="polite"></div>
          <button type="button" id="next" aria-label="Next month">&rsaquo;</button>
        </div>
        <div class="cal" id="cal" role="grid" aria-label="Days of the month"></div>
        <ul class="legend">
          <li><i class="full"></i>Full day · पूरा दिन</li>
          <li><i class="half"></i>Half day · आधा दिन</li>
          <li><i></i>No work · काम नहीं</li>
        </ul>
        <div class="totals" aria-live="polite">
          <div><span>Days worked<br><span lang="hi">काम के दिन</span></span><b id="t-days">0</b></div>
          <div><span>Earned<br><span lang="hi">कमाई</span></span><b id="t-earned">₹0</b></div>
          <div><span>Received<br><span lang="hi">मिला</span></span><b id="t-paid">₹0</b></div>
          <div><span>Still owed<br><span lang="hi">बाकी</span></span><b id="t-owed">₹0</b></div>
        </div>
        <button type="button" class="btn dark needs-speech" id="say-sum" style="width:100%">Hear this month's total · इस महीने का हिसाब सुनें</button>
      </div>

      <div class="panel t-wages" id="money">
        <h2>Money received this month{hi("इस महीने मिला पैसा")}</h2>
        <div class="payrow">
          <div class="field">{I["coins"]}<label for="pay-amt">Amount ₹{hi("रकम ₹")}</label><input id="pay-amt" type="number" inputmode="numeric" min="1" step="1"></div>
          <button type="button" class="btn dark" id="pay-add">Add · जोड़ें</button>
        </div>
        <ul class="paylist" id="paylist"></ul>
        <p class="muted">Money is added to today's date if this month is showing, otherwise to the last day of the month you are looking at.</p>
      </div>

      <div class="panel">
        <h2>Saved on this phone only{hi("सिर्फ़ इस फ़ोन में सेव है")}</h2>
        <p>Nothing here is sent anywhere. If you clear your browser, the diary is deleted. Take screenshots so you don't lose your proof.{hi("यह जानकारी कहीं नहीं भेजी जाती। ब्राउज़र साफ़ करने पर हिसाब मिट जाएगा। स्क्रीनशॉट लेते रहें।")}</p>
        <button type="button" class="btn" id="clear-month">Clear this month · यह महीना मिटाएँ</button>
      </div>
    </div>
'''
page("diary.html", "Work diary", diary, "A tap-based work diary that counts days worked and wages owed, saved only on your own phone.", topic="t-wages", extra_js="diary.js")
