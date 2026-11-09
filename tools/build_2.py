import sys; sys.path.insert(0, sys.path[0])
from build_common import page, pagehead, login_gate, ICONS as I

def hi(t): return f'<span class="hi" lang="hi">{t}</span>'

# ---------------- WAGES ----------------
log_rows = "\n".join(f"<tr><td>{d}</td><td></td><td></td><td></td><td></td><td></td></tr>" for d in range(1, 32))

wages = f'''
{pagehead("money", "t-wages", "Not paid, or paid less than agreed?", "पैसा नहीं मिला, या तय से कम मिला?", "Not paid?")}
    <p class="lead">You can get your money back even without a written contract. What matters is proof that you worked. Start collecting it today.{hi("लिखित कागज़ न हो तब भी पैसा वापस मिल सकता है। ज़रूरी है काम करने का सबूत। आज से ही इकट्ठा करें।")}</p>

    <div class="warn">
      <strong>Don't wait.</strong> A claim can usually be made up to 3 years later, but co-workers move away and messages get deleted. The sooner you act, the easier it is.
      {hi("देर न करें। दावा आम तौर पर 3 साल तक हो सकता है, पर साथी चले जाते हैं और मैसेज मिट जाते हैं।")}
    </div>

    <div class="panel">
      <h2>Step by step{hi("एक-एक कदम")}</h2>
      <ol class="steps">
        <li>
          <h3>Write it down, starting today{hi("आज से लिखना शुरू करें")}</h3>
          <p>Use the <a href="diary.html">work diary</a> on this site, the printable log further down, or any notebook. Things that count as proof:{hi("इस साइट की ‘काम का हिसाब’ डायरी, नीचे दी गई कॉपी या कोई भी कॉपी इस्तेमाल करें। ये सब सबूत हैं:")}</p>
          <ul>
            <li>Photos of you at the work place. Your phone saves the date automatically.{hi("काम की जगह पर आपकी फ़ोटो। फ़ोन तारीख अपने आप रखता है।")}</li>
            <li>A photo of the attendance register with your name.{hi("हाज़िरी रजिस्टर की फ़ोटो जिसमें आपका नाम हो।")}</li>
            <li>WhatsApp messages, voice notes and call records with the employer.{hi("मालिक के साथ WhatsApp मैसेज, वॉइस नोट, कॉल रिकॉर्ड।")}</li>
            <li>UPI or bank records of any earlier payment.{hi("पहले मिले पैसे की UPI या बैंक एंट्री।")}</li>
            <li>Names and phone numbers of 2 or 3 co-workers.{hi("2-3 साथियों के नाम और नंबर।")}</li>
          </ul>
        </li>
        <li>
          <h3>Ask for the money in writing{hi("पैसा लिखित में माँगें")}</h3>
          <p>Send a message, so there is a record that you asked. Copy this and fill in the blanks. A voice note saying the same thing also works.{hi("मैसेज भेजें ताकि सबूत रहे कि आपने माँगा। नीचे वाला मैसेज भरकर भेजें। वॉइस नोट भी चलेगा।")}</p>
          <div class="sheet">
            <p>Namaste ______ ji. I worked at ______ from ______ to ______, for ______ days at ₹______ per day. The total is ₹______. I have received ₹______. Please pay the remaining ₹______ by ______. &mdash; ______</p>
            <p lang="hi">नमस्ते ______ जी। मैंने ______ पर ______ से ______ तक ______ दिन ₹______ रोज़ पर काम किया। कुल ₹______ बनते हैं। मुझे ₹______ मिल चुके हैं। बाकी ₹______ ______ तक दे दीजिए। &mdash; ______</p>
          </div>
          <p class="muted">Keep the reply, even if it is rude. Don't delete the chat.</p>
        </li>
        <li>
          <h3>Go above the contractor{hi("ठेकेदार से ऊपर जाएँ")}</h3>
          <p>If a contractor hired you, the builder, factory or company that hired the contractor also has to make sure you are paid. Go to their office with your proof, preferably with other workers.{hi("ठेकेदार ने रखा हो तो जिस बिल्डर, फ़ैक्ट्री या कंपनी ने ठेकेदार रखा, उसकी भी ज़िम्मेदारी है। सबूत लेकर, हो सके तो साथियों के साथ, उनके दफ़्तर जाएँ।")}</p>
        </li>
        <li>
          <h3>Complain at the labour office{hi("श्रम कार्यालय में शिकायत करें")}</h3>
          <p>Every district has a labour office, usually near the collectorate. You can write the complaint by hand, in Hindi or your own language. If you can't write, tell the officer and they must write it down for you.{hi("हर ज़िले में श्रम कार्यालय है, अक्सर कलेक्ट्रेट के पास। शिकायत हाथ से, हिंदी या अपनी भाषा में लिख सकते हैं। लिख नहीं सकते तो अधिकारी लिखेगा।")}</p>
          <p><strong>Always ask for a stamped copy or receipt of your complaint.</strong> Some complaints can also be filed online on the SAMADHAN portal, samadhan.labour.gov.in.{hi("शिकायत की मुहर लगी कॉपी या रसीद ज़रूर लें।")}</p>
          <p>If you were paid less than the minimum wage, you can claim the difference too, not just the unpaid amount.{hi("न्यूनतम मज़दूरी से कम मिला हो तो वह फ़र्क भी माँग सकते हैं।")}</p>
        </li>
        <li>
          <h3>Get a free lawyer{hi("मुफ़्त वकील लें")}</h3>
          <p>Workers and women get free legal help from the District Legal Services Authority, which has an office at every district court. Call <a href="tel:15100">15100</a> to be connected.{hi("मज़दूरों और महिलाओं को ज़िला विधिक सेवा प्राधिकरण से मुफ़्त कानूनी मदद मिलती है। हर ज़िला अदालत में दफ़्तर है। 15100 पर फ़ोन करें।")}</p>
        </li>
        <li>
          <h3>Go together{hi("साथ मिलकर जाएँ")}</h3>
          <p>If others were also not paid, complain as a group. One complaint signed by ten workers is much harder to ignore. A local union or workers' group can help you do this.{hi("दूसरों को भी पैसा नहीं मिला तो मिलकर शिकायत करें। दस लोगों की एक शिकायत को टालना मुश्किल है।")}</p>
        </li>
      </ol>
    </div>

    <div class="panel">
      <h2>What to take with you{hi("साथ क्या ले जाएँ")}</h2>
      <ul class="check">
        <li>Your work log or notebook{hi("काम की कॉपी")}</li>
        <li>Your phone with the photos and messages{hi("फ़ोटो और मैसेज वाला फ़ोन")}</li>
        <li>A photocopy of your ID. Keep the original with you{hi("पहचान पत्र की फ़ोटोकॉपी। असली अपने पास रखें")}</li>
        <li>Employer's or contractor's name, phone number and site address{hi("मालिक/ठेकेदार का नाम, नंबर, साइट का पता")}</li>
        <li>Names and numbers of co-workers who will back you up{hi("गवाही देने वाले साथियों के नाम-नंबर")}</li>
      </ul>
    </div>

    <div class="panel">
      <h2>Work log to print or copy{hi("काम का हिसाब: प्रिंट करें या कॉपी में उतारें")}</h2>
      <p class="noprint muted">Only the sheets and steps print. Or copy the columns into a notebook.</p>
      <p class="noprint needs-js"><button type="button" class="btn js-print">Print this log · प्रिंट करें</button></p>
      <div class="sheet">
        <div class="fill">
          <div>Your name {hi("आपका नाम")}</div><div></div>
          <div>Employer / contractor {hi("मालिक / ठेकेदार")}</div><div></div>
          <div>Their phone {hi("उनका फ़ोन")}</div><div></div>
          <div>Work place address {hi("काम की जगह का पता")}</div><div></div>
          <div>Agreed wage {hi("तय मज़दूरी")}</div><div>₹ ________ per day / week / month</div>
          <div>Month {hi("महीना")}</div><div></div>
        </div>
        <div class="tablewrap" style="margin-top:14px">
          <table class="log">
            <thead>
              <tr><th>Date<br><span lang="hi">तारीख</span></th><th>Worked? (✓)<br><span lang="hi">काम किया?</span></th><th>Hours<br><span lang="hi">घंटे</span></th><th>Overtime<br><span lang="hi">ओवरटाइम</span></th><th>Paid ₹<br><span lang="hi">मिला ₹</span></th><th>Note / witness<br><span lang="hi">टिप्पणी / गवाह</span></th></tr>
            </thead>
            <tbody>
{log_rows}
            </tbody>
          </table>
        </div>
      </div>
    </div>
'''
page("wages.html", "Not paid?", wages, "Steps to recover unpaid wages in India, a message template to send your employer, and a printable work log.", topic="t-wages")

