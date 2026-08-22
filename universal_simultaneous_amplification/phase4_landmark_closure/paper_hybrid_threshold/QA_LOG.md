# Paper II reproducibility and PDF QA log

Date: 2026-08-22 (America/Los_Angeles)

## Current superseding-version checkpoint

- Public exact replay boundary reduced to labelled lumping, hybrid response
  coefficients and rational specialization, sextic root/tangency algebra, and
  the paper-level integration audit.
- The retired affine certificate, discovery searches, and sparse numerical
  diagnostics are not public replay dependencies.
- Python is pinned to 3.14.6, SymPy to 1.14.0, and mpmath to 1.3.0 for the
  clean replay.
- Tectonic 0.16.9 and Poppler 26.08.0 are the recorded document tools.
- Venue-specific metadata and cover letters are excluded from the public
  source-and-certificate archive.

## Final freeze checks

- [x] Development exact replay exits zero at the package checkpoint.
- [x] Submission static verifier exits zero at the package checkpoint.
- [x] Deterministic archive generated twice is byte-for-byte identical.
- [x] Internal `MANIFEST.sha256` passes after fresh extraction.
- [x] Pinned bootstrap replay exits zero in that extraction.
- [x] PDF rebuilt from the extraction is byte-for-byte identical with the
      repository PDF.
- [x] PDF metadata, page count, page size, fonts, and link rendering pass.
- [x] Every final page is rendered and visually inspected for clipping,
      overlap, missing glyphs, and stale pages.
- [x] Compiler log has no undefined references or citations and no material
      overfull/underfull boxes.
- [x] Final hostile review is repeated after all corrections.

The frozen public archive contains 19 regular members and has SHA-256
`cd6d72187669c7a1df7ba21c71fac42b4699fea340af3f8118b7eafbb9c4f8cc`.
The 20-page PDF has SHA-256
`573f29287ca3620fa0bafb298e75b4d2f72dd69dafd4e7cad8446d3656e462bc`.
All fonts are embedded; the page size is US letter; the PDF is unencrypted.

The earlier ten-page v1 PDF and its release hashes are historical checkpoints,
not QA evidence for this revised manuscript.
