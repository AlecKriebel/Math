# An incidence-dependent upper bound for differential posets

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written proofs and analytical constructions are retained. This is not a computational reproduction package: executable code, raw enumeration datasets, copied source documents and images, and private coordination material are omitted. Historical finite checks are supporting evidence; the uniform theorem and infinite sharpness follow from the written arguments. The historical computations cannot be reproduced from this edition alone.

The general local recurrence remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

## Result and scope

Let r be a positive integer, and let P be an infinite locally finite graded poset with finite ranks, a unique minimum, and the ordinary unweighted relation DU - UD = rI over Q, equivalently the corresponding integer incidence identities. The differential identity is not being interpreted only modulo a positive characteristic. Write P_j for rank j and p_j = |P_j|. The conjecture considered here is

    p_n <= r p_(n-1) + p_(n-2)                  (n >= 2).

This note proves a uniformly valid structural refinement of Byrnes's bound, with a nonnegative correction computed from the two preceding ranks. The refinement gives the conjectured inequality if every element of P_(n-2) has a successor in P_(n-1) that covers only that element. As consequences, the local inequality holds after any reflection-extension and at n = 3 for every positive integer r. Explicit infinite examples show that the correction is positive and sharp.

The full conjecture remains unresolved by this note. The all-n refinement depends on incidence data, not only on the numbers p_j. No claim of novelty or exhaustive literature coverage is made.

## Notation and elementary consequences

For x in P, let d(x) be its number of lower covers and u(x) its number of upper covers. The diagonal entries of the commutator give u(x) = d(x) + r. Its off-diagonal entries give equality of the numbers of common lower and common upper covers of distinct elements in the same rank.

These common-cover numbers are at most one. Indeed, a pair with at least two common upper covers also has at least two common lower covers. The latter pair of lower covers itself has at least two common upper covers. Iteration produces such a pair in rank zero, which is impossible. This also proves that the bipartite incidence graph between consecutive ranks has no 4-cycle.

Let B_j be the bipartite graph with vertex set P_(j-1) disjoint union P_j and with one edge for each cover relation, for j >= 1. Let e_j be its edge count. Each B_j is connected. For a proof, B_1 is a star. If B_j is connected, the graph on P_j joining elements with a common lower cover is connected. The commutator identifies this adjacency relation with having a common upper cover. Thus all vertices in P_j lie in one component of B_(j+1); every vertex in P_(j+1) has a lower cover, so B_(j+1) is connected.

For a finite graph H, including isolated vertices, put

    beta(H) = |E(H)| - |V(H)| + c(H),

where c(H) is its number of connected components. This is the dimension of its cycle space, over any fixed field. In particular it is nonnegative and cannot decrease when a graph is enlarged by vertices and edges. Put b_j = beta(B_j).

Summing u(x) = d(x) + r over a rank gives

    e_j = r sum_(k=0)^(j-1) p_k.

Consequently the following are exact identities:

    b_j = r sum_(k=0)^(j-1) p_k - p_(j-1) - p_j + 1;       (1)

    p_n = 1 + r sum_(k=0)^(n-2) p_k + (r-1)p_(n-1) - b_n;  (2)

    b_n - b_(n-1) = r p_(n-1) + p_(n-2) - p_n.             (3)

Thus Byrnes's inequality is b_n >= 0, whereas the local conjecture is b_n >= b_(n-1). This distinction is important: nonnegative cycle rank does not prove nondecreasing cycle rank.

## The correction term

Fix n >= 2. Set Z = P_(n-2) and X = P_(n-1). Define

    S = {z in Z : some x in X has exactly one lower cover, namely z}.

Construct H_S from B_(n-1) by retaining all vertices of X, retaining just the vertices S on its other side, and retaining the edges between X and S. Isolated vertices of X are retained. Define

    q_n = beta(H_S)
        = sum_(z in S) (u(z)-1) - p_(n-1) + c(H_S).        (4)

Since H_S is a subgraph of B_(n-1),

    0 <= q_n <= b_(n-1).                                  (5)

### Theorem

For every P, r, and n in the stated scope,

    p_n <= 1 + r sum_(k=0)^(n-2) p_k + (r-1)p_(n-1) - q_n. (6)

Equivalently,

    p_n <= r p_(n-1) + p_(n-2) + b_(n-1) - q_n.            (7)

No extra hypothesis on P is imposed in (6) or (7). The correction is determined before rank n is constructed. It is at least as strong as Byrnes's bound, and its right side lies between Byrnes's bound and the conjectured local bound.

### Proof

For each z in S choose a witness x_z in X with lower-cover set {z}. Write N_z for the set of all upper covers of z in X.

Consider every y in N_z other than x_z. The pair x_z,y has z as its unique common lower cover, and therefore has a unique common upper cover t in P_n. If w is any lower cover of this t, then w and x_z have a common upper cover. Unless w = x_z, they must have a common lower cover. The only possible common lower cover is z. Therefore every lower cover of t belongs to N_z.

