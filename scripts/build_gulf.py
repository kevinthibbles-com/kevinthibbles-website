"""Build the Gulf residents section (/gulf/) of kevinthibbles.com.

Pages are written in scripts/gulf_content.py. This script wraps them in the site's
shared template (taken from gcms-notes.html), adds search-engine metadata, live IRCC
processing times from tracker/data/processing-times.json, share images, sitemap entries,
and writes scripts/gulf_posts.json for the Insights page.

Run from the repository root, in this order:
    python3 scripts/build_gulf.py
    python3 scripts/build_blog.py .
    python3 scripts/responsive_patch.py
"""
import html, json, os, re, sys, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import gulf_content as C  # noqa: E402

SITE = "https://kevinthibbles.com"
tpl = open(os.path.join(ROOT, "gcms-notes.html"), encoding="utf-8").read()
bwp = open(os.path.join(ROOT, "business-work-permits.html"), encoding="utf-8").read()
times = json.load(open(os.path.join(ROOT, "tracker", "data", "processing-times.json"), encoding="utf-8"))
UPDATED = times.get("updated_temporary", "")

# ---------- shared template pieces ----------
icons = tpl[tpl.index('<link rel="icon"'):tpl.index('<meta name="theme-color"')]
site_css = tpl[tpl.index('<link rel="preconnect"'):tpl.index('</style><script>') + len('</style>')]
theme_js = tpl[tpl.index('</style><script>') + len('</style>'):tpl.index('</head>')]
nav_end = tpl.index('<!-- /mobile-menu -->') + len('<!-- /mobile-menu -->')
nav = tpl[tpl.index('<nav class="nav"'):nav_end]
footer_and_after = tpl[tpl.index('<footer class="footer">'):tpl.index('</body>')]
blog_css = bwp[bwp.index('/* page-specific */'):bwp.index('</style>', bwp.index('/* page-specific */'))]

GULF_CSS = r'''
/* ── Gulf section ── */
.pt { font-variant-numeric: tabular-nums; font-weight: 600; color: var(--ink); white-space: nowrap; }
.who { overflow-x: auto; margin: 1.25rem 0 2rem; border: 1px solid var(--line); border-radius: 12px; background: var(--card); }
.who table { border-collapse: collapse; width: 100%; min-width: 480px; font-size: .94rem; }
.who th, .who td { text-align: left; padding: .8rem 1rem; border-bottom: 1px solid var(--line); vertical-align: top; color: var(--ink-soft); }
.who th { font-family: var(--font-mono); font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: var(--stone); font-weight: 500; }
.who tr:last-child td { border-bottom: 0; }
.who td:first-child { color: var(--ink); font-weight: 600; }
.who .yes { color: var(--maple); font-weight: 600; }
.live-note { font-size: .85rem; color: var(--stone); margin-top: -1.2rem !important; }
.guide-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; margin: 1.5rem 0 2.5rem; }
.guide { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 1.4rem; display: flex; flex-direction: column; gap: .6rem; min-width: 0; transition: border-color var(--transition), transform var(--transition); }
.guide:hover { border-color: var(--maple); transform: translateY(-2px); }
.guide h3 { font-family: var(--font-display); font-weight: 450; font-size: 1.25rem; line-height: 1.25; margin: 0 !important; }
.guide p { font-size: .94rem !important; margin: 0 !important; }
.guide .more { margin-top: auto; font-weight: 600; color: var(--maple); font-size: .9rem; }
.guide.main { border-color: var(--maple); background: var(--maple-tint); }
.checklist li::before { background: transparent !important; border: 2px solid var(--maple); width: 8px !important; height: 8px !important; border-radius: 2px !important; top: .6em !important; }
@media (prefers-reduced-motion: reduce) { .guide { transition: none; } .guide:hover { transform: none; } }
'''

LIVE_JS = r'''<script>
(function(){
  var spans = document.querySelectorAll('[data-pt]'); if(!spans.length) return;
  fetch('/tracker/data/processing-times.json', {cache: 'no-cache'}).then(function(r){ return r.ok ? r.json() : null; }).then(function(d){
    if(!d) return;
    spans.forEach(function(el){
      var k = el.getAttribute('data-pt').split(':'), t = (d.by_country[k[0]] || {})[k[1]];
      el.textContent = (!t || /no processing time|not enough data/i.test(t)) ? 'not published' : t;
    });
    document.querySelectorAll('[data-pt-date]').forEach(function(el){ el.textContent = d.updated_temporary; });
  }).catch(function(){});
})();
</script>
'''


