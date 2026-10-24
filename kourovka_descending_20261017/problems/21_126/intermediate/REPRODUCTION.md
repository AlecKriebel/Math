# Reproduction of this research checkpoint

From the repository root, run the following with Python 3. All verification uses the standard library and exact integers/rationals; no GAP, Sage, SciPy, network, or downloaded paper is needed for the computations.

```sh
python3 kourovka_descending_20261017/problems/21_126/intermediate/check_positive_transitions.py
python3 kourovka_descending_20261017/problems/21_126/intermediate/check_dead_edge_example.py
python3 kourovka_descending_20261017/problems/21_126/intermediate/review/verify_rectangles.py
python3 kourovka_descending_20261017/problems/21_126/intermediate/review/verify_transitions.py
python3 kourovka_descending_20261017/problems/21_126/intermediate/review/verify_zero_directions.py
```

The scripts write arithmetic certificates next to themselves. Timestamp fields in regenerated certificates can differ. Read each script and its scope statement: these are exact consistency checks for local formulas and explicit models, not computations of a general Dehn function.

The proofs are in the authored notes. `SOURCE_MANIFEST.json` records primary theorem locators and downloaded-file hashes. Raw third-party papers in `sources/` are local reference material and should be excluded from the publication/checkpoint package. No publication-ready preprint is claimed because 21.126 remains unresolved.
