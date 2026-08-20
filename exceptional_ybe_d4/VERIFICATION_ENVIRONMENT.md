# Verification environment

Version 1.2.0 was certified on 19 August 2026 on an Apple M1 Pro Mac running
macOS, using the following reference environment:

- CPython 3.14.6 with optimization disabled;
- SymPy 1.14.0;
- mpmath 1.3.0;
- Tectonic 0.16.9;
- Tectonic default bundle v33;
- `SOURCE_DATE_EPOCH=1787176800` (19 August 2026, 15:00 PDT).

Create a clean environment and install the two universal wheels with their
published hashes:

```text
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: \
  -r requirements.txt
```

Run the five supported exact routes, negative tests, and package-integrity
check:

```text
YBE_PYTHON=.venv/bin/python ./run_all.sh
.venv/bin/python test_failure_modes.py
.venv/bin/python verify_checksums.py
```

The standard-library route and abstract word route do not need SymPy, but the
single locked interpreter makes the complete run easier to audit. Scientific
checks use explicit failures and every supported verifier rejects optimized
Python. `verify_supplied_original.py` is an archival input, not a supported
execution path.

Rebuild the paper with the pinned Tectonic version and bundle:

```text
./build_paper.sh
```

`verification_output.txt` is the frozen standard output of `run_all.sh` in
the reference environment. `SHA256SUMS` records the final PDF and all
package-local source artifacts. The Zenodo upload hashes are in
`submission/SHA256SUMS`; the isolated arXiv archive hash is in
`submission/ARXIV_SHA256SUMS`.

- Frozen verification output SHA-256:
  `108233f563373cc2b3e3e9fb4012f7f8ea52fb1149f58c2f6795344bfc5f3064`.
- Standalone concurrent-equivalence output SHA-256:
  `69aec973c78bdc44e1a4fa4f11e4c467c715dd2ca83a90b7c7c2d898dffd15bc`.
- Standalone braid-and-link output SHA-256:
  `9081354712384deef6043ad15c2d6f28f8a4b7988148fc1d246a77b02ae0042a`.
- Final PDF SHA-256:
  `a769689a4b5b9c48bf675f79d3b80916a7821ad5a8db0b9ec246df460dffb8de`.

The exact programs certify the displayed finite matrix identities, both
partial traces, both dimension-three obstruction trace-square identities,
the generalized operator and far commutativity, the literal GHR comparison
and six-dimensional three-strand image, and the generic tensor-word
certificate. The fourth route independently checks the literal
Galindo--Rowell Family III formula, the intrinsic quaternionic factorization,
the site reversal, and the displayed local unitary.
The fifth route separately rechecks the intrinsic factorization, displayed
unitary, and exact two-site comparison, then checks the enhancement constants,
matrix skein identity, local order, two- and three-strand link values, the
standard-frame non-Clifford witness, ordered Pauli quarter-turns, and the
site-reversal and Garside conjugacies at strand numbers three and four. These
finite checks do not replace the printed tower-faithfulness and all-strand
proofs, the dimension-three classification reduction, or the source-based
concurrent and topological interpretations.
