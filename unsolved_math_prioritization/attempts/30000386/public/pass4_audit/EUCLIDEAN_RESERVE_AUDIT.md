# Acceptance: Euclidean reserve and the restricted light-layer tracker

Shared PASS4 independent audit of `../pass4_coupling/EUCLIDEAN_RESERVE_PRELIMINARY.md`, SHA-256 `2c7aa552806528d0a0d3777354df5c9ea0d0cebc68d027c6600f8f45a92a3af2`.

## Decision

Accepted without a mathematical correction. The first result improves the accepted lead-through-fifteen tracker to reference speed 1/4 and radius 20. The second permits any fixed maximum lead H only under the additional global restriction of at most eight handled bomb sites at each target time. Neither is an arbitrary-H unrestricted result.

## 1. Euclidean rank minima

By symmetry write a unit direction as (u,v), u≥v≥0, u²+v²=1. The nine sorted projections are exactly those displayed in the source. The coordinate-axis, diagonal, and u=2v directions produce the claimed rank minima:

1, 1/√2, 1/√5, 0, 0, −1/√5, −1, −1, −√2.

For the third largest projection, max(v,u−v) is minimized where u=2v, giving 1/√5. For the sixth, the negative of min(v,u−v) is minimized at the same point. The remaining extrema follow directly from the axis/diagonal endpoints. Thus the table handles ties and all intermediate directions, not just tested angles.

The inequalities 1−R_k≤k/3 and 1−R_k≤(k+7)/6 hold at every k=0,…,8. The tight current-only constraints are k=3 and k=6. For the second family the largest potentially close case is k=8, where 1+√2<5/2.

## 2. Guarded reserve and lead-fifteen tracking

Retain the accepted guard: m≤8 current forbidden neighbors, m+b≤15 current/next pairs, and r next-guard-excluded moves satisfying r=0 or b≥r+7. At most m+r≤8 moves are excluded. If r=0, the first rank inequality gives reserve 1−m/3. Otherwise

m/3+b/6≥(m+r+7)/6+m/6≥1−R_(m+r),

so an admissible move has inward Euclidean projection at least 1−m/3−b/6.

For reference speed at most 1/4 and preceding error at least 10, the next-reference distance is at least 39/4. The Taylor remainder is below 1/8 because 39/4−√2>8. The actual selected maximal-projection admissible move therefore obeys

d_n≤d_(n−1)−5/8+m_n/3+b_n/6.

On an N-round excursion, each count sum is at most N+15 by the accepted distinct-announcement witness argument. Summation gives d_end≤d_start−N/8+15/2. Entry from below 10 has overshoot less than √2+1/4<2, so every error is below 12+15/2=19.5<20. Initialization and current-move safety remain those of the previously audited guard.

No intermediate lethal check is omitted; the admissible set checks every current short target, and the following announcement is reserved in the next-time guard.

## 3. Arbitrary-H light-layer statement

Assume every handled announcement has lead at most H and each target time contains at most eight handled bomb sites in total. Then every move has at least one safe neighbor without a next-layer guard. Applying the current-only Euclidean reserve yields

d_n≤d_(n−1)−5/8+m_n/3

outside the same radius-ten threshold. The witness bound is sum m_n≤N+H on every N-round interval. Therefore an excursion gains at most H/3, since the coefficient −5/8+1/3=−7/24 is negative. Entry error is below 12, proving the stated radius 12+H/3.

The restriction concerns the eventual total for each layer, not merely the number announced so far. A full-game Devil may later make a currently light layer heavy. The theorem supplies no justified online classification of such layers and cannot be applied to all bounded-H announcements without that extra restriction.

## Scope boundary

The refined constants change neither the guard's state nor its responsiveness to distant announcements. They do not refute the separate legal lead-sixteen attack on that fixed local policy. No empty-board negative conclusion for all H=16 strategies, or positive conclusion for arbitrary H without the light-layer restriction, is accepted here.
