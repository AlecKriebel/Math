# Complete contraction comparison with Kahle–Sullivant

This is a new audit deduction, written after the named candidate release. It is not a claim that Kahle–Sullivant explicitly stated the full edge-only closure theorem. Primary statements used are Proposition 4.1, Lemma 5.4 and Theorem 5.5 of [Kahle–Sullivant, arXiv:2411.03139v1](https://arxiv.org/pdf/2411.03139), and the arbitrary-design finite-factor criterion of [Geiger–Meek–Sturmfels, Theorems 3.1–3.2](https://arxiv.org/pdf/math/0608054). The full proofs of the additional steps are included here.

## Claim and normalization

Let p_n be normalized laws on a fixed finite binary cube, each a finite nonnegative product of unary and original-edge factors on G, and each MTP2. Suppose p_n tends pointwise to p. Then p also has such finite factors. Literal edge-only and isolated vertices are treated at the end.

Factorization gives full global Markov even at zeros: conditional on an assignment of a separator of positive probability, the remaining components have independent products and finite separate normalizers. Each global conditional independence is a finite polynomial identity in marginal probabilities. It therefore passes to p. The MTP2 inequalities also pass to p, so its nonempty support S is closed under coordinate meet and join.

## 1. Pins and ties produce a natural quotient lattice

Write b=meet S and t=join S. Delete pinned coordinates P={i:b_i=t_i}. For every remaining i define m_i=meet{x in S:x_i=1}. Write i=>j if (m_i)_j=1; this is equivalent to x_i<=x_j for all x in S.

S is exactly the pinned cube subject to these implications. For the converse inclusion, an assignment satisfying the implications is the join of b and the m_i corresponding to its active 1 coordinates. Each chosen m_i is below that assignment, and their join has precisely those active 1 coordinates. Thus the join lies in S and equals the assignment.

Partition active coordinates into mutual-implication classes K, and let Q be their set. Mutual implication is precisely equality of the two coordinate values on every support point. The remaining implication relation is a partial order on Q. Choosing one value y_K per class identifies S with all upsets of this poset. Orienting the order oppositely gives the order ideals used by Kahle–Sullivant. The quotient lattice T contains 0 and 1 and has rank |Q|: take a linear extension and add its elements in a permissible order, one at a time. T is therefore natural in their Definition 2.4.

Let H have vertex set Q and an edge KL whenever some ORIGINAL G edge has endpoints in distinct active classes K,L. Ignore pinned vertices and edges within a class. Let q be the pushforward of p under class values.

If Q is empty, S is the single pinned configuration, and unary pin indicators already give its normalized mass 1. No quotient design or logarithm argument is needed; apply the literal edge/isolate conversion below. Hence the remaining steps can assume Q is nonempty.

## 2. Global Markov passes to the quotient

Suppose disjoint A,B,C subsets of Q have C separating A and B in H. Let A*,B*,C* be unions of their original classes. Then C* union P separates A* and B* in G: any G path avoiding pins and C* projects, after suppressing consecutive repetitions of class labels, to an H walk avoiding C. Such a walk cannot connect A to B.

Full global Markov for p gives X_A* independent of X_B* conditional on X_C*,X_P. X_P is deterministic, and class coordinate vectors are bijective functions of their class values on the support. This yields Y_A independent of Y_B conditional on Y_C for q. This argument works with marginalized variables outside A union B union C and does not assume positivity outside T. It does not assume contraction preserves factorization of arbitrary unconstrained marginals.

## 3. Equality classes induce connected subgraphs of ORIGINAL G

This is the step not stated by KS Proposition 4.1, which only concerns natural support. It is elementary, but it must be supplied.

For active j define n_j=join{x in S:x_j=0}. Then (n_j)_k=0 exactly when k=>j, for active k. Fix i,j in the same class K. The support points l=n_j and h=n_j join m_i agree outside K and have, respectively, all 0 and all 1 on K. Indeed their difference set is {k:i=>k=>j}=K. Pinned coordinates agree as well.

If G[K] were disconnected, partition K into a component A containing i and B=K minus A. C=V minus K separates A and B in G. Conditional on the common C value, l and h each have positive probability. The marginal events X_A=1 and X_B=0 both have positive conditional probability, so conditional independence forces their mixed joint event to have positive probability. A,B,C partition V, so this event is the single mixed configuration. It assigns 1 to some members of K and 0 to others, contradicting the definition of a tie class. Thus G[K] is connected.

This uses full global Markov, not just pairwise Markov: conditioning on the other members of a tied class can make pairwise conditions vacuous.

## 4. Cover localization and the EDGE design

The quotient q has natural support T and is globally, hence pairwise, Markov for H. KS Proposition 4.1 now says that each poset cover is an edge of H. By H's definition, each such edge has a representative original G edge.

KS Lemma 5.4 is written for the maximal-clique incidence design A_H. Its proof, however, singles out a forbidden configuration on each cover pair. The following is the precise edge-design specialization; it does not require using clique factors supplied by Theorem 5.5.

Let B_H be the incidence matrix whose rows are unary cells and H-edge cells, and whose columns are binary assignments y on Q. Every column has a nonzero entry if Q is nonempty. If y is outside T, some cover implication K=>L is violated. The cell (y_K,y_L)=(1,0) on the H edge KL occurs in no point of T. That row is therefore a nonzero entry of y's column absent from every support column. This is exactly B_H-feasibility. Conversely all T columns satisfy every cover constraint. This is the same local missing-cell argument as KS Lemma 5.4, now for the exact smaller edge design.

One can avoid toric terminology by the next direct log-design step.

## 5. Restricted approximation and finite weights

Let D be the subcube consisting of the original pinned values and equal values within each class. Restrict p_n to D and renormalize:
q_n(y)=p_n(x(y))/Z_n, with Z_n=sum_y p_n(x(y)).
Since p is entirely supported on D, Z_n tends to 1. For sufficiently large n it is positive. Each original factor restricted to D is a scalar, a unary class factor, or a factor on an edge of H. Thus q_n has finite unary and H-edge factors and tends to q. No claim is made that the unrestricted pushforward of p_n factorizes on H.

All q_n(y) are positive on T for sufficiently large n, because T is finite and q is positive there. Let L_T be the finite-dimensional subspace of functions on T spanned by the unary and H-edge cell indicators. The constant function belongs to it. Taking logarithms gives log q_n restricted to T in L_T. The logs converge pointwise to log q restricted to T; finite-dimensional linear subspaces are closed. Hence log q on T has finite coefficients in the SAME edge design.

Exponentiate those coefficients on local cells occurring in T and put zero on every missing local cell. On T the product is q; off T a violated cover gives a zero factor by section 4. This proves finite edge factors, without introducing any clique of size greater than two. It is also exactly the content of the GMS arbitrary-design criterion once toric membership and B_H-feasibility have been established.

## 6. Lift to original edges and pins

Choose a spanning tree within each connected G[K] and put equality indicators on its edges. Choose an original cross-class edge for each nontrivial quotient-edge factor and place that factor there. Place each class unary on one member of its class; place pin indicators on pinned vertices. Give unused edges factor 1. The product vanishes outside D by equality and pins; on D it equals q, and hence equals p. All values are finite and nonnegative.

For the literal source family, when E is nonempty every isolated coordinate is uniformly independent of the others in every p_n and p. Remove the isolates; on the remaining graph every vertex has an incident edge, so each unary (including pins) can be absorbed into an original incident edge. Reattach the uniform isolated factor and absorb its scalar 2^(-number of isolates) into any original edge. No nonuniform isolated law is admitted. If E is empty and V is nonempty, the literal normalized empty-product family is empty; under a tacit scalar convention it is the singleton uniform family. Both are closed. V empty has the unique mass 1.

## Priority assessment of this deduction

There is no unresolved mathematical gap in the above derivation. Therefore a categorical assertion that KS is inapplicable merely because original support has pins or ties is untenable. The full closure claim follows from the prior natural-support framework after elementary reductions, an edge-design adaptation of its proof, and the connected-tie lemma proved here.

However, KS Theorem 5.5 as literally stated only supplies clique factors on the quotient; it is not by itself an assumption-preserving statement of the source theorem. The connected-tie lemma and the restricted EDGE design must appear in the specialization. Their proofs are short consequences of standard support and conditional-independence reasoning; they require no new optimization, algebraic theorem, or unresolved equivalent claim. This is strong prior-framework reducibility evidence and substantially weakens a claim of a new closure mechanism. It is not evidence that an earlier author explicitly published or claimed the full corollary. The exact historical status of this omitted corollary remains distinct from mathematical derivability.
