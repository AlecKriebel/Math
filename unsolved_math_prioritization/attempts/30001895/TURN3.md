# Author turn 3: an exact critical-family exclusion at rank three

2026-10-03 UTC. Problem 30001895, separately requested r-element component.
Author response 3 of 5. Overall status: unfinished. Completion estimate: 25%.

The general r≥3 assertion remains unproved and unrefuted. This turn supplies
a finite, independently checkable computational proof for a bounded critical
regime and explains exactly what it implies. It is a candidate partial
mathematical result pending uninvolved review; no novelty claim is made.
The r=2 result remains credited to Alfaro–Rubio-Montiel–Vázquez-Ávila (2024),
as recorded in TURN2.md. Prior checkpoints are preserved byte for byte.

## 1. Partial conclusion and its limits

**Partial theorem, subject to the certificate checks below.** If H is a
finite family of distinct nonempty sets of size at most three and τ(H)≥3,
then

    ν₃(H) ≥ min(|H|,5).                             (6)

Consequently, nonvacuous rank-three families with the (q+1,q)-property,
q≥4, have a transversal of size at most two. This is precisely the target
when r=3 and p=q+1. The p=q case was already elementary in turn 1.
The finite-obstruction lemma extends these positive cases to arbitrary
families. No assertion for p−q≥2 or general r≥4 follows from this turn.

For the global C₃ conjecture, an edge-minimal counterexample must now have
τ≥4, in addition to all conditions from turn 2. This is a genuine exclusion,
but still leaves an unbounded family of cases.

## 2. Why only six through ten edges need computation

Private padding from turn 1 allows us to work with exactly three-element
sets without changing τ or ν₃. From a finite H with τ(H)≥3, delete edges
while the transversal number stays at least three. The resulting family K
is τ-critical and has τ(K)=3: deleting one edge changes τ by at most one,
so minimality could not stop at a larger value.

Bollobás' classical critical-hypergraph bound gives

    h=|K| ≤ binom(3+3−1,3)=10.

