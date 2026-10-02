# Author turn 3: exact kernels of the fixed cup-product test

**Substantive turn 3/5.** This turn tries to recover the source formula from its known pro-étale Chern-class product identity and proves that the proposed cancellation mechanism fails in explicit good-reduction examples. These are **not counterexamples to the original local-system question**.

Throughout i>=2 and kappa_i is the restriction to G_K of the class in the OWR report: the Bloch–Kato exponential of (−1)^i over Q_p. Write

    C_{X,i}:H_et^{2i−1}(X,Q_p) -> H_et^{2i}(X,Q_p(i)),
              a |-> a cup kappa_i.

The source identity c_i(L tensor O_hat)=C_{X,i}(ell_i(L)) cannot determine alpha_X(ell_i(L)) unless this test is injective on the relevant classes, or additional information selects them.

## 1. Projective-space example over every finite extension

**Theorem A.** Let K/Q_p have degree e and X=P_K^{i−1}. Then C_{X,i} has rank one and kernel dimension e−1 over Q_p. The source's alpha_X is an isomorphism from its domain to the one-dimensional K-vector space H_dR^{2i−2}(X/K).

**Proof.** Set d=i−1>=1. The projective-bundle decomposition, compatible with Galois action and cup products, gives

    H_et^{2d+1}(P_K^d,Q_p) = H^1(G_K,Q_p(−d)),
    H_et^{2d+2}(P_K^d,Q_p(d+1)) = H^2(G_K,Q_p(1)).               (1)

All other projective-bundle summands vanish in these degrees because G_K has p-cohomological dimension two. By local Tate duality and the Euler characteristic formula,

    dim_Qp H^1(G_K,Q_p(−d))=e,
    H^2(G_K,Q_p(1)) ~= Q_p.

The first equality also appears in Bloch–Kato, Example 3.9, for negative twists. Under (1), the map C_{X,i} is the perfect local Tate pairing with the fixed vector kappa_i in H^1(G_K,Q_p(i)).

This vector is nonzero. For i>=2, the exponential K->H^1(G_K,Q_p(i)) is an isomorphism: Bloch–Kato, Corollary 3.8.4, Example 3.9 and Definition 3.10; its kernel is D_cris(Q_p(i))^{phi=1}/H^0(G_K,Q_p(i))=0. Equivalently restriction from Q_p is injective by restriction/corestriction and kappa_i over Q_p is already nonzero. Thus perfect duality makes C_{X,i} a nonzero linear functional. Its rank is one and its kernel dimension is e−1.

Projective space has good reduction. The alpha-isomorphism stated in the source applies (n=2i−1>1); it can also be read from the negative-Tate-twist calculation H_g^1(G_K,Q_p(−d))=0 in Bloch–Kato Example 3.9. Therefore every nonzero member of this kernel has nonzero alpha-image. □

In particular, over any nontrivial finite extension K/Q_p the fixed product test fails to determine the desired K-valued answer even in top degree. This does not contradict OWR Theorem 1, whose base field is Q_p. It does not show the formula fails on projective space: its geometric fundamental group is trivial, so turn 1 already proves the higher-degree formula there.

## 2. A two-dimensional kernel over Q_5 itself

The loss of information is not solely a restriction-of-scalars phenomenon.

Let E/Q_5 be the elliptic curve

    y^2=x^3−x,

and X=E×E. Its discriminant is 64, a 5-adic unit, so E and X have good reduction. By Hensel's lemma Q_5 contains an element u with u^2=−1 (lift either root modulo 5). The automorphism

    j(x,y)=(−x,u y)

has order four and j^2=[−1].

**Theorem B.** For this X and i=2, C_{X,2}:H_et^3(X,Q_5)->H_et^4(X,Q_5(2)) has rank four and kernel dimension two. Alpha_X is injective, indeed an isomorphism onto H_dR^2(X/Q_5), of dimension six.

**Proof.** Put M=H_et^2(X_Q5bar,Q_5). The Künneth formula gives dim M=6. The four divisors

    H=E×{0}, V={0}×E, D=diagonal, J=graph(j)

are defined over Q_5. Their intersection matrix in that order is

    [0 1 1 1]
    [1 0 1 1]
    [1 1 0 2]
    [1 1 2 0].                                                   (2)

Each self-intersection is zero by adjunction or translation of an elliptic subgroup. Intersections with H and V are one. D intersection J is the kernel of j−1, which consists of 0 and (0,0); it has degree two in characteristic zero. Thus (2) follows directly. Its determinant is −4, so these cycle classes span a nondegenerate four-dimensional Galois-stable subspace

    S ~= Q_5(−1)^4 inside M.

