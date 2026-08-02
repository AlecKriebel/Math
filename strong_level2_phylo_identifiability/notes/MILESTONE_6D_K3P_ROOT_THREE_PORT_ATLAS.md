# Milestone 6D: complete K3P reticulate three-port root atlas

## Primary theorem

Consider the complete census of binary strongly tree-child reticulate root
blobs with exactly three ordered outgoing ports.  It contains two unlabelled
cycle models and five unlabelled theta models.

**PROVED.** Under K3P these seven models split into exactly two
full-dimensional regular stochastic-overlap classes:

1. a dimension-14 class `H14`, containing both cycles and one theta;
2. a dimension-15 class `A15`, containing the other four thetas.

Every pair inside `H14` satisfies `bowtie_K3P`, and every pair inside `A15`
satisfies `bowtie_K3P`.

**PROVED.** There is also strict one-sided generic containment

\[
\boxed{H14\preceq_{\rm K3P}A15.}
\]

More precisely, all seven model images contain one common strict algebraic
distribution.  At that distribution the three `H14` maps have rank 14 and
the four `A15` maps have rank 15.  The simultaneous intersection is locally
14-dimensional.  Therefore `A15` is not one-sided contained in `H14`, and
the two classes cannot satisfy `bowtie_K3P` because their dimensions differ.

This is a stochastic theorem at a common regular point, not an inference
from containment of Zariski closures.

Equality of complete open stochastic images inside either class is not
claimed.

## The quartic

Write `q_ijk` for the normalized three-leaf K3P Fourier coordinate with
`i xor j xor k=0`.  Define

\[
\begin{aligned}
I={}&q_{000}q_{123}q_{231}q_{312}
-q_{000}q_{132}q_{213}q_{321}\\
&-q_{011}q_{123}q_{202}q_{330}
+q_{011}q_{132}q_{220}q_{303}\\
&+q_{022}q_{101}q_{213}q_{330}
-q_{022}q_{110}q_{231}q_{303}\\
&-q_{033}q_{101}q_{220}q_{312}
+q_{033}q_{110}q_{202}q_{321}.
\end{aligned}
\]

It has eight square-free degree-four terms and coefficients in `{+1,-1}`.

**PROVED.** `I` is irreducible over the rationals.  Indeed, regard it as

\[
I=q_{000}A+B,
\]

where

\[
A=q_{123}q_{231}q_{312}-q_{132}q_{213}q_{321}.
\]

The two coefficients of `A`, viewed as a primitive linear polynomial in
`q_123`, are coprime, so Gauss's lemma makes `A` irreducible.  Moreover `A`
does not divide `B`: setting
`q_231=q_312=q_132=q_213=q_321=0` leaves `A=0` but leaves the term
`-q_011 q_123 q_202 q_330` in `B`.  Hence `gcd(A,B)=1`, and the primitive
linear polynomial `q_000 A+B` is irreducible.  The verifier independently
replays exact multivariate factorization.

**EXACTLY COMPUTED.** The quartic is negated by the K2P character exchange
`2 <-> 3`.  It is also alternating under odd leaf permutations and invariant
under even leaf permutations.  Thus its zero set is well defined for every
port labelling, and every K2P tensor lies in `V(I)`.

## Exact model dimensions and closures

In the stable census order, the K3P ranks are

| record | generator data | generic rank | quartic pullback |
|---:|---|---:|---|
| 1 | cycle, subdivision `(1,1)` | 14 | zero |
| 2 | cycle, subdivision `(0,2)` | 14 | zero |
| 3 | theta core 2, `(0,1,0,0,1)` | 15 | nonzero |
| 4 | theta core 3, `(0,0,0,1,1)` | 14 | zero |
| 5 | theta core 3, `(1,0,0,0,1)` | 15 | nonzero |
| 6 | theta core 0, `(0,0,0,0,0,1)` | 15 | nonzero |
| 7 | theta core 0, `(0,0,0,1,0,0)` | 15 | nonzero |

**EXACTLY COMPUTED.** At one strict rational K3P witness, prescribed rank
minors have exact nonzero rational values for all seven models.  Every edge
at that witness has minimum transition probability `31/240`.

**EXACTLY COMPUTED.** Direct sparse polynomial contraction gives zero
quartic pullback for records 1, 2, and 4.  At the rank witnesses of records
3, 5, 6, and 7, the exact quartic values are respectively

\[
\frac{3301407761}{12597120000000000000000},\quad
\frac{37454327}{3149280000000000000},\quad
\frac{63917011}{94478400000000000000},\quad
-\frac{914207}{787320000000000000}.
\]

**PROVED.** A model closure is irreducible because it is the closure of a
polynomial image of an irreducible parameter space.  Therefore:

\[
\boxed{
V_1=V_2=V_4=V(I),\qquad
V_3=V_5=V_6=V_7=\mathbb A^{15}.
}
\]

The first equality follows because both sides are irreducible of dimension
14; the second follows from rank 15 in the complete normalized 15-coordinate
K3P space.

## One exact common distribution

Use the K2P convention `(s,t,t)` inside K3P and put

\[
\delta=\frac1{100}.
\]

Define a normalized three-leaf tensor `p*` by

\[
q_{000}=1,
\]

\[
q_{011}=q_{101}=q_{110}=\frac{101}{1000000},
\]

\[
q_{022}=q_{033}=q_{202}=q_{303}=q_{220}=q_{330}
=\frac1{10000},
\]

