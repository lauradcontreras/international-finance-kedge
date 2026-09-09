# Working on the slides — the whole loop

## The commands

Run all of these from the project folder:

```bash
cd ~/Documents/GitHub/international-finance
```

| # | Step | Command | What it does |
|:--:|:---|:---|:---|
| 1 | **Edit** | open `01-international-financial-system.qmd` | The only file with slide content. RStudio, Positron or any text editor. |
| 2 | **Write live** | `quarto preview 01-international-financial-system.qmd` | Opens the deck in your browser and re-renders on every save. Leave it running while you work. `Ctrl+C` to stop. |
| 3 | **Build the slides** | `quarto render 01-international-financial-system.qmd --to revealjs` | Produces `_site/01-international-financial-system.html`. This is the file you present from. |
| 4 | **Build the handout** | `quarto render 01-international-financial-system.qmd --to beamer` | Produces the PDF. Needs LaTeX — run `quarto install tinytex` once if it fails. |
| 5 | **Build everything** | `quarto render` | Renders the home page *and* the deck, both formats, into `_site/`. Fails if you have no LaTeX; use step 3 instead. |
| 6 | **Present** | open `_site/01-international-financial-system.html` | Double-click it. Works offline except the two YouTube embeds and the poll. |
| 7 | **Refresh the data** | `rm cache/*.csv` then re-render | Re-downloads the three FRED series. Do this before a new term so the charts are current. |
| 8 | **Save a version** | `git add -A`<br>`git commit -m "what changed"` | Records a snapshot you can go back to. |
| 9 | **Publish** | `git push` | Sends it to GitHub; the Action rebuilds the public site for students. |

## Which file does what

| File | Holds | Edit it when |
|:---|:---|:---|
| `01-international-financial-system.qmd` | All slide content: text, chunks, tables | Always — this is the deck |
| `theme.scss` | Colours, type sizes, callout boxes, dividers | You want it to *look* different |
| `R/setup.R` | Chart palette, ggplot theme, the FRED helper | You want the *figures* to look different |
| `index.qmd` | The course home page students land on | You add a session or change a reading |
| `_quarto.yml` | Site structure, navbar | You add a new session file |
| `data/*.csv` | The France tables in Problems 1.1 and 1.2 | The numbers change |
| `_site/` | **Generated output** | Never — it is overwritten on every render |

## Writing slides

| You write | You get |
|:---|:---|
| `## Title` | A new slide |
| `## Title {.hook}` | A sand-coloured section-opening slide |
| `# Title {.divider .center}` | A full-bleed dark teal section divider |
| `::: ask` … `:::` | Clay question box with a 💬 marker |
| `::: keyidea` … `:::` | Teal box with a 💡 marker |
| `::: incremental` … `:::` | Bullets revealed one at a time |
| `. . .` | A pause — everything after it appears on the next click |
| `::: panel-tabset` + `### Tab` | Tabs inside one slide |
| `::: notes` … `:::` | Speaker notes, visible only in speaker view |
| `:::: columns` + `::: {.column width="50%"}` | Two columns |
| `![](imgs/photo.jpg)` | An image — put the file in `imgs/` first |

## In the room

| Key | Does |
|:--:|:---|
| `→` `←` | Next / previous slide |
| `C` | Draw on the slide |
| `B` | Blank chalkboard |
| `O` | Slide overview |
| `S` | Speaker view — notes, timer, next slide |
| `F` | Fullscreen |
| `E` then print | PDF of the slides as they look on screen |

## Three things that will bite you

**No emoji in the `.qmd`.** They pass into the LaTeX pipeline and break the render — this is what stopped it building on 9 September. The 💬 and 💡 markers are safe because they come from CSS, not from the text.

**Figures re-run on every render.** Fourteen ggplot chunks take a few seconds. It is not frozen.

**`cache/` never refreshes itself.** The FRED charts keep showing the data from the day you first rendered until you delete those CSVs.
