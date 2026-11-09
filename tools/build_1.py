import sys; sys.path.insert(0, sys.path[0])
from build_common import page, pagehead, ICONS as I
import i18n

def hi(t): return f'<span class="hi" lang="hi">{t}</span>'

# ---------------- HOME ----------------
def tile(href, topic, icon, en, h, desc, say_hi, say_en):
    others = i18n.say_attrs(i18n.TILES[href])
    return (f'<li class="{topic}" data-say-hi="{say_hi}" data-say-en="{say_en}" {others}><a href="{href}">{I[icon]}'
            f'<strong>{en}{hi(h)}</strong><span class="desc">{desc}</span></a></li>')

tiles = "\n      ".join([
    tile("wages.html", "t-wages", "money", "Not paid, or paid less", "पैसा नहीं मिला या कम मिला",
         "How to keep proof and get your money back",
         "पैसा नहीं मिला या कम मिला? यह पीला डिब्बा दबाएँ। पैसा वापस पाने के तरीके यहाँ हैं।",
         "Not paid, or paid less? Tap this yellow box to learn how to get your money back."),
    tile("diary.html", "t-wages", "diary", "My work diary", "मेरा काम का हिसाब",
         "Tap the days you worked. It adds up what you are owed",
         "मेरा काम का हिसाब। जिस दिन काम किया उस दिन पर दबाएँ, यह अपने आप जोड़ देगा कि कितना पैसा बाकी है।",
         "My work diary. Tap the days you worked and it adds up how much money you are owed."),
    tile("pictures.html", "t-rights", "pictures", "Your rights in pictures", "तस्वीरों में आपके अधिकार",
         "Twelve rights, one picture each, with sound",
         "तस्वीरों में आपके अधिकार। हर अधिकार की एक तस्वीर है, और आप उसे सुन भी सकते हैं।",
         "Your rights in pictures. Each right has one picture, and you can listen to it."),
    tile("before-job.html", "t-job", "job", "Before you take a job", "काम पकड़ने से पहले",
         "Questions to ask, a job card, warning signs",
         "काम पकड़ने से पहले। मालिक से क्या पूछें और किन बातों से सावधान रहें।",
         "Before you take a job. What to ask the employer, and warning signs to watch for."),
    tile("show.html", "t-help", "show", "Show this screen to someone", "यह स्क्रीन किसी को दिखाएँ",
         "Ready messages to show an officer or helper",
         "यह स्क्रीन किसी को दिखाएँ। यहाँ बने बनाए संदेश हैं जो आप किसी अधिकारी या मददगार को दिखा सकते हैं।",
         "Show this screen to someone. Ready messages you can show to an officer or a helper."),
    tile("help.html", "t-help", "phone", "Talk to someone now", "अभी किसी से बात करें",
         "Free helplines, offices, what to say",
         "अभी किसी से बात करें। मुफ़्त फ़ोन नंबर और दफ़्तर। नीचे की पट्टी में भी फ़ोन के बटन हैं।",
         "Talk to someone now. Free phone numbers and offices. The bar at the bottom also has call buttons."),
])

INTRO_HI = ("नमस्ते। श्रम स्तंभ में आपका स्वागत है। यह साइट मज़दूरों की मदद के लिए है। हर डिब्बे पर एक स्पीकर का बटन है, उसे दबाकर सुनें। "
            "पीले रंग वाले डिब्बे पैसे के बारे में हैं। नीले रंग वाले आपके अधिकार हैं। हरे रंग वाले नया काम पकड़ने से पहले के लिए हैं। लाल रंग वाले मदद के लिए हैं। "
            "स्क्रीन के सबसे नीचे तीन बटन हमेशा रहते हैं। पहला बटन मुफ़्त कानूनी मदद, एक पाँच एक शून्य शून्य, पर फ़ोन करता है। "
            "बीच वाला लाल बटन खतरे में एक एक दो पर फ़ोन करता है। तीसरा बटन यह पूरा पन्ना पढ़कर सुनाता है।")
INTRO_EN = ("Hello. Welcome to Shram Stambh. This site is here to help workers. Every box has a speaker button. Press it to listen. "
            "Yellow boxes are about money. Blue boxes are your rights. Green boxes are for before you take a new job. Red boxes are for getting help. "
            "At the bottom of the screen there are always three buttons. The first calls free legal help on 1 5 1 0 0. "
            "The red one in the middle calls 1 1 2 if you are in danger. The third one reads the whole page out loud.")

