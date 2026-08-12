# Exact verifier archive for PRA review

This compact archive accompanies *Minimum Bell-Setting Complexity for Qubit
POVM–PVM Separation*, version 1.2.0. It contains only the material needed to
rerun the finite exact certificates:

- `artifacts/` with the exact inputs and three verification programs;
- `run_all.sh` and the pinned Python/SymPy environment files;
- `theorem_to_artifact_map.md` and the frozen verifier transcript; and
- citation, provenance, version, license, and checksum metadata.

From the extracted archive root, with Python 3.14.6 and SymPy 1.14.0:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHON=.venv/bin/python ./run_all.sh
```

The executable checks cover finite exact identities and explicit
constructions. They do not formally verify the manuscript's universal
convexity, extremality, physical-reconstruction, multiplier, or
rank-exhaustion arguments.
