# Zero is not an ℓ² eigenvalue of a regular-tree adjacency operator

Verified: 2026-10-07 04:34 UTC.

## Exact claim

Let `T_d` be the infinite connected `d`-regular tree, with `d >= 2`.
Its adjacency operator `A` on complex-valued `ℓ²(V(T_d))` is injective.
In particular, the claim holds for `d = 100`.

## Elementary proof

Write `q = d - 1`. The operator is bounded: vertexwise Cauchy–Schwarz
and regularity give `||Af||² <= d² ||f||²`. Thus `Af = 0` means the
finite-sum equation

`sum_{u adjacent to w} f(u) = 0`

at every vertex `w`.

Root the tree at a vertex `r`. Denote its distance-`n` sphere by `L_n`
and put

`M_n = sum_{v in L_n} |f(v)|²`.

Every nonroot vertex has one parent and exactly `q` children; the root
has `d` children. If `w` is a child of `v`, the zero-adjacency equation
at `w` says

`f(v) = -sum_{z child of w} f(z)`.

Consequently,

`|f(v)|² <= q sum_{z child of w} |f(z)|²`.

For `n >= 1`, sum this inequality over the `q` children `w` of each
`v in L_n`. All sets of grandchildren are disjoint, because the graph
is a tree. This gives

`M_{n+2} >= M_n`  for every `n >= 1`.

For the root the same argument gives

`M_2 >= (d/q) M_0`.

If `f` is nonzero, choose a vertex `r` with `f(r) != 0` as the root.
Then `M_0 > 0`, and therefore

`M_{2k} >= (d/q) |f(r)|² > 0`  for every `k >= 1`.

The spheres are disjoint, so `||f||² = sum_{n >= 0} M_n = infinity`,
contradicting `f in ℓ²`. Hence `ker A = {0}`. ∎

## Checks and limits

- The argument permits complex values; it uses the modulus form of
  Cauchy–Schwarz.
- It covers the boundary case `d = 2` (the doubly infinite path), where
  `q = 1`.
- The exact root factor for `d = 100` is `100/99`; subsequent even-level
  masses cannot decrease.
- No positivity, radiality, symmetry of `f`, spectral theorem, or
  spherical-function formula is assumed.
- This proves injectivity, not a lower bound `||Af|| >= c ||f||` with
  `c > 0`. Absence of a zero eigenvector does not assert invertibility.
- Regular branching is used twice: each nonroot parent has `q` children
  and each child has `q` children. The proof does not automatically
  extend to irregular trees.

Strongest verified result: exact injectivity for all `d >= 2`.
Remaining gap for the requested local claim: none.
