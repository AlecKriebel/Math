# Shared PASS1 independent game audit

## Verdict and scope

The full two-dimensional Time-Bomb conjecture is not resolved. The following partial results are accepted under the shared construction contract and independent source acceptance contract:

1. Exact finite-horizon online minimax recurrence and finite-cone state reduction, preserving all adaptive choices.
2. Compactness from online wins at every finite horizon to one infinite online winning strategy, despite unbounded Devil announcements.
3. A concrete online strategy surviving through move 17 in the full two-dimensional game.
4. The supplied one-dimensional common-time-6 Devil certificate, independently replayed in absolute coordinates on all 729 Angel move words.
5. Defeat of deterministic bounded-time-lookahead policies, and its stated increasing-lookahead extension.
6. Fixed-schedule infinite offline path existence, including in one dimension; the fixed-schedule ballistic measure bound; and adaptive defeat of the entire fixed-velocity family by move 8.
7. The two stated static-invariant obstructions, within their explicitly preloaded/existential-history scope.
8. A single legal adaptive Devil strategy forcing square-root-scale deviations from every constant-velocity line in any infinite surviving play.

No offline result is accepted as an online game proof. No restricted-policy or one-dimensional loss is accepted as a full two-dimensional Devil win. No finite set of horizon tests is accepted as infinite survival.

The reviewed source normalization is Angel first, safety checked only against earlier announcements, followed (if alive) by one adaptive Devil announcement. The bomb budget is per announcement round; distinct bombs may share a detonation time. Current/past-time announcements have no retroactive effect.

## 1. Independent exact finite-horizon state reduction

Fix an absolute terminal horizon H. Immediately before the next Angel move, let the current absolute time be m, current position be a, and remaining number of moves be h=H−m. An earlier announcement (p,t) matters for this continuation exactly when

- 1≤t−m≤h, and
- ||p−a||∞≤t−m.

Retain its relative pair (q,k)=(p−a,t−m). Collapse repeated pairs. The retained finite set B is contained in

C_h = { (q,k): 1≤k≤h, q∈Z², ||q||∞≤k }.

### Why discarded pairs cannot matter

Expired pairs are never lethal again. Pairs after H are outside the objective. A pair with ||q||∞>k cannot be reached at its time. Moreover, after a legal step s with ||s||∞≤1,

||q−s||∞ ≥ ||q||∞−1 > k−1.

Thus a spatially discarded pair cannot enter any descendant reachable cone. This is a permanent irrelevance statement for the specified continuation, not a heuristic distance cutoff.

The cone has exactly

|C_h| = sum from k=1 to h of (2k+1)² = 4h(h+1)(h+2)/3+h

pairs. At depth H−h from the empty initial board, at most H−h distinct retained pairs exist. An upper bound for the number of possible normalized bomb sets at that depth is therefore the sum of binomial(|C_h|,i) over 0≤i≤min(H−h,|C_h|). No enumeration outside this finite state space is needed for the horizon-H objective.

### Exact alternating recursion

Let M={−1,0,1}². For a candidate move s∈M, reject it if (s,1)∈B. Otherwise define

T_s(B) = { (q−s,k−1): (q,k)∈B, k≥2, ||q−s||∞≤k−1 }.

The remaining horizon is h−1. The Devil has the following complete list of effective action types after observing s:

- add any one d∈C_(h−1), including a pair already present; or
- do nothing effective, denoted ⊥.

The latter is a genuine legal action type, represented for example by an announcement at the current absolute time. Every announcement outside C_(h−1) has this same effect through H. Write X+⊥=X and X+d=X∪{d}.

Then

W_0(B)=true,

W_h(B) iff there exists s∈M with (s,1)∉B such that, for every d∈C_(h−1)∪{⊥}, W_(h−1)(T_s(B)+d).

This recursion places Angel's existential move before Devil's universal response at every round. Induction on h establishes exact equivalence with a history-dependent online strategy surviving h more moves. If the condition is false, each Angel move either loses immediately or has an effective Devil response leading to a losing (h−1)-move state, which gives a finite-horizon adaptive Devil strategy.

### Why dropping observed information preserves strategy quantifiers

Different discarded announcements can carry different numerical information, but they change neither legal movement nor any future safety test within this horizon. At every surviving history the same effective Devil continuation choices remain available, with no additional budget or restriction depending on those discarded values. Backward induction therefore assigns identical continuation values to histories with the same normalized state. A winning state rule can ignore discarded data; a losing-state Devil response can be lifted to a legal original announcement after each observed Angel move. This addresses both full-history adaptivity and information carried by irrelevant actions.

