# Exact verification

The universal assertions are proved in `paper.tex`. These executable checks test
the accompanying formulas and limiting examples and are not proof certificates.

Use Python 3 (the recorded reproduction names its exact version):

```
python3 -m venv .venv
.venv/bin/python -m pip install -r verification/requirements.txt
.venv/bin/python -B verification/independent_checks.py > verification/independent_results.json
```

The independent script reruns the inspected original `source_snapshot/checks.py`
and preserves the original snapshot bytes. Its checks include an independent
auxiliary-circle elimination, the exact separating value 16, denominator
conditions, real general-position witnesses, and a non-orthonormal-ellipse
perturbation. The original script adds the candidate's original examples.

`original_snapshot_manifest.json` binds the immutable PR #9 head
`a29887ed0e341851d02fa992c26500d4089267be`. It is historical provenance, not a
claim that the shortened research note is byte-identical to that source.
`PACKAGE_MANIFEST.json` inside the built source archive binds the new source
files and the separately deposited PDF.

The source archive does not include third-party publisher PDFs, installed
dependencies, credentials, or publication receipts. Source URLs and recorded
hashes let readers retrieve the priority evidence independently.
