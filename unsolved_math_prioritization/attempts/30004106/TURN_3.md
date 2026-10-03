# Turn 3: elementary-abelian growth detection does not detect all spectra

**Original unresolved, 3/5 substantive author turns.** The route tested here is to upgrade the credited elementary-abelian detection of gamma for actual modules to a spectral statement for all virtual or complex elements. That upgrade fails, even for an explicit finite self-adjoint element over Q8. The example is a counterexample to this proposed proof shortcut, not to the original symmetry question.

## 1. The precise obstruction

Let k be any field of characteristic two, G=Q8, P=kG, and let Omega^j k denote the projective-free syzygies of k. In the full complexified split Green ring set

    x=[Omega k]+[Omega^3 k]−2[k]−(3/2)[P].                (1)

Then x=x*, and

    restriction_E(x)=0
      for every elementary abelian 2-subgroup E of G,
    spectrum_(A_G)(x)={0,−2,−4}.                         (2)

In particular rho(x)=4. No bound on rho(x), or on its norm, by a constant times the maximum of the corresponding restricted quantities can hold for all complex/virtual elements, even when restricted to self-adjoint finite-support elements.

This does not contradict Benson's Theorem4.4.4: that theorem concerns gamma_G(M)=max_E gamma_E(M) for **actual modules** M and their positive tensor powers. Element (1) has negative rational coefficients. Its spectrum is entirely real, and it belongs to the symmetric endotrivial/projective subalgebra of turn 2. It supplies no failure of Banach *-symmetry.

## 2. A credited periodic resolution, with an exact finite certificate

Use the presentation

    G=<a,b : a^4=1, b^2=a^2, ba=a^{-1}b>,

