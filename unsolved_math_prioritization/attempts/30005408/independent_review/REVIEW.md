# Independent source audit: local Hilbert–Burch parametrization (30005408)

**Verdict: PASS_EXACT_CREDITED_PUBLISHED_RESOLUTION.** Recommend **already_solved, 0/5 original proof attempts**. No mandatory correction.

Reviewed `KNOWN_RESULT.md`: SHA256 `e1fea95d788aa8f1de2606cccb02e3dfa29a2af022c7025cd576537e441c1634`. This is an independent AI source/application audit using gpt-6-astra at xhigh. It is neither a new proof of Oszer's theorem nor human peer review or a discovery claim.

## 1. The original question matches the cited theorem

I read the full relevant OWR6/2023 contribution, printed pp.345–347, and visually checked Definition5 and Conjecture6 on p.347. The contribution explicitly starts with a characteristic-zero field k and R=k[[x,y]]. Its local term order chooses smaller total degree first, with lexicographic x>y ties. Its general monomial ideals permit repeated staircase heights, unlike its earlier lex-segment result.

OWR Definition5 specifies polynomial perturbation entries with both valuation lower bounds and degree upper bounds. Its Conjecture6 calls the parameter space T'(E), after Definition5 calls it T(E). The reference to Homs–Winz Conjecture5.14 resolves that notation discrepancy. I checked the full 2021 primary text around that conjecture and the full 2023 primary text, Definitions2.1–2.5 and4.1 and Conjecture4.2. They give the same complete-local-ring map from the degree-truncated perturbation matrices to V(E).

Oszer's accepted manuscript, arXiv2407.07993v4, Corollary8.12, expressly identifies its result as Homs–Winz Conjecture4.2 and states that this map is an isomorphism. I visually checked the corollary and read its proof and the relevant surrounding definitions and results. The publisher's record corroborates publication in Quarterly Journal of Mathematics76(4),1159–1187, online18September2025, DOI10.1093/qmath/haaf032; its abstract also identifies the Homs–Winz conjecture. The complete proof examined here is the accepted author manuscript. The full publisher PDF was not available, so no page-by-page final-journal comparison is claimed.

Thus the package identifies a known resolution of the original parametrization question. It does not substitute a dimension count, an ambient polynomial Hilbert cell, or the earlier lex-segment special case for the original target.

## 2. Exact matrix bounds and the two typographical cautions

Let m_0=0<m_1≤...≤m_t and d_i=m_i−m_(i−1). Zero d_i and redundant intermediate generators are permitted. Put

    u_ij=m_j−m_(i−1)+i−j.

For nonzero entries, the Homs–Winz conditions say that all exponents e lie in

    max(0,u_ij+1)≤e<d_i  if i≤j,
    max(0,u_ij)≤e<d_j    if i>j.

Zero entries are always permitted, and an empty exponent interval forces zero. These are exactly the ranges in the frozen artifact.

The display before Oszer Corollary8.12 literally uses ord in its upper bound and varies its subscript notation. Read alone, that display would permit arbitrarily high terms and would not describe the required affine space. The proof, however, explicitly identifies the parameter space with the restriction of the spread-out matrix from Definition3.1. That definition imposes **degree** less than d_i above/on the diagonal and less than d_j below it. Homs–Winz Definition4.1 independently gives those same bounds. The artifact correctly preserves this finite ambient truncation and flags the imperfect display; it does not use the erroneous untruncated interpretation.

Likewise Example2.4's adjacent sentence reverses the inequality between deg(x) and deg(y). The displayed order comparison and actual cocharacter give deg(x)=−M+1>−M=deg(y), which favors x in equal-degree ties. The artifact follows those formulas and explicitly notes the discrepancy.

## 3. Weight calculation and applicability of Corollary8.11

Definition4.2 assigns a coefficient of y^e in entry(i,j) bidegree

    (i−j, m_j−m_(i−1)−e).

Pairing with (−M+1,−M) gives

    w=M(e−u_ij)+(i−j).

For M>t, the nonzero integer e−u_ij controls the sign whenever it is nonzero. If e=u_ij, the sign is that of i−j. Thus positive weights give exactly the two displayed lower bounds. A zero weight would require e=u_ij and i=j, but then e=d_i, excluded by the ambient degree bound. This also covers zero d_i and all empty parameter ranges.

Hence the surviving affine parameter space has strictly positive weights, so the origin is its only fixed point. This is precisely the extra condition in Corollary8.11. For any finite monomial range, increasing M also makes the weight order equal to negative-degree lex: different total degrees dominate the bounded x-exponent difference, and equal total degrees compare x exponents. The primary theorem supplies the finite-colength cell dictionary. It is not necessary, or possible, to represent this local order by one weight vector on all monomials without a finite truncation.

The restriction to the original characteristic-zero fields is safe. Oszer fixes a field in Section2 without imposing algebraic closedness, and the isomorphism is a scheme statement over that field. No extension to additional characteristics is needed for this source-status conclusion.

## 4. Completion and extraneous polynomial support

This is a real issue, correctly handled in the artifact. Theorem8.10 uses the family defined by I+(y^(t m_t)), where I is the ideal of maximal minors, rather than assuming all polynomial fibres of I have the desired support.

On the positive parameter cell, the coefficient u of y^(t m_t) in the resultant has weight zero. All parameter variables have positive weights; therefore u is constant. At the origin the extreme minors are, up to harmless signs, x^t and y^m_t, and their normalized resultant has coefficient1. Thus u is nonzero everywhere on this cell. The resultant identity is

    y^(t m_t)(u+yW) ∈ I.

After completion at (x,y), u+yW is a unit. Multiplying the identity by its formal inverse proves y^(t m_t)∈IR, so

    (I+(y^(t m_t)))R=IR.

This is an equality of completed ideals. It does not imply equality of the original polynomial ideals, their global support, or their global colength.

Conversely, a finite-colength ideal in k[[x,y]] is determined by a finite quotient modulo a power of (x,y), and k[x,y]/(x,y)^N equals k[[x,y]]/(x,y)^N. Thus the usual correspondence between punctual polynomial ideals and complete local ideals preserves the local target and its initial ideal. Together with Oszer's theorem and the weight calculation, this verifies application to the exact map in the conjecture.

As an independent concrete diagnostic, I recalculated Oszer's Example8.9 from its 5-by-4 matrix. Its extreme-minor resultant is

    y^12(1+a b² y).

For a=b=1 the uncut polynomial ideal has colength7, while adding y^12 gives colength6, the colength of E=(x^4,xy,y^3). The extra point is (−1,−1); the factor1+y is a unit at the origin. The completed ideals therefore coincide despite their different global colengths. This directly checks why the local completion step is indispensable.

## 5. Reproduction and scope of the verdict

All **160,382** submitted assertions replayed with a byte-identical receipt. The separate checker passes **76,251** exact controls. Its structurally different checks include:

- generating791 staircases from exponent differences, including zero differences
- counting quotient monomials by direct divisibility against the full generator list
- deriving weights by pairing the original bidegrees, then comparing allowed parameters
- comparing sorted finite monomial orders
- constructing inverses of u+yW by a triangular coefficient recurrence with varying nonzero rational u
- symbolic maximal minors and the exact resultant of Example8.9, followed by independent Groebner calculations at16 rational parameter pairs, distinguishing global colength7 from punctual colength6

Reproduce with `python independent_checks.py` in this directory; reproduce the submitted checks with `cd author_replay && python verify.py`. SymPy is required by the independent symbolic diagnostic. The controls do not independently prove Oszer's global isomorphism theorem or its full geometric foundations. The verdict rests on exact published-theorem coverage, with the local completion and convention matching checked above.

The package is ready as a credited **already_solved0/5** source-status correction. Preserve the degree truncation, complete-local-ring target, characteristic-zero scope, and accepted-manuscript versus final-PDF qualification.

## Primary sources

- [Original OWR6/2023](https://doi.org/10.4171/owr/2023/6), pp.345–347
- [Homs–Winz2021](https://arxiv.org/abs/2004.04776), Conjecture5.14
- [Homs–Winz2023](https://arxiv.org/abs/2309.06871), Definition4.1 and Conjecture4.2
- [Oszer accepted manuscript](https://arxiv.org/abs/2407.07993v4), Definitions3.1/4.2, Example2.4, Theorem8.10 and Corollaries8.11–8.12
- [Publisher article record](https://academic.oup.com/qjmath/article/76/4/1159/8257706)