home = f"""
    <div class="listen-intro needs-speech only-narrow">
      <button type="button" class="bigsay" {i18n.say_attrs(i18n.INTRO)} aria-label="Listen: how to use this site">{I["speaker"]}</button>
      <div>
        <p><strong>Can't read? Press this to listen.</strong>{hi("पढ़ नहीं सकते? सुनने के लिए यह बटन दबाएँ।")}</p>
        <p class="muted" style="margin:8px 0 4px">Choose your language · अपनी भाषा चुनें</p>
        <div class="langrow" aria-label="Choose your language"></div>
      </div>
    </div>

    <div class="askwrap only-narrow" {i18n.say_attrs(i18n.ASK_BANNER)}>
      <a class="askbanner" href="ask.html">
        <span class="mic-ico">{I["mic"]}</span>
        <span><strong>Ask a question by speaking</strong>{hi("बोलकर सवाल पूछें")}<span class="desc">Press, ask in your language, hear the answer. 7 languages.</span></span>
      </a>
    </div>

    <div class="home-head">
      <h1>What do you need today?{hi("आज आपको क्या चाहिए?")}</h1>
      <p class="lead">Free help for daily-wage, construction, domestic and factory workers in India. Tap a box, or press its speaker to listen.{hi("दिहाड़ी, निर्माण, घरेलू और फ़ैक्ट्री मज़दूरों के लिए मुफ़्त मदद। कोई डिब्बा दबाएँ, या सुनने के लिए स्पीकर दबाएँ।")}</p>
    </div>

    <ul class="tiles">
      {tiles}
    </ul>

    <div class="panel">
      <h2>Three things every worker should do{hi("हर मज़दूर ये तीन काम ज़रूर करे")}</h2>
      <ol>
        <li><strong>Write down every day you work</strong> and how much you were paid. The <a href="diary.html">work diary</a> on this site does it with taps, no reading needed.{hi("हर दिन का काम और मिला पैसा लिखें। इस साइट की ‘काम का हिसाब’ डायरी में बस दबाना है।")}</li>
        <li><strong>Get the employer's real name and phone number</strong> before you start, not after.{hi("काम शुरू करने से पहले मालिक/ठेकेदार का असली नाम और फ़ोन नंबर लें।")}</li>
        <li><strong>Never hand over your original Aadhaar card, bank passbook or phone.</strong> Give a photocopy if they need one.{hi("अपना असली आधार कार्ड, बैंक पासबुक या फ़ोन किसी को न दें। ज़रूरत हो तो फ़ोटोकॉपी दें।")}</li>
      </ol>
    </div>

    <div class="split">
      <div class="panel">
        <h2>If reading is hard{hi("अगर पढ़ना मुश्किल है")}</h2>
        <ul>
          <li>Press the speaker button on any box to hear it in Hindi or English. Change the voice at the top of the screen.{hi("किसी भी डिब्बे का स्पीकर बटन दबाकर हिंदी या अंग्रेज़ी में सुनें।")}</li>
          <li>Find things by colour. Yellow is money, blue is rights, green is a new job, red is help.{hi("रंग से पहचानें: पीला पैसा, नीला अधिकार, हरा नया काम, लाल मदद।")}</li>
          <li>Tap any phone number to call. The people on these lines explain things by talking.{hi("किसी भी नंबर पर दबाकर सीधे फ़ोन करें। वहाँ लोग बोलकर समझाते हैं।")}</li>
          <li>Use <a href="show.html">Show this screen</a> to show a ready message to an officer or helper.{hi("‘यह स्क्रीन दिखाएँ’ से बना बनाया संदेश किसी अधिकारी को दिखाएँ।")}</li>
        </ul>
      </div>
      <div class="panel">
        <h2>About this site{hi("इस साइट के बारे में")}</h2>
        <p>Free to use. Your name, mobile number and work diary stay on your own phone and are never sent anywhere.{hi("यह मुफ़्त है। आपका नाम, मोबाइल नंबर और काम का हिसाब सिर्फ़ आपके फ़ोन में रहता है, कहीं नहीं भेजा जाता।")}</p>
        <p>Rules are different in each state. Use this site to know what to ask, then check with the labour office or legal aid.{hi("हर राज्य के नियम अलग हैं। यहाँ से जानें क्या पूछना है, फिर श्रम कार्यालय से पक्का करें।")}</p>
      </div>
    </div>
"""
page("index.html", "Home", home, "Free information in English and Hindi, with read-aloud, for construction, domestic, factory and daily-wage workers in India.")

