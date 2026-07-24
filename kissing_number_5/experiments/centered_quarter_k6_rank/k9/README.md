# Centered quarter-grid K9 rank investigation

This folder continues the local consistency hierarchy from the exact direct
K8 triangle-marginal certificate.

Two questions are kept separate:

1. Does the **particular** symmetric 51-orbit K8 distribution extend with
   exactly the same K8-face marginal?
2. Does some symmetric rank-five K9 distribution realize the original
   centered pair/triple marginal after allowing the K8 marginal to change?

The first question has an exact finite negative answer in
`fixed_support_proof.md`.  It is support-specific and not a global
spherical-code obstruction.

The second question has an exact positive answer in
`direct_k9_triangle_proof.md`.  A 51-atom symmetric distribution on
rank-exactly-five K9 Gram matrices realizes the original pair and triangle
marginals.  Changing the K8 marginal again bypasses the sparse-support
obstruction.

Exact reproduction:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k9/verify_fixed_support_obstruction.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k9/verify_direct_k9_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k9.test_fixed_support_obstruction \
  experiments.centered_quarter_k6_rank.k9.test_direct_k9_triangle_extension -v
```

The deterministic discovery pipeline is:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k9/search_direct_k9.py \
  experiments/centered_quarter_k6_rank/k9/results/direct_k9_from_51.csv
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k9/solve_direct_k9_lp.py \
  experiments/centered_quarter_k6_rank/k9/results/direct_k9_from_51.csv \
  experiments/centered_quarter_k6_rank/k9/results/direct_k9_from_51_lp.json
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k9/certify_direct_k9.py \
  experiments/centered_quarter_k6_rank/k9/results/direct_k9_from_51.csv \
  experiments/centered_quarter_k6_rank/k9/results/direct_k9_from_51_lp.json \
  experiments/centered_quarter_k6_rank/k9/direct_k9_triangle_extension.json
```

Discovery used CPython 3.14.6, NumPy 2.5.1, and SciPy 1.18.0.  The direct
verifier uses only the Python standard library.  The fixed-support wrapper
uses the Python standard library and compiles its C++20 standard-library
core; the recorded run used Apple clang 21.0.0.  Neither verifier trusts the
discovery LP.
