# Centered quarter-grid global count MILP

This discovery experiment imposes the finite-population divisibility that is
missing from the pair/triple SDP witness.

For a hypothetical centered 41-point quarter-grid code, let `E_i` be the
number of unordered edges of color `i` and `T_o` the number of unordered
vertex triples of orbit type `o`.  Then

```text
sum E_i = C(41,2) = 820,
sum i E_i = -82,
sum T_o = C(41,3) = 10660,
sum_o count_i(o) T_o = 39 E_i.
```

In particular, the normalized relaxation variables must have the forms
`alpha_i=2E_i/41` and `nu_o=6T_o/41`.

There are at most 18 antipodal edges.  If there are \(r\) antipodal pairs,
the deep-pair graph on the other \(41-2r\) vertices must have independence
number at most \(20-r\): otherwise one representative from each antipodal
pair, together with an independent set, gives 21 unoriented lines with all
absolute inner products at most \(1/2\).  For \(r=19\), the remaining three
vertices would have independence number at most one and hence form a
triangle, impossible because three pairwise inner products below
\(-1/2\) have a Gram matrix with negative all-ones quadratic form.

The model also imposes the universal lower bound of 23 edges with inner
product strictly below \(-1/2\).  On the quarter grid these are precisely
the two colors \(-1\) and \(-3/4\).

`search.py` uses a mixed-integer linear model for these identities, robust
depth, common-pair capacity rows, and ordinary pair harmonics.  It enforces
the matrix-valued BV and low-harmonic frame PSD conditions by iterative
eigenvector cuts.  Those cuts are floating-point discovery cuts, so an
infeasible status is **not** a proof.  A surviving count vector is likewise
only a global count shadow, not an edge-colored graph or spherical code.

Run:

```bash
.venv/bin/python experiments/centered_global_count_milp/search.py \
  --iterations 100 --harmonic-degree 16 \
  --output experiments/centered_global_count_milp/result.json
```

An eventual rigorous obstruction would require rational reconstruction of
every PSD cut and an independently checked MILP/Farkas certificate.

`search_degree_lift.py` additionally introduces one integer multiplicity for
every admissible centered row-degree vector and enforces the exact first and
second row/triangle incidence equations.  It also contains an exact finite
binary lift of the sharp rank-five spectral inequality; only the subsequent
BV eigenvector cuts are floating-point.

The 600-second checkpoint found two integral shadows:

```text
iteration 0: 21 BV cuts, worst unchecked eigenvalue -57.6185616931
iteration 1: 39 BV cuts, worst unchecked eigenvalue  -9.22320461625
iteration 2: time limit after 3415 nodes
```

This is discovery evidence only.  In particular, neither a timeout nor the
floating eigenvalues certify feasibility or infeasibility.

An independent exact finite-population artifact is in
`../centered_integer_degree_moments/audit/finite_population_shadow.json`.
It gives 41 integer rows and 10,660 Gram-feasible triangle counts satisfying
all incidence equations.  The same rows separately admit a simultaneous
edge coloring, but that coloring has 649 Gram-infeasible triangles.  Thus the
uncoupled global count layer is rigorously nonempty; a feasible colored graph
or a spherical code is not supplied.
