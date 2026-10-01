# Final independent review: scope-corrected 5000007

Date: 2026-10-01

## Verdict

**PASS for the explicitly parity-aware theorem in PROOF_V2.md.** The reviewed proof is complete at that stated scope. The literal dataset sentence using only beta-alpha=2pi/5 is false; its two additional direct-face-diagonal exceptions are correctly identified. Do not report this as an affirmative proof of that unqualified extracted sentence.

The source's preceding sign rule, its assertion that there are three pentagon types, and its explicit non-A0 diagonal calibration support the parity-aware reading of the intended Fuchs conjecture. The source's isolated shorthand is insufficient at the exceptional directions. The revision correctly makes this a visible source-formulation issue rather than silently adding a condition.

This is an independent AI adversarial review, not human peer review. It makes no novelty, priority, publication-readiness, or research-budget-provenance claim.

Completion estimate: 100% of the assigned proof/source/witness review.

## Exact version reviewed

PROOF_V2.md SHA256:

f96288e95c946731091989cea3eb087829c94cf966898dae792122567da3f16b

The preceding frozen version and its detailed review are preserved separately in CANDIDATE_PROOF.md and independent_review/REVIEW_V1.md. Suggestions were not silently inserted into that earlier version.

## Checks supporting the verdict

1. **Angle scope.** The terminal interior sector in Figure 8 is pi-beta, and the outgoing ray belongs to the successively reflected billiard polygon. The two literal-shortcut exceptions have (alpha,beta)=(36,108) and (72,144) degrees, N=1, source types A2 and A1 respectively, and graph-distance-two endpoints. The revision proves these are the only extra interior cases; the remaining odd-N cases are the ordinary edges.

2. **Double-pentagon step.** The explicit involution h(z)=1-z maps the initial P corner p0 to q1 in Q. For even N the 72-degree difference selects exactly that terminal corner. Reversing the connection and applying h yields the same initial germ. First-singularity uniqueness gives midpoint invariance. The five regular fixed points are exactly the glued edge midpoints. The facewise translation cover preserves the distinction between vertices, open sides, and face interiors, so the projected midpoint really lifts to a physical edge midpoint. This also supplies the converse identification for interior germs, although the theorem needs only the forward implication.

3. **Physical lifting.** The actual dodecahedral edge-axis half-turn has intrinsic derivative -I at the regular midpoint. Parameterized geodesic uniqueness exchanges the endpoints, including when the image self-intersects. No unjustified global descent of the hyperelliptic map is assumed.

4. **Distance exclusion.** The revised unique-common-neighbor proof is correct: the dodecahedral graph has no 4-cycle, and an involution swapping a distance-two pair would fix its unique common neighbor. A nonidentity rotational half-turn cannot fix a vertex with rotational stabilizer of order 3. The previous coordinate enumeration is now merely corroboration, as it should be.

5. **External witness.** A separately authored exact cyclotomic reconstruction verifies the legal 16-face path, all 15 ordered interior crossings, first-vertex shortness, squared length (307+137sqrt5)/2, and distance 2. Purely combinatorial transported labels select terminal ray 2->16 at 216 degrees. With 0 < alpha < 36 degrees, Figure 8 gives beta-alpha=144 degrees, hence A1. The public 72-degree calculation uses the other physical ray and an interior angle instead of the source's beta. The revision states the disagreement accurately and does not reject the valid geometry.

6. **Attribution.** The revision credits the established translation-cover and virtual-Weierstrass framework and the earlier midpoint involution argument to Athreya-Aulicino-Hooper. It does not attribute a universal pentagon saddle-connection theorem to their triangular/square result. No exhaustive literature or historical-priority claim is warranted by the limited source search.

## Independent artifacts

- reviewer_exact_check.py: new standard-library implementation over Q[z]/Phi_5; does not import author or external programs
- reviewer_exact_check_output.json: all exact checks pass, including the negative-control diagonal
- author_checker_rerun.json and author_half_turn_rerun.json: byte-for-byte reproductions of the supplied author outputs, supplementary to the independent checks
- REVIEW_V1.md: original frozen-version audit and source interpretation details
- reviewed_hashes.json: exact reviewed input and review-artifact hashes

No external source code was executed. The only rerun programs were the locally authored author checkers, inspected before execution, plus the separately authored reviewer checker. No remote write or outreach was performed by this reviewer.

## Remaining non-mathematical limits

The original lost author-turn count is unknown and nonzero. This review neither resets it nor verifies a fresh allowance. The user's current five-substantive-author-turn rule for unfinished work does not require padding an already complete candidate with further proof search, but historical count reconciliation and publication decisions remain with the campaign coordinator. Existing earlier campaign attempts are not reopened by this review.

A suitable concise description is: a reviewed parity-aware proof and explicit source-wording correction, with an independently verified type correction for the identified public witness. Avoid an unqualified claim that the literal extracted problem was proved true, and avoid claiming a certified or first discovery.
