# KOU-21.61 research log

Date: 2026-10-05 UTC. Retained target: 2570, rank 691. Mathematical completion estimates below are subjective progress estimates, not calibrated probabilities or percentages of a proof. The final full-target outcome is unresolved after five substantive approaches. No remote write was performed during this investigation.

## Source and duplicate gate, 07:21-07:27

Started at the requested UnsolvedMath numeric URL; the browser reader could not retrieve it and a direct read returned HTTP 403. The October 2026 editor-hosted 21st edition was retrieved, searched, and visually inspected at printed page 186. It gives the fixed finite-rank free-by-infinite-cyclic problem without a solved or AI-claimed-solution marker. Its reference to archived 4.8 concerns finite presentability, not an algorithm for extracting subgroup presentations.

Live main QUEUE has 2570 queued 0/5. The public catalog retains 2570 and explicitly treats 20001495 as its deferred duplicate, also with zero turns. Exact-ID/code PR and commit searches, exact-ID branch searches, and the main attempts directory found no attempt for either ID. This is a bounded repository search, not a claim of omniscient duplicate detection. Other free-by-cyclic PRs concern different targets. The related-target-group file does not contain this pair, but the individual catalog descriptor does.

## Approach 1: orbit saturation, 07:27-07:29

Mechanism: normalize height and compute free-subgroup orbit windows; test the exact two-sided invariance certificate. Result: complete algorithm when H intersect F_n is finitely generated, including all zero-height inputs. A graph subgroup in F_2 x Z gives an infinite-rank kernel and provable nontermination of saturation even though H is free of rank two. Full-target completion estimate: 10%. Remaining gap: infinite-rank height kernels.

## Approach 2: periodic outer monodromy, 07:29-07:30

Mechanism: reduce to a finite-index free-times-cyclic subgroup, compute central residuals over a free basis, then reconstruct a cyclic finite extension. Result: complete marked presentations and constructive membership in this restricted case. General monodromy is not reduced to the periodic case. Full-target completion estimate: 15%. No novelty claim: the duplicate catalog already describes periodic-monodromy partial progress.

## Approach 3: HNN windows and stopping certificates, 07:30-07:31

Mechanism: construct finite HNN presentations whose relation kernels exhaust the subgroup relation kernel. Coherence implies eventual correctness, but supplies no certified stopping index. Authored exact family in one fixed direct product exhibits arbitrarily many adjacent isomorphism/rank plateaus before a missing relation appears. The relevant Feighn-Handel proof uses global relative-rank minimality in addition to a terminating local tightening operation. Full-target completion estimate: 15%, unchanged because the central effective stopping gap survives.

## Approach 4: finite-index and virtual retractions, 07:31

Mechanism: certify H using a finite cover and a retraction. An explicit Fibonacci mapping torus has exponentially distorted fibre, which cannot be a virtual retract. The fibre itself has an elementary free presentation, so this is only a limitation of the proposed certificate family. Full-target completion estimate: 15%. No counterexample to the target is claimed.

## Approach 5: geometric combination algorithms, 07:31-07:34

Mechanism: benign graphs of groups and relative-hyperbolic transfer. The established Dahmani-Touikan theorem supplies the unipotent-linear/piecewise-trivial regime. The standard general mapping-torus splitting has a non-slender free edge group and does not meet that theorem's hypotheses. Linton's transfer remains conditional on the unresolved peripheral subgroup algorithms.

A final current-literature check found Gray-Linton (July 2026). Full-source inspection of Theorems 1.5, 1.6 and 3.3 and their proofs separated existence of rewriting systems from computing a subgroup presentation from ambient generators. The general algorithm begins with the subgroup's finite presentation already provided. The subgroup-from-generators result has extra locally quasiconvex hyperbolic virtually special assumptions. Thus it does not remove the target gap. Full-target completion estimate: 15%.

## Selected-record recovery, 07:33-07:35

A bounded row request to the dataset server returned the full current row at index 1206; its ID was verified as 2570 and its complete content was inspected. It agrees with the primary target and contains dated open-status triage, with null research-summary fields. The response is not immutably bound to the repository manifest revision. The separate research-results record and full duplicate AI report were not retrieved. No full corpus was downloaded.

## Verification and freeze

The Python verifier uses only the standard library. It checks exact free words, Stallings folding, interval ranks, delayed-window ranks, a finite-kernel saturation example, a Fibonacci automorphism and its inverse, direct-product normal forms, and finite cyclic image indices. The recorded bounded checks do not establish the general algorithm. The written proofs establish only the scoped propositions. The full target remains unresolved, no full candidate is submitted, and independent audit is still required before any publication. All source files and selected records remain outside the release payload.
