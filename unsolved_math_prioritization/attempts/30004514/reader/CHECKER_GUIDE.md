# Reproducible checker guide

The authored analytic arguments establish the counterexamples. These scripts check finite symbolic identities, exact constants, and illustrative numerical integrals. They do not establish global convexity, all-direction sign, smooth infinite-dimensional inversion, or the existential parameter choice by sampling.

## Integrity first

From this reader directory, run:

```sh
python -B checks/verify_integrity.py
```

This requires only the Python standard library. It checks the complete public-file allowlist, file hashes and byte counts, original/output mapping, the cross-review pins for both full proofs, and exact reconstruction of the derived WXY checker from its five listed edits. The manifest excludes its own digest to avoid self-reference; its digest is supplied in the companion archive receipt. Integrity checking establishes byte identity relative to those pins, not mathematical truth or cryptographic authorship.

## Diagnostic environment

The recorded replay used Python 3.12.14 with:

- SymPy 1.14.0
- mpmath 1.3.0
- SciPy 1.17.0
- NumPy 2.3.5

A compatible Python environment with those packages is sufficient. If necessary, install these packages into an isolated environment from the official Python package registry; the checker itself neither installs software nor accesses the network. Other library versions can cause small quadrature or formatting differences. The analytic proof does not rely on reproducing the exact last floating-point digit.

## Replay all supported modes

Run:

```sh
python -B checks/replay_diagnostics.py
```

The runner copies the pinned checker bytes into temporary directories, executes normal, `-O`, and `-OO` Python modes, reads the generated result files, and emits one JSON receipt to standard output. It does not overwrite the recorded evidence files. To save a new receipt, redirect output to a location outside the reader directory. An extra file inside the directory deliberately fails the strict allowlist integrity check.

The six positive runs are:

- MTY preserved `mty/check_constants.py`, in normal, `-O`, and `-OO` modes. Its explicit `require` checks remain active in each mode.
- WXY derived `checks/wxy_normalizations_checked.py`, in normal, `-O`, and `-OO` modes. This copy replaces exactly five `assert` statements with explicit conditional raises, leaving all formulas, loops, tolerances, and result generation unchanged.

The original WXY file is preserved at `wxy/verify_normalizations.py` for provenance. **Do not treat a direct `python -O` or `python -OO` run of that original file as assertion-enforced validation.** Python strips its five `assert` statements. The exact byte-range replacement map is in `integrity/CHECKER_DERIVATION.json`; `verify_integrity.py` reconstructs and checks the derived file from that map.

Three additional negative-control runs force an incorrect WXY spectral residual in a temporary copy. Each Python mode must reject it with an `AssertionError`; no result file may be produced. This checks that failure enforcement remains active, and is not evidence for the mathematical theorem.

## What the diagnostics check

MTY:

- Exact first and second seed derivatives, positive rational convexity margin, cap width and strict cap sign, and polar inverse value
- Thirteen even-degree Radon eigenvalue cases, degrees 0 through 24, including the stated inverse bound
- The two radial Fourier constants that disprove the inspected complementary-degree identity as stated
- High-precision quadrature illustrations of two exact ellipsoid transform identities at five chosen directions

WXY:

- Eighty exact eigenvalue normalizations: dimensions 3 through 10 and odd degrees 1 through 19
- Exact derivatives of the displayed latitude primitives for dimensions 3 and 4
- Numerical phase cancellation in dimensions 3, 4, 5, and 8, with the original tolerances retained
- A sampled half-shift identity, supplementary to the exact argument in the proof

[checks/REPLAY_RESULTS.json](checks/REPLAY_RESULTS.json) records the accepted run, dependency versions, generated result hashes, and negative controls. The original recorded mathematical output JSON files are unchanged. A byte-for-byte output mismatch in another compatible environment can result from floating-point or package-version differences; symbolic results and the scripts' explicit tolerances must still pass.

## Reading the acceptance boundary

The diagnostic scripts do not construct an explicit numerically certified body. They do not choose a certified value of the small perturbation or intermediate-value parameter. Those choices are rigorously existential in the authored proofs. The WXY supplement additionally relies on its explicitly stated standard harmonic-analysis prerequisites. Neither a successful checker nor this reader changes WXY's submitted-preprint status.
