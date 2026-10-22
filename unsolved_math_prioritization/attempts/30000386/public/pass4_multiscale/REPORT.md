# Multiscale bounded-lead composition: exact gates and a failed bootstrap

## Result and scope

This PASS4 lane does not extend the accepted maximum-lead bound or solve the unrestricted Time-Bomb game. It supplies:

1. A restartable-block criterion requiring only positive finite-block success, rather than a positive infinite survival probability.
2. A general obstruction to a uniform-radius, slow-reference, equal-block union-bound bootstrap.
3. Correct shared-announcement-budget amortization and the explicit movement/compatibility hypotheses it does not supply.
4. A legal two-class preload illustrating why independent classwise controllers do not automatically compose.

All statements use the original king-move, Angel-first convention. No additional deadline-count theorem, novelty claim, or full-game Devil win is asserted.

## 1. Positive finite concatenation is sufficient

Fix a finite maximum announcement lead H. Let `0=S_0<S_1<...` be deterministic block boundaries tending to infinity. Let P_j be families of **complete post-announcement controller states** at time S_j; at time zero the family instead contains the specified empty initial state, with no round-zero announcement.

A state includes position, every pending bomb with its timestamp, controller memory, and any already revealed private randomness. Future random draws remain inaccessible until their stated reveal times. Conditioning is on actual observed histories and already revealed private information, not on a hypothetical reference-only history.

**Block criterion.** Suppose one legal nonanticipating randomized Angel policy has the following properties against every adaptive Devil with leads at most H:

- It starts in P_0.
- From each state in P_j, for every adaptive continuation of the Devil, the probability that the next block avoids every lethal move and ends, after the endpoint announcement, in P_(j+1) is strictly positive.
- The policy remains defined on all hypothetical failure branches, with fresh future draws independent at their prescribed reveals.

No uniform lower bound over j or over states is required. Then the Angel has a deterministic infinite winning strategy in the lead-H game.

**Proof.** Fix a Devil and a finite number of blocks. The event of success through zero blocks has probability one. Conditional on success through j blocks, every actual state belongs to P_j. Its conditional next-block success probability is strictly positive. Integrating a strictly positive function over this positive-probability event gives a strictly positive probability of success through j+1 blocks. Induction proves survival through any finite number of blocks with positive probability.

Every finite horizon lies inside finitely many blocks. A finite-horizon Devil-winning strategy would defeat every realization of this randomized policy and therefore give survival probability zero, a contradiction. Exact finite-horizon determinacy and the accepted compactness extraction over the Angel's nine moves give a deterministic infinite strategy.

The infinite product of success probabilities may be zero. That does not invalidate the argument, since finite-horizon winning strategies, rather than positive probability of infinite success of this particular randomized policy, are extracted.

**Missing construction.** The criterion does not establish any P_j or any block policy. A surviving endpoint position alone is insufficient: pending bombs and controller commitments may make the next block unwinnable. The endpoint's own announcement is included in the required closure. Survival-conditioned randomness cannot silently be treated as fresh.

## 2. A necessary tracking-radius bound

**Lemma.** Suppose a controller avoids every legal lead-at-most-H bomb stream while remaining within integer infinity-norm distance R of the stationary reference at the origin. Then

`(2R+1)^2 > H`.

**Proof.** Otherwise put `Q=(2R+1)^2<=H`. In rounds 1 through Q, announce all Q distinct sites of `[-R,R]^2`, one per round, with their common target time `Q+1`. Their leads range from Q down to one, so every announcement is legal in the lead-H game. There are no earlier lethal times. At time Q+1 every position in the permitted tracking band is bombed. The controller must either leave the band or lose.

This is a lower bound on the radius of a tracker valid against every allowed stream. It is not a Devil strategy against an unrestricted Angel, which may leave the band.

## 3. Failure of the uniform-radius equal-block union certificate

Consider the following specific attempted bootstrap from an already handled tracker lead bound H to a strictly larger game bound J>H. For announcement classification in this section, block j contains rounds S_j through S_j+L-1, while its reference displacement is traversed by moves S_j+1 through S_j+L. The round-S_j announcement precedes that block's fresh reference draw. This explicitly fixes the half-open announcement convention independently of the post-announcement transition states in Section 1.

- Equal block length L.
- Every announcement in block j with target before the end of block j+1 is handled by a lead-at-most-H tracker with one uniform integer radius R.
- Later targets are handled by a fresh reference displacement uniform on the integer square `[-M,M]^2` in a completed future block.
- The reference has infinity-norm speed at most v, hence `M<=vL`.
- A hit of the corrected path is bounded only by the radius-R reference preimage square. The resulting per-announcement upper bound is

  `q=min(1,(2R+1)^2/(2M+1)^2)`.

- A block with up to L later-target announcements is certified by the direct union estimate `Lq<1`.

The earliest announcement in a block can target the last time strictly before the end of the next block. Under the new game bound J, the greatest such short lead is `min(J,2L-1)`. Covering the entire short class requires

`H>=min(J,2L-1)`.

Since J>H, this forces `H>=2L-1`, and consequently `J>=2L`. In particular, a block can legally contain L later-target announcements: all may target S_j+2L, with leads from 2L down to L+1. Thus the L-announcement union estimate is not paying for announcements forbidden by the target game.

Combining this with the tracking-radius lemma gives

