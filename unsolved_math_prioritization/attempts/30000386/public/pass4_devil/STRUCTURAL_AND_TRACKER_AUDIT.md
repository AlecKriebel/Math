# Independent PASS4 audit: bounded-lead reductions and the exact local tracker defeat

## Accepted artifacts

1. `pass4_audit/ALL_FINITE_LEADS_REDUCTION.md`
   SHA256 `1680b4843f30390904a6dbd50d0cf5af560f7890530784967d6386fa9b4db7ca`.
2. `pass4_audit/BOUNDED_LEAD_FINITE_ARENA.md`
   SHA256 `0a46caf2242d3ea0e4e2f93247c537e56e4737a138f8bbac544287ce62d5176b`.
3. `pass4_coupling/LOCAL_TRACKER_LEAD16_DEFEAT.md`
   SHA256 `263f26f72b3dea150789ed7a419c0a9fa67cbf3a79dcab3fd938e877d2fbf5db`.

All three are accepted without required correction, with their stated scopes.

## All finite leads reduction

For a prescribed terminal horizon T, deleting or replacing announcements with targets later than T preserves safety through T. Every retained effective target has lead at most T−1. The original Devil may use discarded announcement contents as memory; the virtual Devil simulation explicitly reconstructs these contents from its specified strategy and the observed Angel moves, so the adaptive quantifiers are preserved.

The extraction of a common infinite strategy uses nested nonempty subsets of the Angel's nine moves. It does not incorrectly apply finite-branching compactness to the unbounded Devil action tree. The conclusion requires online winning for each bounded lead, but no uniformity or arbitrary-preload theorem.

## Exact finite arena

The relative cone has the asserted cardinality, by summing (2k+1)^2 for k=1,...,H. A bomb outside the cone cannot later reenter: distance decreases by at most one when its remaining time decreases by one.

For a pending pair of remaining time at least j, its witnessing announcement lies in the last H−j+1 rounds. This proves all tail bounds. One safe step shifts the j-tail into the previous (j+1)-tail; the subsequent single announcement preserves the bounds. For existential reachability, sorting k_i decreasingly and assigning round H−i+1 gives lead k_i+i−1≤H, including ties. All targets exceed H, so the stay-put realization is safe during setup.

The greatest-fixed-point calculation is exact because future legality and death depend only on the normalized pending state, and all future effective actions have representatives in the finite cone. It establishes decidability, not a practical computation or a result for arbitrary H. The displayed sixteen-pair trap is existentially reachable under cooperation, which does not show strategic forceability.

## Exact local tracker defeat

The announced time-17 set has seven sites through move 16; hence it never removes any candidate under the threshold-eight guard. The time-18 set cannot affect that guard before move 17. Thus every admissible move set through move 16 is the full neighborhood, and the stated deterministic, known-reference policy follows its bomb-free path exactly.

The round allocation is legal: one time-17 site at round 1, eight time-18 sites at rounds 2–9, six time-17 sites at rounds 10–15, then one site at each of rounds 16 and 17. The maximal lead is 16. The final two announcements leave exactly one safe move c at time 17 and complete N(c) at time 18. If the guard becomes empty at time 17, any game-legal surviving continuation still has to use c and loses next.

The prediction of the move-16 position relies on the stated policy restriction. A full-history controller can react to distant bombs while its local guard remains unchanged. The result therefore defeats this exact tracker from the empty state, not all Angel strategies. It is consistent with the independently proposed W2-invariant lead-16 survival strategy.
