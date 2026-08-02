# Diagnostics for reflected stationary levels

Date: 2026-08-02 (America/Los_Angeles)

The candidate reflected-level inequality is

\[
 k\pi_k\le (n-k)(r-1)^{2k-n}\pi_{n-k},\qquad k>n/2,
\]

where `pi_k` is the total stationary mass of the dB geometric-union dual on
level `k`.  If `theta=r-1` and

**Status: OPEN.**  Every numerical statement below is diagnostic only.

\[
 h(A)=\frac{\pi(A)}{\theta^{|A|}},
\]

then the conjecture is equivalently

\[
 k\sum_{|A|=k}h(A)
 \le (n-k)\sum_{|A|=k}h(A^c).
\]

The aggregation over all sets of a fixed size is essential.  The pointwise
version is false.  For example, at `r=3/2` on the four-vertex graph

\[
 W=\begin{pmatrix}
 0&1&2&5\\
 1&0&3&1\\
 2&3&0&4\\
 5&1&4&0
 \end{pmatrix},
\]

the set `A={0,2,3}` gives numerically

\[
 |A^c|h(A^c)-|A|h(A)=-0.03537557649\ldots.
\]

Two other tempting strengthenings at `r=2` also fail in direct numerical
screens:

1. the sequence `pi_k/binom(n-1,k)` need not be log-concave;
2. the complete-graph level law need not dominate all upper tails (already
   a five-vertex positive-weight example violates the tail comparison at
   level two), even though the complete-graph mean remained larger in every
   test.

Finally, pairwise negative correlation is false, even exactly at `r=2`.
For the positive integer weights

\[
 (w_{01},w_{02},w_{03},w_{12},w_{13},w_{23})
 =(30,20,30,20,30,1),
\]

the exact stationary covariance of the indicators of vertices 2 and 3 is

\[
 \frac{80738385242712417797218479495402739}
 {12986979462920913004371912333407883289}>0.
\]

The companion exact verifier constructs the geometric-union generator and
solves its stationary equations symbolically.  Thus neither association nor
negative association may be used in a proof of the aggregate reflection
inequality.

There is, however, a useful exact event-chain reformulation.  If

\[
 R(A,B)=\sum_{v\in A}G_v(A,B),
\]

where `G_v` is the one-target burst kernel, stationarity of the continuous
time chain gives

\[
 \sum_A\pi(A)R(A,B)=|B|\pi(B).
\]

Consequently the embedded graphical-event chain has stationary measure
proportional to `|A| pi(A)`.  The reflected-level conjecture is precisely a
reflection inequality for this event-stationary measure after the product
tilt `theta^{-|A|}`.  This event-Palm formulation survives all diagnostics
above and is the current preferred proof route.
