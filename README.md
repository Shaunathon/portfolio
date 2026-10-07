# shaunburley.com

Portfolio site for Shaun Burley, senior product designer. Plain HTML and CSS, served by GitHub Pages.

## Editing

Page copy lives in `content/`. Each file has a few header lines, a `---` line, then the page's HTML.
After editing, run:

```
python3 build.py
```

That rewrites the finished pages (`index.html`, `about/`, `cv/`, `work/`) with the shared header and footer.
Images are in `assets/img/`, styles in `assets/css/site.css`.
