# Upstream replay record

Date: 2026-08-10

The following scoped verifiers were replayed before this review was frozen:

```bash
bash reviews/global_bridge/verify_all.sh
python3 reviews/root_probe/verify_all.py
bash reviews/hard_cover_design/verify_all.sh
bash reviews/invariant_engine/verify_all.sh
```

All exited successfully.  The bridge replay regenerated 77 endpoint cases,
204 one-active strict minors, 20 two-active minors, and rejected all 15 scoped
mutations.  The other three scripts validated their committed scope-limited
certificates and manifests.

These successful replays establish only the statuses stated by their own
reviews.  In particular, the hard-cover verifier certifies the fixed-full
design and preserves the false marginal-lift statement; it does not certify a
complete local relation stream.  The invariant verifier certifies the
graph-to-polynomial engine, not atlas exhaustiveness.

The untracked incoming-boundary draft was not used as an upstream theorem
certificate.  Its historical leaves-versus-internal tree-child bug is recorded
in `REVIEW.md`; the corrected `(9,9)` census is already supported by the
committed root/probe review.
