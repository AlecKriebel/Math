# Independent algebraic proof reconstruction

Checkpoint 2026-10-12 21:51 UTC. This reconstruction was written after reading the frozen candidate, README and source gate, but before historical audit/contributor conclusions or current peer conclusions. It verifies the existing candidate; it does not pursue a new candidate. Completion estimate: 70% of assigned algebraic verification, pending complete historical-file inspection and source-receipt reconciliation.

## Exact mathematical target

For A=Z_(2)G and B=F_2G, the condition is that every indecomposable projective B-module class belongs to the ordinary G_0(B) image of the nonnegative monoid of QG-modules. Since QG is semisimple, this monoid is the nonnegative integral span of simple QG-modules. Since every finite-dimensional projective B-module decomposes into PIMs, giving a witness for every PIM is equivalent to the full positive-projective inclusion in Johnston--Rumynin Conjecture 9. Neither a module isomorphism nor a split Grothendieck equality is required.

I read arXiv:2507.21316v2, full relevant printed pages 3--5 and 9--11, including Conjecture 9, Proposition 1.4 and its proof, Proposition 3.3 and its proof, and Example 3.4/Tables 1, 2 and 5. The exact target was also read on printed p186 of the editors' October 6 replacement notebook PDF. The original frozen notebook URL now returns 404. The replacement retains the target but adds a starred negative answer and earlier-source reference; that source-status discrepancy is separate from the algebraic proof and requires root handling. I have not read the cited earlier solution or audited priority.

## Central quotient and exact doubling

Let z be a central involution, t=z-1, k=F_2, H=G/<z>, C=kG and D=kH. The basis pairs {g,zg} give ker(t:C→C)=im(t:C→C)=tC and t²=0. On a finite free module C^n the same identity holds componentwise. Write C^n=P⊕P' with both summands C-stable. The operator t preserves both summands and therefore ker(t|P)=tP. Consequently multiplication by t induces an isomorphism P/tP→tP. This is C-linear because t is central, and both sides have t acting as zero. Thus

0 → Inf(tP) → P → Inf(P/tP) → 0

is an actual exact sequence (the inflation notation only emphasizes the quotient action), and [P]=2[Inf(P/tP)] in ordinary G_0(C). The quotient functor is not asserted to be exact on arbitrary modules.

Every simple C-module is killed by t: its t-annihilator is a nonzero submodule because t²=0, hence the whole simple module. Thus C and D have the same simple types. If P is projective, D⊗_C P=P/tP is projective over D. The ideal tC is nilpotent and hence is contained in J(C); quotienting does not change the simple top. A PIM over a finite-dimensional algebra is its simple top's projective cover. Therefore quotienting carries PIMs to the corresponding PIMs of D and gives a bijection on types. This establishes the exact doubling for every type without an absolute-splitting assumption.

## Base-field completeness and witnesses

The independently read Example 3.4 is explicitly over F_2 and supplies simple types 1,U,S with dimensions 1,4,4, reductions d(V1)=1, d(V5)=1+U, d(V4)=S, and quotient PIM classes 4·1+2·U, 4·1+3·U, S. In particular, U denotes the entire nonsplit F_2 simple, not one degree-two absolutely simple constituent. The block regular multiplicity is 2 for U, consistent with dim_(F_4) U=2 and End(U)=F_4; the source's regular decomposition is P(1)⊕P(U)^2⊕S^4.

Applying the central lemma for SL(2,5)/<−I>=A5 gives three classes:

| Simple top | PIM class over F_2G | Witness in QG | Rank |
|---|---|---|---|
| 1 | 8·1+4·U | 4V1+4V5 | 24 |
| U | 8·1+6·U | 2V1+6V5 | 32 |
| S | 2S | 2V4 | 8 |

Inflation preserves simplicity over Q because every inflated submodule is an H-submodule. A lattice for an H-module remains a lattice after inflation, so its decomposition class also inflates. All coefficients are nonnegative integers. The regular dimension reconstruction is 24+2·32+4·8=120. This establishes the stated positive condition, conditional only on the independently verified source modular data (also assigned to a distinct computation family by root).

## The obstructed PIM

The five-point augmentation lattice for A5 has ordinary character χ+ with values 4,0,1,−1 on quotient orders 1,2,3,5. Its F_2 augmentation module S has dimension four. On a Sylow V4 fixing the fifth point, the projection onto the other four coordinates is an equivariant isomorphism from the augmentation module to the four-point regular module. Restriction to the Sylow is free, hence S is projective by the finite-group Sylow criterion. The candidate's matrix-span check is a valid sufficient test for absolute simplicity: spanning M4(F_2) implies, after any field extension, the full matrix algebra still acts. Consequently P_H(S)=S. The central lemma makes E=P_G(S) eight-dimensional with [E]=2S, so its Brauer character on every odd-order element is twice χ+.

