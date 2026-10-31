"""Build the business work permits article and the Insights index for kevinthibbles.com.

Uses gcms-notes.html as the shared template (head icons, site CSS, nav, footer, floats)
so the new pages match the existing article pages exactly.
"""
import html, json, os, re, sys

ROOT = sys.argv[1]
TODAY = "2026-10-30"
SITE = "https://kevinthibbles.com"
tpl = open(os.path.join(ROOT, "gcms-notes.html"), encoding="utf-8").read()

# ---------- template pieces ----------
icons = tpl[tpl.index('<link rel="icon"'):tpl.index('<meta name="theme-color"')]
site_css = tpl[tpl.index('<link rel="preconnect"'):tpl.index('</style><script>') + len('</style>')]
theme_js = tpl[tpl.index('</style><script>') + len('</style>'):tpl.index('</head>')]
nav_end = tpl.index('<!-- /mobile-menu -->') + len('<!-- /mobile-menu -->') if '<!-- /mobile-menu -->' in tpl else tpl.index('</nav>') + len('</nav>')
nav = tpl[tpl.index('<nav class="nav"'):nav_end]
if '/insights/' not in nav: nav = nav.replace('      <a href="/#contact">Contact</a>', '      <a href="/insights/">Insights</a>\n      <a href="/#contact">Contact</a>')
footer_and_after = tpl[tpl.index('<footer class="footer">'):tpl.index('</body>')]

PERSON = {"@type": "Person", "@id": SITE + "/#kevin", "name": "Kevin Thibbles",
          "jobTitle": "Regulated Canadian Immigration Consultant (RCIC-IRB Class 3)", "identifier": "R713044",
          "memberOf": [{"@type": "Organization", "name": "College of Immigration and Citizenship Consultants"},
                       {"@type": "Organization", "name": "Canadian Association of Professional Immigration Consultants"}],
          "url": SITE + "/"}
ORG = {"@type": "ProfessionalService", "@id": SITE + "/#practice", "name": "Kevin Thibbles Immigration Services Inc.",
       "url": SITE + "/", "telephone": "+16479076890", "email": "kthibbles@kevinthibbles.com",
       "address": {"@type": "PostalAddress", "addressLocality": "Pickering", "addressRegion": "ON", "addressCountry": "CA"},
       "areaServed": {"@type": "Place", "name": "Worldwide"}, "founder": {"@id": SITE + "/#kevin"}}


def head(title, desc, keywords, url, og_type, og_image, graph, extra_meta="", extra_css=""):
    e = html.escape
    return f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{icons}<meta name="theme-color" content="#F4F2EC">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
<meta name="author" content="Kevin Thibbles, RCIC R713044">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:site_name" content="Kevin Thibbles Immigration Services Inc.">
<meta property="og:locale" content="en_CA">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(title)}">
{extra_meta}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)}
</script>
{site_css}<style>
{extra_css}
</style>{theme_js}</head>
<body id="top">

{nav}
'''


# Shared page-specific CSS (copied from the article template, plus new components)
page_css = tpl[tpl.index('/* page-specific */'):tpl.index('</style><script>')]

NEW_CSS = page_css + r'''
[hidden] { display: none !important; }
/* ── blog components ── */
.post-meta { display: flex; flex-wrap: wrap; gap: .4rem 1.4rem; margin: -1rem 0 2rem; }
.code { font-family: var(--font-mono); font-size: .78rem; font-weight: 500; color: var(--maple);
  background: var(--maple-tint); padding: .2rem .5rem; border-radius: 4px; white-space: nowrap; }
.routes { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 2rem 0; }
.route { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem; min-width: 0; }
.route h3 { font-family: var(--font-display); font-weight: 450; font-size: 1.4rem; margin: .4rem 0 .4rem; }
.route > p { font-size: .95rem; margin-bottom: .9rem; }
.route dl { display: grid; grid-template-columns: auto 1fr; gap: .45rem 1rem; font-size: .92rem; color: var(--ink-soft); }
.route dt { font-family: var(--font-mono); font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: var(--stone); padding-top: .2rem; }
.tbl { overflow-x: auto; margin: 1.5rem 0 2rem; border: 1px solid var(--line); border-radius: 12px; background: var(--card); }
.tbl table { border-collapse: collapse; width: 100%; min-width: 520px; font-size: .94rem; }
.tbl th, .tbl td { text-align: left; padding: .85rem 1rem; border-bottom: 1px solid var(--line); vertical-align: top; color: var(--ink-soft); }
.tbl th { font-family: var(--font-mono); font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: var(--stone); font-weight: 500; }
.tbl tr:last-child td { border-bottom: 0; }
.faq { display: grid; gap: .6rem; margin-top: 1rem; }
.faq details { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.25rem; }
.faq summary { cursor: pointer; font-weight: 600; color: var(--ink); }
.faq details p { margin: .7rem 0 0; font-size: .97rem; }
.tags { margin-top: 2.5rem; display: grid; gap: .7rem; }
.tag-list { display: flex; flex-wrap: wrap; gap: .5rem; list-style: none; padding: 0; margin: 0; }
.tag-list a, .tag-btn { display: inline-block; font-family: var(--font-mono); font-size: .74rem; font-weight: 500;
  color: var(--ink-soft); border: 1px solid var(--line); border-radius: 99px; padding: .45rem .85rem;
  background: var(--card); cursor: pointer; transition: border-color var(--transition), color var(--transition); }
