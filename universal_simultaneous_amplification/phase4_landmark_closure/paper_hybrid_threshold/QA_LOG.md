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
`ce62bfbdb22681ba48b2a04653155b2e06f52659f140c13f5e0220db365b9250`.
The 20-page PDF has SHA-256
`f68142b3d99b95f83ca6ba4688539cb9e0fdb88ed96809aef5316ed22a59888f`.
All fonts are embedded; the page size is US letter; the PDF is unencrypted.

After the pinned clean bootstrap, a plain isolated `release_bundle.sh`
invocation also rebuilds this archive byte-for-byte without an explicit
interpreter override.

The earlier ten-page v1 PDF and its release hashes are historical checkpoints,
not QA evidence for this revised manuscript.

## Neutral referee wrapper

- Folder payload manifest: 29 files, all verified.
- Nested source archive: 19 members, SHA-256
  `ce62bfbdb22681ba48b2a04653155b2e06f52659f140c13f5e0220db365b9250`.
- Nested manuscript PDF: SHA-256
  `f68142b3d99b95f83ca6ba4688539cb9e0fdb88ed96809aef5316ed22a59888f`.
- Transferable outer archive: 30 files, deterministically reproduced twice,
  SHA-256
  `c0a9c93c60d5f985d45d75e6b2f2638065752ed46ee8f05ef96171e74da7cb59`.
- A fresh extraction of the outer archive passed the standard-library package
  verifier.  The full isolated runner then passed manifest verification,
  pinned replay, source-archive regeneration, PDF regeneration, and both
  byte-identity comparisons.
