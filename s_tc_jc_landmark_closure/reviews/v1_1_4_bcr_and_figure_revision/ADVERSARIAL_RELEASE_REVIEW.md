# Final adversarial release and reproducibility review

Status: **PASS**

No actionable release or reproducibility defect remains.

## Repair verification

- The capsule verifier carries an independently declared exact twenty-one
  member set and enforces equality with it.  A second implementation deleted
  `reproducibility/verify_active_release.py`, recomputed the inner checksum
  manifest, and confirmed rejection specifically because the mandatory member
  set differed.
- All three submission capsules contain exactly the required members, every
  payload matches the current source, and the capsules are byte-identical.
- The visual-audit text correctly distinguishes the six PDFs rebuilt from
  source ZIPs from the two cover letters rebuilt from their standalone TeX
  sources.
- Renderer provenance states the exact Poppler, PDFium, and Pillow versions,
  resolution/scale, image mode, and optimization setting.  Independent
  Poppler and PDFium rerenders reproduced all nine page manifests exactly.

## Package verification

- Fresh extracted-source builds reproduced all six article and supplement
  PDFs byte for byte; both cover-letter sources reproduced their PDFs.
- All three outer `SHA256SUMS` manifests pass and exactly cover their intended
  package inventories.
- The PDF table, page-manifest hashes, and all nine contact-sheet hashes in the
  visual audit match the final files.  Full-page inspection found Figure 7
  fixed in every manuscript variant, with no clipping, overlap, missing glyph,
  or unembedded font.
- The v1.1.4 regression rejects all nine mutations.  ZIP structure,
  permissions, timestamps, UTF-8 text, upload filenames, DOI handling, and
  portal routing are coherent.

The active-release inventory is intentionally unsealed until the final
review, commit and tag, and metadata reseal.  That pre-seal state is not a
package defect.

PASS
