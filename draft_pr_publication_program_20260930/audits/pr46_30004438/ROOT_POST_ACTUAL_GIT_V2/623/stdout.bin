# Independent review of the real periodic point source correction

**Verdict: PASS. The exact nonempty-interior question is already answered by the cited 2020 work of Kozhasov and Kummer.** The supplied all-degree, all-period construction is mathematically valid, and its neighborhood is open in the full real rational-map parameter space. No mandatory correction was found. The appropriate project disposition is **already_solved**, with existing-author credit and the preprint publication qualification retained.

Reviewed on 30 September 2026 by a separate gpt-6-astra reviewer at xhigh effort. The frozen SOURCE_STATUS.md has SHA-256 **a0d374da6984537cd9902e2e790177791739bdc32ea820b74830a6b50241ea6c**. It was not edited. This review independently verifies the complete affirmative construction needed for the selected question, rather than merely checking that an abstract claims a result.

## Exact original question and version history

The original contribution occupies printed pages 668–669 of [Oberwolfach Report 12/2020](https://ems.press/content/serial-article-files/46848). The workshop dates are 1–7 March 2020. Its Question 1 asks for real morphisms of every degree with exclusively real periodic points and is answered there by Chebyshev maps. Question 2 asks whether the locus has nonempty interior in the space of all real degree-\(d\) morphisms of the projective line. This second question, not merely existence or a polynomial special case, is the dataset target. I read the complete contribution and visually checked the question page.

The [April 2020 first preprint](https://arxiv.org/pdf/2004.10003v1) explicitly asserts ambient nonempty interior in the introduction and in the second assertion of Theorem 2, page 2. Section 2.2 on page 6 constructs the positive-coefficient strictly interlacing family and proves the all-period conclusion. The same paper separately constructs a lower-dimensional family near Chebyshev maps. That separate result does not limit the dimension of the first open family. Both assertions and the relevant proof were read, and the proof page was rendered.

The [October 2020 revision](https://arxiv.org/pdf/2004.10003v2) retains ambient interior membership in Example 1, page 3. The nearby Theorem 3 and its proof on page 6 address all periodic points using fixed points of the second iterate. Theorem 2 and Lemma 9 also explicitly establish the all-period property. Example 1 contains a sentence mentioning real fixed points, but its stated conclusion is membership in the interior of the locus defined by all periods. That isolated wording does not erase the later all-period statements. I inspected these passages and rendered the example page.

The [current arXiv record](https://arxiv.org/abs/2004.10003) confirms v1 dated 21 April 2020 and v2 dated 27 October 2020. It displays no journal reference or withdrawal notice. It is accurate to call this a preprint result. The review does not infer journal publication from the age of the work. The preprint qualification is compatible with the already-solved recommendation here because the actual sufficient construction has also been independently checked below.

## Ambient openness

A real degree-\(d\) morphism is represented by a pair of homogeneous degree-\(d\) forms with no common projective zero, modulo simultaneous nonzero real scaling. The resulting parameter space is the complement of the resultant hypersurface in \(\mathbb P^{2d+1}(\mathbb R)\). Its ordinary real-manifold topology is the topology relevant to interior in the question; no Zariski-open assertion is required.

The chart \(q_d=1\) has \(d+1\) free numerator coefficients and \(d\) free remaining denominator coefficients, hence \(2d+1\) real coordinates. Normalizing this one coefficient does not require the numerator to remain monic.

For the displayed products

\[
 p_d(z)=\prod_{j=1}^{d}(z+2j-1),\qquad
 q_d(z)=\prod_{j=1}^{d}(z+2j),
\]

all roots are simple, negative, mutually distinct, and strictly alternating. Every coefficient is strictly positive. A sufficiently small real perturbation of every coefficient in the chart preserves these properties. One elementary justification is to choose disjoint intervals about the original roots with alternating endpoint signs. Small coefficient perturbations preserve the endpoint signs and therefore give at least one real root in each interval. The degree is unchanged, so these account for all roots; by taking a sufficiently small discriminant-avoiding neighborhood the roots remain simple. Their interlacing order and negativity persist. The leading coefficients and the resultant remain nonzero.

Thus this is a neighborhood in the entire coefficient chart, not only an image of a selected root-parameter family, a polynomial locus, or a locus fixing infinity. Degenerate pairs, degree drops, and common factors are excluded by open conditions.

## Real fibers and ramification

For equal-degree real polynomials with distinct strictly interlacing roots, the residues

\[
 A_j=\frac{p(b_j)}{q'(b_j)}
\]

at the ordered poles \(b_j\) are nonzero and have a common sign. This follows directly by counting the factors of each sign on either side of each pole. The constant term of the partial-fraction decomposition is real. Therefore, away from the real axis,

\[
 \operatorname{Im}f(x+iy)
 =-y\sum_j\frac{A_j}{(x-b_j)^2+y^2}
\]

cannot vanish. A nonreal point is not a pole because every pole is real. Real projective points map to real projective points. These facts give exactly the real-fibered property, including the projective point at infinity.

The unramified assertion covers all real points:

- At a finite nonpole, \(f'(x)=-\sum_jA_j/(x-b_j)^2\ne0\).
- At a simple pole, the derivative in the target coordinate \(1/f\) is \(1/A_j\ne0\).
- At infinity, using the domain coordinate \(w=1/z\), the linear coefficient of \(f(1/w)\) is \(\sum_jA_j\ne0\).

There is no cancellation in either sum because the residues have one sign. Composition preserves real fibers and nonzero differentials at real projective points. This step handles intermediate iterates that may pass through infinity; an affine derivative product alone would not have been sufficient there.

## The argument for every period

Homogeneous composition is the appropriate way to iterate. If both forms have strictly positive coefficients in every degree, substituting another such pair produces forms with strictly positive coefficients in every resulting degree. Their leading and constant coefficients in the affine chart are positive.

No common projective zero can arise under composition: if an iterated pair vanished simultaneously at a projective point, either the preceding pair would already vanish there or its projective image would be a common zero of the outer pair. Both alternatives are excluded. Thus the \(n\)th iterate \(g=f^n\) has exact degree \(e=d^n\), with coprime affine numerator and denominator both of degree \(e\).

Every pole of \(g\) is real by the real-fibered property, is simple by the unramified property, and is finite because the denominator has nonzero leading coefficient. There are precisely \(e\) poles. Their negativity follows from coefficient positivity: the denominator is positive on the nonnegative real axis.

On each of the \(e-1\) bounded intervals between consecutive poles, \(g'\) is continuous and nonzero, hence \(g\) is strictly monotone. Its two endpoint limits are infinite with opposite signs. Equal infinite signs would contradict monotonicity and a finite value in the interval. Therefore \(g(x)-x\) changes sign and has a real zero in each interval.

There is also a positive real fixed point: \(g(0)>0\), the denominator is nonzero for positive \(x\), and \(g(x)-x\to-\infty\) as \(x\to+\infty\). This positive root is distinct from every root obtained between negative poles.

The fixed-point polynomial \(p_n(z)-zq_n(z)\) has exact degree \(e+1\). The preceding argument gives at least \(e\) distinct real roots, hence at least \(e\) roots counted with multiplicity. If any nonreal root existed, its conjugate would also be a root, requiring at least \(e+2\) roots counted with multiplicity. This contradicts the degree. The argument does not assume that all fixed points are simple.

Poles are not spurious polynomial roots because the numerator and denominator are coprime. Infinity is not fixed by \(g\), since its image is the finite positive quotient of leading coefficients. Consequently every projective fixed point of every positive iterate is real. Taking all integers \(n\ge1\) proves the entire periodic-point assertion. There is no finite-period cutoff or unproved inference from fixed points of the original map alone.

This is a self-contained verification of the known construction sufficient for the exact question. It does not require accepting all unrelated assertions in either preprint, or invoking the classification of Julia sets to justify this particular family.

## Independent controls and exclusions

The author program was copied and rerun outside the author directory. All **51 assertions pass**, and its result is byte-identical to the submitted JSON.

The independent program passes **848 exact assertions**. It tests 30 base or perturbed degree-two/three maps, including both signs of every individual coefficient-chart direction and simultaneous multi-coordinate perturbations. It checks strict negative root locations using exact real-root counting, coprimality, positivity, real simple poles, finite real critical-point exclusion, the derivative in the infinity chart, and all fixed roots for 60 iterated-map cases. A separate degree-two third-iterate check goes beyond the submitted second-iterate tests.

A negative control uses \((z^2-1)/(2z)\), a real-fibered map whose finite fixed-point equation is \(-(z^2+1)=0\). Thus real fibers alone do not imply the conclusion. The positive-coefficient condition supplies essential information in the audited construction. Finite computations serve only as controls; the all-degree and all-period proof is the argument above.

The three primary-source PDF hashes and sizes match the author's manifest. No source PDF is needed in the publication package. The modest source search found no verified journal publication; it is not an exhaustive publication-history investigation.

## Disposition

Recommend **already_solved** for 30004438, explicitly credited to **Khazhgali Kozhasov and Mario Kummer (2020 preprint)**. The imported assessment that only lower-dimensional families were known is contradicted by the cited first version and by the independently verified ambient-open construction. This is a correction of a dated source assessment, not a new discovery by the campaign.

The conclusion does not say that the entire real-periodic locus is open, that every Chebyshev map is an interior point, that the Hermite conjecture is settled, or that an analogous higher-projective-dimensional question is solved. No mandatory revision to the frozen source correction remains.
