# shaunburley.com

Portfolio site for Shaun Burley, product designer. Plain HTML, CSS and a little JavaScript, served by GitHub Pages.

## Editing

Page copy lives in `content/` (the home page and its panels are `content/home.html`; text shared by several pages is in `content/partials/`). Each file has a few header lines, a `---` line, then the page's HTML.
After editing, run:

```
python3 build.py
```

That rewrites the finished pages (`index.html` and `work/`) with the shared header and footer.
Images are in `assets/img/`, styles in `assets/css/` (`site.css` for type and pages, `layout.css` for the sticky header and two columns), and the panel switching in `assets/js/site.js`.
