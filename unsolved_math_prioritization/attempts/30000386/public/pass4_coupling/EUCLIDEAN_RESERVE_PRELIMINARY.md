# Cleaner Euclidean reserve for the two-layer tracker

Status: PASS4 preliminary lemma, submitted for independent audit. This improves constants of an accepted proper restriction; it is not an arbitrary-lead extension. The separate legal lead-sixteen defeat explains why this local controller needs new history-aware logic before it could solve the full problem.

## 1. Rank bound

Let w be a Euclidean unit direction. Sort its nine king-step projections from largest to smallest. After any k excluded moves, the largest remaining projection is at least R_k, where

    k:   0     1          2       3  4      5        6   7     8
    R:   1  1/sqrt(2) 1/sqrt(5)  0  0 -1/sqrt(5) -1  -1 -sqrt(2).

By reflections and coordinate exchange, take w=(u,v), u>=v>=0, u^2+v^2=1. The sorted values are

    u+v, u, max(v,u-v), min(v,u-v), 0,
    -min(v,u-v), -max(v,u-v), -u, -u-v.

The coordinate-axis direction, diagonal direction, and direction u=2v give the displayed minima. In particular, for 0<=k<=8,

    1-R_k <= k/3,
    1-R_k <= (k+7)/6.

These inequalities can be checked directly; the extremal current-only constraints are k=3 and k=6.

## 2. Guarded directional reserve

Use the accepted short-lead-through-fifteen guard. Let m be current forbidden positions in the Angel's nine-move neighborhood, and b the total known next-time bomb positions. Its invariant gives m<=8 and m+b<=15. If r guard moves are excluded because their next neighborhoods contain at least eight next bombs, the geometric lemma gives either r=0 or b>=r+7.

If r=0, the rank bound gives projection at least 1-m/3. If r>0, put k=m+r<=8. Then

    m/3+b/6 >= m/3+(r+7)/6 = (k+7)/6+m/6 >=1-R_k.

Hence a guard-admissible move always satisfies

    w dot delta >= 1-m/3-b/6.                    (1)

## 3. Improved bounded tracking

Start the Angel and reference together at a_0=z_0=(0,0). For a real reference of Euclidean speed at most 1/4, choose the same admissible move of maximal projection toward its next point. Outside preceding error 10, the next-reference distance r is at least 10-1/4=39/4. The Euclidean Taylor remainder is bounded by

    1/(r-sqrt(2)) <= 1/(39/4-sqrt(2)) <1/8,

since sqrt(2)<7/4. Thus

    d_n <= d_(n-1)-5/8+m_n/3+b_n/6.              (2)

For any N-round interval the accepted lead-fifteen witness count gives each of sum m_n and sum b_n at most N+15. On an excursion above error 10, summing (2) gives

    d_end <= d_start-N/8+15/2.

The step first crossing error 10 has new error less than 10+sqrt(2)+1/4<12. Every subsequent point in the excursion has error less than 12+15/2=39/2<20. Therefore the same short-lead controller tracks every speed-1/4 reference within Euclidean distance 20.

## 4. Related arbitrary-H light-layer lemma

Again start at a_0=z_0=(0,0). Suppose instead that all bombs being handled have lead at most a fixed H, and each target time has at most eight such bomb sites in total. Ignore any other bombs. There is always a legal immediately safe move, without any next-layer guard. Choose it to maximize projection toward the next reference point. The rank inequality now gives w dot delta>=1-m_n/3.

The same radial calculation for reference speed 1/4 and threshold 10 yields

    d_n <= d_(n-1)-5/8+m_n/3.

Over any N-round interval the total current-time count is at most N+H, by charging each bomb to its distinct announcement round. Consequently each excursion above 10 has additional increase at most H/3, and the full error is strictly below

    12+H/3.

This proves bounded tracking for every finite H under a global eight-bombs-per-target-time restriction. The original game allows heavier layers, so this is not an unrestricted bounded-H theorem. One cannot classify a future layer as permanently light merely because fewer than nine bombs have been announced so far.
