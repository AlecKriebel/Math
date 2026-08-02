# Exact all-threshold audit of the 600-point dual golden orbit

**Checkpoint:** 2026-08-01

**Status:** the entire 600-point family is eliminated; no subset has a
non-five-colorable diameter graph.

This was a first-principles computation. No web search, construction
catalogue, or prior computational search was consulted.

## 1. Result

Let `V` be the exact 120-vector golden system scaled so that every vector has
squared norm 16. Form its graph at the positive relation

```text
<u,v> = 4+4 sqrt(5).
```

It has exactly 600 four-cliques. For every such clique `Q`, put

```text
p_Q = sum_{v in Q} v.
```

Thus `p_Q/4` is the actual centroid; retaining the sum avoids denominators
and changes no diameter graph. The 600 sums are distinct and form one exact
reflection orbit in `R^4`.

> **Theorem.** For every subset `S` of these 600 points, the diameter graph
> of `S` is five-colorable.

The proof audits all 30 possible pair-product thresholds. Five thresholds
are eliminated by explicit five-colorings of the full relation graph. At
every other threshold an exhaustive compatibility search proves the stronger
statement that every admissible threshold graph is 4-degenerate.

The self-contained standard-library checker is
`borsuk_dimension4/search/h4_dual_subset_search.py`.

## 2. Exact construction

Coordinates lie in `Z[sqrt(5)]`. The 120 starting vectors are

```text
{+-4 e_i},
{(+-2,+-2,+-2,+-2)},
```

together with the even coordinate permutations and independent signs on the
three nonzero coordinates of

```text
(0, 2, 1+sqrt(5), -1+sqrt(5)).
```

The checker reconstructs this set, its complete product table, the positive
`4+4sqrt(5)` relation graph, and all four-cliques. It obtains exactly 600
cliques and 600 distinct sums. Since all six pairs inside a clique have the
same product,

```text
||p_Q||^2
 = 4*16 + 2*6*(4+4sqrt(5))
 = 112+48sqrt(5).
```

The SHA-256 fingerprints of the deterministic clique list and point list are

```text
K4 list:  8413e79e674829660270ea05ef60dbfbb5598c6baa1e523243b010b2b9288517
points:   62ce256266c0d737a9cd3f5c1386539fad1e0fe9c68058824b4305712872c752
```

## 3. Threshold formulation

For a pair-product value `t`, call a vertex set `U` admissible at `t` when

```text
<x,y> >= t                  for every distinct x,y in U.
```

Let `C_t` be the compatibility graph joining all pairs with product at least
`t`, and let `H_t` be the threshold graph joining pairs with product exactly
`t`. Admissible sets are exactly cliques of `C_t`. Because every point has
the same norm,

```text
||x-y||^2 = 2(112+48sqrt(5))-2<x,y>.
```

If `t` is the least product in `U`, the diameter graph of `U` is exactly
`H_t[U]`.

The 30 thresholds, their regular degrees, and their exact elimination
certificates are below. `deg(C_t)` excludes the vertex itself. A zero seed
count means that even the neighborhood of one vertex contains no compatible
five-set.

| # | threshold `(a,b)` for `a+b sqrt(5)` | `deg(H_t)` | `deg(C_t)` | certificate | seeds | states |
|---:|---:|---:|---:|---|---:|---:|
| 0 | `(-112,-48)` | 1 | 599 | no compatible 5-core | 0 | 0 |
| 1 | `(-104,-48)` | 4 | 598 | no compatible 5-core | 0 | 0 |
| 2 | `(-100,-44)` | 12 | 594 | full five-coloring | - | - |
| 3 | `(-88,-40)` | 24 | 582 | full five-coloring | - | - |
| 4 | `(-84,-36)` | 12 | 558 | no compatible 5-core | 792 | 17,729 |
| 5 | `(-76,-36)` | 4 | 546 | no compatible 5-core | 0 | 0 |
| 6 | `(-72,-32)` | 24 | 542 | full five-coloring | - | - |
| 7 | `(-60,-28)` | 24 | 518 | full five-coloring | - | - |
| 8 | `(-56,-24)` | 32 | 494 | full five-coloring | - | - |
| 9 | `(-44,-20)` | 24 | 462 | no compatible 5-core | 16,176 | 19,803 |
| 10 | `(-40,-16)` | 12 | 438 | no compatible 5-core | 192 | 192 |
| 11 | `(-32,-16)` | 24 | 426 | no compatible 5-core | 4,848 | 5,016 |
| 12 | `(-28,-12)` | 28 | 402 | no compatible 5-core | 2,820 | 2,820 |
| 13 | `(-16,-8)` | 24 | 374 | no compatible 5-core | 240 | 240 |
| 14 | `(-12,-4)` | 24 | 350 | no compatible 5-core | 168 | 168 |
| 15 | `(0,0)` | 54 | 326 | no compatible 5-core | 28,500 | 36,516 |
| 16 | `(12,4)` | 24 | 272 | no compatible 5-core | 24 | 24 |
| 17 | `(16,8)` | 24 | 248 | no compatible 5-core | 36 | 36 |
| 18 | `(28,12)` | 28 | 224 | no compatible 5-core | 48 | 48 |
| 19 | `(32,16)` | 24 | 196 | no compatible 5-core | 48 | 48 |
| 20 | `(40,16)` | 12 | 172 | no compatible 5-core | 0 | 0 |
| 21 | `(44,20)` | 24 | 160 | no compatible 5-core | 12 | 12 |
| 22 | `(56,24)` | 32 | 136 | no compatible 5-core | 240 | 240 |
| 23 | `(60,28)` | 24 | 104 | no compatible 5-core | 0 | 0 |
| 24 | `(72,32)` | 24 | 80 | no compatible 5-core | 24 | 24 |
| 25 | `(76,36)` | 4 | 56 | no compatible 5-core | 0 | 0 |
| 26 | `(84,36)` | 12 | 52 | no compatible 5-core | 0 | 0 |
| 27 | `(88,40)` | 24 | 40 | no compatible 5-core | 0 | 0 |
| 28 | `(100,44)` | 12 | 16 | no compatible 5-core | 0 | 0 |
| 29 | `(104,48)` | 4 | 4 | no compatible 5-core | 0 | 0 |

