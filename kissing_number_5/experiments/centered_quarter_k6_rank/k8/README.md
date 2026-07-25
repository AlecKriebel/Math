# Centered quarter-grid K8 rank investigation

This folder continues the local consistency hierarchy from the exact direct
K7 triangle-marginal certificate.

Two questions are kept separate:

1. Does the **particular** symmetric 51-orbit K7 distribution extend with
   exactly the same K7-face marginal?
2. Does some symmetric rank-five K8 distribution realize the original
   centered pair/triple marginal after allowing the K7 marginal to change?

The first question has an exact finite negative answer in
`fixed_support_proof.md`.  It is support-specific and is not a global
spherical-code obstruction.

The second question has an exact positive answer in
`direct_k8_triangle_proof.md`.  A 51-atom symmetric distribution on
rank-exactly-five K8 Gram matrices realizes the original pair and triangle
marginals.  Thus changing the K7 marginal again bypasses the sparse-support
obstruction.

Exact reproduction:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k8/verify_fixed_support_obstruction.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k8/verify_direct_k8_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k8.test_fixed_support_obstruction \
  experiments.centered_quarter_k6_rank.k8.test_direct_k8_triangle_extension -v
```

The deterministic discovery pipeline is:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k8/search_direct_k8.py \
  experiments/centered_quarter_k6_rank/k8/results/direct_k8_from_51.csv
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k8/solve_direct_k8_lp.py \
  experiments/centered_quarter_k6_rank/k8/results/direct_k8_from_51.csv \
  experiments/centered_quarter_k6_rank/k8/results/direct_k8_from_51_lp.json
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k8/certify_direct_k8.py \
  experiments/centered_quarter_k6_rank/k8/results/direct_k8_from_51.csv \
  experiments/centered_quarter_k6_rank/k8/results/direct_k8_from_51_lp.json \
  experiments/centered_quarter_k6_rank/k8/direct_k8_triangle_extension.json
```

Discovery used CPython 3.14.6, NumPy 2.5.1, and SciPy 1.18.0.  The two
verifiers use only the Python standard library and do not trust the
discovery solver.
