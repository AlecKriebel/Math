# Exceptional-unit prefixes: audited partial results

Problem 30002048 / OWR-11784-007. Full target: **unsolved**, five substantive routes.

Independently verified scoped results: e(7)=5, e(8)=7, e(9)=6, and the strict degree bound for every root of unity. The non-root-of-unity case in exact degrees at least ten is unresolved. The known lower-bound witness polynomials are credited to C. L. Stewart. Historical novelty is unverified and is not claimed.

Start with `release/author/PROOF.md` and the original auditor's `binding_audit/ACCEPTANCE.md`. The complete corrected 39-file release is preserved under `release/`, including its original author archive and full initial audit. The five-file supplemental binding acceptance is preserved under `binding_audit/`. The correction ledger and exact diff are retained, so superseded statements remain identifiable in the historical archive.

Run `python3 verify_manifest.py` for a strict full-inventory and SHA256 check. Run `python3 replay.py` for all three exact mathematical replays in this published layout. The second replay requires SymPy; the two other mathematical verifiers use only Python's standard library. Do not use Python's `-O` option, because certificate assertions must be enabled.

The preserved `binding_audit/verify_binding.py` records the auditor's original working layout, which also contained separate original-author and original-audit siblings. Its full contents and review outcome are retained unchanged. Use the root `replay.py` for the portable published layout; the bound original snapshots are available at `release/original_author/` and `release/independent_review/`.

The outer manifest covers all publication files, including the unchanged nested manifests. No source PDF, source full text, private corpus, or repository coordination inventory is included. No merge or release is requested.
