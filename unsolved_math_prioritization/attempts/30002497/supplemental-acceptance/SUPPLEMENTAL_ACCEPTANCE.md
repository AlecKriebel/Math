# Supplemental acceptance: correction C1 closed

Problem 30002497 / OWR-12866-004, rank 623. 2026-10-04 UTC.

**Accepted for the exact corrected release identified below.** The required
outward-endpoint serialization correction is closed. The analytic partial
theorems remain accepted, and the full target remains **unsolved after five
approaches**, with no novelty claim. This is a binding and correction-closure
continuation of the independent audit, not a new mathematical search.

## Release binding

- `MANIFEST.json` SHA-256:
  `1857279d8d5a572c27d337e2625d61189ed2a683f642ed941dfee9a52b8ef67d`
- `SHA256SUMS` SHA-256:
  `1bee70377abb0954cd42a454b865d8fa1f142197ccc2ae393e918b49ce031d15`

Acceptance applies to those exact release bytes. This separate statement
resolves the frozen snapshot's pending reviewer-rebinding notices without
altering them. It does not bind a subsequently modified release.

## Verified closure

1. The release contains exactly 39 regular files: 37 payload entries in the
   safe manifest, plus that manifest and its checksum file. All lengths and
   SHA-256 values match. The root checksum file covers all other 38 files.
   There are no unlisted files or symlinks.
2. All nine frozen original author files and all 14 files of the independently
   bound audit are preserved byte-for-byte. Both `PROOF.md` and `SOURCES.md`
   remain unchanged in the corrected packet.
3. Exactly seven current files differ from the originals. The ledger has the
   correct complete changed/unchanged partition and every before/after hash.
   Reconstructing the unified diff from the two actual directories reproduces
   `CORRECTION.diff` exactly.
4. The corrected verifier is the supplied audited variant verbatim. Its event
   integration functions are AST-identical to the original ones. Both corrected
   JSON certificate files match the previously audited corrected outputs.
5. All four computational replays succeeded: historical original and corrected
   verifier, each at cutoff/precision 2048/40 and 4096/60. Every output matches
   its corresponding saved file byte-for-byte. The complete rerun verification
   record also matches the release's verification record byte-for-byte.
6. All eleven corrected high-precision derivative intervals nest in the lower-
   precision intervals, which lie inside the independent integer-backend
   intervals. Signs remain positive for reciprocal indices 1–9 and negative
   for 10–11. The independent standard-library backend was rerun successfully,
   and all 24 exact-rational outward-serializer tests pass.
7. The inventory and new release wrapper content were checked for safe scope.
   The release contains no source PDFs, extracted source texts, raw catalogues,
   private coordination inventories, or absolute private-workspace references.
   Historical nearest-rounded outputs are explicitly distinguished from the
   current directed-decimal certificates.

## Mathematical disposition

The strongest verified results remain the necessary stationary-Wilton
condition for every positive irrational local maximum and exclusion of the
specified quadratic family and its reciprocals. No stationary Wilton point
with a strict two-sided local maximum has been constructed, and no universal
exclusion has been proved. Certification correction C1 changes none of these
facts, derivative signs, or quantifiers.

The release, original author packet, and original independent audit were not
edited. No remote writes or external communications were performed. This
acceptance is an evidentiary review statement; it does not itself publish or
authorize publication of any files.

## Evidence and reproduction

- `binding_verification.json`: exact inventory, diff, ledger, preservation,
  correction closure, and replay-binding results
- `replayed_release_checks.json`: freshly regenerated complete numerical record
- `verify_binding.py`: portable read-only binding verifier
- `SUPPLEMENTAL_ACCEPTANCE.json`: machine-readable acceptance
- `MANIFEST.json` and `SHA256SUMS`: this supplement's own integrity bindings

With Python 3 and mpmath 1.3.0, choose output paths outside the release:

    PYTHONDONTWRITEBYTECODE=1 python RELEASE/RELEASE_CHECKS.py --output new_replay.json
    python verify_binding.py --release RELEASE --replay new_replay.json --output new_binding.json

Replace `RELEASE` with the corrected release directory. The supplement does
not need source PDFs, any private inventories, or network access.
