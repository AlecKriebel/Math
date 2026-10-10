# Finite-radius left-orderability: a negative uniform-radius result and the remaining algorithmic question

Problem: 10300029 / AMR-102-0029, Calegari Question 8.6.
Prepared: 2026-10-06. Status: scoped, literature-based partial; independent review pending.

## Conclusion and limits

Under the usual word-ball interpretation, there is no universal radius that detects left-orderability among closed orientable hyperbolic 3-manifold groups. This already follows from existing Dehn-filling and non-orderability theorems, even using the images of one fixed two-generator marking of one knot group. In addition, a radius depending only on the unmarked manifold cannot work uniformly over all generating sets: the Weeks manifold supplies a fixed-manifold obstruction.

The weaker question of an effectively computable radius for a supplied marking, or a specified effective marking convention, is not answered here. It is equivalent to the corresponding left-orderability decision problem. Thus the complete two-clause problem is not recorded as solved. These are credited consequences of prior work, not a novelty claim.

## 1. What is being asked

The original source is Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, [arXiv:math/0209081v1](https://arxiv.org/abs/math/0209081v1), Question 8.6, printed page 18. It asks first for a universal finite ordering radius and then for an effective manifold-dependent radius. No generating set or canonical word metric is specified there. This note makes that missing parameter explicit. Question 8.3, concerning taut and R-covered foliations, is a different question.

Write S for a finite generating tuple, B_S(r) for its symmetric word ball, and A_r(G,S) for the existence of a subset P of B_S(r) satisfying

1. B_S(r) is the disjoint union of P, P^{-1}, and {1};
2. (P P) intersected with B_S(r) is contained in P.

This is the finite positive-cone test in Calegari--Dunfield, [*Laminations and groups of homeomorphisms of the circle*](https://arxiv.org/abs/math/0203192v2), Section 8, Question 8.1. It depends on the multiplication table in the ball, not just on its vertices or graph distances. Every left order passes every test.

Throughout the counterexamples below, the manifolds are closed, connected, orientable and hyperbolic. Thus neither noncompact manifolds nor orientation ambiguities are needed.

## 2. First approach: long non-orderable surgeries retain every prescribed local cone

### Local transfer lemma

Let q:G -> H be surjective, let S generate G, and put T=q(S). Suppose

    ker(q) intersected with B_S(3r) = {1}.

Then q restricts to a bijection from B_S(r) to B_T(r), and the restricted multiplication and inversion tables agree. Consequently A_r(G,S) and A_r(H,T) are equivalent.

**Proof.** Surjectivity on the balls follows by lifting a word of length at most r. If x,y in B_S(r) have the same image, xy^{-1} lies in the kernel and has length at most 2r, so x=y. For x,y,z in B_S(r), the equality q(x)q(y)=q(z) is equivalent to xyz^{-1} being in the kernel; its length is at most 3r, so this is equivalent to xy=z. Inversion and the identity are preserved as well. Transport P along the resulting bijection in either direction. Both defining conditions are unchanged. QED.

The factor 3 matters: injectivity merely on the radius-r ball does not by itself rule out new multiplication relations between three of its elements.

### Dehn-filling family

Let K=P(-2,3,7), let X be its exterior in S^3, and set G=pi_1(X). Use the two generators a,b of the presentation in Section 4.2 of Clay--Watson's preprint. For an integer n, let

    M_n = S^3_n(K),     G_n = pi_1(M_n),
    q_n:G -> G_n,      S_n=(q_n(a),q_n(b)).

The meridian-longitude convention is the one in that paper. The following established inputs apply:

- G is left-orderable. For example, X is compact and P^2-irreducible with b_1(X)=1, so Boyer--Rolfsen--Wiest [*Orderable 3-manifold groups*](https://arxiv.org/abs/math/0211110v2), Theorem 1.1(1), applies to its surjection onto Z.
- Clay--Watson [*Left-orderable fundamental groups and Dehn surgery*](https://arxiv.org/abs/1009.4176v2), Theorem 28, gives non-left-orderability of G_n for n>17. This uses their parameter m=1 in the family P(-2,3,5+2m). The same source identifies the knot as hyperbolic. Its integer fillings are therefore closed hyperbolic manifolds for all sufficiently large n by Thurston's hyperbolic Dehn-surgery theorem.
- Osin [*Peripheral fillings of relatively hyperbolic groups*](https://arxiv.org/abs/math/0510195v3), Theorem 1.1 and its final finite-subset clause, gives eventual injectivity of q_n on each fixed finite subset of G. The hypothesis is satisfied because a finite-volume hyperbolic knot group is relatively hyperbolic with respect to its cusp subgroup Z^2.

Here is the explicit verification of the last filling condition. In the cusp subgroup, the filling kernel is N_n=<mu^n lambda>, corresponding in Z^2 to <(n,1)>. A fixed nonzero vector (u,v) can lie in N_n only if (u,v)=k(n,1). If v=0 this is impossible; otherwise k=v and n=u/v, so there is at most one possible n. Consequently N_n eventually avoids every prescribed finite set of nonidentity peripheral elements. Nonperipheral elements cannot belong to N_n at all. This is precisely the avoidance condition in Osin's theorem.

Now fix r. Apply that theorem with the finite set B_S(3r); eventually q_n is injective there. The transfer lemma carries a local cone from the left-orderable group G to (G_n,S_n). Thus

    For every r there exists N_r such that every integer n >= N_r
    gives a closed hyperbolic M_n with A_r(G_n,S_n),
    but G_n is not left-orderable.

This proves the negative universal-radius assertion. The number of generators stays two; the tuple is always the image of the same source tuple. No assertion is made that it is geometrically shortest or selected by a separately prescribed canonical algorithm. The argument does not use the L-space conjecture or any foliation implication. It is an elementary consequence of the cited theorems, and no earliest-priority claim is made for the consequence.

## 3. Second approach: even one manifold defeats a marking-independent radius

Let W be the Weeks manifold and Gamma=pi_1(W). Calegari--Dunfield, Theorem 9.1, prove that Gamma is not left-orderable.

A finitely generated non-elementary hyperbolic group has infinite girth over its finite generating sets. The original result is Akhmedov's *The girth of groups satisfying Tits Alternative*, [doi:10.1016/j.jalgebra.2005.01.053](https://doi.org/10.1016/j.jalgebra.2005.01.053). An inspected primary proof that also suffices here is Yamagata's [*The girth of convergence groups and mapping class groups*](https://doi.org/10.18910/9095), Theorems 1.3 and 3.9; apply it to Gamma acting on its sphere at infinity. The group is finitely generated, is not virtually cyclic, and has limit set containing more than two points. Yamagata also states Akhmedov's hyperbolic-group result as Theorem 1.2.

For any r, choose a finite generating tuple T_r for Gamma whose shortest nontrivial reduced relation has length greater than 3r. The epimorphism from the free group on that tuple to Gamma has no nonidentity kernel element in its radius-3r ball. Free groups are left-orderable, so the transfer lemma gives A_r(Gamma,T_r).

Hence

    For every r, A_r(pi_1(W),T_r) holds for some finite marking T_r,
    although pi_1(W) is not left-orderable.

Therefore even a non-effective number c(W), if required to work for every finite marking of W, cannot exist. This result allows the marking to vary; it does not disprove existence or computability of c(W,S) for a fixed S. No bound on the cardinalities of T_r is needed or asserted for this second argument. The first argument already supplies the separate fixed-two-generator obstruction across manifolds.

## 4. Third approach: identify the exact effective-radius gap

### Compactness

For a fixed finitely generated G and marking S,

    G is left-orderable if and only if A_r(G,S) holds for every r.

For the nontrivial direction, form the tree of finite cones, joining a cone to its restriction at the preceding radius. Each level is finite and nonempty. The infinite-branch lemma gives compatible cones at all radii. Their union partitions G\{1} into inverse pairs and is closed under multiplication, since any two elements and their product lie in some ball. It is a positive cone. This is the compactness mechanism already recorded in Calegari--Dunfield Section 8.

### Effective equivalence

Consider an effectively presented class of finitely generated groups equipped with a uniform solution to the word problem. The following are equivalent:

(i) Left-orderability is decidable in that class.

(ii) A total algorithm computes an integer c(G,S) such that A_c(G,S) implies left-orderability.

**Proof.** Each A_r is decidable by constructing the finite ball and its multiplication table and trying the finitely many sign assignments. Given (ii), compute c and decide A_c; necessity supplies the other implication. Given (i), return 1 on an orderable group. On a non-orderable group, test r=1,2,... until A_r fails. Compactness guarantees termination, and the returned radius satisfies (ii). QED.

Hyperbolic 3-manifold groups have solvable word problem; the automatic-group setting of Calegari--Dunfield Section 8 and the certified geometric implementation in Dunfield [*Floer homology, group orderability, and taut foliations of hyperbolic 3-manifolds*](https://arxiv.org/abs/1904.04628v2), Section 6, provide the relevant setting. The equivalence above is explicitly stated with effective word-problem data so it does not silently treat an existence theorem for a solver as a supplied implementation.

An obstruction-radius search alone is only a semidecision procedure: it terminates on non-orderable inputs and has no stopping condition on orderable ones. No computable stopping bound for all marked hyperbolic 3-manifold inputs is established here.

## 5. Current-status and quantifier audit

Dunfield's 2019 paper, Introduction, explicitly distinguishes unknown decidability in the hyperbolic rational-homology-sphere setting from undecidability for arbitrary finitely presented groups. The inspected 2026 preliminary *K3: A New Problem List in Low-Dimensional Topology*, [Problem 3.31, printed page 154](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), again asks the decision question for closed 3-manifolds. Its wider quantifier is not asserted to be identical to the hyperbolic-only question.

Accordingly, general finitely presented-group undecidability must not be reported as an undecidability theorem for 3-manifold groups. The inspected sources provide no such theorem. Nor does failure of a uniform radius imply undecidability: an input-dependent terminating algorithm could exist without a constant radius.

The L-space formulation in these sources concerns co-orientable taut foliations, and its full equivalence with left-orderability is conjectural in the relevant generality. A foliation on a finite cover does not by itself produce a left order on the base manifold's group. Neither issue is used to justify a theorem in this note. A theorem about every specified foliation is also distinct from a theorem asserting that the manifold admits some foliation.

The original source leaves a marking convention unstated. The first two approaches settle the explicit universal-marking interpretations above. They do not settle an additional formulation with an independently specified geometrically preferred marking, and the effective fixed-marking clause remains unresolved in this work.

## 6. Accounting and review status

Three substantive approaches were used: the Dehn-filling family, the fixed-manifold girth obstruction, and the effective-radius reduction. Source retrieval, the prior-attempt check and integrity packaging are not counted as mathematical approaches. The existing catalog desk assessment was not counted as an earlier proof attempt.

The deliverable contains an authored mathematical deduction and bibliographic metadata, not copied source PDFs, dataset contents, or a computation purporting to solve the remaining algorithmic problem. No executable mathematical checker is included; the proofs are symbolic and rely on the explicitly cited published inputs.

Prepared with extensive AI assistance. This version has not yet received a fresh independent audit, human specialist peer review, or proof-assistant verification. Publication and acceptance require a separate review of this frozen version.