.tag-list a:hover, .tag-btn:hover, .tag-btn[aria-pressed="true"] { border-color: var(--maple); color: var(--maple); }
.sources { font-size: .88rem; color: var(--stone); margin-top: 2.5rem; border-top: 1px solid var(--line); padding-top: 1.5rem; }
.sources a { color: var(--maple); text-decoration: underline; text-underline-offset: 3px; }
.sources ul li { font-size: .88rem; }

/* ── enquiry form (light card, separate from the homepage's dark form) ── */
.bwp { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: clamp(1.4rem, 4vw, 2.5rem); margin-top: 3.5rem; }
.bwp h2 { margin-top: .5rem !important; }
.bwp fieldset { border: 0; border-top: 1px solid var(--line); margin: 1.75rem 0 0; padding: 1.4rem 0 0; display: grid; gap: 1.1rem; min-width: 0; }
.bwp legend { font-family: var(--font-display); font-weight: 450; font-size: 1.3rem; padding-right: .6rem; color: var(--ink); }
.bwp .g2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 1.1rem; }
.bwp .q { display: grid; gap: .4rem; min-width: 0; }
.bwp .q > label, .bwp .ql { font-weight: 600; font-size: .92rem; color: var(--ink); }
.bwp .hint { font-size: .85rem; color: var(--stone); margin: 0; line-height: 1.6; }
.bwp input[type=text], .bwp input[type=email], .bwp input[type=tel], .bwp select, .bwp textarea {
  width: 100%; font: 400 1rem/1.4 var(--font-body); color: var(--ink); background: var(--paper);
  border: 1px solid var(--line); border-radius: 8px; padding: .75rem .85rem; }
.bwp input:focus, .bwp select:focus, .bwp textarea:focus { outline: 2px solid var(--maple); outline-offset: 1px; border-color: var(--maple); }
.bwp textarea { min-height: 110px; resize: vertical; }
.bwp .ch { display: grid; gap: .5rem; }
.bwp .c { display: flex; gap: .6rem; align-items: flex-start; font-size: .93rem; color: var(--ink-soft); cursor: pointer; }
.bwp .c input { margin-top: .3rem; accent-color: var(--maple); flex: none; }
.bwp .paths { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: .7rem; }
.bwp .paths label { border: 1px solid var(--line); border-radius: 10px; padding: .9rem; display: flex; gap: .6rem; cursor: pointer; background: var(--paper); }
.bwp .paths label:has(input:checked) { border-color: var(--maple); box-shadow: inset 0 0 0 1px var(--maple); }
.bwp .paths input { accent-color: var(--maple); margin-top: .3rem; }
.bwp .paths strong { display: block; font-size: .95rem; color: var(--ink); }
.bwp .paths small { font-size: .82rem; color: var(--stone); }
.bwp .note { font-size: .88rem; border-radius: 8px; padding: .75rem .9rem; background: var(--maple-tint); color: var(--ink-soft); margin: 0; }
.bwp .note b { color: var(--maple); }
.bwp .consent-box { background: var(--paper); border: 1px solid var(--line); border-radius: 10px; padding: 1rem; display: grid; gap: .8rem; }
.bwp .human { max-width: 120px; }
.bwp .err { color: var(--maple); font-size: .9rem; margin: 0; }
.bwp button[type=submit] { justify-self: start; font: 600 .95rem/1 var(--font-body); color: #fff; background: var(--maple);
  border: 0; border-radius: 99px; padding: 1rem 1.8rem; cursor: pointer; transition: background var(--transition); }
.bwp button[type=submit]:hover { background: var(--maple-dark); }
.bwp button[type=submit]:disabled { opacity: .6; cursor: progress; }
.bwp .result { border-radius: 10px; padding: 1.1rem 1.2rem; margin-top: 1.2rem; border: 1px solid var(--line); }
.bwp .result h3 { font-family: var(--font-display); font-weight: 450; font-size: 1.25rem; margin: 0 0 .4rem; color: var(--ink); }
.bwp .result p { margin: 0; }
.bwp .hp { position: absolute; left: -9999px; }

