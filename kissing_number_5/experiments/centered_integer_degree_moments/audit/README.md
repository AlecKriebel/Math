# Independent audit: centered integer degree moments

Audit timestamp: 2026-07-24T05:41:30Z.

## Exact conclusions

Let `d_i(x)` count the other code points whose inner product with `x` is
`i/4`, for `i=-4,-3,...,2`.  Under the centered 41-point quarter-grid
hypotheses,

```text
sum_i d_i = 40,
sum_i i d_i = -4,
0 <= d_{-4} <= 1,
d_i is a nonnegative integer.
```

An independent recursive bounded-composition enumeration, different from
the production verifier's elimination loops, gives exactly 27,041 rows:
14,720 without an antipode and 12,321 with one.

For a random base vertex, the exact second moment normalization is

```text
E[d_i d_j] = delta_ij alpha_i + distinct-neighbor triangle contribution.
```

The audit derives the triangle contribution by explicitly applying all six
vertex permutations to every triangle type.  This agrees exactly with the
orbit formula in the production verifier.  It also gives the forced checks

```text
sum_j E[d_i d_j] = 40 alpha_i,
sum_j (j/4) E[d_i d_j] = -alpha_i.
```

The three stored separator polynomials are nonnegative on every one of the
27,041 rows and have the following exact negative expectations at their
respective named moment points:

```text
separator 1:
-298897510609152269959977158772724413
------------------------------------------------
             3198650000000000000

separator 2:
-118224275991956033839890815609
--------------------------------
          24605000000000000

separator 3:
-50752094430723752021787
-------------------------
       53200000000000
```

Thus each separator refutes only its named pair/triple witness.

The next repaired witness,
`repaired_pair_triple_local_3.json`, survives the **entire** integer
first/second row-moment cone.  The independent audit verifies an exact
18-atom positive rational mixture of admissible rows.  Its exact values on
all three earlier separator polynomials are strictly positive.  The same
pair/triple witness also passes the existing exact all-degree verifier:

- full radial BV blocks through degree 660 and an analytic tail from 661;
- ordinary pair moments through degree 137 and an analytic tail from 138;
- exact centered `W_0` and `W_1` kernels;
- all 27 stored sharp harmonic-rank cuts;
- robust positive/negative pair masses and all stored local-cap rows.

This is an exact joint feasibility witness for the integer row-moment lift
and those pair/triple harmonic constraints: the row mixture reproduces the
same `alpha` and full `E[d_i d_j]` matrix used by the harmonic verifier.

The audit additionally reconstructed exact separate local Gram-PSD K4 and
K5 extensions of this same repaired pair/triple marginal.  Each extension
uses 51 positive rational atoms.  The small verifier checks every principal
minor of every stored Gram matrix and the exact triangle marginal.  The
certificate SHA-256 is

```text
f09b0f5d7eb6625ae1b41f6f8b050b667bda725af4da77038ff7c372ad885fa0
```

## Scope boundary

These findings are a relaxation barrier, not a construction and not an
upper bound.

- The row mixture has no vertex labels and imposes no consistency between
  different rows.
- The K4 and K5 mixtures are separate symmetric local extensions; they are
  not proved to be marginals of one projectively consistent hierarchy.
- None of these artifacts gives a 41 by 41 rank-five Gram matrix.
- The conclusions require centering and quarter-grid support.

Consequently, iterating exposed integer row-moment cuts cannot eliminate the
current relaxation: an explicit point in the full row-moment convex hull
survives.  A stronger obstruction must use overlap consistency, higher local
levels, or off-grid/global rank information.

## Finite-population and graphical layer

The repaired rational witness itself fails the first global divisibility
test.  In an actual 41-vertex colored complete graph,

```text
41 alpha_i = 2 E_i is an even integer,
41 nu_o / 6 = T_o is a nonnegative integer.
```

For `repaired_pair_triple_local_3.json`, none of the seven quantities
`41 alpha_i` and none of the 51 quantities `41 nu_o/6` is an integer.  This
is an exact obstruction to that named rational point, not to a nearby
reoptimized point.

