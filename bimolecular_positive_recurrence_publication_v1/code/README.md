# Standalone verification package

This package accompanies Version 1.0 of *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*.

## Reproduce the committed report

Python 3.11 or newer is required. The verifier uses only the Python standard library; no installation, package manager, network access, or third-party runtime dependency is needed.

```bash
./reproduce.sh
```

The script uses `python3` by default. To select another interpreter:

```bash
BIMOL_PYTHON=python3.12 ./reproduce.sh
```

The script:

1. checks the interpreter version;
2. runs the complete unit-test suite directly from `src` via `PYTHONPATH`;
3. generates the canonical report twice in a temporary directory;
4. requires the two generated files to be byte-identical; and
5. requires the regenerated file to be byte-identical to the committed `verification_report.json`.

It never overwrites the committed golden report. Environment-specific provenance, including the Python and platform versions, is emitted separately and is not part of the canonical JSON.

## What is checked

The exact symbolic and combinatorial checks include:

- 3,318 falling-factorial residual-identity instances spanning carried targets, next sources, and channel outcomes;
- 172 exact checks of both sides of the source-probability entropy rewrite, represented as rational prime-exponent signatures, including the zero complex, parallel source channels, pure binary complexes, and mixed complexes;
- every branch and boundary case in the exact scalar-envelope atlas, including
  pointwise monotonicity;
- an exhaustive 98,261-case three-species top-complex audit covering all 1,013 nontrivial subsets of the ten bimolecular complexes, 55 normalized rational weights, and every enlargement of positive-weight support by zero-weight divergent coordinates;
- independent validation of every availability or invariant certificate before it enters the atlas digest; and
- explicit boundary-face, absorbing-singleton, finite-class, parity,
  channel-marking, zero-length-path, target-following-cycle, random-time
  Foster, regenerative occupation, and rate-degeneration calibrations.

The package also runs 5,000 certificate-validated, fixed-seed four-species classifications with seed `20260806`. These random cases are stress tests only and are not used as proof.

`verification_report.json` is canonical JSON with sorted keys and fixed separators. Its mathematical output is independent of Python version, operating system, timestamps, elapsed times, temporary paths, and generated transcripts. Its source hashes come from the closed allowlist `SOURCE_FILES` in `src/bimolecular_pr/verification.py`; an unlisted Python source or test causes verification to fail.

The universal theorem is proved in the manuscript. Finite enumeration and software tests are adversarial calibration, not substitutes for that proof.

## Optional installation

Installation is unnecessary for reproduction. If desired, the included dependency-free build backend supports a regular local install with a sufficiently recent Python packaging frontend:

```bash
python3 -m pip install .
```

## Citation and source

Citation metadata, including the author's ORCID, is provided in
`CITATION.cff`. The maintained Version 1.0 source is in the
[Math repository](https://github.com/AlecKriebel/Math/tree/bimolecular-positive-recurrence-v1.0/bimolecular_positive_recurrence_publication_v1/code).
No DOI has been assigned to this software release.
