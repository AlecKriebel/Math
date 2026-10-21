# Independent mathematical audit of the prior Erdős 776 threshold claim

Date: 2026-10-21 UTC. Scope: the existing claim, not a new theorem or priority claim.

## Decision and precise acceptance boundary

The mathematical argument is accepted **with the explicit manuscript-index correction below**, using classical Kruskal–Katona and its colex attainment as the standard foundation. The audited conclusion is n0(r)=2r+4 for 4≤r≤10 and n0(r)=2r+5 for r≥11, where n0 is the least N for which g(n,r)=n−3 for every integer n>N. Independent exact-integer checks and a symbolic review support both failure at N and success at every larger n. No load-bearing mathematical defect was found. The uncorrected manuscript has a local false shadow-index identity; it is not accepted verbatim as error-free.

This is a mathematical/source audit, **not an independently compiled Lean certificate**. No local Lean build or local `#print axioms` was executed. An externally recorded successful CI build is distinguished below from independently inspected kernel output. The cases r=2,3 remain attributed to He–Tang and are outside this proof audit. Official problem moderation and specialist peer-review acceptance are not established here.

## Hash-bound source

Primary release: https://github.com/mthiim/erdos_776/tree/v0.4.1-proof-claim

The inspected clone resolves to commit `1ca43203123642edaac45bf00b6fc333c848b4c9`. The source manifest accompanying this audit records SHA-256 and byte counts for every tracked file. Key identities:

- Combined PDF: `ff3ea2d22836523f8b6bfb6f3ffaf48e42a998503725faf7848cd31a5c56ed32` (208973 bytes).
- Uniform manuscript: `722c8c77c325806b25498c40e0e65f9d9c83b0f13ca26b733d818a7441255731`.
- L4 manuscript: `85c2d5ffc0a5e67a0b9d31ccb16bc75872b1d4f3970539b9d964166f53af3312`.
- Original-formulation endpoint: `3ef209af1ee22a69cee4ec70beafc66c19a2086888469ef2c8cf60d6585f4177`.

## Formulation and leastness

The finite-family representation contains distinct subsets, with incomparability under inclusion. Relabeling [n] by Fin n preserves all relevant structure. At least r members on each occupied level is equivalent to exactly r for the level-maximization objective: choose r representatives on each level, preserving incomparability and all occupied levels.

For r≥4 and n≥r+1, levels 0,n are forbidden. If r singleton members occur, every nonsingleton member avoids their r points, so at most n−r≤n−4 sizes occur. Complementation gives the analogous exclusion for level n−1. Thus every admissible family has at most n−3 levels; equality is precisely occurrence of all levels 2,…,n−2. The hypotheses hold at the proposed last failures and throughout their tails. Consequently the endpoint's target-existence statement is equivalent there to g(n,r)=n−3, rather than merely a lower bound.

The proof exhibits failure at N and success for every n>N. If a candidate M<N were an eventual threshold, its defining tail would include N, contradiction. No monotonicity-in-n assumption is needed, and no off-by-one shift is permitted: the first successes are 2r+5 for r4–10 and 2r+6 for r≥11. Natural-number quantification suffices; a negative integer threshold would also include the positive failing N.

Source: https://github.com/mthiim/erdos_776/blob/v0.4.1-proof-claim/Erdos776/Uniform/ProblemStatement.lean and GlobalThreshold.lean in the same directory.

## Profile framework

For requested level counts f_i, set m_s=f_s and m_i=f_i+∂_{i+1}(m_{i+1}). Necessity follows by taking the cumulative level-i down-closure of all chosen sets on levels ≥i. Its level-i chosen portion is disjoint from the down-closure of higher members. Kruskal–Katona and monotonicity inductively imply cumulative size at least m_i, hence m_i≤C(n,i).

For sufficiency, construct downward in colex. The down-closure from higher choices is a colex initial segment. Take the next f_i sets after that segment. The capacity bound ensures they lie within [n], and avoiding that down-closure rules out containment in every higher chosen member. This proves the exact requested profile. Only requested levels need checking: lower levels with zero requested count require no selected sets and their shadows fit automatically. This addresses the apparent omission of levels 0,1 in the implementation's middle-profile checker.

Source: https://github.com/mthiim/erdos_776/blob/v0.4.1-proof-claim/docs/TECHNICAL_NOTE.md

## Independently reproduced finite mathematics

The accompanying `independent_arithmetic.py` was authored for this audit and uses Python's exact integers and `math.comb`; it imports no claim code and executes no third-party script. Its binary-search greedy cascade chooses the maximal available upper digit at each position, subtracts that binomial, and sums its one-position-lower shadow. Strictly decreasing digits are enforced by the next search ceiling. Thus the implementation directly evaluates the canonical KK recurrence.

Its successful output establishes:

- For r=4,…,10, the full profile fails at n=2r+4 with level-2 excesses 1,1,1,2,2,2,2. Every higher level fits. The full profile at n=2r+5 fits all requested levels and has zero level-2 slack. The core profile 2,…,r+2 fits on r+5 points.
- For r=11,…,28, the upper-core states fit on r+4 points at levels ≥4; level 3 has positive excess e∈{1,2}, hence 1≤e≤6. The core fits on r+5 points. The full profile at n=2r+5 has level-2 excess 1 and fits all higher levels.
- For all 367 values r=11,…,377, the lower-window profile with top load r−6 fits on r+4 points. Minimum capacity slack is 3, first attained at r=20. Seam values 378,379 also fit, but numerical seam checks are not substituted for the symbolic proof beyond this range.

## Uniform symbolic dependency chain

