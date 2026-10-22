# Connected-sum complexity: normalization correction and partial results

Problem 30002054 / OWR-11786-002. Review date: 2026-10-06.

**Disposition: the intended additivity problem is unresolved by this investigation.**
An unqualified extension to interior connected sums of manifolds with nonempty
boundary is false: two n-balls have complexity zero, whereas their interior
connected sum is S^(n-1) × [0,1], of complexity n+1, for every n ≥ 3.
This is a scope/normalization counterexample, not a disproof of the intended
closed-manifold or boundary-connected-sum conjecture.

The authored note proves the exact puncture formula

    Gamma(N with b open balls removed) = G(N) + (n+1)(b-1), b ≥ 1,

where G(N) is the minimum g2 of a finite simplicial triangulation of a closed
connected n-manifold N. It also gives the elementary subadditivity construction
and the exact loss incurred by cutting along a triangulated separating sphere
and coning off the two new boundaries. These are elementary consequences of
standard constructions and known lower bounds; no novelty claim is made.

Read `PROOF.md` for hypotheses, arguments, and the remaining gap. `STATUS.json`
separates the literal scope correction from the intended unresolved target.
`SOURCES.json` records public source locations and hashes. `verify_math.py`
performs finite combinatorial diagnostics; it is not a proof of general additivity
and does not implement a manifold recognizer.

## Safe replay

Before executing package code, use the accompanying external bootstrap with
isolated Python and no site initialization:

    python -I -S CONNECTED_SUM_30002054_AUTHOR_BOOTSTRAP.py EXTRACTED_DIRECTORY EXTERNAL_MANIFEST.json

The bootstrap pins the external manifest, rejects inventory differences and
symlinks, checks every file, and only then invokes the checker in isolated mode.
Add `--optimized` to run the checker with Python optimization. Direct execution
from an unchecked directory is not the trust boundary.

This package contains authored analysis and diagnostic code plus public
verification metadata. It contains no downloaded source documents, extracted
source text, supplied corpora, or private coordination material. A separate fresh
independent audit is required before publication.
