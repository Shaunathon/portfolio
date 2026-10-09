"""Build the site from the plain text files in text/.

All the words on the site live in text/ as Markdown files (see text/README.md).
Each file starts with a few `key: value` lines, then a line with `---`, then
the text. Lines starting with `#` before the `---` are notes and never appear.

Run `python3 build.py` after editing (it needs `pip install markdown`). It
writes the finished pages next to this file, which is what GitHub Pages serves.
Layout lives here and in assets/; text/ holds only words and image choices.
"""

import html
import re
from pathlib import Path

import markdown
from PIL import Image

ROOT = Path(__file__).parent
TEXT = ROOT / "text"
IMG = ROOT / "assets" / "img"

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


# Reading text files

def read(path):
    head, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = {}
    for line in head.splitlines():
        if line.strip() and not line.startswith("#"):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, blocks(body)


def blocks(body):
    """Split Markdown into blocks at blank lines, keeping each list whole."""
    out = []
    for chunk in re.split(r"\n\s*\n", body.strip()):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        if out and is_list(chunk) and is_list(out[-1]) and chunk[0] == out[-1][0]:
            out[-1] += "\n" + chunk
        else:
            out.append(chunk)
    return out


def is_list(block):
    return bool(re.match(r"(- |\* |\d+\. )", block))


def kind(block):
    if block.startswith("### "):
        return "h3"
    if block.startswith("## "):
        return "h2"
    if block.startswith("!["):
        return "figure"
    if re.fullmatch(r"(\s*\[[^\]]+\]\([^)]+\)\{[^}]*\.button[^}]*\})+\s*", block):
        return "buttons"
    return "text"


# Turning Markdown into HTML

def md(text, base):
    out = markdown.markdown(text, extensions=["attr_list"])
    return fix_links(out, base)


def inline(text, base):
    return re.sub(r"^<p>|</p>$", "", md(text, base))


def fix_links(out, base):
    # Links in text/ are written from the site root ("work/x/"); images are
    # file names in assets/img. Point both at the right place from each page.
    def href(m):
        url = m.group(2)
        if re.match(r"[a-z]+:|#|/", url):
            return m.group(0)
        return f'{m.group(1)}="{base}{url}"'

    out = re.sub(r'(href)="([^"]*)"', href, out)
    out = re.sub(r'src="([^"/:]+)"', lambda m: f'src="{base}assets/img/{m.group(1)}"', out)
    return out


def heading(block):
    # Escape "1. " so a numbered heading isn't read as a list.
    return re.sub(r"^(\d+)\. ", r"\1\\. ", re.sub(r"^#+\s*", "", block))


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-")


class Figures:
    """Turns an image line plus its caption line into a figure."""

    def __init__(self):
        self.count = 0

    def __call__(self, block, base):
        image, _, caption = block.partition("\n")
        m = re.match(r"!\[(.*)\]\(([^)]+)\)(?:\{([^}]*)\})?$", image.strip())
        alt, name, attrs = m.group(1), m.group(2), m.group(3) or ""
        classes = re.findall(r"\.([\w-]+)", attrs)
        width, height = Image.open(IMG / name).size
        lazy = ' loading="lazy"' if self.count else ""
        self.count += 1
        size = " ".join(c for c in classes if c in ("wide", "tall", "small"))
        frame = "frame scroll-x" if "scroll" in classes else "frame"
        fig_class = f' class="{size}"' if size else ""
        caption_html = f"\n  <figcaption>{inline(caption.strip(), base)}</figcaption>" if caption.strip() else ""
        return (
            f'<figure{fig_class}>\n'
            f'  <div class="{frame}"><img src="{base}assets/img/{name}" alt="{html.escape(alt)}" width="{width}" height="{height}"{lazy}></div>'
            f'{caption_html}\n</figure>'
        )


def tradeoff(out):
    return out.replace("<p><strong>Tradeoff:</strong>", '<p class="tradeoff"><strong>Tradeoff:</strong>')


# Shared page parts

def head(title, description, base):
    t, d = html.escape(title), html.escape(description)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
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


def page(site, sections, title, description, base, main, home=False):
    if home:
        # The home page has its own side menu, so the header only carries
        # section links on inner pages, where they lead back to the panels.
        nav = '    <a class="header-contact" href="#contact">Get in touch</a>\n'
    else:
        items = "\n".join(f'        <li><a href="{base}#{key}">{label}</a></li>' for key, label in sections)
        nav = f'    <nav class="site-nav" aria-label="Main">\n      <ul>\n{items}\n      </ul>\n    </nav>\n'
    return (
        head(title, description, base)
        + "<body>\n"
        + '<a class="skip-link" href="#main">Skip to content</a>\n'
        + f"""<header class="site-header sticky">
  <div class="wrap">
    <a class="site-name" href="{base or './'}">{site['name']}</a>
    <p class="site-tagline">{site['tagline']}</p>
{nav}  </div>
</header>
"""
        + '<main id="main">\n'
        + main
        + "\n</main>\n"
        + f"""<footer class="site-footer" id="contact">
  <div class="wrap">
    <h2>{site['footer heading']}</h2>
    <p>{site['footer text']}</p>
    <ul class="contact-links">
      <li><a href="mailto:{site['email']}">{site['email']}</a></li>
      <li><a href="{site['linkedin']}">LinkedIn</a></li>
      <li><a href="{site['github']}">GitHub</a></li>
      <li><a href="{base}#cv">CV</a></li>
    </ul>
    <small>&copy; 2026 {site['name']}</small>
  </div>
</footer>
</body>
</html>
"""
    )


