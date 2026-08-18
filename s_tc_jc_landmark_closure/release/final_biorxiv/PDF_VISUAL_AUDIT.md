# PDF build and visual audit

Status: **VERIFIED — v1.1.4**

The canonical submission PDFs and both journal variants were rebuilt from the
v1.1.4 source with `SOURCE_DATE_EPOCH=1786924800`. Extracted source ZIPs
reproduced the six article/supplement PDFs byte for byte, and the two
standalone cover-letter sources reproduced the remaining PDFs byte for byte.
Tectonic reported no
undefined references, missing citations, or overfull boxes. Its bundled
`lineno.sty` emitted a source-comment UTF-8 warning while building the
Systematic Biology variant; neither independent renderer shows a replacement
glyph or malformed text.

| Output | Pages | SHA-256 |
|---|---:|---|
| bioRxiv main | 32 | `bfee5df1fe0cbf59bd40ad21eaf1b3165fcb085c0cda7e85e539847e8ad6a239` |
| bioRxiv supplement | 7 | `e0bd28d30a774c1e79cf61dea84e5db5e47e83cc83d0bdeeb69957bed9c43c41` |
| Systematic Biology main | 43 | `7dc57e9bc89f34a771336fbe5716983fa02e5280594b129a71a77ae195ed6c05` |
| Systematic Biology supplement | 7 | `e0bd28d30a774c1e79cf61dea84e5db5e47e83cc83d0bdeeb69957bed9c43c41` |
| Systematic Biology cover letter | 1 | `f0c73d386154fa66ae96d3115d817465673bb3eedc1ed66dfd97c7460897d3e0` |
| JMB main | 32 | `01a546f11c65d75c95b47860b17a670ebd5ff4b14eb197e491213206274557f1` |
| JMB supplement (Online Resource 1) | 7 | `f3ec21988407a943dda21b546ed7394b11ebbd74313dbe01605040d618b6424b` |
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

The recorded Poppler images were produced by Poppler `pdftoppm` 26.05.0 with
`-png -r 120`; the PDFium images were produced by `pypdfium2` 5.12.1 at scale
`120/72` and saved as optimized RGB PNGs with Pillow 12.3.0.  Contact sheets
use four columns, 260-pixel-wide aspect-preserving page thumbnails, a 22-pixel
label band, and a light-gray background.  The tracked contact sheets preserve
the inspected output; the page manifests bind the individual renderings.

| PDF | Renderer | SHA-256 of page manifest |
|---|---|---|
| canonical main | Poppler | `c897875274a5d77a558276c0a7e84ba1dd2ae68241419146c705a7ed5e53034c` |
| canonical main | PDFium | `c299d490fc665820f4d76dbe69e5fafb0b95aaff895aed78f21e4cac41e8fcb6` |
| supplement | Poppler | `faf78688b4e72f5abc5985106d6e82e92a717a2a33c8886b343dba32eb1e7e67` |
| supplement | PDFium | `21849d1fea3ebf5df60c19a1ed5f1b525b28ae67aa1b4fdcd702b684be3f03b5` |
| Systematic Biology main | Poppler | `7e1eec996a3c8c710641733501c537412fac61e3d710d4fe472be3af9e8e5bb7` |
| JMB main | Poppler | `9f695a67d3aff089fff9f6e971bed9bbba87f2a5fc49189a871aca10fb475f04` |
| JMB supplement | Poppler | `0af9bb0ae137b85aa3158728a349d006d7515b7a98ab6fa2d90021f288aae882` |

Contact-sheet hashes:

- canonical main (Poppler): `0a4685e1492ed948649526c3aa6c9dd6d5be036349e8f08ff25d8e2bc8512f61`
- canonical main (PDFium): `23472c63dcc31679bd5b91abaf7e11979b4af45d8e3602d41d6b6609cec2f0d9`
- supplement (Poppler): `17e1b851b9a929f10a70d0045abc131c8816c56bd17e0abc11d36651348a3641`
- supplement (PDFium): `0573d835fe7a758091eea3647e83043f49bcfd34deffa00f94a9f1d1b89788cb`
- Systematic Biology main: `772acd548bd1c020c66da3c71c59d1cddbe7b06793426f74d5b72e3a875e5953`
- Systematic Biology cover: `5f7b9fa59435d9fc958b187d9ccf811b5c572e15991367c1f6288170f963445a`
- JMB main: `07e9ad931b9906f21eb47567c849fee3059c0930940e9bab033ab798b89bcc89`
- JMB supplement: `89b192b67eb016f0bcc31ecba6fada2e3432a8273f29fcbf7a0ad89d79fb64dd`
- JMB cover: `08dd968636f7a4ad994cbe20d1e9c43ad8179e2a600731b979b9e9cb933a8f22`

## Inspection findings

Both complete canonical contact sheets and every portal-specific contact
sheet were inspected, followed by full-size checks of the revised
semialgebraic finite-cover proof, the projective-containment definition, the
unboxed finite-atlas theorem, the Omega rank-minor table, the bibliography,
all figures, and the theorem/certificate crosswalk. The Figure 2 core labels
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
