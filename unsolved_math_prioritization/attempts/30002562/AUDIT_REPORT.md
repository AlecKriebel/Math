# Independent mathematical and source audit: ternary zero threshold

## Review status of this edition

This is an AI-assisted mathematical exposition accompanied by an independent internal AI mathematical and source audit. These authored documents are unrefereed. Acceptance means the scoped theorem-dependent conclusion of that audit, not external human peer review, journal acceptance of this exposition or audit, or formal proof-assistant certification. The credited existence theorem and its patchworking foundations are prior mathematics of the cited authors; no novelty or full independent reproof is claimed.

## Outcome

The exact all-degree lower bound is accepted as an implication of a cited prior existence theorem. The authored bridge from finite real plane curves to PSD ternary forms is correct. The proposed edition makes BDIM Theorem 4.5 the primary route and explicitly narrows the source-proof inspection claim concerning Theorem 4.8. The result belongs to prior literature; this audit makes no novelty claim.

Acceptance is theorem-dependent: the existence construction and the deeper patchworking foundations remain imported mathematics. This audit is not a formal proof, a coefficient-level implementation of the construction, or a line-by-line reproof of every external dependency.

## 1. Exact target

The domain is all real PSD homogeneous polynomials of degree exactly 2k in three variables. Zeros are distinct points of RP^2. The excluded factor is the square of a homogeneous real form that changes sign on R^3. The threshold uses a strict inequality in its premise.

The original Oberwolfach text first motivates a question using irreducible examples, but its threshold paragraph quantifies over real PSD ternary forms without imposing irreducibility. Its half-degree alpha(k) is the question's indexing. The 2015 slides use alpha(2k) instead. The slides' parenthetical discussion of complex irreducibility is not an extra assumption on the threshold.

The original contribution contains an evident duplicated alpha(2) index in its low-degree examples. It also reports five historical remaining cases, whereas slides 47-48 report eight degrees. Neither inconsistency changes the explicit all-k conjecture or supplies a current remainder. No historical reconciliation is asserted.

## 2. Authored bridge checked independently

The connectivity proof works in dimension two. Stereographic projection reduces a punctured sphere to a plane minus a finite set, and a two-segment path can avoid that finite set. The antipodal quotient gives the corresponding fact for RP^2.

For a real even-degree form, division by the kth power of the squared Euclidean norm is invariant under every nonzero real rescaling, including negative rescaling. The normalized function is continuous and nonzero off the finite zero set. The complement is nonempty and connected. Its sign is therefore constant. Choosing that sign yields global PSD, including the origin; no numerical sign test is involved.

The real-equation descent is valid for reducible reduced curves as well: conjugation preserves the principal homogeneous ideal and hence sends its degree-d squarefree generator to a unit scalar multiple. The scalar has modulus one and can be removed by rescaling. Degree and zero locus are preserved.

Finiteness excludes an indefinite factor without an irreducibility argument. Positive normalization of two opposite-sign vectors works for forms of either parity. A finite projective zero set would lift to a finite set on S^2; continuity on its connected complement contradicts the opposite signs. If h^2 divides p, every zero of h belongs to the zero set of p. Thus finite p cannot have the specified factor.

Finally, a finite witness with N zeros rules out every A < N, including A = N-1. It says nothing by itself about A = N. The conclusion is alpha >= N, with no off-by-one error.

## 3. Primary source route: Theorem 4.5

The displayed theorem applies to every k >= 3, with no genus or irreducibility hypothesis added. It gives reduced finite real algebraic plane curves of degree 2k in the standard real plane and ordinary cardinalities B(k). The residue formulas in PROOF.md agree with both inspected versions. In each residue class k = 3l + r, the relevant l is at least one; the factorizations in that proof establish B(k) >= k^2+1 universally.

Construction inspection covered Theorem 4.2, its cubic tile and Figure 5, the boundary adjustments in Theorem 4.5 and Figure 6, and the full hypotheses and conclusions of Theorem 3.1. The construction uses real polynomial patchworking on the standard real torus and then coordinate squaring. It is an algebraic construction, not the pseudoholomorphic comparison in the introduction, and it does not use the ellipsoid real structure discussed later in the paper.

