# Independent review: fitness-two theorem and value of Lean

Checkpoint: 2026-09-14 00:41 UTC (2026-09-13 Pacific). Reviewer: independent local-theorem subagent. Bounded publication-readiness review completion: 100%; this is not a claim of complete formal verification of the manuscript.

## Scope and independence

Read manuscript sections 02, 03, 04 and Appendix A, then the symmetric and standard exact verifier sources. Did not read prior adversarial review reports before reaching the assessment below. Did not change the manuscript, run publication steps, or contact anyone. The independent calculations below use only Python standard-library rational arithmetic, import no repository module, and start from the original forward replacement process.

## Assessment

**No substantive error or counterexample found in this bounded review.** The fitness-two result is a substantial all-population-size theorem, not numerical extrapolation: it asserts a strict, nondegenerate local maximum over the entire directed row-stochastic tangent space for each fixed n. It does not assert global optimality, a neighborhood uniform in n, or optimality at every fitness.

The logical structure appears coherent: graphical OR duality gives fixation as stationary expected ancestral size; the sample/retarget stationary-current calculation converts its reciprocal to a linear-kernel Markov observable; stationary perturbation gives the Hessian; symmetry reduces its sign to three scalars; explicit signed-resolvent arguments establish those signs. The treatment of the two sampling phase spaces in Section 3 is important and appears consistent, including the empty cache and proper-nonempty ancestral-state boundary.

The three-sector decomposition has the expected dimensions, including the absent symmetric sector at n=3. The final argument correctly turns directional quadratic negativity into a genuine neighborhood by compactness and a uniform Taylor remainder for each fixed n.

## What was independently checked

1. **Original forward process, exact arithmetic:** constructed all transient mutant subsets for n=3,4,5, directly differentiated the transition probability 2x/(1+x) along P=J+eδ, and solved the three absorbing-chain equations for Taylor coefficients. No active-chain or reduced-sector formulas were used. The averaged first derivatives vanished, and every displayed Frobenius-normalized eigenvalue in (4.12) was reproduced:

| n | Standard | Symmetric balanced | Antisymmetric balanced |
|---|---:|---:|---:|
| 3 | 1/11 | absent | 1/9 |
| 4 | 87/640 | 3/208 | 57/640 |
| 5 | 8585/57314 | 359/26660 | 143/2100 |

The tested directions were E(e₁−e₂), an alternating symmetric four-cycle, and a directed antisymmetric three-cycle. This independently verifies the physical Hessian normalization at the low orders, rather than only reproducing a scalar from the same quotient.

2. **All 248 finite phase margins:** independently evaluated (A.20), (A.30), and (A.32) with `fractions.Fraction` for every 40≤N≤287. Every margin is strictly positive. The minimum is exactly at N=40 and equals the printed fraction

`639304267467075678841 / 115369588296792467144716`.

3. **Both all-order discriminant lists:** used the elementary cubic discriminant formula and elementary coefficient convolution/binomial shifts, with no symbolic-algebra package, to reconstruct the coefficients of −disc(P)/8 after N=25+M and −disc(G)/500 after N=288+M. Both lists exactly match (A.24) and (A.35). All coefficients are positive. Combined with the positive constant and leading coefficient of each cubic, the one-real-root argument used in the text is valid.

4. Read the standard and symmetric checker sources. They use exact rational systems and explicit failure checks. The symmetric finite-exception route directly solves the reduced rational systems for 3≤N≤39; it does not simply take the phase inequality on faith at those orders.

## Verification limits and exact remaining trust edges

