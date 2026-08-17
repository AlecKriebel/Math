# PDF build and visual audit

Status: **VERIFIED — v1.1.3**

The canonical submission PDFs and both journal variants were rebuilt from the
v1.1.3 source with `SOURCE_DATE_EPOCH=1786924800`. Extracted source ZIPs
reproduced all eight delivered PDFs byte for byte. Tectonic reported no
undefined references, missing citations, or overfull boxes. Its bundled
`lineno.sty` emitted a source-comment UTF-8 warning while building the
Systematic Biology variant; neither independent renderer shows a replacement
glyph or malformed text.

| Output | Pages | SHA-256 |
|---|---:|---|
| bioRxiv main | 31 | `aa67aa585a8a8fa49323e92e6be68e7a7ca5d0c4233b8c1f00a403f7aff8c011` |
| bioRxiv supplement | 6 | `923499148d03f271943d1f0646a30120510cce7e16c941a404c161d0f186f63f` |
| Systematic Biology main | 42 | `4f1bba1ec3857f5c6a44ece7f20c88e4e67c1ea4a1facf253978318aef4879ca` |
| Systematic Biology supplement | 6 | `923499148d03f271943d1f0646a30120510cce7e16c941a404c161d0f186f63f` |
| Systematic Biology cover letter | 1 | `f0c73d386154fa66ae96d3115d817465673bb3eedc1ed66dfd97c7460897d3e0` |
| JMB main | 31 | `66553214692d31b9b875dc3e849fe72619f9cd4c4281b87425dea703c9767bc3` |
| JMB supplement (Online Resource 1) | 6 | `c51ba91ece0dab038846f43b340fb3db13971356580df47da6f32f4c903097f6` |
| JMB cover letter | 1 | `fc366d80174d3712b3524dbe97982c6a2328e8ae73e9b28c7553f4e77b3c7096` |

The Systematic Biology supplement is the canonical six-page supplement. The
JMB-specific supplement adds the journal, corresponding-author, and Online
Resource 1 identification requested by that journal's instructions.

## Complete-page rendering

Every page of the canonical article and supplement was rendered independently
by Poppler and PDFium. Every page of the Systematic Biology article, JMB
article, JMB-specific supplement, and both cover letters was rendered by
Poppler. Page-level SHA-256 manifests and complete contact sheets are in
`visual_audit/`.

| PDF | Renderer | SHA-256 of page manifest |
|---|---|---|
| canonical main | Poppler | `01cbc994dd58a81a86d58f51a90f5b26719194032bd024c4be440b3cf8ac1887` |
| canonical main | PDFium | `70ad1e25732d14884294bba2141f679a1676f07ac3405d4ad79a8aa921c5c25a` |
| supplement | Poppler | `ddddd415ab4715d64fe8dbdf0f5b0f821d69ca49fc4b475341e8c8e4756c44b8` |
| supplement | PDFium | `06bce79d9370b7eb19e85a7739886ccb6c9e0ba65f0582eb8b04860314ba1b05` |
| Systematic Biology main | Poppler | `20c6c78e436504452b5711aee9a9e79e0e522bdeaec14753ed602661b79a232b` |
| JMB main | Poppler | `fa09bff008c38443114fafbd736b815d51e0cacdffd337811c799ec94371182e` |
| JMB supplement | Poppler | `09379c0fdcbf198907d57c6cb2f92573a853e16a5739bf53996834a1f943c90a` |

Contact-sheet hashes:

- canonical main (Poppler): `d012bdee9200f50ca92491c1346a7ef4ca8cc5238056477571eebb26ebc4253f`
- canonical main (PDFium): `e2a18a813bf1bed906c4142cafcd7165db94dc22309e58da7ac1aebdc3b417dd`
- supplement (Poppler): `bb263e7168f1fe6eda6dbb9caa778be542aa82427e76b64e13e9ab035af1c65c`
- supplement (PDFium): `c63b944d3f64e75c2942eef8701618e8d5705d0a8ec23ae9964ae66589245c1e`
- Systematic Biology main: `ebe6be9e860c0339c0fbfa937b45a96ba39893e01c697fe2518c8cae597e927e`
- Systematic Biology cover: `62ee18d96850c6fa5d1e845b57af4d5b0063596596d5857c9f78c7b6cd55510c`
- JMB main: `3d4c10006731a045da1bccebe05a1152f41873f6e2567246952e00c74d0e72d0`
- JMB supplement: `8d1b6d2ddbfb3f92c469aa43e095020676fe3843c1fd88550318b3a93b8e99a3`
- JMB cover: `93bfc1bdbb08423db5e0b73561a479e4488224ac94d03114e0add6c4dca5cf40`

## Inspection findings

Both complete canonical contact sheets and every portal-specific contact
sheet were inspected, followed by full-size checks of the new Omega
rank-minor table, the Englander comparison, the bibliography, all figures,
and the theorem/certificate crosswalk. The Figure 2 core labels and all three
Figure 4 triangle panels remain separated. The new supplement table fits
inside the text block and every numerator, denominator, row set, and column
set is legible. The Omega type-(2c) caption is unclipped.

The Systematic Biology variant retains continuous line numbers, running
heads, one-and-a-half spacing, paragraph indentation, and all seven figure
alt-text blocks. The JMB variant's `Statements and Declarations` grouping is
complete, its article cites Online Resource 1, and the supplement's identifying
title block is clean. Both cover letters are unclipped. A direct PDF object
inspection found every referenced font program embedded in all eight PDFs.

No overlap, clipping, missing glyph, malformed equation, unresolved reference,
illegible table, or broken figure was found.
