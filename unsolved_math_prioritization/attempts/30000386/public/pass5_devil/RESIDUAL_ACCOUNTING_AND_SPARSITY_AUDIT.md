# Independent audit of residual accounting and heavy-layer sparsity

Reviewed artifact: Sections 2–4 of `pass5_multiscale/REPORT.md`, SHA256
`acdd49078fca3010de2682d4edf6cb27220034f9afcfea9e1581305ed840f26d`.

**Verdict: accepted without correction.** The construction is a legal safe history that refutes an automatic-flushing inference. It does not defeat an unrestricted Angel or disprove a closed geometric invariant.

## Exact residual identity

Old pending pairs split disjointly into expired pairs E, still-future but permanently unreachable pairs G, and retained relevant pairs. Newly surviving relevant pairs not already in the original set contribute U. The equality m_new=m−E−G+U follows. There are exactly ell announcement opportunities during ell moves, including the announcement immediately after the last move, so U≤ell. Duplicates cannot create a missing old contribution, and a previously unreachable pair cannot reenter a reachable cone.

Thus E>ell guarantees count decrease by expiry alone under the worst-case update bound; E+G>ell does so when endpoint-compatible spatial pruning is proved. The identity does not assert that these sufficient inequalities are necessary for an actual realized count decrease when U is smaller.

## Heavy-time density

For target times a,...,a+N−1, witnessing rounds lie in [a−H,a+N−2], containing N+H−1 integers. Each heavy target requires at least nine distinct effective position-time pairs, and each pair needs a distinct witnessing announcement round. This gives exactly 9K≤N+H−1. It supplies no long-gap or reset claim.

## Periodic counterexample

The prescribed leads are H+1−i for i=1,...,9, all within [1,H] when H≥9. Nine announcements complete before each target H+1+9j. The nine chosen sites are distinct and exclude the origin, so the stationary Angel survives every move.

At time H+1+9j+s, 0≤s≤8, exactly 9(j+1) pairs have expired and exactly n have been announced, giving H−8+s chronological pending pairs. Every ring site is relevant while future. Only the distance-two site can be pruned, and only one move before its target, at phase s=8. It has already been announced then even when H=9. The resulting relevant count is H−8+s for phases 0–7 and H−1 at phase 8. Its minimum is H−8; the relative configuration repeats every nine rounds after the initial transient.

The count replacement is exact over successive heavy periods. Therefore shared-budget sparsity does not itself force long heavy-free gaps, a small residual state, or strict pending-count decrease. A different Angel trajectory can change the geometry; the report explicitly preserves that limitation.

## Independent replay

`replay_periodic_history.py` independently regenerates every announcement from its absolute round, rather than updating the producer's pending-set recurrence. It checked H=9,...,200 and 81 post-transient times per H, totaling 15,552 states. All legality, stationary-safety, chronological-count and relevant-count checks passed. This finite replay corroborates the elementary all-H proof and is not its logical basis or a minimax search.

The stopping-time criterion in Section 1 is outside this scoped audit and has its own independent review.