This is the credited Theorem 2 of *On generalized graphs* (1965), p. 452,
[primary scan](https://web.vu.lt/mif/s.jukna/EC_Book_2nd/Bollobas.pdf), checked
in turn 2. We use only this edge bound, not a conjectured vertex bound.

Since τ(K)=3, each vertex has degree at most h−2. Otherwise one vertex and
one representative from the at most one missed edge would cover K.
If h≤5, the whole K has degree at most three. If h<5 and H has at least five
edges, extend K to five edges within H: every vertex then has degree at most
(h−2)+(5−h)=3. If H has fewer than five edges, τ(H)≥3 itself implies
Δ(H)≤|H|−2≤2, so H is a 3-packing. These observations handle all small cases.

It remains to rule out a family K with 6≤h≤10, τ(K)=3 and ν₃(K)≤4.
The search below in fact excludes the larger class with τ(K)≥3; it does
not require criticality internally. Criticality justifies the upper bound
of ten edges, and is not an extra assumption silently imposed on H.

## 3. Exact finite incidence encoding

Label K's edges by [h]={0,…,h−1}. Each ground-set vertex x has a support
A_x⊆[h], the indices of edges containing it. A vertex of degree at most
three cannot witness four concurrent edges in a five-edge subfamily.
We retain only supports with size at least four, called high supports.

The following necessary conditions hold:

1. Each high support has size between 4 and h−2, by τ(K)≥3.
2. Each edge index belongs to at most three high supports, since the
   corresponding original edge has three elements.
3. No two high supports have union [h], since their two vertices would
   give a transversal of cardinality two.
4. If two edge indices each already belong to three selected high supports,
   their triples of support identities must differ. Otherwise their original
   three-element edges are equal, contrary to simplicity.
5. Every five-element subset I⊆[h] meets some high support in at least four
   indices. This is exactly the assertion ν₃(K)≤4.

Identical high supports can be reduced to one representative. Doing so does
not lose any witness for condition 5 and only decreases row capacities.
Condition 4 remains necessary after this reduction: if a row has three
distinct retained supports, all three corresponding support types originally
had multiplicity one, because its original edge had only three vertices.
Thus two saturated identical rows would already have been identical edges.
This step does not assume that distinct vertices always have distinct
incidence patterns.

In fact any system satisfying these conditions could be completed to a
counterexample with exactly three elements per edge. Add new private
vertices to each edge until its size is three. Unsaturated rows become
distinct through their private vertices; saturated rows are distinct by
condition 4. A high vertex and a private vertex cover at most h−1 edges;
two private vertices cover at most two; pairs of high vertices are excluded
by condition 3. Hence τ≥3, while condition 5 gives ν₃≤4. For the exclusion
proof, only the forward implication is needed.

Choose a largest high support of size d, where 4≤d≤h−2. Relabel the edge
indices so it equals {0,…,d−1}. Every other high support then has size at
most d. This symmetry reduction loses no system. The finite case list is

    h=6,…,10; d=4,…,h−2,

giving 15 cases. No solver or mathematical assumption selects a smaller
class than the explicitly justified conditions above.

## 4. Search tree and independently implemented checker

critical_tau3_search.cpp enumerates candidate support subsets of [h] with
cardinalities 4 through d and fixes the first support as above. At any node,
it selects a five-element target I not yet covered in condition 5. It lists
every feasible candidate support that covers I. Feasibility uses only row
capacity, the forbidden pair union, and saturated-row distinctness.

Every extension must choose at least one support on that list. The branches
partition extensions by the first support chosen in the list's fixed order:
earlier supports are forbidden in later branches. Each child adds its chosen
support. A leaf is an uncovered target with no feasible support remaining.
All three feasibility failures are persistent under further additions, so
discarding a currently infeasible candidate cannot lose a later solution.
Duplicating a support is unnecessary, as proved above.

The complete trees are saved in turn3_tau3_certificate.json.gz. The gzip
container is just a deterministic storage encoding; its decoded JSON has
15 case records. Each node records a target bitmask and the complete list
of (support bitmask, child-node index) branches. A leaf has an empty list.
No floating-point objective, numerical tolerance or external solver status
forms part of the certificate.

verify_tau3_certificate.py reconstructs all possible candidates directly
from h and d using Python sets and integers. At each node it independently
recomputes the feasible candidates covering the recorded target and checks
that the listed branches equal that entire set. It checks target noncoverage,
the ordered-branch exclusions, legal child additions, strictly increasing
child indices, and that every saved node is visited exactly once. Every
leaf must independently have zero remaining candidates. It also verifies
the complete 15-case parameter list. It does not trust the C++ program's
heuristic, pruning counters or printed satisfiability verdict.

Results: all 15 trees pass, comprising 7,116 nodes and 6,172 impossibility
leaves. Certificate SHA-256:

    4129f71058d0723768a96ba8848a6ac99b0eb87a36189150ec6d8d3d511c058a

The separate checker deliberately rejects a corrupted target and an omitted
required branch. This is an implementation cross-check, not uninvolved
mathematical review. Verification details are in
turn3_certificate_verification.json and turn3_reproduction.json.

Reproduce the complete calculation and byte comparison:

    python3 reproduce_turn3.py

Check the existing certificate without compiling or running the search:

    python3 verify_tau3_certificate.py

Python must run with assertions enabled; do not use `python -O`.

## 5. A handwritten check of the six-edge case

For h=6, every high support has size four. Its complement is a pair of edge
indices. Condition 3 says these complement pairs are pairwise intersecting.
Condition 5 says their union is all six indices: the target omitting index
i is covered exactly when i belongs to such a complement pair.

A pairwise-intersecting family of distinct pairs is either contained in a
star or is a triangle. To see this, take {a,b} and {a,c}; a pair missing a
must be {b,c}, after which no fourth distinct pair can meet all three.
A triangle covers only three indices. A star covering six requires at least
five pairs, hence five high supports, using at least 5·4=20 incidences.
But six triples have only 18 incidences. This contradiction supplies a
short separate proof for the first computational case.

## 6. Deriving the advertised (p,q) consequence

The tree certificates exclude every remaining possible K from Section 2,
so they prove (6). Now suppose H has |H|≥q+1 and the (q+1,q)-property,
where q≥4. If τ(H)≥3, then (6) supplies a 3-packing of size five. Turn 1's
packing-growth lemma, with s=q−1, gives

    ν_(q−1)(H) ≥ min(|H|, 5+(q−1)−3)=q+1,

contradicting the (q+1,q)-property. Thus τ(H)≤2. Private padding handles
rank-at-most-three sets, and the previously proved finite-obstruction
argument handles infinite families. All intersections are common
intersections of distinct member sets; no pairwise-intersection variant
is substituted.

## 7. Remaining work

This does not settle the separately requested r-element component. At r=3,
minimal counterexamples with τ≥4 remain; at r≥4 this turn has excluded no
new critical regime. In particular, the next rank-three case τ=4 has up to
binom(6,3)=20 edges and would require a new complete argument or certificate.
The present code intentionally accepts only h≤10 and does not claim coverage
there. The existing proof budget remains three used turns out of five.
