"""Wrap each page in content/ with the shared header and footer.

Each content file starts with a few `key: value` lines, then a line with
`---`, then the page's main HTML. Run `python3 build.py` after editing; it
writes the finished pages next to this file, which is what GitHub Pages serves.

In page HTML, `{base}` and `{home}` are the relative path to the site root,
and `{{include name}}` pastes in content/partials/name.html.

The home page is two columns: a menu on the left switches the panel on the
right (assets/js/site.js). Old addresses in REDIRECTS forward to the new ones.
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
<link rel="stylesheet" href="{base}assets/css/layout.css">
<script src="{base}assets/js/site.js" defer></script>
</head>
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

HEADER = """<header class="site-header sticky">
  <div class="wrap">
    <a class="site-name" href="{home}">Shaun Burley</a>
    <p class="site-tagline">I design AI products people can trust.</p>
{nav}  </div>
</header>
"""

SECTIONS = [("About", "about"), ("Case studies", "case-studies"), ("Archive", "archive"), ("Projects", "projects"), ("CV", "cv")]

REDIRECTS = {
    # Addresses from the first draft of the site
    "v2/index.html": "../",
    "about/index.html": "../#about",
    "cv/index.html": "../#cv",
}

REDIRECT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Shaun Burley</title>
<meta http-equiv="refresh" content="0; url={to}">
<link rel="canonical" href="{to}">
</head>
<body><p>This page has moved. <a href="{to}">Go to the new page</a>.</p></body>
</html>
"""


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


def header(meta, home):
    # The home page has its own side menu, so the header only carries
    # section links on inner pages, where they lead back to the home panels.
    if meta.get("nav") == "home":
        nav = '    <a class="header-contact" href="#contact">Get in touch</a>\n'
    else:
        items = "\n".join(
            f'        <li><a href="{home}#{key}">{label}</a></li>' for label, key in SECTIONS
        )
        nav = f'    <nav class="site-nav" aria-label="Main">\n      <ul>\n{items}\n      </ul>\n    </nav>\n'
    return HEADER.format(home=home, nav=nav)


def write(out, html):
    target = ROOT / out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print("wrote", out)


def build():
    for path in sorted(CONTENT.glob("*.html")):
        meta, body = parse(path)
        out = meta["output"]
        base = "../" * out.count("/")
        html = (
            HEAD.format(title=meta["title"], description=meta["description"], base=base)
            + "<body>\n"
            + '<a class="skip-link" href="#main">Skip to content</a>\n'
            + header(meta, base)
            + '<main id="main">\n'
            + include(body).replace("{base}", base).replace("{home}", base)
            + "\n</main>\n"
            + FOOTER.format(email=EMAIL, linkedin=LINKEDIN, github=GITHUB, cv_href=f"{base}#cv")
            + "</body>\n</html>\n"
        )
        write(out, html)
    for out, to in REDIRECTS.items():
        write(out, REDIRECT.format(to=to))


if __name__ == "__main__":
    build()
