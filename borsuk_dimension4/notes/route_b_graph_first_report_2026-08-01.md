# Route B: graph-first diameter-realization screens

**Research checkpoint:** 2026-08-01T15:55:12-07:00  
**Status:** no resolution of `b(4)=5`; multiple explicit six-chromatic
families are rigorously excluded, and reusable exact obstructions are proved.

No literature, construction catalogue, spherical-code database, or previous
computational search was consulted.  All graphs and arguments below were
derived directly from their definitions.

## 1. Exact conclusions

The following candidate six-chromatic graphs cannot occur as diameter graphs
of distinct points in `R^4` (in fact, several cannot even occur as diameter
subgraphs):

1. `K_3 join C_(2m+1)` for every odd cycle of length at least five;
2. the family `K_t join M(K_(5-t))` for `0<=t<=4` (including `M(K_5)`);
3. the 11-vertex Hajós sum made from two copies of `K_6-e`;
4. `K_2 join M(C_5)`;
5. the 15-vertex graph `M(K_2 join C_5)`;
6. the 19-vertex graph `M(M(K_4))`;
7. the 10-vertex graph `C_5 join C_5`; and
8. the 28-vertex disjoint-pair graph `KG(8,2)`.

There are three independent geometric mechanisms:

* a `K_6-e` is forbidden by regular-simplex rigidity;
* after a universal `K_2`, any `C_4` is forbidden by an exact Gram
  determinant; and
* two blocks, each carrying at least two internal diameter edges and joined
  completely by diameter edges, force two small orthogonal circles whose
  cross distances cannot be the diameter.

The last mechanism excludes `KG(8,2)` without assuming symmetry and without
using its nonedges: additional accidental diameter edges would not rescue it.
The same cross-equidistance mechanism, with exact equal-chord closure on a
circle, excludes `C_5 join C_5`.

## 2. Universal-clique spherical reduction

Normalize the diameter to one.  Suppose a diameter graph has a universal
clique `Q={q_1,...,q_t}`.  It is a regular `(t-1)`-simplex.  With its centroid
at zero,

```
||q_i||^2 = (t-1)/(2t),      q_i . q_j = -1/(2t)  (i != j).
```

Every remaining point `x` is at distance one from every `q_i`.  Subtraction
of two such equations makes `x` orthogonal to the affine difference space of
`Q`; the unsubtracted equation gives

```
||x||^2 = (t+1)/(2t).
```

Thus the remaining points lie on a sphere in a linear space of dimension
`5-t`.  On normalizing this sphere to radius one, two remaining points form a
diameter edge exactly when their inner product is

```
c_t = 1/(t+1),
```

and a nonedge has inner product strictly larger than `c_t`.

In particular:

| universal clique | residual space | residual sphere radius squared | edge inner product |
|---|---:|---:|---:|
| `K_1` | `R^4` | `1` | `1/2` |
| `K_2` | `R^3` | `3/4` | `1/3` |
| `K_3` | `R^2` | `2/3` | `1/4` |

This reduction is useful before any nonlinear coordinate search: it lowers
both the rank and the number of free metric parameters.

## 3. First obstruction: `K_6-e`

### Lemma 3.1 (four-neighbor rigidity of a diameter `K_5`)

Let `q_0,...,q_4` be five points in `R^4` at mutual distance one.  If `x` is
at distance one from the four points `q_j`, `j != i`, and every distance in
the configuration is at most one, then `x=q_i`.

### Proof

Center the regular 4-simplex.  Then

```
||q_i||^2=2/5,        q_i.q_j=-1/10  (i != j).
```

Subtracting the four unit-distance equations shows that `x` is orthogonal to
all `q_j-q_k` with `j,k != i`.  Those differences span a 3-space whose
orthogonal complement is the line through `q_i`, so `x=t q_i`.  For `j != i`,

```
1 = ||t q_i-q_j||^2 = (2t^2+t+2)/5.
```

Hence `2t^2+t-3=0`, so `t=1` or `t=-3/2`.  The second solution has

```
||t q_i-q_i||^2 = 5/2 > 1,
```

and is forbidden.  Therefore `t=1` and `x=q_i`.  QED.

### Corollary 3.2