The executable specification `finite_game_reference.py` implements this recurrence without symmetry reductions or search pruning. Its small smoke tests confirm full-game wins for horizons 1–4. The tests are not needed for the analytic survival-17 result and assert no larger computed horizon.

## 2. Compactness with an infinitely branching Devil

For this argument use full finite future-bomb states, not a horizon-dependent truncation: B may contain any finite set of pairs (q,k) with k≥1. The full successor shifts all unexpired pairs and adds any one future pair or an ineffective announcement. Let W_h be its h-move winning set. The finite-cone theorem above computes the same predicate after projection to C_h.

The sets satisfy W_(h+1)⊆W_h. Define W_∞ as their intersection. For B∈W_∞ define A_h(B) to be the immediately safe moves s∈M for which every legal Devil successor lies in W_h. Each A_h(B) is nonempty because B∈W_(h+1), and these are nested subsets of the fixed nine-element set M. Their intersection is nonempty.

Choose the first member of this intersection in a fixed ordering. For every Devil announcement d and every h, the resulting successor lies in W_h, hence in W_∞. Applying the same rule at each subsequent state maintains membership in W_∞ and never takes a lethal move. This is one online state-based strategy against every adaptive Devil.

Only the Angel's move set must be finite in this argument. There is no unjustified use of König's lemma on an infinitely branching Devil game tree, and no interchange of existential Angel choices with universal Devil choices. The universal quantifiers over h and d commute after the common Angel move has been selected.

Consequently, wins from the empty state for every finite horizon imply an infinite win. Conversely, if no infinite Angel strategy exists, some finite-horizon game is losing and finite-horizon backward induction gives a Devil strategy with a uniform finite loss bound. This is a structural statement, not evidence that any particular untested horizon is winning or losing.

## 3. Independent geometric proof and survival through move 17

For q∈Z² let N(q)=q+M. Suppose ∅≠Q⊆N(a), and a finite set B satisfies |B∩N(q)|≥8 for every q∈Q. Set k=|Q| and C=the union of N(q) over q∈Q.

Write r for the number of occupied rows of Q and c for its occupied columns. Expanding Q horizontally adds at least two cells in each nonempty row, giving at least k+2r cells. That horizontally expanded set has at least c+2 nonempty columns. Vertical expansion adds at least two cells in each of those columns. Therefore

|C| ≥ k+2r+2c+4.

Here 1≤r,c≤3 and k≤rc. Since (r−2)(c−2)≤1, we have rc≤2r+2c−3. Consequently |C|≥2k+7.

Every neighborhood N(q) contains at most one hole from C\B. Assign each hole to any center q whose neighborhood contains it. Two distinct holes cannot be assigned to the same center. Thus |C\B|≤k, giving

|B| ≥ |B∩C| ≥ |C|−k ≥ k+7.

This proof is independent of the author's case split. A supplementary exact enumeration checks the neighborhood-union inequalities for all 511 nonempty Q⊆M; it is recorded in `finite_game_smoke_tests.json`.

### Guard strategy and exact timing

At move n let a=a_(n−1), let A be the already announced time-n positions, and B the already announced time-(n+1) positions. Maintain |A∩N(a)|≤8, so Q=N(a)\A is nonempty. It holds before move 1.

For n≤16, there are at most n−1≤15 previous announcements. If every q∈Q had at least eight next-time bombs in N(q), the lemma would give |B|≥|Q|+7. Also |A|≥9−|Q|. These are different spacetime pairs because their times differ, even when their spatial positions coincide, so they require at least 16 earlier announcements. This is impossible.

Choose a safe q∈Q with at most seven already announced next-time bombs in N(q). After this move the Devil can add at most one such bomb, leaving at most eight for move n+1. This preserves the invariant through moves 1–16. At move 17, take any remaining safe move. Nothing is claimed about maintaining the guard after that final move.

The proof handles repeated pairs, repeated sites, multiple bombs at one future time, and adaptive announcements. Its generalization to a restricted Devil with at most 15 distinct preexisting pairs in every pair of current/next time layers is also correct.

A 16-pair preloaded obstruction is valid: eight current-time bombs leave just one immediate choice q, while eight next-time bombs surround q; Devil adds the ninth after observing that forced move. This shows the local threshold is sharp for arbitrary states. It does not show that the Devil can force such a state from the empty initial board.

## 4. Independent replay of the one-dimensional certificate

Audited certificate: `../pass1_survival/terminal_1d_horizon6_certificate.json`.

- SHA-256: `2cae818fae1b394cf439ca5ebcfff410f50650fab70cc7c5f6cc3f2882c6c206`
- Size: 4,133 bytes
- Eight canonical states; one terminal state
- Every bomb has detonation time 6

