# Independent source/application review: higher-genus skein torsion (10400080)

**Verdict: PASS_EXACT_CREDITED_HIGHER_GENUS_TORSION_RESULT. No mandatory correction.** The original existential question is answered by the credited Belletti–Detcherry examples. Recommend **already_solved, 0/5 new-discovery approaches**. The package correctly preserves integral coefficients and does not claim a new geometric construction or an explicit torsion representative.

Reviewed `KNOWN_RESULT.md`, SHA256 `ea7ac3b85f90ac300027a98c8a61ab10fe506c6647aec78f2a60bd88f8a727a0`. This is an independent gpt-6-astra xhigh source/application audit, not human peer review or an independent re-proof of the deep imported theorems.

All **1,675** submitted exact controls reproduce byte-identically. A separate standard-library implementation passes **9,803** exact algebraic assertions.

## 1. Exact original target and coefficient ring

I read the surrounding original section and visually checked [Ohtsuki, printed p.446](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf). It defines the Kauffman bracket skein module over Z[A,A^(−1)], using unoriented framed links and the empty link. Problem 4.2, attributed to J. Przytycki, asks whether surfaces other than incompressible tori and essential spheres can produce torsion. This is an existence question. It does not demand a classification, an explicit torsion link combination, or a universal assignment from every surface to a torsion class.

The neighboring Conjecture 4.3 is distinct. Nothing in this package settles it. A sphere bounding a ball is not an essential-sphere obstruction; the artifact uses the intended essential-surface convention when excluding low-genus surfaces.

## 2. Credited theorem coverage and publication access

