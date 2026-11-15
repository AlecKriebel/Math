# Row122 personal independent source-first reconstruction

2026-11-15 UTC. I personally read all three actual deposited PDF pages, all201
controlling TeX lines and all three fresh individual1450px rendered pages before
any122 foreign mathematical body, supplied code/result, triage/archived/current
peer opinion. SOURCE_READY was used only for exact metadata, paths and custody;
structural filenames were seen, not their scientific contents. No previous
reviewer's reading is claimed as my own. All findings remain local under the
closed root122 initial gate. The conclusions below are hypotheses to verify,
not assumed clearance.

## 1. Exact category, quantifiers and conventions

For a finite simple graph, an L(2,1) labeling assigns POSITIVE INTEGERS, adjacent
values differing by at least2 and distance-exactly2 values unequal. Ordinary
chi^(2,1) is the least k permitting the common initial segment [k]={1,...,k};
list chi_l^(2,1) is the least k for which EVERY assignment of k-element positive
integer subsets is labelable. Lists need not be consecutive or share the same
maximum. The zero-based ordinary span lambda is chi-1: translating a labeling's
minimum to1 preserves all differences, and an optimal positive initial segment
labeling can have no unused initial offset. The exact primary Kohl conventions
remain to check, rather than assuming that a name/notation matches these ones.

The original main claim is an explicitly given11-vertex tree T with ordinary
chi=5 (lambda4) and arbitrary-list chi_l=6. A specific5-list assignment is
uncolorable; an ordinary5-palette witness and a universal Delta+3 tree list
bound give the exact values. The original corollary covers EVERY tuple of six
independently chosen NONNEGATIVE FINITE pendant-path lengths, including zeros,
with both parameters still5/6 and unbounded diameter over the family.

The abstract also identifies a historical universal tree equality in Kohl2006
OWRConjecture4/dissertationConjecture4.4. It expressly does not assert firstness,
minimum order, a novel general-graph obstruction mechanism, or present openness.
The classical tree list bound and Fiala–Skrekovski2001cyclic example are credited.
These source interfaces and the supplement's exact finite counts are still
unverified at this initial seal. No empirical assumption is part of the short
universal proof.

## 2. Independent combinatorial identity and distance family

The vertices are a,b,c,d,e,a1,a2,b1,d1,e1,e2. Edges are ab,bc,cd,de,
aa1,aa2,bb1,dd1,ee1,ee2. Thus connectedness and acyclicity follow directly
from adjoining pendant vertices to P5; |V|=11, |E|=10. The degree-three
vertices are a,b,d,e; c has degree2, six named leaves have degree1. Hence
Delta3. A longest old leaf-to-opposite-leaf path has six edges, while all other
distances are no greater: diameter6, unique central vertex c, radius3.

On a tree, distance-two pairs are exactly pairs of distinct neighbors of the
same vertex. There are sum_v binom(deg(v),2)=4*3+1=13 such pairs, with no pair
counted twice (that would create a four-cycle). Thus a direct certificate needs
only10edge and13distance-two checks. This avoids a hidden replacement by graph
coloring or by a condition on arbitrary pairs with some common neighbor in a
cyclic graph. In a later independent implementation, shortest-path distances
should be computed from the literal edge set, not accepted from supplied data.

## 3. Hall-style forced-neighborhood obstruction family

Let A={1,2,3,4,5}, B={1,3,4,5,6}. B is assigned precisely to a1,a2,e1,e2;
all other vertices have A. All lists have exactly five distinct positive labels.
For b, the neighbors a,c,b1 have A and are pairwise at distance2, so they need
three distinct labels avoiding b and its two consecutive integers. If b=2,3,4,
their available sets are respectively {4,5},{1,5},{1,2}, only two labels. Thus
b in {1,5}. Exactly the same argument applies to d, since c,e,d1 all have A.
The distance-two condition on b,d forces opposite endpoints.

