# Status and the exact remaining mathematical obligation

The unrestricted Time-Bomb target is **UNSOLVED 5/5** in this investigation.
Five shared substantive passes produced the accepted partial results in the
[index](RESULTS_INDEX.md). Parallel constructions and audits within a pass do
not count as separate passes. This is a statement about the work presented,
not an exhaustive certification of the literature's present status.

## An exact positive target

Fix H>=1. Immediately after an announcement, translate the current Angel
position to zero and retain the finite pending set B. The exact bounded-lead
arena K_H consists of subsets of

C_H={(q,t): q in Z^2, 1<=t<=H, ||q||_infinity<=t}

with the tail-age bounds

#{(q,t) in B: t>=j} <= H-j+1 for 1<=j<=H.

These constraints preserve the one-announcement budget even when many pairs
have the same target time. Cone pruning is exact; an unreachable pair cannot
reenter a later reachable cone. See the
[arena proof](pass4_audit/BOUNDED_LEAD_FINITE_ARENA.md) and
[structural acceptance](pass4_survival/STRUCTURAL_REDUCTION_AUDIT.md).

For a family X within K_H, let F_H(X) contain the states with an immediately
safe king move for which **every** subsequent legal Devil announcement leads
back into X. The order is an Angel choice, then an adaptive Devil response.

For each H, infinite survival from empty history is equivalent to the
existence of a family Y_H with

empty in Y_H and Y_H contained in F_H(Y_H).

Equivalently, the empty state must lie in the greatest fixed point of F_H.
Descending finite safety regions always stabilize, including in games where
the empty state loses; stabilization alone is not the needed membership claim.
The [exact criterion](pass5_audit/FIXED_POINT_CRITERION_AND_DEPTH_OBSTRUCTION.md)
and its [independent audit](pass5_devil/FIXED_POINT_AND_DEPTH_AUDIT.md) explain
these equivalences and qualifications.

Proving this for every finite H would solve the unrestricted game. For each
finite unrestricted horizon, discard only announcements that cannot affect
that horizon, simulate an appropriate bounded-lead strategy, and then use
nested nonempty subsets of the nine Angel actions to extract one infinite
strategy. The [all-H reduction](pass4_audit/ALL_FINITE_LEADS_REDUCTION.md)
requires no compatibility, uniform tracking radius, uniform memory bound, or
uniform computability of the H-dependent strategies.

The package proves the bounded-lead claim through H=16. It does not prove it
for every H.

## A sound conditional route that is still unproved

Let W_k be unrestricted online survival for the next k moves from a full
pending state. The [initialized critical-gap criterion](pass5_coupling/CRITICAL_GAP_BOOTSTRAP.md)
would suffice if W_k implied W_(k+1) on every (k+14)-age-admissible state for
all k>=2. The k=2 case is accepted, while the geometric hypotheses for k>=3
remain unproved. The preceding-lead induction supplies the otherwise easily
missed base W_k(empty); it does not prove those geometric implications.

An unspecified large-depth implication can be vacuous if W_k(empty) has
already failed. Conversely, one fixed depth k cannot close the entire W_k^H
region for all H: terminal carpets at H>=(2k+3)^2+k give either a failed
initialization or a failed full-region closure. This obstruction permits
H-dependent depths and smaller invariant families.

## Exact continuation at a rescue boundary

A finite rescue must avoid every intermediate lethal move, retain all still
relevant residual timestamps, and include the Devil announcement after its
endpoint move. Its actual complete endpoint state must belong to a certified
continuation family. Separate survival of an active portion and a residual
portion does not imply compatible endpoint choices; an
[explicit accepted counterexample](pass5_invariant/RESIDUAL_COMPOSITION_OBSTRUCTION.md)
shows this failure.

Positive finite-block or stopping-time return probabilities can suffice, but
only with a complete-state family and a valid conditional return property at
every actual history. The [reset criterion](pass5_multiscale/REPORT.md) does not
construct that family. Heavy-deadline density and the exact pending-count
identity do not force automatic flushing. The static four-thirds danger
envelope is not an identification of the multitime adaptive Bellman operator.

## What a genuine negative resolution would need

A finite bounded-lead forcing graph rooted at the empty state would suffice.
Give every node a positive rank. At every safe Angel choice, provide a legal
Devil response to a smaller-rank successor; rank-one nodes must have all nine
moves immediately lethal. Verify the exact shifts, additions, cone pruning,
lead rule, and every current-time death test.

No such empty-rooted graph or analytic forcing strategy has been obtained.
The supplied one-dimensional certificate proves only that restricted game.
Losing preloads may be legally realizable along cooperating Angel histories
without being forceable against an Angel trying to survive. Defeating a
specified tracker or a sufficient proof estimate is also not a full-game
Devil win.