def pt(visa, cc):
    t = times["by_country"].get(visa, {}).get(cc)
    shown = "not published" if (not t or re.search(r"no processing time|not enough data", t, re.I)) else t
    return f'<span class="pt" data-pt="{visa}:{cc}">{shown}</span>'


def fill(s):
    s = re.sub(r"\{\{pt (\w+) (\w\w)\}\}", lambda m: pt(m.group(1), m.group(2)), s)
    return s.replace("{{updated}}", f'<span data-pt-date>{UPDATED}</span>')


def times_table(codes, visas=(("trv", "Visitor visa"), ("super", "Super Visa"), ("study", "Study permit"), ("work", "Work permit"))):
    head = "".join(f"<th>{n}</th>" for _, n in visas)
    rows = "".join(f"<tr><td>{C.COUNTRY_NAMES[c]}</td>" + "".join(f"<td>{pt(v, c)}</td>" for v, _ in visas) + "</tr>" for c in codes)
    return (f'<div class="who"><table><thead><tr><th>Applying from</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="live-note">IRCC published times, updated {{{{updated}}}}. They refresh automatically from my <a href="/tracker/" style="color:var(--maple)">wait-times tracker</a>.</p>')


def nice_date(d):
    y, m, dd = d.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{months[int(m) - 1]} {int(dd)}, {y}"


PERSON = {"@type": "Person", "@id": SITE + "/#kevin", "name": "Kevin Thibbles",
          "jobTitle": "Regulated Canadian Immigration Consultant (RCIC-IRB Class 3)", "identifier": "R713044",
          "memberOf": [{"@type": "Organization", "name": "College of Immigration and Citizenship Consultants"}],
          "url": SITE + "/"}
ORG = {"@type": "ProfessionalService", "@id": SITE + "/#practice", "name": "Kevin Thibbles Immigration Services Inc.",
       "url": SITE + "/", "telephone": "+16479076890", "email": "kthibbles@kevinthibbles.com",
       "address": {"@type": "PostalAddress", "addressLocality": "Pickering", "addressRegion": "ON", "addressCountry": "CA"},
       "areaServed": [{"@type": "Country", "name": n} for n in ["United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Oman", "Bahrain"]]}


def head(p, url, og):
    e = html.escape
    graph = []
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Gulf residents", "item": SITE + "/gulf/"}]
    if p["slug"] != "index":
        crumbs.append({"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url})
        graph.append({"@type": "BlogPosting", "@id": url + "#article", "headline": p["headline"], "description": p["desc"],
                      "image": og, "datePublished": p["date"], "dateModified": p["date"], "inLanguage": "en-CA",
                      "mainEntityOfPage": url, "url": url, "author": {"@id": SITE + "/#kevin"},
                      "publisher": {"@id": SITE + "/#practice"}, "keywords": [t for _, t in p["tags"]],
                      "articleSection": "Gulf residents",
                      "isPartOf": {"@type": "CollectionPage", "@id": SITE + "/gulf/#hub"}})
    else:
        graph.append({"@type": "CollectionPage", "@id": url + "#hub", "name": p["headline"], "description": p["desc"],
                      "url": url, "inLanguage": "en-CA", "author": {"@id": SITE + "/#kevin"},
                      "hasPart": [{"@type": "BlogPosting", "headline": q["headline"], "url": SITE + "/gulf/" + q["slug"] + ".html"}
                                  for q in C.PAGES if q["slug"] != "index"]})
    graph += [PERSON, ORG, {"@type": "BreadcrumbList", "itemListElement": crumbs}]
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in p["faq"]]})
    art = ""
    if p["slug"] != "index":
        art = (f'<meta property="article:published_time" content="{p["date"]}">\n<meta property="article:modified_time" content="{p["date"]}">\n'
               '<meta property="article:author" content="Kevin Thibbles">\n<meta property="article:section" content="Gulf residents">\n'
               + "".join(f'<meta property="article:tag" content="{e(t)}">\n' for _, t in p["tags"]))
    return f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
{icons}<meta name="theme-color" content="#F4F2EC">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<meta name="keywords" content="{e(p["keywords"])}">
<meta name="author" content="Kevin Thibbles, RCIC R713044">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{"website" if p["slug"] == "index" else "article"}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:site_name" content="Kevin Thibbles Immigration Services Inc.">
<meta property="og:locale" content="en_CA">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(p["headline"])}">
{art}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(p["title"])}">
<meta name="twitter:description" content="{e(p["desc"])}">
<meta name="twitter:image" content="{og}">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)}
</script>
{site_css}<style>
{blog_css}
{GULF_CSS}
</style>{theme_js}</head>
<body id="top">

