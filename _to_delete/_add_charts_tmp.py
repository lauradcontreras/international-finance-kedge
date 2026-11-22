import io, os

P = os.path.join(os.environ["HOME"],
    "mnt/GitHub/international-finance/07-financial-regulation/07-financial-regulation.qmd")
t = io.open(P, encoding="utf-8").read()

DEPRESSION = '''## 2 · Credit spreads during the Depression

```{r}
#| fig-width: 11
#| fig-height: 4.3
baa <- fred("BAA")
ltg <- fred("LTGOVTBD")
if (is.null(baa) || is.null(ltg)) {
  no_data_note("BAA / LTGOVTBD")
} else {
  d <- merge(baa, ltg, by = "date")
  d$spread <- d$value.x - d$value.y
  d <- d[!is.na(d$spread) &
         d$date >= as.Date("1929-01-01") & d$date <= as.Date("1939-12-01"), ]
  pk <- d[which.max(d$spread), ]
  ggplot(d, aes(date, spread)) +
    geom_line(colour = IF_COL$teal700, linewidth = .7) +
    geom_point(data = pk, colour = IF_COL$clay, size = 2.8) +
    annotate("text", x = pk$date, y = pk$spread + .5, hjust = 0.1,
             label = sprintf("peak %.1f points, %s", pk$spread,
                             format(pk$date, "%B %Y")),
             colour = IF_COL$clay, size = 3.9) +
    labs(x = NULL, y = "Percentage points",
         title = "Lenders could not tell who was good for it, and charged for not knowing",
         subtitle = "Moody's Baa corporate yield less the long-term US government yield",
         caption = "Source: Moody's and NBER long-term government bond yields, via FRED.") +
    theme_if()
}
```

::: notes
One chart, one sentence, and the sentence is the hook slide coming back.

*[point at the level before 1931]*

About two points. That is the normal price of lending to a decent but not
perfect borrower.

*[then the peak]*

Then the peak in 1932. The spread is the compensation a lender demands for not
being sure. It did not widen because firms suddenly became four times worse - it
widened because nobody could tell which firms were which.

*[ask]* If you ran a sound business in 1932 and needed to borrow, what had
changed about you?

Nothing. You simply could not prove it, and the market had stopped believing
anybody who said so. That is a crisis as an information event, measured in
percentage points.

*[if the chart has not rendered]*

It needs the FRED series BAA and LTGOVTBD in the cache - the long-term
government yield is a discontinued series that only covers 1919 to 2000, which
is why it is not the GS10 used later.
:::

'''

HOUSING = '''## 3 · House prices, 2002–2009

```{r}
#| fig-width: 11
#| fig-height: 4.3
hp <- fred("SPCS20RSA")
if (is.null(hp)) {
  no_data_note("SPCS20RSA")
} else {
  hp <- hp[!is.na(hp$value) &
           hp$date >= as.Date("2002-01-01") & hp$date <= as.Date("2009-12-01"), ]
  hp$value <- hp$value / max(hp$value) * 100
  pk <- hp[which.max(hp$value), ]
  tr <- hp[which.min(hp$value), ]
  ggplot(hp, aes(date, value)) +
    geom_line(colour = IF_COL$teal700, linewidth = .8) +
    geom_point(data = rbind(pk, tr), colour = IF_COL$clay, size = 2.8) +
    annotate("text", x = pk$date, y = pk$value + 2.5, hjust = 0.5,
             label = paste("peak,", format(pk$date, "%B %Y")),
             colour = IF_COL$clay, size = 3.9) +
    annotate("text", x = tr$date, y = tr$value - 3.2, hjust = 0.6,
             label = sprintf("down %.0f%% from the peak", 100 - tr$value),
             colour = IF_COL$clay, size = 3.9) +
    labs(x = NULL, y = "Index, peak = 100",
         title = "The collateral behind the whole structure",
         subtitle = "S&P/Case-Shiller 20-city composite, rebased to its own peak",
         caption = "Source: S&P Dow Jones Indices via FRED.") +
    theme_if()
}
```

::: notes
This is the slide that makes the rest of the section inevitable, so put it after
the housing discussion rather than before.

*[the shape]*

Four years up, then down. Nothing unusual about a cycle - what matters is what
was built on top of it.

*[ask]* Every mortgage in those CDOs was secured on one of these houses. So what
does this chart do to the senior tranches?

It is the correlation answer from Problem 4.1, arriving as data. When house
prices fall nationally, defaults are not independent events happening to
unlucky people - they are one event happening to everybody at once, so losses
go straight through the equity tranche and keep going.

*[the near-100% financing point]*

And remember the buyer who put nothing down. At this depth of fall, enormous
numbers of borrowers owed more than the house was worth, with no equity to
lose by walking away.
:::

'''

