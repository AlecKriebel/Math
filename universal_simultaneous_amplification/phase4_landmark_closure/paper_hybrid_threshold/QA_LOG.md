# Manuscript and PDF QA

Date: 2026-08-08 (America/Los_Angeles)

## Exact replay

- Optimized sextic root, tangency, and monotonicity certificate: PASS.
- Independent labelled hybrid lumping: PASS, 512 masks and 108 fibres.
- Hybrid coefficient and rational endpoint certificate: PASS.
- Exact endpoint affine witness: PASS.
- Independent discrete-time labelled-event endpoint solve: PASS.

## Build

- Engine: Tectonic with fixed `SOURCE_DATE_EPOCH=1786147200` and UTC.
- Output: `output/pdf/simultaneous_amplification_beyond_three_halves.pdf`.
- Page size: US Letter.
- Pages: 10.
- TeX overfull boxes: none.
- TeX underfull boxes: none.
- Undefined references: none.
- PDF metadata creation time: fixed.

## Visual inspection

All ten final pages were rendered at 150 dpi and inspected.

- title, abstract, and scope box: clear;
- all displayed equations and transition tables: inside margins and legible;
- graph diagram: sharp, labelled, and unclipped;
- section transitions and page numbers: consistent;
- exact-status table: aligned and wrapped correctly;
- bibliography and DOI: readable;
- no overlap, clipping, black squares, or missing glyphs observed.

The build script deletes stale rendered pages before every render, including
when the page-number padding changes.

## Release status

The paper, source, and replay are prepared but not publicly released from
this folder. No DOI, journal submission, or external contact is claimed.
