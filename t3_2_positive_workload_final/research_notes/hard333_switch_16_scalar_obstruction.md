# Exact scalar obstruction on the hard-333 switch sixteen

## 1. Scope

The exact hard-333 composition leaves sixteen potential switches:

- twelve pairs whose all-active proof uses a rate-dependent invariant
  (H_b); and
- four homogeneous rank-two pairs whose all-active proof uses total
  population (H_w=A+B+C).

This note tests the most direct proposed interface,

\[
  V_q=W_\ell+\eta(1+H)^q,
  \qquad
  W_\ell=\left(K_\ell+\sum_i\log(x_i!)+\ell\cdot x\right)^4,
  \qquad \eta>0.                                      \tag{1.1}
\]

There is an exact exponent conflict in each branch.  No fixed (q) makes
(1.1) simultaneously absorb the all-active stochastic curvature and the
positive workload endpoint of the unchanged hard (W_\ell)-episode.

This is **not** a counterexample to recurrence or T3-2.  It proves only that
the all-active workload cannot be added directly to the already repaired
hard episode.  A marked or stopped workload-repayment block is still
possible.  All analytic, pair-recurrence, and global flags remain false.

The exact sixteen-pair fingerprint is

```text
35aa9260eedf3305abf6ec72704beec44394ecaa851ce7dc045e4d3c899d9896
```

Their failed-incidence histogram is (50,56,64) in active dimensions
one, two, and three.  The hard dormant rows have resistance histogram

\[
                 4\times0+10\times1+2\times2.          \tag{1.2}
\]

## 2. An exact (H_b) witness

Take

\[
 T=\{2A,B+C\},\qquad
 R=\{0,A,2B,A+B\}.                                    \tag{2.1}
\]

Give (T) both directions with unit rates, and orient (R) as the unit-rate
strong cycle

\[
                 0\longrightarrow A\longrightarrow A+B
                 \longrightarrow2B\longrightarrow0.   \tag{2.2}
\]

The applicable all-active workload is

\[
                         H_B=2A+B+3C.                  \tag{2.3}
\]

Both top complexes have (H_B)-value four, so every top firing is exactly
(H_B)-neutral.

### 2.1 All-active curvature forces (q>21/5)

At

\[
                         x_N=(N^3,N,N^5),              \tag{2.4}
\]

the two top propensities are both (N^{6+o(1)}).  For (ell=0), which is
the unit-rate detailed-balance adjustment, the forward factorial increment
is (N^{-1+o(1)}), while the reverse increment is (N^{-3+o(1)}).  Hence

\[
            \mathcal L_TF=\Theta(N^5)>0.               \tag{2.5}
\]

Here (G=\Theta(N^5\log N)), so the exact fourth-power identity gives

\[
            \mathcal L_TW_0
             =\Theta\!\left(N^{20}(\log N)^3\right)>0. \tag{2.6}
\]

The lower cycle has the leading edge (A+B\to2B).  Its propensity is
(AB=N^4), and its exact (H_B)-increment is (-1).  All other lower
terms have strictly smaller power.  Therefore

\[
       \mathcal L_R(1+H_B)^q
          =-\Theta\!\left(N^{5q-1}\right).             \tag{2.7}
\]

At equality (5q-1=20), the logarithmic factor in (2.6) still wins.
Consequently all-active control by (1.1) requires

\[
                             q>\frac{21}{5}.            \tag{2.8}
\]

### 2.2 The unchanged hard endpoint forces (q\le4)

Now start in the hard two-active scale

\[
                         y_s=(s,0,s^3).                 \tag{2.9}
\]

Fast firings (2A\rightleftarrows B+C) form physical-state excursions.
The first effective lower seed is (A\to A+B) with probability (1-o(1)):
its rate is (s), whereas (0\to A) has rate one.  Once the seed is
present, (B+C\to2A) has rate (s^{3+o(1)}) and wins its next race with
probability (1-o(1)).  Thus the dominant completed service word is

\[
       A\longrightarrow A+B,qquad B+C\longrightarrow2A,              \tag{2.10}
\]

with endpoint

\[
                    (s,0,s^3)\longmapsto(s+2,0,s^3-1). \tag{2.11}
\]

The top reaction is (H_B)-neutral and the seed raises (H_B) by one:

\[
                           \Delta H_B=1.               \tag{2.12}
\]

On the other hand,

\[
  \Delta F=\log\frac{(s+1)(s+2)}{s^3}
          =-\log s+O(1),                              \tag{2.13}
\]

so the repaired fourth-power reward has order

\[
                         \Delta W_0
             =-\Theta\!\left(s^9(\log s)^4\right).    \tag{2.14}
\]

Since (H_B(y_s)=\Theta(s^3)), the positive workload-power endpoint has
order

\[
       (1+H_B(y_s)+1)^q-(1+H_B(y_s))^q
          =\Theta(s^{3q-3}).                           \tag{2.15}
\]

