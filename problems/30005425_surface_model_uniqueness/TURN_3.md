# Turn 3 — Sharp cycle-rank and size thresholds for underlying topology

AI-assisted mathematical proof candidate; independent review pending. Original unresolved 3/5. The assertions concern the underlying oriented surface of an acyclic gentle cover, without labels or a claimed interpretation of the OWR rotations.

## 1. A general low-cycle-rank uniqueness theorem

Let Q be a finite connected acyclic quiver admitting a locally gentle quadratic ideal J. Put n=|Q0|, m=|Q1| and β=m−n+1, the cycle rank of the underlying undirected multigraph. For the standard surface S of kQ/J, let g be its genus and b its number of boundary components. Then

2g+b=β+1, with b≥1.

Indeed, neither Q nor its quadratic Koszul dual has a directed cycle, because both have the same acyclic underlying directed quiver. Thus both puncture counts p,p* in Palu–Pilaud–Plamondon Remark 4.11 vanish. Their genus formula gives the displayed equality. The construction is connected for connected Q. A finite acyclic quiver has a source, whose missing incoming arrows give blossoms; equivalently its finite maximal paths provide boundary marked points. Hence b≥1. The isolated one-vertex case has the usual disk model and also satisfies the formula.

Consequences:
- β=0 forces g=0,b=1: every cover has an underlying disk;
- β=1 forces g=0,b=2: every cover has an underlying annulus;
- β=2 permits precisely (g,b)=(0,3) or (1,1).

By classification of compact connected oriented surfaces, the first two cases have unique underlying oriented topological type, independently of the relation choices and their saturation. This is a direct credited consequence of the established genus formula. It does not identify marked/dissected/labelled models, and does not assert the source's tile-rotation equivalence.

The turn-1 example has β=5−4+1=2 and realizes both possibilities. Thus cycle rank two is the sharp threshold for varying underlying topology among acyclic covers.

## 2. Sharp number of vertices and arrows in the acyclic class

No connected acyclic quiver on at most three vertices can have gentle covers with different underlying topological types. Here parallel arrows are allowed and counted separately.

For one or two vertices, the degree bounds permit at most two parallel arrows in a single direction, so β≤1 and Section 1 applies. For three vertices, choose a topological ordering 0<1<2 and write x,y,z for the multiplicities of 0→1, 0→2, 1→2. Then x+y≤2, y+z≤2 and x,z≤2. Thus m=x+y+z≤4. If m≤3, β≤1. If m=4, both inequalities imply y=0 and x=z=2. Therefore the only remaining quiver is the double-arrow chain 0⇒1⇒2.

At its middle vertex the gentle relation table must be one of the two 2×2 permutation matrices. The source and sink have no relations. Swapping the two arrows on either side exchanges these two tables, so the resulting bound quivers are isomorphic. The established surface correspondence therefore gives homeomorphic underlying surfaces. More explicitly, the two maximal permitted threads each have vertex list (0,1,2). Their ribbon graph has two cyclically ordered vertices and three paired edges, with one boundary cycle; hence g=1,b=1. This proves the claim for all possible string ideals I: imposing J⊆I only selects a subset of these two candidates.

The four-vertex five-arrow example from turn 1 attains variation. It is consequently vertex-minimal among connected acyclic quivers, even allowing parallel arrows. It is also arrow-minimal: with at most four arrows, any connected quiver on at least four vertices has β≤1, while the at-most-three-vertex case was just excluded. This minimality is only for variation of underlying topology in the acyclic class, not for arbitrary cyclic covers or the source's undefined rotation relation.

## 3. Exhaustive supplemental controls

`python turn3/verify_minimality.py` enumerates every topologically ordered quiver on at most four vertices with arrow multiplicities 0,1,2, enforces the two-in/two-out bounds and connectedness, and tests every gentle relation table, including nonsaturated ones. This includes 52 quivers and 125 covers. It verifies no punctures, the general formula, the β≤1 conclusions, the three-vertex exceptional chain and the attained four-vertex/five-arrow threshold. Its 480 exact assertions and complete variable-topology records are in turn3/verification.json. Topological ordering makes this enumeration complete up to relabelling; the proof in Section 2 does not rely on the computation.

## 4. Credit and status

The genus formula and bound-quiver/surface correspondence are from Palu–Pilaud–Plamondon, https://arxiv.org/abs/1807.04730v2, Theorem 4.10 and Remark 4.11, with the OPS comparison in Remark 4.13. No novelty certification is claimed for these deductions. Original OWR problem unresolved 3/5. Informal completion estimate 45%: the underlying-topology obstruction is now sharp in a natural class, while the decisive rotation equivalence remains unspecified.
