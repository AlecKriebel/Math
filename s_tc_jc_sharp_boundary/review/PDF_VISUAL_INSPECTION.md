# Corrected PDF preflight and visual-inspection report

## Disposition

**PASS after redraw and complete reinspection.** This report supersedes the
previous visual-inspection record. The earlier record was incorrect: it failed
to identify visible overlaps in Figures 1, 6, and 7. Those defects were
confirmed from the frozen PDF and repaired in the TikZ sources. A full-page
reinspection also identified and repaired a separate overlap in Figure 8.

## Audited bytes

- Manuscript: `submission/Generic_Identifiability_STC_Level2_JC.pdf`
- SHA-256: `1e0548d69262bd56071ccbf16815c86b08c5fb343404654b8d1c3d76dff4920f`
- Pages: 48
- Page size: US Letter, 612 by 792 points
- PDF version: 1.7
- Encryption: none
- Embedded fonts: all fonts reported embedded by `pdffonts`

## Build and preflight checks

The manuscript was rebuilt from `source/paper/main.tex` using `latexmk`,
Biber, and the original TikZ sources. The build completed with no undefined
citations or references and no overfull horizontal or vertical boxes. The PDF
opened successfully with PyMuPDF and was classified as text-based rather than
scanned by the preflight script.

## Render protocol

Every page was rendered at 180 dpi with both:

1. PDFium, through `render_pdf.py --engine pdfium`; and
2. Poppler, through `render_pdf.py --engine pdftoppm`.

Eight six-page contact sheets were inspected to cover all 48 pages. The
figure-bearing and previously defective pages were then inspected at full
resolution in both renderers. The inspection was AI-assisted and visual; it is
not represented as an independent human referee report.

## Repairs verified

- **Figure 1, page 7:** the class-inclusion sentence is now below the diagrams;
  the definition box is enlarged; the semi-directed graph and box are
  horizontally separated; no text crosses a diagram or border.
- **Figure 6, page 47:** each separator has a dedicated panel of sufficient
  height; the orbit-649 factorization is broken across two lines; formulas lie
  inside the borders.
- **Figure 7, page 47:** explanatory prose was moved to the ordinary caption;
  the three orientations and two redirection arrows have separate spacing.
- **Figure 8, page 48:** the two sharpness networks and central exchange arrow
  no longer collide; the substitution diagram and formula remain separate.

## Full-document result

No clipping, overlap, missing glyph, cropped figure, broken link annotation,
unreadable table, empty accidental page, or inconsistent page number was seen
in either renderer. The cover letters and referee guide were separately built,
page-count checked, and font-embedded checked by the publication scripts.
