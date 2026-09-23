# Research log: OWR-4136-011

All times UTC. Completion estimates concern the requested verification and publication package, not a probability of mathematical truth.

## 2026-09-23T04:02:00Z — Intake checkpoint (10%)

- Hypothesis: for a compact convex body K in R^n with nonempty interior, n>=1, r>0 and every extreme point of norm >=r, equality in C2(K)>=[r²+(n+1)|g_K|²]/(n+2) occurs precisely for simplices with all vertices of norm r.
- Success: match the exact source problem; establish every geometric and integration step; search primary prior literature; if supported, publish a concise unrefereed proof with auditable supporting material, site, and manual Zenodo kit.
- Independent routes assigned: countable shell decomposition; finite approximation with a retained simplex; source/priority audit. No person contacted.
- Journal primary source confirms that Theorem 1.1 proves the inequality and polytope equality classification, followed by a general-body equality conjecture.
- Target problem website failed in web retrieval and returned HTTP 429 by direct request. Source matching remains pending.
- Repository is on main, origin https://github.com/AlecKriebel/Math.git. Existing unrelated modified/untracked files are excluded from this effort.
- No GitHub release or automatic Zenodo deposit is planned; user requested a manual upload package.

## 2026-09-23T04:07:00Z — Proof/source checkpoint (40%)

- Independent geometric review accepts the countable extreme-point simplex decomposition, including nonclosed extreme-point sets and coplanar facet boundaries.
- A distinct finite-approximation review proves strictness by retaining two fixed positive-volume simplices, avoiding reliance on an infinite decomposition.
- Browser access recovered the exact live catalogue statement: n>2, the precise centroid-term inequality, and the equality question. It agrees with OWR 53/2009 p. 2908 and FPS Theorem 1.1 p. 499. No scope gap remains.
- Correction adopted: nonregular inscribed triangles also attain the strengthened bound. The dimension restriction in the candidate's closing regularity comment concerns the weaker centered equality problem.
- Strongest verified result: the full claimed equality classification for all n>=1. Remaining work: complete priority search, concise publication artifacts and numerical sanity checks, final adversarial manuscript review, package and deployment.

## 2026-09-23T04:13:01+00:00 — Publication checkpoint (80%)

- Completed bounded priority audit: original sources, four citing primary works from combined citation indexes, and equivalent-formulation/author searches; no prior general equality resolution found. Historical priority remains unproved.
- Four-page manuscript drafted; final adversarial referee accepts all mathematical steps. Layout refined to remove overfull lines, with proof sections on separate pages.
- Exact verifier passes 298 checks in 18 cases under ordinary and optimized Python. Computation is auxiliary to the analytic proof.
- Checkpoint 49b9ec558 committed and pushed independent proof and source audits to main.
- Remaining: final package consistency/hash checks, site visual review and deployment, final commit and push.

## 2026-09-23T04:15:54+00:00 — Final local checkpoint (95%)

- Final manuscript and public-facing claims passed the adversarial review; small website precision edits were applied and independently closed.
- All four PDF pages visually inspected; final LaTeX build has no overfull/underfull warnings. Browser review confirms readable website and proof diagram.
- Paper source, exact verifier, audit trail, metadata, licenses, deterministic archives, and checksums assembled in the dedicated top-level project folder. GitHub Pages assets are a generated mirror under docs/papers/fps-equality.
- No person contacted, no Zenodo deposit initiated, and no GitHub release created.
- Remaining: final extraction/hash/link checks, commit/push, and verify live deployment.
