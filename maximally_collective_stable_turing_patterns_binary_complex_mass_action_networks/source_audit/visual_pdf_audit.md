# Final rendered-PDF audit

Date: 2026-08-17

Rendered with Poppler and inspected page by page. Page counts, document
properties, extractable text, and font resources were also checked with
`pdfinfo`, pypdf, and pdfplumber.

- Main manuscript: 16 pages; no clipped text, overlapping labels, black boxes, or broken glyphs.
- Technical supplement: 17 pages; dense certificate displays remain within the text block.
- Theorem summary: 2 pages.
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

A first standalone-diagram build produced separate float/caption pages and a label overlap. The figure source was split into a nonfloating TikZ body plus manuscript caption, the boundary module was moved downward, and the final one-page rendering was reinspected.

The clean-copy replay compares manuscript page counts and extracted layout
text. Byte equality is not required for manuscript PDFs because TeX-engine
metadata and font-subset streams can differ across absolute build roots; the
standalone vector figure remains byte-identical under the recorded toolchain.

These counts describe the PDFs rebuilt after the final source corrections.