/* ── insights index ── */
.filters { display: flex; flex-wrap: wrap; gap: .5rem; margin: 0 0 2.5rem; }
.posts { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }
.post-card { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 1.6rem; display: flex; flex-direction: column; gap: .8rem; min-width: 0; transition: border-color var(--transition), transform var(--transition); }
.post-card:hover { border-color: var(--maple); transform: translateY(-2px); }
.post-card h2 { font-family: var(--font-display); font-weight: 450; font-size: 1.45rem; line-height: 1.2; letter-spacing: -.01em; }
.post-card p { font-size: .96rem; line-height: 1.7; color: var(--ink-soft); }
.post-card .more { margin-top: auto; font-weight: 600; color: var(--maple); font-size: .93rem; }
.post-card .tag-list a { font-size: .68rem; padding: .3rem .65rem; }
.empty { color: var(--stone); }
@media (max-width: 640px) { .filters { flex-wrap: nowrap; overflow-x: auto; padding-bottom: .4rem; } .tag-btn { white-space: nowrap; flex: none; } }
@media (prefers-reduced-motion: reduce) { .post-card { transition: none; } .post-card:hover { transform: none; } }
'''

# ---------- article ----------
ART_URL = SITE + "/business-work-permits.html"
ART_TITLE = "ICT & Treaty Investor Work Permits Canada | Kevin Thibbles"
ART_DESC = "How intra-company transfer (ICT) and treaty investor work permits work in Canada: eligibility, CUSMA rules, timelines and common pitfalls, from an RCIC."
ART_KW = ("intra-company transfer work permit Canada, ICT work permit Canada, treaty investor work permit Canada, "
          "CUSMA investor work permit, LMIA-exempt work permit, International Mobility Program, specialized knowledge work permit, "
          "C61 start-up work permit, business immigration Canada, RCIC Ontario")
TAGS = [("intra-company-transfer", "Intra-company transfer"), ("treaty-investor", "Treaty investor"), ("cusma", "CUSMA"),
        ("lmia-exempt", "LMIA-exempt work permits"), ("international-mobility-program", "International Mobility Program"),
        ("business-immigration", "Business immigration"), ("work-permits", "Work permits")]

FAQ = [
    ("Do I need an LMIA for an intra-company transfer?",
     "No. Intra-company transfers fall under the International Mobility Program, so they are exempt from the Labour Market Impact Assessment. The Canadian employer still submits an offer of employment through IRCC's Employer Portal and pays the employer compliance fee before you apply."),
    ("Can my company use an ICT to open its first office in Canada?",
     "Only if it is already a multinational. IRCC's start-up category (C61) is for companies with revenue-generating operations in at least two countries. A business that operates only in its home country can't use an ICT to open its first foreign office, though other routes may fit."),
    ("How long can I stay in Canada on an ICT work permit?",
     "Executives and managers can stay up to 7 years in total, and specialized knowledge employees up to 5 years, through an initial permit of up to 3 years and 2-year renewals. A start-up permit to open a new office is normally limited to 1 year."),
    ("Is there a minimum investment for a treaty investor work permit?",
     "No. IRCC doesn't set a dollar minimum. Officers use a proportionality test that compares your investment to the total cost of the business, so smaller businesses need a larger share from the investor."),
    ("Who can apply as a treaty investor?",
     "Only citizens of countries that have an investor category in a trade agreement with Canada, such as the United States and Mexico under CUSMA. Permanent residence in one of those countries doesn't count, and the Canadian business must be at least half owned by citizens of the treaty country."),
    ("Can these work permits lead to permanent residence?",
     "They can be a step toward it. Canadian work experience may help under Express Entry or a Provincial Nominee Program, but each program has its own requirements, and I assess this as part of long-term planning."),
]

art_graph = [
    {"@type": "BlogPosting", "@id": ART_URL + "#article",
     "headline": "Intra-company transfer and treaty investor work permits: bringing your business to Canada",
     "description": ART_DESC, "image": SITE + "/og/business-work-permits.png", "datePublished": TODAY, "dateModified": TODAY,
     "inLanguage": "en-CA", "mainEntityOfPage": ART_URL, "url": ART_URL, "author": {"@id": SITE + "/#kevin"},
     "publisher": {"@id": SITE + "/#practice"}, "keywords": [t for _, t in TAGS], "articleSection": "Business immigration",
     "isPartOf": {"@type": "Blog", "@id": SITE + "/insights/#blog", "name": "Insights", "url": SITE + "/insights/"}},
    PERSON, ORG,
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Insights", "item": SITE + "/insights/"},
        {"@type": "ListItem", "position": 3, "name": "Business work permits", "item": ART_URL}]},
    {"@type": "FAQPage", "@id": ART_URL + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]
art_meta = "".join([f'<meta property="article:published_time" content="{TODAY}">\n',
                    f'<meta property="article:modified_time" content="{TODAY}">\n',
                    '<meta property="article:author" content="Kevin Thibbles">\n',
                    '<meta property="article:section" content="Business immigration">\n'] +
                   [f'<meta property="article:tag" content="{t}">\n' for _, t in TAGS])

tag_html = "\n".join(f'        <li><a href="/insights/#{s}" rel="tag">{t}</a></li>' for s, t in TAGS)
faq_html = "\n".join(f'      <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in FAQ)

CITIZENSHIPS = ["Australia", "Brunei", "Chile", "Colombia", "European Union member state", "Japan", "Malaysia", "New Zealand",
                "Panama", "Peru", "Singapore", "South Korea", "Ukraine", "United Kingdom", "Vietnam"]
cit_opts = "\n".join(f"            <option>{c}</option>" for c in CITIZENSHIPS)

article_body = f'''
<header class="page-hero">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; <a href="/insights/">Insights</a> &nbsp;/&nbsp; Business work permits</div>
    <h1 class="page-title">Intra-company transfer and treaty investor work permits<span class="accent">.</span></h1>
    <p class="page-lede">If you're an executive, a key specialist, or an investor, Canada has LMIA-exempt work permit routes built for business. Here is how intra-company transfers and treaty investor permits work, and how to tell which one fits your situation.</p>
    <div class="post-meta">
      <span class="mono-label">By Kevin Thibbles, RCIC</span>
      <span class="mono-label">Published <time datetime="{TODAY}">October 30, 2026</time></span>
      <span class="mono-label">Last reviewed <time datetime="{TODAY}">October 30, 2026</time></span>
      <span class="mono-label">9 min read</span>
    </div>
    <div class="hero-actions">
      <a href="#enquiry" class="btn-primary">Check which route may fit</a>
      <a href="https://wa.me/16479076890" class="btn-ghost" target="_blank" rel="noopener">Message me on WhatsApp</a>
    </div>
  </div>
</header>

