# PDF build and visual audit

Status: **VERIFIED — v1.1.6 candidate**

The canonical submission PDFs and both journal variants were rebuilt from the
v1.1.6 source with `SOURCE_DATE_EPOCH=1786924800`. Extracted source ZIPs
reproduced the six article/supplement PDFs byte for byte, and the two
standalone cover-letter sources reproduced the remaining PDFs byte for byte.
Tectonic reported no
undefined references, missing citations, or overfull boxes. Its bundled
`lineno.sty` emitted a source-comment UTF-8 warning while building the
Systematic Biology variant; neither independent renderer shows a replacement
glyph or malformed text.

| Output | Pages | SHA-256 |
|---|---:|---|
| bioRxiv main | 33 | `bbf139a8f68c47ec53562e41918a54372a266b70bc69600974b43349f95ed907` |
| bioRxiv supplement | 7 | `0de3f4e5982d6cd6db9c2720079e8175dd9943d1569f330625f2164cb035b339` |
| Systematic Biology main | 45 | `908063bb17b0d4cb42df576a26c423160d01f957b14c240ed382bf9857a95599` |
| Systematic Biology supplement | 7 | `0de3f4e5982d6cd6db9c2720079e8175dd9943d1569f330625f2164cb035b339` |
| Systematic Biology cover letter | 1 | `f0c73d386154fa66ae96d3115d817465673bb3eedc1ed66dfd97c7460897d3e0` |
| JMB main | 33 | `08cd1d0e2454f81141932bc47fbeab3b2263fe6be777118f0a819b6145cf3b57` |
| JMB supplement (Online Resource 1) | 7 | `4cab30a2fc9685bfc8c6d0e130bbe2bb3fdcdca96b0b9f6de229f82ffd750443` |
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
| canonical main | Poppler | `9c4014a73b69307f116cb732aedd29c5c090aa949d91c94358d6c28dbc92443c` |
| canonical main | PDFium | `c8a5cc9766b5b6649d8b1b92852725caa1a7ff31d09a3564d78476ffd9830429` |
| supplement | Poppler | `06f173f0586f12cf7405ee731bb2e4735d0379bf9a248dfd33378e8a5a983f7c` |
| supplement | PDFium | `740208f6869d7224c016a93cdccaded45ba60228a110c95fe744a79d5ec7e8b3` |
| Systematic Biology main | Poppler | `f40fbf28639ebf2a8c3be091458cca5112bce13e32dd451bd19bb52e41e51cf4` |
| JMB main | Poppler | `884e486160d5290b54f7872524663f71b1a0532396abb0ab8858adc4093c7d33` |
| JMB supplement | Poppler | `1c3bb9c3a48b19292ddfa8ba2700b71f5ddc408789145850971ebe819dcaf422` |

Contact-sheet hashes:

- canonical main (Poppler): `48b189dac775d8eb7ee21607dc0390e821809ca158c377cd8de05df717e1633e`
- canonical main (PDFium): `a14e3db52fd2873ce97896d59523574ebaa2023672152dfae004d2bc9680d618`
- supplement (Poppler): `2967165cd46044624ebc05a286ac2cce7d1a24dbb55e8a8a5cfe964858499625`
- supplement (PDFium): `76d7ce3def8aece41b669f62b7452988e86983eaa89827b563e8e0c1dc7d07e1`
- Systematic Biology main: `e91773768a820af4f7a680c721852f2eab42a2d296e9c88d8a3d6cfb42d6ff0c`
- Systematic Biology cover: `72bcdcebf78bbe70c9edd15150a9223143fef47f9a9b42f7828e36ac45124dba`
- JMB main: `5e9ec75f49b464dbbd9eee822202267c6ba18ea336fdf270fb2e2f5482ea55f8`
- JMB supplement: `17148fb7c57daa00acf5480c5fa37c85aaf51add798e92edd4eaed8adbe0c731`
- JMB cover: `8e31afa23565ca8bc052aa215a3eb343ad23d097b95897a3a5a340cccfa7ff2b`

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
