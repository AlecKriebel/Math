# Nonuniform resets, residual accounting, and the limit of heavy-layer sparsity

## Final result and scope

No strategy for every finite maximum lead H was obtained in this final shared pass. This lane proves an exact history-dependent reset criterion and identifies a sharp obstruction to obtaining its reset hypothesis from heavy-layer sparsity or net pending-count arguments alone.

The obstruction is a legal infinite **safe** play with a full one-announcement-per-round budget, periodic heavy deadlines, and a permanently large residual state. It is not a Devil-winning strategy. It does not rule out a geometric, history-aware admissible-state invariant.

All statements use the original Angel-first king-move game. The accepted earlier results are unchanged. No further fixed deadline count or fixed H is claimed.

## 1. History-dependent positive-reset criterion

Fix a finite maximum lead H. Let P be a family of complete post-announcement states or histories, including position, all relevant pending pairs, controller memory, and previously revealed private randomness. At time zero, use the prescribed empty initial state without a round-zero announcement.

Suppose one legal nonanticipating randomized episode policy has these properties:

1. The initial state is in P.
2. Starting from every actual state/history in P, and against every adaptive legal Devil continuation, the policy has strictly positive probability of reaching a later finite stopping time tau at which all moves up to tau have survived and the complete state after the round-tau announcement is again in P.
3. The stopping decision is made from the information actually available by tau. Future private draws cannot be inspected early. The policy is defined on all hypothetical failure branches.
4. On a successful return it starts another episode according to the same prescribed rule, with fresh randomness revealed only at its stated times.

The episode length and its positive success probability may depend on the full initial state and subsequent history. There need be no deterministic duration bound, no uniform success probability, and no positive probability of infinitely many successful episodes.

**Theorem.** These hypotheses imply a deterministic infinite Angel-winning strategy for the lead-H game.

**Proof.** Fix an adaptive Devil. The probability of one finite successful episode is positive. Conditional on any finite sequence of successful returns, the actual complete state is in P, and the conditional probability of the next finite successful return is positive. Integrating this positive conditional probability over the positive-probability preceding success event gives positive probability of one more successful episode.

Thus, for every integer m, there is positive probability of m successive finite successful episodes. Every episode consumes at least one physical move. Taking m equal to a desired finite horizon T therefore gives positive probability of survival through T. This reasoning does not condition a future random draw on a favored success event and then declare it fresh; the required conditional success property is assumed at each actual return history.

A Devil strategy winning by horizon T would defeat every random realization, contradicting the positive probability just obtained. Finite-horizon determinacy followed by the accepted compactness extraction over the Angel's nine actions gives a deterministic infinite strategy.

**What this does not prove.** Neither P nor a successful episode policy is constructed here. A return with a safe endpoint but an uncontrolled residual configuration does not meet condition 2. Reaching an endpoint whose residual state would be winning from some other position also does not meet it. The endpoint announcement is part of the required reset, not an action deferred outside the certificate.

This extends the accepted deterministic-boundary positive-block criterion to genuinely history-dependent finite stopping-time resets. It is a sufficient criterion, not a probabilistic shortcut around an unproved continuation state.

## 2. Exact residual accounting through a successful episode

At a post-announcement state at time n, let B be the finite set of relevant pending pairs, with m=|B|. Relevance means that the position can still be reached by its target time from the current location. An already unreachable pair cannot become reachable later along a legal path, by the triangle inequality.

Suppose an episode lasts ell moves and survives through its endpoint at time n+ell, including observation of that endpoint's announcement. Define:

- E: the number of old pairs in B whose target times are at most n+ell;
- G: the number of the remaining old pairs that are no longer reachable by their targets from the endpoint;
- U: the number of distinct relevant pending pairs at the endpoint that were not in B and arose during the episode.

Then the exact count identity is

`m_new = m-E-G+U`, with `0<=U<=ell`.

The ell bound includes the endpoint's announcement. Repeated pairs and ineffective announcements can only reduce U. Consequently

`m_new<=m-E+ell`.

A strict decrease justified solely by expiry requires `E>ell`. A claim that an episode clears q old bombs but lasts ell moves must account for all ell new announcements, even if some target times lie beyond the episode. Those are precisely the residual bombs that an endpoint-only certificate can miss.

If spatial pruning supplies a certified G, then `E+G>ell` suffices for net count decrease. But the relevant G depends on the actual safe endpoint. It cannot be borrowed from a separately chosen escape path that is incompatible with the episode's lethal-time constraints.