`Q=(2R+1)^2>H>=2L-1`, hence `Q>=2L`.

**Obstruction.** If `v<=1/4`, the displayed union certificate is never strictly below one, at any integer scale L.

For L=1, `M<=1/4` forces M=0, so q=1 and Lq=1. For L>=2,

`2M+1<=L/2+1<=L`.

Consequently

`Lq >= L min(1,2L/L^2) = min(L,2) >= 2`.

Thus this specific coarse estimate cannot establish positive block success. A local-reset transfer with radius `2R` gives an even larger preimage factor and cannot repair this obstruction.

**Interpretation.** The quantity q is an upper bound on actual hit probability. Showing that its union sum is large is not a lower bound on loss probability and is not a counterexample to a safe controller. The result rules out this proof certificate, not all block methods. It applies equally to the previously accepted speed 1/100 tracker and to a speed-1/4 improvement.

The statement pays for one uniform radius against all short streams and all L possible later-target announcements. An effective improvement could retain the actual short/long allocation history, a smaller conditional preimage set, or a different joint safety-and-spread invariant. No such improvement is supplied here. The single announcement budget does not by itself make either uniform assumption disappear.

## 4. Time dilation does not preserve the announcement rate

A second attempted induction is to feed a slower interpolated outer controller into an inner tracker. If a virtual king step is spread over K physical rounds to meet Euclidean reference speed v, arbitrary diagonal virtual steps require

`K>=ceil(sqrt(2)/v)`.

For the accepted v=1/100 reference bound this is at least 142 physical rounds. During one such macroturn the Devil still has K physical announcement opportunities. Even a restriction to targets at macro-boundaries permits all K announcements to belong to the same outer lead class when the maximum lead is large enough.

Therefore the outer game has an announcement budget of up to K per macroturn, not one. The original shared budget limits the total across classes to K; it does not reduce that total to one. A proof may reduce the effect of an individual announcement through a justified spread or nonlinear reserve estimate, but it may not simply assign weight 1/K by time rescaling.

Moreover, announcements targeting interior physical times still require their own death checks. Treating only macro-endpoints omits legal lethal events. These are separate obligations from spare movement speed.

## 5. Correct shared-budget amortization

The following bookkeeping lemma can replace an invalid sum of independent per-layer worst cases.

**Charge lemma.** Each physical announcement receives a class label when made. Its nonnegative charges are allocated at times from its announcement through at most H rounds later, and its total charge is at most `c_class<=C`. Then the total charge in any N consecutive move indices is at most

`C(N+H)`.

Indeed only announcements in an interval enlarged by at most H rounds to the left can contribute. There is at most one announcement per round, and each contributes at most C in total. Classwise rates are not independently maximized. If one announcement is charged at several levels, the bound C must cover the **sum** of its charges, rather than the maximum of the individual charges.

**Conditional drift consequence.** Suppose one actual legal controller supplies a nonnegative potential V, a threshold V0 and entry-jump bound J such that whenever the preceding potential is at least V0,

`V_n <= V_(n-1)-d+charge_n`,

with `d>=C`. Starting below V0, every excursion then stays below or at

`V0+J+CH`,

with the appropriate strictness if the entry bound is strict. Sum the drift over the excursion and use the charge lemma; the term `(C-d)N` is nonpositive.

This is a rigorous way to exploit the one shared announcement budget. It does not construct the legal move satisfying the required drift. Separate controllers may request incompatible movements or have disjoint admissible move sets. Independent radial-progress estimates cannot be added without proving a single common move realizes the combined inequality.

## 6. Classwise feasibility does not imply common feasibility

Here is a legal preload illustrating the missing compatibility condition. It is not asserted to be forced against every Angel strategy.

Let the Angel have stayed at the origin through move 16. During rounds 1 through 8, announce the eight positions in `N(0)\{0}` for time 18. These leads are 17 through 10. During rounds 9 through 16, announce the same eight positions for time 17; these leads are 8 through one. There is only one announcement per round, no lethal time has yet occurred, and the two batches belong to disjoint lead classes `{10,...,17}` and `{1,...,8}`.

Before move 17, the earlier batch alone leaves many safe possibilities for time 17, and the current-time batch alone permits staying at the origin. But together, immediate safety forces the move to the origin, while the next-time guard requiring at most seven already bombed neighbors excludes the origin: it already has eight time-18 neighbors bombed.

After the forced move 17, the Devil announces `(0,18)`. All nine possible move-18 destinations are then bombed. Each preloaded batch had only eight sites at its own target time; assigning them to separate safe subcontrollers did not create a jointly safe move.

The actual history is legal and reachable under the displayed stay-put path, but no assertion is made that a history-aware controller is forced to reach it. An admissible-state invariant may exclude it. The example establishes only that classwise safety or classwise directional bounds alone do not prove the needed intersection or block closure.

## 7. Pass disposition

The positive finite-block criterion relaxes an unnecessarily strong infinite-survival-probability requirement. The radius/lead/speed calculation then shows that one natural uniform-radius implementation cannot meet even that relaxed certificate. Time dilation and classwise separation introduce additional budget and movement obligations rather than solving them.

No all-H tracker, restartable admissible-state family, or unrestricted strategy has been constructed. The remaining requirement is a genuinely shared, history-aware safety-and-spread invariant whose legal moves also provide compatible progress across the relevant lead scales.