# Home page panels

BLANK = "\n\n"


def about(meta, body, base):
    # Plain text goes in prose blocks; each run of ### headings becomes a
    # row of principle cards, and a ## heading after them starts prose again.
    parts = [["prose"]]
    for block in body:
        k = kind(block)
        if k == "h3":
            if parts[-1][0] != "cards":
                parts.append(["cards"])
            parts[-1].append([heading(block)])
        elif parts[-1][0] == "cards" and k != "h2":
            parts[-1][-1].append(block)
        else:
            if parts[-1][0] != "prose":
                parts.append(["prose"])
            parts[-1].append(block)
    out = [f'<h1 id="about-h" tabindex="-1">{meta["headline"]}</h1>', f'<p class="lede">{meta["lede"]}</p>']
    for part in parts:
        if part[0] == "prose" and len(part) > 1:
            prose = md(BLANK.join(part[1:]), base).replace("<ul>", '<ul class="about-list">')
            out.append(f'<div class="prose">\n{prose}\n</div>')
        elif part[0] == "cards":
            items = "\n".join(
                f'  <li>\n    <h3>{inline(c[0], base)}</h3>\n    {md(BLANK.join(c[1:]), base)}\n  </li>' for c in part[1:]
            )
            out.append(f'<ol class="principles">\n{items}\n</ol>')
    return "\n".join(out)


def groups(body):
    """Split blocks into (text before the first ## heading, [(heading, blocks)])."""
    intro, out = [], []
    for block in body:
        if kind(block) == "h2":
            out.append((heading(block), []))
        elif out:
            out[-1][1].append(block)
        else:
            intro.append(block)
    return intro, out


def link_parts(title):
    m = re.fullmatch(r"\[(.+)\]\((.+)\)", title)
    return (m.group(1), m.group(2)) if m else (title, None)


def case_list(meta, body, base):
    _, items = groups(body)
    rows = []
    for title, parts in items:
        name, url = link_parts(title)
        img = next((p for p in parts if kind(p) == "figure"), None)
        parts = [p for p in parts if kind(p) != "figure"]
        meta_line = inline(parts[0], base) if parts else ""
        desc = inline("\n\n".join(parts[1:]), base) if len(parts) > 1 else ""
        href = fix_links(f'href="{url}"', base)
        img_html = ""
        if img:
            file = re.search(r"\]\(([^)]+)\)", img).group(1)
            w, h = Image.open(IMG / file).size
            img_html = f'      <img class="case-thumb" src="{base}assets/img/{file}" alt="" width="{w}" height="{h}" loading="lazy">\n'
        rows.append(
            f'  <li>\n    <a {href}{" class=\"has-thumb\"" if img else ""}>\n{img_html}'
            f'      <span class="case-meta">{meta_line}</span>\n'
            f'      <span class="case-title">{inline(name, base)}</span>\n'
            f'      <span class="case-desc">{desc}</span>\n'
            f'      <span class="case-arrow" aria-hidden="true">&rarr;</span>\n    </a>\n  </li>'
        )
    return f'<h2 id="{{id}}-h" tabindex="-1">{meta["title"]}</h2>\n<ol class="case-list">\n' + "\n".join(rows) + "\n</ol>"


def archive(meta, body, base):
    text = md("\n\n".join(body), base)
    return f'<h2 id="{{id}}-h" tabindex="-1">{meta["title"]}</h2>\n<div class="empty-state prose">\n{text}\n</div>'


def projects(meta, body, base):
    intro, items = groups(body)
    cards = []
    for title, parts in items:
        name, url = link_parts(title)
        img = next((p for p in parts if kind(p) == "figure"), None)
        text = [p for p in parts if kind(p) != "figure"]
        img_html = ""
        if img:
            file = re.search(r"\]\(([^)]+)\)", img).group(1)
            w, h = Image.open(IMG / file).size
            img_html = f'    <img src="{base}assets/img/{file}" alt="" width="{w}" height="{h}" loading="lazy">\n'
        paras = [f"    <p>{inline(text[0], base)}</p>"] if text else []
        paras += [f'    <p class="project-links">{inline(t, base)}</p>' for t in text[1:]]
        head_html = f'<a href="{url}">{name}</a>' if url else name
        cards.append(
            f'  <li class="project">\n{img_html}    <h3>{fix_links(head_html, base)}</h3>\n' + "\n".join(paras) + "\n  </li>"
        )
    intro_html = "".join(f'<p class="prose">{inline(b, base)}</p>\n' for b in intro)
    return (
        f'<h2 id="{{id}}-h" tabindex="-1">{meta["title"]}</h2>\n{intro_html}'
        f'<ul class="project-grid">\n' + "\n".join(cards) + "\n</ul>"
    )