As an independent check of the cubic building block, the polynomial

    1 + x^2 y + x y^2 - 3xy

has the stated triangle as Newton polygon and is nonnegative for positive x,y by the arithmetic-geometric mean inequality. Equality forces x = y = 1. Its gradient vanishes there and its Hessian is [[2,1],[1,2]], positive definite. Thus this local tile indeed supplies a solitary real node in the positive quadrant. This check alone does not construct the entire patchwork.

Under coordinate squaring, a positive-quadrant point gives four distinct real affine points, an appropriate axis tangency gives two, and the specified projective corner contributions are separate. Exact global cardinality and boundary behavior are imported from Theorem 4.5; they are not inferred merely by multiplying an affine count or reading a picture. The formulas are used as an existence input, rather than claiming an independent all-l reconstruction of Figure 6's combinatorial count.

Theorem 3.1 gives a family of real polynomials, with nodal curves and specified control of singularities and toric boundary intersections. Nodal curves are reduced. The coordinate-square pullback is étale off the coordinate divisors. Those divisors are not curve components; thus no generic multiplicity is introduced. Homogenization has degree exactly 2k, and there is no hidden inflation by squaring a lower-degree equation. The standard real structure ensures a locus in RP^2.

Theorem 3.1 identifies its foundations as Shustin's 2006 patchworking theorem, Shustin's 2005 Lemma 5.4(ii), and the local deformation patterns of Itenberg-Kharlamov-Shustin 2015, Lemmas 3.10-3.11. Their bibliographic identities and cited roles were checked. Their entire proofs and all transversality reductions were not independently reproduced. Theorem 4.5 is accepted at the ordinary level of reliance on a published existence theorem, with these dependencies disclosed.

A source arithmetic inconsistency is preserved: the first formula gives B(6)=42, but the ensuing degree-12 discussion mentions a construction with 43 before improvement to 45. No choice between those narrative counts is needed for this audit's theorem-dependent lower bound, since 42 >= 6^2+1. The statement's formula has not been silently corrected.

## 4. Secondary route: Theorem 4.8

The theorem statement has the precise needed range k >= 3 and 0 <= g <= k-3, and count k^2+g+1. Setting g=0 is legitimate even at k=3. Therefore its stated existence conclusion also yields the target through the verified bridge. Its count is |RC|, not the weighted count separately defined in Section 2.

The proof's numerical and parameter checks are sound. With n=1, b=k-2, q=g+1, Lemma 3.2's parameter constraint is satisfied. Its two node counts become k+g and k-g-3, and its B0 tangency count is k-g-1. The stated upper-half-plane node count is

    N = (k-2)(k-3)/2 + 2k + g - 2.

The final count 2N + (k-g-1) equals k^2+g+1 identically. At k=3,g=0 this is 2*4+2=10. The weighted Newton triangle transforms under y -> y^2 to total degree 2k. These arithmetic checks do not prove the intermediate curve exists.

The unresolved geometric interface is precise. The C1 supplied by Theorem 4.8 has one boundary root with multiplicity 2k-4. The named perturbed curve from Lemma 3.2 has b=k-2 distinct simple tangencies on B_infinity, hence k-2 separate boundary roots of multiplicity two. Theorem 3.1 requires matching common-edge restrictions. These profiles coincide when k=3 and differ for every k>=4. Rescaling a polynomial or applying an automorphism of the boundary cannot merge distinct roots. The inspected manuscript and arXiv version both contain this interface. The audit does not supply or certify a deformation that would repair it.

The proof also describes its defining polynomial as positive on the upper half-plane despite specifying isolated zeros there. Read literally that wording cannot mean strictly positive everywhere. The authored global sign argument avoids relying on this phrase.

Accordingly, this audit accepts the theorem-to-threshold implication but does not certify a complete independent reconstruction of Theorem 4.8's patchworking proof. Theorem 4.5 uses a different construction in the same paper and avoids this specific interface. It is not an independent source confirmation.

## 5. Adverse checks and excluded shortcuts

