"""Wrap each page in content/ with the shared header and footer.

Each content file starts with a few `key: value` lines, then a line with
`---`, then the page's main HTML. Run `python3 build.py` after editing; it
writes the finished pages next to this file, which is what GitHub Pages serves.
"""

from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"

EMAIL = "me@shaunburley.com"
LINKEDIN = "https://www.linkedin.com/in/shaunburleyux"
GITHUB = "https://github.com/Shaunathon"

NAV = [("Work", "index.html#work", "work"), ("About", "about/", "about"), ("CV", "cv/", "cv")]

LAYOUT = """<!doctype html>
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
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="site-name" href="{base}">Shaun Burley</a>
    <nav class="site-nav" aria-label="Main">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer" id="contact">
  <div class="wrap">
    <h2>Get in touch</h2>
    <p>I'm looking for senior product design roles on AI products.</p>
    <ul class="contact-links">
      <li><a href="mailto:{email}">{email}</a></li>
      <li><a href="{linkedin}">LinkedIn</a></li>
      <li><a href="{github}">GitHub</a></li>
      <li><a href="{base}cv/">CV</a></li>
    </ul>
    <small>&copy; 2026 Shaun Burley</small>
  </div>
</footer>
</body>
</html>
"""


def parse(path):
    head, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    return meta, body.strip("\n")


def build():
    for path in sorted(CONTENT.glob("*.html")):
        meta, body = parse(path)
        out = meta["output"]
        depth = out.count("/")
        base = "../" * depth
        nav = "\n".join(
            '        <li><a href="{}{}"{}>{}</a></li>'.format(
                base, href, ' aria-current="page"' if meta.get("nav") == key else "", label
            )
            for label, href, key in NAV
        )
        html = LAYOUT.format(
            title=meta["title"],
            description=meta["description"],
            base=base,
            nav=nav,
            body=body.replace("{base}", base),
            email=EMAIL,
            linkedin=LINKEDIN,
            github=GITHUB,
        )
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print("wrote", out)


if __name__ == "__main__":
    build()
