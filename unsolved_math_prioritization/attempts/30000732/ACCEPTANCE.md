# Acceptance of the corrected partial Maker report

Verdict: ACCEPT_CORRECTED_RIGOROUS_PARTIAL_REPORT.

Problem 30000732 / OWR-1536-002. The full original question remains unresolved by this work.

This is an AI-assisted, unrefereed partial-report edition. Acceptance records an independent internal AI audit after its two required hypothesis corrections were applied. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. Every written mathematical argument, formula and example in the authored report and audit is retained. Executable code, raw computational datasets, copied source PDFs or extracted source text, source renderings, raw search responses and private coordination material are not distributed. Historical finite checks support the written arguments and cannot be reproduced from this edition alone.

Source retrieval, source inspection and mathematical-check statements describe the original report and independent audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution.

## Required correction applied

The audit's exact two-line CORRECTION.patch was applied to a separate copy of the original report before editorial changes. Proposition 2 now requires that H have no isolated vertices. Lemma 6 now requires that G have no isolated vertices. The original report was 19,641 bytes, SHA-256 cc0368b966b87617fcef9f4c164e64ab61515dbf019765ba947203c098f630b5. The corrected pre-editorial report is 19,703 bytes, SHA-256 a646db384b6598f66d6cdb4f26fbdc93c7b0e288e9ea1e9cc6c25c8f529f081f. The exact 1,560-byte correction patch has SHA-256 52e33e952a1628ab230f9ef7bbf6d4c1634ddff61162bebe21d794cc356c40cc.

The historical audit's disposition was CONDITIONAL_ACCEPTANCE_AS_RIGOROUS_PARTIAL_AFTER_TWO_HYPOTHESIS_INSERTIONS. That original conditional decision is retained verbatim in AUDIT.md and as a historical record in ACCEPTANCE.json. Its condition is now fulfilled by the corrected report; it does not become an acceptance of the full research target or of the original unqualified statements.

## Why the hypotheses matter

Let H be K_2 together with 100 isolated vertices. Maker obtains H in one move on K_102. The unpatched amplification statement with L=102, t=1 and k=2 would assert that K_110 suffices for 2H, which has 204 vertices. The unpatched compression statement would assert that K_4 suffices for H, which has 102 vertices. Both conclusions are impossible by vertex counting. Untouched isolated vertices can belong to a retained copy or lie outside the touched-vertex simulation map.

The added hypotheses repair those exact issues. Every intended d-regular target has d>=1 and therefore has no isolated vertices; its disjoint unions do too. No intended displayed bound changes. Lemma 1 and the eventual-time interpretation of tau remain valid for a fixed labelled board even when isolates are present, as the full audit explains.

## Accepted mathematical content

- Fresh-board pass simulation and corrected disjoint-union amplification; the exact equivalence log(alpha_d)=o(d), with no claim that the infimum is attained.
- Edge counting, the additional final-edge obstruction for d>=2, and alpha_1=1/2.
- The proved Erdős-Selfridge potential criterion, corrected K_(4t) compression, and the conservative automorphism lower bound with denominator 4.
- The single-clique exponential lower bound and the explanation why it does not scale into a per-component lower bound.
- Exponential pool-size and fully activated fixed-pool bounds only under their stated restrictions.
- The fixed-pair fresh-common-neighbour obstruction with initial freeness, and the finite prescribed-target quantifier counterexample.

All original report text and formulas remain in PROOF.md apart from the two hypothesis insertions; the full audit and supporting authored narratives remain in AUDIT.md. Their historical timing statements are framed explicitly.

## Limits

No subexponential seed sequence is constructed; no universal exponential obstruction, connected-graph extension, novelty or priority is certified. The cited Feldheim-Krivelevich and Gebauer upper bounds were inspected only to the recorded extent. Their full proofs are not independently certified here. Conditional on Gebauer's prior clique theorem, corrected amplification gives 2^((2/3+o(1))d), still exponential.

The 2008 factor-1/4 versus factor-1/2 observation identifies a gap in the inspected displayed derivation, not a counterexample to the stronger theorem. The bound accepted here is the conservative one independently proved in PROOF.md. The source's order-d clique has degree d-1; the intended regular family uses K_(d+1).

Historical finite checks are supplementary illustrations, authenticated without mathematical reruns during preparation. The bounded literature search establishes neither a new discovery nor the current openness of the original question.

## Exact applied patch

The following JSON string decodes to the complete original audit correction without any byte changes, including its blank context lines. It applies to the original REPORT.md; PROOF.md contains its resulting report plus the editorial wrapper.

```json
"--- a/REPORT.md\n+++ b/REPORT.md\n@@ -34,7 +34,7 @@\n \n ### Proposition 2: disjoint-union amplification\n \n-If Maker can force H on K_L in at most t moves, then, for every positive integer k, Maker can force the disjoint union kH on any K_N with\n+If H has no isolated vertices and Maker can force H on K_L in at most t moves, then, for every positive integer k, Maker can force the disjoint union kH on any K_N with\n \n \\[\n N\\ge L+4kt\n@@ -98,7 +98,7 @@\n \n ### Lemma 6: finite-board compression\n \n-If Maker can force G in t≥1 moves on some complete board, then Maker can force it in t moves on K_(4t).\n+If G has no isolated vertices and Maker can force G in t≥1 moves on some complete board, then Maker can force it in t moves on K_(4t).\n \n **Proof.** If the original board has at most 4t vertices, apply Lemma 1. Otherwise simulate its strategy using a partial bijection between the touched vertices in the virtual large board and the actual small board. Each new endpoint requested by the virtual Maker strategy is mapped to an untouched actual vertex. Each new endpoint used by actual Breaker is mapped back to a previously untouched virtual vertex. Before Maker's jth move at most 4(j−1) actual vertices have been touched, so at least two unused actual vertices remain for j≤t. The virtual board has more than 4t vertices, so the reverse extension for Breaker is also possible. These extensions preserve both players' edge sets on all touched vertices and simulate legal play through Maker's tth move. The virtual copy is therefore an actual copy. ∎\n \n"
```
