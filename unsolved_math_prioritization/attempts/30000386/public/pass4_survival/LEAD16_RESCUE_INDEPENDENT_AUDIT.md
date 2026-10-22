# Independent acceptance of the lead-sixteen rescue strategy

Auditor: survival lane, shared PASS4.

Reviewed artifact: `pass4_invariant/LEAD16_RESCUE.md`, SHA256 `fbcf3b299034bff78871b5b61b77f74f873f0a7cd9b963863c0c26a613f09438`.

**Verdict:** accepted as an infinite online winning strategy from the empty history when every effective announcement has lead at most sixteen. This does not establish the unrestricted conjecture or every finite maximum lead.

## 1. Small-set geometry

The expansion inequality is valid for arbitrary finite sets, including separated rows and columns: horizontal expansion adds at least two points in every occupied row, and vertical expansion then adds two in each of at least c+2 occupied columns. The missing-point assignment is injective because any center has at most one missing neighbor.

For 9 through 15 bombs the strict quadratic inequality and integrality give the stated cardinality bound. At sixteen bombs, the only equality case left by the expansion estimate has nine centers in three rows and three columns. The Cartesian-product and sumset-size argument forces a contiguous side-three square. Its four corner neighborhoods cover all twenty-five points, limiting the total holes to four and contradicting sixteen bombs. Thus the endpoint case is valid too.

## 2. Three-move online rescue

The first-announcement cases are exhaustive: an effective announcement at either remaining lethal time, or an irrelevant one. For a fixed first position the second move is losing exactly when every safe second position has at least eight preexisting terminal neighbors. This gives the displayed robust predecessor sets F1 and F2 with the correct order of choices.

In the delicate seven-terminal-bomb case, any augmented eight-neighbor center must contain all seven original points. Seven points fitting a side-three square span all three coordinate values in both directions, so that possible center is unique independently of the announced point. This validates the union over all possible announcements; it is not a separate favorable choice for each announcement.

The other cardinality cases give at most seven universally bad first positions. Removing one currently lethal site still leaves a choice among the nine legal moves. The subsequent second move may depend on the observed announcement, and the third survives any final announcement. No offline path substitution occurs.

## 3. Trigger chronology and reset

Before move s, fifteen distinct pairs at times s+1 and s+2 need fifteen distinct witnesses among rounds s-15 through s-1. Those fifteen rounds are therefore exhausted. A previously announced current bomb can only come from round s-16, and no other future preload exists. Thus every actual trigger satisfies the rescue hypotheses, including the first lethal move.

After rescue moves s through s+2 all trigger pairs have expired. Only the announcements made in those three rounds can remain pending, so reentry to ordinary mode has the guard and no inherited unaccounted preload.

## 4. No ordinary failure is missed

When the guard holds but no ordinary move is admissible, the local expansion lemma requires at least sixteen distinct pairs at the current and next times. Under maximum lead sixteen these exhaust rounds n-16 through n-1. The first fifteen were already visible at move n-1 at its next two times. An ordinary move there must trigger rescue. If that move is inside an earlier rescue, either n is also inside it or the clean reset leaves only three possible pending announcements. Both alternatives exclude the proposed ordinary failure.

This proves the induction from the genuinely empty initial history. It does not assert that every legally preloaded state is winning.

No correction is required.
