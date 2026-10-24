# Fresh adversarial review of compact-support cohomology and exact profiles

Completed: 2026-10-24, 20:23 UTC. Review completion estimate: 100% of the assigned partial-result audit. Kourovka 21.129 is not resolved by these results; this review supplies no originality certificate.

**Verdict: PASS for the stated partial claims, with one minor page-reference correction.** The argument computes identical graded compact-support cohomology rings for the eight pure central quotients within each rank-matched residual pair. It does not identify group-ring modules, ordinary cohomology rings of finite quotients, arbitrary quasi-isometry classes, or commensurability classes.

## Material actually inspected

I read the frozen files `COARSE_COHOMOLOGY_FILTER.md`, `PROFILE_TABLE.md`, `SPECTRAL_FILTER.md`, `profiles.json`, and `compute_profiles.py`. I independently read the cached original DJLO Theorem 1, its proof and Remark 6 (arXiv:1002.3129v2, printed pp.2–5), the 2015 Davis repair introduction, Theorem 2.2, Lemma 3.11, and Theorems 3.13–3.14 with equation (3.3). I visually inspected the relevant complete DJLO p.5 and Davis pp.12–13. I also read Cumplido–Paris Proposition 3.1(1)–(2) and its actual proof, printed pp.508–509. Source and input hashes are in `REVIEW_MANIFEST.json`.

The Davis paper explicitly announces that its poset-of-spaces argument repairs the nonconstant-coefficient problem in the original proofs. I have therefore used its corrected poset setup; merely citing the old Mayer–Vietoris calculation would be insufficient.

## 1. Decone, center, and classifying-space model

There is no unjustified substitution of an arbitrary direct-product factor for the geometric decone. Let M be the reflection-arrangement complement and choose a reflecting form α0. Its projective complement is identified with the affine slice X={α0=1} minus the remaining hyperplanes. The explicit product sends v in M to (v/α0(v), α0(v)); its inverse sends (x,t) to tx. Thus M is homeomorphic to X×C*.

The inspected CP Proposition 3.1 proof establishes that P=π1(M) has infinite cyclic center and that π1(X) is centerless: from P=π1(X)×Z, its center is Z(π1(X))×Z, which is infinite cyclic only when the first factor is trivial. Consequently π1(X)=P/Z(P)=Q. This also verifies that the geometric circle factor generates the entire pure center.

The established asphericity of the spherical reflection complement makes X aspherical, because the higher homotopy groups of X×C* are those of X. Essentiality gives decone rank n−1: a vector parallel to all affine decone hyperplanes and to α0=1 would be killed by every original reflecting form, contradicting essentiality. DJLO Corollary 2's proof records the finite CW model in the arrangement rank. Hence these are finite K(Q,1) models of dimension d=n−1, as required.

Q is countably infinite. Countability follows from the finite CW model. Infinitude can also be seen without assuming a free quotient: a meridian around any affine decone hyperplane, at a point away from all the other hyperplanes, has linking number one under that hyperplane's defining affine function X→C*. Thus π1(X) maps onto Z.

## 2. Spectral sequence, rank, and filtration orientation

The 2015 paper orders flats by **reverse inclusion**. The ambient flat V is its **minimum**, not its maximum. Its local arrangement is empty, and the corresponding space M_V is contractible. The local group-ring coefficient in degree zero is therefore ZQ.

In the repaired Theorem 2.2, condition (Z0) makes the coefficients constant on each relative-poset summand. The proof of Theorem 3.14 verifies (Z0) by the distinct local cohomological degrees for strictly nested flats. Lemma 3.11 and local central-arrangement concentration place every nonzero term in (3.3) in bidegree (r^G,r_G), where r^G+r_G=d. Differentials alter total degree by one; there can consequently be no differential between these nonzero terms. The filtration converges in a finite range.

For the minimum V the actual associated-graded term is

H^d(L(A)_{≥V},L(A)_{>V};Z) ⊗ ZQ = (ZQ)^{β(A)}.

Lemma 3.11 identifies the relative-poset coefficient, and Theorem 3.13 explicitly uses the ambient-flat beta identification. DJLO Remark 6 identifies this same free group-ring term. Here β(A)=c_T>0, verified independently below. The associated-graded term is sufficient: after tensoring the finite filtration with Q, an infinite-rank subquotient forces infinite rank of the whole group. It is not necessary to promote this term to a canonically split ZQ-submodule of the unfiltered group.