# ---------------- BEFORE A JOB ----------------
def q(en, h): return f"<li>{en}{hi(h)}</li>"

before = f'''
{pagehead("job", "t-job", "Before you agree to a job", "काम पकड़ने से पहले", "Before a job")}
    <p class="lead">Most wage problems start with a deal that was never clear. Ten minutes of questions now can save you a month's pay later.{hi("ज़्यादातर झगड़े अधूरी बात से शुरू होते हैं। अभी दस मिनट के सवाल बाद में महीने भर का पैसा बचा सकते हैं।")}</p>

    <div class="panel">
      <h2>Ask these questions{hi("ये सवाल पूछें")}</h2>
      <ul class="check">
        {q("What is your full name, and which company or builder is this for?", "आपका पूरा नाम क्या है, और काम किस कंपनी/बिल्डर का है?")}
        {q("What is your phone number? Call it once in front of them to check it rings.", "आपका फ़ोन नंबर क्या है? सामने ही एक बार मिलाकर देखें।")}
        {q("What is the exact address of the work?", "काम का पूरा पता क्या है?")}
        {q("How much per day or per month? Paid in cash, UPI or bank?", "रोज़ या महीने का कितना? नकद, UPI या बैंक में?")}
        {q("Which day will I be paid? Every day, every week or every month?", "पैसा किस दिन मिलेगा? रोज़, हफ़्ते या महीने?")}
        {q("How many hours a day? Which day is the day off? What is the overtime rate?", "दिन में कितने घंटे? छुट्टी किस दिन? ओवरटाइम का क्या रेट?")}
        {q("Is food or a place to stay included? Is any money cut for it?", "खाना या रहना शामिल है? उसके पैसे कटेंगे?")}
        {q("Who pays for travel to the site and back home?", "आने-जाने का किराया कौन देगा?")}
        {q("Will I get safety gear? Will PF or ESI be given?", "सुरक्षा का सामान मिलेगा? PF या ESI मिलेगा?")}
      </ul>
      <div class="note">
        <strong>Keep a record of the answers.</strong> After the talk, send one message: “As agreed: ₹___ per day, paid every ___, ___ hours, starting ___.” If they reply “ok”, that is proof. You can also record the phone call.
        {hi("बात के बाद एक मैसेज भेजें: “तय हुआ: ₹___ रोज़, हर ___ को भुगतान, ___ घंटे, ___ से शुरू।” जवाब में ‘ok’ आया तो वही सबूत है।")}
      </div>
    </div>

    <div class="panel">
      <h2>Job card: fill it, both sign, take a photo{hi("काम का कार्ड: भरें, दोनों साइन करें, फ़ोटो लें")}</h2>
      <p class="noprint muted">Print this, or copy it onto paper. If the employer refuses to sign something this simple, treat that as a warning sign.</p>
      <p class="noprint needs-js"><button type="button" class="btn js-print">Print the job card · प्रिंट करें</button></p>
      <div class="sheet">
        <h3>Work agreement {hi("काम का समझौता")}</h3>
        <div class="fill">
          <div>Worker name {hi("मज़दूर का नाम")}</div><div></div>
          <div>Employer / contractor name {hi("मालिक / ठेकेदार का नाम")}</div><div></div>
          <div>Employer phone {hi("मालिक का फ़ोन")}</div><div></div>
          <div>Company / builder / house {hi("कंपनी / बिल्डर / घर")}</div><div></div>
          <div>Work address {hi("काम का पता")}</div><div></div>
          <div>Type of work {hi("काम का प्रकार")}</div><div></div>
          <div>Wage {hi("मज़दूरी")}</div><div>₹ ________ per day / week / month</div>
          <div>Pay day {hi("भुगतान का दिन")}</div><div></div>
          <div>Hours and day off {hi("घंटे और छुट्टी")}</div><div></div>
          <div>Overtime rate {hi("ओवरटाइम रेट")}</div><div>₹ ________ per hour</div>
          <div>Food / stay / travel {hi("खाना / रहना / किराया")}</div><div></div>
          <div>Advance given, and how it is repaid {hi("एडवांस और उसकी वापसी")}</div><div></div>
          <div>Start date {hi("शुरू की तारीख")}</div><div></div>
          <div>Worker sign / thumb {hi("मज़दूर साइन / अंगूठा")}</div><div></div>
          <div>Employer sign {hi("मालिक का साइन")}</div><div></div>
        </div>
      </div>
    </div>

    <div class="panel">
      <h2>Warning signs: think twice{hi("खतरे के संकेत: दोबारा सोचें")}</h2>
      <div class="warn">
        <ul style="margin-bottom:0">
          <li>They ask you to pay money to get the job.{hi("काम दिलाने के लिए पैसे माँगें।")}</li>
          <li>They want to keep your Aadhaar, bank card or phone “for safety”.{hi("‘सुरक्षा के लिए’ आपका आधार, बैंक कार्ड या फ़ोन रखना चाहें।")}</li>
          <li>Pay will come “all together at the end of the season”.{hi("‘सीज़न के आखिर में इकट्ठा’ पैसा देने की बात।")}</li>
          <li>A large advance that you must “work off” before you can leave.{hi("बड़ा एडवांस जिसे चुकाए बिना छोड़ नहीं सकते।")}</li>
          <li>They won't give a phone number, a real name or the work address.{hi("फ़ोन नंबर, असली नाम या पता न बताएँ।")}</li>
          <li>You will live somewhere that is locked from outside, or you can't go out.{hi("रहने की जगह बाहर से बंद हो या बाहर जाने न दें।")}</li>
          <li>They ask you to sign or thumbprint a paper you can't read, or a blank paper.{hi("बिना पढ़े या खाली कागज़ पर साइन/अंगूठा लगवाएँ।")}</li>
        </ul>
      </div>
      <p>If you are already in this situation and can't leave, call <a href="tel:112">112</a>. Being held to repay a debt is bonded labour and the police must act.{hi("अगर आप ऐसी हालत में फँसे हैं, 112 पर फ़ोन करें। कर्ज़ के लिए रोकना बंधुआ मज़दूरी है।")}</p>
    </div>

    <div class="split">
      <div class="panel">
        <h2>Before you leave home{hi("घर से निकलने से पहले")}</h2>
        <ul class="check">
          <li>Give your family the work address and the employer's number.{hi("परिवार को काम का पता और मालिक का नंबर दें।")}</li>
          <li>Send them a photo of the job card and of the contractor.{hi("उन्हें काम के कार्ड और ठेकेदार की फ़ोटो भेजें।")}</li>
          <li>If travelling in a hired vehicle, send them its number plate.{hi("गाड़ी से जा रहे हों तो उसका नंबर भेजें।")}</li>
          <li>Carry photocopies of documents. Leave originals at home.{hi("कागज़ों की फ़ोटोकॉपी ले जाएँ, असली घर पर।")}</li>
          <li>Save 112 and 15100 in your phone.{hi("फ़ोन में 112 और 15100 सेव करें।")}</li>
          <li>Register on e-Shram if you haven't. Call 14434.{hi("ई-श्रम पर पंजीकरण नहीं है तो करें: 14434।")}</li>
        </ul>
      </div>
      <div class="panel">
        <h2>Ask people who worked there{hi("पहले काम कर चुके लोगों से पूछें")}</h2>
        <p>The best check on an employer is someone who worked for them. Ask at the labour chowk, in your village group, or at a local union.{hi("मालिक के बारे में सबसे सही जानकारी उनसे मिलेगी जिन्होंने वहाँ काम किया। लेबर चौक, गाँव के ग्रुप या यूनियन में पूछें।")}</p>
        <ul>
          <li>Did you get paid on time, and the full amount?{hi("पैसा समय पर और पूरा मिला?")}</li>
          <li>Were there any cuts you didn't expect?{hi("कोई अचानक कटौती हुई?")}</li>
          <li>Could you leave when you wanted to?{hi("जब चाहा तब छोड़ पाए?")}</li>
        </ul>
      </div>
    </div>

    <div class="panel t-job" id="notebook">
      <h2>Contractor notebook{hi("ठेकेदार की डायरी")}</h2>
      <p>Save what you learn about a contractor: did they pay properly or not? Search it later, and send a warning to your WhatsApp group in one tap. Saved only on this phone.{hi("ठेकेदार के बारे में लिखकर रखें: पैसा ठीक दिया या नहीं। बाद में ढूँढें, और एक बटन से WhatsApp ग्रुप में भेजें। सिर्फ़ इसी फ़ोन में रहता है।")}</p>
      <p class="no-js muted">This notebook needs a newer phone browser. Write the same details in a notebook instead.</p>

      {login_gate("before-job.html#notebook", panel=False)}
      <div class="needs-js noread" data-private>
        <div class="diary-top">
          <div class="field">{I["people"]}<label for="nb-name">Contractor name{hi("ठेकेदार का नाम")}</label><input id="nb-name" type="text" autocomplete="off"></div>
          <div class="field">{I["phone"]}<label for="nb-phone">Phone number{hi("फ़ोन नंबर")}</label><input id="nb-phone" type="tel" inputmode="tel" autocomplete="off"></div>
          <div class="field">{I["house"]}<label for="nb-place">Work place or area{hi("काम की जगह या इलाका")}</label><input id="nb-place" type="text" autocomplete="off"></div>
          <div class="field">{I["slip"]}<label for="nb-note">Short note{hi("छोटी टिप्पणी")}</label><input id="nb-note" type="text" autocomplete="off"></div>
        </div>

        <p class="pay-q"><strong>Did they pay properly?</strong>{hi("क्या उन्होंने पैसा ठीक से दिया?")}</p>
        <div class="verdicts" role="radiogroup" aria-label="Did they pay properly?">
          <button type="button" class="verdict good" data-v="good" role="radio" aria-checked="false">{I["thumbup"]}<span>Paid fully, on time{hi("पूरा, समय पर")}</span></button>
          <button type="button" class="verdict mid" data-v="late" role="radio" aria-checked="false">{I["clock8"]}<span>Paid late or less{hi("देर से या कम")}</span></button>
          <button type="button" class="verdict bad" data-v="bad" role="radio" aria-checked="false">{I["thumbdown"]}<span>Did not pay{hi("पैसा नहीं दिया")}</span></button>
        </div>
        <button type="button" class="btn dark" id="nb-save" style="margin-top:12px">Save · सेव करें</button>

        <h3>Search your notes{hi("अपनी डायरी में ढूँढें")}</h3>
        <div class="field" style="margin-bottom:10px">{I["people"]}<label for="nb-search">Name, phone or place{hi("नाम, फ़ोन या जगह")}</label><input id="nb-search" type="search" autocomplete="off"></div>
        <ul class="nblist" id="nb-list" aria-live="polite"></ul>
      </div>
    </div>
'''
page("before-job.html", "Before a job", before, "Questions to ask an employer, a printable job agreement card, and warning signs of wage theft and bonded labour.", topic="t-job")

