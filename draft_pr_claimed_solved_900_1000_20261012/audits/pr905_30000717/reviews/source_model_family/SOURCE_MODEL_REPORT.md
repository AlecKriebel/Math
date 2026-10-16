# PR905 / 30000717 source and model adversarial report

Review completed 2026-10-13T04:31:14.928595+00:00. Scope: independent source/model adjudication of the frozen author candidate, not a complete historical-priority or proof audit.

**Verdict: SOURCE/MODEL PASS for a negative answer to the unrestricted four-way conjecture.** The candidate does not silently identify the catalogue tangency-minor ideal with the publisher's displayed product ideal: it names both and supplies an obstruction for both. Its attained Robinson example is within the unrestricted target. It addresses the exact radical clause and the all-positive-epsilon original-ideal clause. There is a **catalogue metadata repair** to record and a **historical intent/priority gap** to retain, detailed below. Neither is a gap in the candidate's coverage of the two explicitly defined mathematical models.

## Frozen inputs and independently authenticated source

The frozen inputs inspected are `author/PROOF.md`, `author/SOURCE_ASSESSMENT.md`, and `author/SOURCE_MANIFEST.json` under this audit's `original/unsolved_math_prioritization/attempts/30000717/`. Their exact file hashes, independent download hashes, rendered-page hashes, and private local source paths are in [SOURCE_HASHES.json](SOURCE_HASHES.json). No file in the frozen original was changed.