{nav}
'''


def guide_cards(pages, main_slug=None):
    out = []
    for q in pages:
        cls = "guide main" if q["slug"] == main_slug else "guide"
        out.append(f'''      <a class="{cls}" href="/gulf/{q["slug"]}.html">
        <span class="mono-label">{q["kicker"]}</span>
        <h3>{html.escape(q["card_title"])}</h3>
        <p>{html.escape(q["summary"])}</p>
        <span class="more">Read the guide &rarr;</span>
      </a>''')
    return '<div class="guide-grid">\n' + "\n".join(out) + "\n    </div>"


def body(p):
    url_slug = "" if p["slug"] == "index" else p["slug"] + ".html"
    crumb = ('<a href="/">Home</a> &nbsp;/&nbsp; Gulf residents' if p["slug"] == "index"
             else f'<a href="/">Home</a> &nbsp;/&nbsp; <a href="/gulf/">Gulf residents</a> &nbsp;/&nbsp; {html.escape(p["crumb"])}')
    meta = ""
    if p["slug"] != "index":
        meta = f'''    <div class="post-meta">
      <span class="mono-label">By Kevin Thibbles, RCIC</span>
      <span class="mono-label">Published <time datetime="{p["date"]}">{nice_date(p["date"])}</time></span>
      <span class="mono-label">Last reviewed <time datetime="{p["date"]}">{nice_date(p["date"])}</time></span>
      <span class="mono-label">{p["read"]} min read</span>
    </div>
'''
    content = p["body"]
    content = content.replace("{{times_all}}", times_table(C.GULF_CODES))
    content = content.replace("{{guides}}", guide_cards([q for q in C.PAGES if q.get("group") == "guide"], "canada-visitor-visa-uae-residents"))
    content = content.replace("{{countries}}", guide_cards([q for q in C.PAGES if q.get("group") == "country"]))
    for c in C.GULF_CODES:
        content = content.replace("{{times_" + c + "}}", times_table([c]))
    faq = ""
    if p.get("faq"):
        items = "\n".join(f'      <details><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in p["faq"])
        faq = f'\n    <h2 id="faq">Frequently asked questions</h2>\n    <div class="faq">\n{items}\n    </div>\n'
    tags = ""
    if p.get("tags"):
        tl = "\n".join(f'        <li><a href="/insights/#{s}" rel="tag">{t}</a></li>' for s, t in p["tags"])
        tags = f'\n    <nav class="tags" aria-label="Topics">\n      <span class="mono-label">Topics</span>\n      <ul class="tag-list">\n{tl}\n      </ul>\n    </nav>\n'
    srcs = ""
    if p.get("sources"):
        sl = "\n".join(f'        <li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in p["sources"])
        srcs = (f'\n    <div class="sources">\n      <p>This guide is general information based on IRCC\'s published rules as of {nice_date(p["date"])}. '
                f'It isn\'t legal advice and doesn\'t assess any individual case. Rules, fees and processing times change, so please confirm current requirements on IRCC.ca.</p>\n'
                f'      <ul>\n{sl}\n      </ul>\n    </div>\n')
    related = "\n".join(f'      <a href="{h}">{html.escape(t)} <span class="ar">&rarr;</span></a>' for h, t in p.get("related", []))
    cta = f'''
    <div class="cta-band">
      <h2>{p.get("cta_title", "Applying from the Gulf? Let's talk.")}</h2>
      <p>{p.get("cta_text", "A free 15-minute call, no obligation. I'll give you an honest read on your situation before you spend anything, including whether you need help at all.")}</p>
      <div class="btns">
        <a href="/#contact" class="b primary">Send an enquiry</a>
        <a href="https://wa.me/16479076890" class="b ghost" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
