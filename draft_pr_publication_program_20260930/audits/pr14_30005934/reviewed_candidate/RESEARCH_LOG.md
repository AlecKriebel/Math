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

Saved CANDIDATE.md with a complete narrow negative argument. Finite-rank Riccati tests in D(A²) give the conditional finite-dimensional transform directly, avoiding the global smoothing/order issue. Injective Q gives positive-definite compressed integrated covariance via continuity at time zero. The classical noncentral Wishart parameter theorem then rules out all noninteger alpha. Existing 22 September candidate explicitly credited. No broader theorem or novelty claim. Completion estimate: 90% for narrow proof audit, pending independent review; novelty remains unestablished.

## 03:55 UTC: frozen proof snapshot

Eight exact finite-matrix consistency checks passed, including corrupted sign/order controls. Source audit identifies the exact earlier public candidate and the published finite-dimensional dependency. CANDIDATE.md is frozen for independent review. Completion estimate: 95% of the narrow proof-audit deliverable; independent review is the remaining gate. No novelty or broad existence-classification claim.

03:59 UTC independent-review precision: corrected the Hilbert–Schmidt representative to the adjoint required by the explicitly stated pairing. The scalar noise functional, quadratic variation, and proof are unchanged. Updated frozen candidate hash recorded in provenance.json.

## 04:04 UTC: independent review completed

Independent reviewer passed the exact final proof snapshot and 19 additional finite-matrix diagnostics. Review documents are copied unchanged under independent_review/. The HS representative precision is corrected. Completion estimate: 100% for the narrow proof-audit deliverable; novelty is expressly not claimed because the same conclusion and mechanism were already public on 22 September. No broader external theorem was reviewed.

## 2026-10-01T14:31:36.786230+00:00 — independent acceptance families reconciled

All three families pass the narrow theorem. Source label, Brownian filtration, Anonymous prior attribution, zero/N-convention boundary and runtime documentation are clarified globally; original reviews/provenance/turns remain frozen. Proposed already_solved credited partial outcome, no paper/deposit/tracker. Fresh complete adversary pending. Workflow **78%**, historical first-priority certification **not claimed**.
