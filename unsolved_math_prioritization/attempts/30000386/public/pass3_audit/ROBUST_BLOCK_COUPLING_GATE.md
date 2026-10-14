# Robust block transitions: exact safety and conditional-spread gate

Shared PASS3 structural result. This document supplies precise sufficient hypotheses for a proposed coupling. It does not construct a controller satisfying them for the unrestricted Time-Bomb game and does not claim a resolution.

## 1. Information timing is part of the hypothesis

Fix deterministic integer boundaries 1=S_1<S_2<… and lengths L_j=S_(j+1)−S_j. At a boundary S_j the Angel first arrives and is checked against all earlier announcements. Devil then announces its round-S_j pair. Only afterwards is a new private reference displacement D_j drawn, independently and uniformly from [−M_j,M_j]²∩Z², with 1≤M_j≤L_j.

The reference prefix F_j(u,d), 0≤u≤L_j, is a deterministic function of the block index, elapsed time and d, with F_j(0,d)=0 and F_j(L_j,d)=d. Its increments are legal king increments. It has no dependence on the observed bomb history, earlier reference draws, or the eventual tracking errors.

The corrected controller may use already revealed D_i, its own fresh auxiliary randomness and the entire observed bomb history. It may not inspect future D_i before their boundary draw. This is an adaptedness requirement relative to the reference randomness, stronger than merely saying that the controller reacts to actual observed positions. Presampling all D_i is equivalent only if future values are inaccessible until their prescribed reveal times.

Devil is nonanticipating and sees the actual corrected path, including every correction, and all public history. Its chosen target position and time can depend on all of that history. No proof may replace this actual-history filtration by the less informative reference-path history.

## 2. Exact deterministic block acceptance

A block begins in a complete post-announcement state at S_j: current position, every pending bomb with its timestamp, and any controller memory used in the invariant. Let P_j be an admissible family of such states. A path ending at S_(j+1) is acceptable only if:

- every move in (S_j,S_(j+1)] has been checked against bombs announced strictly earlier;
- the endpoint survives its own time;
- for every legal announcement after that endpoint move, the complete resulting state belongs to P_(j+1).

Equivalently, backwards from P_(j+1), each round has the operation

there exists a legal immediately safe Angel move, followed by every legal Devil announcement.

The last round includes the endpoint announcement before membership in P_(j+1) is tested. This is the block analogue of the accepted robust deadline predecessor. A region alone is not a sufficient state description if pending bombs or internal commitments affect the next block's feasibility.

If a claim handles only a designated class of bombs inside the block, it must identify and separately account for all other possible lethal events. Calling the remainder a long-range objective does not remove its intermediate death checks.

## 3. Local-reset bounded-tracking lemma

Suppose that on a specified good event G the corrected path satisfies, for every block j and prefix u,

||a_(S_j+u)−a_(S_j)−F_j(u,D_j)||∞ ≤ rho_j,

where rho_j are fixed nonnegative integers. The error is measured relative to the actual start of that block. Thus old corrections do not have to remain bounded relative to one global reference origin.

Fix an announcement round n in block j, and suppose its target t obeys t≥S_(j+2). Condition on the full actual observed history and the chosen pair (p,t). Let ell be the block containing t, with S_ell≤t<S_(ell+1), and put i=ell−1. Then i≥j+1, so D_i is a future, unrevealed displacement at announcement time n.

On G, the endpoint has the decomposition

a_t = a_(S_i) + D_i + F_(i+1)(t−S_(i+1),D_(i+1)) + E,

with ||E||∞≤rho_i+rho_(i+1). The two error terms are the completed block-i endpoint error and the current block-(i+1) prefix error. At t=S_(i+1), the latter is exactly zero.

Write Z for the sum of a_(S_i) and the displayed F term. Conditional on the announcement history, Z is independent of D_i:

- the actual anchor a_(S_i) is established before D_i is drawn;
- the later D_(i+1) is independent of D_i and of prior random inputs;
- F_(i+1) is the stipulated fixed function of that later draw;
- the observed history and chosen t precede the reveal of D_i.

The tracking errors may depend on D_i, on later observations, and on Devil's adaptive actions. They are not assumed independent. Instead,

{a_t=p} intersect G

is contained in the event that D_i+Z lies in the radius-(rho_i+rho_(i+1)) square around p. Consequently,

P(a_t=p and G | actual announcement history)

≤ min(1, [2(rho_i+rho_(i+1))+1]² / (2M_i+1)²).

This is a bounded-preimage argument, not a convolution claim for the corrected endpoint. No conditioning on G has been performed. Conditioning on a future good event could bias the fresh draw and would require a separate denominator estimate.

If all rho_j≤rho and M_j are nondecreasing, the bound is at most

