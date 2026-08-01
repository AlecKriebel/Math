# Route A report: symmetric exact families in dimension four

**Checkpoint:** 2026-08-01T15:53:15-07:00  
**Scope:** signed-permutation, simplex-reflection, chiral permutation, and
root-like orbit families  
**Discovery discipline:** no web search, literature search, polytope catalogue,
spherical-code catalogue, or Borsuk-specific source was consulted.

## Outcome

No counterexample was found.  The main result is instead a conceptual
five-coloring theorem which completely rules out the most natural irreducible
noncentral reflection family and its chiral half:

> Let
> \(H=\{x\in\mathbb R^5:\sum_i x_i=0\}\), with its induced Euclidean metric,
> so that \(H\cong\mathbb R^4\).  Every finite set in \(H\) invariant under all
> even coordinate permutations has a five-colorable diameter graph.

Consequently, no finite union of centered \(A_5\)-orbits, with arbitrary seeds
and arbitrary orbit radii, can be a four-dimensional Borsuk counterexample.
This includes every union of full \(S_5\) reflection orbits.  The coloring is
explicit and does not rely on computation.

An exact bounded enumerator independently tested 133,303 distinct
signed-permutation point orbits.  Their exact chromatic-number distribution was

| chromatic number | number of distinct point orbits |
|---:|---:|
| 1 | 161 |
| 2 | 130,418 |
| 3 | 2,584 |
| 4 | 140 |

Thus none of these single orbits even required five colors.  An exact radial
two-orbit tie search also found no stronger graph.  A separate exact
\(\mathbb Q(\sqrt5)\) certificate rules out all \(2^{60}\) antipodal
transversals of a structured 120-vector family via one five-colorable absolute
relation graph and a switching-invariant negative cycle.

## 1. Alternating simplex-orbit theorem

Index coordinates cyclically modulo five.  For every nonzero \(x\in H\), let

\[
 c(x)=\min\{i:x_i=\min_j x_j\ \text{and}\ x_i<x_{i+1}\}.
\]

The set in braces is nonempty: the positions of the global minimum form a
nonempty proper subset of the five-cycle, so some minimum position is followed
by a larger entry.  Hence \(c(x)\in\{0,1,2,3,4\}\).

Let \(S\subset H\) be a finite union of orbits of the even coordinate
permutation group, and suppose \(x,y\in S\) form a diameter pair.  Since the
whole orbit of \(y\) is in \(S\), \(y\) minimizes \(\langle x,gy\rangle\) over
all even permutations \(g\).  There are two cases.

### 1.1 A repeated coordinate occurs

If \(y\) has a repeated coordinate, an odd transposition stabilizes \(y\), so
its even-permutation orbit equals its full-permutation orbit.  If instead \(x\)
has a repeated coordinate, choose an odd transposition \(s\) stabilizing
\(x\).  For every odd permutation \(p\), the permutation \(sp\) is even and

\[
 \langle x,spy\rangle=\langle s^{-1}x,py\rangle=\langle x,py\rangle.
\]

Thus in either situation minimization over even permutations has exactly the
same values as minimization over all permutations.  The rearrangement swap
argument then gives

\[
 (x_i-x_j)(y_i-y_j)\le 0\qquad\text{for every }i,j.
\]

If \(c(x)=c(y)=i\), both vectors have the strict ascent from coordinate \(i\)
to coordinate \(i+1\), contradicting this inequality.

### 1.2 Both coordinate lists are strict

The fully reversed assignment is either available in the even-permutation
coset or it is not.  If available, the preceding opposition argument applies.
If it is unavailable, every allowed assignment differs from full reversal by
an odd permutation.

Among those odd departures, a minimum is obtained by one adjacent rank swap
from full reversal.  Indeed, bubble-sort any other odd departure back to the
strictly decreasing assignment.  Every adjacent correction strictly lowers
the dot product.  Immediately before the final correction the assignment
differs from reversal by one adjacent swap and is already better than the
starting assignment.

For a strict vector, \(c(x)\) is the position of its unique minimum.  Under
full reversal that coordinate receives the maximum value of \(y\); after one
adjacent rank swap it receives either the maximum or second-maximum value.  It
therefore cannot be the minimum position of \(y\), and \(c(x)\ne c(y)\).

This proves that \(c\) is a proper five-coloring of the diameter graph.

The zero orbit is harmless.  If a nonzero orbit is present, averaging it gives
zero, so some within-orbit squared distance from a maximal-norm point is at
least twice that norm squared; every distance from zero is smaller.  Thus zero
is not a diameter endpoint and may receive any color.

