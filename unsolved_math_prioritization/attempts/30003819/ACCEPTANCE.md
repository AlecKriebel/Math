# Acceptance of a structural differential-poset upper bound

## Decision

**Accept the structural partial result without mathematical correction.** PROOF.md retains the complete graph-theoretic proof and analytical constructions. AUDIT.md retains the full eleven-part independent logical review, including boundary cases and the exact remaining gap.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The general local recurrence remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

## Exact accepted statement

Let r be a positive integer and P an infinite locally finite N-graded poset with finite ranks, a unique minimum, and ordinary unweighted up/down operators over Q satisfying DU-UD=rI, equivalently the integer incidence identities. Write p_j=|P_j| and let B_j be the bipartite incidence graph between ranks j-1 and j. With beta(H)=|E(H)|-|V(H)|+c(H), including isolated vertices, put b_j=beta(B_j).

For n>=2, let Z=P_(n-2), X=P_(n-1), and let S comprise precisely the z in Z having at least one successor x in X whose full lower-cover set is {z}. H_S retains all vertices of X, exactly S on the other side, and all their incidences. Set q_n=beta(H_S). Then

    0 <= q_n <= b_(n-1),
    p_n <= 1+r sum_(k=0)^(n-2) p_k+(r-1)p_(n-1)-q_n,

or equivalently

    p_n <= r p_(n-1)+p_(n-2)+b_(n-1)-q_n.

The bound is uniform in this class and determined by the two preceding ranks, but it depends on their incidences rather than only their cardinalities. It improves Byrnes's bound whenever q_n>0. The cycle identities are exact: b_n-b_(n-1)=r p_(n-1)+p_(n-2)-p_n. Thus nonnegativity of b_n does not by itself prove the desired monotonicity b_n>=b_(n-1).

## Retained proof and consequences

For each z in S, a singleton successor supplies a witness. All nonsingleton rank-n vertices above that witness have their entire lower neighborhood among the successors of z. Their stars form a tree on those terminals, with disjoint rank-n internal vertices for different z. Replacing each star of H_S by its witness tree preserves components and changes the edge and vertex counts equally. All X vertices, including isolates, remain. The union is a subgraph K of B_n, so q_n=beta(K)<=b_n. The proof includes S empty, singleton terminal trees, r=1, rank zero and n=2 boundaries; no b_0 is required.

If S=Z, then q_n=b_(n-1), giving the conjectured local inequality at that step. In particular this holds whenever the preceding rank n-1 was created by reflection-extension; the next extension to rank n may be arbitrary. This indexing is essential.

If n>=3 and each z in Z has at least two distinct singleton successors, equality in the local inequality holds if and only if the extension from rank n-1 to rank n is reflection-extension, up to relabeling rank n. The full two-witness argument is retained. It is not asserted with only one witness.

At rank one each element has r+1 successors and at most r-1 nonsingleton successors, hence at least two singleton successors. Consequently p_3<=r p_2+r for every positive integer r, with equality precisely for reflection-extension from rank two.

Both sharp infinite constructions are retained. For r=3, put one rank-two vertex over each pair of the three rank-one vertices and two singleton successors over each, then reflect: ranks (1,3,9,30), q_3=1, and Byrnes's 31 improves sharply to 30. For r=1, use Young's lattice through rank five and reflect twice: ranks (1,1,2,3,5,7,12,19), q_7=1, and Byrnes's 20 improves sharply to 19. The reflection construction is proved to prolong each prefix indefinitely. Replacing q_n by c q_n for any c>1 fails for either example.

The relaxed layers (1,3,3,7) have both middle commutators equal to I while 7>3+3. Their bottom relation fails for r=1, so they are not a differential-poset counterexample. They show that two-middle-commutator data alone are insufficient. The projected common-cover graph contains a triangle; its bipartite incidence graph is a six-cycle. The proof's wording now makes this distinction explicit.

## Historical evidence and distribution

The original independent implementation reconstructs both sharp examples, reflection prefixes for 1<=r<=5 through rank five, and Young's lattice through rank twelve, including proper-S and isolated-vertex cases. Its exhaustive extension enumeration retains prior labels and uses canonical labels for new vertices, without quotienting by isomorphism: r=1 has 1,1,1,1,2,7,60 prefixes through ranks 1,...,7; r=2 has 1,1,4 and r=3 has 1,2,288 through ranks 1,...,3. These are finite labeled enumeration counts, not isomorphism-class counts or an all-rank test.

Saved normal, -O and -OO independent outputs are byte-identical, 912318 bytes with SHA-256 4cf44e1a611ee52374d6a60bb56315ef9319a151c0de628803606fe3d6700a78. The candidate's separately identified outputs are 112111 bytes with SHA-256 8e10b81f219fd77204963bcc4af9cc30353bce4f0c4dd830b5d96e2bbc9d6296. Explicit exception guards survive optimization. Historical negative controls reject a removed top vertex, the invalid relaxed minimum, and the coefficient-two bound. No such mathematical computation was rerun during preparation.

The complete written proofs and analytical constructions are retained. This is not a computational reproduction package: executable code, raw enumeration datasets, copied source documents and images, and private coordination material are omitted. Historical finite checks are supporting evidence; the uniform theorem and infinite sharpness follow from the written arguments. The historical computations cannot be reproduced from this edition alone.

SOURCES.json records the public scholarly citations, PDF hashes and sizes, and precisely bounded historical retrieval and inspection. Neither complete-document inspection nor a new literature survey is claimed. The original candidate and audit remain unchanged; ACCEPTANCE.json binds the exact public proof, audit and this acceptance note.
