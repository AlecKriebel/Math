# A chronology-triggered rescue strategy for maximum lead sixteen

Status: authored PASS4 candidate for independent audit. This proves a
bounded-lead statement from the empty initial history, not merely the
existence of a favorable preloaded state. It does not claim all finite
maximum leads or unrestricted survival.

Use `N(x)=x+{-1,0,1}^2`, and define for a finite spatial set `B`

`A8(B)={x: |N(x) intersect B|>=8}`,
`E(B)={x: N(x) is a subset of B}`.

## 1. A small-set geometric bound

**Lemma 1.** If `|B|<8`, then `A8(B)` is empty. If `|B|=8`, its
cardinality is at most one. If `9<=|B|<=16`, then

`|A8(B)|<=|B|-8`.

**Proof.** Put `Q=A8(B)`, `k=|Q|`, and assume `k>0`. The set is finite.
If `Q` occupies `r` rows and `c` columns, horizontal and then vertical
expansion gives

`|Q+{-1,0,1}^2|>=k+2r+2c+4>=k+4 sqrt(k)+4`.

For the first inequality, horizontal expansion adds at least two sites
per occupied row, and the resulting set has at least `c+2` occupied
columns, each gaining at least two sites upon vertical expansion.
The second follows from `rc>=k`.

Every neighborhood of a point of `Q` has at most one point outside
`B`. Assign each missing point of the union to a neighborhood containing
it. Distinct missing points cannot be assigned to the same neighborhood,
so there are at most `k` missing points. Therefore

`|B|>=4 sqrt(k)+4`.

For `|B|=8` this gives `k<=1`. For `9<=b=|B|<=15`,
`(b-4)^2/16<b-7`, since `(b-8)(b-16)<0`; hence the integer `k` is at
most `b-8`.

For `b=16`, the same estimate gives `k<=9`. If `k=9`, the missing-point
bound gives `|N(Q)|<=25`, while the row/column estimate forces
`r+c<=6`, `rc>=9`, hence `r=c=3`. Thus `Q` is the Cartesian product
of its three rows and three columns. Its expanded product has size at
most 25, forcing both row and column sets to be three consecutive
integers. Therefore `Q` is a full side-three square. The four corner
neighborhoods of that square cover its full side-five neighborhood;
each has at most one missing point of `B`. There are consequently at
most four missing points, requiring `|B|>=25-4=21`, a contradiction.
Thus `k<=8` when `b=16`.

## 2. Three-move rescue with fifteen future preloads

**Lemma 2.** Before a move at time `s`, suppose at most one currently
lethal site is known. Suppose also that the preloaded bomb sets `B_1`
and `B_2` for times `s+1` and `s+2` have total cardinality at most 15.
Then from any current position the Angel can survive moves
`s,s+1,s+2`, against arbitrary one-per-round announcements after the
first and second moves. Bombs with other time coordinates do not affect
these three moves.

Here all three lethal moves are protected; the first move is not treated
as a harmless terminal-only traversal.

### Exact bad first positions

Write `m=|B_1|`, `b=|B_2|`, and `D=B_1 union A8(B_2)`. From a chosen
first position `q`, the remaining two moves are losing against a final
new announcement exactly when `N(q)` is contained in `D`: a currently
safe second move must have at most seven preexisting terminal bombs in
its neighborhood.

After the Devil's first new announcement, the set of first positions
from which it can create such a losing state is contained in the union
of the following two sets:

- `F_1=A8(D)`, covering an announcement at time `s+1`;
- `F_2=union_w E(B_1 union A8(B_2 union {w}))`, covering an announcement
  at time `s+2`.

An irrelevant announcement is already covered because
`E(D)` is contained in `F_1`. In fact these formulae describe the exact
union, but containment suffices below.

### At most seven first positions are bad

- If `b<=6`, then `A8(B_2)` and every `A8(B_2 union {w})` are empty.
  Hence both kinds of bad position lie in `A8(B_1)`, whose cardinality
  is at most seven because `m<=15`, by Lemma 1.
- If `b=7`, then `m<=8`, so `|F_1|<=1`. Any center in
  `A8(B_2 union {w})` must contain all seven distinct points of `B_2`
  in its side-three neighborhood. There is at most one such center,
  independent of `w`: seven points fitting in a side-three square must
  span all three coordinate values in both coordinates, since two rows
  or columns could hold only six. Thus all the possible augmented sets
  are contained in one fixed singleton `{v}`. The set
  `B_1 union {v}` has at most nine points and contains at most one full
  side-three neighborhood. Therefore `|F_2|<=1`, and the union has size
  at most two.