At the initially difficult threshold `(-44,-20)`, the graph of forbidden
lower-product pairs has degree

```text
599-462=137.
```

The compatibility condition is therefore decisive: although coloring the
full 600-vertex equality graph is difficult, only 19,803 exact CEGAR states
are needed to show that no admissible five-core exists.

## 4. Why the five-core test proves five-colorability

A graph that is minimally non-five-colorable has minimum degree at least
five. If a vertex had at most four neighbors, delete it, five-color the
remaining graph by minimality, and return the vertex in a missing neighbor
color.

It is therefore enough to prove:

```text
there is no clique U of C_t for which H_t[U] has minimum degree >=5.
```

This actually proves that every admissible threshold graph is 4-degenerate:
every induced subgraph of an admissible set is again admissible and hence has
a vertex of threshold degree at most four. Greedy deletion and reverse
coloring then use at most five colors.

### 4.1 Exact transitivity reduction

For a norm-16 root `r`, reflection in `r^perp` is

```text
s_r(x)=x-<x,r>r/8.
```

The checker uses the four exact roots

```text
(4,0,0,0),
(1+sqrt(5),1-sqrt(5),0,2),
(2,2,2,2),
(2,2,2,-2).
```

It reconstructs their permutations of the 600 points, verifies every pair
product under every permutation, and obtains an orbit of size 600 from
vertex zero. Thus any putative compatible five-core can be moved so that it
contains vertex zero.

### 4.2 Complete CEGAR recursion

For each non-colored threshold:

1. enumerate every compatible five-subset of the threshold-neighborhood
   `N_H(0)`; together with vertex zero this is a seed;
2. maintain a chosen compatible set `S` and the vertices `C` compatible with
   all of `S`;
3. choose a vertex `v in S` whose threshold degree in `S` is below five;
4. if it needs `r` more neighbors, enumerate every compatible `r`-subset of
   `N_H(v) intersect C` and recurse;
5. reject if fewer than `r` candidates exist; accept only if every chosen
   vertex reaches degree five.

This branching is complete. Any extending five-core must supply the missing
`r` neighbors, and because the core is compatible those neighbors occur in
one of the enumerated compatible subsets. The table records every seed and
recursive state; no accepting state occurs.

## 5. Full-relation color certificates

At five low thresholds, compatible five-cores do occur or are more expensive
to exclude. A five-coloring of the entire relation graph is stronger and
immediately handles every admissible subset. The thresholds are

```text
(-100,-44), (-88,-40), (-72,-32), (-60,-28), (-56,-24).
```

The first two colorings were found by greedy/DSATUR discovery. The last three
were found from a standard one-hot five-color SAT encoding. Discovery method
does not enter the proof: all five 600-character color strings are frozen in
the checker, hashed, and independently checked against every relation edge.

Their SHA-256 fingerprints are

```text
(-100,-44): ced569a0d96eb4fa340e6346f779fbd3d305ce9bbe562e7dfde6819907ef1f1b
(-88,-40):  314347bed87686f429dea4d7154fed2030788d03929511d2feb715de2f9abb01
(-72,-32):  71fe9ac7e86f55f0953e3ebb91cdb81770c63db091fdb923789b4efff79d7eb8
(-60,-28):  3dedc81f06e5881c16c9a7f85a224ce7856087abec33d3d7e7c09024eae10729
(-56,-24):  10d26dddfd0fa4a85f3cf301491af5417c717a4292e84a2045b32740495f4f3b
```

## 6. Completeness and reproduction

Take any subset with at least two points and let `t` be its minimum pair
product. Then `t` is one of the 30 exact values in the table, the subset is a
clique of `C_t`, and its diameter graph is the induced threshold graph
`H_t`. At the five directly colored values it inherits a full-relation
coloring. At every other value it is 4-degenerate by the exhaustive core
search. Hence it is always five-colorable.

Run from the repository root:

```sh
python3 borsuk_dimension4/search/h4_dual_subset_search.py
```

The audit uses only the Python standard library, exact integer-pair
arithmetic in `Z[sqrt(5)]`, and deterministic bit-set search. It completes in
about four seconds on the project machine and ends with

```text
non_5_colorable_admissible_threshold_graphs=0
```