### 1.3 Exhaustive finite check of the ordering lemma

The script also represents every nonconstant weak order on five labeled
coordinates by a surjective rank word.  There are 540 such words.  It builds:

- all 8,280 ordinary opposition edges;
- all 240 additional edges that can arise from parity-forced adjacent swaps;
- the explicit boundary-minimum coloring above.

All 8,520 envelope edges pass the coloring check.  This computation is not
needed for the proof, but independently checks all tie patterns.

## 2. Exact signed-permutation orbit enumeration

The signed-permutation group in four coordinates has 384 matrices.  The
enumerator closes every unordered pair of elements and obtains 1,237 distinct
subgroups generated by at most two elements.  It then uses every primitive
canonical integer seed

\[
 0\le a_1\le a_2\le a_3\le a_4\le 6,
 \qquad \gcd(a_1,a_2,a_3,a_4)=1,
\]

of which there are 161.  This is exhaustive, up to full signed-permutation
conjugacy, for primitive rational seed directions whose cleared integer
coordinates have maximum absolute value at most six and whose acting subgroup
is generated by at most two elements.

After identical point orbits were deduplicated, 133,303 remained.  Every inner
product, diameter edge, clique lower bound, odd-cycle lower bound, and coloring
check used integer arithmetic.  The orbit sizes were

```text
{1: 161, 2: 8631, 3: 2545, 4: 36775, 6: 13629, 8: 36647,
 12: 13509, 16: 9179, 24: 5910, 32: 2185, 48: 3208,
 64: 679, 96: 109, 192: 121, 384: 15}
```

The clique/non-bipartiteness lower bounds exactly matched the verified DSATUR
colorings for every graph.  A smallest four-chromatic witness encountered was
the regular tetrahedral orbit

\[
 (0,-1,-1,1),\ (0,-1,1,-1),\ (0,1,-1,-1),\ (0,1,1,1),
\]

whose six pairs all have squared distance eight.

Groups containing central inversion are especially unpromising on a common
sphere: every point brings its antipode, so the minimum-inner-product graph is
only the antipodal matching.  The enumerator retained these groups rather than
discarding them, as a check on that reduction.

## 3. Exact radial two-orbit tie search

For two spherical group orbits \(A,B\), scale \(A\) by one and \(B\) by
\(t>0\).  Write

- \(n_A,n_B\) for their squared norms;
- \(M_A,M_B\) for their within-orbit maximum squared distances;
- \(c=\min\{\langle a,b\rangle:a\in A,b\in B\}\).

The only three competing distance maxima are

\[
 M_A,\qquad t^2M_B,\qquad X(t)=n_A+t^2n_B-2tc.
\]

Because every enumerated single orbit is four-colorable, all upper-envelope
events except a triple tie are immediately five-colorable:

- a single within-orbit maximum uses at most four colors;
- a cross-only graph is bipartite;
- two within maxima give a disjoint union;
- a within maximum tied with the cross maximum uses four colors on that orbit
  and a fifth color on the other, internally independent, orbit.

At a triple tie,

\[
 t^2=M_A/M_B,
 \qquad n_A+(M_A/M_B)n_B-M_A=2c\sqrt{M_A/M_B}.
\]

The program tests this identity exactly by a rational square equality and the
required sign.  For both seeds placed in canonical alignment, bound four gave:

```text
subgroups:                  1,237
canonical seeds:               51
aligned orbit pairs:     1,560,423
exact triple ties:           5,017
chi=2 ties:                  4,066
chi=3 ties:                    236
chi=4 ties:                    715
```

No triple tie required five colors.  This pair search is exhaustive for the
stated aligned canonical family, but not for all relative orientations of two
seeds.  That limitation is important.

### 3.1 Fully tied aligned triples

As a first probe of three-layer unions, the bound-three pair-tie relation was
formed for every common subgroup.  A triangle in this relation is an aligned
three-orbit configuration in which all three within-orbit maxima and all three
cross-orbit maxima have one common value.  The exact results were

```text
pair-tie instances:          2,301
full six-way triple ties:    1,805
chi=2 triples:               1,112
chi=3 triples:                 117
chi=4 triples:                 576
```

Thus even these maximally coupled small triples remain at most
four-chromatic.  This does not cover partially active upper-envelope patterns
or noncanonical relative seed orientations.

### 3.2 Partially active triples: one internal class and all cross classes