<section class="section">
  <article class="wrap prose">
    <h2>What the International Mobility Program (IMP) is</h2>
    <p>Most employers who hire foreign workers in Canada need a Labour Market Impact Assessment (LMIA), which shows that no Canadian was available for the job. The International Mobility Program is the set of work permits that are exempt from that step, because the work brings a broader benefit to Canada or because Canada has agreed to it in a trade treaty.</p>
    <p>Two IMP routes matter most to businesses: <strong>intra-company transfers</strong> and <strong>treaty investor</strong> permits. They are often confused, but they rest on different rules. The first question I ask every business client is which legal door they are walking through.</p>

    <div class="routes">
      <div class="route">
        <span class="mono-label">Route one</span>
        <h3>Intra-company transfer</h3>
        <p>Your existing employer moves you to its Canadian office.</p>
        <dl>
          <dt>Citizenship</dt><dd>Any nationality under the general rules</dd>
          <dt>Who</dt><dd>Executives, managers, specialized knowledge employees</dd>
          <dt>Key test</dt><dd>A real multinational and one year of employment with it</dd>
          <dt>Codes</dt><dd><span class="code">C61</span> <span class="code">C62</span> <span class="code">C63</span></dd>
        </dl>
      </div>
      <div class="route">
        <span class="mono-label">Route two</span>
        <h3>Treaty investor</h3>
        <p>You invest substantially in a Canadian business and come to run it.</p>
        <dl>
          <dt>Citizenship</dt><dd>Only citizens of certain free trade partners</dd>
          <dt>Who</dt><dd>The investor, plus key executives or essential staff</dd>
          <dt>Key test</dt><dd>A substantial investment and control of the business</dd>
          <dt>Example</dt><dd><span class="code">T35</span> CUSMA investors</dd>
        </dl>
      </div>
    </div>

    <h2 id="ict">Intra-company transfer (ICT) work permits</h2>
    <p>An intra-company transfer lets a multinational company send an existing employee to work at its Canadian parent, branch, subsidiary or affiliate. Under IRCC's instructions, the general ICT category is open to applicants of any citizenship.</p>
    <h3>The core requirements</h3>
    <ul>
      <li>You currently work for the company outside Canada as an executive, a manager, or in a role that requires specialized knowledge.</li>
      <li>You have worked for it continuously, full-time, for at least one year in the last three years. Part-time work that adds up to a year doesn't count.</li>
      <li>The company is a genuine multinational, with revenue-generating operations in at least one country besides its home country.</li>
      <li>The Canadian business is owned or controlled by the same group. Franchise, licensing, supplier and client relationships don't qualify.</li>
      <li>The Canadian business is actively operating from real commercial premises. A home office or a mail-drop address won't do.</li>
      <li>You are moving temporarily, in the same capacity, and your job abroad stays open for your return.</li>
    </ul>
    <h3>The three ICT categories</h3>
    <div class="tbl">
      <table>
        <thead><tr><th>Code</th><th>Purpose</th><th>Time limits</th></tr></thead>
        <tbody>
          <tr><td><span class="code">C61</span></td><td>Opening a new Canadian office for an existing multinational</td><td>Up to 1 year, then you move into one of the categories below</td></tr>
          <tr><td><span class="code">C62</span></td><td>Executives and senior managers</td><td>Up to 3 years at first, renewable in 2-year steps, 7 years in total</td></tr>
          <tr><td><span class="code">C63</span></td><td>Specialized knowledge employees</td><td>Up to 3 years at first, renewable in 2-year steps, 5 years in total</td></tr>
        </tbody>
      </table>
    </div>
    <div class="callout">
      <span class="mono-label">The start-up trap</span>
      <p>A company can't use an ICT to open its very first office outside its home country. It has to be a multinational before it comes to Canada.</p>
    </div>
    <p>"Specialized knowledge" is where many applications struggle. IRCC expects both advanced knowledge of the company's own products, processes or systems and an advanced level of expertise. Being highly skilled in your field is not enough on its own, and the Canadian salary must meet at least the prevailing wage for the job and region.</p>

    <h2 id="treaty-investors">Treaty investor work permits under CUSMA and other trade agreements</h2>
    <p>Several of Canada's free trade agreements let citizens of partner countries come to Canada to develop and direct a business they have invested in. The Canada-United States-Mexico Agreement (CUSMA) is the best-known example, and CPTPP, the UK agreement, and agreements with Korea, Peru and Colombia have investor categories of their own. Eligibility depends on your citizenship, so this is the first thing I check.</p>
    <h3>What officers look for, using CUSMA as the example</h3>
    <ul>
      <li><strong>Nationality of the business.</strong> This depends on ownership, not where the company is incorporated. At least half the Canadian business must be owned by citizens of the treaty country.</li>
      <li><strong>Control.</strong> You generally need a controlling interest. A 50/50 partnership usually isn't enough, especially in a smaller business.</li>
      <li><strong>A substantial investment.</strong> There is no minimum dollar amount. Officers compare what you put in against the total cost of the business: the smaller the business, the larger your share needs to be.</li>
      <li><strong>Money that is committed.</strong> Funds sitting in a personal account don't count. The money must be invested or irrevocably committed, and you must show it came from legitimate sources.</li>
      <li><strong>A real, active business.</strong> It must produce goods or services for profit and earn more than a living for you and your family. Passive or speculative investments, such as holding property for appreciation, don't qualify.</li>
    </ul>
    <p>For CUSMA investors, the first permit is issued for up to one year and extensions are normally granted in two-year increments if the requirements are still met. IRCC asks investors to apply before travelling rather than at the border.</p>

    <h2>Where applications tend to go wrong</h2>
    <ul>
      <li>A Canadian "office" that exists only on paper, with no premises, staff or revenue.</li>
      <li>A manager's title without real managerial duties, or a business too small to justify one.</li>
      <li>Specialized knowledge described in general industry terms rather than company-specific ones.</li>
      <li>An investment that hasn't been committed yet, or a source of funds that isn't documented.</li>
      <li>An employer offer or compliance fee not completed in IRCC's Employer Portal before the worker applies.</li>
    </ul>

    <h2>Can my family come with me?</h2>
    <p>Spouses, common-law partners and dependent children can often come with you, but the rules depend on the route and on your occupation. Some trade agreements include their own spouse provisions; others rely on Canada's general spousal open work permit rules. I review your family situation as part of every business file.</p>

    <h2 id="faq">Frequently asked questions</h2>
    <div class="faq">
{faq_html}
    </div>

    <h2>How I can help</h2>
    <p>I work through each file with you: confirming which route fits, reviewing the corporate structure and ownership, preparing the employer's offer in the Employer Portal, building the business plan and investment evidence, and preparing you for questions at the visa office or the border. Every case depends on its own facts, and no consultant can promise an approval. What I can promise is a clear, honest assessment of where your file is strong and where it needs work.</p>

    <div class="bwp" id="enquiry">
      <span class="mono-label">Pre-consultation enquiry</span>
      <h2>Tell me about your business plans</h2>
      <p>Your answers help me see which IMP route may apply before we speak. It takes about five minutes. Submitting this form doesn't create a consultant–client relationship, and I don't give advice until a consultation agreement is signed.</p>

      <form id="bwpForm" novalidate>
        <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <fieldset>
          <legend>About you</legend>
          <div class="g2">
            <div class="q"><label for="b-name">Full name</label><input type="text" id="b-name" name="name" autocomplete="name" required></div>
            <div class="q"><label for="b-email">Email</label><input type="email" id="b-email" name="email" autocomplete="email" required></div>
            <div class="q"><label for="b-phone">WhatsApp or phone (optional)</label><input type="tel" id="b-phone" name="phone" autocomplete="tel"></div>
            <div class="q"><label for="b-res">Country where you live now</label><input type="text" id="b-res" name="country_of_residence" autocomplete="country-name" required></div>
          </div>
          <div class="q">
            <label for="b-cit">Your citizenship</label>
            <select id="b-cit" name="citizenship" required>
              <option value="">Please choose…</option>
              <optgroup label="CUSMA"><option>United States</option><option>Mexico</option></optgroup>
              <optgroup label="Other trade partners">
{cit_opts}
              </optgroup>
              <option>Another country</option>
            </select>
            <p class="hint">Treaty investor permits depend on citizenship, not where you live. Permanent residence elsewhere doesn't count.</p>
          </div>
          <div class="q" id="b-othercit-wrap" hidden><label for="b-othercit">Which country?</label><input type="text" id="b-othercit" name="citizenship_other"></div>
          <p class="note" id="n-cit" hidden><b>Good to know:</b> investor categories exist only under certain trade agreements, so the treaty investor route may not be open to you. Intra-company transfers are available to any citizenship, and I'll look at other options too.</p>
        </fieldset>

        <fieldset>
          <legend>Which route interests you?</legend>
          <div class="paths" role="radiogroup" aria-label="Route">
            <label><input type="radio" name="route" value="Intra-company transfer" required><span><strong>Company transfer</strong><small>My employer is moving me to Canada</small></span></label>
            <label><input type="radio" name="route" value="Treaty investor"><span><strong>Treaty investor</strong><small>I'm investing in a Canadian business</small></span></label>
            <label><input type="radio" name="route" value="Not sure"><span><strong>Not sure yet</strong><small>Help me work out which fits</small></span></label>
          </div>
        </fieldset>

        <fieldset id="b-ict" hidden>
          <legend>Your employer and role</legend>
          <div class="q">
            <span class="ql" id="ql-mnc">Does your employer earn revenue in at least two countries?</span>
            <div class="ch" role="radiogroup" aria-labelledby="ql-mnc">
              <label class="c"><input type="radio" name="ict_multinational" value="Yes, two or more countries">Yes, two or more countries</label>
              <label class="c"><input type="radio" name="ict_multinational" value="Only in our home country">Only in our home country</label>
              <label class="c"><input type="radio" name="ict_multinational" value="Not sure">Not sure</label>
            </div>
          </div>
          <p class="note" id="n-mnc" hidden><b>Good to know:</b> an ICT is only for multinational companies. A single-country business can't use it to open its first foreign office, but other routes may fit, and I'll go through them with you.</p>
          <div class="g2">
            <div class="q"><label for="b-rel">How is the Canadian business related to your employer?</label>
              <select id="b-rel" name="ict_relationship"><option value="">Please choose…</option><option>Parent company</option><option>Subsidiary</option><option>Branch</option><option>Affiliate (common ownership)</option><option>No Canadian office yet; we plan to open one</option><option>Franchise, licence, client or supplier</option><option>Not sure</option></select></div>
            <div class="q"><label for="b-role">Your role with the employer</label>
              <select id="b-role" name="ict_role"><option value="">Please choose…</option><option>Executive (directs the company or a major function)</option><option>Senior manager (manages managers or professionals)</option><option>Specialized knowledge (company-specific expertise)</option><option>Other</option></select></div>
            <div class="q"><label for="b-ten">Continuous full-time employment with this employer</label>
              <select id="b-ten" name="ict_tenure"><option value="">Please choose…</option><option>Less than 1 year</option><option>1 to 2 years</option><option>More than 2 years</option></select></div>
            <div class="q"><label for="b-prem">Does the Canadian business have commercial premises?</label>
              <select id="b-prem" name="ict_premises"><option value="">Please choose…</option><option>Yes, an office or facility</option><option>Not yet, we're securing them</option><option>Home-based or virtual only</option><option>Not sure</option></select></div>
          </div>
          <p class="note" id="n-ten" hidden><b>Good to know:</b> the ICT rules require at least one year of continuous full-time work with the employer in the last three years. We can talk about timing.</p>
        </fieldset>

        <fieldset id="b-inv" hidden>
          <legend>Your investment</legend>
          <div class="g2">
            <div class="q"><label for="b-own">Your share of the Canadian business</label>
              <select id="b-own" name="inv_ownership"><option value="">Please choose…</option><option>More than 50%</option><option>Exactly 50%</option><option>Less than 50%</option><option>Not decided yet</option></select></div>
            <div class="q"><label for="b-stage">Where is the investment now?</label>
              <select id="b-stage" name="inv_stage"><option value="">Please choose…</option><option>Already invested</option><option>Funds committed under a signed agreement</option><option>Still planning</option></select></div>
            <div class="q"><label for="b-type">New or existing business?</label>
              <select id="b-type" name="inv_business_type"><option value="">Please choose…</option><option>Starting a new business</option><option>Buying an existing business</option><option>Expanding a business I already own in Canada</option></select></div>
            <div class="q"><label for="b-ind">Industry</label><input type="text" id="b-ind" name="inv_industry" placeholder="e.g. restaurant, manufacturing, software"></div>
            <div class="q"><label for="b-total">Approximate total cost of the business (CAD)</label>
              <select id="b-total" name="inv_total_cost"><option value="">Please choose…</option><option>Under $250,000</option><option>$250,000 to $500,000</option><option>$500,000 to $1 million</option><option>$1 million to $5 million</option><option>Over $5 million</option></select></div>
            <div class="q"><label for="b-contrib">Your own contribution (CAD)</label>
              <select id="b-contrib" name="inv_contribution"><option value="">Please choose…</option><option>Under $100,000</option><option>$100,000 to $250,000</option><option>$250,000 to $500,000</option><option>$500,000 to $1 million</option><option>Over $1 million</option></select></div>
          </div>
          <div class="q">
            <span class="ql" id="ql-funds">Can you document where the investment funds came from?</span>
            <div class="ch" role="radiogroup" aria-labelledby="ql-funds">
              <label class="c"><input type="radio" name="inv_source_of_funds" value="Yes, fully documented">Yes, with bank records, sale documents or similar</label>
              <label class="c"><input type="radio" name="inv_source_of_funds" value="Partly documented">Partly</label>
              <label class="c"><input type="radio" name="inv_source_of_funds" value="Not sure">Not sure</label>
            </div>
          </div>
          <p class="note" id="n-own" hidden><b>Good to know:</b> officers usually expect an investor to control the business, and 50% or less often isn't enough. I'll walk through your ownership structure with you.</p>
        </fieldset>

        <fieldset id="b-rest" hidden>
          <legend>Family and timing</legend>
          <div class="g2">
            <div class="q"><label for="b-sp">Will a spouse or partner come with you?</label>
              <select id="b-sp" name="spouse_accompanying"><option value="">Please choose…</option><option>Yes</option><option>No</option><option>Not sure</option></select></div>
            <div class="q"><label for="b-kids">Dependent children coming with you</label>
              <select id="b-kids" name="children_accompanying"><option value="">Please choose…</option><option>None</option><option>1</option><option>2</option><option>3 or more</option></select></div>
            <div class="q"><label for="b-when">When would you like to start work in Canada?</label>
              <select id="b-when" name="target_start"><option value="">Please choose…</option><option>Within 3 months</option><option>3 to 6 months</option><option>6 to 12 months</option><option>More than a year away</option></select></div>
            <div class="q"><label for="b-ref">Have you been refused before?</label>
              <select id="b-ref" name="previously_refused"><option value="">Please choose…</option><option>No</option><option>Yes — once</option><option>Yes — more than once</option><option>I would rather discuss this on the call</option></select></div>
          </div>
          <div class="q"><label for="b-msg">Anything else I should know?</label>
            <textarea id="b-msg" name="message" maxlength="700" placeholder="A short description of the business, your role, and what you'd like to achieve in Canada."></textarea>
            <p class="hint">Please don't send passport numbers, ID numbers or detailed personal history here. I'll ask for documents securely once we've agreed to work together.</p></div>
        </fieldset>

        <fieldset>
          <legend>Before you send</legend>
          <div class="q"><label for="b-human">Quick human check: what is <strong id="b-sa">3</strong> + <strong id="b-sb">4</strong>?</label>
            <input type="text" id="b-human" class="human" inputmode="numeric" autocomplete="off" required></div>
          <div class="consent-box">
            <label class="c"><input type="checkbox" id="b-c1" name="consent" value="Yes" required>I consent to Kevin Thibbles Immigration Services Inc. contacting me about my enquiry and storing this information for that purpose.</label>
            <label class="c"><input type="checkbox" id="b-c2" name="acknowledged_no_guarantee" value="Yes" required>I understand this form is not an assessment or legal advice, does not create a client relationship, and that no outcome can be guaranteed.</label>
          </div>
          <p class="err" id="b-err" role="alert" hidden></p>
          <button type="submit" id="b-send">Send my enquiry</button>
        </fieldset>
      </form>
      <div class="result" id="b-ok" hidden role="status"><h3>Thank you, your enquiry has been sent</h3><p>I review every enquiry personally and reply within 24 hours on business days. If your timeline is urgent, email me at kthibbles@kevinthibbles.com.</p></div>
      <div class="result" id="b-bad" hidden role="alert"><h3>Your enquiry didn't go through</h3><p>Your answers are still in the form. Please try again in a moment, or email me at kthibbles@kevinthibbles.com or message me on WhatsApp at +1 (647) 907-6890.</p></div>
    </div>

    <nav class="tags" aria-label="Topics">
      <span class="mono-label">Topics</span>
      <ul class="tag-list">
{tag_html}
      </ul>
    </nav>

    <div class="sources">
      <p>This article is general information based on IRCC's published program delivery instructions as of October 2026. It isn't legal advice and doesn't assess any individual case. Rules and fees change, so please confirm current requirements on IRCC.ca.</p>
      <ul>
        <li><a href="https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/operational-bulletins-manuals/temporary-residents/foreign-workers/exemption-codes/intra-company-transferees.html" target="_blank" rel="noopener">IRCC: Intra-company transferees [R205(a) – C61, C62, C63]</a></li>
        <li><a href="https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/operational-bulletins-manuals/temporary-residents/foreign-workers/international-free-trade-agreements/cusma/investors.html" target="_blank" rel="noopener">IRCC: Investors – CUSMA [R204(a) – T35]</a></li>
        <li><a href="https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/operational-bulletins-manuals/temporary-residents/foreign-workers/international-free-trade-agreements.html" target="_blank" rel="noopener">IRCC: International free trade agreements</a></li>
      </ul>
    </div>

    <div class="related">
      <a href="/insights/">All insights <span class="ar">&rarr;</span></a>
      <a href="/visitor-visa-refused.html">Visitor visa refused <span class="ar">&rarr;</span></a>
      <a href="/gcms-notes.html">GCMS notes explained <span class="ar">&rarr;</span></a>
      <a href="/super-visa.html">Super Visa for parents &amp; grandparents <span class="ar">&rarr;</span></a>
      <a href="/#contact">Contact <span class="ar">&rarr;</span></a>
    </div>
  </article>
