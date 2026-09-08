# International Finance — KEDGE Business School

Course slides, written in [Quarto](https://quarto.org) and rendered to reveal.js
(HTML) and beamer (PDF) from the same source.

**📊 Slides: <https://lauradcontreras.github.io/international-finance-kedge/>**

Every push to `main` re-renders the deck and republishes that site.

---

## What's here

```
index.qmd                               course home page (the site's landing page)
01-international-financial-system.qmd   Session 1 — the only file you edit for session 1
theme.scss                              the dark teal theme, shared by every session
_quarto.yml                             site structure and navbar
R/setup.R                               palette, ggplot theme, FRED helper
R/make-cache.R                          run once with internet — see below
data/france-savings.csv                 Problem 1.1
data/france-bop.csv                     Problem 1.2
imgs/                                   drop pictures here
.github/workflows/render.yml            renders and publishes on every push
```

## Working on it

```bash
quarto preview 01-international-financial-system.qmd   # live reload while writing
quarto render                                          # build the whole site into _site/
quarto render 01-international-financial-system.qmd --to revealjs   # just the slides
quarto render 01-international-financial-system.qmd --to beamer     # just the PDF
```

In RStudio or Positron: open the `.qmd` and press **Render** (`Cmd+Shift+K`).

One-time setup:

```bash
brew install --cask quarto
quarto install tinytex          # only needed to build the PDF locally
```

```r
install.packages(c("rmarkdown", "knitr", "ggplot2"))
```

```bash
Rscript R/make-cache.R          # once, with internet — see next section
```

To publish: commit and push. The Action does the rest.

```bash
git add -A && git commit -m "Session 1: fix the J-curve slope" && git push
```

## The three FRED charts

The business-cycle, CPI and euro/dollar slides pull their data from FRED at
render time — no API key, no screenshots, drawn in the deck's own palette.
`R/make-cache.R` downloads them into `cache/` once; every render after that
reads the cache, so the deck also builds on a train. The GitHub Action runs
that script on every build, so the published site always has current data.

`cache/` is gitignored. Until you run the script locally, those three slides
show a "not cached yet" note instead of a chart — the published site will have
them either way.

## Sessions 2–10

Copy `01-international-financial-system.qmd`, rename it `02-...qmd`, and change
the content. It picks up `theme.scss` and `R/setup.R` automatically, and
`_quarto.yml` renders every `.qmd` in the folder — add the new file to the
navbar and to the table in `index.qmd` and it appears on the site.

## The deck's own conventions

| Write this | Get this |
|:---|:---|
| `::: ask` | a clay-coloured question block with a 💬 marker |
| `::: keyidea` | a teal box with a 💡 marker |
| `::: {.imgslot}` | a dashed placeholder — replace it with `![](imgs/file.jpg)` |
| `## Title {.hook}` | a sand-coloured section-opening slide |
| `# Title {.divider .center}` | a full-bleed dark teal section divider |
| `::: incremental` | bullets revealed one at a time |
| `::: panel-tabset` | tabs (used for *Data / Questions / Where to look*) |
| `::: notes` | speaker notes, visible only in speaker view (`S`) |

Colour carries meaning in the figures: teal is the domestic/supply side, clay is
the foreign/deficit/shock side, slate is demand. `R/setup.R` holds the palette —
change `IF_COL` and `theme.scss` together if you ever want a different colour.

## In the room

| Key | Does |
|:--|:--|
| `→` `←` | next / previous slide |
| `C` | draw on the current slide |
| `B` | blank chalkboard |
| `O` | slide overview |
| `S` | speaker view: notes, timer, next slide |
| `F` | fullscreen |
| `E` then print | PDF of the slides as they look on screen |

The poll on the outline slide points at `app.sli.do/event/REPLACE-ME` — put your
own Slido or Mentimeter event URL there, or delete the block. The two YouTube
embeds need wifi; if the room's network is unreliable, set
`embed-resources: true` in the deck's YAML so everything else is inlined.

## Licence

Slides and course material: **CC BY-NC-SA 4.0**. Code (theme, R helpers,
workflow): **MIT**. See [LICENSE](LICENSE).
