"""Wrap each page in content/ with the shared header and footer.

Each content file starts with a few `key: value` lines, then a line with
`---`, then the page's main HTML. Run `python3 build.py` after editing; it
writes the finished pages next to this file, which is what GitHub Pages serves.

In page HTML, `{base}` is the path to the site root (for assets), `{home}` is
the path to the current version's home page (for links between pages), and
`{{include name}}` pastes in content/partials/name.html.

Two versions are built while the redesign is in draft:
- v1, the original site, at the root
- v2, the two-column draft, under v2/
A page lists which versions it belongs to in its `variants:` line (default v1).
"""

from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
PARTIALS = CONTENT / "partials"

EMAIL = "me@shaunburley.com"
LINKEDIN = "https://www.linkedin.com/in/shaunburleyux"
GITHUB = "https://github.com/Shaunathon"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">
<link rel="stylesheet" href="{base}assets/css/site.css">
{extra_head}</head>
"""

FOOTER = """<footer class="site-footer" id="contact">
  <div class="wrap">
    <h2>Get in touch</h2>
    <p>I'm looking for senior product design roles on AI products.</p>
    <ul class="contact-links">
      <li><a href="mailto:{email}">{email}</a></li>
      <li><a href="{linkedin}">LinkedIn</a></li>
      <li><a href="{github}">GitHub</a></li>
      <li><a href="{cv_href}">CV</a></li>
    </ul>
    <small>&copy; 2026 Shaun Burley</small>
  </div>
</footer>
"""

V1_HEADER = """<header class="site-header">
  <div class="wrap">
    <a class="site-name" href="{home}">Shaun Burley</a>
    <nav class="site-nav" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>
"""

V2_HEADER = """<header class="site-header sticky">
  <div class="wrap">
    <a class="site-name" href="{home}">Shaun Burley</a>
    <p class="site-tagline">I design AI products people can trust.</p>
{nav}  </div>
</header>
"""

V1_NAV = [("Work", "index.html#work", "work"), ("About", "about/", "about"), ("CV", "cv/", "cv")]
V2_SECTIONS = [("About", "about"), ("Case studies", "case-studies"), ("Archive", "archive"), ("Projects", "projects"), ("CV", "cv")]

VARIANTS = {
    "v1": {"prefix": "", "extra_head": ""},
    "v2": {"prefix": "v2/", "extra_head": '<link rel="stylesheet" href="{base}assets/css/v2.css">\n<script src="{base}assets/js/v2.js" defer></script>\n'},
}


def parse(path):
    head, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    return meta, body.strip("\n")


def include(body):
    while "{{include " in body:
        start = body.index("{{include ")
        end = body.index("}}", start)
        name = body[start + 10:end].strip()
        body = body[:start] + (PARTIALS / f"{name}.html").read_text(encoding="utf-8").strip("\n") + body[end + 2:]
    return body


def header(variant, meta, home):
    if variant == "v1":
        nav = "\n".join(
            '        <li><a href="{}{}"{}>{}</a></li>'.format(
                home, href, ' aria-current="page"' if meta.get("nav") == key else "", label
            )
            for label, href, key in V1_NAV
        )
        return V1_HEADER.format(home=home, nav=nav)
    # v2: the home page has its own side menu, so the header only carries
    # section links on inner pages, where they lead back to the home panels.
    if meta.get("nav") == "home":
        nav = '    <a class="header-contact" href="#contact">Get in touch</a>\n'
    else:
        items = "\n".join(
            f'        <li><a href="{home}#{key}">{label}</a></li>' for label, key in V2_SECTIONS
        )
        nav = f'    <nav class="site-nav" aria-label="Main">\n      <ul>\n{items}\n      </ul>\n    </nav>\n'
    return V2_HEADER.format(home=home, nav=nav)


def build():
    for path in sorted(CONTENT.glob("*.html")):
        meta, body = parse(path)
        for variant in meta.get("variants", "v1").split():
            out = VARIANTS[variant]["prefix"] + meta["output"]
            base = "../" * out.count("/")
            home = base + VARIANTS[variant]["prefix"]
            cv_href = f"{home}#cv" if variant == "v2" else f"{home}cv/"
            html = (
                HEAD.format(
                    title=meta["title"],
                    description=meta["description"],
                    base=base,
                    extra_head=VARIANTS[variant]["extra_head"].format(base=base),
                )
                + "<body>\n"
                + '<a class="skip-link" href="#main">Skip to content</a>\n'
                + header(variant, meta, home)
                + '<main id="main">\n'
                + include(body).replace("{base}", base).replace("{home}", home)
                + "\n</main>\n"
                + FOOTER.format(email=EMAIL, linkedin=LINKEDIN, github=GITHUB, cv_href=cv_href)
                + "</body>\n</html>\n"
            )
            target = ROOT / out
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding="utf-8")
            print("wrote", out)


if __name__ == "__main__":
    build()