- A k-by-k grid with only k^2 zeros misses the requested additional zero.
- An asymptotic lower bound cannot by itself settle every small degree.
- A form with infinitely many zeros is not this finite witness.
- Squaring a sign-changing form would retain the forbidden factor and infinitely many zeros.
- (x^2+y^2)^2 shows why finite zeros do not exclude all square factors; the factor here is semidefinite.
- The real binary form xy changes sign although its RP^1 zero set is finite. The connectivity step is dimension-specific.
- An odd-degree form does not define the normalized scalar-valued projective function used for even degree. The sphere argument for indefinite factors still works.
- Two antipodal points on the sphere are one projective point.
- A zero of multiplicity greater than one is still one distinct projective point.
- A nonreduced divisor's multiplicity is not a substitute for the degree of its reduced support.
- The existence of a real polynomial equation cannot be inferred just from a complex curve's having some real points; conjugation invariance matters.
- No result about the maximum finite zero count for arbitrary SOS forms is needed or accepted here.

## 6. Sources actually inspected

1. Reznick's complete Oberwolfach contribution, printed pages 1010-1013 (PDF pages 34-37), including the last reference continuation, was read in authenticated extracted text. PDF pages 34-35 were visually inspected. Other workshop contributions were not mathematical inputs.
2. Reznick's 2015 slides: title and PSD conventions, definition section on PDF pages 11-16, conjecture and nearby discussion on pages 29-31, and historical lists on pages 47-48 were read. Pages 11, 29, 47 and 48 were visually inspected. The entire 73-page deck was not reread.
3. BDIM author manuscript: Sections 1.1-1.3; the reduced-genus and weighted-count definitions in Section 2; Section 3.1 including all of Theorem 3.1; Section 3.2 through Lemma 3.2 and its full proof; Section 4.1 including Theorems 4.2 and 4.5 and their proofs; Theorem 4.8 and its proof; and relevant bibliography entries were read. Pages 6-9, 14 and 15, including Figures 1-3 and 6, were visually inspected. The Figure 5 tile discussion was read in text. Other portions were consulted for ambient-space and terminology separation; they are not independently certified proofs.
4. The arXiv version's matching Theorems 4.5 and 4.8 and relevant construction text were cross-checked. It is not an independent source.
5. The publisher landing page and arXiv record were inspected for authors, title, DOI, journal, pages, and publication status. The publisher reports publication on March 1, 2019. A request for the publisher PDF yielded the subscription landing page, not a full PDF. No full version-of-record inspection is claimed.
6. External foundations were identified from the source bibliography and primary publisher metadata. Limited primary search text for Shustin's Lemma 5.4 was consulted; the full dependency proofs, including the Harnack and dessins sources, were not freshly audited. The Riemann existence theorem, elementary real-polynomial descent, and the topological facts have the precise roles stated above.

Fresh retrievals of all four principal PDFs matched the authenticated input hashes and byte counts exactly. The fresh arXiv HTML also matched. The fresh publisher HTML differed, while its citation metadata remained equal; it is not reported as a byte match. Hashes and sizes are supplied separately as permitted verification metadata.

## 7. What can be concluded

The full requested lower-bound statement follows, under the explicit prior-theorem dependency, from the corrected primary route. The bridge is complete and independently reviewed; it requires neither irreducibility nor SOS status. The unresolved source-proof interface must remain visible in descriptions of Theorem 4.8 inspection. No exact alpha, general SOS maximum, all-degree coefficient formula, independent second source, current exception list, or novel mathematical discovery is certified.

### Public source links

- BDIM author manuscript: https://www.i2m.univ-amu.fr/perso/frederic.mangolte/FiniteCurves.pdf
- BDIM arXiv record: https://arxiv.org/abs/1807.03992
- BDIM publisher metadata: https://link.springer.com/article/10.1007/s40879-019-00324-9
- Original Oberwolfach report: https://ems.press/content/serial-article-files/46507
- Reznick 2015 slides: https://reznick.web.illinois.edu/10-16-15f.pdf
- Shustin 2006 chapter metadata: https://doi.org/10.1017/CBO9780511526374.014
- Shustin 2005/2006 article metadata: https://doi.org/10.1090/S1061-0022-06-00908-3
