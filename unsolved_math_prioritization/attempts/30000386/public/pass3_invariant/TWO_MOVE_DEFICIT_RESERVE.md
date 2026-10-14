# A sharp two-move terminal deficit reserve

Status: authored PASS3 lemma for independent audit. The hypothesis
excludes intermediate lethal times. It is not a mixed-deadline solution.

## 1. Weighted terminal game

At a post-announcement state, the Angel is at `a` with exactly two moves
remaining until a sole terminal requirement `g(a_final)<1`. The current
field `g:Z^2->[0,infinity)` is nonnegative. After the first of these two
moves, the adversary may add any nonnegative field of total mass at most
`beta`. The adversary observes that first move before choosing its
update. There is no other lethal time.

Let `S=a+[-2,2]^2`, of cardinality 25, and let
`M=sum_{x in S} g(x)`.

**Lemma 1.** If `M<25-4 beta`, the Angel can meet the terminal
requirement against every such adaptive update.

**Proof.** Define the current deficit `d(x)=max(1-g(x),0)`. Its total
on `S` is at least `25-M>4 beta`. The four side-three neighborhoods
centered at `a+(epsilon_1,epsilon_2)`, with both epsilons in `{-1,1}`,
cover `S`. Hence the sum of their deficit totals exceeds `4 beta`, and
one neighborhood has total deficit greater than `beta`.

Move to that neighborhood's center. This is one legal king move. To
raise every value in its nine terminal neighbors to at least one, the
adversary would have to add at least the sum of their current deficits,
which exceeds its mass budget. Thus, after observing the update, the
Angel can choose a terminal neighbor with value strictly below one.
All choices use the observed field, and the adversary was allowed to
adapt to the selected first move.

## 2. Sharpness of the total-mass threshold

For `0<=beta<=4`, the threshold `25-4 beta` is sharp among guarantees
using only the total mass in the full side-five square against arbitrary
nonnegative updates of mass at most `beta`.

Translate to `a=0`. On the sixteen positions of `[-2,2]^2` with both
coordinates nonzero, set `g=1-beta/4`. On its remaining nine positions,
set `g=1`. Values outside the square are irrelevant. The total mass is
`25-4 beta`.

Every side-three neighborhood centered at a legal first move has
exactly four positions with both coordinates nonzero. Its total deficit
is therefore exactly `beta`. After seeing the first move, the adversary
fills those four deficits, spending total mass exactly `beta`, and
makes all possible final moves have value at least one.

For the original unit point-bomb version, the post-boundary threshold
21 is also sharp: preload all positions in `[-2,2]^2` except its four
corners. Each legal first move has at most one unbombed terminal
neighbor. The Devil can fill that neighbor if present, or make an
irrelevant announcement if it is absent. This uses 21 preloaded bombs.

## 3. Boundary announcement reserve

Suppose an additional update of total mass at most `beta` occurs just
before the first of the two Angel moves, after an earlier lethal move.
If the pre-boundary local mass satisfies

`M<25-5 beta`,

then the boundary update raises it to less than `25-4 beta`, and
Lemma 1 applies. Thus a sufficient uniform side-five smoothing
denominator is

`D=25-5 beta`,

when this is positive. This reserve treats the boundary update
universally; it is not assumed observed before the earlier move.

For unit point bombs, the pre-boundary count threshold 20 is sharp:
remove one additional noncorner position from the 21-bomb example,
then fill it with the boundary announcement. The remaining terminal
announcement completes the trap after observing the first move.

## 4. Exact logical scope

The weighted update adversary is stronger than a unit point-bomb
adversary, so the positive weighted lemma can be used for smoothed
hazard fields. Its fractional sharpness example is not asserted to be
an original-game Devil strategy when the update is not a point bomb.
The separately stated unit-point examples are original-rule local
preloaded states, not forced states from the empty initial board.

The lemma is a genuine robust online two-move continuation certificate.
It does not protect an intermediate lethal time on its first move.
