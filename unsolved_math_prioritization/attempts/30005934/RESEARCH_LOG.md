# Research log: Wishart processes, 30005934

Model: gpt-6-astra, xhigh. Start: 30 September 2026, 03:43 UTC. Two-hour ceiling: 05:43 UTC. Five substantive-attempt maximum. Only this problem folder may change.

## 03:43–03:50 UTC: source and prior-art triage

- Upstream problem page attempted first; web reader could not access it. Read pinned full record, original report contribution, arXiv paper, and final published paper.
- Repository row: queued, 0/5. All-state PR, branch, content, and recursive-path searches found no earlier attempt for this target or Wishart work. No matching prior-report entry exists in the pinned research-results corpus.
- Exact target: existence of positive trace-class continuous weak Wishart solutions with injective bounded Q and noninteger parameter, allowing a noninjective C0-semigroup.
- A separate unrefereed candidate dated 22 September 2026, ipitchford/wishart-reachable-noise, Lemma 3 and Corollary 2, already claims the negative answer using finite-rank transforms. This prior claim is credited; no novelty assertion will be made.
- Scope: audit and record the narrow noninteger obstruction, not that external candidate's much broader existence classification.
- Key observation: strict positivity of the integrated covariance follows from continuity at time zero, regardless of later semigroup kernels. A finite-rank transform proof avoids any assumption that the integrated covariance is trace class.

Checkpoint completion estimate: 70% toward a documented narrow proof audit; 0% toward establishing novelty. Independent review remains required.

## 03:53 UTC: substantive response 1/5

Saved CANDIDATE.md with a complete narrow negative argument. Finite-rank Riccati tests in D(A²) give the conditional finite-dimensional transform directly, avoiding the global smoothing/order issue. Injective Q gives positive-definite compressed integrated covariance via continuity at time zero. The classical noncentral Wishart parameter theorem then rules out all noninteger alpha. Existing22September candidate explicitly credited. No broader theorem or novelty claim. Completion estimate: 90% for narrow proof audit, pending independent review; novelty remains unestablished.