- This review did **not** rerun the complete pinned release package or every direct reduced solve for 3≤N≤39. The default `python3` here lacks SymPy, so there was no attempt to describe an unexecuted official replay as passing. The independent standard-library checks above did run successfully.
- Neither a successful official replay nor the finite checks alone establishes the all-n model-to-quotient reduction. That step still relies on the labelled algebra in Appendix A, the all-n feature transformations, the stationary perturbation identity, and the representation-theoretic decomposition.
- The signed standard quotient has more coordinates than the physical two-feature space. The source explicitly checks its intertwining/conjugacy and source/reward scaling at finite orders; the text states the all-n identities. The latter deserve focused human review because an error there could preserve a quotient's positivity while making it irrelevant to fixation. The direct original-process checks above reduce this concern at n≤5 but cannot remove it for all n.
- The symmetric all-n proof uses boundary-aware supersolutions and bounds on an alternating resolvent. The discriminant identities and finite phase margins have now been independently reproduced, but this is not a replacement for checking every antecedent inequality and every feature normalization for general n.
- There is no identified gap that should currently be described as a refutation or as an unproved central theorem. These are the remaining scope boundaries of this review. The package's elaborate integrity checks address faithful execution; they do not by themselves supply independent mathematical validation of the reductions.

The strongest directly verified computational claim from this review is the original-process second variation in the three sectors for n=3,4,5, together with all the specified finite phase margins and both discriminant coefficient certificates. The all-n theorem is supported by the written argument and those checks, but has not been formally verified in this review.

## Lean recommendation

**Do not make full Lean formalization a prerequisite for requesting expert public comment or submitting this paper.** Formalization would provide real additional assurance, especially for this proof's transitions between probabilistic models, signed quotients, and exact certificates. It would not independently establish novelty, biological relevance, or journal fit, and being an amateur author is not itself a reason to postpone submission until a proof assistant accepts the paper.

For the fitness-two theorem, a complete formalization is a substantial specialist project. The substantial value comes from an end-to-end theorem that starts with the actual death–Birth fixation process and ends with strict local maximality, with no unproved bridge axioms. Formalizing only the finite arithmetic should be labelled that way; it must not be presented as a formal proof of the entire paper.

A sensible staged allocation is:

1. First obtain mathematical review of the all-n physical normalization, signed-sector reductions, and boundary/resolvent inequalities. These are the most consequential places for an expert to find a conceptual mistake.
2. If resources remain, commission a bounded Lean pilot for a self-contained central result, preferably the strong-selection theorem after its separate proof review, or the general finite-matrix Schur/alternating-resolvent positivity lemma with explicit hypotheses.
3. For a fitness-two pilot, kernel-check rational certificates and polynomial inequalities, then prove their link to the exact sector scalar. This has a clear deliverable and reduces reliance on external numerical algebra, but the theorem statement should make its assumptions explicit.
4. Expand to the full graphical duality, stationary perturbation, physical sector identification, and local-optimality theorem only if the pilot demonstrates a workable development path and the author wants the resulting reusable formal probability/linear-algebra infrastructure.

Current recommendation: **helpful but optional; targeted formal verification offers better initial value than committing to full-paper Lean before submission.** Do not promise an acceptance improvement or a short completion time without a specialist scoping the actual proof.

## Reproduction recipe for the independent forward calculation

Use exact rational arithmetic. For each transient set S and target v, put x=|S\{v}|/(n−1), y=Σ(u∈S)δ[v,u]. The coefficients of the mutant-parent probability are

- f₀=2x/(1+x),
- f₁=2y/(1+x)²,
- f₂=−2y²/(1+x)³.

Use fₜ/n for the transition to S∪{v}, and (1−f₀)/n or −fₜ/n for the transition to S\{v}. Assemble transient matrices Q₀,Q₁,Q₂ and all-mutant boundary vectors b₀,b₁,b₂. Solve

`(I−Q₀)h₀=b₀`,
`(I−Q₀)h₁=b₁+Q₁h₀`,
`(I−Q₀)h₂=b₂+Q₁h₁+Q₂h₀`.

Let ρₜ average hₜ over singleton states. With ρ₁=0, the eigenvalue reported above is `−ρ₂ / (n ρ₀² ||δ||²_F)`. Note h₂ and ρ₂ are coefficients of e², not second derivatives; this distinction is a common factor-of-two trap and was handled explicitly.
