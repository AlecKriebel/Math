# Independent audit of the short-lead bounded tracker

Decision: accepted for its stated restricted-threat scope.

Reviewed input: `pass3_independent/BOUNDED_TRACKING.md`, SHA-256 `f3aaf3404d9dcadd917ad9c027e284cf54c79cf05c0bf173b19ba30d6430887d`.

## Exact conclusion checked

For every real reference path starting at the origin with Euclidean step at most 1/100, the stated online controller takes legal king moves, avoids all bombs announced with effective lead at most 15, and stays within Euclidean distance 80 of that reference for all times. Other announcements consume budget but are ignored, with hypothetical continuation through their collisions. No probabilistic conditioning is needed for this tracking theorem.

This does not handle unrestricted leads. The mixed-lead corollary is a separate deliverable and is not accepted merely by this audit of its tracking dependency.

## Guard and timing

Before move n, the current short target sites A_n were announced no earlier than n−15. The next-time sites B_n were announced no earlier than n−14 and are known only through round n−1. Thus all distinct pairs counted in |A_n|+|B_n| have distinct announcement witnesses in the 15 rounds n−15,...,n−1. Repeated positions at different target times still require separate announcements. The bound m_n+b_n≤15 is therefore valid.

The inherited invariant m_n≤8 ensures a legal current move. The 3×3 expansion lemma bounds the next-time danger centers by max(0,b_n−7). Choosing a current-safe center outside that set leaves at most seven already-known short bombs in its next neighborhood. The new announcement after the move can add at most one, preserving the invariant. No same-round retroactive avoidance is assumed.

## Directional reserve

After reflection and coordinate exchange, a normalized direction has coordinates (u_1,u_2) with u_1≥u_2≥0 and sum one. The nine ordered projections in the input are correct. Their only ordering breakpoint in the interval is u_1=2/3, with endpoints 1/2 and 1. Maximizing rank loss gives exactly

(0,1/2,2/3,1,1,4/3,2,2,2).

If no future-danger center is removed, D_k≤m_n/2. Otherwise k=m_n+r_n and b_n≥r_n+7 give

D_k≤2(k+7)/13≤m_n/2+2b_n/13.

Scaling back from the L1-normalized direction to a Euclidean unit direction yields

projection≥1−(sqrt(2)/2)m_n−(2sqrt(2)/13)b_n.

The handling of negative lower bounds is correct: use the separate inequalities ||w||_1≥1 and ||w||_1≤sqrt(2), rather than multiplying a possibly negative quantity by an incorrectly ordered norm.

## Radial estimate

When the old error is at least 60, distance to the next reference point is at least 59.99. Every allowed move has Euclidean norm at most sqrt(2), and the Euclidean norm Hessian on the segment is bounded by 1/(59.99−sqrt(2)). Thus the quadratic remainder is below 1/50. Adding reference motion at most 1/100 gives the claimed decrement 97/100 minus the two bomb-count charges.

## Interval accounting and excursions

Each short bomb can contribute at most once to the sum of m_n and at most once to the sum of b_n over an interval, because each sum visits distinct detonation times. Both sums are bounded by N+15 using their announcement windows. A bomb may contribute to both sums, which is explicitly accounted for by the coefficient sum C=17sqrt(2)/26, not ignored.

The strict inequality C<93/100 is valid. An excursion entering error at least 60 begins below 62, since a move plus reference drift changes error by less than 2. During the rest of the excursion the accumulated excess is at most 15C, while the coefficient of the excursion length is negative. Hence the error stays below 62+15C<76<80. Excursions beginning or ending exactly at 60 are covered by the stated weak threshold in the radial inequality.

## Coupling compatibility

The reference may be real-valued. In a later stochastic coupling, only its fresh integer-valued net displacement must be uniform and independent of the earlier observed history. Given an independent real shift, a real square of side 160 contains at most 161² possible integer displacement values. Thus the small-ball counting step described in the input is valid even though the actual tracking error is correlated with later reference draws and Devil actions. Future reference randomness must remain inaccessible before the relevant block starts.

No correction to the reviewed tracker statement or proof is required.