Let T_z consist of all vertices of N_z and every t in P_n that covers x_z and at least one other element, together with all incidence edges from these t to their lower covers. Every such t has all its lower covers in N_z. Two different such t share only x_z among their lower covers, since sharing another vertex would be a 4-cycle. Further, each vertex of N_z other than x_z belongs to exactly one such t. Hence T_z is a tree: it consists of stars centered at these t joined at the single vertex x_z. If N_z is a singleton, T_z is the one-vertex tree.

The internal vertices of T_z and T_w in rank n are disjoint when z != w. Otherwise an upper vertex would cover both witnesses x_z and x_w. Those witnesses have disjoint lower-cover sets, contradicting the commutator. The trees can meet only in their terminal vertices in X.

Let K be the union of all T_z, together with every vertex of X, retaining isolated vertices. This is a subgraph of B_n. It is obtained from H_S by replacing, for each z, the star centered at z by the tree T_z with the same terminal set N_z. Such replacement preserves components and cycle rank. More explicitly, if T_z has a_z internal vertices in P_n, it has |N_z| + a_z - 1 edges. Its replacement changes the vertex count by a_z - 1 and the edge count by the same amount. Both the old star and the new tree connect precisely N_z. The internal vertices for different replacements are disjoint. Therefore

    beta(K) = beta(H_S) = q_n.

Cycle-space monotonicity for the subgraph K of B_n gives b_n >= q_n. Substitution in (2) proves (6), and (1) gives (7). QED.

## Cases reaching the conjectured bound

### A singleton successor for every element

If S = Z, then H_S = B_(n-1), so q_n = b_(n-1). Equation (7) is exactly the conjectured local bound.

In particular, suppose rank P_(n-1) was obtained from the preceding prefix by reflection-extension. This extension adds, for each z in P_(n-2), r distinct vertices that each cover only z. Hence S = Z, and every possible differential extension to rank n satisfies the conjectured local bound. This statement does not restrict the extension to rank n to be a reflection-extension.

### Two singleton successors and equality

Assume n >= 3 and every z in Z has at least two distinct singleton successors in X. Then equality in the local bound holds if and only if the extension from X to P_n is the reflection-extension, up to relabeling of P_n.

For the forward direction, use the subgraph K constructed in the proof. It is connected because H_S = B_(n-1) is connected. It contains all vertices of X. Equality in the local bound gives beta(B_n) = beta(K). Every upper vertex t not used in K attaches to existing vertices of X and contributes d(t)-1 to the cycle rank. It follows that all such unused t have d(t)=1.

Fix z and its chosen witness a = x_z, and choose a second singleton successor b of z. Any upper vertex with at least two lower covers and incident to b must belong to K. It must then belong to T_z: if it belonged to T_w, it would also cover x_w, forcing the singleton lower cover of b to equal w. Every internal vertex of T_z covers a. There is exactly one upper vertex h covering a and b. For any y in N_z other than b, the pair b,y has a common upper cover. That cover is nonsingleton, belongs to T_z, and covers a and b. It is therefore h. Thus h covers every vertex of N_z, and it is the only nonsingleton upper vertex in T_z.

Since n >= 3, all z in Z have u(z) >= r+1 >= 2. The nonsingleton upper vertices are therefore precisely one vertex h_z over each N_z. A vertex x in X belongs to exactly d(x) of these neighborhoods, so the degree condition supplies exactly r further singleton upper covers of x. This is precisely reflection-extension. Conversely, reflection-extension has |Z| + r|X| upper vertices, giving equality.

### Rank three for every r

Every element z of P_1 has r+1 upper covers. Its nonsingleton upper covers in P_2 use disjoint nonempty subsets of P_1 minus {z}; otherwise a pair of elements of P_1 would have two common upper covers. There are only r-1 other elements of P_1, so at most r-1 of the upper covers of z are nonsingleton. Thus z has at least two singleton successors.

The preceding results prove, for every positive integer r,

    p_3 <= r p_2 + r,                                      (8)

with equality precisely for reflection-extension from rank two. This is an all-r low-rank consequence; it is not a proof for arbitrary n.

Here b_2 = r^2 + 1 - p_2, so (8) subtracts the explicit quantity r^2 + 1 - p_2 from Byrnes's rank-three bound. The quantity can be positive.

## Sharp infinite examples

Reflection-extension of a valid finite prefix is always possible. Add one upper vertex above the full set of successors of each element two ranks below, and add r singleton upper vertices over each current element. The diagonal commutator holds because a current element obtains d(x)+r upper covers. Off diagonal, a pair obtains exactly one upper cover for each common lower cover. Every new vertex has a lower cover. Iterating therefore gives an infinite locally finite differential poset with finite ranks and the original unique minimum.

