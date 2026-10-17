# Independent audit: three arbitrary known allowed deadlines

Audited artifact: `../pass2_deadlines/THREE_DEADLINES.md`.

SHA-256:
`8f28f7e3c47dae09fb1fa3067dccaa940b7e2862eda756f8f6020d5d4d386403`.

Date: 2026-10-14. This review belongs to shared PASS2.

## Result

No mathematical defect found. The artifact proves online survival in
the exact two-dimensional speed-one king game when the allowed bomb
times are any three known positive integers `U<V<W`. The proof handles
adaptive position/time choices within that allowed set and reserves the
announcement after each lethal move. It does not establish a uniform
theorem for arbitrary finite sets or the unrestricted conjecture.

## Geometry and update accounting

- At scale `a=2^k`, the four child endpoint sets are disjoint because
  their containing coordinate intervals are separated at zero. Their
  total cardinality is `9a^2`, and the radius is `2a-1`.
- Reaching a chosen child center uses `a` legal king moves and leaves
  exactly `a-1` moves, matching its radius. Recursion ends with the full
  nine-neighbor terminal set and one remaining move.
- For an arbitrary gap, the initial wait obeys `0<=w<=2a-1`.
  The wait and traversals together use exactly `r-1` moves, so all
  charged updates occur before the final move.
- The traversal charge is
  `beta*(4/9)(1-1/a)`. Including the maximum wait gives
  `beta*[4/9-(2a+1)/(9a^2)]`, strictly below one for `beta<=9/4`.
- For a general profile family, a child has `9b^2` endpoints and is
  reached in `2b` moves. Thus its charge `2b C_b` is correct even though
  the endpoint set need not be a contiguous square.
- The backward denominator uses `w+1<=2a`, so it explicitly includes
  every possible boundary announcement. The implication starts from a
  strict pre-boundary hazard inequality and retains strictness.
- Convolution gives the stated mass and peak upper bounds. Equality of
  a profile bound with an actual concentration is not needed; all uses
  are valid upper bounds.

## Algebra and profile regimes

For the last gap, `D_c=5c^2+2c`, `B_c=9c/(5c+2)>1`. The crossover
between the delta and smeared profiles occurs at the dyadic scale `c`:
for `b<c`, `b<=c/2` implies `9b^2<D_c`; for `b>=c`, the smeared mass
bound applies and dominates the delta mass.

When `a<c`, the stated three crossover ranges follow from
`9a^2<D_c` and, for `b<c`, `9b^2<D_c`. The dyadic sums give precisely

`F=(4/9)[1+g(a)+B_a g(c)]`.

The bounds `g(1)=2/7`, `g(x)<=1/4` for dyadic `x>=2`, and `B_a<9/5`
yield the stated strict upper bound `27/35`.

When `a>=c`, independently expanding the charged sums gives

`D=a^2[5-4(B_c-1)/c]+2B_c a`.

Dividing by `B_c` gives the stated
`lambda(c)=(25-6/c+8/c^2)/9`. Its lower bound `8/3` uses the dyadic
restriction importantly: `(c-2)(c-4)>=0` holds for the allowed values
`1,2,4,8,...`. Its upper bound follows from `(c+4)(c-1)>=0`.

The far profile dominates the middle profile in both coordinates.
For `b<a`, the delta dominates because
`4/(9a^2)>1/[lambda(c)a^2+2a]`; for `b>=a`, the far mass dominates.
The resulting dyadic sum is exactly

`F=4/9-4/(9a)+4/[lambda(c)a+2]`.

The case `a=c=1` gives `4/5`. For `a>=2`, using `lambda(c)>=8/3`
gives the artifact's positive difference numerator
`4[32(a-2)^2+57(a-2)+16]`. Therefore `F<=4/5<1`.

## Online composition and scope

The allowed deadlines determine fixed scales and denominators before
play. The actual hazard fields use only announced bombs. The first
phase's strict terminal certificate guarantees survival at `U` and the
robust start of the phase to `V`, uniformly over the announcement after
move `U`. The same reasoning at `V` guarantees the phase to `W`.
There are no allowed intermediate lethal times inside any traversal.

No stage selects an offline path after observing future announcements.
The final infinite continuation is valid because all three allowed
deadlines are past after `W`. Repeated or past-time announcements only
reduce effective updates.

The proof exploits a three-kernel/two-gap structure. Neither this audit
nor the artifact supplies the larger-family induction required for
arbitrarily many deadlines. No historical novelty claim is audited.
