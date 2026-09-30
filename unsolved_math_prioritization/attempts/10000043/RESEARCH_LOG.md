# Research log: infinite clusters and vertical fibers

Actual model: gpt-6-astra, xhigh reasoning. Window: 30 September 2026, 04:52–06:52 UTC. At most five substantive proof attempts.

## 04:55 UTC: original model and status gate

Completion estimate: 5%. Recovered the complete original problem from the archived author manuscript, checked the surrounding section and standing graph/percolation conventions, and visually inspected p.76. No prior project attempt or duplicate was found; the upstream record contains only an OPEN-TRIAGE literature note. Benjamini–Kozma proves a stronger-cutset special case.

## Attempt 1: capped exploration and fiber propagation

Completion estimate: 15%. A deferred-decision exploration capped at M vertices per fiber uses at most 2M horizontal Bernoulli trials per base edge. Its projection is dominated by independent percolation with parameter 1-(1-p)^(2M)<1, excluding uniformly bounded-fiber infinite clusters when p_c(G)=1. A separate conditioning argument propagates an infinite fiber intersection across adjacent fibers. The remaining possibility is an infinite cluster with all fiber intersections finite but with no uniform bound on their sizes. The proof is being written for independent review.

## Attempt 2: cutset and variable-cap obstacles

Completion estimate remains 15%; the full target is unresolved. The existing uniform-cutset condition is not implied by p_c=1: a binary tree with exponentially stretched edges is an explicit negative control. Allowing unbounded fiber capacities yields base-edge bounds approaching 1, which does not contradict homogeneous p_c=1, as an inhomogeneous ray example shows. These examples refute proposed reductions, not the original question. Both selected routes stop at the finite-but-unbounded fiber-size case.

## 05:04 UTC: frozen partial package

Completion estimate remains 15% for the original target. Both selected routes have a precise unresolved gap. The frozen note and exact checker were sent for separate adversarial review. All 4,996 finite assertions passed, including agreement of the original and deferred-decision reached-set distributions. The original universal claim remains unproved, with no counterexample or novelty claim. No PR has been opened.