</section>

'''

FORM_JS = r'''<script>
(function(){
  var ACCESS_KEY = "3bd1aeef-4d7d-4ed8-8434-e9f78f066057";
  var form = document.getElementById("bwpForm"); if(!form) return;
  var $ = function(id){return document.getElementById(id);};
  var a = 2 + Math.floor(Math.random()*7), b = 1 + Math.floor(Math.random()*8);
  $("b-sa").textContent = a; $("b-sb").textContent = b;
  var loadedAt = Date.now();
  function val(n){var el=form.querySelector('[name="'+n+'"]:checked');return el?el.value:"";}
  function update(){
    var route = val("route"), cit = $("b-cit").value;
    $("b-othercit-wrap").hidden = cit !== "Another country";
    $("b-ict").hidden = !(route === "Intra-company transfer" || route === "Not sure");
    $("b-inv").hidden = !(route === "Treaty investor" || route === "Not sure");
    $("b-rest").hidden = !route;
    $("n-cit").hidden = !(cit === "Another country" && (route === "Treaty investor" || route === "Not sure"));
    $("n-mnc").hidden = $("b-ict").hidden || val("ict_multinational") !== "Only in our home country";
    $("n-ten").hidden = $("b-ict").hidden || $("b-ten").value !== "Less than 1 year";
    var own = $("b-own").value;
    $("n-own").hidden = $("b-inv").hidden || !(own === "Exactly 50%" || own === "Less than 50%");
  }
  form.addEventListener("change", update); update();

  form.addEventListener("submit", function(e){
    e.preventDefault();
    var err = $("b-err"); err.hidden = true;
    var miss = [];
    if(!$("b-name").value.trim()) miss.push("your name");
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($("b-email").value.trim())) miss.push("a valid email address");
    if(!$("b-res").value.trim()) miss.push("the country where you live");
    if(!$("b-cit").value) miss.push("your citizenship");
    if(!val("route")) miss.push("the route that interests you");
    if(parseInt($("b-human").value,10) !== a + b) miss.push("the correct answer to the human check");
    if(!$("b-c1").checked || !$("b-c2").checked) miss.push("both acknowledgements");
    if(miss.length){ err.textContent = "Please add " + miss.join(", ") + " before sending."; err.hidden = false; return; }
    if(form.querySelector('[name="botcheck"]').checked || Date.now() - loadedAt < 3000) return;

    var data = {};
    form.querySelectorAll("input,select,textarea").forEach(function(el){
      if(!el.name || el.name === "botcheck") return;
      var fs = el.closest("fieldset"); if(fs && fs.hidden) return;
      if((el.type === "radio" || el.type === "checkbox") && !el.checked) return;
      if(el.value) data[el.name] = el.value;
    });
    data.access_key = ACCESS_KEY;
    data.subject = "Business work permit enquiry: " + data.name + " (" + data.route + ")";
    data.from_name = "kevinthibbles.com: Business Work Permits";
    data.replyto = data.email;
    data.page = location.href;

    var btn = $("b-send"); btn.disabled = true; btn.textContent = "Sending…"; $("b-bad").hidden = true;
    fetch("https://api.web3forms.com/submit", {method:"POST", headers:{"Content-Type":"application/json", Accept:"application/json"}, body: JSON.stringify(data)})
      .then(function(r){ return r.json(); })
      .then(function(j){ if(j && j.success){ form.hidden = true; $("b-ok").hidden = false; $("b-ok").scrollIntoView({block:"center"}); } else { throw new Error("failed"); } })
      .catch(function(){ $("b-bad").hidden = false; })
      .finally(function(){ btn.disabled = false; btn.textContent = "Send my enquiry"; });
  });
})();
</script>
'''

article = (head(ART_TITLE, ART_DESC, ART_KW, ART_URL, "article", SITE + "/og/business-work-permits.png", art_graph, art_meta, NEW_CSS)
           + article_body + footer_and_after + FORM_JS + "</body>\n</html>\n")
open(os.path.join(ROOT, "business-work-permits.html"), "w", encoding="utf-8").write(article)

# ---------- insights index ----------
POSTS = [
    ("/business-work-permits.html", "Intra-company transfer and treaty investor work permits",
     "How ICT and treaty investor permits work under the International Mobility Program, who qualifies, and where applications go wrong.",
     TODAY, TAGS),
    ("/visitor-visa-refused.html", "Visitor visa refused? What to do next",
     "Understand your refusal letter, what GCMS notes reveal, and how to build a stronger reapplication.",
     "2026-09-10", [("visa-refusals", "Visa refusals"), ("visitor-visas", "Visitor visas"), ("temporary-residence", "Temporary residence")]),
    ("/gcms-notes.html", "GCMS notes explained",
     "The officer's internal case notes on your file: what they contain, how to request them, and what they reveal after a refusal.",
     "2026-09-10", [("gcms-notes", "GCMS notes"), ("visa-refusals", "Visa refusals")]),
    ("/super-visa.html", "Super Visa for parents and grandparents",
     "Super Visa requirements, common reasons applications are refused, and how to prepare a strong file.",
     "2026-09-10", [("super-visa", "Super Visa"), ("visitor-visas", "Visitor visas"), ("family", "Family")]),
    ("/study-permit-refused.html", "Study permit refused? Why it happens and what to do",
     "Common study permit refusal reasons, what GCMS notes reveal, and how to build a stronger reapplication.",
     "2026-09-10", [("study-permits", "Study permits"), ("visa-refusals", "Visa refusals")]),
]
all_tags = []
for *_, tg in POSTS:
    for t in tg:
        if t not in all_tags:
            all_tags.append(t)

def nice_date(d):
    y, m, dd = d.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{months[int(m)-1]} {int(dd)}, {y}"

cards = []
for href, title, summary, date, tg in POSTS:
    tl = "".join(f'<li><a href="#{s}" data-tag="{s}">{t}</a></li>' for s, t in tg)
    cards.append(f'''      <article class="post-card" data-tags="{' '.join(s for s, _ in tg)}">
        <span class="mono-label"><time datetime="{date}">{nice_date(date)}</time></span>
        <h2><a href="{href}">{html.escape(title)}</a></h2>
        <p>{html.escape(summary)}</p>
        <ul class="tag-list">{tl}</ul>
        <a class="more" href="{href}" aria-hidden="true" tabindex="-1">Read the article &rarr;</a>
      </article>''')
filters = '<button type="button" class="tag-btn" data-filter="" aria-pressed="true">All topics</button>' + "".join(
    f'<button type="button" class="tag-btn" data-filter="{s}" aria-pressed="false">{t}</button>' for s, t in all_tags)

INS_URL = SITE + "/insights/"
INS_TITLE = "Canadian Immigration Insights | Kevin Thibbles, RCIC"
INS_DESC = "Plain-English guides to Canadian immigration from a licensed RCIC: visa refusals, GCMS notes, Super Visas, study permits and business work permits."
ins_graph = [
    {"@type": "Blog", "@id": INS_URL + "#blog", "name": "Insights", "url": INS_URL, "description": INS_DESC, "inLanguage": "en-CA",
     "author": {"@id": SITE + "/#kevin"}, "publisher": {"@id": SITE + "/#practice"},
     "blogPost": [{"@type": "BlogPosting", "headline": t, "url": SITE + h, "datePublished": d, "keywords": [x for _, x in tg]} for h, t, _, d, tg in POSTS]},
    PERSON, ORG,
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Insights", "item": INS_URL}]},
]
ins_body = f'''
<header class="page-hero">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; Insights</div>
    <h1 class="page-title">Insights<span class="accent">.</span></h1>
    <p class="page-lede">Plain-English guides to Canadian immigration, written from my own practice as a licensed RCIC. Each one is based on IRCC's published rules.</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter by topic">{filters}</div>
    <div class="posts" id="posts">
{chr(10).join(cards)}
    </div>
    <p class="empty" id="empty" hidden>No articles on this topic yet. <a href="/insights/" style="color:var(--maple)">Show all topics</a></p>
    <div class="related">
      <a href="/tracker/">Check visa wait times <span class="ar">&rarr;</span></a>
      <a href="/#services">Services <span class="ar">&rarr;</span></a>
      <a href="/#contact">Contact <span class="ar">&rarr;</span></a>
    </div>
  </div>