and give all six all-distinct coordinates the common value

\[
q_{123}=q_{132}=q_{213}=q_{231}=q_{312}=q_{321}
=\frac1{1250000}.
\]

The tensor is invariant under every leaf permutation.  Direct substitution
gives

\[
I(p^*)=0,
\qquad
\left.\frac{\partial I}{\partial q_{123}}\right|_{p^*}
=-\frac{37}{10^{14}}\ne0.
\]

Hence `p*` is a smooth point of the quartic hypersurface.

## Exact algebraic preimages

For each of the seven models, fix all but nine K2P parameters at the rational
values in `src/r3_k3p_common_point_data.py`.  The remaining nine parameters
must solve the nine exact K2P orbit equations defining `p*`.

**INTERVAL CERTIFIED.** For each model, the verifier uses a rational box of
radius

\[
10^{-30}
\]

around the recorded rational center.  With exact rational interval
arithmetic it verifies:

1. the Krawczyk image is strictly inside the box;
2. the infinity-norm contraction bound is less than `10^-20`;
3. the inclusion margin is greater than `9*10^-31`.

The Krawczyk theorem therefore isolates one unique real root in each box.
Because every equation has rational coefficients and the Jacobian is
nonsingular, every coordinate of each root is a real algebraic number.

**INTERVAL CERTIFIED.** Throughout every box:

- every transition probability is greater than `1/20`;
- every inheritance probability equals `1/2`;
- the complete K3P parameter point is therefore strictly stochastic.

The nine equations determine all 16 Fourier coordinates because the
parameters lie on the K2P diagonal.  Thus all seven algebraic roots map
exactly—not approximately—to the same tensor `p*`.

## Rank at the common point

At each isolated root, take the recorded square K3P Jacobian block: order 14
for records 1, 2, and 4, and order 15 for records 3, 5, 6, and 7.

**INTERVAL CERTIFIED.** For each block, let `Y` be the exact rational inverse
of the block at the box center.  Exact interval evaluation proves

\[
\|I-YJ(X)\|_\infty<10^{-20}.
\]

The Neumann criterion makes every block nonsingular throughout its box.  In
particular, the maps have ranks 14 and 15, respectively, at the exact roots.

## Stochastic geometry

**PROVED.** At the smooth point `p*`, every `H14` map has rank equal to the
dimension of `V(I)`.  The relative submersion theorem gives a neighborhood
of `p*` in `V(I)` contained in each of the three `H14` stochastic images.
Their intersection is therefore relatively open and 14-dimensional.

**PROVED.** Every `A15` map is a submersion onto the full ambient tensor space
at `p*`.  Each of its stochastic images contains an ambient neighborhood of
`p*`; the four-way intersection is open and 15-dimensional.

Intersecting these neighborhoods shows that every `H14` image has a
relatively open 14-dimensional piece inside every `A15` image.  This proves
the one-sided relation `H14 preceq_K3P A15` and gives a simultaneous
seven-model intersection of local dimension 14.

## Labelled topology counts

After all port labels, exact rooted isomorphisms, root suppression, and
semi-directed isomorphisms are accounted for:

| class | rooted topologies | semi-directed topologies | one-triangle semi-directed |
|---|---:|---:|---:|
| `H14` | 15 | 9 | 3 |
| `A15` | 24 | 12 | 12 |

The two semi-directed sets are disjoint and together give the inherited 21
reticulate three-port semi-directed topologies.  Because `p*` is invariant
under all leaf permutations, the exact common-point and rank certificates
apply simultaneously to every labelled presentation in the corresponding
class.

Within the one-triangle root subclass, the 33 rooted and 15 semi-directed
topologies therefore split as follows:

- nine rooted cycle presentations, representing three semi-directed
  topologies, belong to `H14`;
- 24 rooted theta presentations, representing twelve semi-directed
  topologies, belong to `A15`.

The first group is one-sided generically contained in the second group on a
nonempty regular open region.

## Move and propagation statement

Define `R3_H` to replace a three-port root blob by any other labelled member
of `H14`, and define `R3_A` analogously for `A15`.

**PROVED.** `R3_H` and `R3_A` are the complete `bowtie_K3P` moves inside the
reticulate three-port census.  In addition, replacement from an `H14` member
by an `A15` member is a one-sided containment move, not an observational
equivalence move.

**PROVED.** Characterwise Fourier tripod inversion propagates both symmetric
overlaps and the one-sided containment after arbitrary identical
corresponding rooted tree or network components are attached at the ports.
The common external dimensions add on both sides, while the local codimension
one difference remains.

## R3 model hierarchy

**PROVED.** The exact hierarchy for reticulate three-port root blobs is:

- JC: one dimension-4 `R3` class containing all seven models;
- K2P: one dimension-9 `R3` class containing all seven models;
- K3P: one dimension-14 quartic class and one dimension-15 ambient class,
  with strict one-sided containment from the former into the latter.

Thus K2P adds edge information without resolving any `R3` topology, whereas
K3P refines the ambiguity but still does not restore topological
identifiability.

The ordinary three-port tree relation, complete-image equalities, and the
full arbitrary-port K3P root atlas remain unresolved.

## Replay

Run

```sh
PYTHONPATH=src .venv/bin/python src/verify_k3p_root_three_port_atlas.py
```

The verifier reproduces `certificates/k3p_root_three_port_atlas.json` using
exact symbolic arithmetic and exact rational interval bounds.