Six distinct points in `R^4` cannot have all but one of their 15 pairs at the
diameter.  In other words, an exact diameter graph cannot contain `K_6-e`.
(`K_6` itself is already impossible because six equidistant points require
affine dimension five.)

This screen immediately eliminates several first-principles six-chromatic
families.

* `K_3 join C_(2m+1)` has chromatic number `3+3=6`.  Three consecutive cycle
  vertices together with the `K_3` span a `K_6-e`.
* In `M(K_5)`, the five original vertices form a `K_5`, and each shadow is
  adjacent to four of them but not to its own original.  These six vertices
  span a `K_6-e`.  Here is the elementary chromatic argument from first
  principles.  A `k`-coloring of `G` extends by coloring each shadow like its
  original and giving the apex one new color.  Conversely, if `M(G)` had only
  `chi(G)` colors, rename the apex color as the last color and recolor every
  original having that color by its shadow's color.  A shadow never has the
  apex color and is adjacent to every neighbor of its original, so this gives
  a proper coloring of `G` with one fewer color, a contradiction.  Hence
  `chi(M(G))=chi(G)+1`, and `M(K_5)` is six-chromatic.
  More generally, in `K_t join M(K_(5-t))` the universal `K_t` together with
  the original `K_(5-t)` is a `K_5`.  Any shadow is adjacent to the `t`
  universal vertices and to all but its own original, hence to exactly four
  vertices of that `K_5`.  It forms a `K_6-e`.  The chromatic number is
  `t+(6-t)=6`, so this excludes the whole family for `0<=t<=4`; the `t=3`
  member is `K_3 join C_5`.
* Take two copies of `K_6-e`, identify one missing-edge endpoint `x`, and add
  an edge between the other missing endpoints `y_1,y_2`.  In any five-coloring
  of either block its missing endpoints must receive the same color.  Both
  `y_1` and `y_2` would therefore have the color of `x`, contradicting their
  added edge.  A six-coloring is explicit: color `x,y_1` alike, use four
  colors on the first `K_4`, give `y_2` a sixth color, and reuse the four
  `K_4` colors on the second block.  Thus the 11-vertex graph is exactly
  six-chromatic, but either one of its `K_6-e` blocks makes a diameter
  realization impossible.

This lemma is a cheap combinatorial preprocessing rule: enumerate six-sets
spanning 14 or 15 edges before starting an SDP or rank-factor search.

## 4. Second obstruction: a `C_4` after a universal `K_2`

### Lemma 4.1

If `K_2 join H` is a diameter subgraph on distinct points in `R^4`, then `H`
contains no four-cycle, even a non-induced one.

### Proof

By Section 2, normalize the points of `H` to unit vectors in `R^3`.  A
prescribed diameter edge then has inner product `c=1/3`, while every pair has
inner product at least `c`.

For a cycle `1-2-3-4-1`, write

```
q=<y_1,y_3>,       t=<y_2,y_4>.
```

All distances are at most the diameter, so `q,t>=1/3`; distinctness gives
`q,t<1`.  The Gram matrix is

```
G = [[1,c,q,c],
     [c,1,c,t],
     [q,c,1,c],
     [c,t,c,1]].
```

Direct exact expansion and factorization gives

```
det(G)=(q-1)(t-1)((q+1)(t+1)-4c^2).
```

The first two factors have positive product.  The last is positive because

```
(q+1)(t+1) >= (4/3)^2 > 4/9 = 4c^2.
```

Thus `det(G)>0`, whereas four vectors in `R^3` must have Gram determinant
zero.  Contradiction.  QED.

The Mycielski graph `M(C_5)` contains (indeed, induces) a four-cycle

```
w - u_(i-1) - v_i - u_(i+1) - w:
```

the apex is adjacent to every shadow, an original is adjacent to the shadows
of its two neighbors, the shadows are independent, and the apex is not
adjacent to an original.  Since `chi(M(C_5))=4`, the join `K_2 join M(C_5)` is
six-chromatic.  Lemma 4.1 rules out its realization globally, not merely in a
symmetric ansatz.

More generally, `K_2 join M(G)` fails this screen whenever `G` has a vertex
with two distinct neighbors.

