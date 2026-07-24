# Centered atomic BV barrier

## Scope

This experiment asks whether centering alone can make the fixed-cardinality
two/three-point relaxation infeasible at \(N=41\).  It does not.

The numerical search uses the quarter grid, exact centered first-moment
constraint, the forced centered kernels in \(W_0\) and \(W_1\), robust
pair-mass consequences at \(1/300\), full-radial BV blocks through degree 16,
ordinary pair moments through degree 60, common-pair capacities, and 27
rank-aware harmonic cuts.

The numerical output is only a discovery input.  `rationalize.py` rounds it,
then restores every mass, marginal, centered-moment, and centered-kernel
equality with exact rational Gaussian elimination.  The independent
standard-library verifier proves the resulting exact witness works at every
harmonic and pair degree.

## Discovery reproduction

Environment:

- Python 3.14.6
- CVXPY 1.9.2
- NumPy 2.5.1
- SciPy 1.18.0
- Clarabel through CVXPY

From the repository root:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/continuous_rank_bv_search/search.py \
  --grid quarter \
  --harmonic-degree 16 \
  --pair-degree 60 \
  --kernel-profile rich \
  --pair-mode local-baseline \
  --centered \
  --robust-vertex-marginals \
  --solver CLARABEL \
  --output \
    experiments/continuous_rank_bv_search/results/centered_quarter_local_d16.json

PYTHONPATH=. .venv/bin/python \
  experiments/centered_atomic_bv_barrier/rationalize.py

PYTHONPATH=. .venv/bin/python \
  experiments/centered_atomic_bv_barrier/extend_k4.py

clang++ -O3 -std=c++17 \
  experiments/centered_atomic_bv_barrier/enumerate_k5.cpp \
  -o /tmp/kissing5-enumerate-k5
/tmp/kissing5-enumerate-k5 \
  experiments/centered_atomic_bv_barrier/results/k5_triangle_vectors.csv

PYTHONPATH=. .venv/bin/python \
  experiments/centered_atomic_bv_barrier/extend_k5.py \
  experiments/centered_atomic_bv_barrier/results/k5_triangle_vectors.csv
```

The floating solver status and objective are not proof data.  The exact
certificate authenticates the numerical source only to make the discovery
history reproducible.

## Exact verification

```sh
python3 verifiers/verify_centered_quarter_bv_all_harmonics.py
python3 verifiers/verify_centered_quarter_k4_extension.py
python3 verifiers/verify_centered_quarter_k5_extension.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/verify_fixed_support_obstruction.py
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/verify_direct_k6_triangle_extension.py
python3 -m unittest \
  tests.test_centered_quarter_bv_all_harmonics \
  tests.test_centered_quarter_k4_extension \
  tests.test_centered_quarter_k5_extension -v
```

The verifier does not import CVXPY, NumPy, SciPy, the search program, or the
rationalization program.  It reconstructs every support determinant, mass
identity, design kernel, rational \(LDL^{\mathsf T}\) pivot, infinite
harmonic tail bound, infinite ordinary-pair tail bound, robust pair mass,
and sharp rank residual from the stored fractions.
The second verifier independently enumerates all 117,649 edge labelings,
checks every principal minor, and verifies the exact edge and triangular-face
marginals of the 51-atom local \(K_4\) extension.
The third verifier checks all principal minors and the exact edge and
triangular-face marginals of the 51-atom local \(K_5\) extension.  Its
existence claim does not depend on trusting the much larger discovery
enumeration or the floating LP.
The separate \(K_6\) package proves both that this particular \(K_5\)
mixture has no compatible \(K_6\) face extension and that a different local
\(K_6\) mixture with the same pair/triple marginals exists.  Every atom in
the latter is PSD of rank exactly five.

## Interpretation

This is not a 41-point configuration.  It is an exact counterexample to a
proposed centered two/three-point relaxation argument.  It even has a
symmetric distribution of locally Gram-PSD patterns through five vertices.
It even has a local rank-five six-point mixture after changing the
intermediate marginal.  A full higher-point moment-PSD condition,
overlapping-subset consistency, or a genuinely complete common rank-five
Gram condition remains necessary.
