# Route B research log

All times are America/Los_Angeles (UTC-07:00 on this date).

## 2026-08-01

**14:55** — Began graph-first work under the discovery embargo.  Chose
first-principles graph operations with transparent chromatic proofs: joins,
odd cycles, Mycielski shadows, Hajós sums, and disjointness graphs on
two-subsets.

**15:12** — Derived the four-neighbor rigidity lemma for a regular diameter
`K_5`.  Exact quadratic `2t^2+t-3=0` gives only the omitted simplex vertex or
a point at squared distance `5/2` from it.  Recorded the `K_6-e` preprocessing
screen and applied it to `K_3 join C_5`, `M(K_5)`, and the 11-vertex Hajós
sum.

**15:25** — Derived the universal-clique spherical reduction.  A universal
`K_t` leaves unit vectors in dimension `5-t`, with diameter-edge inner product
`1/(t+1)`.

**15:32** — Factored the four-cycle Gram determinant after a universal `K_2`:

```text
(q-1)(t-1)((q+1)(t+1)-4/9).
```

It is strictly positive for distinct points with `q,t>=1/3`, proving that the
remainder of a universal `K_2` cannot contain any four-cycle.  Applied this to
`K_2 join M(C_5)`.

**15:40** — Constructed `KG(8,2)` and proved `chi=6` by classifying
pairwise-intersecting edge families in `K_8` as star families or triangle
families.  Derived its invariant Gram spectrum exactly; every `S_8`-invariant
strict realization has rank at least seven.

**15:47** — Upgraded the `KG(8,2)` result from a symmetry obstruction to a
global impossibility proof.  A 4+4 split of labels gives two six-point blocks,
each with three disjoint diameter pairs and with all 36 cross pairs at the
diameter.  Cross-equidistance forces orthogonal planar circle spans and a
common center.  The angular-neighborhood lemma bounds each radius squared by
`1/3`, contradicting unit cross distance.

**15:53** — Verified the complementary candidate `C_5 join C_5`.  Exact
signed-chord closure leaves circle steps `2pi/3`, `2pi/5`, and `4pi/5`; only
`4pi/5` survives distinctness and the diameter bound.  Each circle has radius
squared `(5-sqrt(5))/10`.  Orthogonal cross-equidistance would make squared
cross distance `(5-sqrt(5))/5<1`, a contradiction.

The same argument generalized further: a circle with merely two distinct
diameter edges has radius at most `1/sqrt(3)`.  Consequently no join whose two
factors each contain at least two edges can be a diameter subgraph in `R^4`.
An exact subgraph scan then found two completely joined three-vertex blocks,
each carrying two edges, inside both `M(K_2 join C_5)` (15 vertices) and
`M(M(K_4))` (19 vertices).  This excludes two additional K5-free
six-chromatic candidates.

**15:55** — Completed the rigorous report and deterministic verifier.  No
literature or priority search was performed, because no final resolution or
counterexample was obtained.  No commit or push was made.

## Reproduction

```sh
cd /Users/alec/Documents/Math-borsuk4
python3 borsuk_dimension4/search/route_b_diagnostics.py --exact

/opt/homebrew/bin/python3.11 \
  borsuk_dimension4/search/route_b_diagnostics.py \
  --numeric kg82 --restarts 12 --seed 20260801
```

The second command is heuristic only and is not used by any proof.