The publisher report was retrieved independently from [EMS Press's PDF](https://ems.press/content/serial-article-files/46100), also linked by [DOI 10.4171/owr/2007/14](https://doi.org/10.4171/owr/2007/14). It has 68 PDF pages, 559,967 bytes, and SHA256 `bd4f914a306afd73002d8c74f76e0c468113749240e90815a62ad151a53f783f`. This agrees with the candidate's hash. Complete printed pp.810-811 (one-based PDF pp.58-59) were rendered and visually inspected, including the formulas and surrounding text. Printed p.798 (PDF p.46), equation (2), was also visually inspected and confirms the candidate uses the classical Robinson sextic already credited in the report. Full PDFs, page images, extracted text, and the selected private dataset record are confined to ignored `private_sources/`; they are not incorporated into this report.

## Exact target and quantifiers

Theorem 1 on printed p.810 has four clauses: global nonnegativity; nonnegativity on the real gradient variety; exact SOS modulo the **ordinary radical**; and SOS for **every epsilon > 0** modulo the **original ideal**. It assumes that the global infimum is attained. Conjecture 2 on printed p.811 removes that assumption while replacing the gradient ideal. The display visibly lists separate cross-products with a comma and an ellipsis, rather than a subtraction sign. These observations come from the [publisher pages](https://ems.press/content/serial-article-files/46100), not from OCR alone.

Use `S = R[x,y,z]` and the candidate's definitions

- `J_f = (y f_x - x f_y, z f_x - x f_z, z f_y - y f_z)`;
- `K_f = (y f_x, x f_y, z f_x, x f_z, z f_y, y f_z)`.

The current selected dataset record uses `J_f` in its normalized statement, but its retained original statement describes the separate-product reading `K_f`. The exact problem identifier, OWR identifier, DOI, and rank agree with the frozen candidate. The live rank is 963. The dataset and catalogue hashes and lookup metadata are recorded separately; no dataset statement is redistributed here.

These are materially different ideals. Independently, for `f=x^2+y^2`, the two-variable minor ideal is zero whereas the separate-product ideal is `(xy)`. Thus inserting a minus sign is not merely changing notation. In general `J_f` is contained in `K_f`, because every minor is a difference of two generators of the latter. The candidate correctly retains the distinction.

## Why attainment does not disqualify the counterexample

Removing a hypothesis gives a claim for all objects previously allowed and any newly admitted ones. It does not require the negation of that hypothesis. Therefore a polynomial attaining infimum zero can refute this unrestricted equivalence after the ideal replacement. The source's nonattainment motivation does not supply a hidden restriction to exclusively nonattaining polynomials.

Robinson's sextic has infimum zero at the origin. The candidate claims `R >= 0` but

`R + epsilon` is outside `SOS + sqrt(L)` for every `epsilon >= 0`, for either `L=J_R` or `L=K_R`.

If its mathematical proof passes the separate proof audit, this is enough to settle the full four-way question negatively: at epsilon zero it disproves the proposed implication from global nonnegativity to the exact clause; at any positive epsilon it disproves the proposed all-epsilon clause, since `L` is contained in `sqrt(L)`. A negative resolution needs one failed implication, not a characterization of every implication. The candidate actually exhibits failures of both certificate implications.

No strict-positivity, genericity, coercivity, finite-variety, degree-bound, or isolated-singularity restriction appears in the target. The source/model audit therefore supplies no such restriction that could exclude the sextic. Its example does not purport to settle a different conjecture restricted solely to nonattaining polynomials.

## Ordinary radical, original ideal, and real vanishing ideal

The ordinary radical is not the same object as the real radical. The source uses the former in the exact clause. The candidate neither assumes equality nor computes a radical: if `h` is in `sqrt(L)`, some positive power belongs to `L`, hence `h` vanishes at every real zero of `L`.

Let `I_real(V(L))` denote all real polynomials vanishing at those real zeros. There are inclusions

`L ⊆ sqrt(L) ⊆ I_real(V(L))`.

By the real Nullstellensatz the last ideal is the real radical, but that theorem is unnecessary for the candidate's restriction argument. Its strengthened obstruction is explicitly against this entire vanishing ideal. Failure for that larger remainder ideal implies failure for both source remainder ideals. This direction is correct: enlarging the allowed ideal enlarges the certificate cone, so excluding the larger cone excludes the smaller ones.

The SOS summands can depend on epsilon, and there is no fixed degree or summand-count limit. The candidate's argument fixes an arbitrary epsilon and arbitrary finite polynomial SOS certificate. Its line restrictions handle nonzero constants when epsilon is positive. Adding epsilon also leaves the derivatives, and therefore either candidate ideal, unchanged. Thus it does not substitute a perturbed-gradient model or a finite numerical relaxation for the quantified target.

For the minor reading, sphere minimization verifies the nonnegativity-on-variety clause captures negative global values; hence Robinson has both nonnegativity clauses true. The separate-product variety has no corresponding general sphere-minimum property. The candidate's additional nonattaining `Q` example addresses this distinction independently; it is unnecessary for the main Robinson refutation.

## Related primary results use different certificate cones

The independently downloaded [Schweighofer author manuscript](https://www.math.uni-konstanz.de/~schweigh/publications/tentacle.pdf), dated 17 May 2006, has SHA256 `c7ad169bfcc28857ae3df6c244742b02a4487e216d4dccb08fdc89010bf661e3`. Theorem 25, Open Problem 33, and Theorem 46 were visually inspected on manuscript pp.13-14, 16, and 21. Their certificates include an SOS multiplier of a gradient-tentacle inequality. Open Problem 33 concerns dropping infinity/compactness hypotheses for that principal-tentacle theorem. These are not the ideal-only four-way target. No inference that the Robinson obstruction settles Open Problem 33 is licensed.

The independently downloaded [Guo, Safey El Din, and Zhi author-hosted primary paper](https://perso.lip6.fr/Mohab.Safey/Articles/gcv_sos.pdf) has SHA256 `961a29e7a5b64420b3129b4fba3361c96471060ad03cf9232185eef9de019eea`. PDF p.2 was visually inspected. It defines tangency minors and the truncated set by `M-f >= 0`, with `M` in the polynomial's real image, and states the credited truncated-tangency theorem with an additional SOS multiplier `t(M-f)`. That multiplier and truncation cannot be removed when comparing models. On the Robinson axis, truncation bounds `R=t^6` above; the candidate's unrestricted-axis contradiction cannot simply be transferred to that bounded set. The displayed theorem's abbreviated wording about `M` is read together with its preceding definition, not as a theorem for arbitrary real `M`.

The [2008 SIAM publisher record](https://epubs.siam.org/doi/10.1137/080719212) confirms the truncated-tangency article, pages 941-951, and its September 11, 2008 online publication. The requested publisher PDF redirected to an abstract/access page. Its full article was not independently inspected in this review. The 2010 primary paper is adequate evidence for the model distinction just described; it does not replace a future full priority audit of the 2008 result.

## Repair, remaining gaps, and promotion boundary

1. **Metadata repair:** the live dataset's `statement_verification` characterizes the normalization as preserving the source-level claim and labels it `corrected_verified`. The product/minor difference is not justified by the printed report. The candidate already flags this correctly; no proof repair is needed for its two-model theorem. Any catalogue repair must preserve evidence of the discrepancy instead of silently treating the source display as verified minors.
2. **Historical-intent gap:** an author-approved correction of the publisher's display was not verified. The accurate claim is a refutation of the catalogue minor formulation and the explicitly defined literal separate-product interpretation. A claim about a further intended formulation would require new primary evidence.
3. **Priority gap:** this review identifies surrounding models, not novelty of the zero-line/axis application or exhaustive literature coverage. Robinson and its ten-zero obstruction are classical ingredients. Candidate mathematical validity and historical novelty require separate judgments.

The strongest source/model conclusion is that the frozen candidate is aimed at the right unrestricted certificate question under both formulations presently evidenced. The source/model family has completed its assigned checks at **100%**, while historical intent and full priority remain expressly outside this family's completion claim.
