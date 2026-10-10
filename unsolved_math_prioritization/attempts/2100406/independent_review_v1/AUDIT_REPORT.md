# Independent audit: 2100406 / AMR-020-0406

Date: 2026-10-03 UTC. Verdict: **PASS, for the literal unrestricted question only.**

The frozen certificate supplies a valid nonelliptic billiard satisfying its stated hypothesis. The decisive existence result is classical and belongs to Lazutkin. Classify this as a **credited, source-derived negative answer to the literal wording**, not as a new research solution or a settlement of a rational/resonant variant. There is no mathematical HOLD. No remote write or new author search was performed.

## Freeze and audit independence

The certificate SHA-256 is `4e47a382af31327e0d04b70f270000cf9ecd2a9ceedf4e6fc1d7d24b2703a3bf`; the author-manifest SHA-256 is `1477830577f747618a6e083148c747d1873f0e77ca55d4146c345d59622a6810`. Both match the assignment. All six author-manifest file lengths and hashes match. The author directory was not edited.

I independently opened the three versions of the target and the original Lazutkin paper, read the relevant theorem and definitions, checked the written geometry and accumulation argument, and reran the exact controls. The three cached PDF hashes also match the source manifest. The audit does not certify the live catalogue detail page or historical priority for explicitly noticing this consequence.

## 1. Source identity and scope

The target is Question 3.10, printed p.22, in [arXiv v1](https://arxiv.org/pdf/1804.03737v1), and Question 4.10, printed p.17, in [arXiv v2](https://arxiv.org/pdf/1804.03737v2). The [published article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6158379/) also labels it Question 4.10. All ask about convex caustics with rotation numbers having an interior limit, without a rationality or periodicity restriction.

The section discusses rational caustics, but does not declare all subsequent caustics rational. The neighboring questions explicitly use rational or rotational language; the target does not. Its reference to Innami also does not impose an additional hypothesis. The section-wide smooth, strictly convex planar-table assumptions are met. No analytic-caustic, prescribed-limit, foliation, or family-regularity requirement appears in the question. Even an analytic-boundary requirement would not exclude the example.

The catalogue label Question 4.6 is wrong: that published problem concerns local conjugacy near a two-periodic orbit. The target is attributed to a suggestion by Vadim Kaloshin. None of this establishes what the proposers intended beyond the printed wording.

## 2. Classical theorem audit

The [original Lazutkin paper](https://www.mathnet.ru/php/getFT.phtml?jrnid=im&option_lang=eng&paperid=2221&what=fullteng), Math. USSR-Izv. 7 (1973), 185–214, was read beyond its abstract. Page 185 defines closed convex caustics and assumes positive bounded curvature radius. Page 186 defines the Diophantine set E(a), estimates its Lebesgue measure in (0.3), and explicitly identifies its elements with rotation numbers. Theorem 1, p.187, supplies C^r caustics for those parameters. Pages 188 and 191 verify envelope convexity through condition (1.10). This is rotation-parameter measure, and the admitted parameters are irrational.

Fixing sufficient finite r, for example r = 2, is enough here; one C-infinity family is unnecessary. The analytic table satisfies every finite differentiability requirement. Retrieved OCR degrades displayed exponents, so this audit does not transcribe the numerical threshold or the coefficient/exponent in (0.3). PDF screenshot retrieval failed; the theorem's text was successfully retrieved.

As an independent precision check, p.515 of [Koudjinan–Ramírez-Ros](https://doi.org/10.1017/etds.2025.10248), ETDS 46 (2026), 514–542, explicitly states the positive-measure Diophantine rotation set in (0,1/2) and existence of a caustic for each parameter, crediting Lazutkin. This matches the parameter meaning in the original theorem. The proof does not depend on a claim merely about planar or phase-space area.

## 3. Explicit table and nonellipse audit

For h(theta) = 1 + cos(3 theta)/16 and X = h n + h' t, differentiation gives

- h + h'' = 1 - cos(3 theta)/2, globally between 1/2 and 3/2;
- X' = (h + h'') t, so the curve is regular and its curvature is positive;
- X(theta) dot n(theta) = h(theta).

The certificate's global support argument is correct. For a fixed normal angle theta, the derivative of X(u) dot n(theta) is (h(u)+h''(u)) sin(theta-u). It is strictly negative and then strictly positive on the successive open half-periods. Hence X(theta) is the unique support maximizer. This proves embeddedness and strict convexity, rather than inferring those global properties from local curvature alone. The positive lower bound on h puts the origin inside.

The arclength change has positive analytic derivative, hence analytic local inverse; the curvature radius is analytic as an arclength function. All finite smoothness requirements of the classical theorem are satisfied.

The translation issue is fully resolved. If the body were centrally symmetric about c, h(theta)-c dot n(theta) would be pi-periodic, so h(theta)-h(theta+pi) would contain only the first sine and cosine harmonics. Its actual value is cos(3 theta)/8. Taking the third cosine coefficient produces pi/8 = 0, a contradiction. Every translated or rotated ellipse is centrally symmetric. The argument therefore excludes every ellipse, not just an origin-centered ellipse. Constant width two, also verified by the controls, supplies another compatible geometric check; it is not needed.

## 4. Accumulation audit

Let R be the positive-measure set of admitted rotation numbers for this single fixed table. The compact intervals K_m = [1/m, 1/2-1/m], m >= 5, cover (0,1/2). Countable subadditivity therefore guarantees positive measure for R intersect K_m for some m. That set is infinite, and Bolzano–Weierstrass yields distinct rotation numbers converging to a point of K_m. Both interval endpoints are strictly inside (0,1/2), so accumulation only at zero cannot be the outcome.

The caustics are distinct because, after fixing orientation, a caustic has one rotation number. Their existence does not require a foliation or convergence in a geometric function-space topology. The optional stronger selection of a nonisolated point belonging to R is also correct: isolated points of a subset of the real line are countable, whereas R is uncountable. Thus the certificate can even choose an irrational interior limit, although that refinement is unnecessary.

## 5. Controls and source corrections

The independent execution of verify_geometry.py passes all 13 exact assertions. These are supplementary identity checks, not a computational replacement for convexity, Lazutkin's theorem, or the infinite-sequence argument. The global curvature bounds use the elementary global cosine bound, not just the two endpoint tests in the script.

The imported arXiv:1806.08849 citation is unrelated: it is Matei Mandache's [arithmetic-progressions paper](https://arxiv.org/abs/1806.08849). The source article credits Innami for the endpoint result and Arnold–Bialy for a simpler proof. [arXiv:1708.04280](https://arxiv.org/abs/1708.04280) verifies the Arnold–Bialy authorship and Pacific J. Math. 295 (2018), 257–269 reference. An endpoint limit 1/2 is outside the target interval and is not a solved special case of its literal hypothesis.

The certificate already carries these source corrections. No blocking correction is required. A nonblocking editorial improvement is to state the classical input as sufficiently differentiable convex caustics, or C^2 caustics, to avoid reading the word smooth as a claim about one C-infinity family derived solely from the finite-r statement.

## 6. Permitted classification and release condition

**PASS: already_solved / credited literal negative consequence of Lazutkin**, with the mandatory qualification **unrestricted convex-caustic rotation numbers; rational/resonant variants unaddressed**. The reported zero author-turn accounting is consistent with a literature-gate deduction; this mathematical audit is not a separate accounting investigation.

Preserve that qualifier in any queue or release description. Do not claim an author-issued correction, historical recognition of this exact question as solved, an explicit preassigned value of the limiting rotation number, or any result for rational/resonant sequences. Do not infer the intended strengthened question. These scope restrictions are material to the PASS.