A second exact bound-two probe targeted the genuinely new activation pattern
consisting of one within-orbit diameter and all three cross-orbit diameters.
With layer \(A\) at radius one and layers \(B,C\) at radii \(t,u>0\), its tie
equations are

\[
 M_A=n_A+n_Bt^2-2c_{AB}t
     =n_A+n_Cu^2-2c_{AC}u
     =n_Bt^2+n_Cu^2-2c_{BC}tu.
\]

Thus

\[
 t=\frac{c_{AB}\pm\sqrt{c_{AB}^2-n_B(n_A-M_A)}}{n_B},\qquad
 u=\frac{c_{AC}\pm\sqrt{c_{AC}^2-n_C(n_A-M_A)}}{n_C},
\]

and, after using the first two quadratics, the remaining condition is

\[
 M_A-2n_A+2c_{AB}t+2c_{AC}u-2c_{BC}tu=0.
\]

The probe squarefree-decomposed both radicals, expanded this expression in the
rational basis generated by the two square roots, and used exact signs of
\(a+b\sqrt d\) for positivity and the envelope inequalities
\(M_Bt^2\le M_A\), \(M_Cu^2\le M_A\).

For distinct canonical orbit directions under the 882 usable noncentral
bound-two groups, it tested 99,621 orbit triples.  There were 805 algebraic tie
incidences, of which 122 lay on the upper envelope.  Their active-category
counts were 114 with four classes and eight with one additional internal
class.  Corrected verified coloring upper bounds were

```text
{2: 49, 3: 48, 4: 25}.
```

The one graph for which the initial greedy pass used five colors was checked
by complete DSATUR and is actually three-colorable.  A repeated-direction
extension checked 84,710 additional orbit multisets and 99,606 envelope
incidences; its coloring upper counts were

```text
{2: 82442, 3: 10957, 4: 6207}.
```

No event required five or six colors.  These are incidence counts, not
isomorphism-deduplicated configurations.  The exact equations, counts, and the
false-alarm witness are retained in the Route A triple-probe result note; the
unified enumerator currently reproduces the full-tie search, while this
partial-activation probe was a separate bounded run.

## 4. Root-like families and aggressive falsification

### 4.1 All antipodal transversals of the signed two-support roots

Take the 24 vectors in \(\mathbb R^4\) with exactly two nonzero coordinates,
each equal to \(\pm1\), and select exactly one vector from each antipodal pair.
All \(2^{12}=4096\) transversals were checked exactly.  Every one has squared
diameter six and chromatic number exactly three.  The edge-count distribution
is

```text
{16: 192, 18: 192, 20: 576, 22: 192, 24: 1344,
 26: 576, 28: 960, 30: 64}.
```

There is a uniform three-coloring: color a root by the one-factor of \(K_4\)
containing its two-coordinate support.  Same-colored supports are equal or
disjoint, whereas a diameter inner product of \(-1\) requires overlapping,
unequal supports.  The verifier additionally checks non-bipartiteness for the
matching lower bound.

### 4.2 Lexicographic positive halves

Four exact positive-half tests gave:

| explicit family | points | \(D^2\) | diameter edges | \(\chi\) |
|---|---:|---:|---:|---:|
| differences \(e_i-e_j\) in the 4-space \(\sum x_i=0\subset\mathbb R^5\) | 10 | 6 | 10 | 3 |
| signed two-support vectors in \(\mathbb R^4\) | 12 | 6 | 16 | 3 |
| preceding vectors plus unit axes | 16 | 6 | 16 | 3 |
| preceding vectors plus doubled axes | 16 | 10 | 6 | 2 |

### 4.3 A 24-point mixed transversal is always bipartite

There is also an exact analytic rejection of the equal-norm union

\[
 \{\pm2e_i\}\ \cup\
 \{(\pm1,\pm1,\pm1,\pm1)\}\ \cup\
 \{\sqrt2(\pm e_i\pm e_j):i<j\}.
\]

All vectors have squared norm four.  Choose one from every antipodal pair,
giving 24 points.  Within each of the three layers every nonantipodal inner
product is at least \(-2\).  Between the two-support layer and either other
layer, the minimum possible inner product is \(-2\sqrt2\).

Every transversal realizes such a cross minimum.  For each support
\(\{i,j\}\), the two antipodal two-support pairs have the same-sign and
opposite-sign patterns.  Relative to the chosen signs of the two axis vectors,
one of these pairs cannot agree in both coordinates, producing inner product
\(-2\sqrt2\) with a chosen axis.  Hence the global diameter graph uses only
edges between the two-support layer and the union of the other two layers, and
is bipartite.

