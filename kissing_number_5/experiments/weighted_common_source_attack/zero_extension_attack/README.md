# Scalar zero-extension countermodel

This folder isolates the exact obstruction that survives after applying
all one-zero-point moment and strict-tail bounds independently.

Start with the exact 12-point weighted support and its exact Gram matrix
inside \(D_5\) from the parent checkpoint.  Eight weights are \(1/10\),
and four are \(1/20\).  The certificate gives 29 formal height profiles
with entries \(-1/2,0,1/2\).  Every profile has:

\[
\sum_i p_it_i=0,\qquad
\sum_i p_it_i^2=\frac15,
\]

support mass \(2/5\) at each of \(-1/2\) and \(1/2\), and hence satisfies
both strict-tail bounds.  Every two profiles also satisfy

\[
\sum_i p_it_i^{(y)}t_i^{(z)}\leq\frac1{10},
\]

which is the exact mixed-moment image of
\(\langle y,z\rangle\leq1/2\).

The verifier goes further: every \(3\)-by-\(3\) Gram determinant with two
support points and one formal zero point is nonnegative, and every such
determinant with one support point and two formal zero points is
nonnegative.

Thus the scalar relaxation has formal total size \(12+29=41\).
However, the profile matrix has exact rational rank 7.  The profiles do
not lie in the five-dimensional column space determined by the actual
support, so this is deliberately **not** a Gram matrix and not a
41-point construction.

The conclusion is precise: one- and two-zero-point scalar moments, strict
tail masses, all relevant triangle PSD constraints, and an exact sparse
support do not suffice.  A proof must enforce at least four-point
compatibility or the common rank-five realization (equivalently, the
exact linear relations among all height profiles induced by the support
Gram matrix).

`projection_membership.md` proves that common realization of one profile
is equivalent to a single exact quadratic equality
\[
h^{\mathsf T}PSPh=1/25.
\]
All 29 formal profiles obey the corresponding upper bound, but only two
saturate it.  This identifies the exact missing equality without assuming
a finite height alphabet.

## Reproduction

```sh
PYTHONPATH=experiments/weighted_common_source_attack/zero_extension_attack \
  python3 \
  experiments/weighted_common_source_attack/zero_extension_attack/verify_scalar_extension_countermodel.py
PYTHONPATH=experiments/weighted_common_source_attack/zero_extension_attack \
  python3 -m unittest \
  experiments/weighted_common_source_attack/zero_extension_attack/test_scalar_extension_countermodel.py -v
PYTHONPATH=experiments/weighted_common_source_attack/zero_extension_attack \
  python3 -O -m unittest \
  experiments/weighted_common_source_attack/zero_extension_attack/test_scalar_extension_countermodel.py -v
```

The verifier uses only the Python standard library and does not trust a
solver.
