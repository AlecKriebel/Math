# Independent scope and primary-literature review — Zenodo 23191301

Completed: 2026-10-25T01:46:14.779172+00:00  
Completion: 100% of the assigned acquisition/scope/content review. This is not a mathematical gate.

## Conclusion

No publication-scope or attribution defect was identified at the exact stated scope. The candidate page is suitable for consideration **only after the independent analytic and adversarial gates**. The important claim is fixed-exponent nonconvexity for real homogeneous sextics: an explicit cube example in 3 · 10^62 variables and an existence statement in some finite n(q) for each odd q ≥ 3. It is neither a ternary result nor a uniform-in-q dimension theorem. No worldwide-firstness claim is justified by this bounded review.

The most interesting point is that separate copies of one classical polynomial each have an SOS cube, but their average eventually does not. This is compatible with the known convexity of the union over odd exponents because that earlier statement increases the exponent.

## Published edition and complete coverage

The reviewed bytes are the freshly acquired public record 23191301, concept 23191300, DOI 10.5281/zenodo.23191301. Zenodo reports version 1.0 and publication date 2026-10-06; the six-page manuscript prints “6 October 2026” without a version number. These are separate metadata facts, not an inferred printed edition. The public API record was retrieved at 2026-10-25T01:42:02.070006+00:00.

- odd_power_sos_nonconvexity.pdf: 92,284 bytes; SHA-256 78930bbd8e727df2de0ca64ac3b5994a7e3392a289bd9058a4fc8dce02fd9e66.
- odd_power_sos_verification.zip: 28,376 bytes; SHA-256 680fb649cc1288684611fd2767334c5c9d9b62f8be086441319539704551033c.

Both files match the live MD5 and size, the inventory hashes and final local hashes. All 13 safe ZIP members match the archive CRC and original SHA-256 after review. No extra or embedded reader PDF exists. Original assets and extracted sources are unchanged. Receipts, extraction map and reader map remain under sources/; final recheck is final_source_verification.json.

Read all six actual PDF pages and complete paper.tex. Printed p.1 gives the exact cone and theorem; p.2 gives the finite product/partition obstruction and begins separation; p.3 completes separation, gives the exact classical seed and moment table; p.4 gives the local Schur certificate and finite cubic calculation; p.5 completes the sign, limits and disclosure and begins the credited cube identity; p.6 completes the identity and bibliography. The p.3 visual check confirms that the two large degree-six moments are 2^24, not the plain-text extraction's ambiguous “224”.

Complete verifier source was inspected, together with the moment table, initial blocks and all Schur-extension certificate fields. **This scope reviewer did not run either verifier and makes no mathematical PASS claim.** Authored expected output and historical check totals are not evidence of a fresh run. Analytic positivity, exact arithmetic reproduction, falsification controls and mathematical promotion remain the separate reviewers' responsibilities.

## Exact hypotheses and boundaries

C(n,m,q) uses real homogeneous forms, positive even m and positive odd q; SOS means a finite sum of squares of real polynomials. For odd q, f^q being SOS already implies f ≥ 0. “Cone” means closed and nonnegatively scaling-stable here, not an assumption of addition or convexity. In this paper n counts variables, not the dimension of the coefficient vector space.

The seed is p = x^4 y^2 + x^2 y^4 + z^6 − x^2 y^2 z^2, with coefficient 1 on the negative term. It is not the coefficient-3 original Motzkin polynomial, whose stubbornness is discussed in the primary literature. Each disjoint copy has an SOS cube by a credited identity, and p^q = p^3 (p^((q−3)/2))^2 extends membership to all odd q ≥ 3.

For each fixed q the proof selects a separating functional through degree qm = 2d, positive on squares of degree at most d and negative on p. Its finite product is positive on the required global squares because the total-degree moment matrix is a principal submatrix of a tensor product. Expansion over set partitions has leading term L(p)^q s^q < 0; collisions have lower degree. This is an analytic claim for arbitrarily large but finite s, not an infinite product measure or a numerical enormous-matrix computation. Degree-bounded square summands suffice because their highest homogeneous sums of squares cannot cancel.

The cube certificate is local to three variables through degree 18. Its 220 monomials split into eight parity blocks. The supplied table sets L(p) = −1, L(p²) = 11292 · 10^53 and L(p³) = 35039520 · 10^116. The stated cubic formula and bound give a negative value at N = 10^62 if the local positivity certificate is established. The q-general proof obtains a fresh functional rather than extrapolating this degree-18 table outside its domain.

A finite average outside a cone disproves convexity. The least-failing-prefix comment only gives existence of a violating pair in the same ambient space; it does not assign an SOS power to any prescribed untested prefix. Positive scaling transfers the sum obstruction to the average. Adding unused variables preserves the obstruction by restriction.