and put K=ab, K'=a^3b, N=sum_(g in G) g. The following right-kG free resolution is the one displayed in Langer, arXiv:0803.0252v1, Proposition2.2, p5. Its four maps are

    d1=(a+1, b+1),
    d2=((b+1, K'+1),(K+1, a+1)),
    d3=(a+1, b+1)^T,
    d4=(N),

with free ranks 1,2,2,1 in degrees0,1,2,3 and period four thereafter. Matrices act by left multiplication on column vectors, hence are right-module maps. Right modules and the original left-module convention are related by g acting through g^{-1}; this equivalence preserves tensor product, duality, projectivity and the trivial module.

Here is a direct check of the resolution, so the omitted elementary verification in that source is not a gap in its use. Multiplication in G is

    (a^i b^j)(a^k b^l)=a^(i+(-1)^j k+2jl) b^(j+l mod2).

It gives d1d2=d2d3=d3d4=d4d1=0 in characteristic two. In the ordered group basis

    1,a,a²,a³,b,ab,a²b,a³b,

expand the maps as ordinary matrices over F2. Their ranks are respectively

    rank d1=7, rank d2=9, rank d3=7, rank d4=1.           (3)

A fully explicit lower-rank certificate is given by the following zero-based row/column sets; each indicated square minor has determinant1 in F2:

- d1 rows (0,1,2,3,4,5,6), columns (0,1,2,4,5,6,8)
- d2 rows (0,1,2,3,4,5,6,8,9), columns (0,1,2,3,4,5,6,8,9)
- d3 rows (0,1,2,4,5,6,8), columns (0,1,2,3,4,5,6)
- d4 row (0), column (0)

The checker constructs these matrices directly from the multiplication formula and verifies the minors exactly. For the upper bounds, d1 lands in the seven-dimensional augmentation ideal, d3 kills N, d4 has the one-dimensional norm image, and d1d2=0 forces rank d2<=16−7=9. Thus (3) is certified without a numerical rank tolerance.

Dimension comparisons and the zero composites prove exactness in each of the four repeating positions and at the augmentation. Every matrix entry has augmentation zero, so the resolution is minimal over the local algebra kG. The F2 calculations remain valid over every characteristic-two extension field, since the nonzero minors equal1 and all zero-composite identities are integral modulo2.

## 3. The exact stable order of Omega k

The consecutive syzygy dimensions from (3) are

    dim k=1, dim Omega k=7,
    dim Omega²k=9, dim Omega³k=7, dim Omega⁴k=1.          (4)

The last module is the norm image kN, on which G acts trivially, so Omega⁴k is isomorphic to k.

No minimal syzygy here has a projective summand. Indeed kG is self-injective (the coefficient-of-identity form makes it a symmetric finite-dimensional algebra). A projective summand of the kernel of a projective cover would be injective and split off from the covering projective, while being contained in its radical. A nonzero direct summand cannot lie in that radical, by Nakayama's lemma.

The stable tensor identity

    core(Omega^i k tensor Omega^j k)=Omega^(i+j) k

follows by tensoring projective presentations and applying Schanuel's lemma; tensoring a projective with any module is projective. Duality gives (Omega^i k)*=Omega^(-i)k after taking cores. Equivalently, Omega k is the standard endotrivial stable generator.

Its stable order divides4 by (4). It is not1 because its projective-free representative has dimension7, and not2 because Omega²k is projective-free of dimension9 rather than1. Hence its exact stable order is4. The four core representatives are pairwise distinct. In particular Omega³k is the dual of Omega k, and (1) is self-adjoint.

## 4. Compute the spectrum inside the actual completion

Let u be the image of Omega k in the stable completed ring A_st. Its four powers are distinct nonprojective basis elements, so their span is an injected copy of

    C[u]/(u^4−1) ≅ C^4.

Put h=u+u^{-1}−2. Its values at u=1,i,−1,−i are 0,−2,−4,−2.

These values are its spectrum in the whole stable completion, not merely in the finite subalgebra. To verify this directly, use the Fourier idempotents

    e_zeta=(1/4)sum_(j=0)^3 zeta^{-j}u^j,  zeta^4=1.

They are nonzero because the four powers are linearly independent. For each displayed value lambda, (h−lambda)e_zeta=0 for a suitable nonzero idempotent, so h−lambda cannot be invertible in any containing unital algebra. Conversely, for lambda outside the displayed set, a polynomial inverse is obtained by summing (h(zeta)−lambda)^{-1}e_zeta. Thus

    spectrum_(A_st)(h)={0,−2,−4}.                         (5)

For Q8 the idempotent of turn2 is e=P/8. The canonical nonprojective representative of h has dimension 7+7−2=12. Its lift J(h)=h−12e is exactly (1). Under the full/stable product splitting, x has scalar component zero and stable component h. The spectrum is the union of the two factor spectra, giving (2). This also checks why the coefficient 3/2 is essential.

## 5. Restriction really vanishes as a split-ring element

The unique element of order two in Q8 is a². Therefore its only nontrivial elementary abelian 2-subgroup is E=<a²>≅C2.

Restrict a projective presentation to E. Projectives stay projective, and Schanuel's lemma gives

    Res_E(Omega_G^j k) is stably Omega_E^j k.

In characteristic two, the nonprojective syzygy of the trivial C2-module is again k. The only indecomposables for kC2 are k and kE. Since both Omega_G k and Omega_G³k have dimension7, their actual restrictions are

    k ⊕ 3 kE.

Also Res_E(P)=4kE. Consequently (1) restricts to

    (k+3kE)+(k+3kE)−2k−(3/2)(4kE)=0

in the full complexified split ring, before completion. Restriction to the trivial subgroup is zero because dim(x)=0. This proves every vanishing in (2).

## 6. Consequence for the research route

The positive core-dimension comparison in Benson Theorem4.4.2 cannot be extended to all signed/complex Green-ring elements merely by linearity. Restriction can cancel genuinely nonzero spectral directions; even its kernel can contain a self-adjoint element of spectral radius4.

Likewise, the positive gamma detection theorem does not establish that the full or stable completed restriction map is spectrally faithful. Any reduction of the original symmetry question through elementary abelian subgroups needs an additional argument controlling the invisible directions. This example shows that they need not be radical or quasinilpotent.

It remains possible that those directions are all Hermitian, as they are here. The result therefore closes a tempting invalid proof route while leaving the source question unresolved at3/5.
