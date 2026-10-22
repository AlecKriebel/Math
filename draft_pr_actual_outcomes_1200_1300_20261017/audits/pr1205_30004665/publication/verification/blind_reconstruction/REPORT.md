# Blind reconstruction report

Completed 2026-10-17T16:54:33Z. Completion estimate: 100% of the assigned canonical-support, chamber-pullback and independent facet audit; no candidate comparison performed.

## Result and exact claim

For D4 with center 2 and chronological reduced word i=(1,2,3,2,4,2,1,2,3,2,4,2), the canonical GHKK potential in the KS2022 reduced-word dual X torus has **22 monomials**, in summands of sizes **14,1,5,2** for simple roots **1,2,3,4**. Every coefficient is **1**. All 22 inequalities define distinct facets of a full-dimensional cone.

The canonical X expression has two monomials with X6 exponent -2, both in W1. The KS2022 Definition 9 chamber-ansatz pullback has the same 22 coefficients and all coordinate exponents in {-1,0,1}. The canonical X-coordinate exponent condition and the chamber-pullback exponent condition therefore differ on this example.

Set yk=Xk^{-1} and A=1+y3+y2*y3. An exact compact expression is

    W1 = y7*(1+y6+y6*y8*A
              +y6*y8*y10*(A*(1+y5)+y2*y3*y4*y5)
              +y2*y3*y4*y5*y6^2*y8*y10*(1+y1))
    W2 = y12
    W3 = y9*(1+y8*(1+y10*(1+y5*(1+y4))))
    W4 = y11*(1+y10).

The complete ordered support, coefficients, chamber exponent matrix, transformed exponents, positive roots, exchange matrix and explicit braid routes are in blind_frozen.json. Its immutable SHA256 is

7881d1d0ef80ff7ca036f16a06d2d7f23cb666bab223500226d6cded3f66a30d.

## Primary-source normalization

