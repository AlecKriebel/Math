# 30002011: five-turn scoped results on corruption choice and Poisson-thinning selection

**Proposed disposition: unsolved, 5/5 substantive author turns, pending independent review.** No claim of historical novelty, human peer review, or unrestricted source resolution is made. The exact original contribution is Brown--Greenshtein--Ritov's OWR14/2012 discussion, printed pp.819--821, qualified using their full2013 paper. It proposes choosing corruption h, including inbred cross-validation, without fixing a single quantified selector theorem.

The full intended general adaptive tuning/refit objective remains unresolved. The strongest proved construction in this packet is restricted and explicit: for iid priors supported on a fixed [0,M], the original Delta_h family with h_n=n^-4 has the known minimax average-regret order (log n/log log n)^2/n. Moreover, arbitrary data-dependent positive h in a sufficiently small window preserves that order. In particular, original finite-thinning CV over H_n={k n^-4:1<=k<=n}, with any deterministic alpha_n in(0,1), any finite B_n>=1 and full-data refitting, has that order. This is a shrinking-grid theorem, not a general-grid oracle theorem.

## Retained mathematical artifacts

1. TURN_1.md: exact sample-maximum envelope, posterior suffix identity, and conditional oracle inequality for the thinned training loss.
2. TURN_2.md: uniform centered-score Hudson limit, exact full-data adaptive deletion correction, and a positive-optimism example inside the original family.
3. TURN_3.md: a modified delete-one-anchored finite Monte Carlo implementation with explicit error bounds, and actual-family failure of the naive fixed-B small-noise selection limit.
4. TURN_4.md: quantitative positive-h convergence to the known gap-filled endpoint, an expected missing-bin discrepancy bound, and a positive-h bounded-prior minimax-order comparator.
5. TURN_5.md: arbitrary-selector shrinking-window guarantee, narrow-window correction bound, and an explicitly modified output safeguard for a general grid.

## Remaining boundary

Unmodified CV and full-data refitting on a general grid permitting moderate h have no sharp adaptive-regret bound here. A better positive comparator alone does not control selection over a wider grid. The guarded protocol is a modification, and the shrinking grid is a substantive restriction. Heavy-tailed priors, unspecified compound-decision regret, and practical performance guarantees are not included.

## Provenance and budget

The two saved October1 author turns were recovered byte-exactly from remote0470e3c086118e50a123cdcffd7becc8ee4234a4; all historical manifests and checks replayed. October2 adds exactly three substantive author turns, numbered3--5. Recovery, source reading, packaging and independent review do not reset or add to that budget. The source's known gap-filled limit, fixed-algorithm coupled-bootstrap/Hudson identity, classical Robbins minimax rate, isotonic projection facts, and general concentration techniques are explicitly credited. All final-source-scope and correctness judgments remain subject to the separate review requested in FINAL_REVIEW_REQUEST.md.
