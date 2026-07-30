# Exact verification and reproducibility package

Version: **1.1.0**

Immutable source tag:
`qubit-povm-pvm-minimum-settings-v1.1.0`

Tag target:
`773356a1de85290c3e85a361e0019f5f82b8e6d9`

This is the dependency-complete software and expert-review package for
“Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation.”

The mathematical result concerns shared-randomness-convexified fixed-qubit
behavior sets. It does not assert equality of raw strategy images,
same-state simulation, or operator-level projective simulability of
individual POVMs.

## Contents

- `artifacts/`: exact symbolic certificates and machine-readable data.
- `paper/`: manuscript source, bibliography, figures, publication PDF, and
  line-numbered review PDF.
- `reports/`: proof, dependency, equivalence, priority, risk, readiness,
  revision, and verifier reports.
- `review_packet/`: theorem summary, proof roadmap, load-bearing lemma index,
  theorem-to-artifact map, and focused reviewer questions.
- `run_all.sh`: one-command exact verification.
- `VERSION.txt`: immutable version and source identification.
- `SHA256SUMS.txt`: checksums for every other file in this ZIP.

Private or submission-specific editorial materials are intentionally excluded
from this software archive.

## Exact verification

Run from the top-level directory:

```sh
./run_all.sh
```

The reference environment is Python 3.14.6 with SymPy 1.14.0. The exact
verification path uses rational and algebraic arithmetic and does not require
network access.

To rebuild both 34-page PDFs with Tectonic 0.16.9:

```sh
./paper/build.sh
```

Passing the executable checks verifies encoded finite algebraic identities and
explicit constructions. It is not formal verification or independent peer
review and does not replace the universal mathematical arguments in the
manuscript.

## License

Paper, reports, figures, and machine-readable mathematical data are under
CC BY 4.0. Verification source code is under the MIT License. The bundled
third-party `paper/lineno.sty` is under LPPL 1.3a or later as stated in that
file. See `LICENSE`.

