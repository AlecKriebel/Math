# A published negative answer to Kapovich's equivariant EZ-boundary question

## 1. Claim and result

The target asks whether, for every word-hyperbolic group Gamma and every EZ-structure (Ybar,B) on that group, B is Gamma-equivariantly homeomorphic to the group's Gromov boundary. The EZ-structure is understood in the finite-dimensional sense immediately preceding Problem 25 in Kapovich's problem list: compact Euclidean retract, negligible Z-set remainder, free cocompact covering action on the complement, nullity of translated compact subsets, and extension of the action to the compactification.

The answer is **no**, as a consequence of Guilbault--Healy--Pietsch [GHP], Theorem 1.6 and the explicit boundary action in Section 7.1. This is an application of existing published results, not a proposed new theorem.

More precisely, take a closed orientable surface S of genus at least two and a homeomorphism in a pseudo-Anosov mapping class. Put H=pi_1(S), and let phi be an induced automorphism. Choose the stable-letter convention

    Gamma = < H,t | t^{-1} g t = phi(g), g in H >.

Changing to the inverse monodromy if necessary reconciles this convention with the geometric mapping torus. Both choices are pseudo-Anosov and have hyperbolic mapping tori.

Then Gamma has an EZ-boundary B homeomorphic to S^2 on which Gamma fixes two points. Its Gromov boundary is also S^2 but has no Gamma-fixed point. Consequently there is not even a Gamma-equivariant map B -> boundary(Gamma), and in particular there is no equivariant homeomorphism.

## 2. Why the group is an admissible hyperbolic group

Pseudo-Anosov mapping classes exist on closed orientable surfaces of genus at least two. By Thurston's mapping-torus hyperbolization theorem [Thu, Theorem 0.1, Proposition 2.6, and Section 5], the mapping torus M is a closed hyperbolic 3-manifold. Its fundamental group is the above surface-by-infinite-cyclic group Gamma. Deck transformations give a free, proper, cocompact isometric action on H^3. The orbit-map quasi-isometry therefore proves that Gamma is word-hyperbolic and identifies its Gromov boundary equivariantly with the visual sphere S^2 of H^3.

Gamma is non-elementary: it contains the closed surface subgroup H, which is not virtually cyclic. The canonical boundary action is minimal and the boundary has more than one point, so it has no global fixed point. For this particular Kleinian realization, minimality on the sphere at infinity is also stated explicitly in [Thu, page 3]. For the general hyperbolic-group statement see [KB, Proposition 4.2(2)].

Only a closed surface is used here. A punctured-surface mapping torus typically has cusps and is only relatively hyperbolic; substituting such an example would not verify this target.

## 3. The published EZ-structure and its action

The group H is hyperbolic, and its canonical boundary is a circle C. [GHP, Theorem 1.6, journal page 871] applies to every automorphism of H and supplies an EZ-boundary

    B = suspension(C).

The suspension may be written as (C x [-1,1]) with all points of C x {1} identified to a point P_+ and all points of C x {-1} identified to a different point P_-. Its underlying topology is S^2.

The action is essential: a bare statement that B is a sphere is insufficient. In [GHP, Section 7.1, journal page 898], each element g of H acts by the suspension of its action on C; the stable letter acts by the suspension of the boundary map induced by a phi^{-1}-variant map. Thus, writing q for the suspension quotient map and h_C for that boundary homeomorphism, the formulas are

    g q(z,r) = q(gz,r),
    t q(z,r) = q(h_C(z),r).

Every generator and its inverse preserves the height coordinate and fixes P_+ and P_-. Hence every word in those generators fixes both points. The relation t^{-1}gt=phi(g) holds because h_C^{-1} g h_C=phi(g) on C. Section 7 proves continuity of the extended action, including at the poles; it is not merely a proposed action on an unattached abstract boundary.

This proves B^Gamma contains {P_+,P_-}. In fact equality holds: H's action on its canonical circle is minimal and has no global fixed point, so no non-pole suspension point is fixed by all of H.

## 4. Matching the original Euclidean-retract definition

[GHP] formulates Z-structures using compact metric absolute retracts, which may in general be infinite-dimensional. It is therefore necessary to check the stronger finite-dimensional requirement of Kapovich's list rather than silently identify the two definitions.

Here that check is straightforward from the construction.

1. Choose a finite 2-dimensional CW model K=S for H. The torsion-free construction in [GHP, Section 3.2, journal pages 876--878] uses a cellular homotopy equivalence f':K->K inducing phi, a lift f:X->X to the universal cover X, and the bi-infinite mapping telescope Y=Tel_f(X). The space X is a locally finite 2-complex; Y is a locally finite 3-complex. It is the universal cover of the finite mapping torus of f'. Hence Gamma acts freely by covering transformations and Y/Gamma is compact.