# ---------------- HELP ----------------
def h_row(need, need_hi, num, tel, note):
    sp = " ".join(tel)
    say_hi = f"{need_hi}: {sp} पर फ़ोन करें।"
    say_en = f"{need}: call {sp}. {note}."
    return f'<tr data-say-hi="{say_hi}" data-say-en="{say_en}"><td>{need}{hi(need_hi)}</td><td><a class="callbtn slim" href="tel:{tel}">{num}</a></td><td class="muted">{note}</td></tr>'

help_rows = "\n".join([
    h_row("In danger now, locked in, beaten, or forced to work", "अभी खतरे में, बंद, मारपीट या ज़बरदस्ती काम", "112", "112", "Police, ambulance, fire. 24 hours"),
    h_row("Unpaid wages, injury, any work problem: free lawyer", "पैसा न मिलना, चोट, कोई भी काम की समस्या: मुफ़्त वकील", "15100", "15100", "National legal aid helpline (NALSA)"),
    h_row("e-Shram card, schemes for unorganised workers", "ई-श्रम कार्ड, असंगठित मज़दूरों की योजनाएँ", "14434", "14434", "Ministry of Labour"),
    h_row("Woman facing harassment or violence", "महिला के साथ उत्पीड़न या हिंसा", "181", "181", "Women's helpline. 24 hours"),
    h_row("A child is working or in danger", "कोई बच्चा काम कर रहा है या खतरे में है", "1098", "1098", "Childline. 24 hours"),
    h_row("PF not deposited, PF withdrawal", "PF जमा नहीं हुआ, PF निकालना", "1800-118-005", "1800118005", "EPFO, toll free"),
    h_row("ESI card or ESI hospital", "ESI कार्ड या ESI अस्पताल", "1800-11-2526", "1800112526", "ESIC, toll free"),
])

