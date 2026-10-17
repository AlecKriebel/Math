# Acceptance: concentration profiles and the allowed set {13,17,21}

Shared PASS2 independent audit. The two authored inputs are `../pass2_invariant/CONCENTRATION_PROFILE_LEMMA.md` and `../pass2_invariant/THREE_DEADLINES_13_17_21.md`. Exact hashes are pinned in the accompanying acceptance manifest. The unrestricted game remains unresolved.

## Verdict

Accepted. The concentration-profile lemma is a valid online terminal bound and boundary reduction. Its concrete application gives one online strategy winning against every adaptive Devil whose allowed timestamps are exactly the prescribed set {13,17,21}. The earlier estimate's failure on this set was only a failed bound; this new proof supplies a valid sufficient certificate.

## 1. Concentration-profile chronology

For each permitted nonnegative update kernel K_j, let c(q) bound its average over every translated axis-aligned q-by-q lattice square. An adaptive choice of update type and translation is covered by taking the maximum over types and all square locations. If an actual increment is merely bounded pointwise by such a translate, its square average obeys the same bound.

Start after a boundary announcement with r moves remaining, a centered side-L initial square containing current mass M, L the largest power of three at most 2r+1, and w=r−(L−1)/2. Waiting w rounds raises that square's average by at most w c(L). At each subsequent scale 3q, a least-average child square has average no larger than its parent's. Its center is reached in q legal king moves, and exactly q updates occur during that traversal, including the one after arrival. Each raises that fixed chosen square's average by at most c(q).

At the final side-three square, exactly one Angel move remains. All nine cells are reachable, so its least-valued cell gives

terminal field ≤ M/L² + w c(L) + sum_(q=3,9,…,L/3) q c(q).

The last included update is at terminal time minus one. No update after the terminal move is observed early or credited against its immediate safety test. Intermediate positions are safe under the stated hypothesis that there is no intermediate lethal timestamp.

The elementary bound c(q)≤max_j min(beta_j/q²,alpha_j), with total kernel mass beta_j and peak alpha_j, follows from two separate upper bounds on local mass. It is valid even if the maximizing update type changes from scale to scale or round to round.

## 2. General boundary reduction

Write A_r(c) for the traversal/wait expression above. If

D=L²[1−A_r(c)−c(L)]>0,

then the proposed earlier field

f(a)=current-deadline indicator at a + local side-L downstream g-mass divided by D

has the required robust implication. A value f(a)<1 excludes a current bomb and gives pre-announcement downstream mass M<D. The immediately following announcement increases that local mass by at most L²c(L). Applying the terminal lemma after the update gives a downstream value strictly less than

D/L²+c(L)+A_r(c)=1.

Convolution with the symmetric side-L square indicator, divided by D, gives exactly the stated new update kernels. The current-deadline update contributes the delta kernel. Repeated bombs only decrease actual increments relative to these kernel bounds.

For recursive use, the next deadline must be the next allowed lethal time, and g<1 must itself certify safe robust continuation for the complete later state. Starting from the final-deadline indicator and recursively applying this reduction supplies that meaning. The lemma does not prove positive denominators or an initial bound below one for every allowed set.

## 3. Complete audit of the concrete triple

Let Q=[−4,4]² and U=1_Q, with |Q|=81. All indicator fields below refer to announcements observed at the relevant time.

### Acceptance at time 17

Set g=b_17+(U*b_21)/53. If g(a_17)<1, the current time-17 move is safe and the integer count of time-21 bombs in a_17+Q is at most 52. The subsequent round-17 announcement can raise it to at most 53. The gap-four robust terminal construction has side nine, no waiting, and threshold C=54, so this post-announcement state is winning for time 21.

Thus g<1 is a robust pre-announcement acceptance predicate, rather than merely an endpoint safe for one timestamp.

### Acceptance at time 13

Each g update has total mass at most beta=81/53: a time-17 bomb adds one, a time-21 bomb adds 81/53, and a time-13 update has no effect on g. Put

D_2=81−28 beta=2025/53,

f=b_13+(U*g)/D_2.

If f(a_13)<1, the move is safe and the current local g-mass in a_13+Q is strictly below D_2. The round-13 update adds at most beta. During rounds 14,15,16, the Angel traverses to the selected side-three square, receiving exactly three further g updates. Its time-17 terminal value is strictly below

(D_2+beta)/81 + beta/3 = 1.

This accounting reserves the boundary update separately from the three traversal updates. There are no lethal times 14–16 or 18–20, so the two terminal traversals do not omit any death checks.

### Producing f(a_13)<1 online

The three f update kernels have exact mass/peak bounds:

- time 13: delta, mass 1, peak 1;
- time 17: U/D_2, mass 53/25, peak 53/2025;
- time 21: (U*U)/2025, mass 81/25, peak 1/25.

For the last peak, the convolution's largest overlap is 81, attained at zero. Total mass is 81²/2025=81/25.

At T=13 the ternary initial square has side 27 and no waiting. The first traversal has length nine and target square side nine, covering announcements 1–9. The second has length three and target square side three, covering announcements 10–12. The final move is at 13.

The two-norm profile bounds are c(9)≤1/25 and c(3)≤1/9. Therefore

f(a_13)≤9/25+1/3=52/75<1.

Each child choice uses only the currently observed field, while every later update is bounded uniformly over all target locations and update types. No future target information is assumed.

The strict first inequality, the strict local-mass acceptance, and the integer reserve at time 17 jointly establish survival at 13,17,21. Afterwards every allowed time has passed. This completes the restricted online proof.

## Scope

The profile improvement is real: a future smoothed target with large total mass has a smaller peak, so it cannot behave like the current-deadline delta at every spatial scale. Nothing here establishes that the recursion succeeds for all triples or all finite allowed sets. Failure of a later denominator or initial estimate would remain a failure of this sufficient certificate, not a losing-game proof.