The sharp antipodal count constraint at this layer is `E_{-1} <= 18`.
Indeed, if there are `r` antipodal pairs, one representative from each pair
is an unoriented line.  On the other `41-2r` vertices, let the deep graph
join pairs with inner product below `-1/2`.  An independent set in this graph,
together with the `r` antipodal lines, is a projective code with absolute
inner products at most `1/2`.  The 20-line projective bound therefore gives

```text
alpha(deep graph) <= 20-r.
```

The deep graph is triangle-free, since three pairwise inner products below
`-1/2` would make the all-ones quadratic form of their Gram matrix negative.
The case `r=20` already contradicts the projective inequality.  If `r=19`,
the remaining graph has three vertices and independence number at most one,
so it must be a triangle, also impossible.  Hence `r<=18`.

The finite-population layer is nevertheless not empty.  The exact certificate
`finite_population_shadow.json` uses 41 rows from the 18-row support of the
repaired mixture:

```text
1  copy of (0,4,6,4,14,0,12),
40 copies of (0,4,7,3,13,1,12).
```

It has even color half-edge totals

```text
(0,164,286,124,534,40,492),
```

and 10,660 integer triangle counts supported only on Gram-feasible triangle
types.  The verifier checks all 28 exact row/triangle incidence equations

```text
sum_v (d_i(v)d_j(v)-delta_ij d_i(v))
  = sum_o T_o L_o(i,j),
```

where `L_o(i,j)` is regenerated from all six vertex orders.

The same row multiset also has an exact simultaneous edge coloring of
`K_41`; all seven color degree sequences pass Erdős--Gallai and every
vertex has its prescribed row.  That particular graph has 649
Gram-infeasible triangles.  Thus:

- global divisibility plus feasible triangle-count incidence has an exact
  shadow;
- simultaneous graphical realization of the row degrees has an exact
  shadow;
- coupling the two shadows in one triangle-feasible colored graph remains
  unresolved.

The last distinction is essential.  The certificate does not splice the
two shadows together and does not claim a quarter-grid code.

The finite-population certificate SHA-256 is

```text
c75ee18a923438f7a912547d72a1220c1a1935a5e479cb7d138b64bb535eee15
```

## Reproduction

From the repository root, with only the standard Python library:

```bash
python3 experiments/centered_integer_degree_moments/audit/independent_audit.py \
  --output experiments/centered_integer_degree_moments/audit/independent_audit_results.json
python3 -m unittest \
  experiments.centered_integer_degree_moments.audit.test_independent_audit
python3 verifiers/verify_centered_quarter_integer_degree_mixture.py
python3 -m unittest tests.test_centered_quarter_integer_degree_mixture
python3 experiments/centered_integer_degree_moments/audit/verify_repaired_local_flags.py
python3 -m unittest \
  experiments.centered_integer_degree_moments.audit.test_repaired_local_flags
python3 experiments/centered_integer_degree_moments/audit/verify_finite_population_shadow.py
python3 -m unittest \
  experiments.centered_integer_degree_moments.audit.test_finite_population_shadow
```

The all-degree rational verification is:

```bash
python3 verifiers/verify_centered_quarter_bv_all_harmonics.py \
  --source experiments/centered_integer_degree_moments/repaired_pair_triple_local_3.json \
  --tail experiments/centered_integer_degree_moments/repaired_local_3_all_harmonics.json
```

To reproduce discovery and exact reconstruction of the local K4/K5 atoms,
use the pinned repository environment:

```bash
.venv/bin/python \
  experiments/centered_integer_degree_moments/audit/certify_repaired_local_flags.py
.venv/bin/python \
  experiments/centered_integer_degree_moments/audit/discover_finite_population_shadow.py
```

The discovery step uses NumPy 2.5.1 and SciPy 1.18.0.  Its output is not
trusted: the standard-library verifier independently checks the resulting
exact certificate.

## Adversarial checks

The tests reject altered expected values, altered source masses, zeroed
mixture/local-extension weights, and invalid Gram edge labels.  The audit
also regenerated each separator's floating exposed face and recovered the
same exact integral coefficients before relying on the independent exact
enumeration.

A direct lifted SDP solve was also attempted as a redundant check.
CLARABEL failed numerically on the large 27,041-variable formulation, and an
SCS run did not produce a usable result.  No solver-status claim is used:
the exact 18-row mixture is a direct feasibility certificate for the lift.