helpp = f'''
{pagehead("phone", "t-help", "Get help", "मदद लें", "Get help")}

    <div class="callbox danger">
      <p><strong>In danger right now?</strong>{hi("अभी खतरे में हैं?")} If you are locked in, hurt, or someone is stopping you from leaving.</p>
      <a class="callbtn red" href="tel:112">{I["alert"]}<span>Call 112<small>Emergency · आपातकाल</small></span></a>
    </div>

    <div class="panel">
      <h2>Free helplines{hi("मुफ़्त हेल्पलाइन")}</h2>
      <p class="muted">Tap a number to call. All of these are free.</p>
      <div class="tablewrap">
        <table>
          <thead><tr><th>If you need help with</th><th style="width:150px">Call</th><th style="width:28%">Who answers</th></tr></thead>
          <tbody>
{help_rows}
          </tbody>
        </table>
      </div>
    </div>

    <div class="panel">
      <h2>What to say when you call{hi("फ़ोन पर क्या बोलें")}</h2>
      <p>You don't need to explain everything perfectly. Say these five things and they will ask the rest.{hi("सब कुछ ठीक से समझाने की ज़रूरत नहीं। ये पाँच बातें बोलें, बाकी वो पूछ लेंगे।")}</p>
      <div class="sheet">
        <ol style="margin:0">
          <li>My name is ______. I work as a ______.{hi("मेरा नाम ______ है। मैं ______ का काम करता/करती हूँ।")}</li>
          <li>I work at ______ (place, district).{hi("मैं ______ (जगह, ज़िला) में काम करता/करती हूँ।")}</li>
          <li>My problem is ______.{hi("मेरी समस्या ______ है।")}</li>
          <li>It started on ______.{hi("यह ______ से शुरू हुआ।")}</li>
          <li>I want ______ (my wages, to leave safely, treatment...).{hi("मुझे ______ चाहिए (मेरा पैसा, सुरक्षित निकलना, इलाज...)।")}</li>
        </ol>
      </div>
      <p class="muted">Ask for your language at the start. Write down the name of the person you spoke to and any complaint number they give.</p>
    </div>

    <div class="panel">
      <h2>Where to go in person{hi("कहाँ जाएँ")}</h2>
      <div class="tablewrap">
        <table>
          <thead><tr><th style="width:32%">Office</th><th>Go here for</th></tr></thead>
          <tbody>
            <tr><td><strong>District labour office</strong>{hi("ज़िला श्रम कार्यालय")}</td><td>Unpaid or low wages, no wage slip, PF problems, welfare board registration. Usually near the collectorate.{hi("पैसा न मिलना या कम मिलना, PF, कल्याण बोर्ड पंजीकरण।")}</td></tr>
            <tr><td><strong>Legal services office at the district court</strong>{hi("ज़िला अदालत में विधिक सेवा कार्यालय")}</td><td>A free lawyer and help writing your complaint. Para-legal volunteers there can also visit your area.{hi("मुफ़्त वकील और शिकायत लिखने में मदद।")}</td></tr>
            <tr><td><strong>Police station</strong>{hi("पुलिस थाना")}</td><td>Violence, threats, documents taken, being held to repay a debt. They must register your complaint.{hi("मारपीट, धमकी, कागज़ छीनना, कर्ज़ के लिए रोकना।")}</td></tr>
            <tr><td><strong>Local Committee, district office</strong>{hi("स्थानीय समिति, ज़िला कार्यालय")}</td><td>Sexual harassment at work, including domestic workers in private homes.{hi("काम पर यौन उत्पीड़न, घरों में काम करने वाली महिलाओं के लिए भी।")}</td></tr>
            <tr><td><strong>Common Service Centre</strong>{hi("कॉमन सर्विस सेंटर (CSC)")}</td><td>e-Shram registration and printing your card, if you don't have a smartphone.{hi("ई-श्रम पंजीकरण और कार्ड प्रिंट।")}</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="panel t-help">
      <h2>If you can't read or write{hi("अगर आप पढ़-लिख नहीं सकते")}</h2>
      <ul>
        <li>You can make a complaint by speaking. The officer or legal aid volunteer will write it for you.{hi("आप बोलकर शिकायत कर सकते हैं। अधिकारी या वॉलंटियर लिखेंगे।")}</li>
        <li>Ask them to read it back to you before you sign or give your thumbprint.{hi("साइन या अंगूठा लगाने से पहले पढ़कर सुनाने को कहें।")}</li>
        <li><strong>Never put your thumbprint on a blank paper.</strong>{hi("खाली कागज़ पर कभी अंगूठा न लगाएँ।")}</li>
        <li>Take a trusted person with you. You are allowed to.{hi("किसी भरोसेमंद इंसान को साथ ले जा सकते हैं।")}</li>
        <li>Open <a href="show.html">Show this screen</a> on your phone and hand it to the officer. It tells them in writing what you need.{hi("फ़ोन पर ‘यह स्क्रीन दिखाएँ’ खोलकर अधिकारी को दें। उसमें लिखा है कि आपको क्या चाहिए।")}</li>
      </ul>
    </div>
'''
page("help.html", "Get help", helpp, "Free helplines and offices for workers in India: legal aid 15100, e-Shram 14434, emergency 112, women 181, child 1098.", topic="t-help")
