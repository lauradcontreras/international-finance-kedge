# International Finance — shared plotting setup
# Sourced by every session's .qmd. Colours mirror theme.scss.

suppressPackageStartupMessages({
  library(ggplot2)
})

IF_COL <- list(
  teal900 = "#06302F",
  teal700 = "#0E5250",
  teal500 = "#1C7F79",
  teal300 = "#63ADA6",
  teal050 = "#EAF2F1",
  clay    = "#B4573C",
  slate   = "#40607D",
  sand    = "#FAF8F4",
  ink     = "#1B2321",
  muted   = "#63716E"
)

if_pal <- function(n = 4) {
  unname(unlist(IF_COL[c("teal700", "clay", "slate", "teal300")]))[seq_len(n)]
}

theme_if <- function(base_size = 15) {
  theme_minimal(base_size = base_size) +
    theme(
      text             = element_text(colour = IF_COL$ink),
      plot.title       = element_text(face = "bold", colour = IF_COL$teal700,
                                      size = rel(1.05), margin = margin(b = 6)),
      plot.subtitle    = element_text(colour = IF_COL$muted, size = rel(.85)),
      plot.caption     = element_text(colour = IF_COL$muted, size = rel(.7), hjust = 0),
      axis.title       = element_text(colour = IF_COL$muted, size = rel(.85)),
      axis.text        = element_text(colour = IF_COL$muted, size = rel(.8)),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(colour = "#E8EDEC", linewidth = .35),
      legend.position  = "bottom",
      legend.title     = element_blank(),
      legend.text      = element_text(size = rel(.85)),
      plot.margin      = margin(4, 4, 4, 4)
    )
}

# ---- schematic axes: an economics diagram, not a data plot ----------------
theme_schematic <- function(base_size = 15) {
  theme_if(base_size) +
    theme(
      panel.grid  = element_blank(),
      axis.text   = element_blank(),
      axis.title  = element_text(colour = IF_COL$ink, size = rel(.95)),
      axis.line   = element_line(colour = IF_COL$ink, linewidth = .5,
                                 arrow = grid::arrow(length = unit(.018, "npc"),
                                                     type = "closed"))
    )
}

# ---- where the repo root is, whatever folder we are rendering from --------
# Slides live in slides/<session>/, this file in slides/R/, the FRED cache at
# the repo root. Walk up until we find _quarto.yml so every session shares one
# cache instead of downloading its own copy.
if_root <- function(start = getwd()) {
  d <- normalizePath(start, mustWork = FALSE)
  for (i in 1:6) {
    if (file.exists(file.path(d, "_quarto.yml"))) return(d)
    parent <- dirname(d)
    if (parent == d) break
    d <- parent
  }
  start
}

# ---- FRED without an API key ----------------------------------------------
# First render WITH internet writes cache/<id>.csv; every later render — and
# every laptop in a classroom with no wifi — reads the cache. Returns NULL if
# the series has never been cached, so the slide degrades to a note instead of
# breaking the render.
fred <- function(id, dir = file.path(if_root(), "cache")) {
  dir.create(dir, showWarnings = FALSE, recursive = TRUE)
  f <- file.path(dir, paste0(id, ".csv"))
  if (!file.exists(f)) {
    url <- paste0("https://fred.stlouisfed.org/graph/fredgraph.csv?id=", id)
    ok <- tryCatch({
      utils::download.file(url, f, quiet = TRUE, mode = "wb"); TRUE
    }, error = function(e) FALSE, warning = function(w) FALSE)
    if (!ok || !file.exists(f) || file.size(f) < 100) {
      unlink(f)
      return(NULL)
    }
  }
  d <- utils::read.csv(f, stringsAsFactors = FALSE, na.strings = c("", ".", "NA"))
  names(d) <- c("date", "value")
  d$date  <- as.Date(d$date)
  d$value <- suppressWarnings(as.numeric(d$value))
  d[!is.na(d$value), ]
}

no_data_note <- function(id) {
  ggplot() +
    annotate("text", 0, 0.15, label = paste0("FRED series ", id, " not cached yet"),
             colour = IF_COL$teal700, size = 5.2, fontface = "bold") +
    annotate("text", 0, -0.15,
             label = "Render once with an internet connection to fetch and cache it",
             colour = IF_COL$muted, size = 4) +
    xlim(-1, 1) + ylim(-1, 1) + theme_void()
}

# US recession shading for FRED-style charts (NBER peaks -> troughs)
us_recessions <- data.frame(
  start = as.Date(c("1953-07-01","1957-08-01","1960-04-01","1969-12-01","1973-11-01",
                    "1980-01-01","1981-07-01","1990-07-01","2001-03-01","2007-12-01",
                    "2020-02-01")),
  end   = as.Date(c("1954-05-01","1958-04-01","1961-02-01","1970-11-01","1975-03-01",
                    "1980-07-01","1982-11-01","1991-03-01","2001-11-01","2009-06-01",
                    "2020-04-01"))
)

