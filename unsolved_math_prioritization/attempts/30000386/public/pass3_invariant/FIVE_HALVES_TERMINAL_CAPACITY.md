# A terminal-hazard strategy tolerating mass 5/2 per round

Status: authored PASS3 theorem for independent audit. It improves the
restricted weighted terminal lemma; it does not permit intermediate
lethal times or solve arbitrary mixed deadlines.

**Theorem.** Start with the zero nonnegative hazard field at time zero.
After each Angel move, an adaptive adversary may add a nonnegative field
of total mass at most `beta`, where `0<=beta<=5/2`. For any known
terminal time `T>=1`, the speed-one king Angel can guarantee
`g(a_T)<1`, counting updates through round `T-1` only, provided there
are no intermediate lethal requirements.

## 1. Endpoint geometry

Set `E_0=[-2,2]^2`. For `k>=1`, define

`E_k = union_{epsilon in {-1,1}^2}
       [3*2^(k-1) epsilon + E_(k-1)]`.

The four children are disjoint: each lies in a distinct sign quadrant,
with its closest coordinate of absolute value one. For `a=2^k`,

`|E_k|=25a^2`,
`R_k=3a-1`.

Every endpoint has king distance at most `R_k` from its center. At a
state with exactly `R_k` moves left, reaching a chosen child center
takes `3a/2` moves when `k>=1`, and leaves `3(a/2)-1=R_(k-1)` moves.
The child has `25(a/2)^2` endpoints.

## 2. Waiting and averaging

The case `T=1` is immediate because no update has preceded the first
move. For `T>=2`, choose the largest `k` with `R_k<=T` and set
`w=T-R_k`. Then `0<=w<=3a-1`.

Wait `w` moves. The average hazard on the initial translate of `E_k`
is at most `beta w/(25a^2)`. At each subsequent branch, choose a child
whose currently observed average is no larger than its parent's
average. Reach that child's center in the stated number of king moves.
Its added average during this traversal is at most

`beta*(3a/2)/(25(a/2)^2)=6 beta/(25a)`.

At the final base square `E_0`, exactly two moves remain. Summing over
all child scales shows that its average hazard is at most

`beta [w/(25a^2)+(6/25)(1-1/a)]`.

The geometric sum is empty for `a=1`, as required.

## 3. The two-move deficit finish

The deficit lemma in `TWO_MOVE_DEFICIT_RESERVE.md` wins the last two
moves whenever the base-square average is strictly below
`1-4 beta/25`. It therefore suffices that

`beta [w/(25a^2)+2/5-6/(25a)] < 1`.

Using `w<=3a-1`, the left side is at most

`beta [2/5-3/(25a)-1/(25a^2)] < 1`

for every `beta<=5/2`. The bracket is nonnegative, so replacing `beta`
by its upper bound is legitimate. Strictness remains at `beta=5/2`.

All block traversals and the initial wait end at time `T-2`. The
deficit-based first move then occurs at `T-1`; the adversary's update
after that move is precisely the one reserved by the base lemma.
The final safe neighbor is selected after observing that update.
No round-`T` update is counted or used retroactively.

## 4. Information and scope

The endpoint sets and waiting time depend only on the known terminal
time. Every branch uses the current field; the final two-move choice
uses current deficits. Future updates are never assumed known and may
adapt to every actual Angel move. Staying and all prescribed traversals
are legal king moves.

This is a stronger sufficient terminal theorem than the prior `9/4`
mass capacity. It is not claimed optimal. Its use in a mixed-deadline
strategy would still require a fully proved continuation certificate
covering every intermediate lethal time and every boundary update.
