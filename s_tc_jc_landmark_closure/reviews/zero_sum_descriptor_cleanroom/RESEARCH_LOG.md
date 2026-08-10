# Research Log

## 2026-08-10 04:40:24 PDT

Created isolated review effort `reviews/zero_sum_descriptor_cleanroom/`.
Read `primary/hard_cover_compiler.py`, `primary/atlas_compiler.py`,
`primary/jc_tensor.py`, and the quarantined
`descriptor_cache_scope_failure/schema3_n3` graph stream as source text/data
only.  No primary or prior-review modules were imported.

Checkpoint estimate: 35% complete.  The active hard-cover source declares
quartet-width complement normalization and a descriptor cache keyed by
selected port count plus exact rooted graph id.  The atlas source intentionally
uses raw rooted selected-side masks.

## 2026-08-10 04:40:24 PDT

Reconstructed the preserved quarantine failure from graph encodings.  The
same mixed-code rooted graph ids
`513afdd7dd8826c2bba2eaff47af1d37bacf98fd3a2906de825bf5705a70f2a2`
and
`83fbeab153b433dea88528707b25a74898a924b90b1eff000c5a7c10257c8dd8`
have different raw chunk-5 descriptors and invariant-50 pullbacks, reproducing
the README hashes `e53478...` and `070141...`.  Their complement-normalized
descriptors and normalized pullbacks agree.

Checkpoint estimate: 70% complete.  Remaining work is packaging the independent
verifier, mutation tests, certificates, and final review text.

## 2026-08-10 04:45:10 PDT

Implemented and ran `cleanroom_verifier.py` through `verify_all.sh`.  The
verifier passed, generated deterministic JSON certificates, rejected all five
required mutations, and recorded the release verdicts in
`certificates/manifest.json`.

Checkpoint estimate: 100% complete for this review goal.  Residual risk is
limited to future primary changes invalidating the inspected source-text
markers, which would make this verifier fail closed.
