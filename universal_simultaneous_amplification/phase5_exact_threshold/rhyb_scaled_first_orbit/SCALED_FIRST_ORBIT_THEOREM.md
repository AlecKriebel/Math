# A scaled first Bd-to-dB orbit theorem at `R_hyb`

Date: 2026-08-13 (America/Los_Angeles)

## Status

**PROVED.**  The scalar-flow inequality needed by the diffuse-support route
holds not only at `R_hyb`, but uniformly for every

\[
                         \frac32\le r\le\frac{151}{100}.
\]

The proof uses a convex tangent and a single explicit linear flow multiplier.
It does not enumerate kernels, graphs, or endpoint solutions.  Reversibility
is unnecessary.

## 1. The theorem

Let `p_i>0`, `sum_i p_i=1`, let `P` be row-stochastic, and define

\[
 R=D_p^{-1}P^TD_p,
 \qquad \mu_{ij}=p_iP_{ij}.
\]

Fix `3/2 <= r <= 151/100`, put `c=r-1`, and suppose `q in [0,1]^n`
satisfies the Bd endpoint flow equations

\[
 (1-q_i)\sum_j\mu_{ji}
       =r q_i\sum_j\mu_{ij}(1-q_j).                 \tag{1}
\]

Then

\[
 \boxed{\quad
 E_p\!\left[
   \frac{c^2(Rq)\{r(Rq)-1\}}{1+rc(Rq)}
 \right]\ge0 .\quad}                               \tag{2}
\]

Equivalently, if

\[
 \mathcal F_r(y)={rRy\over1+rRy},
\]

then

\[
                       E_p\mathcal F_r(cq)\le cE_pq. \tag{3}
\]

In particular, (2)--(3) hold at the algebraic number `r=R_hyb`, the unique
root in `(3/2,151/100)` of

\[
 r^6-8r^5+22r^4-30r^3+21r^2-6r+1.
\]

## 2. Convex flow reduction

Define

\[
 \phi_r(z)={c^2z(rz-1)\over1+rcz}.
\]

This function is convex on the whole nonnegative axis, since

\[
                    \phi_r''(z)={2r^2c^2\over(1+rcz)^3}>0.       \tag{4}
\]

Adjointness and `P 1=1` give `E_pRq=E_pq`.  Therefore

\[
 cE_pq-E_p\mathcal F_r(cq)=E_p\phi_r(Rq).            \tag{5}
\]

Apply the tangent bound for `phi_r` at the labelled value `q_i`.  After
summing and using adjointness,

\[
 E_p\phi_r(Rq)\ge\sum_{ij}\mu_{ij}C_r(q_i,q_j),      \tag{6}
\]

where

\[
 C_r(x,y)=\phi_r(x)-x\phi_r'(x)+x\phi_r'(y).         \tag{7}
\]

Multiplying (1) by an arbitrary scalar function `lambda(q_i)` and summing
shows that

\[
 \sum_{ij}\mu_{ij}(1-q_j)
       \{\lambda(q_j)-rq_i\lambda(q_i)\}=0.          \tag{8}
\]

Thus it is enough to find a `lambda` for which the corresponding two-label
edge slack is nonnegative on the unit square.

## 3. The linear multiplier certificate

Choose

\[
 \boxed{\quad
 \lambda_r(x)={c\over r}-{2c\over r}\left(x-{1\over r}\right)
              ={c(r+2-2rx)\over r^2}.\quad}          \tag{9}
\]

Set

\[
 S_r(x,y)=C_r(x,y)
 +(1-y)\{\lambda_r(y)-rx\lambda_r(x)\}.             \tag{10}
\]

The exact algebraic claim is

\[
 S_r(x,y)\ge0
 \quad\left(\frac32\le r\le\frac{151}{100},\qquad
             0\le x,y\le1\right).                  \tag{11}
\]

For a compact certificate, clear the positive denominator

\[
 D=r^2(1+rcx)^2(1+rcy)^2
\]

and write `N=DS_r`.  The replay reconstructs `N` symbolically rather than
storing its 130-term expansion.

Partition each label interval at

\[
                 0,\quad {16\over25},\quad {69\over100},\quad1. \tag{12}
\]

On each of the eight noncentral label cells, every three-variable tensor
Bernstein coefficient of `N`, including the fitness coordinate on
`[3/2,151/100]`, is nonnegative.

For the central square `[16/25,69/100]^2`, the equality point
`(1/r,1/r)` lies in its interior for the full fitness interval.  Direct
symbolic calculation gives

\[
 N(r,1/r,1/r)=N_x(r,1/r,1/r)=N_y(r,1/r,1/r)=0.       \tag{13}
\]

Every tensor Bernstein coefficient on the central three-dimensional box is
strictly positive for each of

\[
                         N_{xx},\qquad N_{yy},\qquad
                         N_{xx}N_{yy}-N_{xy}^2.       \tag{14}
\]

Their exact least coefficients are respectively

\[
 {4250351362833\over640000000000},\qquad
 {3141746343\over312500000},\qquad
 {1666401798181235013\over24414062500000000}.        \tag{15}
\]

Hence the Hessian in `(x,y)` is positive definite throughout the central
square for every allowed `r`.  Equation (13) proves `N>=0` there, while the
outer Bernstein coefficients prove it on the complement.  This establishes
(11).

Finally, sum (10) against the nonnegative flow `mu`, use the null identity
(8), and insert the result into (6).  This proves (2), and (5) gives (3).

## 4. Scope

This closes exactly the scaled first-orbit scalar-flow lemma requested by the
diffuse-support reduction.  In the surrounding notation, it proves only the
**upper half of the `T` sandwich**, not nonnegativity of `T` itself.  It is
still a one-step inequality: by itself it does not identify the limiting dB
fixed point or prove the full diffuse-support inequality.

## 5. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_scaled_first_orbit/verify_scaled_first_orbit.py
```

The replay uses only exact integer/rational symbolic arithmetic.