I checked the complete [Belletti–Detcherry 2024 preprint](https://arxiv.org/abs/2406.17454v1), especially Theorem 2.1, Corollary 3.1 and Proposition 3.2 with their proofs. Corollary 3.1 explicitly supplies torsion in closed hyperbolic manifolds with positive first Betti number and examples excluding incompressible surfaces below an arbitrary genus bound. Proposition 3.2 is the credited geometric existence input. Taking the bound at least one removes essential spheres and tori.

The primary [IMRN record](https://academic.oup.com/imrn/article/2025/21/rnaf333/8315094) verifies publication on 5 November 2025, Volume 2025, Issue 21, article rnaf333, and describes torsion over the same integral Laurent ring. The full final typeset article was not obtained or compared line by line; the complete preprint is the text actually audited. This access limit is disclosed in the submitted package and does not turn the known theorem into a new campaign claim.

I also checked the introduction of [Kalfagianni's August 2026 preprint](https://arxiv.org/html/2608.12668v1). It expressly attributes the earlier irreducible, atoroidal examples to Belletti–Detcherry, specifically their Proposition 3.2 and Corollary 3.1. Its stronger claims about selected surface families are unnecessary here and were not imported or certified by this review.

## 3. The integral dimension-jump argument is correct

The reconstruction avoids an important localization error. A relation among v_i after tensoring with Q(A) need not already hold in the original module. After clearing coefficient denominators, a further nonzero Laurent polynomial s is needed to annihilate the resulting localization-kernel element. The candidate supplies exactly that multiplier.

Now factor the maximal common power of h=A+1 from the actual relation coefficients. This is legitimate in the integral Laurent ring: evaluation at A=−1 has kernel (A+1), and A is a unit. At least one remaining coefficient has a nonzero integer value at −1. Rational independence of the specialized v_i then makes their corresponding combination v nonzero in the rational specialization, hence nonzero in the original module.

The actual relation says h^e v=0. If e were zero it would contradict this nonzero specialization. Taking the least annihilating positive exponent yields a nonzero element killed by h itself. This is genuine integral (A+1)-torsion, not merely a class appearing after scalar extension. The argument requires neither finite generation of the original module nor injectivity into its fraction-field localization.

The displayed R plus R/(h) diagnostic correctly demonstrates why the additional localization annihilator cannot be skipped. Integer coefficient content must also be preserved; dividing by arbitrary nonunits in Z would be invalid, and the proof does not do so.

The general preprint theorem is phrased with a complex specialization parameter. This package only needs the integral factor A+1, for which the divisibility and evaluation argument above is completely explicit. No assertion about a nonintegral linear factor being an element of Z[A,A^(−1)] is made.

## 4. The specialization has arbitrarily large rational dimension

Positive first Betti number gives an epimorphism of the fundamental group onto Z. The diagonal SL_2 family with eigenvalues z^phi and z^(−phi) is therefore available. A loop mapping to one can be represented by an embedded framed knot in a 3-manifold, and disjoint parallel copies exist in its tubular neighborhood.

The trace evaluation at A=−1 respects the skein relations with the stated signs: the empty link is one, a trivial component contributes −2, and the crossing relation is the SL_2 trace identity. Reversing a component leaves its trace unchanged. A framing twist contributes −A³, which becomes one. Thus there is a well-defined evaluation of the rational specialization into Laurent polynomial functions of z.

The j parallel copies evaluate to (−z−z^(−1))^j, with leading coefficient (−1)^j at z^j. Distinct j therefore give linearly independent Laurent polynomials over Q. This proves independence of arbitrarily many specialization classes. It needs only the classical trace evaluation, not an identification of every nilpotent or scheme structure in a character variety.

## 5. Generic finiteness has the right hypotheses and parameter

The full published [Gunningham–Jordan–Safronov article](https://doi.org/10.1007/s00222-022-01167-0), Inventiones mathematicae 232 (2023), 301–363, was available. Theorem 1 on p.302 states finite dimension over Q(A) for the skein module of every closed oriented 3-manifold. Theorem 5.8 gives the general group-skein formulation; Corollary 5.9 explicitly returns to the Kauffman bracket case and identifies the parameter by q=A².

Thus no boundary-manifold theorem or wrong coefficient field is substituted. Applying this substantial known result together with the preceding independent specialization argument gives exactly the needed torsion. This review checks the statement, coefficient matching and application; it does not independently reconstruct the categorical and deformation-quantization proof of generic finiteness.

## 6. Geometric existence and higher genus

I read Proposition 3.2 and its construction in the full Belletti–Detcherry source. It uses a high-distance Heegaard splitting with Torelli gluing, preserving first homology of rank equal to the chosen Heegaard genus. The free choice of that genus can be made strictly larger than the requested Betti bound. This supplies the strict inequality even though the displayed construction uses a weak inequality in its intermediate choice.

I checked the cited primary distance statements in [Hempel, Theorem 2.7 and its proof](https://arxiv.org/abs/math/9712220), and [Hartshorn, Theorem 1.2](https://msp.org/pjm/2002/204-1/pjm-v204-n1-p05-p.pdf). Hartshorn's irreducible Haken hypothesis is not omitted: an essential sphere forces Heegaard distance zero, while the presence of an orientable incompressible positive-genus surface in an irreducible manifold places it in the Haken setting and bounds distance by twice that genus. Taking sufficiently large distance excludes the specified low genera. The measured-lamination, pseudo-Anosov and Torelli existence machinery remains part of the credited geometric proposition, rather than a new stand-alone construction in this package.

Positive b_1 in a closed oriented manifold gives nonzero integral H_2. An embedded oriented representative can be compressed, preserving its homology class, until its positive-genus components are incompressible. In these examples any sphere component bounds a ball and can be discarded without changing the class. Not all components can disappear, since the class was nonzero. Exclusion of essential tori then forces some surviving component to have genus at least two. Closedness excludes boundary-parallel alternatives.

This verifies that the witnesses genuinely have higher-genus essential surfaces and skein torsion while excluding the old sphere/torus sources. It does not supply an explicit surface-supported torsion formula. That additional mechanism remains separate from the source's existence question.

## 7. Exact controls and disposition

The submitted verifier was copied with its frozen artifact dependency and rerun, reproducing its 1,675-assertion receipt byte for byte. The independent checker verifies trace identities on integer SL_2 families, Laurent leading terms, integral quotient-module annihilators, survival under the Laurent unit A=h−1, the extra localization multiplier and minimal-exponent extraction. All 9,803 assertions pass.

Run `python author_replay/verify.py` and `python independent_checks.py` from this directory. These algebraic controls do not certify the imported quantum-algebra or high-distance geometric theorems; the report states precisely which published results are being used.

No correction is required. Publish as a **credited known affirmative answer**, already_solved and 0/5 new-discovery approaches, preserving integral coefficients, the existential scope, the imported geometric and finiteness dependencies, the final-typeset access qualification and the absence of a new-construction claim.
