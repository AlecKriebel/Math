# Function Theory 6.86: qualitative improvement and remaining quantitative gap

UnsolvedMath ID 2306086 / AMR-022-6086; campaign rank 687.

**Status: rigorous partial results; target-interpretation review required. No claim of a new full solution.**

For normalized real-coefficient univalent functions, the standard pre-Schwarzian disk radius is strictly reducible at every fixed nonreal point, uniformly over the class. Equality rigidity and compactness prove this. The radius cannot be reduced uniformly over a circle, because real-axis Koebe maps attain the old bound.

The exact primary wording asks whether improvement is possible and does not explicitly request a best constant. Thus the note answers its qualitative existence interpretation. It does not determine an explicit positive improvement, the sharp radius, or the full variability region. The distinction is retained for independent review rather than silently replacing the research goal with either a weaker or stronger formulation.

## Contents

- `PROOF_PARTIALS.md`: complete authored proofs, class definitions, equality cases, compactness, one-parameter reduction, exact lower bounds, and a convex-hull obstruction
- `APPROACH_LOG.md`: five distinct substantive approaches, their outcomes and remaining gaps
- `SOURCE_VERIFICATION.json`: public bibliographic/retrieval metadata, dataset identifiers, source-access limitations, and bounded duplicate checks
- `LIMITATIONS.md`: scope, proof dependencies, access and novelty limits
- `exact_controls.py` and `EXACT_CONTROL_RESULTS.json`: standard-library exact-arithmetic regression controls, including negative controls
- `explore_loewner.py` and `LOEWNER_EXPLORATION.json`: explicitly non-certified numerical exploration; requires NumPy, SciPy, and SymPy
- `FROZEN_MANIFEST.json`: byte counts and SHA-256 hashes of the authored/public-metadata files

Run the exact checks with:

    python3 exact_controls.py
    python3 -O exact_controls.py

Both modes give 3,558 passing checks. These controls supplement the proofs and do not certify the numerical ODE search.

Only authored mathematics, authored code, generated experiment results, and public verification metadata are included here. No scholarly PDF, extracted source text, dataset record contents, or private coordination material is included.

This is an author freeze awaiting fresh independent audit. It is not an audit receipt, publication receipt, or claim that repository state has been changed.
