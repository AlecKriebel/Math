# Attempt 5: infinite enlargement and aggregation

Attempt 4 shows that finitely many annulus orbits are insufficient for the
modular cusp. This attempt tests the most direct infinite enlargements.

## Proposition 5.1: taking all annuli destroys finite crossratios

Let Z be an infinite perfect compact metric space. Let A_all contain every
annulus in Z. It is automatically symmetric and invariant under every
homeomorphism. Given four distinct points a,b,c,d, however,

(a,b|c,d)=infinity.

Proof. Put L={c,d}, K={a,b}, and f(z)=dist(z,L). Since c is nonisolated and
d!=c, f takes positive values arbitrarily close to zero. Choose positive
values delta_j in f(Z) decreasing to zero sufficiently rapidly. Around each
delta_j choose numbers 0<s_j<delta_j<r_j such that

r_1<dist(K,L), and r_{j+1}<s_j.

Define A_j-={f>=r_j} and A_j+={f<=s_j}. These are disjoint closed sets and
their complement is nonempty because f takes the value delta_j. K lies in
the interior of A_1-, and L in every interior A_j+. Since r_{j+1}<s_j,
the open sets {f<s_j} and {f>r_{j+1}} cover Z, proving A_j<A_{j+1} with our
nesting convention. Thus chains of every length separate K and L. This
violates (A1), not merely a numerical estimate in (A2).

This is a failure of the unrestricted choice A_all. It does not prove that
every carefully selected infinite-orbit system fails.

## Proposition 5.2: aggregating hyperbolic pseudometrics need not work

On Q=Z^2 let

rho_1((x,y),(x',y'))=|x-x'|,
rho_2((x,y),(x',y'))=|y-y'|.

Both are translation-invariant 0-hyperbolic pseudometrics, being pullbacks
of the integer-line metric. Both are path quasimetrics: interpolate the
relevant integer coordinate, choosing the other coordinate arbitrarily at
intermediate steps. If the relevant coordinate difference is zero but the
endpoints differ, a one-step sequence has additive error 1, which provides
a uniform path-quasimetric constant for all pairs.

Their sum is the l1 metric on Z^2. For the four points

(0,0), (n,n), (0,n), (n,0),

the three opposite-pair distance sums are 4n,2n,2n. No fixed four-point
hyperbolicity constant exists. Their maximum is the l-infinity metric. For
the four points

(n,0), (-n,0), (0,n), (0,-n),

the three sums are again 4n,2n,2n. It also is not hyperbolic.

This example is an obstruction to a purported general metric-aggregation
lemma. It is not a convergence action on a compactum and is not presented
as a counterexample to the original question. Scaling both summands by any
fixed positive weights does not salvage the sum: suitably long rectangles
still have arbitrarily large four-point defects.

## Exact remaining gap

The universal target is unresolved after these five substantive approaches.
A sufficient continuation would construct, from an arbitrary minimal
convergence action, an invariant symmetric annulus system simultaneously
satisfying finite pair-pair depths (A1), a uniform crossing bound (A2), and
unbounded pair-point depth (A3). Attempt 2 then applies. We have not shown
this criterion to be necessary for arbitrary uniform quasi-actions, and do
not claim that its failure alone would answer the original question.

Alternatively one needs an interior hyperbolic construction with a proved
equivariant homeomorphism onto the entire given compactum and uniform
quasi-action constants. Group-level acylindrical hyperbolicity, an
almost-everywhere boundary correspondence, and element-dependent extension
constants each leave a different part of this requirement unproved.

The all-annuli construction fails (A1); finite families fail at the cusp;
naive sums or maxima have no general hyperbolicity theorem. No argument
here supplies the missing controlled infinite construction or a
non-realizable minimal convergence action.

Checkpoint: approximately 15% toward the universal target. Five scoped
routes are documented; finite checks supplement the proofs and cannot
decide the unbounded or topological assertions.