For the unchanged hard episode to absorb (2.15), one needs (q\le4);
at (q=4), the logarithmic factor in (2.14) is favorable.  This is
incompatible with (2.8).

## 3. An exact (H_w) witness

Take

\[
 R=\{0,C\},\qquad T=\{2A,2C,A+C,B+C\}.               \tag{3.1}
\]

Orient the top as

\[
       2A\longrightarrow A+C\longrightarrow2C
       \longrightarrow B+C\longrightarrow2A,          \tag{3.2}
\]

with rates (10,1,1,1) in that order.  Give (0\rightleftarrows C)
unit rates.  Every top edge preserves

\[
                             H=A+B+C.                  \tag{3.3}
\]

### 3.1 All-active control forces (q>5)

At the flat sequence

\[
                         z_N=(N,N,2N),                 \tag{3.4}
\]

the leading factorial increments on the four edges are respectively
(log2,log2,-\log2,-\log2).  Their propensity coefficients are
(10,2,4,2).  Therefore

\[
             \mathcal L_TF(z_N)
                =6(\log2)N^2+o(N^2)>0.                \tag{3.5}
\]

Since (G=\Theta(N\log N)),

\[
             \mathcal L_TW_0(z_N)
                =\Theta\!\left(N^5(\log N)^3\right)>0.\tag{3.6}
\]

The lower death has rate (C=2N), so

\[
                  \mathcal L_R(1+H)^q=-\Theta(N^q).   \tag{3.7}
\]

The logarithmic margin at equality shows that (1.1) requires

\[
                              q>5.                     \tag{3.8}
\]

### 3.2 A retained lower birth forces (q\le14/3)

Start at

\[
                         u_s=(s,s^3,0).                \tag{3.9}
\]

Normally (2A\to A+C), followed by the faster (B+C\to2A), gives the
top-only service endpoint ((s+1,s^3-1,0)), with no change of (H).
However, the physical lower birth is retained.  It wins the first race
against the (2A)-clock with probability

\[
            \frac{1}{1+10s(s-1)}=\Theta(s^{-2}).       \tag{3.10}
\]

Conditional on that event, (B+C\to2A) has rate (s^{3+o(1)}), while
(C\to0) has rate one.  Hence with conditional probability (1-o(1)),

\[
        0\longrightarrow C,qquad B+C\longrightarrow2A               \tag{3.11}
\]

ends at

\[
                    (s+2,s^3-1,0),qquad \Delta H=1.   \tag{3.12}
\]

Both the ordinary and rare-birth service endpoints give a fourth-power
factorial reward of order (-s^9(\log s)^4).  The event-weighted positive
workload cost in (3.12) is instead

\[
              \Theta(s^{-2})\,\Theta((s^3)^{q-1})
                    =\Theta(s^{3q-5}).                 \tag{3.13}
\]

Thus direct compatibility with the unchanged hard endpoint requires

\[
                         3q-5\le9,qquad
                         q\le\frac{14}{3},              \tag{3.14}
\]

which is incompatible with (3.8).

## 4. Consequence for the repair strategy

The two empty intervals are

\[
   q>21/5\quad\hbox{and}\quad q\le4,
   \qquad
   q>5\quad\hbox{and}\quad q\le14/3.                 \tag{4.1}
\]

Increasing the fourth power does not remove the first conflict: both the
all-active top-curvature cost and the hard reward acquire the same extra
power of (G), while the all-active requirement retains a positive power
gap.

The smallest plausible next theorem must therefore carry a workload debt.
Whenever the (W_\ell)-episode uses a seed with positive (H)-increment,
it must retain that mark and append an all-reaction block which repays the
debt before the process is allowed to switch to the all-active workload
potential.  A valid theorem must prove, for every fixed orientation and
rate vector:

1. a strong-Markov repayment stopping time with the seed, service, and all
   competing reactions retained;
2. negative expected marked workload after charging the initial debt;
3. endpoint and physical-duration moments of some order (m>8);
4. a common-(W_\ell) positive endpoint cost below the original
   (G^3\log n) reward; and
5. exact telescoping at returns to the dormant (W_\ell)-tube or entry into
   a generator-good all-active region.

For the four (H_w) pairs, a service-window block which waits for enough
(C\to0) firings is the natural candidate.  For the twelve (H_b) pairs,
the repayment clock belongs to the second linkage and can be dormant on the
boundary; this is the harder marked-transfer problem.  Neither block is
proved here.

## 5. Reproduction

```text
PYTHONPATH=src python3 -B src/hard333_switch_16_scalar_obstruction.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_switch_16_scalar_obstruction.py -v
```

The executable freezes all sixteen pairs, all 170 failed incidences, the
hard-resistance split, the 16 curvature-obstructed incidences, and the two
exact exponent conflicts.  It changes no certified count.
