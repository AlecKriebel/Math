# Fixed complex special-Euclidean inverse signatures

**Row 1793 / ID 20000200: scoped_resolved1/5.** This portable authored proof and exact-check package treats the fixed ordered pair (κ²,κ_s) over C, for all reduced integral one-dimensional targets. It makes no broad AIM, novelty, or general software-implementation claim.

## Read

- [Contract](CONTRACT.md) and [result and scope](RESULTS_AND_SCOPE.md)
- [Canonical-cover theorem](cover/CANONICAL_COVER_THEOREM.md)
- [Finite rational differential-equation tests](differentials/EXACTNESS_AND_BASE_ODES.md)
- [Degeneracies and actual image proof](degeneracies/DEGENERACIES_AND_IMAGE_AUDIT.md)
- [Exact coefficient model and classical effectivity](effectivity/EFFECTIVITY_AUDIT.md)
- [Worked exact examples](exact/EXACT_EXAMPLES_AND_CONTROLS.md)
- [Independent acceptance report](audit/INDEPENDENT_ACCEPTANCE_REPORT.md)
- [Sources and prior-art limits](SOURCES.md)

## Replay

Use Python 3.11 or later and SymPy 1.14.0. Install the pinned dependency in your own environment, then run:

    python verify_package.py
    python -O verify_package.py
    python -OO verify_package.py
    PYTHONOPTIMIZE=2 python verify_package.py

For an external integrity anchor, add `--manifest-sha256 SHA256_FROM_THE_SEPARATE_RECEIPT`. `--integrity-only` checks the exact inventory, hashes and acceptance bindings without running the symbolic scripts. The default reruns all four original scripts in temporary directories and requires byte-identical output for 158 named exact checks. The independent suite also performs 108 rational homogeneous-slope comparisons inside one aggregate named check; these are not 108 additional named checks.

The verifier uses explicit exceptions, not optimizable assertions. Each original checker is executed in an isolated nonoptimized child, with source compilation explicitly fixed to optimize=0 and a failing-assertion probe. Thus caller -O, -OO and PYTHONOPTIMIZE cannot disable checker assertions. The package is unchanged by replay. Stored controls distinguish integrity rejection, semantic-check rejection and optimization safety.

The scripts verify supporting algebraic identities and examples. The general theorem, torsion specialization bound, normalization and Riemann–Roch effectivity are justified by the proofs, not exhaustive computation; those general algorithms are not implemented here. Risch's two-good-reductions mechanism is classical prior art.

Only authored results and public verification/source metadata are included. No copied source paper, source text, dataset contents or private coordination file is included. The public edition is explicitly bound to the accepted originals in [EDITION_MAP.json](EDITION_MAP.json). Hash consistency alone is not authenticity: retain the separately delivered manifest or archive hash as a trust anchor.