First take r=3 and label P_1 by a,b,c. At rank two put one element above each of {a,b}, {a,c}, {b,c}, together with two singleton successors above each of a,b,c. Then p_2=9 and each rank-one element has four upper covers. Reflect to rank three. The ranks are

    (p_0,p_1,p_2,p_3) = (1,3,9,30).

Here Byrnes gives 31, while q_3=1 and (6) gives the attained bound 30. Continue reflecting to obtain an infinite example.

For a strict example with r=1 at a later rank, use Young's lattice through rank five and then reflection-extend twice. The ranks through seven are

    (1,1,2,3,5,7,12,19).

The graph B_6 has e_6=19 edges and 7+12 vertices, hence b_6=1. Every rank-five element has a singleton successor in rank six, so q_7=1. Byrnes gives p_7<=20; (6) gives the attained bound p_7<=19. Continue reflection-extension forever. In particular, replacing q_n in (6) by a fixed multiple c q_n with c>1 is false for this family.

## A sharp obstruction to a purely local matrix argument

The following finite incidence data are not a differential-poset prefix with a unique minimum. They show why checking only the two middle commutators cannot prove the target inequality.

Take layer sizes 1,3,3,7. Every element of the first 3-element layer covers the sole bottom vertex. The next layer has lower-cover sets {1,2}, {1,3}, {2,3}. The 7-element layer has one element covering all three current vertices and two singleton successors above each of them.

If M is the 3 by 1 all-one matrix, C is the 3 by 3 pair-incidence matrix, and N is the 7 by 3 top incidence matrix, then

    C^T C = I + J,       M M^T = J,
    N^T N = 2I + J,      C C^T = I + J.

Thus both middle commutators equal I. Nevertheless 7 > 3+3. The bottom relation fails: the sole bottom vertex has three upper covers rather than r=1. This is not a counterexample to the conjecture. It is an exact one-unit obstruction to discarding the lower-rank consistency conditions. In this relaxed example none of the three relevant lower vertices has a singleton successor, and the triangle in the projected common-cover graph can collapse to a single three-element upper cover. The corresponding bipartite incidence graph is a six-cycle, not a three-edge cycle.

## Historical exact checks and their limits

The following describes the saved candidate checks, which were not rerun during editorial preparation. The program and its raw outputs are not distributed in this edition. The authored program uses integer bit masks and integer incidence counts. It verifies the commutator, connectedness, formulas (1)-(3), the correction (4), and the actual tree replacement K used in the proof. It checks:

- The two sharp examples and their explicit incidence lists.
- Reflection examples for 1<=r<=5 through rank five.
- Young's lattice through rank twelve.
- Exhaustive recursively generated, labeled rank extensions for r=1 through rank seven, with 1,1,1,1,2,7,60 generated prefixes at ranks 1 through 7.
- The corresponding labeled enumeration for r=2 and r=3 through rank three, with respectively 4 and 288 rank-three prefixes.
- Acceptance of the two middle commutators in the relaxed example, and rejection when it is presented as a full prefix.

Labels are retained. These counts are not counts of isomorphism classes and are not compared as such to Byrnes's table. For example, the r=1 generated prefixes have 7 rather than 5 entries at rank six because isomorphic prefixes can appear with different labels.

Every asserted mathematical condition in the checker uses an explicit exception-based test, not Python assert. The saved historical runs under normal Python, -O, and -OO produced byte-identical JSON. These finite checks support implementation and example correctness; the proof of (6) is the graph argument above, and finite checks do not establish the full conjecture.

## Sources

1. Patrick Byrnes, Structural Aspects of Differential Posets, University of Minnesota dissertation, December 2012. Chapter 5, PDF pages 47-51 / printed pages 38-42, supplies the connectedness argument, edge-count identity, global Fibonacci upper bound, and separately stated Conjecture 5.9. https://conservancy.umn.edu/server/api/core/bitstreams/45a1bae8-402f-42a7-ad67-4caa7b55d104/content
2. Pritam Majumder, Rank sizes of Differential Posets, Oberwolfach Report 23/2018, printed page 1452 / PDF page 72. This states the requested improvement problem and the local recurrence. Its common-cover axiom has an erroneous terminal '=1'; the present note uses the standard operator definition, allowing zero common covers. https://ems.press/content/serial-article-files/46745
3. Christian Gaetz and Praveen Venkataramana, Path Counting and Rank Gaps in Differential Posets, arXiv:1806.03509v3. PDF page 2 gives the unweighted operator definition and reflection construction; PDF pages 3-4 distinguish Byrnes's global upper bound from lower rank-gap results. https://arxiv.org/pdf/1806.03509

The original upper-bound proof was inspected before the mathematical attempt. This note's connectedness proof is written independently: Byrnes's PDF page 48 contains a rank-inconsistent sentence saying that z in P_k covers x,y in P_k, where the intended pair is v,w in P_(k-1). The result itself follows from the direct incidence-graph induction given here.