- If `b=8`, then `m<=7` and `|A8(B_2)|<=1`, so `|D|<=8` and
  `|F_1|<=1`. Every augmented terminal set has at most nine points, so
  its `A8` set has at most one point. Consequently
  `|B_1 union A8(B_2 union {w})|<=8`; `F_2` is empty.
- If `9<=b<=15`, then `|A8(B_2)|<=b-8`, whence `|D|<=7` and
  `F_1` is empty. By Lemma 1, every augmented terminal set has at most
  `b-7` bad centers. Thus
  `|B_1 union A8(B_2 union {w})|<=m+b-7<=8`, and `F_2` is also empty.

There are nine possible first moves, at most seven bad positions, and
at most one currently lethal position. At least one first move is
therefore safe and outside `F_1 union F_2`.

Choose it. After observing the new announcement, choose a safe second
move whose neighborhood has at most seven existing time-`s+2` bombs.
The following announcement raises that number by at most one. A safe
third move exists among its nine neighbors. This is an online strategy
with a universal response to each of the two new announcements.

## 3. Controller for announcements of lead at most sixteen

Assume the initial history is empty and every effective announcement
after round `r` has `1<=t-r<=16`. Before move `n`, let `A_n` and `B_n`
be all already announced sites at times `n` and `n+1`, and let the
current position be `a`. The ordinary guard is

`|A_n intersect N(a)|<=8`.

An ordinary admissible move is a `q in N(a)\A_n` with
`|B_n intersect N(q)|<=7`. Such a move preserves the guard after the
next Devil announcement.

Use this controller:

1. Before an ordinary move `s`, if the already announced sets at
   `s+1` and `s+2` together contain 15 distinct pairs, start the
   three-move rescue of Lemma 2 and run it through time `s+2`.
2. At every other ordinary move, choose any ordinary admissible move.
3. After a rescue, return to ordinary mode.

The trigger's hypotheses hold by announcement chronology. All fifteen
trigger pairs must have been announced in rounds `s-15,...,s-1`:
an earlier announcement cannot target even `s+1` with lead at most
sixteen. These are exactly fifteen rounds, so they account for every
announcement in that interval. At most one older announcement, from
round `s-16`, can still be currently lethal at time `s`; all earlier
ones are expired. There are no other preexisting future bombs.

Thus Lemma 2 applies. At rescue completion, all fifteen trigger pairs
and any older currently lethal pair are past. Only the three
announcements made in rounds `s,s+1,s+2` can remain pending. Hence the
ordinary guard is restored, with at most three current/next bombs.

## 4. Why an ordinary guard failure is unreachable

The guard holds initially. Consider an ordinary state where it holds,
but suppose no admissible ordinary move existed. Put
`Q=N(a)\A_n`, so `|Q|>=1`. Every `q in Q` would have at least eight
neighbors in `B_n`.

The accepted local neighborhood lemma gives
`|B_n|>=|Q|+7=16-|A_n intersect N(a)|`.
For completeness, when `Q` lies in a side-three square the expansion
estimate gives `|N(Q)|>=2|Q|+7`, and the same missing-point injection
used above gives this bound.

Therefore at least sixteen distinct current/next pairs were previously
announced. All their witnesses lie in the sixteen rounds
`n-16,...,n-1`; hence there are exactly sixteen pairs and all those
rounds announced a pair at `n` or `n+1`.

At the preceding move `n-1`, the first fifteen of those pairs were
already known, all at its next two times. If that move was ordinary,
the controller necessarily started a rescue, so the move at `n` would
be inside it, a contradiction. If move `n-1` was inside a rescue, then
either `n` remains inside that rescue or `n-1` was its final move.
In the latter case at most three pending announcements remain, which
cannot give the sixteen-pair failure. These exhaust the possibilities.

Thus ordinary admissible moves always exist whenever requested. The
guard and each rescue guarantee survival, and every rescue has a valid
reset. This constructs one infinite online winning strategy for the
maximum-lead-sixteen game from the empty history.

## 5. Boundary of the result

The proof crucially uses that sixteen threatening pairs exhaust a
sixteen-round announcement window. That turns a possible local failure
into a previously observable rescue trigger and gives a clean reset.
It does not assert that an arbitrary preloaded sixteen-pair trap is
unreachable under every Angel policy, or that this trigger works for a
larger lead bound. Extending the method requires a scalable rescue
certificate and a valid chronology/reset argument for larger windows.