q_j = min(1,(4rho+1)²/(2M_(j+1)+1)²).

More generally a bound depending only on the announcement block is

q_j = sup_(i≥j+1) min(1,[2(rho_i+rho_(i+1))+1]²/(2M_i+1)²).

The choice of t may be fully adaptive at announcement time: after conditioning, its block index is fixed. The upper bound is uniform over those choices.

## 4. A sufficient safe-controller plus spread theorem

Classify each effective announcement in block j as long when t≥S_(j+2), and short otherwise. Past/current-time announcements are ineffective. This partitions every possible lethal announcement in the original game.

Assume a single nonanticipating corrected controller and admissible-state families P_j have the following properties:

1. Initialization: after a legal first move and every possible round-1 announcement, the complete state lies in P_1. No round-zero update is assumed.
2. Fresh draws: D_j has the uniform independent law and reveal timing in Section 1 on every history, including a chosen hypothetical extension after a failure.
3. Block safety and closure: from every state in P_j, for every adaptive Devil, the probability that block j has a short-bomb collision, violates its tracking bound, or fails post-endpoint membership in P_(j+1) is at most epsilon_j. The endpoint's own announcement is included in this test. These bounds are conditional on the actual state/history before the block, not averages over a favored starting distribution.
4. Movement is legal on the hypothetical trajectory. Long-bomb collisions can be ignored only for bookkeeping so that the controller and all future draws remain defined. Actual play stops at the first lethal collision as usual.

The probability of any block failure is at most sum_j epsilon_j, by considering the first failure and the conditional uniform bounds. Let G be the event of no block failure. On G, every intermediate short-bomb check succeeds, the invariant states concatenate, and all tracking inequalities hold.

For each long announcement n in block j, define the effective hit event E_n={t_n>n and a_(t_n)=p_n}. Section 3 bounds P(E_n intersect G) by q_j. There are L_j announcement rounds in block j, so

P(actual loss) ≤ sum_j epsilon_j + sum_j L_j q_j.

No intermediate death has been dropped: short deaths are in the failure event; long deaths are in the union of E_n. Repeated timestamps and targets remain covered. A bound strictly below one supplies positive survival probability against every adaptive Devil. Exact finite-horizon determinacy and finite-Angel-action compactness then give a deterministic infinite winning strategy for whichever full announcement class satisfies the controller hypotheses.

If these hypotheses were proved for all unrestricted announcements with the displayed sum below one, this would resolve the original conjecture. This document proves only the conditional implication. In particular, epsilon_j=0 and bounded tracking under all short threats are substantial unproved controller requirements.

## 5. Relation to a global-reference transfer

A simpler transfer is valid when a reference trajectory X_t has the needed conditional fresh-block spread and, on G, ||a_t−X_t||∞≤r(t). Then

{a_t=p} intersect G is contained in {X_t belongs to p+[−r(t),r(t)]²},

so its probability is bounded by the number of lattice points in that square times the reference's maximal conditional endpoint mass. The correction may be correlated with X_t. Again, the actual history must not have revealed the supposedly fresh reference block, and one bounds the intersection with G without conditioning on G.

The local-reset lemma improves the bookkeeping when old tracking errors accumulate: use the last completed fresh block before t and absorb all older errors into its actual start anchor. Only the most recent endpoint and prefix errors enter the multiplicity factor. This still does not create a safe tracker.

## 6. Failure modes that a candidate must exclude

- A controller that reads future reference displacements can leak them through current corrections; freshness fails even if Devil sees only actual moves.
- A reference interpolation chosen from earlier bomb observations or from an earlier displacement can make the purported independent remainder depend on the selected fresh draw.
- The corrected endpoint is generally not an independent convolution. A displacement-dependent error can concentrate mass, so its preimage factor must be paid or replaced by a proved sharper bound.
- Conditioning on successful survival or a future good event can concentrate the reference distribution. An unconditional or good-event-intersection estimate is required unless the conditioning cost is proved.
- Uniform marginal spread at a completed endpoint does not constitute future hidden randomness: Devil observes that endpoint before its next announcement.
- Checking only the endpoint ignores every allowed intermediate lethal time. A block traversal may be killed before its destination is reached.
- Omitting the announcement made after the endpoint move can destroy the next block's invariant immediately.
- A bound for one carefully chosen starting distribution does not justify restarting after arbitrary adaptive histories. The stated transition guarantee must hold on the actual admissible state family, or carry and verify the required conditional information state.

In particular, long pauses or zero-slack motion in a proposed reference may make bounded-band safe tracking impossible. The spread implication remains correct while controller existence fails. An impossibility result for that tracker would not itself be a full-game Devil win.