# ---------------- RIGHTS ----------------
def row(right, right_hi, what, what_hi):
    return f'<tr><td><strong>{right}</strong>{hi(right_hi)}</td><td>{what}{hi(what_hi)}</td></tr>'

rows = "\n".join([
    row("Minimum wage", "न्यूनतम मज़दूरी",
        "Every job must pay at least the minimum wage set by your state. This includes domestic work and daily-wage work. Being new or a helper does not change this.",
        "हर काम में कम से कम राज्य की तय न्यूनतम मज़दूरी मिलनी चाहिए। घरेलू काम और दिहाड़ी भी इसमें आते हैं। नया या हेल्पर होने से यह नहीं बदलता।"),
    row("Paid on time", "समय पर भुगतान",
        "Daily wage: at the end of the shift. Weekly: on the last working day of the week. Monthly: before the 7th of the next month.",
        "दिहाड़ी: उसी दिन शिफ़्ट खत्म होने पर। हफ़्तेवार: हफ़्ते के आखिरी कामकाजी दिन। महीनेवार: अगले महीने की 7 तारीख से पहले।"),
    row("No unfair cuts", "गलत कटौती नहीं",
        "Pay can only be cut for reasons the law allows, such as PF or an advance you took. All cuts together cannot be more than half your pay.",
        "पैसा सिर्फ़ कानूनी कारणों से कट सकता है, जैसे PF या लिया हुआ एडवांस। कुल कटौती आधी मज़दूरी से ज़्यादा नहीं हो सकती।"),
    row("Overtime", "ओवरटाइम",
        "Work beyond your normal hours must be paid at least double the normal rate.",
        "तय घंटों से ज़्यादा काम का कम से कम दोगुना पैसा मिलना चाहिए।"),
    row("Hours and rest", "घंटे और आराम",
        "Normally up to 8 hours a day with a break, and one day off every week.",
        "आम तौर पर दिन में 8 घंटे तक, बीच में आराम, और हफ़्ते में एक दिन छुट्टी।"),
    row("Equal pay", "बराबर वेतन",
        "Women and men doing the same work must get the same pay.",
        "एक जैसे काम के लिए औरत और आदमी को बराबर पैसा।"),
    row("Written proof of the job", "काम का लिखित सबूत",
        "In most workplaces the employer must give you an appointment letter with your job, wage and start date, and a wage slip.",
        "ज़्यादातर जगहों पर नियोक्ता को नियुक्ति पत्र और वेतन पर्ची देनी होती है।"),
    row("Free to leave", "छोड़ने की आज़ादी",
        "Nobody can force you to keep working to repay an advance, or keep your documents to stop you leaving. That is bonded labour and it is a crime.",
        "एडवांस चुकाने के लिए ज़बरदस्ती काम करवाना या कागज़ रखकर रोकना बंधुआ मज़दूरी है। यह अपराध है।"),
    row("Safety and injury", "सुरक्षा और चोट",
        "Safety gear such as a helmet, gloves and harness must be given free. If you are hurt at work, the employer is responsible for compensation.",
        "हेलमेट, दस्ताने, बेल्ट मुफ़्त मिलने चाहिए। काम पर चोट लगे तो मुआवज़ा नियोक्ता की ज़िम्मेदारी है।"),
    row("Respect", "इज़्ज़त",
        "Sexual harassment at any workplace, including inside someone's home, can be reported.",
        "किसी भी काम की जगह पर, किसी के घर के अंदर भी, यौन उत्पीड़न की शिकायत हो सकती है।"),
])