DJLO Theorem 1 (used with the repair) supplies actual **abelian freeness** of H^d(X;ZQ), not merely torsion-freeness. Since the finite complex has countable cochain groups, its top cohomology has at most countable rank. Since Q is infinite, the displayed associated-graded term has countably infinite abelian rank. Thus H^d(X;ZQ) is exactly a free abelian group of rank ℵ0. The other degrees vanish.

No equivariant identification between the modules for different types follows from this argument.

## 3. Compact supports, products, and large-scale scope

For a finite K(Q,1), the cellular cochains with group-ring coefficients are the finite-support cochains on its locally finite universal cover, so the group computation identifies H_c^*(E;Z). The only nonzero degree is d. In all eight types d≥3, so products of possibly nonzero classes have degree 2d>d and vanish. Degree-zero compact-support cohomology vanishes as part of the same computation. This verifies the zero multiplication assertion.

The assertion that these groups/rings agree within each pair is therefore correct. A proper homotopy equivalence induces the usual compact-support ring map; for the uniformly contractible bounded-geometry universal covers of finite classifying complexes, the standard controlled extension of a quasi-isometry and its inverse supplies such proper homotopy maps. Nothing here claims that ordinary finite-quotient Betti numbers or their Poincare polynomials are quasi-isometry invariants. Nothing supplies an action-preserving isomorphism of dualizing modules under a bare quasi-isometry.

## 4. Source phrase deliberately excluded

Davis 2015 p.12 describes a local group as free abelian of rank β′(A_G). If “rank” means finite underlying abelian rank, this cannot be correct generally. A central arrangement of three distinct lines has complement C*×(C minus two points); its top group-ring cohomology is the first group-ring cohomology of F2, which has infinite abelian rank. The proof under review explicitly rejects using this phrase. The needed freeness and degree concentration follow by the induction in DJLO and the repaired argument and do not require the incorrect finite-rank interpretation.

This is a source-level wording issue already disclosed in the authored note, not a fatal objection to its actual deduction. Rank β in the **free ZQ ambient term** is module rank and correctly yields infinite abelian rank.

## 5. Independent exact arithmetic and H4 root selection

`independent_profiles.py` contains a separate implementation using exact pairs of rational numbers for Q(√5), direct simple-reflection action, and a **Leibniz polynomial determinant** of xI−C. It does not import the author's code or use Faddeev–LeVerrier. It checks every positive power through h to verify the exact Coxeter-element order, checks cyclotomic factors, reconstructs Poincare polynomials and Euler characteristics, and compares all eight stored rows. All checks pass; the output is `independent_arithmetic.json`.

For H4 it independently obtains f=x^4+a(x^3+x^2+x)+1 with a=(1−√5)/2 and verifies f·bar(f)=Φ30 exactly. It checks the signs of g(y)=y²+ay+a−2 at 19/10, 2, −7/5, −13/10 by exact arithmetic and exact comparisons in Q(√5). Hence its two real y-roots lie in (19/10,2) and (−7/5,−13/10). The four possible primitive-30th-root y-values correspond to k=1,7,11,13. The k=7 value lies in (0,1), while the k=13 value is less than −√3<−7/5. The selected values are therefore k=1 and k=11, giving exponents 1,11,19,29. This root-selection step uses inequalities, not numerical approximations.

The verified c_T values, in table order, are 240; 5,040; 1,536; 5,040; 19,200; 368,640; 276,480; and 127,733,760. Positivity is enough for the infinite-rank argument. Their differing numerical values do not supply the missing quasi-isometry or commensurability obstruction.

## Minor correction and final limits

The note cites Davis Theorem 3.14 and equation (3.3) as pp.11–12. In the inspected PDF their correct printed/PDF pages are **12–13**. The theorem starts on p.12 and (3.3) is on p.13. This is a citation locator correction; it changes no deduction.

No substantive mathematical objection remains to the compact-support/coarse-cohomology filter or to the finite arithmetic claims within the exact scope just reviewed. I have not audited a complete solution of 21.129, because no such solution is asserted or supplied. I have not established originality of these arrangement-theoretic consequences and do not recommend publication as a solved Kourovka problem.
