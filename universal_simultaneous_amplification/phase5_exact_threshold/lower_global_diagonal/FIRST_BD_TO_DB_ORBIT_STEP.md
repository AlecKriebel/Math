# An exact first Bd-to-dB orbit-average obstruction

Date: 2026-08-08 (America/Los_Angeles)

## Status

**PROVED.**  At fitness two, the first dB survival-map iterate started from
the Bd extinction vector cannot increase its uniform-start average.  The
result holds for every finite adjoint kernel, with no reversibility,
symmetric-weight, regularity, or bounded-temperature assumption.

This is a genuine global obstruction, but it is only a **one-step theorem**.
The dB orbit is not pointwise monotone and its averages are not known to be
temporally monotone.  Consequently the result below does not yet prove the
sharp conjecture `beta+sigma <= 1` for the limiting dB survival vector.

## 1. The theorem

Let `p_i>0`, `sum_i p_i=1`, let `P` be any row-stochastic matrix, and put

\[
 R=D_p^{-1}P^TD_p,\qquad t=R\mathbf 1.
\]

Suppose `b in [0,1]^n` satisfies the endpoint Bd survival equations

\[
                       t_i b_i=2(1-b_i)(Pb)_i.       \tag{1}
\]

Write `q=1-b`, and define the endpoint dB survival map

\[
             \mathcal F(y)_i={2(Ry)_i\over1+2(Ry)_i}.             \tag{2}
\]

Then

\[
                         \boxed{\ E_p\mathcal F(q)\leq E_pq\ }.  \tag{3}
\]

Thus the first point of the orbit
`q,F(q),F^2(q),...` lies in the correct average half-space.

## 2. Flow reduction

Set

\[
 \mu_{ij}=p_iP_{ij},\qquad
 \phi(z)={z(2z-1)\over1+2z}.
\]

Adjointness and `P 1=1` give `E_p Rq=E_pq`.  Hence

\[
 E_pq-E_p\mathcal F(q)
 =E_p\left[Rq-{2Rq\over1+2Rq}\right]
 =E_p\phi(Rq).                                      \tag{4}
\]

The function is convex on the whole nonnegative axis because

\[
                         \phi''(z)={8\over(1+2z)^3}>0.             \tag{5}
\]

Tangent-line bounds at the labelled values `q_i`, followed by adjointness,
therefore give

\[
 E_p\phi(Rq)\geq
 \sum_{ij}\mu_{ij}C(q_i,q_j),                       \tag{6}
\]

where

\[
 C(x,y)=\phi(x)-x\phi'(x)+x\phi'(y).                \tag{7}
\]

Equation (1), written in the edge flow, is

\[
 (1-q_i)\sum_j\mu_{ji}
       =2q_i\sum_j\mu_{ij}(1-q_j).                  \tag{8}
\]

Thus the sum over edges of

\[
 (1-y)\{\lambda(y)-2x\lambda(x)\}                  \tag{9}
\]

vanishes when `x=q_i,y=q_j`, for every scalar function `lambda`.

## 3. Exact edge certificate

Choose

\[
 \lambda(x)=-{(2x-3)(12x^2-12x+11)\over16(2x+1)}.  \tag{10}
\]

Direct rational simplification gives

\[
 C(x,y)+(1-y)\{\lambda(y)-2x\lambda(x)\}
 ={N(x,y)\over16(1+2x)^2(1+2y)^2},                 \tag{11}
\]

where

\[
\begin{aligned}
N={}&-384x^5y^3+288x^5y+96x^5
 +768x^4y^3-576x^4y-192x^4\\
&-448x^3y^3+256x^3y^2+592x^3y+48x^3\\
&+192x^2y^5-576x^2y^4+672x^2y^3-256x^2y^2
  -148x^2y-12x^2\\
&+192xy^5-576xy^4+872xy^3-192xy^2-234xy+50x\\
&+48y^5-144y^4+152y^3-64y^2-25y+33.
\end{aligned}                                                    \tag{12}
\]

The key algebraic fact is

\[
                              N(x,y)\geq0
                 \quad(0\leq x,y\leq1).             \tag{13}
\]

Here is a compact exact certificate for (13).  On the central rational box

\[
                         [7/16,9/16]^2,              \tag{14}
\]

all tensor Bernstein coefficients of `N_xx`, `N_yy`, and
`N_xx N_yy-N_xy^2` are strictly positive.  Their respective exact minima
are

\[
 {3502069\over32768},\qquad
 {30540247\over65536},\qquad
 {412937481237167\over17179869184}.                 \tag{15}
\]

The Hessian is therefore positive definite throughout (14).  Since

\[
 N(1/2,1/2)=N_x(1/2,1/2)=N_y(1/2,1/2)=0,            \tag{16}
\]

the polynomial is nonnegative on that box.

The complement is the other eight cells of the grid with endpoints
`0,7/16,9/16,1`.  After at most two midpoint subdivisions, all tensor
Bernstein coefficients of `N` are nonnegative.  There are 26 leaf boxes.
The replay constructs the subdivision rather than trusting rounded stored
coefficients; the SHA-256 hash of its complete rational leaf certificate is

```text
df5aaf698f23680e53614cbc9bc1e8b65571178455506d7ae1ad41ffcc40e0eb
```

Bernstein nonnegativity bounds a polynomial below by its least coefficient,
so these finite checks prove (13) over the full square.

Summing (11) against the nonnegative edge flow and using (9) in (6) proves
`E_p phi(Rq)>=0`.  Equation (4) then proves (3).

## 4. What remains for the sharp boundary

Let `s` be the positive fixed point of (2), let `h=1-s`, and write
`beta=E_p b`, `sigma=E_p s`.  A sufficient inequality for the desired
endpoint boundary is

\[
 W:=E_p[b(1-b)]-E_p\left[{b^2s\over1-s}\right]\geq0.              \tag{17}
\]

It has the exact stability form

\[
 \begin{aligned}
 W
 &=E_p\left[{b(q-s)\over h}\right]\\
 &=E_p(q-s)-E_p\left[{(q-s)^2\over1-s}\right].       \tag{18}
 \end{aligned}
\]

Thus (17) is strictly stronger than `beta+sigma<=1`: it would prove the
target gap together with a quantitative square deficit.  Broad numerical
tests support (17), but neither (17) nor the passage from the one-step
theorem to the limiting fixed point is claimed here.

## 5. Replay

From the repository root run

```bash
.venv/bin/python \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_diagonal/verify_first_orbit_step.py
```

The script uses exact integer/rational symbolic arithmetic and reconstructs
all Bernstein coefficients and all 26 leaf boxes deterministically.

