# Final rendered-PDF audit

Date: 2026-08-22

Rendered with Poppler and inspected page by page (49 pages total). Page counts, document
properties, extractable text, and font resources were also checked with
`pdfinfo`, pypdf, and pdfplumber.

- Main manuscript: 18 pages; no clipped text, overlapping labels, black boxes, or broken glyphs.
- Technical supplement: 18 pages; dense certificate displays remain within the text block.
- Theorem summary: 3 pages.
- Proof skeleton: 6 pages.
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

The clean-copy replay compares manuscript page counts and extracted layout
text. Byte equality is not required for manuscript PDFs because TeX-engine
metadata and font-subset streams can differ across absolute build roots; the
standalone vector figure remains byte-identical under the recorded toolchain.

These counts describe the PDFs rebuilt after the final source corrections.

The 22 August notation repair was also inspected at full rendered resolution.
In particular, the complete critical vectors are now consistently denoted by
$r$ and $\ell$ while $r_m$ and $\ell_m$ remain scalar components; the physical
scaled-family PDE, its Neumann domain, the transformed left vector, and the
scaled cubic quotient render without crowding.  Supplement S9 uses the local
design parameter $\omega$ throughout.  Contact-sheet inspection of every page
and full-resolution inspection of every changed page found no new overlap,
clipping, broken glyph, or ambiguous line wrap.
