# Independent audit: topological-bordism Euler nonvanishing

Problem 30000323 / OWR-1063-006, rank 1094. Audit date: 8 October 2026.

## Verdict and acceptance scope

**Accept the stated partial results and the unresolved disposition. No substantive mathematical correction is required.** The original authored files and verifier are preserved byte-for-byte. This audit adds verification and explicit proof-interface explanations; it does not add a sixth approach.

The universal assertion for MSTOP_(p), and even the value of its Euler class for the displayed representation W, remain **unresolved by this work**. Five approaches have been used, 5/5. Nothing here certifies worldwide openness, a new theorem in the literature, or a solution or counterexample to the target.

Accepted items are the mod-p detection criterion, the exact cyclic/K-theory criterion, the dimension and reciprocal-order sufficient conditions, the three obstruction properties of W, the localization/nonnilpotence equivalence, and the formal Euler expression with its expressly limited ring interface. The splitting discussion is accepted as an explanation of a missing comparison, not as a new structural theorem or proof of impossibility.

## 1. Target and source identities

The target is the natural complex orientation

    MU → MSO → MSTOP → MSTOP_(p)

and the Euler class of EG ×_G V on BG, in degree 2 dim_C(V). Here p is odd, G is a finite abelian **p-group**, and V has no trivial character summand. This last condition is V^G = 0, and does not assert that the action on the sphere is free. For V = 0 the Euler class is the unit. The p-local nonvanishing implications also prove nonvanishing before p-localization, without asserting that localization commutes with cohomology of every infinite CW complex.

