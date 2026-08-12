# Exact verification and reproducibility package — version 1.2.0

This archive accompanies *Minimum Bell-Setting Complexity for Qubit
POVM–PVM Separation*. It is the self-contained software/reproducibility object
prepared for a new version of Zenodo concept DOI
[`10.5281/zenodo.21699223`](https://doi.org/10.5281/zenodo.21699223).

## Contents

- `artifacts/`: manifest-pinned exact coefficient, strategy, symbolic-verifier, and
  rank-zero simulator sources;
- `paper/`: one canonical mathematical source, thin build wrappers, figures,
  archival, line-numbered, and PRA PDFs, and the official REVTeX 4.2f runtime;
- `reports/`: proof, dependency, comparison, priority, risk, regression, and
  readiness audits plus the fresh verifier transcript;
- `review_packet/`: theorem summary, proof roadmap, load-bearing lemma index,
  theorem-to-artifact map, and focused reviewer questions;
- `run_all.sh`: one-command offline exact verification; and
- version, citation, provenance, license, dependency, and checksum metadata.

No private correspondence, journal-planning material, temporary numerical
search output, virtual environment, Git history, or build scratch file is
included.

## Run the checks

Use Python 3.14.6 and SymPy 1.14.0, then run from the archive root:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHON=.venv/bin/python ./run_all.sh
```

The programs verify finite exact identities and explicit constructions. The
universal convexity, extremality, physical-reconstruction, multiplier, and
rank-exhaustion arguments are mathematical proofs in the manuscript rather
than proof-assistant-verified theorems.

## Licenses

Verification source code is MIT licensed. Manuscript text, reports, figures,
and machine-readable mathematical data are CC BY 4.0. The vendored
`paper/lineno.sty` and official REVTeX 4.2f materials retain the LPPL terms
documented with those files. See `LICENSE`.
