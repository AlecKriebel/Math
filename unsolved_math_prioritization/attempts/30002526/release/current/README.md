# Whitney umbrellas and projective group realization

Problem 30002526 / OWR-12869-003. Status: **unsolved**.

This five-approach investigation does not settle the universal realization problem. It gives a source-checked account of the exact target, explicit local algebra explaining the pinch-point obstruction, and elementary controls that disprove several tempting shortcuts. No novelty claim is made for the partial results.

The target requires a complex **irreducible projective surface**, with fundamental group isomorphic to an arbitrary prescribed finitely presented group, and **normal-crossing singularities only**. Normal crossings here are analytic/étale local; they need not be simple globally.

Two official 2016 seminar announcements claim a stronger normal-crossing-only realization theorem. Neither contains a proof, and the author's 2019 research statement still gives the general theorem with Whitney umbrellas. This unresolved literature discrepancy is recorded explicitly. We did not verify a full prior resolution, and do not claim that a bounded search proves the problem remains open.

Files:

- `PROOF.md`: five mechanisms, exact computations, counter-controls and remaining gaps
- `SOURCES.md`: primary source locations and scope
- `RESEARCH_LOG.md`: five substantive approaches and completion estimates
- `RESULT.json`: machine-readable conservative result
- `verify_controls.py`, `control_results.json`: deterministic standard-library algebra checks
- `SHA256SUMS`: frozen author-file hashes

Reproduce with `python3 verify_controls.py` and compare the JSON output with `control_results.json`. The checks certify the stated polynomial identities and small finite calculations. The proofs in `PROOF.md`, rather than the program, establish the topological statements. Neither constitutes a full solution.

Author metadata: Alec Kriebel, https://orcid.org/0009-0001-9320-500X.
