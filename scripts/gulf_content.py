"""Content for the Gulf residents section. Edit the text here, then run scripts/build_gulf.py.

Placeholders in body text:
  {{pt trv AE}}     live IRCC processing time (visa type, country code)
  {{updated}}       date IRCC last updated its times
  {{times_all}}     table of all six Gulf countries
  {{times_AE}} etc. table for one country
  {{guides}}        cards for the six UAE guides
  {{countries}}     cards for the five country pages
"""
import re

DATE = "2026-10-30"
GULF_CODES = ["AE", "SA", "QA", "KW", "OM", "BH"]
COUNTRY_NAMES = {"AE": "United Arab Emirates", "SA": "Saudi Arabia", "QA": "Qatar", "KW": "Kuwait", "OM": "Oman", "BH": "Bahrain"}

# Verified sources (fetched October 30, 2026)
S_ENTRY = ("IRCC: Entry requirements by country", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/entry-requirements-country.html")
S_ELIG = ("IRCC: Visitor visa, who can apply", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/eligibility.html")
S_TRV = ("IRCC: Visitor visa", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/visitor-visa.html")
S_VAC = ("IRCC: Find a visa application centre", "https://www.canada.ca/visa-application-centre")
S_ETA13 = ("IRCC: eTA expanded to 13 more countries, including the Philippines", "https://www.canada.ca/en/immigration-refugees-citizenship/news/2023/06/eligible-travellers-from-13-more-countries-now-qualify-for-an-electronic-travel-authorization.html")
S_SUPER = ("IRCC: Super visa, who can apply", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/parent-grandparent-super-visa/eligibility.htm")
S_SUPER_FEES = ("IRCC: Super visa application and fees", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/parent-grandparent-super-visa/apply/paper-application.html")
S_SUPER_INC = ("CIC News: Super Visa income rules eased from March 31, 2026", "https://www.cicnews.com/2026/03/canada-eases-income-requirement-for-hosting-parents-and-grandparents-on-super-visa-0373315.html")
S_BIZ = ("IRCC: Business visitors attending meetings, events and conferences", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/business/visitors-events-conferences.html")
S_REPS = ("IRCC: Who can act as a representative", "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/operational-bulletins-manuals/service-delivery/use-representatives/who-act.html")
S_LAWSOC = ("IRCC: Authorized representatives and law societies", "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigration-citizenship-representative/choose/authorized.html")
S_CICC = ("CICC public register of licensed consultants", "https://register.college-ic.ca/")
S_CICC_FIND = ("CICC: Find an immigration consultant", "https://college-ic.ca/protecting-the-public/find-an-immigration-consultant")
S_KT = ("Khaleej Times: The rise of immigration scams in the UAE (2024)", "https://www.khaleejtimes.com/long-reads/rise-of-immigration-scams-in-uae-how-expat-dreams-turned-to-nightmares?amp=1")
S_TRACKER = ("My Canada visa wait-times tracker", "https://kevinthibbles.com/tracker/")

R_HUB = ("/gulf/", "All guides for Gulf residents")
R_UAE = ("/gulf/canada-visitor-visa-uae-residents.html", "Canada visitor visa for UAE residents")
R_REF = ("/gulf/canada-visa-refused-uae-resident.html", "Refused while living in the UAE")
R_RES = ("/gulf/uae-residence-visa-canada-visa.html", "How your UAE residence visa affects the decision")
R_SUP = ("/gulf/super-visa-parents-gulf.html", "Super Visa for parents living in the Gulf")
R_BIZ = ("/gulf/canada-business-visitor-dubai.html", "Visiting Canada on business from Dubai")
R_VER = ("/gulf/verify-canadian-immigration-consultant-uae.html", "How to check a consultant is licensed")
R_GCMS = ("/gcms-notes.html", "GCMS notes explained")
R_TRACK = ("/tracker/", "Check visa wait times")

T_GULF = ("gulf-residents", "Gulf residents")
T_UAE = ("uae", "UAE")
T_TRV = ("visitor-visas", "Visitor visas")
T_REF = ("visa-refusals", "Visa refusals")

WHO_TABLE = '''    <div class="who">
      <table>
        <thead><tr><th>Your passport</th><th>What you need to fly to Canada</th></tr></thead>
        <tbody>
          <tr><td>United Arab Emirates, Qatar</td><td>An eTA (electronic travel authorization), not a visitor visa</td></tr>
          <tr><td>Philippines</td><td>A visitor visa, <span class="yes">or an eTA</span> if you've held a Canadian visa in the last 10 years or hold a valid U.S. non-immigrant visa, and you're flying</td></tr>
          <tr><td>India, Pakistan, Bangladesh, Sri Lanka, Nepal</td><td>A visitor visa</td></tr>
          <tr><td>Egypt, Jordan, Lebanon</td><td>A visitor visa</td></tr>
          <tr><td>Saudi Arabia, Kuwait, Oman, Bahrain</td><td>A visitor visa</td></tr>
        </tbody>
      </table>
    </div>
    <p class="live-note">Based on IRCC's entry requirements by country, checked October 30, 2026. Always confirm with IRCC's own tool before you apply.</p>'''

PAGES = []

# ─────────────────────────────── HUB ───────────────────────────────
PAGES.append(dict(
    slug="index", crumb="Gulf residents", date=DATE, read=6,
    title="Canadian Visas for Gulf Residents | Kevin Thibbles, RCIC",
    headline="Canadian visas for Gulf residents",
    desc="Visitor visas, Super Visas, business trips and refusals for residents of the UAE, Saudi Arabia, Qatar, Kuwait, Oman and Bahrain, from an RCIC who lived in Dubai.",
    keywords="Canada visa UAE residents, Canada visa from Dubai, Canada visitor visa Gulf, Canada visa Saudi Arabia residents, Canada visa Qatar residents, Canada visa Kuwait residents, Canada visa Oman residents, Canada visa Bahrain residents, RCIC Dubai",
    h1="Canadian visas for people living in the Gulf",
    lede="I lived in Dubai for 11 years before I immigrated to Canada. These guides are for the millions of people who call the Gulf home but hold another country's passport, and who want to visit, do business, or bring family to Canada.",
    kicker="Gulf residents", card_title="Canadian visas for Gulf residents",
    summary="The hub for my Gulf guides: who needs a visa, live processing times for all six Gulf countries, and where to start.",
    og_kicker="Gulf residents · Canada", og_title="Canadian visas for people living in the Gulf",
    tags=[T_GULF, T_UAE, ("saudi-arabia", "Saudi Arabia"), ("qatar", "Qatar"), ("kuwait", "Kuwait"), ("oman", "Oman"), ("bahrain", "Bahrain")],
    body='''    <h2>Why living in the Gulf changes your application</h2>
    <p>Most Canadian visa advice is written for people applying from their home country. If you live in Dubai, Riyadh or Doha on a residence permit, your situation is different. Your job, your home and often your family are in one country, while your passport, your property and your long-term plans may be in another.</p>
    <p>A Canadian visa officer looks at all of it to decide one thing: whether you will go home at the end of your visit. For a Gulf resident, "home" has two meanings, and a strong application explains both. That is what these guides are about.</p>

    <h2>Start here</h2>
    {{guides}}

    <h2>Processing times from each Gulf country</h2>
    <p>IRCC publishes processing times by the country you apply from, not by your passport. A Filipino nurse in Kuwait and a Filipino engineer in Dubai can wait very different lengths of time.</p>
    {{times_all}}

    <h2>Guides for each Gulf country</h2>
    <p>The UAE guides apply across the region, but each country has its own residence documents and its own published times.</p>
    {{countries}}

    <div class="callout">
      <span class="mono-label">Why work with a licensed consultant</span>
      <p>Anyone who charges you for Canadian immigration advice must be licensed in Canada, wherever they are based. I'm a Regulated Canadian Immigration Consultant, registration R713044, and you can check my licence on the CICC public register in under a minute. <a href="/gulf/verify-canadian-immigration-consultant-uae.html" style="color:var(--maple)">Here's how</a>.</p>
    </div>
''',
    related=[R_UAE, R_TRACK, R_GCMS, ("/insights/", "All insights")],
    sources=[S_ENTRY, S_TRV, S_TRACKER],
))

# ─────────────────────────────── PILLAR ───────────────────────────────
PAGES.append(dict(
    slug="canada-visitor-visa-uae-residents", group="guide", crumb="Visitor visa for UAE residents", date=DATE, read=11,
    title="Canada Visitor Visa for UAE Residents (2026 Guide) | RCIC",
    headline="Canada visitor visa for UAE residents: a guide from an RCIC who lived in Dubai",
    desc="Applying for a Canadian visitor visa while living in the UAE: visa or eTA, the documents that matter, fees, biometrics and live processing times.",
    keywords="Canada visitor visa UAE residents, Canada visit visa from Dubai, Canada tourist visa UAE, Canada visa Abu Dhabi, Canada visa Indian in UAE, Canada visa Filipino in UAE, Canada visa Pakistani in UAE, Canada eTA UAE",
    h1="Canada visitor visa for UAE residents",
    lede="I lived in Dubai for 11 years before moving to Canada, so I know how a UAE residence visa, an employer letter and a Dubai bank account look from both sides of the application. This is the guide I wish my friends there had.",
    kicker="Start here", card_title="Canada visitor visa for UAE residents",
    summary="Who needs a visa or an eTA, the documents that matter for UAE residents, fees, biometrics and live processing times.",
    og_kicker="Gulf residents · UAE", og_title="Canada visitor visa for UAE residents",
    tags=[T_GULF, T_UAE, T_TRV],
    body='''    <h2>First, check what your passport needs</h2>
    <p>Whether you need a visitor visa depends on your <strong>passport</strong>, not on where you live. Your UAE residence visa doesn't change it. Here is how it works for the nationalities I met most often in the UAE:</p>
''' + WHO_TABLE + '''
    <p>If you only need an eTA, the process is short and online. The rest of this guide is for everyone who needs a visitor visa, which is most UAE residents.</p>

    <h2>What the officer is deciding</h2>
    <p>IRCC lists the basic requirements: a valid passport, good health, no criminal or immigration-related convictions, enough money for your stay, ties that will take you home, and convincing the officer you'll leave Canada at the end of your visit. You may also need a medical exam or a letter of invitation from someone living in Canada.</p>
    <p>For UAE residents, most visitor visa refusals come back to the same question: <strong>will this person leave Canada on time?</strong> The officer can't ask you in person, so your documents have to answer it.</p>

    <h2>How ties work when you live in the UAE</h2>
    <p>Your ties are split between two places, and both count.</p>
    <ul>
      <li><strong>Your life in the UAE.</strong> A steady job, a residence visa that stays valid well beyond your trip, a home lease, children in school, years of continuous residence.</li>
      <li><strong>Your home country.</strong> Property, family, investments, or a clear plan to return there eventually.</li>
      <li><strong>Your money.</strong> Savings that match your income and your plans, rather than a sudden large deposit with no explanation.</li>
      <li><strong>Your travel history.</strong> Previous trips to Canada, the U.S., the U.K., Europe or elsewhere where you returned on time.</li>
    </ul>
    <p>I explain how officers read a Gulf residence permit in more detail in <a href="/gulf/uae-residence-visa-canada-visa.html" style="color:var(--maple)">How your UAE residence visa affects the officer's decision</a>.</p>

    <h2>Documents that carry weight for UAE residents</h2>
    <ul class="checklist">
      <li>Your passport and your <strong>UAE residence visa and Emirates ID</strong>, valid for the whole trip and ideally well beyond it.</li>
      <li>An <strong>employer letter</strong> on company letterhead: your role, salary, start date, approved leave dates, and that your job continues when you return. A <strong>salary certificate</strong> helps.</li>
      <li><strong>Bank statements</strong> from your UAE account showing salary credits and savings over several months.</li>
      <li>Your <strong>tenancy contract</strong> (in Dubai, the Ejari registration), or proof of the home you own.</li>
      <li>Evidence of ties at home: property papers, family details, investments.</li>
      <li>A clear <strong>travel plan</strong>, and an invitation letter if you're staying with family or friends in Canada.</li>
      <li>Copies of previous visas and entry stamps.</li>
    </ul>
    <div class="callout">
      <span class="mono-label">A common mistake</span>
      <p>Applying with a residence visa that expires during or soon after the trip. If you're renewing, consider waiting for the new visa before you apply, or explain the renewal clearly with evidence.</p>
    </div>

    <h2>Fees, biometrics and where to apply</h2>
    <ul>
      <li>You apply <strong>online</strong> through your IRCC account.</li>
      <li>The visitor visa fee starts at <strong>CAD $100</strong>. Most applicants also give <strong>biometrics</strong> (fingerprints and a photo) for <strong>CAD $85</strong>.</li>
      <li>Biometrics are taken at a Canada Visa Application Centre run by VFS Global. Use IRCC's visa application centre finder for the current UAE locations.</li>
    </ul>

    <h2>How long it takes from the UAE</h2>
    <p>IRCC's current estimate for visitor visas applied for from the UAE is {{pt trv AE}}, updated {{updated}}. That doesn't include the time to give biometrics, so plan for longer.</p>
    {{times_AE}}

    <h2>Mistakes I see most often</h2>
    <ul>
      <li>Leaving the purpose of the trip vague. "Tourism" alone tells the officer very little.</li>
      <li>Large, unexplained deposits shortly before applying.</li>
      <li>Leaving out a previous refusal from any country. Always disclose it. Hiding it can lead to a finding of misrepresentation, which is far more serious than a refusal.</li>
      <li>Reapplying quickly with the same documents after a refusal. See <a href="/gulf/canada-visa-refused-uae-resident.html" style="color:var(--maple)">Refused while living in the UAE</a>.</li>
    </ul>
''',
    faq=[
        ("Can I apply for a Canadian visitor visa from the UAE if I'm not an Emirati citizen?",
         "Yes. Many people apply from the UAE on a residence visa. The officer will look at your status and life in the UAE as well as your ties to your home country, so include your residence visa, Emirates ID and evidence of your job and home there."),
        ("Do Emirati citizens need a visa for Canada?",
         "No. UAE citizens need an electronic travel authorization (eTA) to fly to Canada, not a visitor visa, according to IRCC's entry requirements by country."),
        ("How much does a Canadian visitor visa cost from the UAE?",
         "The visitor visa fee starts at CAD $100, and most applicants also pay CAD $85 for biometrics. The visa application centre may charge its own service fees."),
        ("How long does a Canadian visitor visa take from the UAE?",
         "IRCC publishes a processing time for applications from the UAE that changes over time. My wait-times tracker shows the latest figure, and this page updates automatically. Biometrics time is extra."),
        ("I'm Filipino and live in Dubai. Can I get an eTA instead?",
         "Possibly. Filipino citizens can apply for an eTA instead of a visa when flying to Canada if they've held a Canadian visa in the last 10 years or currently hold a valid U.S. non-immigrant visa. Otherwise a visitor visa is needed."),
    ],
    related=[R_REF, R_RES, R_SUP, R_BIZ, R_HUB],
    sources=[S_ENTRY, S_ELIG, S_TRV, S_VAC, S_ETA13, S_TRACKER],
))

# ─────────────────────────────── REFUSED ───────────────────────────────
PAGES.append(dict(
    slug="canada-visa-refused-uae-resident", group="guide", crumb="Refused while living in the UAE", date=DATE, read=8,
    title="Canada Visa Refused While Living in the UAE? What To Do",
    headline="Canada visa refused while living in the UAE: what to do next",
    desc="Refused a Canadian visitor visa while living in Dubai or Abu Dhabi? How to read the letter, when to order GCMS notes, and how to reapply stronger.",
    keywords="Canada visa refused UAE, Canada visa rejected Dubai, Canada visitor visa refusal UAE resident, 179(b) refusal UAE, reapply Canada visa from Dubai",
    h1="Refused while living in the UAE",
    lede="A refusal is not a ban, and it is not the end. But reapplying with the same documents usually gets the same answer. Here is how I approach a refusal for clients living in the UAE.",
    kicker="Refusals", card_title="Refused while living in the UAE",
    summary="How to read the refusal letter, when GCMS notes are worth ordering, and how to build a stronger reapplication.",
    og_kicker="Gulf residents · Refusals", og_title="Canada visa refused while living in the UAE",
    tags=[T_GULF, T_UAE, T_REF, T_TRV],
    body='''    <h2>Read the letter carefully</h2>
    <p>Your refusal letter lists the reasons the officer was not satisfied. For visitor visas, they usually come back to the same few areas: whether you'll leave Canada at the end of your stay, your ties outside Canada, the purpose of your visit, and your finances.</p>
    <p>For people living in the UAE, a "ties" reason often means the officer didn't see a clear picture of <strong>both</strong> your life in the UAE and your connection to your home country. A strong job in Dubai doesn't help much if the file doesn't show it.</p>

    <h2>Order your GCMS notes when the letter isn't clear</h2>
    <p>The letter shows which boxes were ticked. The officer's notes in IRCC's Global Case Management System (GCMS) often show what they were actually thinking: a document they doubted, an answer that didn't match, or something missing. If your refusal surprised you, the notes are usually worth ordering before you reapply. I explain them in <a href="/gcms-notes.html" style="color:var(--maple)">GCMS notes explained</a>.</p>

    <h2>Your options</h2>
    <ul>
      <li><strong>Reapply with a stronger application.</strong> This is the right choice for most visitor visa refusals. There is no mandatory waiting period, but you should only reapply once something has genuinely changed or you can now show what was missing.</li>
      <li><strong>Challenge the decision in Federal Court.</strong> If the decision was unreasonable, judicial review is possible within strict deadlines. This is legal work: I'll refer you to an immigration lawyer if it's the better route.</li>
      <li><strong>Wait and strengthen your profile.</strong> Sometimes the honest answer is that a few more months of savings, travel or residence history will make the difference.</li>
    </ul>

    <h2>What a stronger UAE reapplication usually includes</h2>
    <ul class="checklist">
      <li>A short, clear <strong>letter of explanation</strong> that addresses each refusal reason directly.</li>
      <li>An updated <strong>employer letter</strong> confirming your role, salary, approved leave and that your position continues.</li>
      <li><strong>Bank statements</strong> that tell a consistent story, with any large deposits explained.</li>
      <li>A <strong>residence visa</strong> with plenty of validity left.</li>
      <li>Stronger <strong>home-country ties</strong>: property, family responsibilities, business or investments.</li>
      <li>A specific <strong>trip plan</strong> that matches your leave dates and budget.</li>
      <li>Full disclosure of the previous refusal. Every new application must declare it.</li>
    </ul>

    <div class="callout">
      <span class="mono-label">Second or third refusal?</span>
      <p>Each refusal stays on your record, and repeating the same application can make the next decision harder. If you've been refused more than once, get the GCMS notes and a professional review before you spend another fee.</p>
    </div>

    <h2>Current processing times from the UAE</h2>
    <p>A visitor visa applied for from the UAE currently takes about {{pt trv AE}}, according to IRCC's latest published estimate ({{updated}}).</p>
''',
    faq=[
        ("How long should I wait to reapply after a Canadian visa refusal?",
         "There is no mandatory waiting period for a visitor visa. What matters is whether your new application answers the reasons for refusal. Reapplying quickly with the same documents usually leads to the same result."),
        ("Do I have to declare a previous refusal when I reapply?",
         "Yes. You must declare every previous refusal, from Canada or any other country. Not declaring it can be treated as misrepresentation, which can lead to a five-year bar from applying."),
        ("Should I order GCMS notes after a refusal from the UAE?",
         "If the refusal letter is generic or the refusal surprised you, usually yes. The notes often show the officer's specific concern, which tells you what the next application must fix."),
        ("Can I appeal a Canadian visitor visa refusal?",
         "There is no appeal for a visitor visa refusal. The legal route is judicial review in the Federal Court of Canada, which has strict deadlines and requires a lawyer. For most people, a stronger new application is the better option."),
    ],
    related=[R_GCMS, R_UAE, R_RES, ("/visitor-visa-refused.html", "Visitor visa refused: what it means"), R_HUB],
    sources=[S_ELIG, S_TRV, S_TRACKER],
    cta_title="Refused from the UAE? Let's look at it together.",
    cta_text="Send me your refusal letter and a short summary. I'll give you an honest read on whether to reapply now, wait, or change your approach.",
))

# ─────────────────────────────── RESIDENCE ───────────────────────────────
PAGES.append(dict(
    slug="uae-residence-visa-canada-visa", group="guide", crumb="UAE residence visa and your application", date=DATE, read=7,
    title="How Your UAE Residence Visa Affects a Canada Visa Decision",
    headline="How your UAE residence visa affects the Canadian visa officer's decision",
    desc="How a Canadian visa officer weighs your UAE residence visa, employer, family and home-country ties, and how to show both sides of your life clearly.",
    keywords="UAE residence visa Canada visa, Canada visa ties UAE resident, Emirates ID Canada visa application, golden visa Canada visitor visa, expat ties Canada visa officer",
    h1="How your UAE residence visa affects the officer's decision",
    lede="Your residence visa is one of the most important documents in your application, and one of the most misunderstood. Here is how I think about it, from 11 years of living on one.",
    kicker="Ties and status", card_title="How your UAE residence visa affects the decision",
    summary="How officers weigh Gulf residence, employer sponsorship and home-country ties, and how to show both sides of your life clearly.",
    og_kicker="Gulf residents · UAE", og_title="How your UAE residence visa affects a Canada visa decision",
    tags=[T_GULF, T_UAE, T_TRV],
    body='''    <h2>Two homes, one question</h2>
    <p>A Canadian visitor visa officer must be satisfied that you'll leave Canada at the end of your visit. IRCC describes this as having ties to your home country, such as a job, a home, financial assets or family. When you live in the UAE, those ties are usually split between the UAE and your country of citizenship, and a good application shows both.</p>

    <h2>What your residence status says about you</h2>
    <p>Most UAE residence visas are linked to an employer or a family sponsor and must be renewed. That's normal, and officers understand it. What matters is the story your documents tell together:</p>
    <ul>
      <li><strong>How long you've lived there.</strong> Several years of continuous residence shows a settled life you're likely to return to.</li>
      <li><strong>How much validity is left.</strong> A visa that expires soon after your trip raises an obvious question: where will you go when you leave Canada?</li>
      <li><strong>Who sponsors it.</strong> An established employer, your own company, or a family sponsor each tells a different story. Make sure the supporting letters match.</li>
      <li><strong>Longer-term residence.</strong> If you hold a longer-term residence permit, such as a UAE Golden Visa, include it. A longer commitment to the UAE can support your case, though it doesn't decide it on its own.</li>
    </ul>

    <h2>The home-country side</h2>
    <p>Many people in the Gulf plan to return home one day: to a house they're building, to parents they support, or to retire. Those plans are real ties, but they only count if the officer can see them. Property records, proof of regular money sent home, family responsibilities and business interests all help.</p>

    <h2>When the two sides don't line up</h2>
    <ul>
      <li><strong>Between jobs or on a visit visa in the UAE.</strong> Your status there is temporary in a different way. Explain it honestly and lean more heavily on home-country ties.</li>
      <li><strong>Family in Canada.</strong> Having relatives in Canada isn't a problem, but the officer will weigh it. Show why you'll return to your job and life in the UAE.</li>
      <li><strong>Recently arrived in the UAE.</strong> A short residence history means less to show. Consider building a travel history first.</li>
    </ul>

    <div class="callout">
      <span class="mono-label">Be consistent</span>
      <p>Your forms, employer letter, bank statements and residence documents must all agree on dates, salary and job title. Inconsistencies are one of the fastest ways to lose an officer's confidence.</p>
    </div>
''',
    faq=[
        ("Does a UAE residence visa help my Canadian visa application?",
         "It can. A valid residence visa with good remaining validity, backed by a stable job and home, shows a settled life you're likely to return to. It works best alongside evidence of ties to your home country."),
        ("Does a UAE Golden Visa guarantee a Canadian visitor visa?",
         "No. Nothing guarantees a visa. A longer-term residence permit can support your case as evidence of commitment to the UAE, but the officer looks at your whole situation."),
        ("My UAE visa is being renewed. Should I still apply?",
         "If your current visa expires during or soon after your trip, consider waiting for the renewal or include clear evidence that it's in progress. A visa about to expire raises questions about where you'll go after Canada."),
    ],
    related=[R_UAE, R_REF, R_SUP, R_HUB],
    sources=[S_ELIG, S_TRV],
))

# ─────────────────────────────── SUPER VISA ───────────────────────────────
PAGES.append(dict(
    slug="super-visa-parents-gulf", group="guide", crumb="Super Visa for parents in the Gulf", date=DATE, read=8,
    title="Super Visa for Parents Living in the Gulf (UAE, Saudi, Qatar)",
    headline="Super Visa for parents and grandparents living in the Gulf",
    desc="Bringing parents who live in the Gulf to Canada on a Super Visa: who qualifies, the 2026 income rules, insurance, medical exam, fees and processing times.",
    keywords="Super Visa parents UAE, Super Visa from Dubai, Super Visa Gulf, Super Visa parents Saudi Arabia, Super Visa Qatar Kuwait Oman Bahrain, Super Visa income requirement 2026",
    h1="Super Visa for parents living in the Gulf",
    lede="Many Canadian families have parents who live and work in the Gulf, or who have retired there. The Super Visa lets them visit for long stretches, and the rules have some Gulf-specific details worth knowing.",
    kicker="Family", card_title="Super Visa for parents living in the Gulf",
    summary="Who qualifies, the host's income rules (eased in 2026), insurance, medical exams, fees and current Gulf processing times.",
    og_kicker="Gulf residents · Family", og_title="Super Visa for parents living in the Gulf",
    tags=[T_GULF, ("super-visa", "Super Visa"), ("family", "Family"), T_UAE],
    body='''    <h2>What the Super Visa is</h2>
    <p>The Super Visa lets parents and grandparents of Canadian citizens, permanent residents and registered Indians stay in Canada for up to 5 years at a time. It's a visitor document, so your parents can visit but not work.</p>

    <h2>What the host in Canada needs</h2>
    <ul>
      <li>To be the applicant's child or grandchild, and able to prove it.</li>
      <li>To be a Canadian citizen, permanent resident or registered Indian, at least 18, and living in Canada.</li>
      <li>To meet the <strong>minimum income</strong> for the family size.</li>
      <li>To write and sign a <strong>letter of invitation</strong>.</li>
    </ul>
    <div class="callout">
      <span class="mono-label">Income rules eased in 2026</span>
      <p>From March 31, 2026, hosts can use either of the two tax years before the application, and a parent's own income can top up the host's income once the host meets a minimum share. For parents with income in the Gulf, this can make a real difference.</p>
    </div>

    <h2>What your parents need</h2>
    <ul>
      <li>To apply from <strong>outside Canada</strong>. Parents legally living in the UAE or another Gulf country can apply from there.</li>
      <li><strong>Private medical insurance</strong> from a Canadian company or an approved company outside Canada, valid for at least one year from entry. Check IRCC's current minimum coverage before buying.</li>
      <li>An <strong>immigration medical exam</strong> with an IRCC-approved panel physician.</li>
      <li>To show they're genuine visitors who will leave Canada at the end of their stay, with ties, finances and a clear purpose.</li>
    </ul>

    <h2>The Gulf-specific details</h2>
    <ul>
      <li><strong>Their passport decides the visa.</strong> Parents with Emirati or Qatari passports don't need a visitor visa but still get a Super Visa approval letter for the longer stay, plus an eTA to fly.</li>
      <li><strong>Long absences from the Gulf.</strong> A 5-year stay in Canada can affect a Gulf residence visa that requires regular presence. Plan the trip around their residence rules so they have a home to return to.</li>
      <li><strong>Retired in the Gulf.</strong> If their residence is sponsored by another child or relative there, explain it and include that sponsor's documents.</li>
    </ul>

    <h2>Fees and processing times</h2>
    <p>The Super Visa fee is CAD $100 per person, plus CAD $85 per person for biometrics (CAD $170 maximum for a family). Current IRCC estimates for Super Visa applications from the Gulf:</p>
    <div class="who"><table><thead><tr><th>Applying from</th><th>Super Visa</th></tr></thead><tbody>
      <tr><td>United Arab Emirates</td><td>{{pt super AE}}</td></tr>
      <tr><td>Saudi Arabia</td><td>{{pt super SA}}</td></tr>
      <tr><td>Qatar</td><td>{{pt super QA}}</td></tr>
      <tr><td>Kuwait</td><td>{{pt super KW}}</td></tr>
      <tr><td>Oman</td><td>{{pt super OM}}</td></tr>
      <tr><td>Bahrain</td><td>{{pt super BH}}</td></tr>
    </tbody></table></div>
    <p class="live-note">IRCC published times, updated {{updated}}. "Not published" means IRCC hasn't published a time for that country right now.</p>
''',
    faq=[
        ("Can my parents apply for a Super Visa from the UAE?",
         "Yes, if they're legally living there. Super Visa applicants must apply from outside Canada, and parents with UAE residence can apply from the UAE."),
        ("How long can parents stay in Canada on a Super Visa?",
         "Up to 5 years at a time, according to IRCC."),
        ("What changed with the Super Visa income requirement in 2026?",
         "From March 31, 2026, hosts can meet the income requirement using either of the two tax years before applying, and the visiting parent's income can make up the remainder once the host meets a minimum share of the threshold."),
        ("Do Emirati parents need a Super Visa?",
         "Emirati citizens don't need a visitor visa, but they can apply for a Super Visa to stay up to 5 years. If approved, they receive a letter to show the border officer and need an eTA to fly."),
    ],
    related=[("/super-visa.html", "Super Visa: the full guide"), R_UAE, R_RES, R_HUB],
    sources=[S_SUPER, S_SUPER_FEES, S_SUPER_INC, S_ENTRY, S_TRACKER],
))

# ─────────────────────────────── BUSINESS ───────────────────────────────
PAGES.append(dict(
    slug="canada-business-visitor-dubai", group="guide", crumb="Visiting Canada on business from Dubai", date=DATE, read=7,
    title="Visiting Canada on Business from Dubai: Business Visitor Guide",
    headline="Visiting Canada on business from Dubai and the UAE",
    desc="Travelling from the UAE to Canada for meetings, a conference or a trade fair? What business visitors can do, documents to carry, and when you need a work permit.",
    keywords="Canada business visa Dubai, Canada business visitor UAE, Canada conference visa UAE, Canada trade show visa, business visitor Canada documents, Canada business trip from Dubai",
    h1="Visiting Canada on business from Dubai",
    lede="Dubai is a business hub, and people based there travel to Canada for meetings, conferences and trade fairs. Canada has clear rules for business visitors, and a short trip can usually be done without a work permit.",
    kicker="Business", card_title="Visiting Canada on business from Dubai",
    summary="What business visitors can do in Canada, the documents to carry from the UAE, and when you'd need a work permit instead.",
    og_kicker="Gulf residents · Business", og_title="Visiting Canada on business from Dubai",
    tags=[T_GULF, T_UAE, ("business-visitors", "Business visitors"), ("business-immigration", "Business immigration")],
    body='''    <h2>Who counts as a business visitor</h2>
    <p>IRCC describes a business visitor as someone coming to Canada for a few days or weeks, up to 6 months, who won't enter the Canadian labour market, and whose main place of business and source of income are outside Canada.</p>
    <p>If you work for a company in the UAE and you're paid there, a short business trip usually fits. You still need a visitor visa or eTA based on your passport, the same as for tourism.</p>

    <h2>What you can do</h2>
    <ul>
      <li>Attend meetings, conferences, conventions and trade fairs.</li>
      <li>Buy Canadian goods or services for your UAE company.</li>
      <li>Take orders for goods or services.</li>
      <li>Provide after-sales service under a warranty or sales agreement.</li>
      <li>Receive training from your parent company, or from a Canadian company that sold you equipment or services.</li>
      <li>Train employees of a Canadian branch of your company.</li>
    </ul>

    <h2>What you can't do</h2>
    <p>You can't work in the Canadian labour market. If you'll be doing hands-on work for a Canadian company, staying longer than 6 months, or being paid in Canada, you likely need a work permit. If your company is moving you to its Canadian office, see my guide to <a href="/business-work-permits.html" style="color:var(--maple)">intra-company transfer and treaty investor work permits</a>.</p>

    <h2>Documents to carry</h2>
    <p>IRCC recommends carrying these with you rather than packing them in checked luggage:</p>
    <ul class="checklist">
      <li>A passport valid for your whole stay, plus your visitor visa or eTA.</li>
      <li>A <strong>letter of support</strong> from your UAE employer or parent company.</li>
      <li>A <strong>letter of invitation</strong> from the Canadian business you're visiting.</li>
      <li>Any relevant contracts, warranty or service agreements.</li>
      <li>24-hour contact details for your host in Canada.</li>
      <li>Proof you can pay for your stay and return home.</li>
    </ul>
    <div class="callout">
      <span class="mono-label">Attending a registered event?</span>
      <p>If the event is registered with IRCC, the organizer gives you an event code to enter on your visa application. Ask for it before you apply.</p>
    </div>

    <h2>How long to allow from the UAE</h2>
    <p>If you need a visitor visa, IRCC currently estimates {{pt trv AE}} for applications from the UAE ({{updated}}), plus time for biometrics. Apply as soon as your event dates are confirmed.</p>
''',
    faq=[
        ("Do I need a work permit to attend a conference in Canada from Dubai?",
         "Usually not. Attending meetings, conferences and trade fairs are business visitor activities. You need a visitor visa or eTA based on your passport, and supporting letters from your employer and the Canadian host."),
        ("How long can a business visitor stay in Canada?",
         "Business visitors can stay up to 6 months. Staying longer, or working in the Canadian labour market, usually needs a work permit."),
        ("What is an IRCC event code?",
         "Some events are registered with IRCC. If yours is, the organizer gives you an event code to enter on your visitor visa application."),
    ],
    related=[("/business-work-permits.html", "ICT and treaty investor work permits"), R_UAE, R_HUB],
    sources=[S_BIZ, S_ENTRY, S_TRACKER],
))

# ─────────────────────────────── VERIFY ───────────────────────────────
PAGES.append(dict(
    slug="verify-canadian-immigration-consultant-uae", group="guide", crumb="Check a consultant is licensed", date=DATE, read=6,
    title="Is Your Canadian Immigration Consultant in the UAE Licensed?",
    headline="How to check that a Canadian immigration consultant in the UAE is licensed",
    desc="Before you pay anyone in the UAE for Canadian immigration help, check they're licensed: who can legally charge you, the CICC register, and red flags.",
    keywords="verify Canadian immigration consultant UAE, licensed immigration consultant Dubai, CICC register, RCIC Dubai, immigration scam Dubai Canada, authorized representative Canada",
    h1="How to check a consultant is licensed",
    lede="Dubai has no shortage of people offering to help you reach Canada. Some are excellent. Some are not licensed to charge you at all. Checking takes a minute, and it's the best protection you have.",
    kicker="Protect yourself", card_title="How to check a consultant is licensed",
    summary="Who can legally charge you for Canadian immigration help, how to search the CICC register, and the red flags to watch for in the UAE.",
    og_kicker="Gulf residents · Protect yourself", og_title="How to check a Canadian immigration consultant in the UAE is licensed",
    tags=[T_GULF, T_UAE, ("choosing-a-consultant", "Choosing a consultant")],
    body='''    <h2>Why this matters in the UAE</h2>
    <p>A Khaleej Times investigation found more than 400 immigration fraud cases in the UAE in 2023, with victims losing an estimated Dh20 million, and named Canada as the most prominent destination targeted.</p>

    <h2>Who can legally charge you</h2>
    <p>Under Canadian law, anyone who charges a fee for advice or representation on a Canadian immigration application must be authorized. That means:</p>
    <ul>
      <li>A <strong>licensed member of the College of Immigration and Citizenship Consultants (CICC)</strong>, such as a Regulated Canadian Immigration Consultant (RCIC), or</li>
      <li>A <strong>lawyer or notary in good standing with a Canadian law society</strong>.</li>
    </ul>
    <p>Helping someone without charging, as a friend or family member often does, is allowed. Charging without authorization is an offence in Canada, with fines of up to $100,000 and up to two years in prison on conviction by indictment.</p>

    <h2>How to check a consultant in under a minute</h2>
    <ul class="checklist">
      <li>Ask for their full name and their <strong>CICC registration number</strong>, which starts with R.</li>
      <li>Search the <strong>CICC public register</strong> at register.college-ic.ca.</li>
      <li>Confirm their status is <strong>active</strong> and they're <strong>entitled to practise</strong>.</li>
      <li>Make sure the name on the register matches the person who will actually handle your file, not just a name used by the agency.</li>
      <li>For a lawyer, check the relevant Canadian law society's directory. IRCC lists them on its authorized representatives page.</li>
    </ul>
    <div class="callout">
      <span class="mono-label">Check me</span>
      <p>I'm Kevin Thibbles, RCIC-IRB Class 3, registration <strong>R713044</strong>. Search for me on the CICC register before you send me anything.</p>
    </div>

    <h2>Red flags</h2>
    <ul>
      <li><strong>Guaranteed approval.</strong> No one can guarantee a Canadian visa. Only IRCC decides.</li>
      <li><strong>A "job offer" for a fee</strong>, or a promise of permanent residence in a few months.</li>
      <li><strong>Payment to a personal account</strong> or a money-transfer service, with no written agreement.</li>
      <li><strong>Refusing to be named</strong> as your representative on the IRCC "Use of a Representative" form, or asking you to sign forms they've filled with information you haven't seen.</li>
      <li><strong>Suggesting false documents</strong> or leaving out a past refusal. This can lead to a misrepresentation finding and a five-year bar.</li>
      <li><strong>No licence number</strong>, or a number that doesn't match the register.</li>
    </ul>
''',
    faq=[
        ("Can a consultant based in Dubai legally help me with a Canadian visa?",
         "They can charge you only if they're authorized under Canadian law: a licensed CICC member such as an RCIC, or a lawyer or notary in good standing with a Canadian law society. Location doesn't change this."),
        ("How do I check if an immigration consultant is licensed?",
         "Search their name or registration number on the CICC public register at register.college-ic.ca. Their status should be active and they should be entitled to practise."),
        ("Is it illegal to pay an unlicensed consultant?",
         "Under Canadian law, the offence is committed by the person who charges for advice or representation without authorization. You also risk your application, so it's always worth checking first."),
    ],
    related=[R_UAE, R_REF, R_HUB],
    sources=[S_REPS, S_CICC, S_CICC_FIND, S_LAWSOC, S_KT],
    cta_title="Want a second opinion before you sign?",
    cta_text="If someone has offered you a deal that sounds too good, send me the details. I'll tell you honestly whether it makes sense.",
))

# ─────────────────────────────── COUNTRY PAGES ───────────────────────────────
COUNTRIES = [
    dict(code="SA", name="Saudi Arabia", slug="saudi-arabia", demonym="Saudi", resid="Iqama (residence permit)",
         citizens="Saudi citizens need a <strong>visitor visa</strong> to travel to Canada.",
         extra="Saudi Arabia has one of the larger expat communities in the Gulf, and many residents travel to Canada for family visits and study. Your Iqama is the key document showing your status and employer, so make sure it's valid well beyond your trip.",
         cities="Riyadh, Jeddah or the Eastern Province"),
    dict(code="QA", name="Qatar", slug="qatar", demonym="Qatari", resid="Qatar ID (QID) and residence permit",
         citizens="Qatari citizens need an <strong>eTA</strong> to fly to Canada, not a visitor visa.",
         extra="Qatar's expat population includes many professionals in energy, aviation, health care and construction. If your residence permit is sponsored by your employer, an employer letter confirming your role and approved leave is especially important.",
         cities="Doha"),
    dict(code="KW", name="Kuwait", slug="kuwait", demonym="Kuwaiti", resid="Kuwait Civil ID and residence",
         citizens="Kuwaiti citizens need a <strong>visitor visa</strong> to travel to Canada.",
         extra="Many expats in Kuwait work in health care, oil and gas, and education. Your Civil ID and residence show your status. If you've lived in Kuwait for many years, that settled history is worth showing clearly.",
         cities="Kuwait City"),
    dict(code="OM", name="Oman", slug="oman", demonym="Omani", resid="Oman Resident Card",
         citizens="Omani citizens need a <strong>visitor visa</strong> to travel to Canada.",
         extra="Oman's expat residents often have long, stable work histories. Your Resident Card and employer documents show that stability, and they matter as much as your ties to your country of citizenship.",
         cities="Muscat"),
    dict(code="BH", name="Bahrain", slug="bahrain", demonym="Bahraini", resid="CPR card and residence permit",
         citizens="Bahraini citizens need a <strong>visitor visa</strong> to travel to Canada.",
         extra="Bahrain is a regional banking and services centre, and many residents commute or travel across the Gulf for work. Your CPR card and residence permit show your status, so make sure they're valid well beyond your trip.",
         cities="Manama"),
]

for c in COUNTRIES:
    code, name = c["code"], c["name"]
    PAGES.append(dict(
        slug=f"canada-visitor-visa-{c['slug']}-residents", group="country", crumb=f"Living in {name}", date=DATE, read=6,
        title=f"Canada Visitor Visa for {name} Residents (2026) | RCIC",
        headline=f"Canada visitor visa for people living in {name}",
        desc=f"Applying for a Canadian visitor visa while living in {name}? Visa or eTA, the documents that matter, and IRCC's current processing times.",
        keywords=f"Canada visitor visa {name} residents, Canada visa from {name}, Canada visit visa {name} expats, Canada visa {c['cities'].split(',')[0].split(' or ')[0]}, Canada eTA {name}, Canada super visa {name}",
        h1=f"Canada visitor visa for people living in {name}",
        lede=f"Most of what I've written for UAE residents applies across the Gulf. This page covers what's different if you live in {name}: your residence documents, who needs a visa, and how long IRCC is taking right now.",
        kicker=name, card_title=f"Living in {name}",
        summary=f"Visa or eTA, the {c['resid'].split(' and ')[0]} and other documents that matter, and live processing times from {name}.",
        og_kicker=f"Gulf residents · {name}", og_title=f"Canada visitor visa for people living in {name}",
        tags=[T_GULF, (c["slug"], name), T_TRV],
        body=f'''    <h2>Visa or eTA?</h2>
    <p>{c["citizens"]} For everyone else living in {name}, it depends on your passport, not your residence:</p>
''' + WHO_TABLE + f'''

    <h2>Living in {name} on a residence permit</h2>
    <p>{c["extra"]}</p>
    <p>The officer is deciding whether you'll leave Canada at the end of your visit. For someone living in {name}, that means showing both your settled life there and your ties to your country of citizenship.</p>

    <h2>Documents that carry weight</h2>
    <ul class="checklist">
      <li>Your passport and your <strong>{c["resid"]}</strong>, valid well beyond your trip.</li>
      <li>An <strong>employer letter</strong>: role, salary, start date, approved leave, and that your job continues.</li>
      <li><strong>Bank statements</strong> from your {name} account showing regular salary and savings.</li>
      <li>Your <strong>lease</strong> or proof of home, and family details if your family lives with you.</li>
      <li>Evidence of ties in your home country, and copies of previous visas and travel.</li>
      <li>A clear trip plan, and an invitation letter if you're staying with family or friends.</li>
    </ul>

    <h2>Fees and biometrics</h2>
    <p>You apply online. The visitor visa fee starts at CAD $100 and most applicants pay CAD $85 for biometrics, given at a Canada Visa Application Centre. Use IRCC's visa application centre finder for current locations serving {c["cities"]}.</p>

    <h2>Processing times from {name}</h2>
    <p>IRCC currently estimates {{{{pt trv {code}}}}} for visitor visa applications from {name} ({{{{updated}}}}), not including biometrics.</p>
    {{{{times_{code}}}}}

    <h2>Read next</h2>
    <p>These guides were written for the UAE, but the same principles apply in {name}:</p>
    <ul>
      <li><a href="/gulf/canada-visitor-visa-uae-residents.html" style="color:var(--maple)">The full visitor visa guide for Gulf residents</a></li>
      <li><a href="/gulf/canada-visa-refused-uae-resident.html" style="color:var(--maple)">What to do after a refusal</a></li>
      <li><a href="/gulf/uae-residence-visa-canada-visa.html" style="color:var(--maple)">How your residence status affects the decision</a></li>
      <li><a href="/gulf/super-visa-parents-gulf.html" style="color:var(--maple)">Super Visa for parents living in the Gulf</a></li>
    </ul>
''',
        faq=[
            (f"Do {c['demonym']} citizens need a visa for Canada?",
             re.sub("<[^>]+>", "", c["citizens"]) + " This is based on IRCC's entry requirements by country."),
            (f"Can I apply for a Canadian visitor visa while living in {name}?",
             f"Yes. Many people apply from {name} on a residence permit. Include your {c['resid']}, employer letter and evidence of ties to your home country."),
            (f"How long does a Canadian visitor visa take from {name}?",
             f"IRCC publishes a processing time for applications from {name} that changes regularly. This page shows the latest figure automatically, and biometrics time is extra."),
        ],
        related=[R_UAE, R_REF, R_SUP, R_HUB],
        sources=[S_ENTRY, S_ELIG, S_TRV, S_VAC, S_ETA13, S_TRACKER],
    ))

