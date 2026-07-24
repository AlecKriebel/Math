# Quadratic-positive residual and weighted-isotropy audit

## Status

This folder continues from the exact \(-1/50\) enlarged-cap theorem in
`../quadratic_positive_locus/`.  It contains two separate results:

1. an exact positive-width subregion of normalized quadratic separators
   whose positive loci lie in a certified cap; and
2. an explicit audit showing that eliminating every quadratic separator
   would still leave the nonnegative weighted two-design branch unresolved.

It does **not** prove \(\tau(5)=40\).

## Exact results

[`top_eigen_cap_subregion.md`](top_eigen_cap_subregion.md) proves a
three-parameter semialgebraic cap-containment criterion in terms of
\(\lambda_4\), the top-axis coefficient \(b_5\), and
\(\|(b_1,\ldots,b_4)\|\).  It includes, for example,
\[
\lambda_4\leq0,\quad b_5\geq2,\quad
\|(b_1,\ldots,b_4)\|\leq99/2500.
\]
Every kissing code in these positive loci has at most 39 points.

[`weighted_branch_audit.md`](weighted_branch_audit.md) derives the exact
weighted projection, stress, Gram, and \(B\)-matrix identities.  Its main
warning is:

> QPL would establish only the existence of nonnegative weights.  It does
> not force uniform weights, unweighted centering, or an unweighted tight
> frame.

The exact verifier constructs:

- the sharp six-point regular-simplex weighted code;
- a 40-point \(D_5\) code with full-support nonuniform design weights;
- the same 40-point code with design weights supported on only 12 roots.

It also verifies the universal bounds
\[
p_i\leq1/6,\qquad
\sum_{\langle u,x_i\rangle<-1/50}p_i\geq9/98.
\]

`verify_local_depth_weight_countermodel.py` gives an exact 41-vertex
graph-and-weight relaxation showing that the current cap counts and
weighted deep-mass inequalities do not contradict one another.

[`harmonic_metzler_shadow.md`](harmonic_metzler_shadow.md) records the
global low-rank transform.  The weighted branch produces a centered
41-point spherical shadow of rank at most 19 with off-diagonal interval
\([-21/104,3/13]\).  Dropping its Veronese origin is presently too weak.

## Numerical attacks

`analyze_near_minimizers.py` scans existing unrestricted construction
artifacts.  All 132 distinct stored 41-point arrays admit numerical
nonnegative weighted two-designs.  All 102 with maximum inner product below
0.55 admit robust full-support solutions.

`analyze_best_weighted_transform.py` shows that the best current
near-minimizer satisfies the weighted projection, equilibrium, rank, and
harmonic-shadow equations to floating precision.  Its only decisive
failure is the original kissing inequality: the maximum inner product is
about 0.51499465, creating negative off-diagonal entries in the Metzler
transform.

These computations are `NUMERICAL EVIDENCE ONLY`.

## Reproduction

Exact checks:

```sh
python3 -m unittest discover \
  -s experiments/quadratic_positive_residual -p 'test_*.py' -v
```

The exact verifiers use always-on exceptions.  The tests also execute
valid and deliberately invalid inputs under `python -O`, ensuring that
optimized mode cannot erase proof-critical checks.

Numerical scans:

```sh
.venv/bin/python \
  experiments/quadratic_positive_residual/analyze_near_minimizers.py \
  --output \
  experiments/quadratic_positive_residual/near_minimizer_weighted_designs.json
.venv/bin/python \
  experiments/quadratic_positive_residual/analyze_best_weighted_transform.py \
  --output \
  experiments/quadratic_positive_residual/best_weighted_transform.json
```

## Precise remaining branches

- Quadratic-separation branch: prove the residual positive-locus occupancy
  bound outside the exact cap subregions.
- Weighted-isotropy branch: rule out \(N=41\) solutions of
  \[
  G\succeq0,\ \operatorname{rank}G=5,\ G_{ii}=1,\ G_{ij}\leq1/2,\quad
  p\geq0,\ {\bf1}^{\mathsf T}p=1,\ Gp=0,\ GPG=G/5.
  \]

Both are theorem-strength gaps.  Neither may be replaced by an assumption
of uniformity or full support.