rights = f'''
{pagehead("rights", "t-rights", "Your rights at work", "काम पर आपके अधिकार", "Your rights")}
    <p class="lead">These rights come from India's labour codes and apply whether or not you have anything in writing. A verbal deal is still a deal.{hi("ये अधिकार भारत के श्रम कानूनों से आते हैं। लिखित कागज़ न हो तब भी लागू हैं। ज़ुबानी सौदा भी सौदा है।")}</p>
    <p><a href="pictures.html">See the main rights as pictures, with sound</a>{hi("मुख्य अधिकार तस्वीरों में, आवाज़ के साथ")}</p>

    <ul class="jump" aria-label="Jump to your type of work">
      <li><a href="#construction">{I["helmet"]}<span>Construction{hi("निर्माण / बिल्डिंग")}</span></a></li>
      <li><a href="#domestic">{I["house"]}<span>Domestic work{hi("घरेलू काम")}</span></a></li>
      <li><a href="#factory">{I["factory"]}<span>Factory{hi("फ़ैक्ट्री")}</span></a></li>
      <li><a href="#migrant">{I["bus"]}<span>From another state{hi("दूसरे राज्य से")}</span></a></li>
    </ul>

    <div class="panel t-rights">
      <h2>Rights every worker has{hi("हर मज़दूर के अधिकार")}</h2>
      <div class="tablewrap">
        <table>
          <thead><tr><th style="width:28%">Right</th><th>What it means for you</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <p class="muted">Minimum wage amounts change every few months and differ by state and skill level. Ask your district labour office or call 14434 for the current rate.</p>
    </div>

    <div class="panel" id="construction">
      <h2>Construction workers{hi("निर्माण मज़दूर")}</h2>
      <details open>
        <summary>Register with the construction workers welfare board{hi("निर्माण मज़दूर कल्याण बोर्ड में पंजीकरण")}</summary>
        <div>
          <p>Every state has a Building and Other Construction Workers Welfare Board. You can usually register if you are 18 to 60 years old and did construction work for at least 90 days in the last year.{hi("हर राज्य में निर्माण मज़दूर कल्याण बोर्ड है। 18 से 60 साल के और पिछले साल में 90 दिन काम किया हो तो पंजीकरण हो सकता है।")}</p>
          <p>Benefits depend on the state but often include accident help, money for children's education, maternity help, tools and a pension.{hi("फ़ायदे राज्य के हिसाब से हैं: दुर्घटना मदद, बच्चों की पढ़ाई, प्रसव मदद, औज़ार, पेंशन।")}</p>
          <p>Ask at the district labour office. A contractor's certificate or other workers' word is usually enough as proof of 90 days.</p>
        </div>
      </details>
      <details>
        <summary>The contractor ran away or is not paying{hi("ठेकेदार भाग गया या पैसा नहीं दे रहा")}</summary>
        <div>
          <p>The builder or company that hired the contractor is responsible for making sure you get paid. Go to the site office and ask for the main company's name. Then follow the steps on the <a href="wages.html">Not paid</a> page.{hi("जिस बिल्डर या कंपनी ने ठेकेदार रखा, उसकी ज़िम्मेदारी है कि आपको पैसा मिले।")}</p>
        </div>
      </details>
      <details>
        <summary>What the site must have{hi("साइट पर क्या होना चाहिए")}</summary>
        <div>
          <ul>
            <li>Clean drinking water, toilets and first aid{hi("पीने का पानी, शौचालय, प्राथमिक उपचार")}</li>
            <li>Free helmet, shoes, gloves, and a safety harness for work at height{hi("मुफ़्त हेलमेट, जूते, दस्ताने और ऊँचाई पर काम के लिए सेफ़्टी बेल्ट")}</li>
            <li>A place to rest and eat, and a creche on large sites where women work{hi("आराम और खाने की जगह, बड़ी साइट पर बच्चों के लिए पालना घर")}</li>
          </ul>
        </div>
      </details>
      <details>
        <summary>Someone got hurt on site{hi("साइट पर किसी को चोट लगी")}</summary>
        <div>
          <ol>
            <li>Get treatment first. Keep every bill and the hospital paper.{hi("पहले इलाज करवाएँ। हर बिल और अस्पताल का कागज़ संभालकर रखें।")}</li>
            <li>Take photos of the place and write down the site name and address.{hi("जगह की फ़ोटो लें, साइट का नाम और पता लिखें।")}</li>
            <li>Get names and numbers of workers who saw it.{hi("जिन्होंने देखा, उनके नाम और नंबर लें।")}</li>
            <li>Report it to the labour office and call 15100. Do not sign any paper that says you will not claim.{hi("श्रम कार्यालय को बताएँ और 15100 पर फ़ोन करें। ‘दावा नहीं करूँगा’ वाले किसी कागज़ पर साइन न करें।")}</li>
          </ol>
        </div>
      </details>
    </div>

    <div class="panel" id="domestic">
      <h2>Domestic workers{hi("घरेलू कामगार")}</h2>
      <details open>
        <summary>Minimum wage applies to you too{hi("न्यूनतम मज़दूरी आप पर भी लागू है")}</summary>
        <div>
          <p>The Code on Wages covers all workers, including people who cook, clean, look after children or the elderly in homes. Several states also set a separate rate for domestic work.{hi("मज़दूरी संहिता हर कामगार पर लागू है, घर में खाना बनाने, सफ़ाई, बच्चों या बुज़ुर्गों की देखभाल करने वालों पर भी।")}</p>
        </div>
      </details>
      <details>
        <summary>Agree on hours and day off before you start{hi("शुरू करने से पहले घंटे और छुट्टी तय करें")}</summary>
        <div>
          <p>Rules on hours for domestic work are weak in most states, so your own agreement matters most. Fix the hours, the weekly day off, the salary date and paid leave. Use the job card on the <a href="before-job.html">Before a job</a> page.{hi("ज़्यादातर राज्यों में घरेलू काम के घंटों के नियम कमज़ोर हैं, इसलिए पहले ही घंटे, साप्ताहिक छुट्टी और वेतन की तारीख तय करें।")}</p>
        </div>
      </details>
      <details>
        <summary>Register on e-Shram{hi("ई-श्रम पर पंजीकरण करें")}</summary>
        <div>
          <p>Registration is free on eshram.gov.in or by calling 14434. You get a card with a number that links you to government schemes for unorganised workers. Some states also have a welfare board for domestic workers. Ask at the district labour office.{hi("eshram.gov.in पर या 14434 पर फ़ोन करके मुफ़्त पंजीकरण करें। इससे सरकारी योजनाओं से जुड़ते हैं।")}</p>
        </div>
      </details>
      <details>
        <summary>Harassment or abuse in the house{hi("घर में उत्पीड़न या मारपीट")}</summary>
        <div>
          <p>Sexual harassment of a domestic worker can be reported to the Local Committee in your district. You do not have to go to the police first. Call 181 for the women's helpline, or 112 if you are in danger now.{hi("घरेलू कामगार के यौन उत्पीड़न की शिकायत ज़िले की स्थानीय समिति में कर सकती हैं। 181 महिला हेल्पलाइन, खतरा हो तो 112।")}</p>
        </div>
      </details>
      <details>
        <summary>Accused of theft, or salary held back{hi("चोरी का इल्ज़ाम या वेतन रोका गया")}</summary>
        <div>
          <p>An accusation does not give anyone the right to keep your salary. Do not sign or put your thumbprint on any paper you cannot read. Call 15100 for a free lawyer.{hi("इल्ज़ाम लगने से किसी को आपका वेतन रोकने का हक़ नहीं मिलता। जो कागज़ पढ़ नहीं सकते उस पर साइन या अंगूठा न लगाएँ। 15100 पर मुफ़्त वकील।")}</p>
        </div>
      </details>
      <details>
        <summary>Came through a placement agency{hi("एजेंसी के ज़रिए काम मिला")}</summary>
        <div>
          <p>Get the agency's name, address, phone number and fee in writing. Do not let the agency collect your salary for you or keep your documents. Children under 14 cannot be employed in any home. Report it on 1098.{hi("एजेंसी का नाम, पता, नंबर और फ़ीस लिखकर लें। एजेंसी को आपका वेतन या कागज़ न रखने दें। 14 साल से कम उम्र के बच्चे से घरेलू काम करवाना मना है: 1098।")}</p>
        </div>
      </details>
    </div>

    <div class="panel" id="factory">
      <h2>Factory workers{hi("फ़ैक्ट्री मज़दूर")}</h2>
      <details open>
        <summary>PF: check that your money is actually deposited{hi("PF: जाँचें कि पैसा सच में जमा हो रहा है")}</summary>
        <div>
          <p>If the factory has 20 or more workers, PF must be cut from your pay and deposited with EPFO along with the employer's share. If it is cut but not deposited, that is a serious offence.{hi("20 या ज़्यादा मज़दूर हों तो PF कटकर EPFO में जमा होना चाहिए। कटे पर जमा न हो तो यह गंभीर अपराध है।")}</p>
          <p>To check your balance, give a missed call to <a href="tel:9966044425">99660 44425</a> from the phone number linked to your UAN. For help, call EPFO on <a href="tel:1800118005">1800-118-005</a>.</p>
        </div>
      </details>
      <details>
        <summary>ESI card for free treatment{hi("मुफ़्त इलाज के लिए ESI कार्ड")}</summary>
        <div>
          <p>If the factory has 10 or more workers and you earn up to ₹21,000 a month, you should be covered by ESI. That means free treatment for you and your family, and cash help when you are sick or injured.{hi("10 या ज़्यादा मज़दूर हों और आपकी कमाई ₹21,000 महीना तक हो, तो ESI मिलना चाहिए: आपके और परिवार के लिए मुफ़्त इलाज।")}</p>
        </div>
      </details>
      <details>
        <summary>Wage slip, overtime and night shifts{hi("वेतन पर्ची, ओवरटाइम और रात की शिफ़्ट")}</summary>
        <div>
          <ul>
            <li>You should get a wage slip showing days worked, overtime and every cut.{hi("आपको वेतन पर्ची मिलनी चाहिए जिसमें दिन, ओवरटाइम और हर कटौती लिखी हो।")}</li>
            <li>Overtime is paid at double the normal rate.{hi("ओवरटाइम का दोगुना पैसा।")}</li>
            <li>Women can work night shifts only if they agree, and the employer must arrange safety and transport.{hi("महिलाएँ रात की शिफ़्ट सिर्फ़ अपनी मर्ज़ी से करेंगी, और सुरक्षा व आने-जाने का इंतज़ाम नियोक्ता का।")}</li>
          </ul>
        </div>
      </details>
      <details>
        <summary>Hired through a contractor or agency{hi("ठेकेदार या एजेंसी के ज़रिए रखा गया")}</summary>
        <div>
          <p>The factory is still responsible for making sure you get your wages, PF and ESI. Write down the contractor's name and the factory's name.{hi("फ़ैक्ट्री की भी ज़िम्मेदारी है कि आपको वेतन, PF और ESI मिले।")}</p>
        </div>
      </details>
      <details>
        <summary>Leaving after many years{hi("कई साल बाद काम छोड़ना")}</summary>
        <div>
          <p>After 5 years with the same employer you are owed gratuity when you leave. For fixed-term workers it is after 1 year.{hi("एक ही नियोक्ता के यहाँ 5 साल बाद छोड़ने पर ग्रेच्युटी मिलती है। तय अवधि वाले कर्मचारी को 1 साल बाद।")}</p>
        </div>
      </details>
    </div>

    <div class="panel" id="migrant">
      <h2>If you came from another state{hi("अगर आप दूसरे राज्य से आए हैं")}</h2>
      <ul>
        <li><strong>Ration:</strong> your ration card works in any state under One Nation One Ration Card. Ask at any ration shop.{hi("राशन: ‘एक देश एक राशन कार्ड’ से किसी भी राज्य में राशन ले सकते हैं।")}</li>
        <li><strong>e-Shram:</strong> register once and it stays valid wherever you work.{hi("ई-श्रम: एक बार पंजीकरण, हर जगह मान्य।")}</li>
        <li><strong>Travel home:</strong> in many workplaces, workers from other states are owed a yearly travel allowance to visit home.{hi("घर जाने का किराया: कई जगहों पर दूसरे राज्य के मज़दूरों को साल में एक बार घर जाने का किराया मिलता है।")}</li>
        <li><strong>Same rights:</strong> everything on this page applies to you. Being from outside does not reduce your wage.{hi("बराबर अधिकार: बाहर से होने से आपकी मज़दूरी कम नहीं होती।")}</li>
      </ul>
    </div>
'''
page("rights.html", "Your rights at work", rights, "Rights of construction, domestic, factory and migrant workers in India, in plain English and Hindi.", topic="t-rights")
