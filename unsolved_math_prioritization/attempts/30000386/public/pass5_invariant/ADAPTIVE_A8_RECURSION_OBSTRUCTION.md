# Four newly dangerous centers from one later-time announcement

Status: final shared PASS5 counterexample to a precisely stated
backward-layer certificate. It is not a losing strategy from empty
history and does not obstruct arbitrary nonlinear online invariants.

## 1. The candidate certificate

For finite B, write

`A8(B)={q: |(q+{-1,0,1}^2) intersect B|>=8}`.

For three preloaded time layers A,B,C, a tempting backward calculation
is

`D_3=C`, `D_2=B union A8(C)`,
`D_1=A union A8(D_2)`.

It accounts for a single added next-layer point at each step by
reserving two safe neighbors. The candidate sufficiency claim is that
a legal first move outside D_1 guarantees three-move online survival.
The claim is false because an announcement directed to a later layer
can create several new intermediate danger centers at once.

## 2. Exact sets

Let `N=N(0)={-1,0,1}^2`, and put `Q={0,1}^2`. Define

`C' = {-1,0,1,2}^2 minus {(-1,-1),(-1,2),(2,-1),(2,2)}`,
`p=(0,0)`, `C=C' minus {p}`,
`B=N minus Q`, `A=N minus {0}`.

The sizes are `|A|=8`, `|B|=5`, `|C|=11`, `|C'|=12`.
Preload A at time 1, B at time 2, and C at time 3, starting from
position zero before move 1. There are twenty-four distinct pairs.

The exact dense-center identities are

`A8(C)=empty`, `A8(C')=Q`.

Indeed, each q in Q has a side-three neighborhood containing exactly
eight points of C': the only missing point is its corresponding
extreme corner of the side-four square. All four neighborhoods contain
p, so removing p lowers each count to seven. For a center outside Q,
at least one coordinate lies outside {0,1}; in that coordinate its
neighborhood meets at most two columns or rows of the side-four set.
The exterior column or row has only two C'-points, so such a
neighborhood contains at most five C'-points. It cannot be a dense
center for either C' or C.

## 3. Failure of the backward certificate

Since `A8(C)=empty`, the proposed recursion gives `D_2=B`. Since B
has only five points, `A8(B)=empty`, so `D_1=A`. The origin is a
legal first move outside D_1, and in fact it is the only first move
that avoids the preloaded current layer A.

After this forced first move, the Devil announces (p,3). The new
terminal set is C'. Every time-2 move either lies in B and dies
immediately, or lies in Q. For any chosen q in Q, exactly eight of
its nine time-3 neighbors lie in C'. The Devil's announcement after
move 2 fills the remaining neighbor at time 3, forcing loss on move 3.

Thus the state is losing within three moves despite the candidate's
first-move certificate. It is nevertheless viable for two moves:
the first move to zero is safe, and after one new announcement the
time-2 neighborhood has at most six lethal points.

The precise amplification is one newly added terminal point producing
four new intermediate danger centers. It is not caused by treating
multiple simultaneous announcements as legal, omitting a stay move,
or revealing an announcement before the Angel's preceding move.

## 4. Legal preload chronology

The state is in the exact maximum-lead-24 arena. The tail counts are

`N_1=24`, `N_2=16`, `N_3=11`,

which satisfy `N_j<=24-j+1`; all sites lie in their relative reachable
cones. This is the smallest possible H for its total pending count.

For an explicit existential history, let the Angel stay at zero
through absolute round 24. Announce the eight A-pairs targeting time
25 in rounds 1 through 8, the five B-pairs targeting time 26 in
rounds 9 through 13, and the eleven C-pairs targeting time 27 in
rounds 14 through 24. Their leads are respectively 24 through 17,
17 through 13, and 13 through 3. They are all legal and none has
detonated by round 24. This is a cooperating-history realization,
not a Devil strategy forcing entry against every Angel.

## 5. Scope for nonlinear closure envelopes

A uniform mass envelope for repeated applications of A8 may still be
useful. This example does not contradict such an envelope. It shows
that controlling repeated A8 operations on a fixed set does not by
itself justify replacing the exact adaptive, mixed-time predecessor
by the displayed backward recursion. Any proposed envelope-based
strategy must additionally pay for changes in intermediate danger
sets caused by announcements at later times and prove that the same
legal move satisfies all continuation constraints.
