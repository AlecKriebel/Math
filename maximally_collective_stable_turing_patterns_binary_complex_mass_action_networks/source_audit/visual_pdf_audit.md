# Final rendered-PDF audit

Date: 2026-09-06

Rendered with Poppler and inspected page by page (96 pages across the seven
canonical, audit, and journal-facing PDFs). Page counts, document properties,
extractable text, and font resources were also checked with `pdfinfo`, pypdf,
and pdfplumber.

- Main manuscript: 19 pages; no clipped text, overlapping labels, black boxes, or broken glyphs.
- Technical supplement: 19 pages; dense certificate displays remain within the text block.
- Theorem summary: 3 pages.
- Proof skeleton: 6 pages.
- SIADS review manuscript and supplement: 24 pages each; PDF cover letter:
  1 page.
- Standalone figures: amplitude scaling, network family, stable profiles, and
  stable trade-off are each 1 page and render cleanly; the network diagram is
  vector and grayscale-compatible.
- Fonts are self-contained in all release PDFs. The three Matplotlib figures
  use embedded CID TrueType fonts rather than Type 3 glyph fonts; the
  manuscript preserves those embedded resources where the figures appear.
- `computation/audit_pdfs.py` reports every principal PDF openable, with the
  expected page count, extractable text, self-contained page fonts, and no
  rendered semantic regression.

A first standalone-diagram build produced separate float/caption pages and a
label overlap. The figure source was split into a nonfloating TikZ body plus
manuscript caption, the boundary module was moved downward, and the long-chain
reaction labels were consolidated into one centered range label. The final
annotation now describes the outlined reaction complexes literally rather
than identifying the outline with the species principal block. The final
one-page rendering was reinspected.

The release-qualified build uses the pinned TinyTeX 2022.04/pdfTeX
1.40.24/Biber 2.17 route.  The semantic audit requires that producer for the
four TeX-built review documents, in addition to current page counts and
extracted content.  Byte equality is not required for PDFs; exact generated
JSON and TeX artifacts have separate byte-level baseline checks.

These counts describe the PDFs rebuilt after the final source corrections.

The 22 August notation repair was also inspected at full rendered resolution.
In particular, the complete critical vectors are now consistently denoted by
$r$ and $\ell$ while $r_m$ and $\ell_m$ remain scalar components; the physical
scaled-family PDE, its Neumann domain, the transformed left vector, and the
scaled cubic quotient render without crowding.  Supplement S9 uses the local
design parameter $\omega$ throughout.  Contact-sheet inspection of every page
and full-resolution inspection of every changed page found no new overlap,
clipping, broken glyph, or ambiguous line wrap.

The v1.0.8 referee-repair PDFs were rebuilt and inspected again.  The expanded
fixed-mass Fourier/Fredholm argument, high-mode inverse estimate, explicit
$3\times3$ Schur remainder, $b=2a$ clarification, and DOI lineage statement
all fit without overfull boxes.  The 19-page main manuscript, 19-page
supplement, 3-page theorem summary, and 6-page proof skeleton were rendered at
120--140 dpi and checked across all 47 review-document pages.  All four
standalone one-page figures were separately rendered and inspected; Figure 1's
chain labels are distinct and nonoverlapping.  No clipping, overlap, broken
glyph, malformed equation, or anomalous blank page was found.

The v1.0.11 certificate-regeneration and journal-layout repair documents
received a fresh primary page-by-page inspection. The canonical manuscript and
supplement remain 19 pages each; the
theorem summary and proof skeleton remain 3 and 6 pages. The separate SIADS
review presentation is 24 pages for the manuscript and 24 pages for the
supplement, with a one-page cover letter. All 96 rendered pages are clean. In
particular, the standalone diffusion-ray statements visibly require positive
diagonal $D$ and the proof skeleton visibly assumes $\det J=0$; all 50 affected
certificate coefficients render unambiguously as $aA/b$ with no collision.
The two verifier commands, the contrast table, the $P_R$/$R_m$ display, and the
operator-space definitions now remain inside the 6-by-8-inch SIADS text block;
continuous line numbers remain outside that block, and Figure 1's labels remain
separated.  The seven retained final logs contain no overfull box or unresolved
reference/citation warning. No clipping, overlap, missing glyph, malformed
equation, or anomalous blank page was found.
