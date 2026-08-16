# PDF build and visual audit

Status: **VERIFIED**

The submission PDFs were rebuilt twice from the proof-hardened LaTeX source with
`SOURCE_DATE_EPOCH=1786665600`; the two builds were byte-for-byte identical.
The main manuscript has 30 letter-size pages and the supplement has 6.  The
TeX logs contain no undefined references, missing citations, overfull boxes,
or clipped-box warnings.  The reported underfull data-availability and
bibliography lines are line-breaking diagnostics and are visually
unobjectionable.

Every page was rendered independently by Poppler and Ghostscript at 100 dpi.
Both renderers produced 30 main-manuscript images and 6 supplement images,
all at 850 by 1100 pixels.  The aggregate page-manifest hashes are:

| PDF | Renderer | SHA-256 of page-hash manifest |
|---|---|---|
| Main | Poppler | `074f4d4daa8bd042ef8e494f53704b83a2ade34b04e2f6ce15166f22b5ccca15` |
| Main | Ghostscript | `d8fe0d0019be29ef3274b37565aaf322d2dfa5f80cb915e01a461dbf51b13e16` |
| Supplement | Poppler | `cacc841175ed88e2d3935abb4ce6bc514de56f9d9d1ec6df7a08701af49c5c71` |
| Supplement | Ghostscript | `4afa2c69992b66060ed4b36e692584a9cd17b3de976e46a977773826162ed91a` |

The contact sheets were inspected page by page, with full-size checks of the
dense parameter tables, certificate crosswalk, bibliography, and all vector
figures.  Figure 4 on manuscript page 18 was also checked full-size after increasing the panel
spacing; no labels or panels overlap.  No clipping, overlap, missing glyph,
malformed equation, illegible table, or broken figure was found.  Independent
inspection of every PDF font descriptor reports all 31 main-manuscript and 18
supplement fonts embedded.  Poppler and Ghostscript agree on page geometry
and content; their remaining pixel differences are ordinary antialiasing
differences.

Contact-sheet hashes:

- Main: `ef2c512063b024d1aa89250b394691afb802b3413b95c67eaeec13cde09f30b5`
- Supplement: `7d42ca43ad4d1d317989817e379de8046a384b006e15ebad93c15041cc71283e`

The page-level manifests and contact sheets are stored in `visual_audit/`.
