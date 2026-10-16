# Problem 30003634: third-derived pure-braid counterexample candidate

The proposed universal inclusion has a candidate negative answer already at (n=1,m=3). An explicit nested commutator in (P_3^{(3)}) closes to a link with ordinary signature (-2), while the supplied argument proves that every 1-solvable algebraically split link has signature zero.

Start with `PROOF.md`. The derived-series certificate uses only two pure generators. The signature has two separate exact computations: a 48-dimensional Goeritz matrix with inertia (23,25,0), and a two-dimensional Burau/Meyer calculation. The full finite data are in `certificate.json`.

Run, with Python 3 and no third-party packages:

    python -B verify.py
    python -B test_replay.py

The latter checks normal, `-O`, `-OO`, and `PYTHONOPTIMIZE=2`, performs a relocated replay under read-only file/directory permissions, verifies that the relocated bytes are unchanged, and rejects 88 false-claim or malformed-input cases. The mathematical checker uses explicit exceptions, never `assert`. Its 286 additional exact controls supplement the proof; they are not formal verification of the topology.

Recommended disposition: `claimed_solved`, `1/5`, pending a fresh independent mathematical/source audit. A complete candidate arose on the first substantive signature-obstruction route, so four artificial extra proof routes were not added. No prior target attempt was found in the bounded gate; that is not an exhaustive originality certificate. `SOURCE_AUDIT.md` preserves source conventions and qualifications. `ATTEMPT_LEDGER.json` and `PRIOR_ATTEMPT_GATE.json` record scope and counting.

This packet contains authored work and public verification metadata only. It includes no copied papers, extracts, screenshots, imported dataset records, credentials, or private coordination material. It makes no publication, priority, human-peer-review, or formal-proof-assistant claim.