The graph automorphism a<->e,b<->d,a_i<->e_i,b1<->d1 preserves EVERY list.
Thus orient b=1,d=5. This is a graph/list reflection, not a color reflection:
the latter need not preserve B and must not be silently used. Adjacency to both
b,d forces c=3. Adjacency to b and distance-two inequality with c force a=4or5.
If a=4, a1/a2 can only use {1,6} after adjacency and only{6} after avoiding b=1.
If a=5, adjacency leaves{1,3} and avoiding b leaves only{3}. Two siblings cannot
use that single label because they are distance2. This is a local system-of-
distinct-representatives failure, not a heuristic pruning argument. The right
end's B-lists make the opposite b,d orientation equally impossible by the graph
reflection. No case assumes that B is an interval or that a positive common
palette may be replaced by arbitrary five distinct spaced-out integers.

This directly proves the displayed assignment infeasible. Since the list
parameter quantifies over EVERY5-list assignment, one such assignment proves
chi_l>5; it does not say that all5-list assignments are infeasible.

## 4. Ordinary witness, lower bound and an independent exact count family

The listed witness in vertex order above is

    (1,5,3,1,5,3,4,2,4,2,3).

Its spine edge differences are4,2,2,4; pendant differences are2,3,3,3,3,2.
Neighbor-label sets at a,b,c,d,e are respectively
{5,3,4},{1,3,2},{5,1},{3,5,4},{1,2,3}; all have distinct entries. Thus it
passes exactly the stated edge/distance-two conditions. A degree-three center
in [4] has at most two permissible distinct neighbor labels for any own label:
for centers1,2,3,4 these sets have sizes2,1,1,2. Thus no [4] labeling exists,
and the ordinary parameter is exactly5. The lower bound does not generalize
to an arbitrary four-label set with large gaps, which is not the definition.

The paper states eight ordinary [5] labelings; I can independently derive this
without a search. Under b=1,d=5,c=3, ordinary A leaves make a=4 impossible
(both a-leaves would be forced2), hence a=5 with leaf labels2and3 in two orders.
Likewise e=2 is impossible and e=1 with leaf labels3and4 in two orders. The
remaining pendant b1 must be4 (it avoids a=5,c=3 and is nonconsecutive to b=1);
d1 must be2. This gives2*2=4 labelings in this orientation, and4 in the other
orientation by graph reflection, total8. In particular the ordinary witness is
not being confused with the bad B-list instance. The stated [6] count6336 still
needs independent verification, not mere agreement with the printed number.

## 5. Universal arbitrary-list upper bound family

Root an arbitrary nonempty finite tree and process breadth-first. The root has
no earlier constraints. For a nonroot v, the parent is the only earlier adjacent
vertex, excluding at most parent_label-1,parent_label,parent_label+1: three
integers, possibly fewer near the positive boundary or outside the current list.
All earlier distance-two vertices are its grandparent (if present) and earlier
siblings; descendants are later and other same-level vertices are farther away.
If the parent is root, at most Delta-1 earlier siblings exist and no grandparent.
Otherwise the parent has at most Delta-1children; earlier siblings at most
Delta-2 plus one grandparent again totalDelta-1. Therefore at mostDelta+2 list
labels are excluded, leaving one from any arbitrary Delta+3-element list.
At Delta0 the singleton is trivially labelable, so the nonsharp bound still
holds. The rule uses only finiteness/cardinality, not a bounded global label
universe or interval structure. For T, Delta3 gives chi_l<=6, completing exact6.

The claimed historical attribution of the more general sDelta+2d-1 bound to
Voigt/Kohl–Schreyer–Tuza–Voigt needs actual primary verification. The special
(2,1) bound already has a self-contained proof here and is not claimed novel.

## 6. Uniform six-parameter pendant-path extension family

For any tuple(m_a1,m_a2,m_b1,m_d1,m_e1,m_e2) in N0^6, attach a fresh path of that
many new vertices outward from each named old leaf. These are separate paths,
not extra arbitrary branch trees or identifying vertices on different paths.
The old T remains an induced ISOMETRIC subtree: no alternate route between old
vertices is created. All old degree-three vertices remain, original leaves gain
at most one new neighbor, and all new vertices have degree<=2, so Delta stays3.

