# Attempt log

All times UTC on 2026-10-04. Estimates concern author proof preparation, not probability of novelty or independent certification.

## Source triage, 10:51–10:53

Completion estimate: 10%. Verified numeric identity, live queue 0/5, absence of a target attempt/PR in the searches performed, exact OWR definition, and the distinction between multiplicative vertex profiles and edge weights. The catalogue was blocked, but the official primary report and pinned corpus were accessible. A corpus prior-report entry was absent. No substantive proof attempt was hidden as source triage.

## Substantive attempt 1: threshold reduction to additive eccentricities, 10:53–11:02

Completion estimate at 10:54: 70%; at proof freeze: 100% author candidate, audit pending.

Mechanism: for D=n−1 and a threshold R, convert each demand w(u)d(x,u)≤R to the integer radius restriction d(x,u)≤b_R(u), where b_R is the capped inverse profile. A common shift produces nonnegative integer additive weights a_R(u)=D−b_R(u). One call to the known BDH algorithm determines the exact feasible center set. Optimization searches the implicit rows k w(u), with weighted medians guaranteeing constant-factor candidate elimination.

Early challenge: a naive binary search in value space can depend on the bit length or spread of the weights, and explicitly sorting n² candidates is too slow. Resolution: an implicit row-interval search uses O(log n) calls. Equal weights, duplicate products, zero weights, singleton rows, and exact ties are retained in the proof and controls. Floors are implemented by integer-index binary searches, avoiding a hidden real-RAM floor assumption.

Attribution update at 10:54–10:55: Ducoffe's July/August 2026 paper already supplies the generic decision-to-optimization lemma. The packet credits this prior result and makes no novelty claim for weighted-median search. Our main theorem is a short consequence of known algorithmic tools and the threshold mapping. The arXiv BDH theorem has the required additive, nonnegative-integer interface; it does not require bounded dimension or a product-of-trees embedding.

Deliverable: a complete O(n log^5(2n)) theorem for all finite median graphs, with exact mathematical scope and an explicit dependence on the published BDH theorem. This is stronger in graph scope than the finite bounded-cube-dimension target.

## Checks and stopping condition

The controls use exact rational arithmetic, brute-force optimization as a separate expected result, a quadratic reference additive oracle, and an independent linear-time rerooting oracle for trees. They check complete feasible sets and every pruning step's 3/4 contraction. They do not implement BDH or demonstrate its asymptotic bound. The source theorem and interface must be independently audited.

No additional proof-search turns are allocated because a full candidate was obtained in turn 1. No five-approach exhaustion is asserted. The author search stops at this frozen candidate; a fresh independent audit and a separate publication gate remain required. There is no theorem gap within the stated finite, unit-edge, exact-arithmetic model; historical priority and independent certification remain unestablished.
