# Independent acceptance: continuous two-layer lead-sixteen invariant

Accepted input: `pass4_coupling/LEAD16_INDEPENDENT_AUDIT_AND_CONTINUOUS_PROOF.md`,
SHA256 `6b87f9ef63851c16fb171bd79acdf4bc0542d2dbe8db21276c5d11599ccf4e22`.
This is the same H=16 advance as the chronology-triggered rescue theorem,
with a different continuous invariant proof. It does not increase H.

## Robust-choice lemma

If at least seven centers Q lie in one 3 by 3 square, Q occupies three rows
and columns. The expansion estimate gives |N(Q)|>=|Q|+16. If every center
has eight neighbors in B, the missing-point injection gives |B|>=16.
For all nine centers the four corner neighborhoods instead give |B|>=21.
Both stronger local bounds used in the input are valid.

Now let |A|+|B|=15 be the known next-two-layer loads.

If 2<=|A|<=7, choose two distinct A-points. Their sets of containing
king-neighborhood centers have intersection of size at most six: two
shifted side-three integer squares intersect in at most 2 times 3 points.
Consequently at least three q in N(a) omit an old A-point. They already
have at most seven A-neighbors.

If 8<=|A|<=15, seven centers with eight A-neighbors would contradict the
stronger local bound. Again at least three q have at most seven A-neighbors,
and each omits an A-point. For either case, after any one new announcement,
the omitted old A-point remains outside N(q), so

|A' intersect N(q)|<=8,
|A' intersect N(q)|+|B'|<=15.

The ordinary local lemma makes these sufficient for a safe next position
with at most seven terminal neighbors. The single update is reserved, not
averaged, and it can target either layer or an irrelevant time.

Finally, if |A|<=1, every q is robust. After an update, |A'|<=2 and
|A'|+|B'|<=16. If A' is nonempty, at least seven currently safe centers
are available while |B'|<=15, contradicting the stronger bound if all
were bad. If A' is empty, all nine are available and |B'|<=16<21.
Thus every asserted robust choice is valid against every first update and
supports a safe second move against the following adaptive update.

## Continuous preservation

Before move n, I_n is exactly the assertion that some current-safe q has
at most seven known time-(n+1) neighbors. This is the correct two-move
winning condition with one new announcement between the moves.

The next-two known layers A,B at n+1,n+2 have total F<=15 by the exact
fifteen-round birth window. If F<=14, a move witnessing I_n is currently
safe, and after the next announcement its next-layer neighborhood contains
at most eight bombs while the next-two-layer total is at most fifteen.
The ordinary local bound therefore reestablishes I_(n+1).

If F=15, these pairs exhaust the fifteen newest relevant slots, leaving
at most one known current-time bomb from the one older slot. The robust
lemma supplies at least three possible moves; deleting that current lethal
site leaves a valid safe move. Its universal update property gives I_(n+1).
This handles every intermediate death check and every Devil announcement.

I_1 holds at the empty initial history. Induction proves infinite online
survival for maximum effective lead sixteen. The robust-choice proof and
chronology are independently verified; no computation is needed.
