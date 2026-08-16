# Final rendered-PDF audit

Date: 2026-08-15

Rendered with the PDF skill renderer and inspected page by page.

- Main manuscript: 14 pages; no clipped text, overlapping labels, black boxes, or broken glyphs.
- Technical supplement: 8 pages; dense certificate displays remain within the text block.
- Theorem summary: 2 pages.
- Proof skeleton: 4 pages.
- Standalone family diagram: 1 vector page, grayscale-compatible.
- Numerical figures: stable profiles, amplitude scaling, and asymptotic scaling render cleanly.
- Fonts are embedded in all release PDFs.
- `pdf_preflight.py` reports every principal PDF openable, unencrypted, and not scan-like.

A first standalone-diagram build produced separate float/caption pages and a label overlap. The figure source was split into a nonfloating TikZ body plus manuscript caption, the boundary module was moved downward, and the final one-page rendering was reinspected.

The clean-copy replay compares manuscript page counts and extracted layout text. Byte equality is not required for manuscript PDFs because pdfTeX font-subset streams can differ across absolute build roots; the standalone vector figure remains byte-identical.