Explicit limits retained in content.json: no ternary theorem; no minimum or small prescribed dimension; no common dimension for all q; no full degree/dimension/exponent classification; no failure of closedness; no claim that every odd power of the average fails. The separating functional cannot be integration against a positive measure because p is nonnegative but L(p) is negative.

## Primary-source interfaces and credit

Fresh source receipts and exact reading extents are in primary_sources.json. Seven primary PDFs were acquired directly from their publishers, institutional archive or official arXiv versions. No third-party summary substitutes for the following interfaces.

1. **Reznick, OWR 14/2023, printed pp.778–781:** the entire contribution was read. Page 779 asks about the closed/convex property of the fixed-odd-power sets. This supports attribution to the question recorded in 2023, not a certificate that every subcase remained open at the time of this review. The contribution also records the modified Motzkin cube phenomenon.
2. **Blekherman–Kozhasov–Reznick, published Forum of Mathematics, Sigma 14 (2026), e65:** definitions and relevant introduction, Theorem 5.3 with proof, and §6 through the displayed cube formula were read. Theorem 5.3 takes exponents k and k̃ to k + k̃ − 1 for a sum; its convex union conclusion does not preserve a fixed q. Section 6 separately repeats the fixed-power question. The displayed identity specializes at a = 1 to the paper's seed cube, so this ingredient is credited rather than new.
3. **Berg–Christensen–Jensen (1979):** the entire seven-page original article was read visually from the digitized scan. Lemma 1 is exactly x²y²(x² + y² − 1) + 1, the seed dehomogenized at z = 1. Theorems 3–4 prove SOS closure and separation by a positive-on-squares functional that is not a moment functional. The new manuscript includes a finite-degree proof; it does not need to claim that classical duality is new.
4. **Barak–Kelner–Steurer, ECCC TR13-184 (2013):** Appendix A definition A.1 and Lemma A.5 with proof were read. A normalized truncated functional positive on squares has exactly the needed pseudoexpectation convention. Products preserve the relevant positivity. This is an established ingredient, not the added contribution.
5. **Acevedo–Blekherman, arXiv:2303.11823v1, Lemma 2.1**, and **Blekherman–Riener, arXiv:1205.3102v4, Proposition 6.4:** the relevant notation, statements and proofs were read. Distinct-variable terms determine the leading contribution while coincidences have lower asymptotic order. These are appropriate precedents for the counting technique, not assertions of the precise present fixed-power theorem.
6. **Baldi et al., Stubborn Polynomials, arXiv:2602.01191v1, Definition 2.1 and Theorem 2.2 with proof:** the nonstubborn cone is convex in the stated totally real projective setting, by allowing odd powers to increase. This reinforces the crucial distinction and does not contradict the candidate fixed-q claim.

The plausible added contribution is the application of these classical ingredients to a fixed prescribed odd power, plus a fully specified local rational certificate giving an explicit finite cube dimension. The review found no exact earlier fixed-power counterexample in the bounded inspected sources and targeted search, but it is not an exhaustive literature audit. The candidate page therefore makes no verified firstness claim, no claim of a new product-positivity method, and no claim that all cited sources were read in full.

## Follow-up and collaboration

follow_up is null. Reducing the dimension or resolving the ternary case would matter mathematically, but neither the paper nor this scope review supplies a new mechanism or carefully supported conjecture beyond those immediate boundaries. These are not padded into a public follow-up section. The proposed collaboration invitation seeks substantive specialist review or journal preparation and makes no promise of authorship.

## Independence and exposure disclosure

The independent scope conclusion was logged at 70% before any sibling mathematical findings. No sibling or historical review report, dedicated PRIORITY_NOTE.md, or expected_output.json was read. The public metadata and manuscript §6 necessarily contain author claims about earlier priority audits and verification. README, CLAIM_SCOPE, SOURCE_VERSIONS and PROVENANCE likewise contain accepted-scope/audit statements, source-reading statuses, author-turn provenance, and the origin of a checker in an earlier adversarial effort. These were encountered while reading required mathematical support and locating primary versions. They are source-authored assertions and were not adopted as evidence of correctness or novelty; raw primary documents were freshly acquired and compared independently. No old check count is reported as a fresh execution result.

The original abstract is reproduced completely in content.json, with only whitespace and math typography normalized. AI-use and unrefereed status are separate fields. The manuscript expressly states extensive AI assistance, no human peer review and no formal proof-assistant certificate. This review does not convert those statuses into independent human validation.

No original asset was repaired or altered. No website, spreadsheet, Git, Zenodo, publication or outreach action was performed. Scope content is a candidate awaiting the independent mathematical gates.