### 4.4 All transversals of an exact 120-vector golden family

Let \(\phi=(1+\sqrt5)/2\), using the real embedding \(2<\sqrt5<3\), and take
the following 120 unit vectors:

\[
 \{\pm e_i\}_{i=1}^4,
 \qquad
 \{(\pm\tfrac12,\pm\tfrac12,\pm\tfrac12,\pm\tfrac12)\},
\]

together with all even coordinate permutations of

\[
 (0,\tfrac12,\tfrac\phi2,\tfrac1{2\phi})
\]

and all eight sign choices on its three nonzero entries.  These are 60
antipodal lines.  Exact arithmetic in \(\mathbb Q(\sqrt5)\), after multiplying
all coordinates by four, gives the nonantipodal inner-product spectrum

\[
 \left\{-\frac\phi2,-\frac12,-\frac1{2\phi},0,
 \frac1{2\phi},\frac12,\frac\phi2\right\}.
\]

The projective absolute-relation graph defined by
\(|\langle x,y\rangle|=\phi/2\) is 12-regular on 60 vertices, with 360 edges.
The verifier contains and checks an explicit five-coloring with five equal
classes of size 12.

It remains to ensure that an arbitrary orientation of the 60 lines actually
has a negative \(-\phi/2\) edge.  For the deterministic line representatives
used by the verifier, vertices

\[
 0,21,41,36,32,0
\]

form a signed five-cycle with signs \(+,-,-,-,+\), whose product is negative.
Changing a line orientation switches all incident edge signs and leaves the
cycle product invariant.  Every one of the \(2^{60}\) transversals therefore
has at least one negative \(\phi/2\)-magnitude edge.  The exact spectrum shows
that no nonantipodal inner product is smaller, so each transversal's diameter
graph is a subgraph of the five-colorable absolute-relation graph.  This rules
out all \(2^{60}\) transversals without enumerating them.

## 5. Reproduction

From `/Users/alec/Documents/Math-borsuk4`:

```bash
python3 borsuk_dimension4/search/route_a_orbit_search.py a5-envelope
python3 borsuk_dimension4/search/route_a_orbit_search.py signed-orbits --bound 6
python3 borsuk_dimension4/search/route_a_orbit_search.py signed-pair-ties --bound 4
python3 borsuk_dimension4/search/route_a_orbit_search.py signed-triple-ties --bound 3
python3 borsuk_dimension4/search/route_a_orbit_search.py d4-transversals
python3 borsuk_dimension4/search/route_a_orbit_search.py positive-root-halves
python3 borsuk_dimension4/search/route_a_orbit_search.py golden-transversals
```

Observed runtimes on the project machine were about 0.2 seconds, 21 seconds,
22 seconds, 8 seconds, 0.5 seconds, 0.2 seconds, and 0.2 seconds respectively.
Peak family sizes are small enough for the stated 16 GB RAM constraint.  The
script uses only the Python standard library.

## 6. Strongest next lead

Full simplex symmetry is now ruled out conceptually, and single signed orbits
are empirically much too low-chromatic.  Antipodal transversals likewise lose
too many constraints.  The strongest remaining Route A lead is therefore a
**three-layer, partially symmetry-broken construction**:

1. start with a noncentral signed-permutation subgroup whose bounded orbits
   contain exact four-chromatic diameter subgraphs;
2. use three distinct orbits or cosets, not merely antipodal transversals;
3. solve the simultaneous exact upper-envelope tie equations for two radial
   parameters;
4. test the resulting invariant graph before attempting any coordinate
   deformation.

Three layers can couple several internally constrained color classes at once;
the simple “reserve a fifth color for the independent layer” argument that
destroys every non-triple two-layer event no longer applies.  Relative seed
orientations, omitted from the aligned pair enumeration, should be included
before increasing the integer bound.  The fully tied aligned bound-three
subfamily and the bound-two one-internal/all-cross subfamily have already been
eliminated.  The next bounded search should raise the latter to bound three and
include noncanonical relative seed orientations rather than repeat either
case.

No exact counterexample or proof of \(b(4)=5\) has been obtained.  Best-guess
completion of the assigned Route A survey is **80%**; best-guess completion
toward a full resolution of the four-dimensional Borsuk problem remains only
**1%**, reflecting that this report mainly eliminates broad natural families.