'''
    return f'''
<header class="page-hero">
  <div class="wrap">
    <div class="breadcrumb">{crumb}</div>
    <h1 class="page-title">{p["h1"]}<span class="accent">.</span></h1>
    <p class="page-lede">{p["lede"]}</p>
{meta}    <div class="hero-actions">
      <a href="/#contact" class="btn-primary">Send me an enquiry</a>
      <a href="https://wa.me/16479076890" class="btn-ghost" target="_blank" rel="noopener">Message me on WhatsApp</a>
    </div>
  </div>
</header>

<section class="section">
  <article class="wrap prose">
{fill(content)}
{fill(faq)}{cta}{tags}{srcs}
    <div class="related">
{related}
    </div>
  </article>
</section>

'''


def og_image(p, path):
    from PIL import Image, ImageDraw, ImageFont
    S = "/usr/share/fonts/truetype/dejavu/"
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#F4F2EC"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill="#A8001E")
    d.text((80, 78), p["og_kicker"].upper(), font=ImageFont.truetype(S + "DejaVuSansMono.ttf", 24), fill="#5E584C")
    size = 62
    f = ImageFont.truetype(S + "DejaVuSerif-Bold.ttf", size)
    lines = textwrap.wrap(p["og_title"], width=28)
    while len(lines) > 4:
        size -= 6; f = ImageFont.truetype(S + "DejaVuSerif-Bold.ttf", size); lines = textwrap.wrap(p["og_title"], width=int(28 * 62 / size))
    y = 150
    for ln in lines:
        d.text((78, y), ln, font=f, fill="#1C1A17"); y += int(size * 1.3)
    d.rectangle([80, y + 18, 140, y + 22], fill="#A8001E")
    d.line([(80, 520), (1120, 520)], fill="#DDD8CC", width=2)
    d.text((80, 548), "Kevin Thibbles, RCIC", font=ImageFont.truetype(S + "DejaVuSerif-Bold.ttf", 30), fill="#1C1A17")
    t = "R713044 · kevinthibbles.com"; fm = ImageFont.truetype(S + "DejaVuSansMono.ttf", 22)
    d.text((1120 - d.textlength(t, font=fm), 556), t, font=fm, fill="#A8001E")
    im.save(path, optimize=True)


def main():
    os.makedirs(os.path.join(ROOT, "gulf"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "og", "gulf"), exist_ok=True)
    posts = []
    for p in C.PAGES:
        fname = "index.html" if p["slug"] == "index" else p["slug"] + ".html"
        url = SITE + "/gulf/" + ("" if p["slug"] == "index" else fname)
        og_rel = f"og/gulf/{p['slug']}.png"
        og_image(p, os.path.join(ROOT, og_rel))
        page = head(p, url, SITE + "/" + og_rel) + body(p) + footer_and_after + LIVE_JS + "</body>\n</html>\n"
        open(os.path.join(ROOT, "gulf", fname), "w", encoding="utf-8").write(page)
        posts.append({"href": "/gulf/" + ("" if p["slug"] == "index" else fname), "title": p["card_title"],
                      "summary": p["summary"], "date": p["date"], "tags": p["tags"]})
    json.dump(posts, open(os.path.join(ROOT, "scripts", "gulf_posts.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    sm_path = os.path.join(ROOT, "sitemap.xml")
    sm = open(sm_path, encoding="utf-8").read()
    add = ""
    for p in C.PAGES:
        loc = SITE + "/gulf/" + ("" if p["slug"] == "index" else p["slug"] + ".html")
        if f"<loc>{loc}</loc>" not in sm:
            pr = "0.9" if p["slug"] in ("index", "canada-visitor-visa-uae-residents") else "0.8"
            add += f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{p['date']}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{pr}</priority>\n  </url>\n"
    if add:
        open(sm_path, "w", encoding="utf-8").write(sm.replace("</urlset>", add + "</urlset>"))
    print("built", len(C.PAGES), "Gulf pages")


if __name__ == "__main__":
    main()
