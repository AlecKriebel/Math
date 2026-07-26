# Order-12 frontier manuscript package

This directory contains the submission-oriented manuscript for the
certificate-backed order-12 frontier:

> Relative explicitly to MacGillivray--Mynhardt--Virgile's published
> computation through order 11, every counterexample to the one-guard
> \(\gamma\)--\(\theta\) conjecture has order at least 13.

The manuscript does **not** claim a campaign-only enumeration through order
12, a result at any order at least 13, a counterexample, or a universal
proof.

## Deterministic build

From this directory:

```text
SOURCE_DATE_EPOCH=1785074656 \
  tectonic --keep-logs --keep-intermediates main.tex
```

The epoch is the creation time of the frozen C-050 acceptance record,
`2026-07-26T14:04:16Z`.  With Tectonic 0.16.9, two clean builds produced
byte-identical `main.bbl` and `main.pdf` files.

The retained submission files have these SHA-256 values:

```text
5437afac6f3c3e5ee291e7389939bc6708d20521524bce700eba26e051fbf0b5  main.tex
8471090ae03babda7794aea6bbcbc6fbcb36ffa8a859a86005bbb0b7ae2f9ec6  references.bib
f9789755c4ec0c83b1e2493f5301e7d4d4dfaa4398810aa9e28d22148da4849a  main.bbl
1084efc8372a5615dca68bc0f80a4fad88557ebfed8930a655126246de5cd8fc  main.pdf
```

The exact research artifacts are not duplicated into this directory.
Section 7 of the manuscript gives the archive-relative replay commands,
paths, hashes, and accepted verdicts.

## Rendering QA

The final 17-page PDF was rendered at 144 DPI with Poppler and every page
was visually inspected.  The inspection found no clipped or overlapping
text, broken glyphs, margin overflow, malformed tables, or missing page
numbers.  The TeX and BibTeX logs contain no warning, overfull-box,
underfull-box, undefined-reference, or multiply-defined-reference message.
Text extraction found no replacement characters.

The machine-readable QA record and the separate hostile manuscript review
are retained beside the campaign reviews.

## Submission placeholders

Before external submission, the human author must replace the author line
and insert a permanent archive identifier in the data-availability section.
No external communication or publication has been performed.