1. Koshevoy–Schumann, publisher version, *Journal of Algebraic Combinatorics* 56 (2022), 1031–1053, published 6 July 2022, DOI [10.1007/s10801-022-01144-z](https://doi.org/10.1007/s10801-022-01144-z). [Publisher PDF](https://link.springer.com/content/pdf/10.1007/s10801-022-01144-z.pdf). Equation (3), printed p.1039: with b_ik positive for i→k, X'_i=Xi(1+Xk^{-sgn(b_ik)})^{-b_ik}, and X'_k=Xk^{-1}. Definition 7, printed p.1040: optimized means that every adjacent mutable arrow enters the frozen vertex; the summand there is its inverse X-coordinate. Definition 8 and Lemma 2, pp.1041–1042: last occurrences are frozen; a three-term braid at positions t,t+1,t+2 mutates position t then swaps positions t+1,t+2. Definition 9 and Proposition 5, p.1043: CAhat_i(x)_k=product_l x_l^{M_kl}, with M_kl=-b_{i_k,i_l} for k<l<k+, half that at l=k or k+, and zero otherwise; varsigma_i,a=W_a∘CAhat_i.

2. Koshevoy–Schumann [arXiv:2109.14439v1](https://arxiv.org/abs/2109.14439v1), submitted 29 September 2021. I downloaded and checked its definitions independently of the publisher text. In particular, the later publisher example changes the displayed word in §7; the preprint word is not silently treated as the publisher word.

3. Genz–Koshevoy–Schumann [arXiv:1711.07176v1](https://arxiv.org/abs/1711.07176v1), submitted 20 November 2017. §4.2.2, printed p.15, explicitly requires c_kl<0 for an inclined edge l<k+<l+. KS2022 Definition 8 omits this adjacency condition in its literal display; including it agrees with its cited BFZ/GKS construction and is independently validated by every braid edge below. GKS2017 equation (20) displays the opposite bilinear-form index order from KS2022 equation (3), so I do not combine those formulas indiscriminately. Its Definition 7.1 gives the graded chamber construction; the reduced specialization used here is the explicit later KS2022 Definition 9.

4. Schumann, *Optimality of string cone inequalities and potential functions*, [original OWR2021 PDF](https://ems.press/content/serial-article-files/46898), printed pp.1123–1125. The A2 cone on p.1124 uses a permutation of the last two cluster coordinates relative to the chronological KS2022 example: its displayed normals correspond to support {1/x2,1/x3,1/(x1*x3)}, whereas chronological coordinates give support {1/X3,1/X2,1/(X1*X2)}. Setting (x1,x2,x3)=(X1,X3,X2) identifies them; the cone display does not specify coefficients. Its displayed A2 string transition also has a middle coordinate x1+x2, while KS2022 Definition 2 has x1+x3; the latter is the formula satisfying the exact chamber commutation check. These displays must not be used as an unstated chronological-coordinate normalization.

These source issues are handled by redundant algebraic checks, not by assuming any conjecture or desired conclusion.

## Mechanism and checkable evidence

The verifier constructs the reduced-word quiver: horizontal k→k+ edges; inclined l→k edges precisely when l<k+<l+ and the letters are Dynkin adjacent; no frozen–frozen edges. Frozen positions in the input are 7,9,11,12. Mutable positions are 1,2,3,4,5,6,8,10.

Exact simple-reflection matrices give 12 distinct positive ordered roots and product w0=-I. Thus the given word is reduced and represents the D4 longest element. This check uses the stated Dynkin edges independently of cluster combinatorics.

A deterministic 0–1 breadth-first search enumerates all 2316 reduced words, minimizing actual three-term mutations while commuting adjacent orthogonal letters at zero cost. All 12504 directed graph edges are checked for quiver transport and frozen-set transport. Routes ending in letters 1,2,3,4 use 8,0,4,1 actual mutations. Each target is explicitly checked to be optimized for its last frozen vertex. Pulling its inverse frozen coordinate back by the displayed X rule and collecting exact Laurent coefficients gives the immutable support.

A second ordinary breadth-first search reverses neighbor order and selects different optimized target words. Its four independent route choices reproduce every support coefficient exactly.

The chamber matrix is upper triangular with diagonal -1 and determinant +1. For every directed graph edge, verify_supplement.py checks the exact chamber/mutation commutative square. It uses the positive string-braid lift

    (u,v,w) -> (v*w/(u*w+v), u*w, (u*w+v)/w),

whose min-tropicalization is the later KS2022 Definition 2 string map. Both sides are compared exactly as monomial times a power of u*w+v, eliminating numerical tolerances and arbitrary rational simplifications. This establishes agreement of the quiver, X sign convention, coordinate permutation, chamber map, and source string map on all 12504 edges.

The A2 regression independently gives b=[[0,-1,1],[1,0,0],[-1,0,0]], W1=1/X3 and W2=(1+1/X1)/X2 in chronological coordinates.

## Independent facet certificates

For each support row e_i, supplement_exact.json gives an integer vector v_i with e_i·v_i<0 and e_j·v_i>0 for every j≠i. Every pairing is also recorded and rechecked by exact integer arithmetic. The common vector u=(-1,...,-1) strictly satisfies all 22 inequalities. Therefore the cone has nonempty interior and no inequality is redundant.

For each row, set d_i=-e_i·v_i>0 and h_i=e_i·u>0. The recorded integer point p_i=h_i*v_i+d_i*u has e_i·p_i=0 and e_j·p_i>0 for all j≠i. A neighborhood of p_i inside the hyperplane e_i·x=0 satisfies every other inequality strictly, so this row defines an 11-dimensional facet. This proves all 22 facet claims directly. No polyhedral solver is trusted: witness discovery simply enumerates directions in {-1,0,1}^8 and every certificate is subsequently checked by integers.

An initial SymPy free-variable LP attempt reported infeasibility; the explicit integer witnesses disprove that solver outcome. That route was abandoned. No mathematical conclusion rests on the LP result.

The chamber matrix is unimodular, so the transformed 22 inequalities have the same facet and nonredundancy status.

Supplement SHA256: a5a007b37cd3e257ca84f015b399eca7708f2c273b8e8e4966cafccec2749bbf.

## Interpretation and exact remaining gap

The strongest independently verified result is the exact canonical support and its 22 direct facet certificates. The exponent -2 in the canonical X torus coexists with complete nonredundancy. Read literally as an equivalence involving coordinate exponents of W in reduced-word X tori, the OWR2021 converse is contradicted by this example. In contrast, this example satisfies the later KS2022 multiplicity-free criterion for varsigma after chamber pullback; it does not contradict that later varsigma conjecture. Coefficients are 1 and every inequality is necessary, so this example gives no counterexample to a coefficient-greater-than-1 redundancy criterion.

No parent candidate or prior review has been inspected. Therefore I make no assertion that another artifact does or does not agree with this freeze. Any post-freeze comparison is separate work requiring the parent's explicit authorization.

## Reproduction and provenance

Run Python with SymPy 1.14.0 and bytecode writing disabled:

    PYTHONDONTWRITEBYTECODE=1 python -B verify_blind.py
    PYTHONDONTWRITEBYTECODE=1 python -B verify_supplement.py

The first command compares exact output against the immutable freeze without writing it. The second compares or creates the neutral supplement and never rewrites historical chronology. INITIAL_RECEIPT.md records the original information boundary; replays do not create or update that receipt.

Primary PDFs were downloaded directly. Because the shared disk filled, the downloaded PDFs were deleted only after their SHA256 hashes were captured, while extracted text was retained in ignored sources/. The OWR text was subsequently trimmed to the relevant pp.1123–1125. Original download hashes:

    a64b2b3385ac60b84aa49494eaf09e4247b35a431500cdc0d935bb3b79e55ff1  arXiv1711.07176.pdf
    e52425965d7082bdd302d1849f2f152e792631a6ce270bf3cecd7b76d7d2086b  arXiv2109.14439.pdf
    8eaf1548b90a759ca10d42f2d3c27daed2625ef2f7b2f681483681c88950864d  KS2022publisher.pdf
    04b1a4cbfa4552a0eee16d10323003ee459ffe1811b1466fadb821e24596ee5a  OWR2021.pdf

Published D4 source regression: verify_source_regression.py reproduces the KS2022 section 7 count of 27 terms and its unique coefficient 2 from the stated word and mutation sequence. All computed terms contain X9^-1; the printed expansion omits that factor twice. source_regression.json SHA256: 0f42d5d7aaefa4ed883b00e060142b868ab785b23027b625f5316da6fd77f79e. The report compact W1 formula was also checked exactly against the immutable blind support. No candidate inspection occurred.
