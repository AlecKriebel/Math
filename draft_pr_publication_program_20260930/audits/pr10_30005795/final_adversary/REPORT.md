# Fresh complete adversarial acceptance report: PR10

Checked 2026-10-01 04:57:27 UTC. Assigned review completion: **100%**. Novel-discovery completion: **0%**, by design of the accepted known-method disposition.

**Verdict: PASS. Accept the corrected candidate as a known bound/source-status correction. There are no unresolved mathematical, source, scope or immutable-evidence issues within this acceptance target. No novel paper or DOI is justified by this result.**

The accepted object is the six repaired files in `reviewed_candidate/`, with hashes in `repair_manifest.json`, plus the original unchanged turn evidence. This is a certificate of the corrected candidate, not retrospective approval of every phrase of the immutable original PR snapshot. The frozen original has the documented ordinary/log-discrepancy terminology error, source bibliography locator error and stale scope metadata. Those repairs are meaningful and complete in the reviewed candidate.

## 1. Independence and exact target

I first read `reviewed_candidate/BOUND.md` directly and reconstructed its proof obligations before opening any earlier family report. An agent inventory subsequently exposed summarized prior status messages; the independent target and stress cases were already chosen. I then checked the mathematics, geometric boundary mechanism, snapshot and corrected metadata. A fresh subagent reconstructed the primary OWR and CFKO sources from PDFs and visual renders without reading previous source-family reports. Only after the direct reconstruction did I read the LCT, Mori and source-priority reports to search for missed objections and verify repair coverage.

The exact target is a finite constant depending on the input surface and actual negative-part family, uniform over prime divisors over the surface. In the smooth projective complex Fano threefold setting, S is integral, normal, prime and Du Val. With the report's nef restricted positive part, the weight is nonnegative. The global statement covers every surface center; the point-local version covers precisely centers containing the distinguished point. Neither a universal number independent of X,S nor a sharp application-specific K-stability estimate is part of this acceptance target.

## 2. Mathematical acceptance matrix

| Obligation | Independent finding | Status |
| --- | --- | --- |
| Correct valuation domain | The divisor and discrepancy are on S; an arbitrary divisor over X has no such typed surface valuation. | PASS after explicit statement repair |
| Surface singularities | Du Val implies klt and positive log discrepancies. Merely lc can fail by the cubic cone counterexample. | PASS |
| Actual divisor equality | The finite decomposition is expressly an equality of actual real Cartier divisors, retaining restriction multiplicity. Linear or numerical equivalence would not determine the orders. | PASS |
| Compact interval | Ampleness near zero and the H^2 intersection inequality give 0<tau<infinity. | PASS |
| Rational effective endpoint | Closed rational Mori cone in Pic_R, together with Pic_Q=N1_Q, gives rational tau and a Q-effective representative of H-tau S. | PASS |
| S absent from N | A positive S coefficient in an endpoint representative contradicts maximal tau; convex interpolation with an anticanonical representative avoiding S proves rational-u avoidance and closed-chamber extension proves real-u avoidance. | PASS |
| Finite support, walls and endpoint | Okawa's finite closed chambers and Q-linear maps, with fixed-part uniqueness on overlaps, give bounded piecewise affine actual negative coefficients on the entire compact segment. | PASS |
| Cartier restriction | Smooth X makes each negative prime Cartier; E distinct from integral S gives a nonzero local equation in a domain, hence a nonzerodivisor and an effective Cartier restriction. Zero restrictions are allowed. | PASS |
| Integral finiteness and sign | Bounded coefficient functions and a bounded piecewise quadratic weight give finite integrals. For signed weights, clipping is a valid separate upper bound; it is not used in the effective-boundary optimal identity. | PASS |
| Threshold positivity and endpoint | A finite resolution including exceptional divisors and strict transforms has a finite nonempty minimum of positive A/order ratios. The SNC crepant boundary at the minimum has coefficients at most one. | PASS |
| Real boundary and optimum | The same resolution and minimum work for arbitrary nonnegative real integrated coefficients. The reciprocal supremum is attained globally for B nonzero. | PASS |
| Global/local and zero conventions | Global thresholds are used globally; local thresholds only for admitted centers. Infinite local thresholds give zero contribution on those centers. B=0 gives nonnegative optimum 0 and any requested positive K can be chosen. | PASS |

The complete independent derivations and explicit scope falsifiers are in `DERIVATIONS_AND_FALSIFIERS.md`. They show that the repair does not hide a central unsupported equivalence or transfer the hard step to another unproved claim.

The final core certificate is

    B=sum_j aj Dj,  I(F)=ord_F(B),
    I(F)<=A_S(F) sum_j aj/lct(S;Dj),
    Kopt=0 for B=0, otherwise 1/lct(S;B).

On a common log resolution, the threshold is the minimum of A_i/m_i for m_i>0, so its reciprocal is a finite maximum and is attained. This certifies the claimed real-coefficient generality as well as the endpoint. It makes no threshold-additivity assumption and no stability conclusion from mere finiteness.

## 3. Concrete nonzero reproduction and adversarial edge tests

I independently verified the geometry in `verification/EXACT_EXAMPLES.md`, then ran `verification/check_exact_examples.py` successfully. For the blowup of P3 along a line, the incidence embedding in P3×P1 makes -K=3H+(H-E) ample. A plane fiber S is P2; E|S is an actual reduced line. The intersection data give volume 54. The effective cone and normalized fixed part give tau=4, N=0 on [0,1] and N=(u-1)E on [1,4]. The weight on the second piece is (4-u)^2/18. Thus B=(3/8)C, its threshold is 8/3, and K0=Kopt=3/8, attained at C.

