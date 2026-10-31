"""Phone and tablet improvements shared by every page on kevinthibbles.com.

Safe to run more than once: each page is checked for the markers below before anything is added.
Run from the repository root:  python3 scripts/responsive_patch.py
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTICLE_PAGES = ["visitor-visa-refused.html", "gcms-notes.html", "super-visa.html", "study-permit-refused.html",
                 "business-work-permits.html", "insights/index.html"]
HOME = "index.html"

CSS = """<style id="responsive">
/* ── Phone and tablet layer (scripts/responsive_patch.py) ── */
/* Menu: switch to the menu button below 900px so tablets in portrait don't get a cramped link row */
@media (max-width: 900px) {
  .nav-links, .nav-cta { display: none !important; }
  .nav-mobile-btn { display: flex !important; }
}
.nav-mobile-btn { min-width: 44px; min-height: 44px; align-items: center; justify-content: center; border-radius: 8px; }
.nav-mobile-btn span { transform-origin: center; }
.nav-mobile-btn[aria-expanded="true"] span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.nav-mobile-btn[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
.nav-mobile-btn[aria-expanded="true"] span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
.mobile-menu { overflow-y: auto; padding-bottom: calc(2rem + env(safe-area-inset-bottom, 0px)); }
.mobile-menu a { min-height: 48px; display: flex; align-items: center; }
.mobile-menu .mm-cta { margin-top: 1.5rem; justify-content: center; border: 0; border-radius: 99px;
  background: var(--ink); color: var(--paper); font-family: var(--font-body); font-size: 1rem; font-weight: 600; padding: 1rem 1.5rem; }
.mobile-menu .mm-cta:hover { background: var(--maple); }
body.menu-open { overflow: hidden; }
body.menu-open .tracker-float, body.menu-open .wa-float { display: none; }

/* Touch screens: bigger tap targets everywhere */
@media (pointer: coarse) {
  .nav-links a { padding: .8rem .2rem; }
  .theme-toggle { width: 44px; height: 44px; }
  .breadcrumb a { display: inline-block; padding: .55rem 0; }
  .related a { padding: 1.05rem 0; }
  .footer-links a { padding: .35rem 0; }
  .text-link { display: inline-block; padding: .35rem 0; }
}

/* Headlines: drop desktop-only line breaks and balance the lines on smaller screens */
.page-title, .hero-title, .section-title { text-wrap: balance; }
@media (max-width: 768px) { .page-title br, .hero-title br { display: none; } }

/* Tablet portrait: the full-height hero leaves large empty space, so let content set the height */
@media (max-width: 1024px) and (orientation: portrait) {
  .hero { min-height: auto; padding-top: 9rem; padding-bottom: 5rem; }
}

/* Keep the floating buttons clear of the iPhone home bar and leave room for them at the end of the page */
.tracker-float, .wa-float { margin-bottom: env(safe-area-inset-bottom, 0px); }
@media (max-width: 1024px) { body { padding-bottom: 5.5rem; } }

/* Phones: a little more room for text, and 16px form fields so iOS doesn't zoom in when you tap them */
@media (max-width: 420px) { .wrap { padding-left: 1.25rem; padding-right: 1.25rem; } }
@media (max-width: 900px) { input, select, textarea { font-size: 16px !important; } }

/* Wide content scrolls inside its own box instead of pushing the page sideways */
img, svg, video { max-width: 100%; }
.prose table { display: block; overflow-x: auto; }
</style>
"""

JS = """<script id="responsive-menu">
(function () {
  var btn = document.getElementById('mobileBtn'), menu = document.getElementById('mobileMenu');
  if (!btn || !menu) return;
  function set(open) {
    menu.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  btn.addEventListener('click', function () { set(!menu.classList.contains('open')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('open')) { set(false); btn.focus(); } });
  window.addEventListener('resize', function () { if (window.innerWidth > 900) set(false); });
  window.closeMobile = function () { set(false); };
})();
</script>
"""

THEME_BTN = re.compile(r'<button class="theme-toggle" data-theme-toggle[\s\S]*?</button>')
HAMBURGER = ('<button class="nav-mobile-btn" id="mobileBtn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">\n'
             '        <span></span><span></span><span></span>\n      </button>')


def article_menu(theme_btn):
    links = [("/", "Home"), ("/#about", "About"), ("/#services", "Services"), ("/#process", "Process"),
             ("/tracker/", "Visa wait times"), ("/insights/", "Insights"), ("/#contact", "Contact")]
    a = "\n".join(f'  <a href="{h}">{t}</a>' for h, t in links)
    return (f'\n<!-- ── MOBILE MENU ── -->\n<div class="mobile-menu" id="mobileMenu">\n{a}\n'
            f'  <a href="/#contact" class="mm-cta">Book free call</a>\n  {theme_btn}\n</div>\n<!-- /mobile-menu -->\n')


def patch(path, is_home):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    orig = s
    if 'id="responsive"' not in s:
        s = s.replace("</head>", CSS + "</head>", 1)
    s = s.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">', 1)
    if is_home:
        s = s.replace('<button class="nav-mobile-btn" id="mobileBtn" aria-label="Open menu">',
                      '<button class="nav-mobile-btn" id="mobileBtn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">', 1)
        if 'class="mm-cta"' not in s:
            s = s.replace('  <a href="#contact" onclick="closeMobile()">Contact</a>\n',
                          '  <a href="#contact" onclick="closeMobile()">Contact</a>\n'
                          '  <a href="#contact" class="mm-cta" onclick="closeMobile()">Book free call</a>\n', 1)
        # the shared script below replaces the old open/close handler
        s = s.replace("document.getElementById('mobileBtn').addEventListener('click', () => {\n"
                      "  document.getElementById('mobileMenu').classList.toggle('open');\n});\n"
                      "function closeMobile() { document.getElementById('mobileMenu').classList.remove('open'); }\n", "", 1)
    else:
        if 'id="mobileBtn"' not in s:
            nav_end = s.index('</nav>')
            cta = s.index('class="nav-cta"', s.index('<nav class="nav"'))
            cta_end = s.index('</a>', cta) + len('</a>')
            s = s[:cta_end] + "\n      " + HAMBURGER + s[cta_end:]
            nav_end = s.index('</nav>') + len('</nav>')
            theme_btn = THEME_BTN.search(s).group(0)
            s = s[:nav_end] + "\n" + article_menu(theme_btn) + s[nav_end:]
    # keep a space before forced headline line breaks, so words stay apart when phones hide the breaks
    s = re.sub(r'(<h1[^>]*class="[^"]*(?:page-title|hero-title)[^"]*"[^>]*>)([\s\S]*?)(</h1>)',
               lambda m: m.group(1) + re.sub(r'(\S)<br>', r'\1 <br>', m.group(2)) + m.group(3), s)
    if 'id="responsive-menu"' not in s:
        s = s.replace("</body>", JS + "</body>", 1)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        print("patched", path)


if __name__ == "__main__":
    patch(HOME, True)
    for f in ARTICLE_PAGES:
        if (ROOT / f).exists():
            patch(f, False)
