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
byte-identical `main.bbl` and `main.pdf` files.  The public edition identifies
**Alec Kriebel** as author and binds data availability to the tagged
reproducibility release.

The retained submission files have these SHA-256 values:

```text
44e49d6dbf90174ca27f5b65e99e55a9852fb6deafb0ba3dd78770c53e0faa9e  main.tex
8471090ae03babda7794aea6bbcbc6fbcb36ffa8a859a86005bbb0b7ae2f9ec6  references.bib
f9789755c4ec0c83b1e2493f5301e7d4d4dfaa4398810aa9e28d22148da4849a  main.bbl
b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2  main.pdf
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

## Public edition

The manuscript has no remaining publication placeholder.  It is the current
paper for the complete order-12 frontier.  The earlier
`paper/c035_order12_k3/` manuscript is retained only as an archival component
draft because its parameter-three theorem is subsumed here.