The independent program `replay_1d_certificate_independent.py` imports none of the author's solver, generator, or verifier. It enumerates all 3^6=729 complete Angel move words, retains every actual absolute-coordinate bomb, lifts each reflected certificate response back to actual coordinates, verifies each child state against the full announcement history, and checks that the final Angel position is among the five bombs announced in rounds 1–5. Every word passes; every listed certificate state is visited. Four explicit absolute-coordinate traces are included in `independent_1d_replay.json`.

The first bomb is placed at the observed a_1, so there is no preannouncement or prediction of the first move. Responses are selected after the corresponding Angel move. Canonical reflection is implemented with a tracked orientation; it is not assumed that the real Angel has moved in canonical coordinates. No bomb is lethal before move 6, and no announcement at move 6 is used.

The source solver's omission of an explicit ineffective announcement is harmless for h≥2: adding any available in-cone bomb weakly favors Devil, because a strategy safe against a superset of forbidden pairs is safe against a subset. If all such additions leave winning states, an ineffective announcement does too. Its h=1 base case separately checks immediate safety. This validates the solver's action-domain reduction for its reported common-time horizons 1–5, though the independent exhaustive replay here establishes only the horizon-6 loss certificate.

The result applies to the one-dimensional three-move game. A transfer to a fixed coordinate is valid only when that terminal coordinate is deterministically prescribed and known, so the Devil can attach it to every one-dimensional target. It is not a loss proof for the unrestricted two-dimensional game.

## 5. Deterministic time-lookahead obstruction

Use the following precise policy restriction. At move n, histories with identical previous Angel positions and identical announcement histories after replacing every pair with t>n+H by a common blank produce the same move. Announcement-round indices may be retained. In particular, a policy cannot use a stored summary of ignored target positions. H is a fixed nonnegative integer.

Set K=(2H+3)² and T=K+H+1. In any history whose first K announcements all have time T, none of their target positions is visible to the policy during moves 1 through K: T>n+H throughout. Inductively those Angel positions, including c=a_K, are independent of the K target positions. Thus c can be computed before specifying the schedule; there is no circular dependence.

During rounds 1 through K, announce every cell of c+[-H−1,H+1]², all for time T. There are exactly K cells. The announcements are strictly earlier than T. From a_K=c, the Angel has only T−K=H+1 steps before T, so every legal time-T endpoint is already bombed. Later motion after targets become visible cannot escape this radius. This is a fixed schedule tailored to the specified deterministic policy.

The theorem is accepted for this policy class. It is not a defeat of arbitrary online policies or privately randomized policies. Knowing T in advance does not defeat the argument if ignored target cells still cannot affect the prefix; the prefix may simply depend on T.

For nondecreasing integer h(n), the same proof works whenever m≥(2h(m)+3)²: take R=h(m)+1 and T=m+R, use at most m rounds to enumerate the square about the predictable a_m, and fill extra rounds with repeated targets. For n≤m, n+h(n)≤m+h(m)<T. Thus a universal winning policy in this class must satisfy h(m)>(sqrt(m)−3)/2 for every m. The stated o(sqrt(m)) and c sqrt(m), c<1/2, impossibility consequences follow. The report's nonmonotone sufficient condition, n+h(n)<m+R for every n≤m and (2R+1)²≤m, is also correct.

This is a restriction on time lookahead. It should not be identified with any source's spatial notion of a local strategy without a separately proved connection.

## 6. Offline paths and explicit adaptive separation

### One-dimensional fixed-schedule infinite path

For a complete fixed schedule, let F_n be the set of positions effectively announced for time n by some round r<n, and b_n=|F_n|. Distinct spacetime pairs through time n require distinct announcement witnesses from rounds 1,…,n−1; hence the cumulative sum of b_j for j≤n is at most n−1.

Set R_0={0} and R_n=(R_(n−1)+{−1,0,1})\F_n. For any nonempty finite A⊆Z, its one-step expansion contains A and the two additional extremal points min(A)−1 and max(A)+1. Inductively,

|R_n| ≥ 1+2n−sum_(j≤n)b_j ≥ n+2.

Nonemptiness required for each expansion follows from the preceding induction step. The tree of finite safe paths has at most three children per node and a node at every depth. König's finite-branching lemma then supplies one infinite safe path. Restricting a two-dimensional path to a fixed horizontal line gives the corresponding two-dimensional offline statement.

This proof is accepted. The supplied one-dimensional adaptive loss certificate shows concretely that these offline witnesses cannot be promoted to one online strategy: every fixed schedule has an infinite survivor, while an adaptive Devil defeats every one-dimensional online strategy by time 6.

### Fixed-schedule ballistic measure bound