recession_bands <- function(from = as.Date("1954-01-01")) {
  d <- us_recessions[us_recessions$end >= from, ]
  geom_rect(data = d, inherit.aes = FALSE,
            aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf),
            fill = IF_COL$muted, alpha = .13)
}

# ---- the in-class survey ---------------------------------------------------
# The Google Form writes into a Sheet. The Sheet is read as CSV at render time
# and cached, exactly like FRED: refresh before class, and the deck still
# builds later on a train. No API key and no login — this works only because
# the Sheet is shared as "Anyone with the link -> Viewer". If you ever set it
# back to restricted, this returns NULL and the slides show a note instead.

IF_SHEET <- "1dxAmDONqRF-6cTS9HgQKucEKZCKV5eCObg1CtYdOA0c"

survey <- function(sheet = IF_SHEET, dir = file.path(if_root(), "cache"),
                   refresh = TRUE) {
  dir.create(dir, showWarnings = FALSE, recursive = TRUE)
  dest <- file.path(dir, "survey.csv")
  url  <- sprintf("https://docs.google.com/spreadsheets/d/%s/export?format=csv",
                  sheet)

  if (isTRUE(refresh)) {
    tmp <- tempfile(fileext = ".csv")
    ok <- tryCatch({
      utils::download.file(url, tmp, quiet = TRUE, mode = "wb")
      file.exists(tmp) && file.size(tmp) > 0 &&
        !grepl("<HTML|<html", readLines(tmp, n = 1, warn = FALSE)[1])
    }, error = function(e) FALSE, warning = function(w) FALSE)
    if (ok) {
      file.copy(tmp, dest, overwrite = TRUE)
    } else {
      message("survey(): could not read the sheet. Either there is no internet, ",
              "or its sharing is not 'Anyone with the link'. Falling back to ",
              "cache/survey.csv.")
    }
  }

  if (!file.exists(dest)) return(NULL)
  x <- utils::read.csv(dest, check.names = FALSE, stringsAsFactors = FALSE)
  if (nrow(x) == 0) return(NULL)
  x
}

# Google Forms joins the ticked boxes of one answer with ", " — and several of
# the option labels contain a comma themselves ("Finance, banking or audit"),
# so splitting on the comma would shred them. Instead: pull out every known
# label first, longest first, and only then split whatever is left over. An
# option missing from IF_OPTIONS therefore shows up as its own odd-looking
# bar rather than being silently dropped — that is the signal to add it here.
IF_OPTIONS <- list(
  work = c(
    "Finance, banking or audit",
    "International trade, logistics or supply chains",
    "Public sector / international organizations",
    "Management"
  ),
  topics = c(
    "Exchange rates",
    "Balance of payments",
    "Interest rates and yield curves",
    "Financial crises",
    "Derivatives and hedging",
    "Central banks and monetary policy",
    "None of them yet"
  )
)

split_multi <- function(x, options = character()) {
  options <- options[order(nchar(options), decreasing = TRUE)]
  out <- character()
  for (cell in x[!is.na(x) & nzchar(trimws(x))]) {
    rest <- cell
    for (o in options) {
      while (grepl(o, rest, fixed = TRUE)) {
        out  <- c(out, o)
        rest <- sub(o, "", rest, fixed = TRUE)
      }
    }
    left <- trimws(unlist(strsplit(rest, ",", fixed = TRUE)))
    out  <- c(out, left[nzchar(left)])
  }
  out
}

# Counts, ordered smallest to largest so the bars read top-down when flipped.
count_multi <- function(x, options = character()) {
  v <- split_multi(x, options)
  if (!length(v)) return(NULL)
  tb <- sort(table(v))
  data.frame(answer = factor(names(tb), levels = names(tb)),
             n = as.integer(tb), row.names = NULL)
}

bar_answers <- function(d, n_respondents = NA, fill = IF_COL$teal700,
                        title = NULL, subtitle = NULL) {
  ggplot(d, aes(answer, n)) +
    geom_col(fill = fill, width = .68) +
    geom_text(aes(label = n), hjust = -0.35, colour = IF_COL$muted, size = 4.4) +
    coord_flip(clip = "off") +
    scale_y_continuous(expand = expansion(mult = c(0, .12))) +
    labs(x = NULL, y = NULL, title = title, subtitle = subtitle) +
    theme_if() +
    theme(panel.grid.major.y = element_blank(),
          axis.text.x = element_blank(),
          axis.text.y = element_text(colour = IF_COL$ink, size = rel(.95)))
}

no_survey_note <- function(
    msg = "No responses yet",
    sub = "The charts appear once the form has answers and the deck is re-rendered") {
  ggplot() +
    annotate("text", 0, 0.15, label = msg,
             colour = IF_COL$teal700, size = 5.2, fontface = "bold") +
    annotate("text", 0, -0.15, label = sub, colour = IF_COL$muted, size = 4) +
    xlim(-1, 1) + ylim(-1, 1) + theme_void()
}

# ---- small table helper ----------------------------------------------------
fmt_eur <- function(x) ifelse(is.na(x), "", formatC(x, big.mark = " ", format = "d"))
