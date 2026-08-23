# Paper II reproducibility and PDF QA log

Date: 2026-08-22 (America/Los_Angeles)

## Current superseding-version checkpoint

- Public exact replay boundary reduced to labelled lumping, hybrid response
  coefficients and rational specialization, sextic root/tangency algebra, and
  the paper-level integration audit.
- The retired affine certificate, discovery searches, and sparse numerical
  diagnostics are not public replay dependencies.
- Python is pinned to 3.14.6, SymPy to 1.14.0, and mpmath to 1.3.0 for the
  clean replay.  The two dependency wheels are bundled and hash-pinned for an
  offline Python bootstrap.
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
- [x] Optimized interpreter, early/late mutation, wheel corruption, mode,
      payload, and internal-manifest negative tests fail closed.

The corrected public archive contains 23 regular members and has SHA-256
`e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`.
The 21-page PDF has SHA-256
`1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`.
All fonts are embedded; the page size is US letter; the PDF is unencrypted.

After the pinned clean bootstrap, a plain isolated `release_bundle.sh`
invocation also rebuilds this archive byte-for-byte without an explicit
interpreter override.

The earlier ten-page v1 PDF and its release hashes are historical checkpoints,
not QA evidence for this revised manuscript.

## Superseded v2.0.1 neutral referee wrapper

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

This wrapper record is historical.  A new v2.0.2 wrapper will be recorded
below after the corrected scientific commit and tag are frozen.

## Corrected v2.0.2 neutral referee wrapper

- Scientific source commit:
  `03e94e877ce10d9d459fd284bd652934cde08bb3`.
- Annotated, unsigned tag:
  `simultaneous-amplification-beyond-three-halves-v2.0.2`; tag object
  `be3946c051c7f7e2073d6adf81bca31ae750251a`.  The remote tag object and
  peeled commit were checked against the local freeze.
- Referee folder: 34 manifested payloads plus
  `PACKAGE_MANIFEST.sha256`, for 35 regular files total.
- Nested source archive: 23 members, SHA-256
  `d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274`.
- Nested and convenience manuscript PDF: 21 pages, SHA-256
  `4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c`.
- Deterministic outer referee archive: 35 regular files, reproduced
  byte-for-byte, SHA-256
  `2216c6a31545b38d9ca89c9d43c5a309bfcc6c2c1f7ab63ea5fabc171116e1d2`.
- A fresh outer-archive extraction passed wrapper and nested manifests,
  offline pinned Python bootstrap, every exact verifier and fail-closed
  regression, source-archive regeneration, PDF regeneration, and both
  byte-identity comparisons.
- The optional Git binding check matched all 21 archived repository source
  blobs and modes to the supplied checkout and frozen tag.  It explicitly
  does not authenticate the unsigned tag, checkout, or authorship.
- Separate hostile tests rejected optimized Python and wrong top-level and
  extracted-source executable modes before any success verdict.

The corrected paper, scientific archive, and neutral referee handoff are
internally consistent.  Research and packaging completion: **100%**; public
release, preprint posting, and journal submission remain human actions.

## Submission-polish v2.0.3 neutral referee wrapper

- Scientific source commit:
  `bd66a3bbf1c530ef67a4b7be5ee69a6825678457`.
- Annotated, unsigned tag:
  `simultaneous-amplification-beyond-three-halves-v2.0.3`; tag object
  `755969d69cdd7f86ad8eceddb4df52a4fe2b23ee`.  The remote tag object and
  peeled commit were checked against the local freeze.
- Referee folder: 34 manifested payloads plus
  `PACKAGE_MANIFEST.sha256`, for 35 regular files total.
- Nested source archive: 23 members, SHA-256
  `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`.
- Nested and convenience manuscript PDF: 21 pages, SHA-256
  `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`.
- Deterministic outer referee archive: 35 regular files, reproduced
  byte-for-byte, SHA-256
  `f4baf76a66a12e4942f13bd7c73bbead0ff31555df5b69a489b914064c597bdf`.
- A fresh outer-archive extraction passed wrapper and nested manifests,
  offline pinned Python bootstrap, every exact verifier and fail-closed
  regression, source-archive regeneration, PDF regeneration, and both
  byte-identity comparisons.
- The optional Git binding check matched all 21 archived repository source
  blobs and modes to the supplied checkout and frozen tag, with the unsigned-
  tag authentication limitation stated explicitly.
- The compiler log has no undefined references, citations, or box warnings;
  all fonts are embedded.  All 21 rendered pages were visually inspected,
  including the corrected complete-clique schematic on page 4.

The v2.0.3 paper, upload archive, metadata, and neutral referee handoff are
internally consistent.  External submission remains a human action.

## bioRxiv submission-handoff checkpoint

- Checked the public bioRxiv submission, scope, screening, licensing, funder,
  and proof-approval guidance on 2026-08-22.
- Prepared a portal walkthrough and copy-ready plain-text metadata for
  **Evolutionary Biology**, article category **New Results**.
- The portal abstract is ASCII-safe, 224 words, and pinned by its normalized
  SHA-256 in the submission-material verifier.
- Reconfirmed the 21-page US-Letter PDF, embedded fonts, unencrypted status,
  and SHA-256
  `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`.
- Reconfirmed the 23-member supplemental archive and SHA-256
  `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`.
- The submission verifier now pins identity fields, title, running title,
  abstract, keywords, contribution roles, prior-version DOIs, upload paths,
  exact counts, and artifact hashes, and refuses optimized Python.
- An independent mutation audit confirmed fail-closed rejection of altered
  identity, category, subject, license, funding, interests, ethics, prior DOI,
  scientific-claim, file-path, count, role, and artifact-hash fields.
- Human-only gates remain for authenticated identity/address fields, truthful
  affiliation entry, author consent, license authority and selection, prior
  online-material disclosure, live terms, portal proofing, and final approval.

bioRxiv handoff preparation: **100%**.  Portal entry, policy acceptance,
license selection, and posting remain human actions.