## 5. Third obstruction: orthogonal cross blocks

The following argument eliminates the most promising set-system graph tried
in this checkpoint.

### Lemma 5.1 (two diameter edges on a circle)

Let a finite set of distinct points lie on a circle, have diameter one, and
contain at least two distinct diameter edges.  Then the circle radius `R`
satisfies

```
R <= 1/sqrt(3).
```

### Proof

Necessarily `R>=1/2`.  If `R=1/2`, the conclusion is immediate.  Otherwise a
unit chord subtends a minor central angle

```
delta = 2 asin(1/(2R)) < pi.
```

Choose one unit chord and put its endpoint angles at `0` and `delta`.  Suppose
`delta<2pi/3`.  A second unit chord sharing the endpoint at zero would have to
use the other possible unit-chord endpoint at `-delta`.  The minor angle
between `delta` and `-delta` is `min(2delta,2pi-2delta)>delta`, so those two
points would be farther apart than the diameter.

If the second unit chord is disjoint from the first, both its endpoints must
be within circular angular distance at most `delta` of both `0` and `delta`.
For `delta<2pi/3`, the intersection of those two closed angular neighborhoods
is the minor arc `[0,delta]`.  The only two points of that arc separated by
`delta` are its already-used endpoints.  This is also impossible.  Therefore
`delta>=2pi/3`.  It follows that

```
1/(2R)=sin(delta/2) >= sin(pi/3)=sqrt(3)/2,
```

which is the claimed bound.  QED.

### Lemma 5.2 (orthogonal two-edge-block obstruction)

There do not exist two finite sets `A,B` of distinct points in `R^4` such that

1. every cross distance `||a-b||`, `a in A,b in B`, equals one;
2. all distances are at most one; and
3. each of `A` and `B` contains at least two distinct unit-distance pairs.

### Proof

Let

```
U=span(A-A),       V=span(B-B).
```

Taking the alternating sum of four equal cross-distance equations gives

```
(a-a').(b-b')=0,
```

so `U` is orthogonal to `V`.  Neither span can have dimension at most one: on
a line, a set of distinct points has only one diameter pair, its unique two
extreme points.  Hence `dim U,dim V >=2`.  Orthogonality in `R^4` forces both
dimensions to equal two and `U+V=R^4`.

All points of `A` are equidistant from every fixed `b`, so their affine plane
meets that sphere in a circle.  Orthogonality makes the circle center
independent of `b`; call it `c_A`.  Similarly `B` lies on a circle centered at
`c_B`.  Projection of `c_B` to `aff(A)` is `c_A`, so `c_B-c_A` is orthogonal
to `U`.  Symmetrically it is orthogonal to `V`.  Since `U+V=R^4`, the centers
coincide: `c_A=c_B=c`.

Write the circle radii as `R_A,R_B`.  Lemma 5.1 gives

```
R_A^2 <= 1/3,       R_B^2 <= 1/3.
```

For `a in A,b in B`, the vectors `a-c` and `b-c` lie in the orthogonal spaces
`U,V`.  Consequently

```
1 = ||a-b||^2 = R_A^2+R_B^2 <= 2/3,
```

a contradiction.  QED.

### Application to `KG(8,2)`

Define a graph on the 28 two-subsets of an eight-element set, joining two
vertices exactly when the corresponding pairs are disjoint.  Split the eight
labels into two four-sets `I,J`.  Let `A` be the six pairs contained in `I`
and `B` the six pairs contained in `J`.

Within either block, the three pairs of complementary two-subsets form a
matching of three graph edges.  Every pair in `I` is disjoint from every pair
in `J`, so all 36 cross pairs are graph edges.  Lemma 5.2 therefore rules out
even a non-induced diameter realization of this graph in `R^4`.

For completeness, its chromatic number is exactly six by a short elementary
argument.  A color class is a pairwise-intersecting family of edges of `K_8`.
Such a family either has a common endpoint (a star family) or is contained in
a triangle: take two intersecting edges `ab,ac`; any edge meeting both either
contains `a` or is `bc`, and the presence of `bc` confines the family to that
triangle.

