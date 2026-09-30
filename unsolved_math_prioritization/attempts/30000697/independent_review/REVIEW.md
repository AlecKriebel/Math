# Independent review: two-atom Upsilon injectivity

**Verdict: PASS_COMPLETE_TWO_ATOM_CLASSIFICATION_WITH_GENERAL_TARGET_OPEN.** No mandatory correction was found. The submitted artifact completely classifies the positive two-atom case on the full Lévy domain, including both endpoints and every positive dimension. The original question for arbitrary dilation measures remains **unsolved, 2/5 approaches**. The negative answer to the particular imaginary-Mellin-line converse is already implied by the credited 2009 theorem.

Reviewed artifact: PARTIAL_RESULT.md, SHA-256 `e4c51feb408015a7777b774b2464b9f9dddc9f0c2f5fe6fb1f56e9f4ff799dcf`.

Reviewer: a separate GPT-6 Astra agent, reasoning effort xhigh. This is an adversarial AI audit, not human peer review. No priority claim is certified. The author’s mathematical file was not modified.

## 1. Exact source and domain

I read the original Rosiński contribution on printed pp.439–440 of [Oberwolfach Report7/2007](https://ems.press/content/serial-article-files/46095?nt=1) and visually inspected p.440. The definition uses dilation by a positive scalar: the integrand is rho(A/t). Its Mellin convention is M_gamma(z)=integral t^(z−1) gamma(dt), and the proposed sufficient condition concerns zeros at z=1+iu with nonempty interior. The question about its converse is stated explicitly. The artifact uses this shift correctly.

The source’s Lévy domain initially consists of all sigma-finite positive inputs whose output is a Lévy measure. It is not permissible simply to assume that the inputs were finite. For a positive two-atom kernel, however, the author correctly proves that this full domain is exactly the class of Lévy measures. The aI output term controls the weighted input integral, and dilation by c preserves its finiteness because min(1,c²||x||²) is bounded by max(1,c²) min(1,||x||²). Normalizing atoms s<t by the invertible dilation D_s is also valid.

This agrees with Theorem3.4 of [Barndorff-Nielsen, Rosiński and Thorbjørnsen, General Upsilon-transformations](https://alea.math.cnrs.fr/articles/v4/04-07.pdf), ALEA4(2008),131–165: finite gamma with finite second moment gives the full Lévy class in every dimension. I also checked the start of Section6, its multiplicative cancellation formulation, and Proposition6.2’s dimension reduction. The Aarhus report is a version of this same work, not another independent source.

The web renderer failed to refetch two of these PDFs, but their complete locally cached primary PDFs and extracted texts were available and inspected. The source hashes match the author’s manifest. This is not a full audit of all proofs in the 35-page general paper.

## 2. Independent analytic audit of the classification

Put q=b/a and E={1≤||x||<c}. The sets c^jE, j in the integers, form a disjoint Borel partition of the punctured space. Their half-open boundary convention matters: it prevents atoms on sphere boundaries from being counted twice.

For two inputs with equal transforms, their difference is used only as a signed locally finite measure on the punctured space. On each annulus its Jordan variation is finite. This avoids subtracting infinite masses on sets accumulating at zero. Its variation is dominated locally by the sum of the two inputs and has finite integral against min(1,||x||²).

Pulling the signed restriction on c^jE back to E gives finite signed measures eta_j satisfying a eta_j+b eta_(j−1)=0. Thus eta_j=(−q)^j eta_0 for positive and negative j. Because dilation is a Borel bijection, variation is transported exactly, and each annular mass is q^j m with m=|eta_0|(E). There is no angular cancellation loophole: m is total variation, not signed total mass.

If m>0, the large-radius annuli require q<1. On the small-radius annuli the quadratic weight is at least c^(2j), so their contribution requires c²q>1. These conditions are simultaneously equivalent to b<a<bc². Equality at either endpoint produces a nonzero constant term in one of the two divergent geometric tails. Thus both endpoints are genuinely injective. If m=0, every annular restriction vanishes; equality of the original positive measures follows by their common countable partition.

Conversely, for 1/c²<q<1, the bilateral orbit measure with coefficient (−q)^j at c^j e has finite weighted total variation. Its Jordan halves are distinct positive Lévy measures. At each output atom the coefficient cancellation is a(−q)^j+b(−q)^(j−1)=0. Each atom has finite mass, and both positive outputs are supported on the same countable set, so atomwise equality proves equality on every Borel set by countable additivity, even when both values are infinite. No global subtraction of infinity from infinity is used.

The proof works in every d≥1 by choosing any unit vector e; the necessity argument already treats all angular distributions. It imposes no density, absolute continuity, finite total mass, or extra finite-moment requirement. The excluded degeneracies a=0, b=0 and c=1 are outside the stated assumptions and do not create endpoint problems.

The finite-input statement is also correct: finite total variation would require both tails of sum_(j in Z)q^j to be summable, impossible for every q>0. This neatly identifies why finite-measure Fourier cancellation cannot establish the full-domain result.

## 3. Mellin-line counterexample and prior attribution

For gamma=2 delta_1+delta_2, the original source’s imaginary-line transform is 2+exp(iu log2), whose modulus is at least one. Nevertheless, the two-atom criterion gives noninjectivity because 1<2<4. The explicit alternating orbit measures have infinite total mass near zero but finite quadratic small-jump integral. This is fully admissible for the source’s domain.

I checked Theorem2.1 and its noncancellation proof in [Jacobsen, Mikosch, Rosiński and Samorodnitsky, arXiv:0712.0576v2](https://arxiv.org/abs/0712.0576), including equations(2.3)–(2.6). The current arXiv page lists v2, revised4March2009, with Annals of Applied Probability19(2009),210–242 and DOI10.1214/08-AAP540. The retrieved PDF identifies the published article but notes typographical/pagination differences from the original journal; I did not compare it byte-for-byte with the journal PDF.

Taking alpha=1 and theta=pi/log2 makes the tilted integral 2+2 exp(i pi) vanish, while all neighboring tilted moments are finite. The densities x^−2 and (1+cos(pi log(x)/log2))x^−2 are distinct, positive, and Lévy integrable. Under dilation by2, the density multiplier is2 and the cosine changes sign, so the transform equality can also be checked directly. This verifies the prior implication independently of merely matching theorem statements.

That theorem’s cancellation is relative to a prescribed power-law reference measure. It is not silently promoted to a characterization of injectivity against all Lévy inputs for arbitrary gamma. The author’s no-novelty qualification and distinction between these quantifiers must be retained.

## 4. Reproduction and independent controls

The submitted verifier was copied and run with its frozen artifact in an isolated replay directory. All **42,782 assertions**, across512 parameter cases, passed; the generated verification.json is byte-identical to the submitted receipt. Its finite truncations correctly retain their two boundary residuals.

The independent checker passes **2,331 exact assertions**. In particular it uses signed seeds on three distinct rays in two dimensions, at two radial levels inside a fundamental annulus. It tests transported total variation, exact small- and large-radius weights, Jordan-half output equality on every interior orbit atom, both nonzero boundary residuals, scalar normalization, exact omitted-tail formulas and endpoint divergence. It also verifies the smooth oscillatory-density cancellation algebra and imaginary-line modulus bounds through rational unit-circle parametrizations.

These controls support the algebra; they do not prove the infinite measure statements by numerical exhaustion. Those statements are justified analytically in Section2 of this review.

## 5. Publication recommendation

Publish only as a scoped partial toward the original question, with queue status **unsolved, 2/5**. The positive two-atom classification is complete, including injective endpoints. The negative imaginary-line converse is credited prior work, with an elementary discrete certificate supplied here. No characterization for arbitrary sigma-finite dilation kernels, general continuous kernels, or three-or-more-atom kernels is established.

No mandatory mathematical, source-scope, or checker correction remains.