An integer residual rank can make a nonuniform reset proof finite: if every rank-positive admissible state has a positive-probability safe episode ending in the same admissible family with strictly lower rank, repeated episodes reach the rank-zero family after finitely many successes. A usable theorem must still prove admissibility and robust continuation for that rank-zero family. Counting alone does not supply either condition.

## 3. What the shared budget really implies about heavy deadlines

Call a target time heavy if at least nine distinct positions were effectively announced for it before that time. Consider N consecutive target times under maximum lead H. Every announcement witnessing one of these heavy layers lies in an interval of at most N+H-1 rounds. Distinct position-time pairs require distinct announcement rounds. Therefore

`9 * number_of_heavy_times <= N+H-1`.

This is a genuine shared-budget bound. It gives asymptotic density at most one heavy time per nine rounds. It does **not** imply that arbitrarily long heavy-free intervals occur, that all pending bombs expire during such an interval, or that the residual count decreases across heavy episodes.

The next construction attains that asymptotic density while maintaining a large residual state.

## 4. A periodic, budget-saturated, safe counterexample to automatic flushing

Fix any H>=9. Let

`P = ({-1,0,1}^2 minus {(0,0)}) union {(2,0)}`,

a set of nine distinct nonzero sites, each at king distance at most two from the origin. Choose any fixed ordering p_1,...,p_9 of these sites.

For every j>=0 and i in {1,...,9}, in round

`r=9j+i`

announce

`(p_i, T_j)`, where `T_j=H+1+9j`.

There is exactly one announcement in every round. Its lead is

`T_j-r=H+1-i`,

which ranges from H down to H-8 and is positive. Thus every announcement obeys the same maximum-lead-H rule. All nine announcements are made before T_j, so every T_j is heavy.

Now let the Angel stay at the origin forever. This is a legal safe play, because the origin is never targeted. The construction therefore does not force a loss; its purpose is to test the proposed reset inference.

### No long heavy-free interval

The heavy target times are exactly H+1, H+10, H+19, and so on. After the initial transient they are separated by nine rounds. There are never nine consecutive heavy-free target times. In particular, sparsity does not provide a heavy-free window of length H when H>=9.

### Pending count never becomes small

At a post-announcement time

`n=T_j+s`, where `0<=s<=8`,

exactly `9(j+1)` previously announced pairs have expired. Exactly n pairs have been announced in total, with no duplicate pairs. Hence the number of chronologically pending pairs is

`m_n=n-9(j+1)=H-8+s`.

It cycles through H-8,...,H indefinitely. Every interval from one heavy time to the next expires nine old pairs and permits exactly nine new announcements. The net count decrease is zero.

### Spatial pruning does not produce a small reset either

Along the stationary path, all ring sites are relevant until their deadline. The only possible irrelevant pending pair is the site (2,0) when its target is one move away. There is at most one such pair, and it occurs exactly at s=8 in the above cycle, when the chronological count is H. Thus the relevant pending count is

- H-8+s for 0<=s<=7;
- H-1 for s=8.

Its minimum is H-8. The complete relative pending configuration repeats after nine rounds once the initial transient has passed. Therefore no reset to a residual-count bound independent of H follows from heavy-layer sparsity, expiry, or automatic spatial pruning in this legal play.

For any proposed fixed residual threshold K, choosing H>K+8 keeps the relevant count above K forever. Any successful proof must either allow a nonempty residual admissible family or supply an additional geometric control argument that changes this history. The example is not a proof that another Angel policy cannot change it.

## 5. Why the original reset proposal remains unproved

The proposed mechanism was to control weak layers, wait for sparse heavy episodes to pass, and then restart with a sufficiently small residual state. Sections 3–4 show that the budget bound alone does not provide the required flushing or rank decrease. A heavy layer may consume nine announcements over nine rounds, and its expiry may be exactly replenished by the next nine announcements.

The positive-reset theorem in Section 1 still permits a residual state of large cardinality, provided it belongs to a rigorously closed family P. But such a family must retain geometry, timestamps, and the actual endpoint. Separate certificates for active-episode survival and residual-state viability do not automatically certify their intersection. The independent residual-composition lane supplies an explicit geometric example of that failure; it is not duplicated here.

The final missing object is therefore a complete-state, history-aware admissible family together with a safe, nonanticipating episode transition that returns to it under every allowed adaptive continuation with positive probability. Neither density one-ninth nor the count identity constructs that object.

## 6. Final pass disposition

No all-H construction, no unrestricted Angel strategy, and no legal forcing strategy from the empty history were established by this lane. The exact reset criterion and residual identities are valid conditional tools; the periodic schedule is a sharp counterexample only to an automatic-reset inference based on sparsity and counts. The full target remains unresolved after the fifth shared mathematical pass.
