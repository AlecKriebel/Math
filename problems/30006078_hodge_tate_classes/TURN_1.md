# Author turn 1: finite geometric monodromy and unipotent extensions

**Status:** rigorous restricted positive result for every i>=2; the general question remains open in this packet. This is substantive turn **1/5**. No novelty assertion is made for these consequences of standard regulator and Hodge–Tate theory.

## 1. Conventions and statement

Let X be smooth and geometrically connected over a finite extension K/Q_p, and let L be a Hodge–Tate Z_p-local system of finite rank. Put V=L[1/p] and

    W_i(V)=(i−1)! sum_m m ch_{i−1}(gr^m D_HT(V)).

Use the primitive regulator classes fixed in SOURCE_GATE.md. All claims are with rational coefficients; integral torsion is not being computed.

**Theorem.** Suppose there is a finite étale surjection f:Y->X such that, on each connected component of Y (viewed over its field of constants), the rational local system f^*V admits a finite filtration by local subsystems whose successive quotients are pulled back from representations of the Galois group of that field of constants. Then, for every i>=2,

    ell_i(V)=0,     ch_j(gr^m D_HT(V))=0 for every j>0 and every m,

and consequently alpha_X(ell_i(V))=W_i(V)=0.

This applies in particular when the geometric monodromy of V is finite. It also applies if, after a finite étale cover, the geometric monodromy is conjugate into a unipotent upper triangular group. The arithmetic monodromy need not be finite, and the arithmetic quotient representations need not be de Rham.

## 2. Exact-sequence invariance of the odd primitive classes

For any exact sequence of rational p-adic local systems

    0 -> V_1 -> V -> V_2 -> 0,

one has ell_i(V)=ell_i(V_1)+ell_i(V_2). This assertion is about the primitive regulator classes, not arbitrary odd cohomology generators.

Here is a direct verification. Choose a vector-space splitting of the fiber, so the image lies in a block upper triangular subgroup. It is compact. Compatible invariant lattices exist: intersect a stable lattice with the invariant subspace and use the saturated quotient. On its Lie algebra, write a tangent vector as

    A = [ A_1  B ; 0  A_2 ].

For every finite list A^(1),...,A^(q) of such matrices,

    Tr(A^(1)...A^(q))
      = Tr(A_1^(1)...A_1^(q)) + Tr(A_2^(1)...A_2^(q)).             (1)

This follows by multiplying block upper triangular matrices: each diagonal block of a product is the product of the corresponding diagonal blocks. Alternating (1) over q=2i−1 gives exactly the analogous identity for the universal primitive cocycle

    p_i(A^(1),...,A^(2i−1))
      = c_i sum_sigma sgn(sigma) Tr(A^(sigma(1))...A^(sigma(2i−1))),

where c_i is the fixed universal normalization. The Huber–Kings representative has c_i=((i−1)!)^2/(2i−1)!; its exact scalar does not affect this identity.

To transfer the identity to continuous cohomology, restrict the compact image group to a sufficiently small open p-adic analytic subgroup where Lazard comparison with Lie algebra cohomology applies. This comparison is natural for the inclusion and both block projections, so the cohomology-class difference restricts to zero. Restriction to a finite-index subgroup is injective with Q_p coefficients: corestriction followed by restriction in the relevant order gives multiplication by the index on the original cohomology class. Therefore the difference already vanishes on the entire image group. Pullback to the fundamental group and then to X proves additivity. If necessary stabilize all block sizes by trivial summands; the trace identity is unchanged.

The same proof handles any finite invariant filtration. In particular, extension parameters in off-diagonal blocks cannot create one of these primitive classes.

## 3. Arithmetic quotient systems

Let Z be geometrically connected over a finite extension F/Q_p and let V_0 be pulled back from a finite-dimensional continuous Q_p-representation U of G_F. Naturality gives a factorization

    ell_i(V_0) in image[H^{2i−1}(G_F,Q_p) -> H_et^{2i−1}(Z,Q_p)].

For i>=2 the source group is zero, by local p-adic Galois cohomological dimension (the usual continuous finite-dimensional Q_p cohomology vanishes in degrees above two). Hence ell_i(V_0)=0. This is an arithmetic cohomological-dimension argument, not the large-p geometric vanishing theorem in the source.

If V_0 is Hodge–Tate, its associated graded bundle is

    gr^m D_HT(V_0) = O_Z tensor_F D_HT^m(U).

It is therefore trivial of rank dim_F D_HT^m(U). Its positive-degree Chern character is zero. The Hodge–Tate assertion for U can be checked after a finite extension supplied by any closed point of Z, and Hodge–Tate admissibility descends through finite field extensions.

