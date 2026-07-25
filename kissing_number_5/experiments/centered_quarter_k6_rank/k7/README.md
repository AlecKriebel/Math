# Centered quarter-grid K7 rank investigation

This folder continues the local consistency hierarchy from the exact direct
K6 triangle-marginal certificate.

Two questions are kept separate:

1. Does the **particular** symmetric 51-orbit K6 distribution extend with
   exactly the same K6-face marginal?
2. Does some symmetric rank-five K7 distribution realize the original
   centered pair/triple marginal after allowing the K6 marginal to change?

The first question has an exact finite negative answer in
`fixed_support_proof.md`.  It is support-specific and is not a global
spherical-code obstruction.

The second question has an exact positive answer in
`direct_k7_triangle_proof.md`.  A 51-atom symmetric distribution on
rank-exactly-five K7 Gram matrices realizes the original pair and triangle
marginals.  Thus changing the K6 marginal again bypasses the sparse-support
obstruction.

Exact reproduction:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k7/verify_fixed_support_obstruction.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k7/verify_direct_k7_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k7.test_fixed_support_obstruction \
  experiments.centered_quarter_k6_rank.k7.test_direct_k7_triangle_extension -v
```
