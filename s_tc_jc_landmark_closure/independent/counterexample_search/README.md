# Independent counterexample search

This directory is a clean-room adversarial review of the proposed standard
strongly tree-child level-2 Jukes--Cantor classification.  It does not import
the historical graph, Fourier, atlas, canonicalization, or separator code.

The locked conventions are read from `../../docs/DEFINITIONS_LOCK.md`.  The
certified weak-class result is used only as a regression target and is not
treated as a move inside `S_TC`.

Status labels used here:

- `EXACTLY COMPUTED`: reproduced by finite exact arithmetic from primitive
  graph data;
- `PROVED`: accompanied by a mathematical completeness argument;
- `NUMERICALLY OBSERVED`: screening evidence only;
- `UNRESOLVED`: no certificate has been obtained.

No result in this directory is a proof of the global theorem unless its
stated enumeration and algebraic scope covers the quantified class.

## Main result of this subtask

See `COUNTEREXAMPLE_SEARCH_REPORT.md`.  No standard-strong non-`T`
counterexample was found.  The topology census is exact through five leaves;
the negative four- and five-leaf model searches are explicitly numerical.
The three-leaf tree/3-sunlet separation and the at-most-one-triangle lemma are
exact proofs.

## Reproduction

Run from this directory with the repository virtual environment:

```bash
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python regression_checks.py
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python exact_three_leaf_separator.py
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python check_local_stc_criterion.py
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python root_invariance_check.py \
  --census census_n5_deterministic.json.gz --max-n 5 \
  --output root_invariance_n5.json
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python \
  networkx_isomorphism_crosscheck.py \
  --census census_n5_deterministic.json.gz --max-n 5 \
  --output isomorphism_crosscheck_n5.json
```

The complete census can be regenerated (about five minutes on the audited
machine) with:

```bash
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python enumerate_census.py \
  --max-n 5 --output census_regenerated.json
gzip -n -9 -c census_regenerated.json > census_regenerated.json.gz
```
