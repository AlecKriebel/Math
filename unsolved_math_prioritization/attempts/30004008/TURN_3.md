# Turn 3: exact color quotas around a retained core

Status: an exact criterion for a specified gluing construction and a sufficient condition using credited two-multi-root theory. Full original target unresolved. No novelty certification.

## 1. Setup and restriction

Let C be a nonempty connected vertex set. Suppose every connected component P_j of the underlying graph outside C is adjacent to exactly one vertex v_j of C. Different P_j may have the same attachment. Write s=|C|, d=s-1, a_j=|P_j|, A=Σa_j=n-s, q=A+d=n-1. The case A=0 is allowed.

Each input tree restricts to a spanning out-arborescence on C. Its root is the original root if that root lies in C, or v_j if its root lies in P_j. This follows by the same unique-path argument as Turn2: leaving C and returning would revisit the sole attachment. Write π(r) for this projected root. The restriction to P_j∪{v_j} is rooted at v_j exactly when the original root is outside P_j.

Let R_j be the set of colors rooted in P_j and c_j=|R_j|. These color sets are pairwise disjoint. We seek d colors J for a rainbow core tree, and assign each of the other A colors to exactly one pendant piece, a_j colors to P_j, always choosing colors outside R_j so each pendant tree can be built greedily from v_j.

## 2. Exact quota lemma

**Lemma.** For a fixed J of size d, that assignment exists if and only if

|J∩R_j| ≥ L_j := max(0, c_j-A+a_j) for every j.

Necessity follows because among the A remaining colors exactly c_j-|J∩R_j| are forbidden for piece j, which needs a_j distinct colors.

For sufficiency, make a bipartite graph with a_j identical slots for piece j and all A remaining colors. A slot of piece j is adjacent to colors not in R_j. A set of slots from just one piece has enough neighbors by the inequality. Any set of slots meeting two or more pieces has *all* A colors as neighbors: a color's root belongs to at most one P_j, so it cannot be forbidden for both pieces. Hall's condition follows, and a perfect assignment exists. Afterward, build each pendant arborescence from its attachment using its assigned colors and glue to any rainbow core tree on J. Intersections at attachments create no cycles or extra indegrees.

This is an iff statement for this outward pendant-piece construction. It is not asserted necessary for an unrestricted global rainbow tree, whose root could lie outside C.

A feasible reserved set J of size d exists iff ΣL_j≤d (since the R_j are disjoint and L_j≤c_j), assuming q≥d. Equivalently, the original slot-to-q-colors graph has an injection iff a_j+c_j≤q for every j; its Hall conditions again reduce to the single-piece conditions. Thus those simple balance inequalities also imply ΣL_j≤d. If there are no pendant pieces, all conditions are vacuous.

## 3. Selecting a core with few repeated projected roots

Let m_v count all q colors whose projected root is v∈C, and let ℓ_v=Σ_{j:v_j=v}L_j. For a set P⊆C of at most two vertices, define u_v=m_v if v∈P, and u_v=min(m_v,1) otherwise.

There exists a feasible reserved J of size d whose only possible repeated projected roots belong to P iff

ℓ_v≤u_v for every v, and Σℓ_v≤d≤Σu_v.

Necessity is immediate. For sufficiency choose integer k_v between ℓ_v and u_v summing to d, filling capacities greedily after the lower bounds. In the projected-root group of v, first choose L_j colors from each disjoint R_j attached there, then fill to k_v from the other available colors of that group. This is possible because k_v≤m_v. The quota lemma assigns the discarded colors to pendant pieces. The credited Theorem4.5 of [arXiv:2412.15457v2](https://arxiv.org/abs/2412.15457v2) solves the reserved core instance, and gluing solves the original instance.

This criterion can be checked by enumerating at most quadratically many P. It is a sufficient condition for existence, with an exact combinatorial test for whether this particular use of the two-multi-root theorem is possible.

The lower bounds cannot be discarded. Take three one-vertex pendant pieces at three distinct core vertices, core size10, d=9, A=3, q=12, and four colors rooted in each piece. Then m=(4,4,4) and the unconditioned two-repeat capacity is9, but L=(2,2,2). Every feasible reserved set has three repeated projected roots. The criterion correctly refuses to certify this instance. This is not a counterexample to the original conjecture.

## 4. A balanced block always exists

Give each graph vertex weight w(v)=1+ρ(v), where ρ(v) is its original input-root multiplicity. Total weight is2n-1. In the block-cut tree of the underlying connected graph, place each articulation vertex's weight on its cut node and each non-articulation vertex's weight on its unique block node. A weighted tree has a centroid node for which every complementary component has weight at most half the total: repeatedly move into a component with more than half the weight; a move cannot be reversed, so this finite walk terminates.

If the centroid is a block node, take that block as C. If it is a cut node, take any incident block as C. Every component P_j outside C lies within a complementary centroid-tree component. Hence w(P_j)≤(2n-1)/2, and integrality gives a_j+c_j≤n-1=q. The quota lemma therefore permits some reserved core set J. This recovers a direct, simultaneous block reduction without requiring sequential root-count updates.

It also gives an instance-specific sufficient condition: if a balanced block supports the conjecture for all its possible retained color instances, that one block suffices, even if other blocks are large and structurally unrestricted. In particular a balanced cycle block, or one of order≤6, is enough by the credited results. For the general case, locating a balanced block does not solve its arbitrary-root core instance.

## 5. Boundary checks

A singleton core is permitted; it requires J=∅ and all quota lower bounds zero. A non-balanced chosen core can fail even in a trivially solvable instance: a two-vertex core with a two-vertex pendant piece and all three color roots in that piece has L=3>d=1. One must not silently move the output root into the proposed core.

`verify_turn3.py` checks the quota lemma against explicit matching, and the projected-root capacity test against exhaustive reserved subsets on bounded abstract instances. It also verifies the displayed obstruction vectors. This finite computation does not assert anything about the unresolved core problem.
