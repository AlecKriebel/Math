# Fixed-diagonal finite universal paving (20000566)

Status: CLAIMED_SOLVED, limited to the recovered finite universal formulation. Five approaches are in PROOF.md; the full independent mathematical audit is in INDEPENDENT_AUDIT.md. Bibliographic novelty is unestablished.

For an admissible decreasing diagonal d in [0,1]^n with integer sum and 1 <= r <= n, every real or complex orthogonal projection with that diagonal is strictly r-pavable if and only if sum(d[1:kr+1]) < (r-1)k+1 for every k >= 0 with kr+1 <= n. Compactness gives a common positive gap on that one finite fiber. The gap is not computed or dimension-uniform. This is not an existential classification, a prescribed-epsilon answer, or an infinite-dimensional theorem.

Casazza–Edidin already prove sufficiency. The necessity proof uses real Schur–Horn fractional coupling to attain minimum compression rank, followed by the classical matroid partition criterion. The M4 profile is prior-attributed; M6 distinguishes individual strict from non-strict behavior on a common diagonal. The CFMT family prevents a dimension-uniform gap. Public scholarly links and priority limitations are in the proof and audit. No source PDF or copied source text is included.

## Reproduce

Requires Python 3 and SymPy (recorded version in output). Run from this directory:

    python verify.py
    python -O verify.py
    python run_checks.py
    python -O run_checks.py

The two runs execute explicit guards, not removable assertions. Original accepted scripts are retained solely for provenance; the runner executes their guarded derivatives. CHECK_PROVENANCE.json contains the complete normalized transformed and emitted ASTs. Verification is read-only; checks run in temporary directories and compare complete output to frozen logs. The 28,092 rational cases, symbolic identities, and all 31 M6 partitions are sanity checks, not the general proof. Additional theorem checks exercise fractional/integer rank construction and strict-boundary logic.

MANIFEST.json inventories every other file recursively and rejects extra files, nested manifests, symlinks, unsafe paths and unexpected directories. The manifest cannot authenticate itself; a private external freeze receipt pins its hash. This is a publication candidate requiring a separate package audit, not a claim that the publication package itself has already passed that audit.
