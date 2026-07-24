# Centered quarter-grid K10 rank investigation

The direct hierarchy continues through K10: an exact 51-atom symmetric
distribution on rank-exactly-five K10 Gram matrices realizes the original
pair and triangle marginals.  See `direct_k10_triangle_proof.md`.

The frozen K9 support was not exhaustively glued.  An exact orbit audit
finds 16,057,440 labeled support matrices and proves that a complete gluing
has at least 112,402,080 missing-edge color trials, before accounting for
its roughly half-gigabyte pair of packed support/overlap arrays and prefix
index.  See `frozen_support_note.md`.  This size audit is not an obstruction.

Exact verification:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k10/verify_frozen_support_size.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k10/verify_direct_k10_triangle_extension.py
PYTHONPATH=. .venv/bin/python -m unittest \
  experiments.centered_quarter_k6_rank.k10.test_frozen_support_size \
  experiments.centered_quarter_k6_rank.k10.test_direct_k10_triangle_extension -v
```

The deterministic discovery pipeline is:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k10/search_direct_k10.py \
  experiments/centered_quarter_k6_rank/k10/results/direct_k10_from_51.csv
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k10/solve_direct_k10_lp.py \
  experiments/centered_quarter_k6_rank/k10/results/direct_k10_from_51.csv \
  experiments/centered_quarter_k6_rank/k10/results/direct_k10_from_51_lp.json
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k10/certify_direct_k10.py \
  experiments/centered_quarter_k6_rank/k10/results/direct_k10_from_51.csv \
  experiments/centered_quarter_k6_rank/k10/results/direct_k10_from_51_lp.json \
  experiments/centered_quarter_k6_rank/k10/direct_k10_triangle_extension.json
```

Discovery used CPython 3.14.6, NumPy 2.5.1, and SciPy 1.18.0.  The direct
verifier uses only the Python standard library.  The size-audit wrapper uses
the Python standard library and compiles its C++20 standard-library core;
the recorded run used Apple clang 21.0.0.
