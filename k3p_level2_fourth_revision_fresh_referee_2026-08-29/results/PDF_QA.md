# PDF reading and visual-quality audit

Date: 2026-08-29 (America/Los_Angeles)

## Files

- Article: `paper/K3P_Level2_Identifiability_Article.pdf`, 38 pages,
  SHA-256
  `3d08a722ba1fa53f6e336ab285c1cd32d1307bac08e1d4dd2460da71df1816d6`.
- Reader supplement:
  `paper/K3P_Level2_Identifiability_Reader_Supplement.pdf`, 14 pages,
  SHA-256
  `96508f4b4eddb89de99881172abee307b3fe86d236f48e17508bdd1ca9c30efa`.

## Method

I extracted and read the complete text of both PDFs before accepting any
stored proof-package report.  I separately rendered every page with Poppler,
assembled six contact sheets, and visually inspected all 52 rendered pages.
I also inspected the load-bearing mathematical and revised reproducibility
pages at full page resolution.  `pdfinfo` supplied page counts and page-box
metadata; `pdffonts` supplied the font-embedding inventory.

The rendering products are disposable audit material under `tmp/pdfs/` and
are intentionally excluded from version control.  Their use was visual QA,
not mathematical evidence.

## Result

**PASS.**  I found no clipped or overlapping text, missing-glyph box,
unresolved citation/reference marker, malformed formula, cut-off figure or
table, blank unintended page, or inconsistent page box.  All reported fonts
are embedded.  The article and supplement are legible and professionally
typeset.

Text/source comparison also found that article mathematical sections
`01`--`16` are byte-identical to the third revision; the fourth revision
changes the reproducibility disclosure and supplement rather than silently
changing the theorem or handwritten proof.

This finding concerns visual integrity and source continuity.  Exact PDF
reproduction from the packaged source archives is assessed separately in the
source-reproduction subaudit.
