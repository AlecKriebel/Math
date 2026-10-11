# Independent source and mathematical audit: 30000703

**Verdict: PASS for `already_solved` on the exact unrestricted-limit formulation.** The conclusion is a credited application of the Kraus–Roth–Ruscheweyh reflection theorem, not a new result. No mandatory mathematical correction was found.

- Date: 30 September 2026
- Reviewer: separate gpt-6-astra worker, xhigh
- Artifact: `SOURCE_STATUS.md`
- Frozen SHA-256: `7690840787fd9be528beb649dc6db4b77bc637867720765812ec4cb31d5a73ba`
- No author mathematics or source files were edited
- The full 2007 journal proof was not available and is not independently certified by this review

## 1. Exact primary statements and quantifiers

I read the original OWR contribution and visually inspected printed pp. 528–529. Problem 1 prints an ordinary limit as z approaches 1, with no radial or non-tangential restriction. The preceding Theorem 1 explicitly equates a positive unrestricted liminf of the displayed hyperbolic distortion at every point of an open boundary arc with holomorphic extension across that arc mapping it into the unit circle. It also equates these conditions with the distortion tending to one at every arc point. The neighboring Problem 2 concerns a different conformal-metric boundary-regularity question and is not part of the selected target.

Source: [original OWR contribution](https://ems.press/content/serial-article-files/46093), pp. 528–530.

The exact one-point conclusion is independently explicit in [Gumenyuk–Kourou–Moucha–Roth, arXiv:2410.13965v1](https://arxiv.org/abs/2410.13965v1), Section 8.2, p. 31, equation (8.3). I visually checked that page. The current unversioned arXiv record lists only v1, 17 October 2024. The subsequent angular-distortion discussion is explicitly different: equation (8.4) concerns non-tangential convergence and weak conformality, while the finite-angular-derivative conclusion needs an additional condition. Definitions and Theorems 1–2 are consistent with this separation. The source correction does not confuse either of those weaker hypotheses with the unrestricted one.

The [2007 publisher record](https://link.springer.com/article/10.1007/s11854-007-0009-x) confirms Daniela Kraus, Oliver Roth and Stephan Ruscheweyh, Journal d'Analyse Mathématique 101, 219–256, DOI 10.1007/s11854-007-0009-x. It displays subscription-preview material rather than the complete article. The review imports the established theorem as precisely stated in the primary OWR source and credited in the later paper. It does not infer the theorem merely from a publisher abstract, nor claim to have reconstructed its 38-page proof.

## 2. The point-to-arc step is valid

The central quantifier argument is correct. An unrestricted limit of the distortion to one gives a uniform lower bound, say one half, throughout the intersection of the disk with some Euclidean ball centered at 1. A smaller unit-circle arc lies strictly inside that ball. For each fixed point of that arc, every sufficiently close point in the disk lies in the original ball. Its unrestricted liminf is therefore at least one half, so the cited arc theorem applies.

There is no interchange of a pointwise limit with a uniform limit over an arc. The uniform lower bound is furnished directly by the single unrestricted limit, and only this lower bound is transferred to neighboring points. The resulting reflection theorem supplies the stronger limits afterward. The same argument works from a strictly positive unrestricted liminf at 1.

Conversely, holomorphic continuation across an open arc mapping it into the unit circle is exactly one of the equivalent hypotheses in the imported theorem, so it implies the original distortion limit. Thus the package records an equivalence for the literal target.

A radial segment or a fixed Stolz region does not contain full interior neighborhoods near neighboring boundary points. Such restricted convergence cannot supply this argument's hypothesis. The artifact accurately identifies this distinction rather than silently strengthening an angular assumption.

## 3. Boundary derivative and reflection formula

The extension gives f(1)=eta on the unit circle and the unrestricted boundary value. Nonvanishing of the boundary derivative is not assumed.

Choose a small neighborhood where the continued function is nonzero. The function u=−log|f| is harmonic, strictly positive on the disk side, and zero on the boundary arc. The strict positivity uses f(D) contained in D, and the initial distortion condition excludes a constant function. The unit-circle boundary is smooth and satisfies the interior-ball condition. Hopf's boundary point lemma consequently gives a positive inward derivative of u, equivalently a positive outward derivative of log|f|.

Differentiating the boundary identity |f(e^(it))|=1 at t=0 makes conjugate(eta)·f'(1) real. The preceding normal derivative equals its real part and makes it strictly positive. This proves the stated alpha>0, Taylor expansion and local conformality. It does not assert alpha=1 or global injectivity.

After shrinking the neighborhood to avoid zeros, circle reflection yields the displayed reciprocal-conjugate formula. Both sides agree on the arc and give the same holomorphic continuation. The possibility of zeros or singularities elsewhere on the circle does not interfere with this local statement.

## 4. Sharpness controls

For f(z)=z², the distortion is 2|z|/(1+|z|²), tending to one at 1. This is a proper disk self-map but not an automorphism, so the local theorem cannot be promoted to a disk-automorphism conclusion.

For f(z)=exp(−(1−z)/(1+z)), the Cayley transform has positive real part u=(1−|z|²)/|1+z|² in the disk. Thus f maps the disk strictly into itself. Its derivative gives distortion u/sinh(u), and u tends to zero under unrestricted approach to 1. The function extends holomorphically near 1 and has derivative 1/2 there. At −1, the exponent has a genuine pole, so the exponential has an essential singularity. It is not a finite Blaschke product and does not extend over the whole unit circle.

The examples satisfy the original hypothesis and the claimed local conclusion. They are controls on overstrong conclusions, not counterexamples to the reflection theorem.

## 5. Reproduction and disposition

The submitted verifier was copied before execution. All **69** exact assertions pass with SymPy 1.14.0, and the regenerated receipt is byte-identical to the original.

The independent checker passes **187** exact assertions. It checks powers z^k, rational circle-neighborhood geometry, the reflection identity for the Cayley transform, the parameter family exp(−a(1−z)/(1+z)) for several positive rational a, its derivative a/2, and the associated distortion formulas and limits. These are finite symbolic controls. They do not prove the imported reflection theorem or replace the analytic Hopf argument.

**Required corrections: none.** `already_solved` is appropriate for the exact selected unrestricted condition, with credit to the known theorem and with no campaign discovery or priority credit. Retain the full-journal-PDF access qualification. No conclusion is certified here for a radial-only hypothesis, an unspecified alternative intended question, or the adjacent boundary-set regularity problem.

The six publication files are `REVIEW.md`, `verdict.json`, `submitted_verify.py`, `verification.json`, `independent_checks.py`, and `independent_results.json`. The independent checker is self-contained and does not require a source snapshot. If the frozen artifact's administrative review sentence changes, link the final hash with an exact diff.
