# The minimal portal product for every weighted triangle at `R_hyb`

Date: 2026-08-13 (America/Los_Angeles)

No graph search, external communication, or floating-point sign test is used
in this theorem.  The finite sign discharge consists of exact rational
tensor-Bernstein coefficients.

## 1. Theorem

Let `H` be a positive weighted triangle.  Put

\[
 p_0=1-{1\over R},\qquad
 b=\rho_{Bd}(H,R),\qquad d=\rho_{dB}(H,R),
 \qquad R=R_{hyb}.
\]

Let `u_i` and `v_i` be the Bd and dB singleton atoms of the two exact
stationary OR duals at fitness `R`, and let `e_i=1/d_i`, where `d_i` is the
internal weighted degree.  For every nonzero portal load vector `x>=0`, set

\[
 q_B={x\cdot u\over x\cdot\mathbf1},\qquad
 q_D={x\cdot(ev)\over x\cdot e}.                       \tag{1}
\]

Then

\[
 \boxed{
 q_Bq_D\ge R^3[b-p_0]_+[d-p_0]_+.}                    \tag{2}
\]

The inequality is strict for every positive triangle and every nonzero
nonnegative portal vector.

Equation (2), not the stronger Hellinger/BDM inequality, is the exact local
condition needed by the corrected gate-disjunction reduction.  Thus every
positive weighted three-vertex module satisfies the minimal separated-module
disjunction at `R_hyb`.  Together with the separate weighted-path theorem,
this covers every connected weighted support of order three.

## 2. Chamber and exact chain data

Every permutation of the three triangle edges is induced by a vertex
permutation.  After sorting and scaling, write

\[
 (A,B,C)=(pq,q,1),\qquad0<p,q\le1.                    \tag{3}
\]

The individual singleton atoms are kept in a compact exact Schur form rather
than expanded.  Write `S_i` for forward singleton fixation at fitness `f`
and `D_ij` for doubleton fixation.  For `{i,j,k}={0,1,2}`, Bd satisfies

\[
 D_{ij}={fT_k+(w_{ki}/d_k)S_j+(w_{kj}/d_k)S_i\over fT_k+1},
 \qquad
 T_k={w_{ik}\over d_i}+{w_{jk}\over d_j},              \tag{4}
\]

\[
 S_i={f\sum_{j\ne i}(w_{ij}/d_i)D_{ij}\over
           f+\sum_{j\ne i}w_{ji}/d_j}.                 \tag{5}
\]

For dB put

\[
 h_{ki}={w_{ki}\over w_{ki}+f w_{ji}},\qquad
 h_{kj}={w_{kj}\over w_{kj}+f w_{ij}}.
\]

Then

\[
 D_{ij}={1+h_{ki}S_j+h_{kj}S_i\over1+h_{ki}+h_{kj}},   \tag{6}
\]

and, for `j\ne i`, with `k` the third vertex,

\[
 h_{ij}={f w_{ij}\over f w_{ij}+w_{kj}},\qquad
 S_i={\sum_{j\ne i}h_{ij}D_{ij}\over1+\sum_{j\ne i}h_{ij}}. \tag{7}
\]

Solving the three linear equations at `f=R` gives `b` and `d`.  Type
complementation gives the reciprocal atoms without a second symbolic solve:

\[
 u_i=1-D_{V\setminus\{i\}}^{Bd}(R),\qquad
 v_i=1-D_{V\setminus\{i\}}^{dB}(R).                   \tag{8}
\]

After (3), every rational denominator appearing in (4)--(8), `b`, and `d`
has strictly positive coefficients in `(R,p,q)`.  This fixes the sign
orientation before numerator reduction.

## 3. Entrywise portal reduction

Put

\[
                         T=r^3(b-p_0)(d-p_0).           \tag{9}
\]

When both excesses are positive, the desired target in (2) is `T`.  The
denominator-cleared portal gap is the quadratic form with entries

\[
 M_{ij}={u_i e_jv_j+u_j e_iv_i-T(e_i+e_j)\over2}.      \tag{10}
\]

It is enough to prove the stronger entrywise inequalities

\[
 {u_i e_jv_j+u_j e_iv_i\over e_i+e_j}>T
                   \qquad(0\le i\le j\le2).            \tag{11}
\]

Indeed, (11) makes every coefficient of `x^TMx` positive.  If either excess
in (2) is nonpositive, its positive-part target is zero and (2) follows
immediately from positivity of `q_B,q_D`.

## 4. Exact two-regime certificate

Let

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1.               \tag{12}
\]

The proof uses the exact isolating interval

\[
 I=\left[{150285691279056962670\over10^{20}},
          {150285691279056962671\over10^{20}}\right]. \tag{13}
\]

Sturm counting gives exactly one root of `P` in `I`; its endpoint signs are
opposite.  This root is `R_hyb`.

All numerator polynomials below are first reduced modulo (12) in `r`.  This
keeps degree at most five and preserves their values at `R_hyb` exactly.

### Singular regime

On

\[
                   (r,p,q)\in I\times[0,1]\times[0,1/2000],
\]

the reduced numerator of

\[
                         -\{d-p_0\}                    \tag{14}
\]

has multidegree `(5,4,4)`.  All of its 150 tensor-Bernstein coefficients
are strictly positive.  Hence `d<p_0`, so the right side of (2) is zero.

### Remaining chamber

On

\[
                  (r,p,q)\in I\times[0,1]\times[1/2000,1],
\]

clear the positive denominator in each of the six gaps (11), then reduce its
numerator modulo (12).  The exact certificate sizes are

\[
\begin{array}{c|c|c}
(i,j)&\text{multidegree in }(r,p,q)&
      \text{positive Bernstein coefficients}\\ \hline
(0,0),(1,1),(2,2)&(5,24,24)&3750\text{ each}\\
(0,1)&(5,39,39)&9600\\
(0,2),(1,2)&(5,38,39)&9360\text{ each}.
\end{array}                                             \tag{15}
\]

Every one of the 39,570 coefficients in (15) is strictly positive.  Thus
(11) holds throughout the remaining chamber.  Equations (14)--(15) prove
(2).

This is a fixed finite algebraic certificate on two scalar regimes, not a
search over weighted graphs.  The split at `1/2000` isolates the only
singular edge degeneration; the theorem on that side is the stronger fact
that the required target vanishes.

## 5. Relation to the stronger BDM target

The earlier Hellinger BDM target is

\[
 r(r-1)^2
 [\sqrt{ab'}-\sqrt{(1-a)(1-b')}]_+^2,
 \quad a={d\over r-1},\quad b'=b.                      \tag{16}
\]

It is strictly stronger than (2) and is not needed for the gate disjunction.
At the equal triangle, the old product target in (2) is
`0.03116645192037...`, whereas (16) is `0.03132009800338...`.  This explains
why the previous BDM route appeared to miss a small amount of slack.  The
minimal product theorem closes the actual triangle obligation; arbitrary
triangle BDM remains an optional second-stage question.

## 6. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_triangle_bdm_reduction.py

PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_triangle_portal_product.py
```

The first replay independently solves a nonregular labelled six-state chain
and audits (4)--(8) plus the complete-triangle anchor.  The second derives
the general chamber Schur systems, checks every denominator sign, isolates
the algebraic root, and verifies all 39,720 exact Bernstein coefficients in
(14)--(15).