The question appears on printed p.2423 of the [Oberwolfach report](https://ems.press/content/serial-article-files/46013). The [Hanke–Puppe preprint](https://arxiv.org/pdf/math/0301279), §§2 and 5, identifies Borel cohomology, Euler localization, cyclic K-sensitivity, and the oriented topological Thom spectrum. I inspected these interfaces in the saved text and checked the question and Lemma 5 visually. The inspected paper is arXiv:math/0301279v1. The published Trans. AMS version was not independently inspected; the earlier publisher-access failure does not justify a claimed published/preprint comparison.

The [Madsen–Milgram book](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/madmil.pdf), Remark 2.25, identifies TOP/PL as K(Z/2,3). Its odd-primary disappearance supports the natural PL/TOP equivalence used in the packet; it does not identify topological with smooth bordism. Chapter 5.A, Lemma 5.3, and p.116 concern the KO orientation and its multiplicativity. Complexification supplies the multiplicative KU orientation. Pages 105, 113–114, 116 and 219–220 were inspected visually. The original tom Dieck proof underlying the attributed MU sensitivity was not re-audited and is not required for the elementary partial proofs.

## 2. Mod-p detector

For G = product_i C_(p^a_i), the reductions u_i of the integral degree-two character classes generate a polynomial subring of H*(BG; F_p). The full ring is that polynomial ring tensored with the exterior algebra on degree-one classes. For a_i > 1, the mod-p Bockstein of the degree-one class need not be u_i; the original correctly avoids this identification.

A character with weights b_i has c1 modulo p equal to sum_i (b_i mod p)u_i. Consequently the product Euler polynomial is nonzero exactly when every summand has at least one weight nonzero modulo p. This uses the integral-domain property only in the polynomial subring, not in the entire exterior-polynomial cohomology ring. The coordinate condition is equivalent to the character lying outside pG*, and also to its restriction to G[p] being nontrivial. The ordinary orientation of MSTOP sends its canonical complex Euler class to this polynomial. Nonzero image therefore proves nonzero source.

This is an if-and-only-if criterion for the **mod-p image**, not an if-and-only-if criterion for MSTOP. A nontrivial order-p character on C_(p²) has weight p and shows exactly why nontriviality alone is insufficient.

## 3. K detector and the orientation interface

Let x_std and x_S denote the customary KU complex orientation and the orientation induced by the Sullivan map composed with the canonical MU orientation. After matching the normalized fiber generator, the projective-bundle calculation on CP∞ gives

    x_S = x_std u(x_std), with u(0) = 1.

The series u has its inverse on CP∞. Pullback by each character classifying map carries both u and its inverse to BG. Thus the corresponding Euler factors, and their finite products, differ by an actual unit. This does not require summing an arbitrary formal geometric series directly on BG. The unit is formed universally first. The original argument is therefore sufficient even though the two K orientations have not been identified as equal.

The customary Euler class is, up to a Bott unit, the image of product_j(1 − χ_j^(-1)) in R(G). If the kernels cover G, its character function is zero at every g, so character injectivity makes this element zero already in R(G). If some g avoids every kernel, restriction to C = <g> has only nontrivial character summands, and the cyclic sensitivity theorem applies. These two implications prove the exact K criterion without assuming an injection from an arbitrary representation ring into an unspecified completion.

For completeness, the cyclic interface can be checked directly. The KU Gysin calculation gives

    KU_(p)^0(BC_(p^r)) = Z_(p)[[t]] / ((1+t)^(p^r) − 1).

Take a primitive p^r-th root ζ in a finite extension of Q_p. Since ζ−1 is topologically nilpotent, evaluation t ↦ ζ−1 defines a ring homomorphism to its complete valuation ring, killing the displayed relation. Every nontrivial character factor maps to 1−ζ^(-a) ≠ 0. The target is a domain, so any finite product is nonzero. This supplies the particular nonvanishing needed here and avoids treating a nonzero constant term p as, by itself, a general primality criterion. This is verification of the existing cyclic route, not a further target approach.

For the numerical corollary let o_j be the order of χ_j. Its kernel has |G|/o_j elements. All kernels contain the identity, so for d ≥ 2,

    |union_j ker χ_j| ≤ 1 + sum_j(|G|/o_j − 1).

When sum_j 1/o_j ≤ 1 this is at most |G|−d+1 < |G|. The d=1 and d=0 cases are handled separately. Since o_j ≥ p, d ≤ p implies this condition. Equality at d=p is valid because the common identity is subtracted repeatedly. No assertion of necessity is made for this numerical sufficient condition.

## 4. The simultaneous obstruction W

For G=C_(p²)×C_p, let α=λ^p and let β be the second-factor character. Then

    W = α ⊕ sum_(a=0)^(p−1) α^a β

has p+1 nontrivial summands. Its kernels are the p+1 distinct maximal subgroups. Indeed, nonzero maps G→C_p factor through G/pG ≅ F_p², and the listed weights represent all projective lines of the dual.

The ordinary integral Euler class is zero: the factors α and β contribute p u v, and p v=0. This argument does not require an asserted full presentation of integral cohomology. At (s,t), if s=0 modulo p, α=1; otherwise the equation as+t=0 has one solution a modulo p. Hence every group element lies in a listed kernel, and the representation-ring Euler product is zero. Every proper subgroup lies in a maximal subgroup, so it has a trivial restricted summand. Its Euler restriction vanishes in every complex-oriented theory by the Whitney formula and the vanishing Euler class of a trivial line.

These are three genuine failures of detectors. They are not an MSTOP calculation. Removing any listed character uncovers p(p−1) elements, which verifies sharpness of the cyclic-detection dimension threshold. Replacing α by λ makes the ordinary detector nonzero. The elementary-abelian projective-line representation has zero K Euler and nonzero mod-p Euler; repeated weight-p characters of C_(p²) give the converse detection pattern.

The transfer warning is also correct. The projection formula contains tr_H^G(1), not a freely replaceable index. In K-theory this is Ind_H^G(1). For an index-p subgroup its character is p on H and zero off H, distinct from the scalar p. This distinction also survives in Borel p-local K-theory: restrict to a cyclic subgroup generated by g outside H and apply the cyclotomic evaluation above. The induced representation evaluates to the sum of all p-th roots, zero, while the scalar evaluates to p, nonzero. Thus zero restriction of an Euler class alone supplies no deduction that p times it is zero in MSTOP.

## 5. Localization, formal groups, and splitting

The relevant ring is graded-commutative, and all Euler denominators are even and central. Its localization is zero precisely when the multiplicative Euler set contains zero. Finitely many nontrivial characters occur. With Δ_G their product, a vanishing monomial divides some Δ_G^N, while each Δ_G^N itself is an allowed Euler monomial. Universal nonvanishing for fixed G is therefore equivalent to nonnilpotence of Δ_G. Proving only Δ_G ≠ 0 is insufficient.

In the canonical formal group law, put x=e(λ), y=e(β), and z=[p]_F(x). The Euler identity is exactly

    e(W) = z product_(a=0)^(p−1) F([a]_F(z),y),

with [p²]_F(x)=0 and [p]_F(y)=0. These follow from tensor powers and Whitney multiplication. The classifying map through (CP∞)² induces the stated homomorphism from the formal power-series quotient. To interpret this source, use the graded power-series ring supplied by finite projective spaces and their inverse limit; orientation gives surjective transition maps, so this particular universal power-series construction has no unresolved lim¹ term. This observation does **not** establish the analogous quotient presentation for E*(BG). The latter still needs the actual Gysin, Künneth, torsion and completion analysis. An algebraic ideal quotient suffices for the homomorphism asserted in the original.

Additive and multiplicative specializations of this Euler expression both vanish. Neither simultaneous vanishing nor nonvanishing before inflation decides the MSTOP class. The unknown higher-information interface is retained honestly.

The cited Sullivan decomposition does involve the Thom map of γ_p. The book explicitly describes this map as exotic and associates the coefficient isomorphism modulo torsion with it. A spectrum splitting alone does not supply the required orientation-compatible multiplicative detector for the natural MU→MSTOP composite. Nor does a coefficient theorem modulo torsion establish injectivity on BG. The report correctly claims only that this proposed deduction is missing, not that every possible refinement is impossible.

## 6. Computational audit and evidence limits

The original verifier was reproduced in normal, -O and -OO modes. It checks 3,135 small character subsets and W at p=3,5,7,11. The independent verifier uses rational phases and a subset expansion in the character group ring rather than the original common-denominator/convolution routines. It checks 11,632 character multisets over six groups, including repetitions and the zero-dimensional case. There are 11,302 reciprocal-order cases, 8,498 mod-p-detected cases, and 16 kernel-cover cases. It checks W at p=3,5,7,11,13 and enumerates every proper subgroup for p=3,5,7: respectively 9,13,17 proper subgroups. The integral polynomial check concerns only the Chern-generated tensor subring; the short p u v=0 proof above is the mathematical justification.

Seven explicit source mutations are rejected in every optimization mode: wrong kernel phase, addition instead of subtraction in the group ring, wrong ordinary modulus, primitive replacement for α, a missing projective character, scalar substitution for transfer, and composite-p acceptance. The existing representation mutations also test removal of each summand, trivial summands, inflation, and complementary detectors. No Python assert controls these results.

Both verifiers additionally run in all three modes from a 0444-file/0555-directory snapshot under actual UID=EUID=1000. Write-opening an existing sentinel, creating a new file, and unlinking the sentinel are denied. The snapshot is hash-identical afterward. These are ordinary OS-permission checks; they do not claim protection against an owner changing modes or against root.

All finite checks support only finite exact algebra. They do not compute MSTOP*(BG), prove a formal quotient presentation, detect every Euler class, reprove Sullivan's construction, audit the tom Dieck original, or establish novelty. The full target and the particular mixed-exponent class remain unresolved.

## 7. Deliverable and stopping condition

The evidence manifest identifies the accepted original authored bytes, the authored audit, the test programs, and their receipts. Public source metadata contain titles, public URLs, sizes, hashes and inspection locations only. Source PDFs, extracted source text, page images and private coordination records are excluded from the shareable packet.

There is no corrected replacement or contextual correction patch, because no correction is required. This report is an audit supplement. The original packet remains the accepted partial-result packet. No repository, pull request or queue action is part of this audit. The stopping condition is reached with the partial claims checked and the unresolved five-route disposition preserved.
