# Run this ONCE, with an internet connection, before the first render.
# It downloads the FRED series the slides use into cache/ so that every later
# render — and every classroom with no wifi — works offline.
#
#   Rscript R/make-cache.R
#
# Delete cache/*.csv and run it again whenever you want fresh data.

source("R/setup.R")

series <- c(
  TB3MS    = "3-month Treasury bill, secondary market rate",
  CPIAUCSL = "CPI, all urban consumers (for the yoy inflation series)",
  DEXUSEU  = "U.S. dollars per euro, daily"
)

for (id in names(series)) {
  d <- fred(id)
  if (is.null(d)) {
    message("FAILED  ", id, " — ", series[[id]])
  } else {
    message("ok      ", id, "  ", nrow(d), " obs, to ", max(d$date))
  }
}