For (u,v) uniformly distributed on [−1,1)², a_n=(floor(nu),floor(nv)) is a legal path, including for negative velocities. A fixed time-t cell has parameter preimage area at most 1/t² and probability at most 1/(4t²). A lethal announcement in round r has t≥r+1. The countable union bound therefore limits the losing measure for a fixed schedule by

sum_(r≥1) 1/(4(r+1)²) = (ζ(2)−1)/4.

The safe measure is at least (5−ζ(2))/4, approximately 0.8387664833. Repeated target times/pairs do not invalidate the upper bound, and ineffective announcements are omitted. This statement requires a fixed schedule independent of the sampled parameters.

### Adaptive trap for the same ballistic family

After observing a_4=(x,y), the Devil announces the four cells in {2x,2x+1}×{2y,2y+1}, one in each round 4–7, all for time 8. Earlier rounds can use ineffective announcements. The identity floor(2z)∈{2floor(z),2floor(z)+1}, valid for every real z, forces a_8 into that set. This defeats the whole fixed-velocity family, even if the velocities were privately sampled. It does not defeat an Angel permitted to revise its movement in response to the targets.

The two propositions are compatible: the adaptive target set depends on the observed trajectory, so a fixed-target probability bound cannot be treated as an unconditional bound on that adaptive strategy.

## 7. Static-invariant obstructions

The reviewed `../pass1_invariant/STATIC_INVARIANT_OBSTRUCTIONS.md` makes two correct scoped claims.

First, with only a bomb at (p,n+2), the additional future vertex-cut capacity at (p,n) is 9 while it is 8 at every immediate successor. For the root lower bound, the eight nonzero-velocity rays p+kv and the ninth delayed eastward path p at k=1, p+(k−1,0) at k≥2 are pairwise spacetime-vertex-disjoint after the root and avoid the bomb. For each successor, the eight constant-velocity rays excluding its step to p similarly prove the lower bound 8. The displayed immediate cuts attain both bounds. This refutes the stated one-step capacity-refresh assertion, and the single pending bomb can be announced legally after reaching p.

Second, eight bombs at time n+1 leaving only p and nine bombs on N(p) at n+2 allow an endpoint at each deadline in isolation, but no jointly safe two-step path. The first step must stay at p and every next step is bombed. The 17-pair state is an existentially reachable legal history, for example by staying at p=0 through round 17 while announcing only those future pairs. There is no claim that this history is forced.

## 8. Square-root-scale deviation from linear motion

The additional `../pass1_devil/LINEAR_MOTION_OBSTRUCTION.md` is accepted. For j≥1 set n_j=4^j, R_j=2^(j−1)−1 and K_j=(2R_j+1)²=(2^j−1)². After seeing a_(n_j), announce all K_j cells of the radius-R_j square centered at 2a_(n_j), one per round n_j through n_j+K_j−1, all with time 2n_j. Because K_j≤n_j, all announcements precede detonation. Since n_(j+1)=4n_j, stages never compete for an announcement round. Other rounds can announce current-time ineffective pairs. The list requires no future Angel positions.

Every play surviving through 2n_j satisfies

||a_(2n_j)−2a_(n_j)||∞ > R_j.

In fact, integer-valuedness strengthens this to at least R_j+1=√n_j/2 exactly. If an infinite surviving play had a_n=nv+o(√n) for any vector v, the left side would be ||e_(2n_j)−2e_(n_j)||∞=o(√n_j), a contradiction. The same single Devil strategy therefore rules out all such trajectories, including every bounded-distance constant-velocity approximation, even when the velocity and error bound are unknown and the trajectory responds to announcements.

For every infinite surviving trajectory and every v, the triangle inequality gives

limsup as n tends to infinity of ||a_n−nv||∞/√n ≥ 1/[2(2+√2)].

Indeed, an eventual upper bound smaller than that constant would make ||e_(2n_j)−2e_(n_j)||∞/√n_j eventually smaller than 1/2. The constant is approximately 0.1464466094. No claim is made that an unrestricted Angel cannot achieve the required fluctuations, nor that this strategy forces a uniform finite death horizon on the whole restricted class.

## 9. Audit corrections and boundaries

No substantive error was found in the accepted frozen statements. Precision improvements are:

- State the time-lookahead restriction as a history-equivalence property, excluding retained information about ignored target cells.
- State the fixed-coordinate transfer using a known deterministic terminal coordinate.
- Keep full, horizon-independent states in the compactness argument; use finite-cone projection only to evaluate W_h.
- Preserve the explicit distinction between exact finite-horizon games and offline reachable-path calculations.
- State that the 16-pair local trap and 17-pair multi-deadline example are preloaded/existential states, not forced traps from the empty board.

The mathematical gap remains proving W_h(empty) for all finite h, or exhibiting a reachable finite-horizon full-game Devil win. Neither is supplied by this audit.
