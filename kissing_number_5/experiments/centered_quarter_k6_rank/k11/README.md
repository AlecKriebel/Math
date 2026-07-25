# Centered quarter-grid K11 rank investigation

The direct local hierarchy continues through K11.  An exact 51-atom
symmetric distribution on rank-exactly-five quarter-grid K11 Gram matrices
realizes the original pair marginal \(\alpha/40\) and triangle marginal
\(\nu/1560\).

The discovery catalog exhausts extensions of each of the 51 stored labeled
K10 atoms, but it is not a catalog of all possible K11 atoms.  See
`direct_k11_triangle_proof.md` for the exact scope.

Exact verification:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k11/verify_direct_k11_triangle_extension.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k11/verify_extension_catalog.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k11.test_direct_k11_triangle_extension \
  experiments.centered_quarter_k6_rank.k11.test_extension_catalog -v
```

Deterministic discovery replay:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k11/search_direct_k11.py \
  experiments/centered_quarter_k6_rank/k11/results/direct_k11_from_51.csv \
  --all-output \
  experiments/centered_quarter_k6_rank/k11/results/direct_k11_all_extensions.csv
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k11/solve_direct_k11_lp.py \
  experiments/centered_quarter_k6_rank/k11/results/direct_k11_from_51.csv \
  experiments/centered_quarter_k6_rank/k11/results/direct_k11_from_51_lp.json
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k11/certify_direct_k11.py \
  experiments/centered_quarter_k6_rank/k11/results/direct_k11_from_51.csv \
  experiments/centered_quarter_k6_rank/k11/results/direct_k11_from_51_lp.json \
  experiments/centered_quarter_k6_rank/k11/direct_k11_triangle_extension.json \
  --all-catalog \
  experiments/centered_quarter_k6_rank/k11/results/direct_k11_all_extensions.csv
```

Discovery used CPython 3.14.6, NumPy 2.5.1, and SciPy 1.18.0.  The exact
verifier uses only the Python standard library and does not trust the LP.
