# The session 1 survey

Two questions, both multiple-response, no free text. Copy the text below into a
Google Form, paste the link into the deck, re-render, done.

## Building the form

1. **forms.new** in your browser
2. Title: `International Finance — before we start`
3. Description: `Two quick questions. Anonymous. Tick as many as apply to you.`
4. Settings (the gear):
   - **Collect email addresses: off** — anonymity gets you honest answers on question 2
   - **Limit to 1 response: off** — that would force a Kedge login
   - **Edit after submit: on** — harmless, saves you from "I ticked wrong"
5. Add the two questions below. Both are **Checkboxes**, both **Required**, and
   leave **"Add Other" off** — you asked for no open answers.
6. **Send → link icon → Shorten URL → Copy**
7. Paste it into `survey_url` in the deck (see below), re-render, and the QR
   appears on the slide.
8. Answers: **Responses** tab → the Sheets icon → a spreadsheet you own.

## Question 1

> **Where do you want to work after your studies?**
>
> Tick as many as apply.

- Finance or audit
- Marketing
- Business development
- Consulting
- Management
- Logistics
- Something else
- I don't know yet

## Question 2

> **Which of these have you already come across — in a course, an internship, or the news?**
>
> Tick as many as apply. There is no wrong answer; this tells me where to slow down.

- Exchange rates
- Balance of payments
- Interest rates and yield curves
- Financial crises
- Derivatives and hedging
- Central banks and monetary policy
- None of them yet

## Putting the link in the deck

In `01-international-financial-system/01-international-financial-system.qmd`,
find the survey slide and change one line:

```r
survey_url <- "https://forms.gle/REPLACE-ME"
```

Re-render. The QR code is generated from that string by the `qrcode` package —
no external service, no tracking, and it works offline once rendered. Until you
change it, the slide shows a "QR appears here" placeholder, so a half-set-up
deck never looks broken in front of a room.

Install the package once:

```r
install.packages("qrcode")
```

The GitHub Action already has it in its package list, so the published deck
builds the QR too.

## Showing the results in the room, immediately

Google Forms will draw the charts for you and you can project them.

1. In the Form: **Settings → Responses → "See summary charts and text responses" ON**
2. **Send → link**, copy it, and swap `/viewform` for `/viewanalytics`
3. Put that link in `results_url` on the "What the room said" slide

That `/viewanalytics` URL is public once the setting is on — no Google login on
the classroom machine, which is the part that usually goes wrong at 8am.

**Open it in a second browser tab before class** and switch tabs rather than
clicking from the deck. Reveal's link preview tries to open external links in an
overlay and Google refuses to be framed, so the slide's link is marked to open in
a real tab — but a tab you opened beforehand is still faster and never surprises
you.

Charts redraw on refresh, not by themselves. Reload once the last hand goes down.

If you ever want the results to appear *on the slide itself*, updating as they
answer, that is Slido or Mentimeter — but their free tiers cap you at roughly
your two questions, which is why the Form is the better trade here.

## Reading the answers

**Question 1** tells you which examples land. A room that is mostly consulting
and marketing needs the Ireland and Swiss franc stories more than it needs the
mechanics of BKA sub-accounts; a room of finance-and-audit students will want
the opposite.

**Question 2** is the one that changes your teaching. The four sections of
session 1 map onto its options: exchange rates and central banks → section 4,
balance of payments → section 2, interest rates and yield curves → section 3,
financial crises → the Asian crisis and Monasterolo. Whichever boxes stay empty
is where to spend the extra ten minutes.

Watch for the gap between the two questions: students heading into finance who
tick "none of them yet" are the ones the course is really for.

## Asking it again later

Duplicate the form before session 10 and ask question 2 again, unchanged. The
shift in the boxes is the most honest measure of the course you will get, and
it costs you two minutes. Keep both spreadsheets.