Poincaré duality makes the orthogonal complement T a Galois-stable direct summand, so M=S direct sum T, with dim T=2. The Hodge–Tate weights of M, in cohomological grading, are 0,1,2 with multiplicities 1,4,1. The entire middle-weight part is supplied by S. Thus T has weights 0 and 2, once each.

We spell out the two spectral-sequence identifications to prevent a hidden differential from spoiling the calculation. For a good-reduction smooth proper variety, crystalline Frobenius on geometric cohomology of positive degree has the corresponding positive Weil weight, so there are no Galois invariants in H^a(X_bar,Q_5) for a>0. In particular H^0(G_Q5,H^3)=0. Also

    H^2(G_Q5,H^1(X_bar,Q_5))=0

by local duality, since its dual invariant space is H^0(G_Q5,H^1(X_bar,Q_5)^*(1)); its Hodge–Tate weights are strictly negative. The Hochschild–Serre sequence therefore identifies

    H_et^3(X,Q_5) = H^1(G_Q5,M).                                (3)

For the target, the filtration-two subspace is

    F^2 H_et^4(X,Q_5(2)) = H^2(G_Q5,M(2)).                       (4)

The only possible incoming differential would come from H^0(G_Q5,H^3(X_bar,Q_5(2))), which is zero by good-reduction purity (Weil weight 3−4=−1). There are no higher Galois cohomology columns. The product by the base-field class kappa_2 takes (3) into (4) and is precisely the local cup product on those identifications.

On S=Q_5(−1)^4, each one-dimensional H^1(G_Q5,Q_5(−1)) pairs nontrivially with kappa_2 by perfect local duality and the nonzero exponential argument above. Thus the S contribution has rank four.

On T,

    H^2(G_Q5,T(2)) = H^0(G_Q5,T^*(−1))^* = 0,

because the two weights of T^*(−1) are 1 and −1 and neither is zero. Therefore this entire contribution is killed. Moreover H^0(G_Q5,T)=0 by purity and H^2(G_Q5,T)=0 because T^*(1) has weights −1 and −3. The local Euler characteristic formula gives dim H^1(G_Q5,T)=2. Equations (3)–(4) now show rank four and kernel dimension two, with no additional source summand. Finally X has good reduction, so the alpha statement follows as in Theorem A. □

The cycle matrix proves the needed four-dimensional Tate summand directly. No Tate conjecture, Picard-rank guess, classification of endomorphisms, or numerical approximation to a Galois cohomology group is used. The point count #E(F_5)=8 is included as a check, not required for the argument.

## 3. What survives of the attempted recovery mechanism

Theorem B identifies two genuine directions in arithmetic cohomology whose alpha-images survive but whose product with the one fixed kappa_2 is zero. It does **not** produce L with ell_2(L) in those directions. Establishing that all characteristic classes avoid the invisible directions would itself be a substantial theorem about the image of the regulator; it cannot be deduced from the product identity alone.

For Theorem A, allowing all pairings with exp_K(a), a in K, would recover a class by perfect duality, whereas the source supplies the single class arising from a fixed rational scalar. No construction in this packet provides corresponding independent Chern-class identities for all those a. Field extension alone merely repeats the restricted fixed-vector pairing and does not prove such a family.

The result of this author turn is therefore an **exact failure certificate for an attempted proof method**, with concrete source-compatible X and coefficients, not a negative answer. The route “compute the pro-étale Chern classes and cancel kappa_i” is closed unless a new injectivity-on-the-regulator-image theorem or genuinely additional pairings are supplied.

## 4. Dependencies and checks

The primary additional input is Bloch–Kato, *L-functions and Tamagawa numbers of motives*, Proposition 3.8, Corollary 3.8.4, Example 3.9 and Definition 3.10, [primary scan](https://virtualmath1.stanford.edu/~conrad/BSDseminar/refs/BKTamagawa.pdf). The proof of Proposition 3.8 explicitly uses local duality and the local Euler characteristic formula. Standard projective-bundle, Künneth, Poincaré-duality and good-reduction comparison/purity theorems are used with the indicated twists; none is claimed as a new result.

The verifier checks the elliptic discriminant and automorphism identities, the intersection matrix and inverse, exact point count, Hodge-weight subtraction and dual twists, and the dimensions of the stated model cup maps. Its cohomological matrices encode the proven decompositions; they are not independently computed p-adic cochains.
