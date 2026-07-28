# Research log: hostile review of the terminal-completion layer

## 2026-07-28 16:46 PDT

- Froze candidate commit
  `e83ad600adcd1932ce9612239cf8a72b2f15a7a8` and checked every candidate
  source, manifest, strict-output, and accepted-dependency digest.
- Reconstructed Theorems 2.1 and 2.2 directly from the one-guard model.
  Audited every occupied set, move edge, successor, and use of domination.
- Checked the only unresolved named collision \(d=w\).  The correct
  conclusion is the candidate's closed-neighborhood statement
  \(d\in N_G[w]\); no loop edge is inferred.
- Audited the branch quantifier.  The response split guarantees at least one
  retained *reachable* state, while \(R_v,R_t\) are intentionally defined by
  state membership.  Exact controls contain retained branch states whose
  corresponding entry move is not an edge.  The formal theorem remains
  correct; informal “both branches survive” language must be read as state
  retention.
- Confirmed that the proof never converts palette or family nonmembership
  into a graph nonedge and makes no deletion-rank comparison.
- Wrote a clean-room adjacency-set/frozenset implementation and independently
  recomputed all three exact controls, including all five parameters,
  greatest families, restricted kernels/ranks, completion sets, response
  splits, witness covers, unique returns, and dominating pairs.
- Verdict: **UNCONDITIONAL PASS**.

Best-guess completion of this hostile review: **85%**.  Remaining work:
freeze review hashes, finish the strict runner and manifest, replay from
clean bytes, and commit/push only the review directory.

## 2026-07-28 16:52 PDT

- Froze the independent result at SHA-256
  `6a4dd3fbf82835b049d71717266e88a24436e1bc9c17558ac4230fd249bc4526`.
- Added a strict runner that checks the exact candidate commit, candidate and
  dependency hashes, the candidate replay, the independent replay, and the
  branch-state/move-edge distinction.
- Final verdict remains **UNCONDITIONAL PASS**.  No mathematical correction
  is required; the review records the terminology caution explicitly.

Best-guess completion of this hostile review: **100%**.