2. The lifts implementing phi and phi^{-1} are continuous coarse equivalences, indeed quasi-isometries with respect to the cocompact path metrics. Their extensions to the hyperbolic circle meet [GHP, Theorem 7.1]. Theorems 1.1 and 7.1, together with the construction in Sections 4--5, produce a compact metric AR Ybar=Y disjoint-union B, with B a Z-set, the required nullity condition, and a continuous Gamma-action extending that on Y.

3. The compactification is finite-dimensional. Exhaust the locally finite 3-complex Y by compact subsets K_n of covering dimension at most 3. Each K_n is closed in the Hausdorff compactification. The remainder B is closed and has covering dimension 2. The countable closed-sum theorem for covering dimension in metric spaces, applied to

       Ybar = B union K_1 union K_2 union ...,

   gives dim(Ybar)<=3.

4. A finite-dimensional compact metric AR is a Euclidean retract: embed it as a closed subset of some R^N using the finite-dimensional metrizable embedding theorem and apply the defining absolute-retract property. Thus Ybar meets exactly the Euclidean-retract hypothesis from the problem list.

The original homotopically negligible description of a Z-set agrees, in this compact metric AR setting, with the instantaneous-pushing homotopy definition used in [GHP]. This standard equivalence is discussed in [GM, Section 3]. No torsion variant, weak Z-structure without nullity, or infinite-dimensional relaxation is needed.

## 5. The obstruction is equivariant, not a topological mismatch

Suppose F:B->boundary(Gamma) were Gamma-equivariant. For every gamma in Gamma,

    gamma F(P_+) = F(gamma P_+) = F(P_+).

Then F(P_+) would be a global fixed point of the canonical boundary action, contradicting Section 2. This argument does not need continuity or injectivity of F.

The underlying spaces B and boundary(Gamma) are both S^2. In particular, this example refutes the equivariant uniqueness asked in Problem 25; it does not refute ordinary homeomorphism for this group. It makes no conformal, quasisymmetric, or quasiconformal identification. The constructed action need not be a uniform convergence action. Bowditch's characterization is therefore compatible with this example.

## 6. Attribution, closure, and limits

Classification: **already_solved, negative**, by a direct consequence of the published GHP construction. [GHP] was published online on 10 November 2023 and appeared in Groups, Geometry, and Dynamics 18 (2024), 869--919. The claim here is not that GHP explicitly named Kapovich's numbered problem, or that this note establishes the earliest date of the negative answer. It establishes that a publicly available published theorem already supplies a counterexample under all the original hypotheses.

No additional proof search is required after this complete prior-resolution route. A separate audit should check the theorem application, the action formulas, and especially the finite-dimensional/covering-action bridge. Executable controls are limited sanity checks of suspension algebra, quotient poles, and conjugacy invariants; they are not machine verification of Thurston hyperbolization, the GHP compactification, or the topological dimension theorems.

## References

[GHP] C. R. Guilbault, B. B. Healy, B. Pietsch, *Group boundaries for semidirect products with Z*, Groups Geom. Dyn. 18 (2024), 869--919. Theorem 1.6 (p. 871), Definition 2.6 (p. 874), Section 3.2, Theorem 7.1 (p. 897), Section 7.1 (p. 898), Section 7.5 (p. 905). https://doi.org/10.4171/GGD/750 . Published PDF: https://ems.press/content/serial-article-files/47884?nt=1

[Thu] W. P. Thurston, *Hyperbolic structures on 3-manifolds, II: Surface groups and 3-manifolds which fiber over the circle*, 1986 preprint / 1998 eprint, Theorem 0.1, Proposition 2.6, Section 5; page 3 for minimality. https://arxiv.org/abs/math/9801045

[KB] I. Kapovich and N. Benakli, *Boundaries of hyperbolic groups*, Proposition 4.2(2). https://arxiv.org/abs/math/0202286

[GM] C. R. Guilbault and M. A. Moran, *Proper homotopy types and Z-boundaries of spaces admitting geometric group actions*, Expo. Math. 37 (2019), 292--313. https://doi.org/10.1016/j.exmath.2018.03.004 ; https://arxiv.org/abs/1707.07760

[Kap] M. Kapovich, *Problems on Boundaries of Groups and Kleinian Groups*, Problem 25 and preceding definitions, PDF page 8. https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf
