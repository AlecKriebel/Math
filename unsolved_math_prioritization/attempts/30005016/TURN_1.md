# Turn 1: field dependence, universal upper bound and exact scope

AI-assisted mathematical proof candidate; independent review pending.

## 1. Injection-to-interpolation lemma

Let K be infinite, and let h∈K[x,y] induce an injection K²→K. For each integer n≥1, V_n=span_K{1,h,…,h^(n−1)} has dimension n and interpolates arbitrary data on every n-point subset of K².

Proof. The polynomial h is nonconstant. If d=deg h≥1, its powers have distinct total degrees 0,d,…,(n−1)d and are linearly independent. For distinct points P_1,…,P_n, the scalars a_i=h(P_i) are distinct. The evaluation determinant in the displayed basis is the Vandermonde product ∏_{i<j}(a_j−a_i), which is nonzero. Thus evaluation is an isomorphism. ∎

The same assertion is not a theorem about univariate source data: the points are arbitrary points of K², and injectivity of a fixed bivariate polynomial on the whole plane is essential.

## 2. An unconditional characteristic-zero field with m_4(K)=1

Use Cornelissen, Stockage diophantien et hypothèse abc généralisée, C. R. Acad. Sci. Paris 328 (1999), 3–8, Proposition 8, printed pp6–7. Primary author-hosted PDF: https://webspace.science.uu.nl/~corne102/docs/abc.pdf . The relevant pages were visually inspected. The proposition supplies the polynomial injection x^m+t y^m for a function field K/k of a smooth proper curve, under its characteristic-zero, odd-exponent, root-of-unity and valuation hypotheses.

Apply it to K=Q(t), k=Q, the projective line of genus g=0. The extension K/k(t) is the identity and is separable. The only places where t has nonzero valuation are 0 and infinity, so N_t=2. Choose m=449. Then m is odd and

449 > 64·(2+max{5,2·0+3}) = 448.

Every element of Q(t) algebraic over Q belongs to Q: a nonconstant rational function of t is transcendental over Q (otherwise t is algebraic over an algebraic extension of Q). Thus every root of unity in Q(t) is ±1, and an odd m has only the trivial mth root of unity. Finally v_0(t)=1 excludes t being an mth power. All hypotheses hold. Therefore the polynomial

h(x,y)=x^449+t y^449

is injective on Q(t)². Section 1 gives m_4(Q(t))=1: a one-member family works, and the empty family cannot interpolate any four-point set. This is an explicit specialization of Cornelissen’s prior theorem, not an independently discovered injection.

The very same argument gives m_3(Q(t))=1. Consequently, the report’s assertion excluding a single universal three-dimensional space cannot be valid for every field allowed by its printed characteristic-zero hypothesis. This observation concerns the preamble, not a proof of the intended four-point minimum over R or C.

## 3. Over the real field one space cannot suffice

Let V⊂R[x,y] have dimension four and fix any basis f_1,…,f_4. Suppose its determinant were nonzero at every ordered four-tuple of distinct planar points. Start with P_1=(−1,0), P_2=(1,0), P_3=(0,3), P_4=(0,4). Move P_1 and P_2 along opposite semicircles of the unit circle until they exchange positions, keeping P_3,P_4 fixed. At every time the four points remain distinct. The evaluation determinant is a continuous real function of time. Its final value is the negative of its initial value, since two rows were exchanged. The intermediate value theorem forces a zero, a contradiction. Hence m_4(R)≥2.

This proof uses the real intermediate value theorem. It must not be asserted for arbitrary K or complex-valued determinants.

Together with Section 2, the exact minimum depends on the allowed field. In particular no single number can equal m_4(K) for every characteristic-zero K. However, a worst-case uniform minimum across fields is still a meaningful problem and is not resolved here.

## 4. Conditional number-field implication, clearly separated

Poonen, Multivariable polynomial injections on rational numbers, Acta Arith. 145 (2010), 123–127, Theorem 1.1 and Remark 1.2, proves that the relevant Bombieri–Lang hypothesis yields a polynomial injection for each number field. Primary manuscript: https://math.mit.edu/~poonen/papers/QQ.pdf . Combining this theorem with Section 1 would yield m_4(k)=1 for number fields under that conjectural hypothesis. This is conditional; it is not an unconditional result for Q.

## 5. Remaining target

This note does not determine m_4(R), m_4(C), m_4(Q), or the worst-case minimum over characteristic-zero fields. The known five-space upper bound remains credited. A later field-specific lower bound cannot be silently promoted to an all-field statement. No author clarification has been obtained, and no novelty claim is made.

## 6. The classical upper bound five, with a self-contained proof

For every characteristic-zero K, the following five spaces suffice:

A=span{1,x,x²,x³}; B=span{1,x,y,x²}; C=span{1,x,y,xy}; D=span{1,x,y,y²}; E=span{1,y,y²,y³}.

This is the five-staircase construction explicitly recorded by Shekhtman, cited in SOURCE_GATE.md. We give an elementary verification to make the scope independently checkable, not as a novelty claim.

Take four distinct planar points. If they are collinear, one coordinate restricts to a nonconstant affine coordinate on the line; its four values are distinct. Space A or E then works by Vandermonde. If they are not collinear, evaluation of 1,x,y has rank three. Evaluation of all polynomials of total degree at most two has rank four: for each selected point P, choose two of the other three points whose connecting line does not contain P, and a line through the remaining point avoiding P. Such a pair exists; otherwise all four points would be collinear. The product of these two affine linear equations vanishes at the other three points and not at P, and rescaling gives its Lagrange cardinal polynomial. Thus at least one of x²,xy,y² increases rank from three to four, so B, C or D works. This proves m_4(K)≤5.

Each member of this particular five-space family is indispensable, even over Q: exclusive configurations for A,B,C,D,E respectively are

- {(0,0),(1,0),(2,0),(3,0)};
- {(0,0),(1,0),(2,0),(0,1)};
- {(0,0),(0,1),(1,0),(1,1)};
- {(0,0),(0,1),(0,2),(1,0)};
- {(0,0),(0,1),(0,2),(0,3)}.

For each configuration, the named space has nonzero determinant while the other four have zero determinant, by direct evaluation. This only rules out deleting a member of this specific family. It does not exclude a different family of four, three or two arbitrary spaces.

## 7. Turn outcome

This is substantive author turn 1 of a maximum of five. It establishes the exact credited value m_4(Q(t))=1, the real obstruction m_4(R)≥2, the credited uniform upper bound five and five explicit indispensable-member witnesses for the standard family. The four-point minimum for R or C, the unconditional value for Q, and the best worst-case characteristic-zero bound remain unresolved. The source’s three-point preamble is separately qualified; the parameterized four-point question remains meaningful.

The accompanying pure-Python exact checker tests every four-point subset of the 5×5 integer grid, the five exclusive witnesses, 840 ordered Vandermonde cases and the exponent threshold. Finite controls supplement rather than replace the proof or the cited function-field theorem.