The binary icosahedral SU(2) construction provides an actual two-dimensional complex representation of G. Chung--Kostant--Sternberg printed pages 3--5 and 14--16 were read completely: they identify the central double cover with SL(2,5), explain homogeneous-polynomial representations, and display the degree-four symmetric-cube row. With x the natural trace, χ−=x³−2x. Its values, together with χ+, are:

| Order | 1 | 2 | 3 | 4 | 5 | 6 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Count | 1 | 1 | 20 | 30 | 24 | 20 | 24 |
| χ+ | 4 | 4 | 1 | 0 | −1 | 1 | −1 |
| χ− | 4 | −4 | 1 | 0 | −1 | −1 | 1 |

Both order-five classes (and both order-ten classes) have the same row values, so aggregating them is legitimate here. The norm numerator for χ− is 16+16+20+24+20+24=120. As it is an actual character, norm one establishes complex irreducibility. Squaring takes order columns to 1,1,3,2,5,3,5; the indicator numerator is 4+4+20−120−24+20−24=−120. Thus ν(χ−)=−1.

There is also a direct check of the parity hypothesis in this particular construction: the natural SU(2) module has a commuting antilinear map J(v1,v2)=(−conj(v2),conj(v1)), with J²=−1. Its symmetric cube has the induced antilinear map with square (−1)^3=−1. For an irreducible V of this type, the conjugation on V⊗C^m inside a real representation has form J⊗K, with K antilinear and K²=−1. Writing K=B·conjugation gives B·conj(B)=−I_m. Taking determinants yields |det(B)|²=(−1)^m, so m must be even. This is the standard quaternionic parity restriction, with all its field hypotheses visible. Every rational representation extends to a real representation. Neither rational-valued character entries alone nor a 2-adic Schur index is being mistaken for rational realizability.

## Semiperfectness really forces a finite projective lift

Assume A=Z_(2)G is semiperfect. View the finite-dimensional projective B-module E as an A-module via reduction. It is finitely generated, so it has an A-projective cover π:P→E. This P is finitely generated: take finitely many preimages of generators of E and their A-span P0. Since P=P0+ker(π) and the kernel is superfluous, P=P0. Thus P is a direct summand of A^n, and its underlying Z_(2)-module is finite free.

Because 2E=0, π factors through a surjection P/2P→E. As E is B-projective it splits. Its kernel is superfluous in P/2P because ker(π) is superfluous in P and contains 2P. A split superfluous direct summand is zero. Hence P/2P≅E, an exact rank-eight projective lattice lift. This uses only the defining projective-cover consequence of semiperfectness. It does not use general extension lifting, Proposition 3.3, rational descent, local Schur-index classification, or the disputed historical coinvariant claim.

## Character values of a projective lattice

Let L be any finite projective Z_(2)G-lattice. On an odd-order g, complete at 2 and extend scalars to an unramified coefficient DVR containing the required odd roots of unity. The spectral idempotents for g are integral because its order is a unit. Their free ranks are unchanged by reduction. The characteristic-zero trace therefore agrees with the Brauer trace of L/2L.

For a 2-singular g, restriction of L to C=<g> is projective, because Z_(2)G is finite free over Z_(2)C. Write C=C_(2^a)×C_m, a≥1, m odd. After completion and an unramified extension containing μ_m, the group algebra splits by the odd-part spectral idempotents into copies of O'C_(2^a). Each copy is local: all simple modules over this finite O'-algebra reduce modulo the maximal ideal, and F'C_(2^a) is local. A finite projective module over each such local ring is free. The nonidentity 2-part of g has zero trace on its regular representation, hence zero trace on every free summand; multiplication by the scalar odd eigenvalue does not change the zero. Thus the trace of g on L is zero. The completion is used solely to prove a necessary trace identity; the original fraction field remains Q.

For a lift of E these facts force Ψ=8,0,2,0,−2,0,0 in the order columns above. Column by column Ψ=χ++χ−. Equality holds on every conjugacy class, including both degree-five splits; no decomposition-matrix uniqueness inference is needed. Since χ− is irreducible and χ+ factors through the quotient while χ− has z acting as −1, the χ− multiplicity is exactly one. This contradicts the even-multiplicity requirement for the real extension of Q⊗L. Therefore E has no projective rational integral lift, and Z_(2)SL(2,5) is not semiperfect.

## Current checkpoint conclusion

The main algebraic implication chain passes this independent reconstruction. No main-proof counterexample or central unsupported equivalence was found. Remaining tasks in this family are complete 26-file mathematical inspection, historical-scope findings, and public/private receipt finalization. The source-status discrepancy is real but does not falsify the displayed counterexample theorem.
