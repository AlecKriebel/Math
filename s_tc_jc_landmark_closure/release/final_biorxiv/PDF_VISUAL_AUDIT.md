# PDF build and visual audit

Status: **VERIFIED**

The submission PDFs were rebuilt twice from the referee-hardened LaTeX source with
`SOURCE_DATE_EPOCH=1786838400`; the two builds were byte-for-byte identical.
The main manuscript has 31 letter-size pages and the supplement has 6.  The
TeX logs contain no undefined references, missing citations, overfull boxes,
or clipped-box warnings.  The reported underfull data-availability and
bibliography lines are line-breaking diagnostics and are visually
unobjectionable.

Every page was rendered independently by Poppler and Ghostscript at 100 dpi.
Both renderers produced 31 main-manuscript images and 6 supplement images,
all at 850 by 1100 pixels.  The aggregate page-manifest hashes are:

| PDF | Renderer | SHA-256 of page-hash manifest |
|---|---|---|
| Main | Poppler | `979917d1aec890a9d5d7b062226bfebc08114f1732756e1b6fae52fdc4ffa6e6` |
| Main | Ghostscript | `ad5549e2ef16c1865dab773aa29db57ac352f1a2e3e4a7386558927b4f1a3c5f` |
| Supplement | Poppler | `5efba3050437959b89fa97db2ba85fc0ccb30e9c32333c657d169b7e85331903` |
| Supplement | Ghostscript | `ec249d19fd8dbe38d3269625732ad1476a1b62ad2147bec6684f445d06144bd4` |

The contact sheets were inspected page by page, with full-size checks of the
dense parameter tables, certificate crosswalk, bibliography, and all vector
figures.  Figure 2 on manuscript page 8 was checked full-size after increasing
the graph-to-label clearance, and Figure 4 on page 18 was rechecked; no labels
or panels overlap.  No clipping, overlap, missing glyph,
malformed equation, illegible table, or broken figure was found.  Independent
inspection of every PDF font descriptor reports all 31 main-manuscript and 18
supplement fonts embedded.  Poppler and Ghostscript agree on page geometry
and content; their remaining pixel differences are ordinary antialiasing
differences.

Contact-sheet hashes:

- Main: `d0479348c448f5a667dcb10a69e26d933169919310006ccef9691509b1bafd71`
- Supplement: `7fb1047da85f2bd43c7eaeb628e781b162cf850e5a04a4f6010470da9481d19d`

The page-level manifests and contact sheets are stored in `visual_audit/`.
