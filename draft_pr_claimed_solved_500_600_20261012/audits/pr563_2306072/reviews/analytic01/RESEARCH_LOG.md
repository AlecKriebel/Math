# Independent analytic adversarial review log

Scope: PR #563 / attempt 2306072, global existence, analytic estimates,
and identification of the constructed trajectory with the actual omitted slit.
AI-authored, unrefereed. No historical priority determination. No external
communication or remote mutation is authorized for this review.

## 2026-10-13 05:58:52 UTC — checkpoint 1

Completion estimate: 10% of the assigned audit.

- Read the complete frozen `PROOF.md` independently before any old independent-audit conclusion.
- Confirmed current branch is `main` and created the dedicated `reviews/analytic01` folder.
- The candidate logically depends on an actual global maximizer and a tip-radius gate, rather than asserting that a rational quadratic-differential trajectory is sufficient for extremality.
- Exact remaining work: primary-source hypothesis inspection, independent derivation of root-transform and radius estimates, rigorous continuation/open-closed argument, and adversarial finite checks.

## 2026-10-13 05:59:59 UTC — checkpoint 2

Completion estimate: 25% of the assigned audit.

- Retrieved the primary ETH scan of Duren (1981), extracted text, and rendered source pp.352–355.
- Visually inspected pp.352–353. Equation (1) has exactly the sign and functional stated by the candidate; p.352 asserts one analytic arc and increasing modulus; p.353 asserts `L(f²) ≠ 0` and uniqueness of the trajectory reaching the simple pole at infinity.
- No theorem-hypothesis mismatch found at this checkpoint.
- Exact remaining gap in my audit: independently prove the candidate's trajectory remains on the omitted arc through the two sign-test points, and review quantitative error budgets rather than relying on source or author code.

## 2026-10-13 06:06:48 UTC — checkpoint 3

Completion estimate: 70% of the assigned audit.

- Visually inspected the primary Problem 6.72 statement (printed p.143 / PDF p.144) and Duren's source pp.354–355; both angle conventions in the candidate cover the stated target.
- Re-derived compactness/existence, odd-root univalence, the area-theorem tail control, the conformal-radius upper bound, and the actual tip-radius gate.
- Replaced informal continuation by an explicit open-and-closed intersection argument on `(0,7/4]`, using closedness of the actual complement and local natural-coordinate uniqueness away from the actual tip.
- Additional independently derived estimate: `|tV′/V − 1| < 223 ε` on the entire positive trajectory segment, giving strictly decreasing modulus and a consistent outward angle branch.
- Authored and executed `checks.py`, with exact rational arithmetic and independent composition-based coefficient extraction. All finite controls passed; independently propagated the fine endpoint error below `800 ε η`, stronger than the frozen `2000 ε η` allowance.
- No fatal mathematical gap found. One minor exposition issue: the `7/2` reciprocal numerator uses the stronger `|H| < 11/6` consequence of (8), not merely the displayed coarse `|H| < 2`; the stronger bound follows immediately from the stated parameter.
- Exact remaining work: produce final report/verdict, review consistency of its stated evidence, and hash the authored artifacts. No old independent-audit conclusion has been read.

## 2026-10-13 06:11:40 UTC — checkpoint 4

Completion estimate: 100% of the assigned analytic audit.

- Completed `REPORT.md` with a full independent global-existence, tip-gate, local simple-pole, open-and-closed continuation, orientation, and error-propagation derivation.
- Final finite checker has 31 passing exact rational controls. It supplies tighter fine-angle margins and an additional uniform orientation bound; neither is described as a formalization of the analytic inputs.
- Machine verdict: `PASS_CONDITIONAL_CLASSICAL_INPUTS`. No fatal finding or required mathematical revision; one minor clarity improvement about the reciprocal numerator is recorded.
- Strongest verified result: every genuine maximizer of the specified functional has all three stated forms of nonmonotonicity on its actual omitted support slit.
- Exact remaining gap: no new-argument gap found in this family. The classical theorems and continuous analytic proof are not machine-formalized; novelty and human peer review are not established by this AI audit.
- Source download hashes and inspected page locations are recorded in `SOURCE_NOTES.json`; temporary source PDFs, rendered source PNGs, and full extracted source text are removed to avoid republishing third-party source copies in an authored review package.