def cv(meta, body, base, site):
    out, after_h3 = [], False
    for block in body:
        k = kind(block)
        rendered = md(block, base)
        if after_h3 and k == "text" and not is_list(block):
            rendered = rendered.replace("<p>", '<p class="role-meta">', 1)
        out.append(rendered)
        after_h3 = k == "h3"
    return (
        f'<h2 id="{{id}}-h" class="panel-title" tabindex="-1">{meta["title"]}</h2>\n'
        f'<div class="print-only">\n  <p class="cv-name">{site["name"]}</p>\n  <p class="role-meta">{meta.get("print line", "")}</p>\n</div>\n'
        f'<p class="no-print"><a class="button" href="{base}assets/Shaun-Burley-CV.pdf">Download PDF</a></p>\n'
        f'<div class="prose">\n' + "\n".join(out) + "\n</div>"
    )


PANELS = {"about": about, "case-studies": case_list, "archive": archive, "projects": projects, "cv": cv}


def panel_files():
    for path in sorted((TEXT / "home").glob("*.md")):
        key = re.sub(r"^\d+-", "", path.stem)
        meta, body = read(path)
        yield key, meta, body


def build_home(site, sections):
    menu, panels = [], []
    for key, meta, body in panel_files():
        menu.append(f'      <li><a href="#{key}" data-panel="{key}">{meta["menu label"]}</a></li>')
        maker = PANELS[key]
        inner = maker(meta, body, "", site) if key == "cv" else maker(meta, body, "")
        cls = "panel cv" if key == "cv" else "panel"
        panels.append(
            f'    <section class="{cls}" id="{key}" aria-labelledby="{key}-h">\n{inner.replace("{id}", key)}\n    </section>'
        )
    main = (
        '<div class="wrap split">\n  <nav class="side" aria-label="Sections">\n    <ul>\n'
        + "\n".join(menu)
        + "\n    </ul>\n  </nav>\n\n  <div class=\"panels\">\n"
        + "\n\n".join(panels)
        + "\n  </div>\n</div>"
    )
    return page(site, sections, site["home tab title"], site["home description"], "", main, home=True)


# Case study pages

def build_case(site, sections, meta, body, base):
    figure = Figures()
    facts = "\n".join(
        f"      <div><dt>{k}</dt><dd>{inline(v, base)}</dd></div>" for k, v in meta.items() if k[:1].isupper()
    )
    out, prose, decision = [], [], None

    def flush():
        nonlocal prose, decision
        if decision is not None:
            out.append('<div class="decision prose">\n' + tradeoff("\n".join(decision)) + "\n</div>")
        elif prose:
            out.append('<div class="prose">\n' + tradeoff("\n".join(prose)) + "\n</div>")
        prose, decision = [], None

    for block in body:
        k = kind(block)
        if k == "figure":
            flush()
            out.append(figure(block, base))
        elif k == "buttons":
            flush()
            out.append('<div class="links-row">\n' + inline(block, base) + "\n</div>")
        elif k == "h2":
            flush()
            text = heading(block)
            prose.append(f'<h2 id="{slug(text)}">{inline(text, base)}</h2>')
        elif k == "h3":
            flush()
            decision = [f"<h3>{inline(heading(block), base)}</h3>"]
        elif decision is not None:
            decision.append(md(block, base))
        else:
            prose.append(md(block, base))
    flush()

    nxt = ""
    if meta.get("next link"):
        nxt = (
            '    <nav class="next-case" aria-label="Next case study">\n'
            '      <p class="eyebrow">Next case study</p>\n'
            f'      <a href="{base}{meta["next link"]}">{meta["next title"]}</a>\n    </nav>\n'
        )
    main = f"""<div class="wrap">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="{base}">Home</a></li>
      <li><a href="{base}#case-studies">Case studies</a></li>
      <li aria-current="page">{meta['short title']}</li>
    </ol>
  </nav>

  <header class="case-header">
    <p class="eyebrow">{meta['eyebrow']}</p>
    <h1>{meta['title']}</h1>
    <dl class="facts">
{facts}
    </dl>
  </header>

  <div class="case-body">
""" + "\n".join(out) + "\n" + nxt + "  </div>\n</div>"
    return page(site, sections, meta["tab title"], meta["description"], base, main)


# Writing pages

def write(out, text):
    target = ROOT / out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print("wrote", out)


def build():
    site, _ = read(TEXT / "site.md")
    sections = [(key, meta["menu label"]) for key, meta, _ in panel_files()]
    write("index.html", build_home(site, sections))
    for path in sorted((TEXT / "case-studies").glob("*.md")):
        meta, body = read(path)
        write(f"work/{path.stem}/index.html", build_case(site, sections, meta, body, "../../"))
    for out, to in REDIRECTS.items():
        write(out, REDIRECT.format(to=to))


if __name__ == "__main__":
    build()
