# Infinite generation with the mapping-class Steinberg module

Problem 30003298 / OWR-15177-016, queue rank 997.

**Disposition: unsolved, five approach families.** The original question is settled here only in genus two, by a short corollary of established work. The general-genus question is not settled. No novelty, priority, conventional human peer review, or formal proof-assistant verification is claimed.

The retained theorem proves that, for every g >= 2 and every torsion-free finite-index subgroup Gamma of the orientation-preserving closed-surface mapping class group,

    H^(4g-5)(Gamma; H_(2g-2)(C_g; Z))

has infinite rational rank. For g=2, 4g-5=2g-1=3, so this is exactly an affirmative answer to the source question. For g>=3 the degrees differ, and no conclusion of infinite generation in degree 2g-1 follows.

The main argument combines Harer/Bieri–Eckmann duality with Fullarton–Putman's finite-image rational quotients. Invariant positive forms on quotients of unbounded dimension yield invariant bilinear forms of unbounded finite rank. Their span cannot be finite-dimensional. This argument requires neither irreducibility nor a classification of finite simple groups.

- `PROOF.md`: complete proof of the retained theorem, including the integral/rational comparison and exact imported results.
- `APPROACHES.md`: five genuinely different routes, derived statements, failure tests, and precise remaining gaps.
- `SOURCES.md`: exact source qualification, conventions, inspected locations, later-literature limits, and manuscript status.
- `PROVENANCE.json`: public source and dataset hashes, byte counts, and inspection history; no source content.
- `LEDGER.md`: chronological mathematical work log; preparatory retrieval is not counted as an approach.
- `CLAIMS.json`: machine-readable scope.
- `verify.py`: source-free integrity, scope, and small exact diagnostic checks. Run `python -B verify.py`; `-O` and `-OO` are supported.

`test_verifier.py` replays normal, -O, and -OO checks after read-only relocation and exercises 20 hostile mutations in each mode. Run `python -B test_verifier.py`. It writes only to temporary directories.

The executable does not calculate mapping-class cohomology, certify Fullarton–Putman's theorem, or constitute a proof of the target. The mathematical proof is in the text. Sources and dataset contents are deliberately not packet members. This is an author freeze pending independent review, not an acceptance report. No remote changes were made in this investigation.
