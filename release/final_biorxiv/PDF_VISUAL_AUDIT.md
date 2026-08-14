# PDF build and visual audit

Status: **VERIFIED**

The submission PDFs were rebuilt twice from the released LaTeX source with
`SOURCE_DATE_EPOCH=1786665600`; the two builds were byte-for-byte identical.
The main manuscript has 23 letter-size pages and the supplement has 5.  The
TeX logs contain no undefined references, missing citations, overfull boxes,
or clipped-box warnings.  The one reported underfull bibliography line is a
line-breaking diagnostic and is visually unobjectionable.

Every page was rendered independently by Poppler and Ghostscript at 100 dpi.
Both renderers produced 23 main-manuscript images and 5 supplement images,
all at 850 by 1100 pixels.  The aggregate page-manifest hashes are:

| PDF | Renderer | SHA-256 of page-hash manifest |
|---|---|---|
| Main | Poppler | `772500029633f93c913aa447cb79824d72b8ef11eeb3a9efd0b4bc67fb6c0fca` |
| Main | Ghostscript | `7d37171fd6ee375a9c69e7d35dff577c511b4fa133e55e2969c228c051c96bf2` |
| Supplement | Poppler | `dc5d2b5d651a71abe426d15170da1bb2c3dbd622ce123061d525bda2c4dfe251` |
| Supplement | Ghostscript | `75e1d32c72e93a7718a70eef705e935d21ca5ae322df41e4685c2d4b06894ebd` |

The contact sheets were inspected page by page, with full-size checks of the
dense parameter tables, certificate crosswalk, bibliography, and all vector
figures.  No clipping, overlap, missing glyph, malformed equation, illegible
table, or broken figure was found.  `pdffonts` reports every font embedded and
subsetted.  Poppler and Ghostscript agree on page geometry and content; their
remaining pixel differences are ordinary antialiasing differences.

Contact-sheet hashes:

- Main: `2e02a70c4c75fad1307dfb8d2e60ced9bd4c3ab42ceb10497f0dd385261f549d`
- Supplement: `d9016433d666864324a10aedc2ab88aa1495dccd9c5d4e1a7317b0c44bf155cd`

The page-level manifests and contact sheets are stored in `visual_audit/`.
