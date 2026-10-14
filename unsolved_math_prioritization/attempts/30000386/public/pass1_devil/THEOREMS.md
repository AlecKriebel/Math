# Time-Bomb game: restricted-policy obstructions and offline separation

## Scope and rules

These are partial results for the two-dimensional, speed-one Time-Bomb game. The Angel moves first in round n, from a_(n−1) to a_n with maximum-coordinate distance at most one. The Devil then announces one pair (p_n,t_n). An announcement is lethal only on the named future move. There are no initial announcements. Multiple announcements may have the same detonation time.

The shared construction contract has SHA-256 `1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c`.

None of the results below proves or disproves survival against unrestricted adaptive Devil play. In particular, a Devil victory against a restricted family of Angel policies is not a victory in the full game.

## 1. Every fixed schedule leaves many ballistic paths alive

**Proposition 1.** Fix in advance any infinite legal sequence of announcements (p_r,t_r), one per round r. For (u,v) in [−1,1)^2 define

    a_n(u,v) = (floor(nu), floor(nv)).

These are legal paths from (0,0). Under normalized Lebesgue measure on the parameter square, the set of paths that survive every announcement has measure at least

    1 − (ζ(2)−1)/4 = (5−ζ(2))/4 > 3/4.

Numerically this lower bound is approximately 0.8387664833.

**Proof.** For any real w in [−1,1), floor((n+1)w)−floor(nw) belongs to {−1,0,1}, so every path is legal, including negative velocities. For a fixed positive integer t and integer cell p=(x,y), the condition a_t=p restricts u to [x/t,(x+1)/t) and v to [y/t,(y+1)/t), intersected with the parameter square. Its normalized area is at most 1/(4t²).

An announcement in round r can kill only if t_r≥r+1. Consequently the union of the parameter sets killed by all lethal announcements has measure at most

    sum_(r≥1) 1/(4t_r²) ≤ sum_(r≥1) 1/(4(r+1)²) = (ζ(2)−1)/4.

This countable union bound permits repeated target cells and repeated detonation times. Nonfuture announcements are simply ignored. Finally sum_(k≥2)1/k² < integral_1^∞ x^(−2) dx = 1, proving the elementary lower bound greater than 3/4 without evaluating ζ(2). ∎

**Quantifiers.** This is an offline statement:

    for every fixed schedule, there exists a ballistic path surviving it.

Equivalently, sampling the two velocities once gives the displayed survival probability against every fixed schedule that is independent of the sampled velocities. It does not produce an online winning strategy against an adaptive Devil.

## 2. One adaptive Devil defeats that entire ballistic family by move 8

**Proposition 2.** There is a legal adaptive Devil strategy which defeats every path of the exact form a_n=(floor(nu),floor(nv)), with fixed (u,v) in [−1,1)^2, no later than move 8. The result remains valid if the velocities are sampled privately and the Devil does not know them.

**Strategy and proof.** In rounds 1, 2 and 3 announce irrelevant past/current-time pairs. After observing a_4=(x,y), form the four cells

    (2x,2y), (2x+1,2y), (2x,2y+1), (2x+1,2y+1).

Announce these in that order in rounds 4, 5, 6 and 7, all with detonation time 8. Every announcement is made strictly before its detonation time.

The identity

    floor(2z) ∈ {2 floor(z), 2 floor(z)+1}

holds for every real z, including negative z. Applying it to z=4u and z=4v shows that a_8 is one of the four announced cells. Thus the Angel loses at move 8. ∎

**Why this does not conflict with Proposition 1.** The four time-8 target cells depend on a_4, which depends on the sampled velocities. The probability estimate for a fixed target cell cannot be applied conditionally as if this target were independent of the observed path. Each realized branch of the Devil strategy still has surviving ballistic paths, but those other paths need not generate that branch.

**Scope limitation.** An unrestricted Angel can change its later movement after the announcements. This strategy does not trap such an Angel; it traps the fixed-velocity family because its four possible time-8 endpoints were already determined by the observed time-4 position.

## 3. Every bounded-lookahead policy fails

A deterministic policy has **time lookahead H**, where H is a nonnegative integer, if its choice at move n is independent of the positions and timestamps of all previously announced bombs with detonation time greater than n+H, once its past Angel positions, n, and the retained announcement history are fixed. The retained history records the announcements with detonation time at most n+H, together with their announcement rounds. This is a restriction on the policy, not a restriction in the original game.

**Proposition 3.** Every deterministic time-lookahead-H Angel policy can be defeated by a fixed nonadaptive schedule in which every relevant bomb has one common detonation time

    K = (2H+3)²,       T = K+H+1.

The schedule may be selected after the policy is specified.

**Proof.** Consider histories whose first K announcements all have time T. For each move n≤K, one has n+H≤K+H=T−1, so none of these bombs appears in the policy's retained history. By induction, the positions a_1,…,a_K are independent of all K target cells. Thus the Devil can compute a_K=c from the given deterministic policy before selecting its schedule.

There are exactly K cells in

    c + {−H−1,…,H+1}².

Announce all of them, one per round 1,…,K, each with time T. All of those announcements occur strictly before T. From c at time K, any legal path can travel maximum-coordinate distance at most T−K=H+1 by time T. Its time-T position is therefore among the announced cells, so it loses then. Subsequent announcements, if needed, can be irrelevant. ∎

The proof remains valid if the policy is told the common detonation time T in advance: its prefix may depend on T, but still cannot depend on the ignored target cells. It also remains valid if it knows the number and announcement rounds of ignored messages, because these are fixed in this construction. It does not cover a policy that uses remote target cells to change its prefix.

For H=0 the construction kills on move 10. For H=1 it kills on move 27. Thus a policy that only checks current or finitely many impending layers cannot be extended to a solution merely by reusing that fixed lookahead forever.

## 4. A quantitative obstruction to slowly increasing lookahead

Let h: positive integers → nonnegative integers be nondecreasing. A time-lookahead-h policy retains at move n only announcements with time at most n+h(n), in the same precise sense as above.

**Proposition 4.** If for some positive integer m,

    m ≥ (2h(m)+3)²,

then every deterministic time-lookahead-h policy can be defeated by a fixed nonadaptive common-time schedule. Set R=h(m)+1 and T=m+R. The first m moves ignore all time-T targets, so a_m is predictable. Announce every cell of its radius-R maximum-coordinate square by round m. The displayed inequality supplies enough announcement rounds, and every possible time-T endpoint is covered. Extra announcement rounds may repeat one of those targets. ∎

A necessary condition for a nondecreasing-lookahead policy to be a universal winning strategy is therefore

    h(m) > (sqrt(m)−3)/2    for every positive integer m.

In particular h(m)=o(sqrt(m)) is insufficient, as is h(m)≤c sqrt(m) eventually for any fixed c<1/2. This is only a necessary condition within this policy class, not a sufficient construction at or above the threshold.

**Without monotonicity.** The same proof works whenever there are integers m,R≥1 such that (2R+1)²≤m and n+h(n)<m+R for every 1≤n≤m. Monotonicity above is merely an easy way to verify the latter condition.

## 5. What remains open in this analysis

The full Angel may react immediately to any announced future target and may continually change direction or scale. Neither the ballistic trap nor the lookahead trap handles that behavior. A proof of survival must accommodate information from arbitrarily distant future times; the offline measure estimate alone provides no adaptive guarantee. A proof of defeat must force confinement despite those reactions. No such unrestricted strategy has been obtained here.
