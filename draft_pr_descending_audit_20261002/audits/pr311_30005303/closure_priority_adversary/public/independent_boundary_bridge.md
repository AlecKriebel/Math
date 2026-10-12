# Independent boundary-support bridge (candidate-blind derivation)

Recorded 2026-10-04T17:07:57.136397+00:00. Candidate/root/sibling/inherited reports remain unread. This is an independent mathematical derivation, not a claim of historical novelty. It addresses the exact gap recorded in the first historical conclusion.

## Lemma: facial Boolean sublattices are feasible for original-edge models

Let G=(V,E) have E nonempty. Let A have rows indexed by (e,a), with e in E and a in {0,1}^e, and columns x in {0,1}^V, with A[(e,a),x]=1[x_e=a]. If nonempty S is both a sublattice of the Boolean cube and facial for A, then S equals the intersection, over e in E, of the cylinders over its edge projections S_e. Hence S is A-feasible.

Faciality supplies a finite real vector c with H(x)=c dot A_x zero on S and at least 1 outside S, by GMS Lemma A.2. This H is a finite pairwise energy on ORIGINAL edges, nonnegative everywhere. No submodularity of H is assumed.

Delete coordinates pinned throughout S. Each remaining coordinate takes both values. Define i <= j when, throughout S, x_j=1 implies x_i=1; identify coordinates with both i<=j and j<=i. The equivalence classes form a poset Q. S is exactly the collection of downsets of Q, together with its pinned coordinates. To verify this statement from prior LUZ Lemma4.9, use the uniform law on S: it is MTP2 because S is a sublattice. After removing pins, all its pair projections contain 00 and 11 (the full meet and join of S give them). Each pair projection is full, one of the two three-cell implication supports, or the two-cell equality support. All-pair reconstruction gives exactly the preorder constraints above. The empty/single nonpinned-coordinate cases follow directly from meet/join and full unary margins.

### Equality classes must be connected in G

Fix an unpinned class C. The downsets I=downarrow C minus {C} and I union {C} give two elements x0,x1 of S with all coordinates outside C fixed and every coordinate of C changing from 0 to 1. If the subgraph induced by C were disconnected, partition C into nonempty unions D,F of its components, with no G edge between D and F. Under the fixed exterior, H has no interaction crossing D,F, so

H(x with D=1,F=0)+H(x with D=0,F=1)=H(x0)+H(x1)=0.

Nonnegativity forces both split states to be zero-energy states and hence elements of S. But such a state splits one equality class, a contradiction. Thus G[C] is connected.

### Every cover relation has an original edge

Let C<D be a cover in Q, so no class lies strictly between them. Set I=downarrow D minus {C,D}. This is a downset: if a predecessor of a class in I were C, there would be a class strictly between C,D. Also I union {C} and I union {C,D} are downsets. These three elements of S have the same values outside C union D and the class states 00,10,11. The fourth state 01 is forbidden by C<D.

If there were no G edge joining a coordinate of C to a coordinate of D, the pairwise form of H would give

H(01)=H(00)+H(11)-H(10)=0,

contradicting that the fourth state lies outside S and must have H>=1. Therefore at least one original G edge joins every cover pair C,D.

### Reconstruct S using original edges

A state whose every edge projection lies in S_e satisfies equality along every edge within each class C; connectedness makes its entire C constant. On an original edge joining each cover C<D, its edge support forbids the class state 01, so the state respects every cover and therefore every order relation in Q. Every pinned nonisolated coordinate is forced by its assigned incident edge support. Any isolated coordinate cannot be pinned or related to another coordinate: H is independent of it, so membership in its zero set S is independent of its value. Thus no isolated restrictions need be imposed. Consequently the state belongs to S.

The reverse inclusion is immediate, proving original-edge cylinder equality and A-feasibility.

## Exact closure deduction

Let p_n in source-literal M_I(G) intersect M_2(G) converge pointwise to p. The simplex and all MTP2 inequalities are closed; global Markov is closed because each separated conditional independence is a finite collection of polynomial identities, including zero-conditioning cells. Thus p remains normalized, MTP2, and globally G-Markov. Replacing each real factor by its absolute value yields the same p_n, so p_n lies in the nonnegative original-edge monomial image. The toric binomials are continuous, giving p in X_A. By GMS Lemma A.2, S=supp(p) is facial, and MTP2 makes it a sublattice. The new derivation above makes S A-feasible. GMS Theorem3.1 gives finite nonnegative (hence finite real) ORIGINAL-edge factors for p with exact normalization already built in.

If E is empty,V nonempty the source-literal M_I is empty, so closure is vacuous. If V is empty it contains the unique law. Isolated coordinates for E nonempty stay uniform and independent in every p_n and its limit; the proof's A has no isolate rows and handles this literal convention directly.

## Priority interpretation pending exact comparison

GMS Theorem3.1, its LemmaA.2, and LUZ Lemma4.9 are explicitly prior. The equality-connectivity and cover-edge arguments above are an unstated support bridge in those inspected bodies. They are elementary once the facial-lattice formulation is isolated. It would be inaccurate to label this derivation a prior explicitly stated full theorem. It would also be inaccurate to presume a genuinely substantive new lemma before further priority comparison: this may qualify as a short corollary combining standard Boolean-lattice and exposed-face facts. The exact historical status of this bridge remains the priority target.

Completion estimate: 65% of independent priority audit. Strongest verified result: an independent exact hypothesis-preserving closure deduction with an elementary bridge, subject to adversarial review of the downset reconstruction and cover-context claims. Gap: whether the bridge/full consequence has been previously stated or is routine enough to fail the intended research novelty bar.
