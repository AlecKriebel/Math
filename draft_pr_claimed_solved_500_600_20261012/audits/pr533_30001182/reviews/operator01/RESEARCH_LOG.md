# Independent operator/state audit log

Target: PR #533, problem 30001182 / OWR-3392-009. Frozen head `135911efff1ad14314f0506b0d5f158ba986426f`.

All output stays in this folder. No remote mutations or outside communications are authorized. Historical priority is outside this review.

## 2026-10-13T04:45:06Z — scope and hypotheses (10% complete)

Read frozen `PROOF.md`, `SOURCE_GATE.md`, eligibility and snapshot metadata. Treat the central claim as a hypothesis: there is a state-preserving unital inclusion of finite-dimensional probability spaces for which the exact printed extremal-exchangeable definition changes. The load-bearing burdens are (i) exclusion of **every** witness in the smaller ambient algebra, (ii) purity and exchangeability upstairs, (iii) equality on the full free product of the two coordinate subalgebras, and (iv) matching the source's convex set and state conventions.

Initial independent approach: use equality in the projection Cauchy–Schwarz bound to derive a rank-two cyclic representation downstairs; separately prove quotient pullback purity using dominated states and the kernel. No supplied checker has been read or run. Official source PDF opened independently through the web reader; screenshot/text follow-up timed out, so printed-page confirmation remains pending.

## 2026-10-13T04:47:55Z — independent derivation and source convention (55% complete)

The universal quantifier downstairs survives attack. For general `0 < t < 1`, constraints `ω(p_i)=ω(q_j)=ω(p_i q_j)=ω(q_j p_i)=t` for `i != j` give `(p_i-q_j)Ω=0`. With three indices, all `p_i Ω,q_j Ω` agree with a vector `v`; idempotence gives `R v=v` for every generator. The cyclic space is `span{Ω-v,v}` and every generator acts as the same projection. The resulting state is exactly `(1-t)χ_00+tχ_11`, which is nonextreme among all invariant states. This does not assume a null space is a two-sided ideal.

Independent source retrieval succeeded via the publisher PDF at `https://ems.press/content/serial-article-files/46209?nt=1`. Web extraction identifies printed page 540 / PDF page index 47. The definition and item (1) use unital free products, full state equality, and unqualified extremal exchangeable states; no fixed-marginal convex slice or faithfulness/tracial assumption is present in the contribution's definition. Web screenshot requests failed, so the read is from the complete printed-page text extraction and diagram labels, not a reused local PDF.

New adversarial boundary observation: the downstairs mixture is actually extreme in the **fixed-full-marginal** invariant slice. In a decomposition within that slice, zero expectations of all `(p_i-q_j)^2` force each component through the same collapse, hence equal to the mixture. Thus changing the convex set really destroys this particular counterexample. The original proof's narrower scope warning is warranted, not cosmetic.

The upstairs quotient argument works algebraically without boundedness: a decomposed pullback state kills the quotient kernel by Cauchy–Schwarz, and positive liftings show each component factors to a state of the quotient. A rank-one matrix density then has no nontrivial decomposition. The canonical diagonal inclusion uses the full identity, so no corner or nonunital error occurs. Independent exact checker construction remains; supplied checker still unread/unrun.

## 2026-10-13T04:50:47Z — independent assessment fixed before replay (75% complete)

Independent mathematical decision: **PASS for the unrestricted positive-state definition** in both unital algebraic and universal C*-free products. No counterexample to the claimed counterexample was found. Strongest verified claim: the admissible downstairs witness is unique and equals the explicitly nontrivial invariant character mixture; pure folding supplies an upstairs witness with the exact complete law and full prescribed marginal. The algebraic no-positive-extension example is also valid by Cauchy–Schwarz.

Independent checker `independent_verify.py` completed successfully using exact rational arithmetic: 12,282 binary-generator words, 23,436 alternating rational affine words, 42 Gram principal minors, 60 positivity checks, the rank-one density and the coordinate intersection. The six exact weights include `0`, `1`, `1/2`, `1/5`, `4/5`, and `9/13`. Boundary weights correctly remove nonextremality; three-copy graph connectivity is essential to the mechanism. Finite checks are auxiliary and do not certify infinite quantifiers.

Additional attack: any tracial state on the upstairs free product restricts to normalized trace on each `M4` copy. A tracial witness matching the proposed joint law would force `p_iΩ=q_iΩ`, hence zero expectation of `(p_i-q_i)^2`, whereas normalized matrix trace gives `1/2`. Thus the upstairs example has **no** tracial witness. This confirms that positivity without a trace restriction matters. The source definition contains no such restriction.

The supplied verifier has still not been read or run. Next step is a confined replay after inspecting its output paths, followed by the complete independent proof report and manifest. No mathematical gap remains within this review's scope; source historical priority and modified definitions are outside it.

## 2026-10-13T04:55:08Z — final independent audit checkpoint (100% complete)

Completed `REPORT.md` with independently checkable proofs of every-witness exclusion, algebraic and universal C*-quotient purity, and the complete `B*C` state identity. The report includes an explicit extreme two-copy boundary witness and proofs for the fixed-marginal and tracial variants. It also checks the separate Laurent-polynomial non-lifting example and the contextual C*-compactness argument.

After independence was fixed at the prior checkpoint, the authored checker replay passed all 14,944 assertions; its output matches the frozen expected JSON exactly. `REPLAY_RECEIPT.json` records the interpreter, order, checksum and timestamp. `INPUT_VERIFICATION.json` confirms that the four selected authored inputs match the frozen snapshot. `SOURCE_READ_RECEIPT.json` records independent source access and the failed screenshot limitation precisely.

Final disposition: **PASS mathematics within the unrestricted positive-state definition; no blocking issue and no exact remaining mathematical gap in this operator/state scope.** Historical novelty remains outside this assigned review. Modified faithful-only, fixed-marginal, tracial-only, and W*-definitions are not promoted as solved. All original inputs were preserved. No remote mutation, commit, push, release, outside-human communication, or other-shard communication was performed. The final integrity manifest freezes this review's checkable artifacts.