Suppose five color classes cover `E(K_8)`, and let `s` of them be star
families.  Delete the set of their distinct centers; if it has size `r`, then
`r<=s`.  All edges of the remaining `K_(8-r)` must be covered by the other
`5-s` triangle families, each of size at most three.  In particular, since
`8-r>=8-s`, this would require

```
C(8-s,2) <= 3(5-s),       0<=s<=5,
```

but the two sides are respectively

```
28>15, 21>12, 15>9, 10>6, 6>3, 3>0.
```

Thus five colors do not suffice.  Six do: use successive star colors centered
at five labels, then one final color for the triangle on the remaining three
labels.

### Corollary 5.3 (two-edge join obstruction)

No graph join `G join H` with at least two edges in each factor can be a
diameter subgraph in `R^4`: its two vertex blocks satisfy Lemma 5.2.  This
subsumes the cycle-join obstruction.  In particular, it eliminates every join
of two 3-chromatic graphs, since each contains an odd cycle (and hence at
least two edges).

This corollary also eliminates two compact K5-free Mycielski candidates that
are not themselves graph joins.

* Let `G=K_2 join C_5`, with edge endpoints `a_0,a_1` and cycle vertices
  `v_0,...,v_4`.  Then `chi(G)=5`, so `M(G)` is six-chromatic and has 15
  vertices.  In `M(G)`, the block `{a_0,a_1,u_(a_0)}` contains the two edges
  `a_0a_1,a_1u_(a_0)`, while `{v_0,v_1,v_2}` contains `v_0v_1,v_1v_2`.
  Every cross edge is present: `a_0,a_1` were joined to the whole cycle, and
  the shadow `u_(a_0)` is adjacent to every neighbor of `a_0`.  These two
  three-vertex blocks trigger Corollary 5.3.
* In `M(M(K_4))`, name the original `K_4` vertices `q_0,...,q_3`, the
  first-layer shadow of `q_i` by `s_i`, and the second-layer shadow of `q_i`
  by `t_i`.  The blocks `{q_0,q_1,s_0}` and `{q_2,q_3,t_2}` contain the edge
  pairs `q_0q_1,q_1s_0` and `q_2q_3,q_3t_2`, respectively.  All nine cross
  edges follow directly from the `K_4` edges and the shadow-neighbor rule.
  Thus this 19-vertex six-chromatic graph also fails.  Its chromatic number is
  `4+2=6` by applying the Mycielski recoloring theorem twice.

### Application to `C_5 join C_5`

This smaller K5-free graph is also six-chromatic, since chromatic number is
additive under graph join and `chi(C_5)=3`.  It survives both the `K_6-e`
screen and the universal-`K_2` screen, but Corollary 5.3 rules it out.  The exact
circle calculation below gives a sharper description of why.

First determine exactly what one of its cycles would look like after the
cross-distance argument forces it into a plane.  Five distinct points on a
circle have consecutive cycle chords of length one.  If the circle radius is
`1/2`, every cycle step is antipodal and two steps repeat a point, impossible.
Otherwise let `0<delta<pi` be the minor central angle of a unit chord.  Give
the five directed cycle steps signs `epsilon_i in {+1,-1}`.  Closure around
the circle says

```
delta (epsilon_0+...+epsilon_4) = 2 pi k
```

for an integer winding number `k`.  The signed sum is odd.  Reversing all
orientations if needed, it is one of `1,3,5`; the constraint `delta<pi`
leaves exactly

```
delta in {2pi/3, 2pi/5, 4pi/5}.
```

For `delta=2pi/3`, all walks use only the three angular positions generated
by `2pi/3`, so five distinct vertices are impossible.  For `delta=2pi/5`,
closure requires all five signs to agree; the two-step chord then subtends
`4pi/5` and is strictly longer than a cycle chord, contradicting the global
diameter bound.  The sole possibility is the regular pentagram step
`delta=4pi/5`.  Its circle radius satisfies

```
R^2 = 1/[2(1-cos(4pi/5))] = (5-sqrt(5))/10.
```

Now call the two cycle point sets `A,B`.  Every cross pair is a join edge and
therefore has distance one.  As in Lemma 5.2, the difference spans
`span(A-A)` and `span(B-B)` are orthogonal.  Each has dimension at least two,
because a line has only one diameter pair; hence both are orthogonal planes
spanning `R^4`.  Cross-equidistance puts the two circles at the same center.
The squared cross distance would therefore be

