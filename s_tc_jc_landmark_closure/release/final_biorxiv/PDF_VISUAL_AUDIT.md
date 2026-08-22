# PDF build and visual audit

Status: **VERIFIED — v1.1.7 candidate**

The canonical submission PDFs and both journal variants were rebuilt from the
v1.1.7 source with `SOURCE_DATE_EPOCH=1786924800`. Extracted source ZIPs
reproduced the six article/supplement PDFs byte for byte, and the two
standalone cover-letter sources reproduced the remaining PDFs byte for byte.
Tectonic reported no
undefined references, missing citations, or overfull boxes. Its bundled
`lineno.sty` emitted a source-comment UTF-8 warning while building the
Systematic Biology variant; neither independent renderer shows a replacement
glyph or malformed text.

| Output | Pages | SHA-256 |
|---|---:|---|
| bioRxiv main | 33 | `3e8966ebffd91fc24dcfa48f93c7da910c9385c05e4691b3bd5f288538bb6ba8` |
| bioRxiv supplement | 7 | `a50920a2bc3bb0fb5fb0e624965fd5b8660b3ad1fe05ae592b826311fbfad7c3` |
| Systematic Biology main | 45 | `0c19be4f3ed50e41cd7f199c4141f96f5268f8522fafeb8e706e488063c2e168` |
| Systematic Biology supplement | 7 | `a50920a2bc3bb0fb5fb0e624965fd5b8660b3ad1fe05ae592b826311fbfad7c3` |
| Systematic Biology cover letter | 1 | `f0c73d386154fa66ae96d3115d817465673bb3eedc1ed66dfd97c7460897d3e0` |
| JMB main | 33 | `d3aab5c3edc91ee9bc8ebf47938cb95a3971bd7733848f21c8285c0559ad85e2` |
| JMB supplement (Online Resource 1) | 8 | `dd26de8099b812f591a8ec518d71f67d6145bda3ae453aec6cc2525b539ff688` |
| JMB cover letter | 1 | `fc366d80174d3712b3524dbe97982c6a2328e8ae73e9b28c7553f4e77b3c7096` |

The Systematic Biology supplement is the canonical seven-page supplement. The
JMB-specific supplement adds the journal, corresponding-author, and Online
Resource 1 identification requested by that journal's instructions.

## Complete-page rendering

Every page of the canonical article and supplement was rendered independently
by Poppler and PDFium. Every page of the Systematic Biology article, JMB
article, JMB-specific supplement, and both cover letters was rendered by
Poppler. Page-level SHA-256 manifests and complete contact sheets are in
`visual_audit/`.

The recorded Poppler images were produced by `pdftoppm` at 110 dpi; the
PDFium images were produced by `pypdfium2` 5.12.1 at scale `110/72` and saved
as optimized RGB PNGs with Pillow 12.3.0. Contact sheets use five columns and
204-pixel-wide aspect-preserving page thumbnails. The tracked contact sheets
preserve the inspected output; the page manifests bind the individual
renderings.

| PDF | Renderer | SHA-256 of page manifest |
|---|---|---|
| canonical main | Poppler | `da3d61daa865a77a42ea61078e8c68b7f98e7ec51d0cb4cab664d2ca030ebcde` |
| canonical main | PDFium | `136aa309a4bc595f99de74ebf10d79aa27c428e7949ae3b2560817da85fbaf27` |
| supplement | Poppler | `d821b37c7041cef50a711e153cdf93651abac7a07088ca3ed1829415c495cf84` |
| supplement | PDFium | `6c72c8f3b048952a42da58ae60bde81c5eb85c32f68b4d042b3b4c4ccfabb9dc` |
| Systematic Biology main | Poppler | `22336b581c7e4dc8fa98d8ea7a302a86870627cafb5c8a3b757f100df93458fe` |
| JMB main | Poppler | `50db1385a9d75fcc58fee4653744db3ad659f4cdb0e38af7936932fce505b7a8` |
| JMB supplement | Poppler | `c1dcfeb39eb69563c89e211aaaebe4598418796e631914d18e020f7a4c50e0e1` |

Contact-sheet hashes:

- canonical main (Poppler): `8fb561a859abb02f670c48ca939b042ee18ca84f02a950a637a75d54e1e1876f`
- canonical main (PDFium): `140930984430b7cbf8d483957daa3195b116bb0657b6597821435c96f25a2bfc`
- supplement (Poppler): `18046c0aedf007e337e2b827b45b412f0a8eb455aed288a08977d49575166715`
- supplement (PDFium): `d43df90ced7fcc6ba9f6ae6762e8124db5254fd593110b0d386ee92729842e44`
- Systematic Biology main: `aae493d966554d188171898ebd3c28667ebf8f29b79d19a5a3c5284aba853c42`
- Systematic Biology cover: `a92124a02dcbce3bf9bfada4eb8f6c955681fe2d7070b0e2be2cbca5b27e525e`
- JMB main: `5a55ebb112fcf5299818240afa15eeb81c8f16b1fad903189b29e85a28ad5cb3`
- JMB supplement: `79c9b2556db15f0f59a6d65164fe8bd0373a15a752db9fbded2d84c161aeb4eb`
- JMB cover: `7f110108355b91449a4c7610c522f0fd12fb35cb121c373249b93d833fddf19b`

## Inspection findings

Both complete canonical contact sheets and every portal-specific contact
sheet were inspected, followed by full-size checks of the repaired cut-word
reduction, normalized endpoint dichotomy, smooth-branch localization,
finite-atlas theorem, contextual triangle contraction, four-port quotient
crosswalk, Omega rank-minor table, bibliography, all figures, and the
theorem/certificate crosswalk. The Figure 2 core labels
and all three Figure 4 triangle panels remain separated. In Figure 7, leaf 2
is visibly separated from vertex D and its pendant edge is unambiguous on
both networks. The supplement table, alternative-rooting arc array, and exact
source and target parameter vectors fit inside the text block; every
numerator, denominator, row set, and column set is legible in both renderers.

The Systematic Biology variant retains continuous line numbers, running
heads, one-and-a-half spacing, paragraph indentation, and all seven figure
alt-text blocks. The JMB variant's `Statements and Declarations` grouping is
complete, its article cites Online Resource 1, and the supplement's identifying
title block is clean. Both cover letters are unclipped. Poppler's font audit
reports every referenced font program embedded and subsetted in all eight
PDFs.

No overlap, clipping, missing glyph, malformed equation, unresolved reference,
illegible table, or broken figure was found.
