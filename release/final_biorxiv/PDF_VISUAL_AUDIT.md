# PDF build and visual audit

Status: **VERIFIED**

The submission PDFs were rebuilt twice from the released LaTeX source with
`SOURCE_DATE_EPOCH=1786665600`; the two builds were byte-for-byte identical.
The main manuscript has 25 letter-size pages and the supplement has 5.  The
TeX logs contain no undefined references, missing citations, overfull boxes,
or clipped-box warnings.  The reported underfull data-availability and
bibliography lines are line-breaking diagnostics and are visually
unobjectionable.

Every page was rendered independently by Poppler and Ghostscript at 100 dpi.
Both renderers produced 25 main-manuscript images and 5 supplement images,
all at 850 by 1100 pixels.  The aggregate page-manifest hashes are:

| PDF | Renderer | SHA-256 of page-hash manifest |
|---|---|---|
| Main | Poppler | `35567f79fb101bd2a1e1640151535f4988c4242eae4d5e4d433b6f5414fdd55d` |
| Main | Ghostscript | `aab090cb13d534319270fb7c9a5ee697472d2e24d3995e16814bb73cecf9b024` |
| Supplement | Poppler | `65ec2830f7e7e4e6694d42b9bb84a879c279637b35767b71b4d248d411079dff` |
| Supplement | Ghostscript | `7d2239393702a5d647e054db93b5b9a32c61e52a4897db4840216ff81d711b3b` |

The contact sheets were inspected page by page, with full-size checks of the
dense parameter tables, certificate crosswalk, bibliography, and all vector
figures.  Figure 4 was also checked full-size after increasing the panel
spacing; no labels or panels overlap.  No clipping, overlap, missing glyph,
malformed equation, illegible table, or broken figure was found.  Independent
inspection of every PDF font descriptor reports all 31 main-manuscript and 17
supplement fonts embedded.  Poppler and Ghostscript agree on page geometry
and content; their remaining pixel differences are ordinary antialiasing
differences.

Contact-sheet hashes:

- Main: `aae1396aafb0dbce109225c6160f7594d890d0c90caf803df6ba7f1d3dfb17eb`
- Supplement: `5d35ea2ab8086e4dcea633ee1a2cf4ceb033cd83b101e5179d15b9882f1dbda4`

The page-level manifests and contact sheets are stored in `visual_audit/`.
