# A viable rescue and a viable residual state need not compose

Status: authored final shared PASS5 obstruction, submitted for independent
audit. This is a finite online composition counterexample. It is not a
Devil strategy forcing the preload from the empty initial history, and
it does not disprove bounded-lead or unrestricted survival.

## 1. Exact preload

Start at the origin immediately before move 1. All displayed bombs are
already announced. Let the active set consist of the fifteen pairs

`P = {((x,y),2): x in {0,1,2}, -2<=y<=2}`.

Let the unrelated later residual set consist of the fifty-four pairs

`R = {((x,y),4): -4<=x<=1, -4<=y<=4}`.

As always, between successive Angel moves the Devil may make one
adaptive announcement at any position and time. An ineffective
announcement is allowed and consumes that round's budget.

The following three statements hold:

1. P alone admits an online strategy surviving moves 1,2,3 against all
   intervening adaptive announcements.
2. R alone admits an online strategy surviving moves 1,2,3,4 against
   all intervening adaptive announcements.
3. P union R is losing by move 4 even if all subsequent announcements
   are ineffective. Indeed, every endpoint of a surviving three-move
   rescue is already trapped for the next move by R.

Thus independent finite viability of the active and residual parts
does not provide a compatible continuation strategy for their union.

## 2. Active-set online viability

The accepted three-move lemma in
`../pass4_invariant/LEAD16_RESCUE.md`, SHA256
`fbcf3b299034bff78871b5b61b77f74f873f0a7cd9b963863c0c26a613f09438`,
applies directly: there are no current-time bombs, fifteen preloaded
bombs at the next time 2, and none at the following time 3. Its
conclusion covers arbitrary adaptive announcements after moves 1 and
2, including announcements creating new dangerous terminal centers.
Therefore P alone is online viable through move 3.

## 3. Residual-set online viability

Use only moves with `x_n=n` for n=1,2,3,4. Their y-coordinates form a
one-dimensional king walk with three choices per move, including a
stay in y. The initial residual carpet is lethal only at time 4 and
has x<=1, so none of its points can hit this restricted path. We must
still handle every newly announced bomb adaptively.

Choose y_1=0. Before move 2 only one new announcement has occurred.
Among the three possible y_2 values, at most one is newly lethal at
the position/time pair `(2,y_2,2)`. Choose a safe y_2.

Before move 3 only two new announcements have occurred. Let A be the
set of their effective y-coordinates at position x=3 and time 3; let
B be their effective y-coordinates at position x=4 and time 4. Put
`m=|A|`, `b=|B|`; then `m+b<=2`.

If b<=1, every candidate y_3 has at most one B-point among its three
possible y_4 neighbors. At most m<=2 candidates are currently lethal,
so choose a currently safe one.

If b=2, then m=0. Two distinct integers are both contained in the
three-point neighborhood of at most two integer centers. Among the
three available choices `y_2-1,y_2,y_2+1`, there is consequently a
y_3 whose neighborhood contains at most one point of B. Choose it.

In either case the chosen move 3 is safe and at most one preexisting
time-4 bomb lies among the three restricted final choices. After the
third adaptive announcement there are at most two such bombs. At
least one choice `(4,y_4)` is safe at time 4. This proves the claimed
online four-move viability, not just a path through a fixed schedule.

## 4. Incompatibility in the union

Every position reachable at time 2 lies in `[-2,2]^2`. Avoiding P at
that time therefore forces

`x_2<=-1`.

Consequently a surviving time-3 position has x_3<=0, and every possible
time-4 position satisfies

`-4<=x_4<=1`, `-4<=y_4<=4`.

Every such time-4 position is in R. Thus any path either hits P at
time 2 or hits R at time 4. No additional effective announcements are
needed.

The endpoint incompatibility can be stated exactly. Within the
time-3 reachable square `[-3,3]^2`, the centers with at least one
time-4 neighbor outside R are precisely those with x_3>=1. All
endpoints of a P-safe three-move path have x_3<=0. These two sets are
disjoint. The union is nevertheless online viable through move 3,
because R cannot affect an earlier move and the active rescue applies.

## 5. Legal age accounting, without forceability

This preload belongs to the exact maximum-lead-70 arena. At its
post-announcement state, the pending relative times are 2 and 4. Its
tail counts are

`N_1=N_2=69`, `N_3=N_4=54`, `N_j=0` for j>=5.

They satisfy `N_j<=70-j+1`, and every spatial pair is in its relative
reachable cone. In fact H=70 is the smallest lead bound for these
tail counts, since `N_2=69` requires H>=70.

An explicit legal witnessing history is available. Have the Angel
stay at the origin through absolute round 70. Put the fifteen active
pairs, now targeting absolute time 72, in announcement rounds 2
through 16. Their leads range from 70 down to 56. Put the fifty-four
residual pairs, now targeting time 74, in rounds 17 through 70. Their
leads range from 57 down to 4. Use an ineffective announcement in
round 1. None detonates before round 70, and the normalized pending
state is exactly P union R.

This demonstrates existential legal reachability along a cooperating
staying path. It gives no strategy that forces such a state against
an Angel choosing differently during those seventy preparation rounds.

## 6. Exact missing continuation interface

Let K_H be the complete normalized post-announcement arena, retaining
every still-reachable pending pair. For a target collection X of such
states, define the robust one-move predecessor

`Pre_H(X) = {S: some immediately safe king move has every legal
                    post-move Devil successor in X}`.

Define `Pre_H^0(X)=X` and iterate this operator. A rescue of length L
that promises continuation in X needs its full initial state in
`Pre_H^L(X)`. The universal successor quantifier includes announcements
at times after the rescue and the announcement immediately following
its final move. All old residual pairs must be shifted and retained
unless expired or permanently outside the reachable cone.

This interface is sufficient by backward induction and composes with
any valid continuation strategy on X. It is also necessary for a
deterministic L-move guarantee of ending in X. If an augmented state
records additional history, the same definition must be applied to
that augmented state rather than silently discarding the information.

The example shows why separate statements of active L-move viability
and residual later viability do not establish this interface. Nor does
a reduced pending count at rescue completion suffice without an
admissible endpoint and the appropriate continuation predicate.

For a full residual-carrying induction, the missing lemma is a family
of initial-state-containing classes X_H, together with legal robust
rescue/ordinary choices that keep the complete residual state in the
same class or reach a previously established winning class. A closure
claim for a finite-horizon viability class additionally needs explicit
membership of the empty state; closure of an empty or irrelevant fixed
point gives no initial winning strategy. No such arbitrary-H lemma is
proved here.
