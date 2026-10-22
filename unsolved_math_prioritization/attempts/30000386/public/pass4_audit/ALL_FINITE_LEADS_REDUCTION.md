# Every finite maximum lead is equivalent to the unrestricted survival target

Shared PASS4 structural lemma. This proves the reduction and its exact quantifiers. It does not prove that every bounded-lead game is winning.

## 1. Precise hypothesis

For each positive integer H, let G_H be the original game with the sole additional restriction that every effective announcement made in round r satisfies 1≤t−r≤H. Past/current-time announcements remain ineffective and allowed. Positions are arbitrary, timestamps may repeat, and Devil observes the Angel move before announcing.

The hypothesis is:

For every finite H there exists one online Angel strategy sigma_H that survives forever from the empty initial state against every adaptive legal Devil in G_H.

The strategies may depend on H and need not agree on shared histories. Their bounds, memory, or descriptions need not be uniform in H. There is no hypothesis about arbitrary preloaded states.

Under this hypothesis the unrestricted game has one infinite online winning strategy. Conversely, an unrestricted winning strategy wins every G_H by restriction.

## 2. Exact finite-horizon simulation

Fix a terminal horizon T≥1 and choose H=T. Given an unrestricted announcement (p,t) in round r<T, retain it in a virtual G_H history when r<t≤T. Its lead then satisfies t−r≤T−1≤H. Replace every other announcement by a fixed legal ineffective announcement, for example (0,r).

The virtual Angel uses sigma_H. Its actual moves are exactly those prescribed from this virtual finite history. All retained pairs have identical safety effects in the actual and virtual games. A discarded pair is either expired/current at its announcement or detonates after T, so it cannot cause a loss through T. No round-zero announcement is created.

Thus the virtual strategy's safety through T implies actual safety through T.

### Adaptivity and discarded information

The replacement does not require the actual Devil to forget discarded values. For any fixed unrestricted Devil strategy tau, define a virtual Devil that internally simulates tau using the virtual Angel moves as its actual Angel inputs. It recursively reconstructs every original announcement that tau would make, keeps those values in its internal simulation, and emits their retained/replacement versions.

This is a legal nonanticipating virtual strategy: its internal history is a deterministic function of the observed Angel move sequence and the specified tau. Its next announcement can depend on the just-observed move, exactly as required. Off the resulting consistent history it can be defined arbitrarily. No future action is used.

Since sigma_H wins against every such virtual Devil, the actual simulated strategy wins through T against every unrestricted adaptive tau. This argument retains the order exists Angel strategy, then for every Devil strategy; it does not choose a path after a completed schedule.

If one instead defines a bounded-lead variant forbidding ineffective announcements, an irrelevant replacement can be a next-time bomb at a position outside the entire horizon-T reachable cone. The same finite-horizon argument works. Under the present contract the explicit current-time null action already suffices.

## 3. One strategy from all finite horizons

Let W_h be the full unrestricted game's winning set for h further moves, on full finite future-bomb states. The simulation gives empty∈W_T for every finite T. These are exact online winning predicates, not separate offline paths.

The W_h are nested. For a state B in their intersection, let A_h(B) be the immediately safe Angel moves such that every legal Devil successor belongs to W_h. Each A_h(B) is a nonempty nested subset of the same nine moves. Their intersection is nonempty. Choose its first member under a fixed ordering. Every Devil successor then remains in the intersection of all W_h, regardless of its arbitrarily distant position or timestamp. Repeating this rule yields one infinite online strategy.

This uses finiteness only of the Angel's action set. It does not invoke a finite-branching argument on the unbounded Devil action tree, and it does not assume sigma_H themselves converge or are compatible.

## 4. What is and is not required

- No H-independent tracking radius, speed, invariant, memory bound, or computational complexity is needed.
- No theorem for all preloaded states is needed. Winning from the genuine empty initial state for each H is sufficient.
- An algorithm producing sigma_H uniformly in H is not needed for the existence claim. The extracted infinite strategy is not automatically an effectively computable strategy; the target contract does not require computability.
- Merely surviving some H-dependent finite number of rounds is insufficient unless it covers every desired unrestricted horizon. A weaker sufficient hypothesis is winning horizon H in G_H for every H.
- A separate path for each completed bounded-lead schedule is insufficient; it has the wrong quantifiers.
- A strategy that ignores targets beyond H in the unrestricted game is not justified by this theorem. The virtual truncation is used only for a fixed finite horizon, followed by common-strategy extraction.
- A bad preloaded state compatible with maximum lead H is not a refutation of the empty-board hypothesis unless Devil can force entry into a losing state against every Angel response.

## 5. Consequence for a negative result

By the same finite-horizon dichotomy, if the unrestricted Angel has no infinite winning strategy, some finite full-game horizon T is losing. The horizon-T finite-cone game has the same effective moves as a bounded-lead game with H=T: all relevant attacks have lead at most T−1, and irrelevant attacks share a null effect. Therefore some finite H already has an empty-board finite-horizon Devil win.

This is a structural equivalence. It does not identify such an H or establish that a losing instance exists.
