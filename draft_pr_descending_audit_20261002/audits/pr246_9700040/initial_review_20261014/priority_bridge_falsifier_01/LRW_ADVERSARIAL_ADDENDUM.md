# Independent LRW 2001 adversarial addendum

Completed UTC: 2026-10-15. Bounded-audit completion estimate: 100%.

This is a separate route from the verified BO/Nica bridge. It was investigated
after root supplied a primary-source lead. No earlier family report was read.
Root later reported a false finite/unrestricted pile-count identity in another
draft; the proof here had already used finite-prefix autonomy instead. The
explicit false-identity control is retained below.

## Source and exact result used

[Levikson-Rolski-Weiss, “Layering of the Poisson process in the quadrant,” 2001](https://www.math.uni.wroc.pl/~pms/files/21.2/Article/21.2.11.pdf)
defines on printed page 420 the finite nearest-right downward-jump process,
started from 0<y_1<...<y_k, and the probability F_k(t;y) that the kth coordinate
has not jumped by t. Printed page 423, equation (2.4), and page 425, Theorem 2.5,
give

    F_k(1;y_1,...,y_k)=exp(-y_k) H_(k-1)(y_1,...,y_(k-1)),
    H_m(y)=det[ell_(i-j)(y_j)]_(i,j=1,...,m),
    ell_theta(z)=z^(theta/2) I_|theta|(2 sqrt(z)).

The source's definition (2.10) has the entire power series

    ell_theta(z)=sum_(p>=max(theta,0)) z^p/[p!(p-theta)!].

The determinant orientation is checked against the printed matrix: row 1 is
`ell_0(y_1),ell_-1(y_2),...`; row 2 starts `ell_1(y_1)`.
The source proves the determinant via the unique renewal integral equation,
not merely the exploratory differential equation: it explicitly warns that the
latter's boundary data alone do not select the correct solution. I inspected
the relevant definitions, equation, determinant, and proof structure; the
central pages were rendered and visually checked because OCR is poor.

The directly retrieved PDF has 3,126,456 bytes and SHA-256
`a5745a08113987d9a1db2b4b8403144c99a2f4a1355032538f8a588bccd6aa0d`.
Normal-certificate curl retrieval succeeded after Python's local certificate
store rejected the site. No certificate validation was disabled.

## Exact deterministic bridge, with finite and unrestricted counts separated

Fix 0<x_1<...<x_k=a and x_0=0. Define

    y_j=a-x_(k-j), j=1,...,k; y_0=0.

Then 0<y_1<...<y_k=a. Drive the finite ordinary Hammersley process with the
unit Poisson field during time (0,1). Events at coordinates >=a can be ignored:
the finite kth coordinate never exceeds a. Consider instead unrestricted
patience sorting of the augmented word

    y_1,y_2,...,y_k, followed by all event coordinates in chronological order.

Its first k pile tops equal the finite process after every event. This is
an induction: an event below the kth top changes the same first eligible top;
an event above it changes or appends only a later pile. Appending later piles
can never affect the updates of the first k.

Let M be the number of unrestricted final pile tops strictly below a. Small-value
compatibility removes the initial a and all event coordinates >=a. The ordinary
patience identity therefore gives

    M=LIS(y_1,...,y_(k-1), followed by the events below a).

This M can exceed k. The number of finite pile tops below a is **min(k,M)**,
not M. Since the finite kth coordinate is nonincreasing, it is still exactly a
at time 1 if and only if M<k. That is also equivalent to no kth jump.

For j=0,...,k-1, a subsequence using j initial entries has last initial value
at least y_j; choosing the first j initial entries attains y_j. All later entries
must lie above that value. Consequently the deterministic identity is

    M=max_(0<=j<=k-1) [j+L((y_j,a)x(0,1))].

Rotate the finite rectangle by `(u,t)->(a-u,1-t)`. The unit Poisson law is
unchanged. Increasing chains remain increasing when their order is reversed,
and every suffix rectangle `(y_j,a)x(0,1)` becomes the prefix rectangle
`(0,a-y_j)x(0,1)`. Thus

    {kth initial particle a has not jumped}
      = {L(x_r,1)<=r-1 for all r=1,...,k}

after rotation, jointly and pathwise. The equality is between events under this
deterministic reflection, not an equality of the two configurations before
reflection. These are exactly the candidate's stationary survival constraints.
Only finitely many Poisson events lie in this rectangle, so no infinite event
ordering or process limit occurs.

Combining this finite event identity with LRW's theorem yields

    P(X_1>x_1,...,X_k>x_k)
      =exp(-x_k) det[ell_(i-j)(x_k-x_(k-j))]_(i,j=1,...,k-1).

For k=1 the determinant is empty and equals 1. For k=2 the formula becomes
`exp(-x_2) ell_0(x_2-x_1)`, matching the known old two-particle expression.

## Boundary cases and every finite joint event

Poisson coordinates hit deterministic boundaries with probability zero.
The stationary particle coordinates likewise have no fixed atoms, since each
is a spatial Poisson point. Thus strict versus weak thresholds have the usual
continuous extension. The determinant is entire in each argument by the stated
series, so equal thresholds and zero thresholds follow continuously without
introducing an unproved stochastic limit theorem.

For arbitrary queries `(r_j,t_j)`, set k=max r_j and

    z_i=max({0} union {t_j:r_j<=i}), i=1,...,k,

after discarding nonpositive t_j. Then z_i are nondecreasing and

    {X_(r_j)>t_j for every j}={X_i>z_i for every i=1,...,k}.

The forward implication uses particle ordering; the reverse uses z_(r_j)>=t_j.
Apply the continuous extension of the ordered-threshold determinant at z.
This handles missing indices, repeated thresholds, and nonmonotone query indices.

## Accepted objection and negative control

The assertion “all events are below the initial last coordinate, hence ordinary
patience sorting never creates more than k piles” is false. With k=1, initial
particle 2, and chronological events 1/2 then 1, unrestricted patience sorting
creates two piles. The finite process has a single particle at 1/2. The correct
count relation is `finite_count_below_a=min(k,M)`. Both counts still give exactly
the same no-jump event through the condition M<k. This correction is essential
if the route is promoted; the false assertion cannot be left in a proof.

## Independent exact controls

`lrw_controls.py` uses direct finite-particle updates and a separate dynamic
programming LIS routine. It checked 154,589 chronological histories, k<=5 and
up to five distinct event coordinates, with unequal initial gaps and explicit
events above the initial last coordinate. In every case it checked:

- removal of outside-strip events;
- finite count = min(k,unrestricted augmented LIS);
- augmented LIS = maximum over suffix-chain values;
- no last jump = all rotated prefix-LIS bounds.

The script retains the one-particle counterexample against the false count
equality. A separate computation enumerates uniform permutations and independent
Poisson strip counts, without tableau dimensions or Schur weights. For k=2,3,4,5
at unequal threshold gaps, the raw series coefficients through degree 7 agree
exactly with the Bessel determinant. `LRW_CONTROL_RESULTS.json` records the
rational coefficients and timestamps. These are finite falsification checks;
the general proof is the deterministic identity above plus LRW's theorem.

## Assessment

I find no unresolved mathematical gap in this corrected LRW route. It produces
a finite determinant for the entire stationary joint survival law, an even
stronger explicit form than the submitted positive infinite sum. The exact
application/rotation bridge is written out here; I have not established that
LRW themselves printed it as an answer to the later drift-jump question.
Accordingly it reinforces complete automatic earlier mathematical coverage,
while preserving the distinction between a source's theorem and our explicit
identification of its application. The conclusion does not rely on the failed
finite/unrestricted count equality or on the BO/Nica route.
