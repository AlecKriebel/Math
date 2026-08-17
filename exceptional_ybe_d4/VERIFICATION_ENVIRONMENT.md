# Verification environment

Version 1.1.3 was certified on 16 August 2026 on an Apple M1 Pro Mac running
macOS, using the following reference environment:

- CPython 3.14.6 with optimization disabled;
- SymPy 1.14.0;
- mpmath 1.3.0;
- Tectonic 0.16.9;
- Tectonic default bundle v33;
- `SOURCE_DATE_EPOCH=1786930200` (16 August 2026, 18:30 PDT).

Create a clean environment and install the two universal wheels with their
published hashes:

```text
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: \
  -r requirements.txt
```

Run the three supported exact routes, negative tests, and package-integrity
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
  `b24067217009d8fbee4e412ef5b02dd3c4923de8ac699a19900a97de5524f83f`.
- Final PDF SHA-256:
  `af1255b7702f78e73ba9981ca29d2cdfffcb26e6aa093b7b5d0a2bcaebf03ec8`.

The exact programs certify the displayed finite matrix identities, both
partial traces, both dimension-three obstruction trace-square identities,
the generalized operator and far commutativity, the literal GHR comparison
and six-dimensional three-strand image, and the generic tensor-word
certificate.
They do not replace the printed proofs of tower faithfulness, the
dimension-three classification reduction, or the literature-based priority
claim.
