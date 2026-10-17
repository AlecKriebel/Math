# Independent scoped audit: positive blocks and shared charge

## Disposition and exact input

**Accepted, with the scope below.** This audits Sections 1 and 5 of the frozen
`pass4_multiscale/REPORT.md`, SHA256
`b7b490a9ec6cb9e58a15cadb5e5fcf239f9c0ae316e6f30ac2e1bea86c891608`.
It does not certify an implemented controller or a family of admissible states.
Sections 2--4 and 6 are outside this scoped acceptance and are independently
assigned elsewhere. This is an audit within shared PASS4.

## 1. Positive finite-block continuation suffices

Fix finite H, deterministic boundaries tending to infinity, and the one legal
nonanticipating randomized policy in the statement. Let G_j be its event of
safe play through boundary S_j with complete post-announcement state in P_j.
Fix any adaptive Devil strategy. On G_j, condition on the full actual history
and all private information revealed by that boundary. The continuation of
this fixed Devil is one of the universally quantified continuations covered
by the block hypothesis. Future draws obey the prescribed fresh-draw law.
Therefore the conditional probability p_j of G_(j+1) is strictly positive
on G_j. As usual, the conditional law and the policy are measurable; the
complete-state requirement means this is a conditional statement at each
actual history, not an average over omitted hidden state.

If P(G_j)>0, then E[1_(G_j) p_j]>0. One direct justification is that the
sets G_j intersect {p_j>=1/k}, k=1,2,..., cover G_j up to null sets; at least
one has positive measure. Thus induction gives P(G_j)>0 for every finite j.
There need be no state-uniform or j-uniform positive lower bound.

Every finite horizon lies before some such boundary. If the Devil won that
finite-horizon game, its strategy would kill every legal realization of this
randomized Angel policy, contradicting the strictly positive survival
probability. Finite-horizon determinacy therefore gives an Angel winning
strategy at each finite horizon. The established nested-winning-set argument
uses only the Angel's nine legal moves to extract a single infinite winning
strategy. It tolerates all spatial choices of Devil announcements.

The randomized block policy itself may have probability zero of surviving
forever. Its role is to rule out each finite-horizon Devil win, not to supply
a positive-probability infinite path. This is a valid quantifier order:
for every fixed adaptive Devil and every finite block count, finite success
has positive probability. Neither a fixed schedule nor an offline path is
substituted for an adaptive opponent.

The endpoint announcement and all intermediate death checks are explicitly
included. Complete post-announcement states carry every pending timestamp,
controller memory, and revealed private randomness. A next-block claim only
for an endpoint location, or one conditioning away survival correlations,
would not satisfy the accepted premise.

## 2. Shared-announcement charge bound

Take N consecutive move indices a,...,a+N-1. If an announcement in round r
can be charged only at times in [r,r+H], a charge in that move window must
come from r in [a-H,a+N-1]. There are N+H integer round indices in this
interval, and at most one physical announcement per round. Nonnegative
charges and the total per-announcement bound C imply total window charge
at most C(N+H). Boundary truncation at the initial round can only reduce it.

Class labels may depend on history when assigned. Their rates do not enter:
C bounds the sum of every charge assigned to a single announcement, including
all levels or classes through which that announcement may contribute. Using
only the largest separate-level charge would fail the premise.

## 3. Excursion calculation

Let an excursion first enter V>=V0 at index e. The entry-jump bound gives
V_e<=V0+J. If the excursion continues for N further steps, every preceding
potential in those steps is at least V0, so summing the assumed drift and
then applying the charge bound to exactly those N indices gives

V_(e+N) <= V_e-dN+C(N+H)
          <= V0+J+CH+(C-d)N
          <= V0+J+CH.

The entry time itself obeys the same upper bound, and times outside the
excursions are below V0. Thus the asserted uniform potential bound follows
when d>=C. Strict entry inequalities give the corresponding strict bound.
The assumption that the process starts below V0 makes the entry argument
complete; an initially high state would need its own initial bound.

This calculation concerns one actual legal controller and one potential.
It cannot combine incompatible requested moves from separate controllers.
The report explicitly states this missing existence condition, so it does
not overclaim an arbitrary-H construction.
