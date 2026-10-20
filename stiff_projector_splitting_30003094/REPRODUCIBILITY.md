# Replaying the stiff projector-splitting corroborations

## Requirements

The recorded environment is Python **3.12.14**, NumPy **2.3.5**, SciPy
**1.17.0**, and mpmath **1.3.0**. The latter three versions are listed in
`requirements.txt`; dependencies are not vendored. Use an environment where
these dependencies are installed. A compatible different version may also
pass; the runner reports its versions and whether they match the recorded
ones. No bitwise reproducibility across BLAS implementations or platforms
is promised. Assertions must remain enabled: do not use `-O` or `-OO`.

No input dataset, scholarly PDF, copied source text, network retrieval,
private file or other repository checkout is needed. The checker scripts
contain all tested numerical matrices and parameters.

## Commands and isolation

From the package directory:

    python3 -I -S -B verify_manifest.py
    python3 -I -B run_checks.py

The manifest verifier is standard-library-only and may omit site packages
with `-S`. It checks the exact payload inventory, byte counts and SHA-256
values, rejects extra/missing files and symbolic links, and checks the
audited manuscript and audit hashes. The manifest excludes only itself to
avoid circular hashing. It is an integrity check, not independent
authentication or a correctness proof.

The numerical runner **must not** use `-S`, because it needs installed
third-party packages. It creates a fresh temporary directory and copies
only the four checker scripts into it. Each checker runs with Python
`-I -B`: isolated mode ignores Python environment variables and user site
packages, and bytecode caching is disabled. The runner explicitly adds
only that fresh temporary directory to the child import path, so the
Strang checker can import the sibling `audit_exact_subflows` module.
Installed system/virtual-environment site packages remain available.

The checker scripts make no network requests. This is filesystem/input
isolation, **not** a network sandbox or a standard-library-only execution.
The runner requires zero exit codes, empty stderr, valid JSON, strict
structural/discrete agreement, numerical agreement within the tolerances
below, and the additional stated regression checks. It reports exact JSON
equality separately when it happens. The scripts emit their results to
stdout; they do not rewrite the shipped result files. Any unexpected file
created in the temporary directory is rejected. The original package is
not modified, and the temporary directory is removed after the run.

`REPLAY_VERIFICATION.json` records the packaging-time run. A later run's
timestamp, elapsed time and potentially last numerical digits can differ.
The final frozen package was separately manifest-checked and replayed.

## Precision schedules and actual checks

### Two-sided affine formulas: nine cases

`check_affine_counterexample.py` uses mpmath to compare a literal K, S, L
formula with a cancellation-aware algebraic rearrangement. Four cases use
λ=10,100,1000,10000 with τ=0.1 and η=0.01, at max(100,int(0.1λ)+60)
decimal digits. Five cases use n=10,30,100,300,1000 with λ=n² and
τ=η=1/n, at max(100,n+60) digits. High-precision values are converted to
ordinary floats for several reported fields, so those saved fields do
not carry the full working precision. At sufficiently high precision,
a tiny printed residual can become 0 on that conversion.

The wrapper requires each literal-versus-rearranged residual below 10⁻⁴⁰
and each tested K norm positive. The last diagonal-sequence error is
about 0.1767773985, approaching the analytically proved 1/(4√2).

### Rank-two regression: 24 cases

`check_subclass_identities.py` uses NumPy's seeded generator (1829), SciPy
matrix exponentials and double precision. Dimensions are 4-by-3, rank two;
the second initial singular value ranges down to 10⁻⁸. It checks homogeneous
separable exactness, the right-affine projection identity, the left-affine
endpoint identity and the conditional local error bound.

Both the script and wrapper require each identity discrepancy below
10⁻¹⁰ and local error at most the displayed bound plus 10⁻¹². The recorded
maximum identity discrepancy is about 5.5868×10⁻¹⁶. These tolerances
accommodate floating-point calculations; they do not prove uniformity
over all ranks, meshes, stiffnesses or singular values.

### Literal affine subflows: nine cases

`audit_exact_subflows.py` independently integrates each affine subflow by
an augmented matrix exponential using mpmath. Its two-sided and ordinary
one-sided families use n=30,100,300 at max(100,n+60) digits. The rough-
initialization family uses n=100,1000,10000 at max(100,int(√n)+60) digits,
with λ=n², α=n^(−1/4), and τ=η=1/n.

The wrapper requires each reported K-formula, S-cancellation and
projection-identity residual below 10⁻⁴⁰. The recorded error at n=300 is
about 0.1767844082 for the two-sided example and 0.7071067812 for the
one-sided example. At n=10000 the rough-initializer error is
indistinguishable from 1 at the printed precision. These observations do
not establish limits; the analytic proofs do.

### Standard Strang: four cases

`check_strang_obstruction.py` calls the literal affine-subflow routine for
KSL(τ/2), then calls it on the transposed equation to implement LSK(τ/2).
It uses n=10,30,100,300, α=η=τ=1/n and λ=n⁴, at max(100,n+80) digits.
The displayed decimal strings have the significant digits requested by
the script, not all working digits.

The script and wrapper require an adjoint endpoint-identity residual below
10⁻⁵⁰, an LSK error at most 2h‖C‖ plus 10⁻⁵⁰, positive tested S endpoints,
and nonzero QR/output endpoints. At n=100 the printed Strang error is
0.9999999999999999999903558; at n=300 it is 1. Entire-subflow rank
preservation is established in the manuscript/audit, not by endpoint
positivity tests alone.

## Saved-result comparison tolerances

For NumPy/SciPy result values, the runner compares actual and expected
values using absolute tolerance **10⁻¹²** and relative tolerance **10⁻¹⁰**.
For mpmath output, including decimal strings and float-converted fields,
the tolerances are **10⁻⁴⁵** absolute and **10⁻¹²** relative. The condition is
|actual−expected| ≤ atol + rtol·max(|actual|,|expected|). Decimal comparisons
use Python's Decimal with 80 digits and an expanded exponent range; this
does not make the original mpmath computation exact.

JSON object keys, array lengths, booleans, integer parameters and descriptive
strings must match exactly. Every numerical value must be finite. The
additional residual/bound thresholds above apply even when reference values
match. Numeric reference agreement is a regression test, not a certificate
that the reference itself is mathematically valid.

## Limits and acceptance basis

All four checks are **NUMERICAL CORROBORATION**, not exact arithmetic,
interval enclosures, symbolic identities, formal proof checking or external
peer review. Arbitrary precision reduces cancellation error in these
finite examples but does not prove an asymptotic statement. Read the full
analytic proofs and independent mathematical audit for the accepted
counterexamples and conditional bounds. The original broad problem remains
**UNSOLVED**; 5/5 counts mathematical avenues, not claimed independent
historical sessions.
