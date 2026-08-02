# Exact screen of the 47-vertex Mycielski tower

**Checkpoint:** 2026-08-01  
**Discovery status:** `M^3(C_5)` is rigorously excluded as an *exact*
diameter graph in `R^4`. This does not resolve `b(4)=5`.

No literature, construction catalogue, or web search was used. The graph,
obstruction, and certificate below were derived directly from the Mycielski
definition.

## 1. Result

Let

```text
T_0=C_5,                 T_(r+1)=M(T_r),
```

where `M(G)` has an original `v_i` and a shadow `u_i` for every vertex of
`G`, retains the original edges, joins `u_i` to every original neighbor of
`v_i`, and joins a new apex `w` to every shadow. The exact sizes are

| graph | vertices | edges | chromatic number |
|---|---:|---:|---:|
| `T_0` | 5 | 5 | 3 |
| `T_1` | 11 | 20 | 4 |
| `T_2` | 23 | 71 | 5 |
| `T_3` | 47 | 236 | 6 |

The main conclusion is:

> **Theorem.** There is no set of 47 distinct points in `R^4` whose exact
> diameter graph is `T_3=M^3(C_5)`.

The proof uses only strict graph-nonedge inequalities, rank at most five for
one rectangular diameter-slack matrix, and elementary face theory for a
four-dimensional polytope. It does not assume that a realization respects
the fivefold graph symmetry.

## 2. Chromatic and inherited structural screens

The elementary Mycielski recoloring argument gives

```text
chi(M(G))=chi(G)+1.
```

The upper coloring copies an optimal coloring of `G` to its shadows and
gives the apex one new color. For the lower bound, suppose `M(G)` used only
`chi(G)` colors and call the apex color `c`. No shadow has color `c`.
Recolor every original of color `c` by the color of its shadow. A shadow is
adjacent to every original neighbor of its mate, so this is a proper coloring
of `G` that avoids `c`, a contradiction.

The construction also preserves vertex-criticality. If `G` is
`k`-vertex-critical, then:

* after deleting the apex, copy a `k`-coloring of `G` to both layers;
* after deleting an original `v_i`, color `G-i` with `k-1` colors, put all
  shadows in a new color, and give the apex any old color;
* after deleting a shadow `u_i`, color `G-i` with `k-1` colors, give `v_i`
  and the apex a new color, and color every other shadow like its original.

Starting with the critical pentagon proves that `T_3` is 6-vertex-critical.
Thus it has no smaller proper induced six-chromatic core.

Mycielski also preserves triangle-freeness. The exact checker confirms that
`T_3` is triangle-free, has no universal vertex, and is maximal
triangle-free: every graph nonedge has a common neighbor. Consequently all
three previously established local screens fail for immediate structural
reasons:

* a `K_6-e` contains a triangle;
* a universal `K_2`, or even a `K_2 join C_4` subgraph, contains a triangle;
* if one completely cross-joined block contains an edge and the other block
  is nonempty, either endpoint of that edge and any opposite vertex make a
  triangle. Hence two cross-joined blocks each containing two edges cannot
  occur.

## 3. The top-layer slack matrix

Assume for contradiction that `T_3=M(T_2)` is the exact diameter graph of
distinct points in `R^4`, and normalize the diameter to one. Write

```text
x_i = point of the top-level original indexed by i in T_2,
y_j = point of the top-level shadow indexed by j in T_2,
z   = top-level apex.
```

Translate so that `z=0`. Every apex-shadow pair is a diameter edge, hence

```text
||y_j||=1.
```

Define the 23 by 23 original-shadow slack matrix

```text
B_ij = 1-||x_i-y_j||^2
     = 2 x_i.y_j-||x_i||^2.
```

Because the diameter graph is exact,

```text
B_ij=0  if ij is an edge of T_2,
B_ij>0  otherwise.
```

Moreover

```text
B = [2x_i^T, -||x_i||^2] [y_j; 1],
```

so `rank(B)<=5`.

The following exact support minor is lower triangular with a strictly
positive diagonal. Here `0` is a graph edge and `+` is a graph nonedge.

```text
rows:
 A_0, A_2, B_0, C_0, A_1

columns:
 A_0, A_4, B_1, C_1, A_1

 + 0 0 0 0
 + + 0 0 0
 + 0 + 0 0
 + 0 0 + 0
 0 + + + +
```

The notation for `T_2=M(M(C_5))` is

```text
A_i = O2(O1(c_i)),       B_i = O2(S1(c_i)),       a = O2(w1),
C_i = S2(O1(c_i)),       D_i = S2(S1(c_i)),       b = S2(w1),
w   = w2.
```

The minor proves `rank(B)>=5`, hence `rank(B)=5`. In particular, the
homogeneous columns `[y_j;1]` have rank five, so the 23 shadows affinely span
`R^4`.

## 4. The shadows force a full four-polytope

Let

```text
P=conv{y_j:j in V(T_2)}.
```

It is a four-dimensional polytope. Every `y_j` is a vertex: distinct points
on one Euclidean sphere are all exposed by their tangent hyperplanes.

