# International Finance :bank:

Hi! Welcome to the International Finance course website :wave:

:closed_book: This is a course for [KEDGE Business School](https://kedge.edu/). We build a set of operational models of how international financial markets work — and then spend most of our time on where they break.

:link: **[Course website](https://lauradcontreras.github.io/international-finance-kedge/)** — slides, handouts and readings in one place.

:paperclip: [Syllabus](http://learn.kedgebs.com) *(replace with the direct link)*

:calendar: [Calendar](http://learn.kedgebs.com) *(replace with the direct link)*

:loudspeaker: [Announcements](announcements.md)

:computer: Course description and materials on [LEARN](http://learn.kedgebs.com)

---

:clipboard: **Slides below:**

- [Session 1: The international financial system](https://lauradcontreras.github.io/international-finance-kedge/01-international-financial-system.html) [[pdf](https://lauradcontreras.github.io/international-finance-kedge/01-international-financial-system.pdf)]

- Session 2: The international financial system, continued *(to come)*

- Session 3: Securities markets *(to come)*

- Session 4: Securities markets *(to come)*

- Session 5: Financial institutions and firms *(to come)*

- Session 6: Financial institutions and firms *(to come)*

- Session 7: Regulation — **individual assignment** *(to come)*

- Session 8: Security analysis — **group presentations** *(to come)*

- Session 9: Regulation *(to come)*

- Session 10: **Final examination**

---

:books: **Readings.** Read the paper *before* the session it belongs to.

- Sessions 1–2 — Monasterolo, I. (2020), *Climate Change and the Financial System*, **Annual Review of Resource Economics** 12
- Sessions 3–4 — Sartzetakis, E.S. (2021), *Green bonds as an instrument to finance low carbon transition*, **Economic Change and Restructuring** 54
- Sessions 5–6 — Muñoz, F. (2020), *How do the size and independence of the board of trustees affect the financial and sustainable performance of socially responsible mutual funds?*, **Corporate Social Responsibility and Environmental Management** 27(4)

:trophy: **Assessment.** 20% individual assignment (session 7) · 40% group work, security analysis in groups of 5 (session 8) · 40% final exam (session 10). A calculator is required for most sessions.

:mag: **Using the slides.** They open in any browser. `→` and `←` move between slides, `O` gives you the overview, `F` is fullscreen, and `E` then print produces a PDF. The PDF handout of each session is linked next to it above.

---

You can reach me at **your.email [at] kedgebs.com**

---

<details>
<summary>For me — building the slides</summary>

Written in [Quarto](https://quarto.org), rendered to reveal.js and beamer from one source. See **[WORKFLOW.md](WORKFLOW.md)** for the commands, the file layout and the slide syntax.

Quick version:

```bash
quarto preview 01-international-financial-system.qmd                  # write with live reload
quarto render 01-international-financial-system.qmd --to revealjs     # build the slides
git add -A && git commit -m "..." && git push                         # publish
```

Pushing to `main` triggers the GitHub Action, which renders everything and republishes the site.

Slides and course material are licensed **CC BY-NC-SA 4.0**; the code (theme, R helpers, workflow) is **MIT**. See [LICENSE](LICENSE).

</details>