GFC_SPREAD = '''## 3 · Credit spreads, 2002–2009

```{r}
#| fig-width: 11
#| fig-height: 4.3
baa <- fred("BAA")
gs  <- fred("GS10")
if (is.null(baa) || is.null(gs)) {
  no_data_note("BAA / GS10")
} else {
  d <- merge(baa, gs, by = "date")
  d$spread <- d$value.x - d$value.y
  d <- d[!is.na(d$spread) &
         d$date >= as.Date("2002-01-01") & d$date <= as.Date("2009-12-01"), ]
  pk <- d[which.max(d$spread), ]
  ggplot(d, aes(date, spread)) +
    geom_line(colour = IF_COL$teal700, linewidth = .8) +
    geom_point(data = pk, colour = IF_COL$clay, size = 2.8) +
    annotate("text", x = pk$date, y = pk$spread + .3, hjust = 0.9,
             label = sprintf("peak %.1f points, %s", pk$spread,
                             format(pk$date, "%B %Y")),
             colour = IF_COL$clay, size = 3.9) +
    labs(x = NULL, y = "Percentage points",
         title = "The same measurement, eighty years later",
         subtitle = "Moody's Baa corporate yield less the 10-year Treasury yield",
         caption = "Source: Moody's and the Board of Governors of the Federal Reserve System, via FRED.") +
    theme_if()
}
```

::: notes
Show this one beside the Depression chart if you can - the comparison is the
whole point.

*[the flat years]*

From 2002 to mid-2007 the spread sits under two points and barely moves. That is
a market that believes it can tell good borrowers from bad.

*[the spike]*

Then it goes vertical. Not because corporate America became insolvent in six
months, but because nobody knew which institutions held what.

*[ask]* Put the two charts side by side. 1932 reached about eight points, 2008
about six. Why was the outcome so much less severe the second time?

Because of everything in sections five to seven. Deposit insurance meant no
queue outside the branch. The central bank lent instead of sitting by. The
spread still tells you the information problem was severe - the difference is
what was standing underneath it.

That is the bridge into the second half of the session. Use it.
:::

'''

ins = [("## 2 · What it cost", DEPRESSION),
       ("## 3 · Was the Fed to blame?", HOUSING),
       ("# 4 · The European sovereign debt crisis", GFC_SPREAD)]
for anchor, block in ins:
    assert t.count(anchor) == 1, anchor
    i = t.index(anchor)
    t = t[:i] + block + t[i:]

old = """Hook and roadmap 8 · anatomy of a crisis 20 · the Great Depression 15 · the
global financial crisis 35 · the European sovereign debt crisis 15 · asymmetric
information and capital 35 · banking regulation 35 · Dodd-Frank 15. That is 178
of 180."""
new = """Hook and roadmap 8 · anatomy of a crisis 20 · the Great Depression 18 · the
global financial crisis 41 · the European sovereign debt crisis 15 · asymmetric
information and capital 35 · banking regulation 33 · Dodd-Frank 15. That is 185
of 180.

The three data charts are what pushes it over, and they are worth the overrun -
so plan to drop **electronic banking** and **the Fed and the housing bubble**
before you start, which brings it back to 179."""
assert t.count(old) == 1
t = t.replace(old, new)

io.open(P, "w", encoding="utf-8").write(t)
print("headings:", sum(1 for l in t.split("\n") if l.startswith("# ") or l.startswith("## ")),
      "| notes:", t.count("::: notes"), "| fred:", t.count("fred("),
      "| no_data_note:", t.count("no_data_note("))