For every `i`, the top original `x_i` is distinct from the apex, so
`x_i != 0`. The diameter equalities and strict inequalities give

```text
x_i.y_j = ||x_i||^2/2   for j in N(i),
x_i.y_j > ||x_i||^2/2   for j not in N(i).
```

Thus

```text
F_i = P intersect {y:x_i.y=||x_i||^2/2}
```

is an exposed face whose vertex set is exactly the open neighborhood `N(i)`
in `T_2`.

The neighborhoods are all distinct and have at least four vertices. The
following seven-orbit table gives, for each `F_i`, another face `F_j` such
that `F_i intersect F_j` is proper and has at least three vertices.

| type of `i` | multiplicity | `|N(i)|` | witness `j` | `|N(i) intersect N(j)|` |
|---|---:|---:|---|---:|
| `A_i` | 5 | 8 | `A_(i+2)` | 4 |
| `B_i` | 5 | 6 | `A_i` | 4 |
| `a` | 1 | 10 | `A_0` | 4 |
| `C_i` | 5 | 5 | `A_i` | 4 |
| `D_i` | 5 | 4 | `B_i` | 3 |
| `b` | 1 | 6 | `a` | 5 |
| `w` | 1 | 11 | `A_0` | 4 |

Indices are modulo five. If `F_i` were two-dimensional, every proper face
of it would have at most two vertices. The table rules this out. Since `F_i`
is a proper face of a four-polytope, it follows that every `F_i` is a facet.

## 5. The 23 facets are all the facets

The remaining assertion is finite and is checked exactly from common
neighborhoods.

* For each pair `i,j` with at least three common neighbors,
  `F_i intersect F_j` has at least three vertices. Two distinct facets of a
  four-polytope meet in dimension at most two, so this intersection is a
  polygonal ridge. There are 62 such pairs, all with different vertex sets:
  30 triangles, 30 quadrilaterals, and two pentagons.
* An intersection of three specified facets having exactly two vertices is
  an edge. There are 62 distinct such vertex pairs.
* In each of the 62 ridges, the specified edges form one cycle through all
  ridge vertices. They are therefore the complete boundary of that polygon.

The local data on the seven facet orbits are:

| facet type | multiplicity | vertices `V` | edges `E` | ridges `F` | `V-E+F` |
|---|---:|---:|---:|---:|---:|
| `A_i` | 5 | 8 | 12 | 6 | 2 |
| `B_i` | 5 | 6 | 9 | 5 | 2 |
| `a` | 1 | 10 | 15 | 7 | 2 |
| `C_i` | 5 | 5 | 8 | 5 | 2 |
| `D_i` | 5 | 4 | 6 | 4 | 2 |
| `b` | 1 | 6 | 10 | 6 | 2 |
| `w` | 1 | 11 | 20 | 11 | 2 |

Within each `F_i`, every listed edge is already in exactly two listed
ridges. This proves that the list is complete by a short Euler argument.
Indeed, if a three-polytope had `e'` additional edges and `f'` additional
two-faces, Euler and the table would give `e'=f'`. No extra face can use an
already listed edge, since such an edge is already in its two incident
faces. Thus the extra faces and edges would satisfy

```text
3 f' <= 2 e'.
```

Together with `e'=f'`, this forces `e'=f'=0`.

The adjacency graph of the 23 facets through the 62 ridges is connected.
Every listed facet has now accounted for all of its ridges, so it cannot be
ridge-adjacent to an unlisted facet. The facet-adjacency graph of a convex
polytope is connected. Hence there are no unlisted facets: the `F_i` are all
facets of `P`.

## 6. Final contradiction

Every facet-containing halfspace of `P` has the orientation

```text
x_i.y >= c_i,            c_i=||x_i||^2/2>0.
```

Since these are all facets,

```text
P = intersection_i {y:x_i.y>=c_i}.
```

Take any `q in P`. For every `t>=1`,

```text
x_i.(tq) = t x_i.q >= t c_i >= c_i
```

for every facet. Therefore the entire ray `{tq:t>=1}` lies in `P`. This is
impossible because `P` is the convex hull of finitely many points. The
assumed exact diameter realization does not exist.

## 7. Reproduction and scope

Run from the repository root:

```sh
python3 borsuk_dimension4/search/mycielski_tower_screen.py
```

The checker uses only the Python standard library. It reconstructs all four
tower levels, verifies the explicit critical-coloring certificates, applies
the inherited screens, verifies the rank-five support minor, and replays all
facet/ridge/edge counts and incidence assertions used above.

The strictness qualification matters. If a nonedge of `T_3` were allowed to
be another diameter pair, its slack entry could vanish, the exposed faces
could acquire more vertices, and this proof would no longer apply. Thus the
argument excludes `T_3` as an exact diameter graph but does not exclude a
diameter graph that properly contains it. Such a supergraph would itself be
six-chromatic and would already be a counterexample, so weak realizations
remain worth testing separately.

As secondary numerical evidence only, unconstrained edge-equality fitting
found machine-precision fits in five dimensions but no comparable
four-dimensional fit. Cyclically averaged rank relaxations were feasible, so
they do not supply an independent obstruction. No numerical statement is
used anywhere in the theorem.
