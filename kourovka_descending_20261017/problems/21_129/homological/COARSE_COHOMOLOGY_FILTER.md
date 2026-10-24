# Compact-support/coarse cohomology cannot separate the four pairs

**Claim being checked.** Let Q_T=P_T/Z(P_T) for one of the eight residual irreducible spherical types, and let d=rank(T)−1. For a contractible cocompact free Q_T-complex E_T of finite type,

\[
H_c^j(E_T;\mathbb Z)\cong
\begin{cases}
\bigoplus_{\mathbb N}\mathbb Z,&j=d,\\
0,&j\ne d.
\end{cases}
\tag{1}
\]

The isomorphism here is only one of abelian groups. The compact-support cup product is identically zero. Therefore the resulting graded rings agree within every residual pair. No isomorphism of dualizing modules as modules over group rings is claimed.

This is a failure filter for one coarse invariant, not a solution and not a novelty claim for the arrangement-cohomology theorem.

## Proof from the inspected spectral sequence

The affine decone X_T is an aspherical arrangement complement of rank d, with π1(X_T)=Q_T. The model and center identifications are the ones recorded in `SPECTRAL_FILTER.md`; their Artin-group inputs belong to the reviewed reduction.

Use [Davis–Januszkiewicz–Leary–Okun, Theorem 1](https://arxiv.org/pdf/1002.3129v2), published in IMRN 2011(9), 2110–2116, together with [Davis, *Complements of hyperplane arrangements as posets of spaces*, Theorem 3.14 and its repaired proof](https://people.math.osu.edu/davis.12/papers/DavisHyper.pdf), pp.12–13. These give

\[
H^j(X_T;\mathbb ZQ_T)=0\quad(j\ne d),
\qquad H^d(X_T;\mathbb ZQ_T)\text{ free abelian}.
\tag{2}
\]

For clarity, infinite rank in this particular application is not inferred from the word “usually” in the statement of that theorem. It follows from a specific term of the proof. For each flat G, write r_G=codim(G), r^G=d−r_G. The displayed spectral-sequence terms (3.3) in that proof can be nonzero only in bidegree (r^G,r_G), hence only in total degree d. The spectral sequence collapses: any differential changes total degree by 1 and has zero target/source away from that diagonal.

For the ambient flat G=V=C^d, r_G=0, and the associated local space M_G is contractible. Thus its local coefficient group is H^0(M_G;ZQ_T)=ZQ_T. The term (3.3) for this G is

\[
H^d(L(\mathcal A)_{\ge V},L(\mathcal A)_{>V};\mathbb Z)
  \otimes_{\mathbb Z}\mathbb ZQ_T
 \cong (\mathbb ZQ_T)^{\beta(\mathcal A)}.
\tag{3}
\]

Here β(𝒜)=c_T>0, as in (1)–(2) of `SPECTRAL_FILTER.md`. The identification of the relative-poset cohomology with this beta invariant is explicitly used in Davis's proof of Theorem 3.13, immediately before Theorem 3.14. DJLO Remark 6 also explicitly identifies this ambient-flat free group-ring term of rank β(𝒜) in the associated graded module. The source's term “rank” there refers to rank over Zπ; its underlying abelian rank is infinite.

Consequently the associated graded group of H^d(X_T;ZQ_T) has a subquotient isomorphic to (ZQ_T)^{c_T}. Since Q_T is countably infinite, this subquotient has countably infinite abelian rank. It follows that H^d(X_T;ZQ_T) has infinite abelian rank. It has at most countable rank because X_T has a finite CW model and Q_T is countable. Combining this with freeness from (2) proves it is the free abelian group of rank ℵ0.

For a finite K(Q_T,1), equivariant cellular cochains with group-ring coefficients identify with compactly supported cochains on its locally finite universal cover. This identifies (2) with (1). Finally d≥3 in the four residual pairs, so any product of two possibly nonzero compact-support classes would have degree 2d>d and is zero; there are no degree-zero classes. This proves the ring assertion. ∎

## Why this is the relevant coarse failure

Contractible universal covers of finite classifying complexes admit uniformly contractible bounded-geometry models. A quasi-isometry between such models gives mutually inverse controlled chain maps and controlled chain homotopies, hence isomorphisms of compact-support/coarse cohomology. The point of the argument above is that even this stronger topological invariant has identical values within the pairs. The failed filter does not rely on ordinary Betti numbers of the finite quotient being quasi-isometry invariant.

The action of Q_T on H_c^d(E_T;Z), its dualizing module, can carry additional information. A bare quasi-isometry does not come with an isomorphism Q_T→Q_U making its induced compact-support map equivariant. Requiring such equivariance without a new rigidity theorem transfers the original difficulty into an unsupported stronger hypothesis. That route is blocked in its current form.

## Source wording excluded from the proof

Davis's 2015 proof includes an apparent local-rank error: it describes H^j(M(A_G);Zπ_G) as free abelian of rank β′(A_G). Read as finite abelian rank, that phrase cannot be literal. A central three-line arrangement has complement C*×(C minus two points), so its top group-ring cohomology is H^1(F2;ZF2)⊗H^1(Z;ZZ), of infinite abelian rank. The argument above imports only freeness and degree concentration, not that local-rank phrase. The original DJLO Theorem 1 supplies precisely the two needed properties, and its Remark 6 distinguishes free group-ring rank from abelian rank. No correction of the published theorem is being proposed here; the suspect sentence is an unused proof-level phrase in the 2015 repair manuscript.

**Exact remaining gap:** distinguish the proper homotopy or coarse structure beyond these groups/rings, or recover a canonical pattern/module action through a verified large-scale construction. Equation (1) alone provides no separation.
