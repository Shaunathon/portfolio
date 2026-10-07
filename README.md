# shaunburley.com

Portfolio site for Shaun Burley, product designer. Plain HTML, CSS and a little JavaScript, served by GitHub Pages.

## Editing

All the words are in `text/` as Markdown files; `text/README.md` explains the format. Layout and styling live in `build.py` and `assets/`.
After editing, run:

```
pip install markdown pillow   # once
python3 build.py
```

That rewrites the finished pages (`index.html` and `work/`). If the CV text changed, also remake the PDF: serve the site with `python3 -m http.server 8765` and run `node tools/cv-pdf.js`.
Images are in `assets/img/`, styles in `assets/css/` (`site.css` for type and pages, `layout.css` for the sticky header and two columns), and the panel switching in `assets/js/site.js`.

Shaun edits a copy of `text/` in `~/Documents/Portfolio site text/` on his Mac. To publish, copy that folder over `text/` (except `README.md`), build, and push.