The companion symbolic review checks the lower-window anchor, phase, envelope, and scalar-collapse arguments, plus L4's reverse envelope, with the correction below. The lower window supplies all upper-core capacities at levels ≥4 and a level-3 excess at most 6 by complementing the feasible profile. If the excess were nonpositive, the truncated core profile on levels 3,…,r+2 would fit on r+4 points; complementing it would produce L4's forbidden profile on levels 2,…,r+1. Thus the excess is positive.

Writing A=r+4, the resulting a3=C(A,3)+e with 1≤e≤6 gives a2=r+C(A,2)+∂2(e)≤r+C(A,2)+4=C(A+1,2). Higher capacities already fit, so the canonical core exists on r+5 points. Its top r colex members are the (r+2)-subsets of [r+3] obtained by deleting one of r distinct points other than a fixed common point. Puncturing that common point gives r distinct free (r+1)-sets: any core member inside one would be contained properly in another core member, impossible.

Two-point padding appends D_i∪{x,y}. Freeness prevents old-to-new containment, and new points prevent reverse containment. Persistent free sets retain one point of each added pair and omit the other, so they cannot contain any later-added member. At stage t the core has q=r+5+2t points and top size s=r+2+t. A pivot plus r private points converts it to a full middle profile on both n=2r+6+2t and n=2r+7+2t. Within each side antichainness follows from the core/private points; across complementary sides, common pivot forbids disjointness, while the union of two lower sets has size at most 2 floor(n/2)−1<n. This covers every n≥2r+6, not just one parity.

For obstruction at 2r+5, put B=2r+4. Upper-core capacities are strict at levels ≥4: equality would violate the next capacity, or at level4 would force e=r>6. The no-carry diagonal-shell identity transfers the full-profile recurrence to a state M_{r+3}=C(B,r+3)+e. Starting from residual1, peel the shell with residual recurrence v_{k−1}=r+∂_{k−1}(v_k). The index k−1 here is correct because the residual lies below the leading position-k digit. If a residual reaches C(B,k−1), Pascal gives full capacity at level k and the positive next load forces overflow (or there is already strict overflow). Otherwise shell separation persists to level3. Residual domination of the L4 chain yields v3>C(A,2), hence ∂2(v3)≥A+1. Therefore M2≥r+C(B,2)+(A+1)=C(B+1,2)+1, impossible. This verifies both branches of the obstruction, including a possible carry, rather than assuming all residuals remain subcritical.

Sources: https://github.com/mthiim/erdos_776/blob/v0.4.1-proof-claim/docs/UNIFORM_THEOREM.md , https://github.com/mthiim/erdos_776/blob/v0.4.1-proof-claim/docs/L4_PROOF.md

## Explicit manuscript correction and Lean comparison

Uniform manuscript §6's worked schematic applies ∂_{b_j−L} directly to the isolated run R_{j,L}. Its displayed cascade begins at position u_j−L, whereas b_j−u_j=t+j+1>0. Accordingly the isolated-run identity must use ∂_{u_j−L}, in both displayed occurrences and the subsequent inequality. Equivalently, keep the full-level index but apply it to the complete canonical state, then extract the run contribution. The fixed anchors/stones shadow separately because their concatenation with the run is canonical. Appending Q pays r and gives the next run, so this correction does not change any construction or bound.

The actual Lean source avoids this typo: `phaseDigits` concatenates `phaseFixedDigits` with `phaseRunDigits`; `phaseState` evaluates that whole list at `phaseBirth−L`. `phase_extension_pays` shadows `phaseState`, not the isolated run, and `phaseExtension_actual_index` accounts for the length of the entire fixed prefix. This is source inspection, not fresh compilation.

Source: https://github.com/mthiim/erdos_776/blob/v0.4.1-proof-claim/Erdos776/Uniform/LowerWindow/PhaseTransitions.lean

## Formalization trust boundary and reproducibility status

Source scan of the project Lean directory found exactly three `native_decide` invocations and no `sorry`, `admit`, explicit project `axiom`, `unsafe`, or `implemented_by` matches. This lexical result is not a compiled dependency audit. The finite certificates cover 4–10, 11–28, and 29–377; checker soundness translates bounded shadow evaluations to canonical recurrence statements, then to actual antichains. The large-r endpoint is assembled from symbolic statements and contains no finite-certificate premise. The numerical KK bridge calls mathlib's `Finset.kruskal_katona`; KK is not introduced as a custom project axiom.

The declared audit allowlist for the full endpoint consists of propext, Classical.choice, Quot.sound, plus the generated native-evaluation axiom for each of `smallThresholdFiniteCheck_verified`, `smallUniformFiniteCheck_verified`, and `lowerWindowFiniteBaseCheck_verified`. The large-r endpoint's declared allowlist is just the three standard axioms. Native evaluation therefore adds compiler/evaluator trust for bounded computations; calling the entire result pure kernel reduction would be misleading.

Required toolchain is Lean v4.30.0 and mathlib v4.30.0. Neither lean nor lake was available locally. No installation or execution of unrecognized source was undertaken. GitHub API metadata for the pinned commit reports successful CI run29609689503, job87981183297, including both build-with-warnings-as-errors and axiom-audit steps. This is an independently retrieved **external success record**, not independently inspected theorem-axiom output. Retrieving its job log returned HTTP410; no inference is made about the missing log contents beyond the step metadata.

CI record: https://github.com/mthiim/erdos_776/actions/runs/29609689503/job/87981183297

A future clean local build and exact axiom-output comparison would strengthen formal reproducibility, but are not being represented as completed. This acceptance concerns the corrected mathematical argument and independently reproduced finite arithmetic, not a fresh machine certification or official resolution.