```
R_A^2+R_B^2 = (5-sqrt(5))/5 < 1,
```

contradicting that every cross pair has unit distance.  Thus `C_5 join C_5`
cannot occur even as a diameter subgraph in `R^4`.

## 6. Independent symmetry-only spectral check for `KG(8,2)`

Although Lemma 5.2 is already global, the symmetry calculation is a useful
reusable diagnostic for other orbit graphs.

An `S_8`-invariant centered Gram matrix has entries `a` on the diagonal, `b`
on intersecting pairs, and `c` on disjoint pairs.  Put `g=b-c`.  Centering and
unit diameter give

```
a+12b+15c=0,       a-c=1/2,       g>0.
```

The disjointness adjacency matrix has eigenvalues

```
15 (multiplicity 1), -5 (multiplicity 7), 1 (multiplicity 20).
```

This follows directly: constants have eigenvalue 15; functions
`f({i,j})=x_i+x_j` with `sum x_i=0` have eigenvalue `-5`; the last eigenvalue
is then one by the zero trace and the remaining dimension 20.  Since the
intersecting adjacency matrix is `J-I-A`, the two nonconstant Gram eigenvalues
are

```
lambda_7  = 1/2+4g,
lambda_20 = 1/2-2g.
```

PSD requires `0<g<=1/4`, and `lambda_7` is always strictly positive.  Every
invariant Gram matrix therefore has rank at least seven, with the minimum
rank seven attained at `g=1/4`.  This alone would not rule out a nonsymmetric
rank-four realization—averaging Gram matrices can raise rank—which is why the
independent global argument in Section 5 matters.

## 7. Reproducible verifier and numerical diagnostic

The standard-library exact structural checks are in
`search/route_b_diagnostics.py`.  From the repository root:

```sh
python3 borsuk_dimension4/search/route_b_diagnostics.py --exact
```

The command independently constructs the graph families, computes exact
chromatic numbers for the small examples by DSATUR backtracking, locates
`K_6-e` subsets, enumerates four-cycles (and induced four-cycles separately),
checks the two matching blocks of `KG(8,2)`, verifies the complete cross block
of `C_5 join C_5`, enumerates the signed five-chord closure possibilities, and
evaluates the invariant spectrum with rational arithmetic.

An optional non-certifying rank-four least-squares diagnostic uses the
machine's NumPy/SciPy installation:

```sh
/opt/homebrew/bin/python3.11 \
  borsuk_dimension4/search/route_b_diagnostics.py \
  --numeric kg82 --restarts 12 --seed 20260801
```

The recorded run returned

```text
edge_L2                 1.5492184868965588
edge_Linf               0.5358443736757622
nonedge_min_d2          0.0002783263567540953
nonedge_max_d2          2.659317430313096
best_trial              6
```

This numerical failure is not used in any proof.

## 8. Search implications and next graph families

The exact screens suggest the following ordering for future graph-first work.

1. Reject `K_6`, `K_6-e`, and universal-`K_2`/`C_4` patterns before
   solving any Gram equations.
2. Search six-critical graphs with clique number at most four and without a
   universal `K_2`; if a universal `K_2` is present, its remainder must be
   `C_4`-free.
3. For set-system graphs, search for complete cross-distance blocks.  Their
   affine difference spans must be mutually orthogonal, often producing a
   dimension or radius contradiction before SDP.
   In particular, immediately reject a graph join whose two factors each
   contain at least two edges.
4. The direct triangle-free Mycielski tower remains structurally available,
   but its first six-chromatic member has 47 vertices.  Before any numerical
   work, it should be screened for smaller complete-cross blocks and exact
   stress/rank certificates.
5. A useful next algebraic target is a general rank lower bound for centered
   partial Gram matrices with zero pattern on diameter edges after the
   universal-clique reduction.  Sign-pattern min-rank alone was too weak on
   `M(C_5)`; the determinant argument succeeded only after incorporating PSD
   and the exact edge correlation.

No exact viable rank-four candidate survived this checkpoint.
