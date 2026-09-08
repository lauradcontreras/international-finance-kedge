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

# ---- FRED without an API key ----------------------------------------------
# First render WITH internet writes cache/<id>.csv; every later render — and
# every laptop in a classroom with no wifi — reads the cache. Returns NULL if
# the series has never been cached, so the slide degrades to a note instead of
# breaking the render.
fred <- function(id, dir = "cache") {
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

# ---- small table helper ----------------------------------------------------
fmt_eur <- function(x) ifelse(is.na(x), "", formatC(x, big.mark = " ", format = "d"))
