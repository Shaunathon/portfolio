# Editing the words on shaunburley.com

Every word on the site is in these files. Open any of them in a text editor (TextEdit works; set it to plain text), change the words, save, then tell Claude **"publish my site text"**.

| File | What it holds |
| --- | --- |
| `site.md` | Header, footer, contact links, and the home page's title in browser tabs and link previews |
| `home/1-about.md` | The About panel: headline, intro, 2024 to now, and the five principles |
| `home/2-case-studies.md` | The list of case studies |
| `home/3-archive.md` | The Archive panel |
| `home/4-projects.md` | The AI-assisted projects grid |
| `home/5-cv.md` | The CV panel (the PDF is remade from it when you publish) |
| `case-studies/designing-for-uncertainty.md` | The AI assistant case study |
| `case-studies/turkish-transcriber.md` | The transcriber case study |

## How the files work

- **The top of each file** has short `name: value` lines, such as the headline or the page title, and ends at a line with `---`. Change the words after the colon; leave the name before it alone.
- **Lines starting with `#` above the `---`** are notes for you. They never appear on the site.
- **Below the `---`** is the page text, written in Markdown:
  - A blank line starts a new paragraph.
  - `## Heading` makes a section heading; `### Heading` a smaller one (a principle, a key decision, a job).
  - `**bold**` for bold, `*italic*` for italic.
  - `- ` at the start of a line makes a bullet. Keep a list's bullets on consecutive lines.
  - `[link text](https://address)` makes a link. Links to your own pages leave off the domain, like `[case study](work/turkish-transcriber/)`.
- **Images** are one line, `![description for screen readers](file-name.webp)`, with the caption on the line right under it. Image files live in `assets/img` in the site's code; to use a new image, put it next to these files and tell Claude.

You can add a new case study by copying one of the files in `case-studies/` and giving it a new name; its file name becomes its web address. Add it to `home/2-case-studies.md` too so people can find it.

## Where these files live

The originals are in the site's code on GitHub (the `text` folder of Shaunathon/portfolio). The copy in your Documents folder is the one you edit. When you say "publish my site text", Claude copies your edits into the code, rebuilds the site and puts it live. If Claude changes site text for you another way, it updates your copy too.
