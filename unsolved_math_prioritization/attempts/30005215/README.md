# Norm estimation from asymmetric black-box linear operators

Catalogue ID 30005215; code OWR-11101919-002; rank 562.

**Outcome:** credited affirmative finite-dimensional resolution already addressed
by Bresch, Lorenz, Schneppe, and Winkler. Both ||A|| from A alone and ||A-V||
from A and V^T admit almost-surely convergent, incremental O(d+m)-storage
estimators. No novelty or first-priority claim is made.

`PROOF.md` gives a self-contained compact random-plane formulation and complete
uniform-cap convergence argument. It handles rank-one/zero maps, repeated
singular values, and dimensions one without divisions by exceptional scalars.
The proof also documents two specific cautions in the inspected mismatch
preprint; its conclusion is established independently of those steps.

This is an AI-assisted research note, not expert peer review. It concerns exact
oracles and asymptotic lower estimates, not certified upper estimates for an
optimization step size or floating-point convergence guarantees.

## Contents

- `PROOF.md`: theorem, algorithm, full proof, source-proof cautions, references
- `SOURCE_GATE.md`: exact source identification and bounded prior-work checks
- `SOURCE_MANIFEST.json`: retrieved-source versions and local-file hashes
- `ATTEMPT_LOG.md`: one substantive turn; stopped on credited/full resolution
- `verify.py`, `checks.json`: reproducible checks with explicit evidential limits
- `STATUS.json`: outcome and proposed two-cell queue change
- `FROZEN_MANIFEST.json`: SHA-256 integrity manifest of this packet

## Reproduce

Python 3.9+ and NumPy are required. From this directory run:

    python verify.py --output /tmp/norm-estimation-checks.json

The frozen run used NumPy 2.3.5. It passed 600 exact rational identities,
600 geometric identities (floating-point checks), and 11 matrix smoke tests
covering zero, scalar, one-row, one-column, rank-one, repeated-top-spectrum,
isometry, 2-by-2, and dense rectangular cases. The convergence proof is analytic.

Primary articles:
https://arxiv.org/abs/2410.08297v3
https://arxiv.org/abs/2503.21361v2

Only this public packet is intended for publication. Downloaded PDFs, extracted
source text, rendered pages, catalogue records, and repository-search data are
excluded.
