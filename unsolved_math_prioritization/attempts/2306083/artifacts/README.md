# Function Theory 6.83: coincidence sets

This is a partial-results note for [Problem 2306083](https://www.unsolvedmath.com/problems/2306083), AMR-022-6083. It does not solve the general characterization problem.

The main constructive result gives an explicit pair of bounded normalized univalent functions for sequences satisfying a weighted boundary condition, including all Blaschke sequences in finitely many fixed Stolz regions. It also reconstructs Overholt's necessary Dirichlet-space condition and shows why small-norm and finite-interpolation converse arguments fail. No novelty claim is made.

- `PROOF.md`: proofs, exact scope, and the remaining gap
- `SOURCE_GATE.md`: primary sources, prior-work checks, and source limitations
- `RESEARCH_LOG.md`: five substantive approaches and their outcomes
- `STATUS.json`: machine-readable classification
- `verify.py`, `verification.json`: exact-rational regression checks and saved output

Run with Python 3 from this directory:

```sh
python verify.py > verification.regenerated.json
cmp verification.json verification.regenerated.json
```

Finite computation supplements the proofs; it does not certify the unrestricted characterization.
