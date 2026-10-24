# A finite-index obstruction for the two restricted-arrangement groups

2026-10-24. Bounded lemma; no claim of novelty or resolution of 21.128.

Let R_13 be the rank-three restriction of the F4 arrangement to the selected
mirror, and R_31 the analogous H4 restriction. Write G_N for the fundamental
group of the projectivized complement of R_N. Then

    G_13 and G_31 are not abstractly commensurable with F_r x F_s,
    for any finite r,s >= 2.                           (*)

This does not separate G_13 from the central pure H3 group, or establish a
classification of all stable centralizers in Q_F4.

## 1. An elementary rational cohomology criterion

For a group G define R^1(G) to consist of a in H^1(G;Q) for which there exists
b linearly independent from a with a cup b=0; include 0. This is the degree-one
Aomoto resonance set. Suppose H^1(G;Q) contains three linear subspaces W_1,W_2,W_3
of dimension at least two such that

* each W_i is totally isotropic for the cup product;
* for each i != j there are a in W_i and b in W_j with a cup b != 0.

Then G has no finite-index subgroup isomorphic to a product of two nonabelian
finite-rank free groups.

Proof. Restriction to a finite-index subgroup U is injective on rational
cohomology in every degree: the composition with transfer is [G:U] times the
identity. It also preserves products. Therefore each res(W_i) is a linear
subspace contained in R^1(U), and the indicated cross products stay nonzero.
If U=F_r x F_s, Kunneth gives H^1(U)=V_r direct-sum V_s and
H^2(U)=V_r tensor V_s. A direct calculation shows

    R^1(U)=V_r union V_s.

Indeed, for a=x+y with nonzero x,y, the equation a cup (u+v)=0 is
x tensor v=u tensor y and forces u+v to be a scalar multiple of a. If exactly one
of x,y is nonzero, its factor has dimension at least two, giving resonance.
A linear subspace over Q contained in the union of two subspaces is contained
in one of them. Hence each res(W_i) lies entirely in V_r or entirely in V_s.
The nonzero cross products force each pair to lie in different factors. Three
subspaces cannot meet that condition. Contradiction.

If G were merely commensurable with F_r x F_s, a finite-index subgroup of the
latter contains a finite-index product of its intersections with the two
factors. Pulling this product back gives exactly the forbidden U. Thus the
criterion rules out abstract commensurability as well.

## 2. Exact arrangement witnesses

The classifying map of any connected CW complex to its group classifying
space is an isomorphism on H^1(-;Q) and injective from group H^2 into space H^2.
Consequently relations and nonzero values of cup products of degree-one
classes can be checked in the complement itself. This low-degree assertion
also follows from the universal-cover spectral sequence, since the universal
cover has zero H^1. No unproved asphericity assumption is required here.

The Orlik--Solomon cohomology presentation (Orlik--Solomon, Invent. Math. 56
(1980), 167--189, DOI10.1007/BF01392549, Theorem5.2) provides degree-one basis
e_i for the central complement. In the projective complement the degree-one
space identifies with vectors whose coefficient sum is zero. This follows also
from the standard C*-factor splitting: restriction to the global Hopf loop is
the coefficient-sum homomorphism.

For a rank-two flat whose set of incident mirrors is L, define

    W_L = {sum_{i in L} a_i e_i : sum a_i = 0}.

Its dimension is |L|-1. It is totally isotropic: for distinct i,j,k in L the
Orlik--Solomon relation is e_i e_j - e_i e_k + e_j e_k=0, so all products of
vectors e_i-e_j in this sum-zero subspace vanish. The projective pullback on
cohomology is injective, so the same assertion holds in projective cohomology.

The exact certificates provide three different multiple flats L_1,L_2,L_3
containing mirror 0:

* R_13: {0,1,2,3}, {0,4,5,6}, {0,7,8,9}, dimensions 3,3,3;
* R_31: {0,1,2,3,4,5}, {0,7,8}, {0,9,10}, dimensions 5,2,2.

Distinct rank-two flats intersect in at most one mirror. For any i != j choose
p_i in L_i minus {0}, p_j in L_j minus {0}, and let

    a_i=e_0-e_{p_i}, a_j=e_0-e_{p_j}.

Their product is nonzero. Project the degree-two Orlik--Solomon algebra to the
summand indexed by L_i, using basis {e_0 e_l : l in L_i minus {0}}. The coefficient
of e_0 e_{p_i} in a_i a_j is +1. Terms associated with other rank-two flats cannot
alter this coefficient. Thus the three W_L satisfy the criterion, proving (*).

The script resonance_product_obstruction.py constructs integer coordinates for
the zero local cups and the three nonzero cross products. Its output is
resonance_certificate.json. It uses the exact mirror indexing in
restriction_certificate.json, independently checked by verify_incidence.py.
The proof above is not contingent on an experimental rank cutoff.

## 3. Scope

This rules out the known rank-two product profiles as possible groups
commensurable with either projective restriction group. It does not establish
that G_13 or G_31 is strongly indecomposable against all possible product
factors, and does not compare them to G_H3, G_A3 or one another. Those stronger
claims would need additional arguments. Ordinary resonance dimensions and
unmarked local multiplicities remain noninvariants of commensurability in
general; the argument uses rational restriction injectivity and the rigid
resonance shape of a **hypothetical** finite-index product.