The endpoint has P=0 and a finite N, the two positive pieces agree at the wall, and the local zero bound outside C correctly fails as a global bound. Both the geometric argument and exact rational arithmetic pass. The script's limitation is accurate: arithmetic checks use separately justified resolution/geometry inputs and do not replace the general proof.

Fresh stress tests covered: actual versus equivalent divisors; point-local versus remote centers; centers containing P versus equal to P; an lc non-klt elliptic cone; a nonreduced Cartier divisor on an A1 Du Val surface; missing strict transforms; negative integrated weights; infinite support with unbounded orders; irrational real coefficients; reducible S or E=S; negative u outside the parameter interval; empty/zero families; scaling and the zero limit; and interacting tangent versus transverse curves. Every counterexample targets a hypothesis omitted from the accepted statement or a stronger claim expressly disclaimed by it. No counterexample within the stated hypotheses was found.

## 4. Primary-source and classification acceptance

The fresh source certificate is `source_check/REPORT.md`. It visually checks the official OWR PDF pp.836, 837, 839, 840 and 844, confirms the genuine printed ambient-domain typo, inherited Du Val context and immediate worked example, and identifies CFKO as reference [3]. Its reconstruction agrees with the independently supplied surface-domain certificate. [Official OWR source](https://ems.press/content/serial-article-files/48650).

The published CFKO Appendix B **Lemma 27, pp.712–713**, and author-preprint **Lemma 26, p.23**, have the same first discrepancy-bound mechanism. The lemma is stated under the del Pezzo fibration assumptions. The candidate correctly identifies the geometry-independent first proof step as the basis for its finite-family extension; it does not misquote the lemma as a statement without those assumptions. The later volume comparison uses fibration geometry and is not promoted. [Published article](https://doi.org/10.1017/nmj.2023.5), [author preprint](https://www.maths.ed.ac.uk/cheltsov/pdf/220608539.pdf).

The source question imposes neither a universal numerical K nor an optimal/sharp K requirement. Useful stability estimates for particular examples may require more work, but no separate stronger unresolved source target is identifiable in this passage. Therefore `already_solved` with the explicit known-bound/source-status note is an accurate queue disposition for the corrected finite-bound task. No new mathematical-solution or historical-priority credit is warranted.

The source checker found a further harmless printed summation upper-index typo in both CFKO versions: tau in place of the number of components. The candidate reconstructs the correct finite sum. This need not be added to the mathematical exposition unless someone later quotes that display literally.

BCHM's published Corollary 1.3.2 is correctly cited; an early arXiv version numbers the corresponding Fano/Mori-dream result 1.3.1. Direct AMS PDF retrieval returns 403, but the primary indexed published text and rendered author manuscript establish the numbering and hypotheses. Okawa Proposition 2.8, Remark 2.12 and Proposition 2.13 directly support closed finite chambers, fixed-part uniqueness and linear negative parts. The candidate's broad original-model nef caution does not overclaim; it assumes the source's nef restriction and offers a correct sign safeguard.

## 5. Full metadata and immutable-snapshot consistency

`INTEGRITY.json` independently certifies that all seven immutable source-snapshot byte strings match their manifest SHA-256, size and the repository object at audited PR head `925f9e9f46f2c7407fd142cedf36995a4519a378`. All six repaired candidate hashes match `repair_manifest.json`. No mathematical candidate or snapshot changed during this review.

The complete PR diff from base `01358d66fc67d1c462bddf31c0d4ee5b120e6737` has eight paths: seven effort files and exactly one central QUEUE row. The repaired `PUBLICATION.json`, `readiness.json` and `PR_DRAFT.md` accurately set central modification true and identify the row's known-bound classification. The source record retains every original dataset field and adds a clearly separated statement-audit object identifying the required correction. Its historical `open` and `corrected_verified` fields are upstream provenance, not the corrected active conclusion; the audit and readiness metadata explicitly distinguish them.

I independently reread the cached pinned dataset, recomputed its SHA-256 as `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`, matching the repository manifest, and checked selected records 30005795 and 30005796. The frozen selected record equals the original dataset record; the corrected record preserves every original field. Record 30005796 expressly states that it repeats the preceding negative-part question and has no independent target. `DUPLICATE_CHECK.json` records these checks.

The original PR metadata/body and initial log entries saying no central files changed remain truthful evidence of the initial checkpoint and stale evidence of the later delivery. They should remain frozen. The reviewed draft description corrects the current scope. Updating live delivery metadata after acceptance is normal parent workflow finalization; it is not an unresolved mathematical or source acceptance issue. No retroactive alteration of the frozen record is needed.

## 6. Actionable disposition and remaining gap

**Required substantive repairs: none. Acceptance blockers: none. Exact remaining mathematical/source gap: none for the accepted finite input-dependent bound and source-status correction.**

The authorized parent may promote the reviewed files and finalize current acceptance/PR metadata. Preserve the original snapshot, classification note, explicit global/local distinction, prime/integral algebraic surface assumptions, actual divisor equality and source-proof generalization qualifier. Keep new-paper/DOI plans false. Do not reinterpret this pass as certification of the full surrounding stability formulas or of any universal/sharp/application-specific estimate.

Only audit files under `final_adversary/` were authored by this reviewer and its source subagent. Scratch primary PDFs/renders live only under ignored `tmp/final/`. The checkout remained main. No git mutation, push, release, external contact or outreach occurred.