Along any new path, each next label from [5] must be nonconsecutive to its
parent (at most3forbidden) and different from its grandparent (at most1more).
For the first new vertex the grandparent is the old neighbor of its leaf; after
that it is the preceding path vertex. Thus at least one label always remains.
Between new vertices on distinct paths, distance is the sum of their positive
depths plus the old leaf-to-leaf distance>=2, hence at least4. No cross-path
edge or distance-two condition is missed. This proves ordinary<=5 uniformly;
restriction to the old isometric T gives>=5.

Extend the bad five-lists by ANYfive-element lists at added vertices. A labeling
would restrict to the forbidden old instance, so chi_l>=6; the universal tree
bound gives<=6. All-zero tuple includes T; any chosen single length tending to
infinity yields diameter at least that length+6, so unbounded diameter is a
deduction, not sampling. The claim does not cover infinite paths, new branching,
arbitrary graph superextensions or a uniform family count formula.

## 7. Independent local-state count and adversarial checks planned

A separate exact tree sum-product recurrence can check all finite counts.
For rooted v and candidate parent/own labels p,x, set F_v(p,x)=0 unless
x belongs to its list and the parent edge is admissible. Otherwise sum over
ordered child label tuples(y_i), with all y_i in the respective child lists,
|y_i-x|>=2, y_i!=p and y_i pairwise distinct, the product of F_child(x,y_i).
At the root omit the nonexistent-parent edge and the y_i!=p restriction.
These constraints explicitly include adjacency, grandparent inequality and
distance-two siblings. They are necessary and sufficient: constraints between
different child subtrees can only involve their root children at distance2;
any deeper cross pair has distance>=3. This provides an exact induction-based
mechanism distinct from ordered vertex backtracking and the short forcing proof.
It must not silently allow a locally inadmissible own/parent state; that would
not be an equality recurrence. After the initial seal I can compare a fresh
implementation with the actual supplied checker, without importing its proof.

Useful falsifiers: omit the sibling condition (bad leaves could share one label),
omit adjacent separation2 (ordinary graph-coloring permits consecutive labels),
omit grandparent exclusion (one path might repeat p after two steps), assume a
color reflection preserves the noninterval lists, or infer a universal list
bound from a common-palette count. Each changes a load-bearing condition.
Small explicit witnesses and six independent path lengths should test the
boundary quantifiers; no entire-tree-minimality search or massive campaign is
needed or authorized. Existing negative/historical failures must be retained.

## 8. Exact initial status/gap table and primary interfaces

| Family | Mechanism/evidence personally reconstructed | Initial status / exact remaining gap |
|---|---|---|
|Category|Positive integer labels; initial segment vs arbitrary lists; shift to span|Target conventions clear; actual Kohl notation/conjecture body still uninspected.|
|Graph|Literal10edges/11vertices;13distance-two pairs; Delta3/radius3/diameter6|Direct deduction; later mechanical edge/distance check pending.|
|Obstruction|Three-neighbor endpoint forcing + local distinct-leaf Hall failure|Complete hand proof reconstructed; exact list/graph reflection matters.|
|Ordinary|Direct witness, degree3 [4] lower bound, analytic [5] count8|Complete hand proof; independent [6] count6336 still unchecked.|
|Universal list bound|BFS parent/grandparent/earlier-sibling forbidden set|Complete self-contained proof; historical general-bound attribution still unchecked.|
|Infinite family|Isometric old subtree + separate nonbranching paths + five-choice induction|All six independent finite lengths covered by proof; finite controls pending.|
|Independent count route|Parent/own-label local admissibility + distinct-child sum-product|Complete recurrence definition/induction; fresh implementation and code comparison pending.|
|Credit/target match|OWR2006Conjecture4p416; thesis4.4p124; KSTV2005bound; FS2001Fig4p14|Actual primary bodies and figure topology/earlier general-graph separation need inspection. No firstness/minimality/current-open claim.|

At this point I have found no within-category contradiction in the short proof,
but full source/primary/artifact verification remains open. If a substantive
defect is found, retain the exact gap/counterexample and recommend Deferred—
defect found; do not repair extensively or substitute a narrowed result.
Follow-up defaults to null. No human review or proof-assistant certification
is implied by this initial reconstruction.