## 4. Passing through a Hodge–Tate filtration

Subobjects and quotients of Hodge–Tate representations are Hodge–Tate, and the Hodge–Tate functor is exact on a short exact sequence all of whose terms are Hodge–Tate. In the relative setting these statements can also be seen from the exact decompleted Higgs functor and its semisimple integral Sen operator: each integral eigensummand is exact; after a finite cyclotomic extension the remaining finite descent is exact in characteristic zero. Petrov's Theorem 2.4, Proposition 3.5, Lemma 3.6 and rigidity Proposition 7.2/Corollary 7.3 provide this relative framework. Equivalently, check the exact sequence on every classical fiber and use the locally free Hodge–Tate bundles and base change.

Thus an invariant filtration of a Hodge–Tate V induces, for every m, a filtration of gr^m D_HT(V) with successive quotients gr^m D_HT(V_a/V_{a−1}). The latter are trivial when V_a/V_{a−1} is arithmetic. Additivity of the Chern character in K_0 gives ch_j(gr^m D_HT(V))=0 for j>0. Section 2 and Section 3 give ell_i(V)=0 for i>=2.

Notice that we are not assuming arbitrary extensions of Hodge–Tate local systems are Hodge–Tate. The full V is Hodge–Tate by the theorem's hypothesis, and only its subquotients are used.

## 5. Finite étale descent

For a finite étale surjection f:Y->X of degree d, pullback is injective on rational étale cohomology and on algebraic de Rham cohomology. On the étale side the trace satisfies Tr_f f^*=d. On the de Rham side, locally

    Omega_Y^q = O_Y tensor_{O_X} Omega_X^q,

and the algebra trace on O_Y defines a map of de Rham complexes to Omega_X^bullet. The equality d Tr(a)=Tr(da) can be checked after an étale splitting of the finite étale algebra, where trace is the sum of the components. This trace also satisfies Tr_f f^*=d. Hypercohomology gives the desired left inverse after division by d. Disconnected covers cause no difficulty; traces sum over their components.

Odd characteristic classes, Hodge–Tate graded bundles and their Chern characters commute with finite étale pullback. Applying the preceding arguments on Y and descending by injectivity proves the theorem. In particular each positive ch_j vanishes separately, a stronger statement than vanishing only of the weighted sum.

For a connected component Y_0, the algebraic closure F of K in its function field is finite over K, and Y_0 is geometrically connected over F. Since Omega_{F/K}=0, using relative de Rham complexes over F or over K on this component makes no difference.

## 6. Two useful geometric-monodromy hypotheses

**Finite geometric image.** Let Gamma=rho(pi_1(X)) and H=rho(pi_1(X_Kbar)), with H finite. Since Gamma is Hausdorff profinite, there is an open subgroup U of Gamma satisfying U intersection H={1}: take a sufficiently small congruence kernel excluding the finitely many nonidentity elements of H. The inverse image of U defines a connected finite étale cover Y. The geometric fundamental group of a component maps into U intersection H and hence acts trivially. The pulled-back representation factors through the Galois group of its field of constants. This supplies a one-step filtration and proves the claimed special case.

**Unipotent geometric image after a cover.** Work on such a component and let N be its geometric fundamental group. If rho(N) is conjugate into a unipotent upper triangular group, its common fixed space is nonzero. Because N is normal in the arithmetic fundamental group, this fixed space is stable under the arithmetic group: n(gv)=g(g^{-1}ng)v=gv. Repeat on the quotient. Each quotient of an upper triangular unipotent representation is again unipotent, so induction constructs a finite arithmetic-invariant filtration on which N acts trivially on successive quotients. The theorem applies. This argument does not require the arithmetic group itself to be simultaneously upper triangular.

## 7. Scope, controls, and remaining obstruction

This proves the target in higher odd degrees for the stated potentially arithmetic-filtered class, in every dimension and for every prime p. It does not compute i=1: arithmetic systems can have nonzero logarithmic determinant and nonzero weighted rank, so the zero argument is inapplicable there. It also leaves genuinely nontrivial semisimple geometric monodromy untouched.

The exact verifier checks the multilinear alternating-trace block identity on bases of small parabolic Lie algebras, the finite-cover trace identity in split models, and graded Chern-character additivity in explicit polynomial models. These are finite consistency controls, not substitutes for the general proofs above and not empirical evidence for the unrestricted conjecture.

**Next mechanism:** study the unweighted Chern character and Tate-twist covariance using the filtered flat bundle A(L) of Petrov Proposition 5.1, then test whether this removes or merely restates the lost-information obstruction in the source's cup-product calculation.
