# Research log: hostile review of full-list three-color coupling

## 2026-07-28 16:01 PDT

- Froze candidate commit `db9c046d029b7d074676e658a9728e5fa2846ca9`
  and all five accepted dependency notes at their declared hashes.
- Replayed the candidate strict checker successfully.
- Traced Theorem 2.1 from the exact C-149/C-157 hypotheses.  Checked every
  occupancy, move edge, retained endpoint, domination inference, and palette
  inference.  In particular, the proof never turns \(v\notin Q(q)\) into
  \(vq\notin E(G)\).
- Wrote an independent set/frozenset graph and game implementation.  It
  imports no campaign implementation and independently recomputes
  \(\gamma,i,\alpha,\gamma^\infty,\theta\), both greatest families, all
  restricted peelings, palettes, ranks, named attacks, and ladder endpoints.
- Independently recovered the eight fixed-point-free three-color maps, with
  two directed 3-cycles and six 2-cycle-with-tail maps.
- Audited the discovery CNF semantically and independently reconstructed all
  variable/clause counts for orders 10 through 16.  The unlogged solver
  statuses remain `OBSERVED` and are not evidence for an exclusion.
- Verdict: **UNCONDITIONAL PASS**.  Estimated completion of this hostile
  review: **100%**.  Estimated contribution of this lemma toward the remaining
  all-three-empty rank-zero corridor subcase: **about 20%**; this is a workload
  estimate, not a probability that the conjecture is true.