</section>

'''
INS_JS = r'''<script>
(function(){
  var cards = document.querySelectorAll(".post-card"), btns = document.querySelectorAll(".tag-btn");
  function apply(){
    var tag = decodeURIComponent((location.hash || "").slice(1)), shown = 0;
    btns.forEach(function(b){ b.setAttribute("aria-pressed", b.dataset.filter === tag ? "true" : "false"); });
    cards.forEach(function(c){ var on = !tag || c.dataset.tags.split(" ").indexOf(tag) > -1; c.hidden = !on; if(on) shown++; });
    document.getElementById("empty").hidden = shown > 0;
  }
  btns.forEach(function(b){ b.addEventListener("click", function(){
    if(b.dataset.filter){ location.hash = b.dataset.filter; } else { history.replaceState(null, "", location.pathname); apply(); }
  }); });
  window.addEventListener("hashchange", apply); apply();
})();
</script>
'''
os.makedirs(os.path.join(ROOT, "insights"), exist_ok=True)
ins = (head(INS_TITLE, INS_DESC, "Canadian immigration blog, RCIC insights, visa refusal guide, GCMS notes, Super Visa, study permit refused, intra-company transfer, treaty investor",
            INS_URL, "website", SITE + "/og/insights.png", ins_graph, "", NEW_CSS)
       + ins_body + footer_and_after + INS_JS + "</body>\n</html>\n")
open(os.path.join(ROOT, "insights", "index.html"), "w", encoding="utf-8").write(ins)
print("built")
