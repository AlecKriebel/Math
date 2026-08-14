# Endpoint support as a signed adjoint autocorrelation

Date: 2026-08-13 (America/Los_Angeles)

No graph search, parameter search, numerical optimization, literature search,
or external communication was used.

## 1. Status

**PROVED EXACT REDUCTION AND SHARP ROUTE OBSTRUCTION.**  For every finite
reversible diffuse-adjoint endpoint datum and every `r>1`, the support

\[
                         T_r=(r-1)E_pq-E_ps
\]

has the particularly short representation

\[
 \boxed{
 T_r=r\left\{E_p(xPx)+{1\over r-1}E_p\!\left({u^2\over h}\right)\right\}.}
 \tag{1}
\]

Here

\[
 x={1\over r}-q=b-{r-1\over r},\qquad
 u={1\over r}-h=s-{r-1\over r}.                         \tag{2}
\]

Thus the endpoint support is exactly a positive dB Pearson term plus a
possibly negative one-step Bd autocorrelation.  The desired sign is

\[
 E_p\!\left({u^2\over h}\right)
       \geq -(r-1)E_p(xPx).                              \tag{3}
\]

Formula (1) is a useful compression of the stored ground-energy square, but
it is not by itself a new sign mechanism.  The autocorrelation is taken in
`L^2(p)`, whereas `P` is self-adjoint in `L^2(pi)`.  Its correct self-adjoint
representative under `p` is `(P+R)/2`, whose bottom can lie below `-1` after
temperature weighting.  The canonical edgewise spectral lower bound loses
too much even on the existing exact positive symmetric three-type family.

Moreover, that same family makes the coefficient `r-1` in (3) sharp: its
ratio of the positive term to the negative autocorrelation tends to
`(r-1)/(1-theta)` and hence to `r-1` as `theta` decreases to zero.  Any
successful proof must therefore retain the exact joint endpoint alignment;
it cannot replace (3) by a uniformly stronger norm inequality.

This note does **not** prove or refute `T_r>=0`.

## 2. Setup

Let `P` be finite, row stochastic, and self-adjoint in `L^2(pi)`.  Let
`a>0`, normalized by `E_pi a=1`, and put

\[
 p=\pi a,\qquad R=D_a^{-1}PD_a,\qquad t={Pa\over a}.       \tag{4}
\]

The positive endpoint survival vectors satisfy

\[
 tb=r(1-b)Pb,\qquad s=r(1-s)Rs.                          \tag{5}
\]

Write

\[
 c=r-1,\qquad p_0={c\over r},\qquad
 q=1-b,\quad h=1-s,\quad x=b-p_0,\quad u=s-p_0.          \tag{6}
\]

Adjointness gives

\[
 E_p(Pf)=E_p(tf),\qquad E_p(fRg)=E_p(gPf).               \tag{7}
\]

## 3. The two scalar balances

The Bd equation in centered variables is

\[
 t(p_0+x)=(1-rx)(p_0+Px).                                \tag{8}
\]

Average (8), use `E_p(tb)=E_p(Pb)`, and expand its right side.  The common
`E_pb` term cancels and leaves

\[
                  \boxed{\ cE_px+rE_p(xPx)=0.\ }          \tag{9}
\]

For dB, divide (5) by `h` and average:

\[
                         E_p\left({s\over h}\right)=rE_ps.
\]

Equivalently, `E_p(su/h)=0`.  The pointwise identity

\[
                         {su\over h}=cu+{r u^2\over h}
\]

therefore gives

\[
             \boxed{\ cE_pu+rE_p\!\left({u^2\over h}\right)=0.\ }
                                                                    \tag{10}
\]

Finally,

\[
 T_r=cE_p(1/r-x)-E_p(p_0+u)=-cE_px-E_pu.
\]

Substitution of (9)--(10) proves (1).

## 4. Exact relation to the stored ground-energy square

Put

\[
 A=Px-{x\over h},\qquad
 V=E_p\!\left({t x^2\over q}\right),\qquad
 U=E_p\!\left({u^2\over h}\right),\qquad
 J=E_p(xPx).                                             \tag{11}
\]

The stored endpoint balances give

\[
 E_p(tx)=-{r\over c}V,qquad
 E_p[(1-t)x]={r\over c}E_p(uA).                          \tag{12}
\]

Together with (9), these imply the exact cancellation

\[
                         \boxed{\ E_p(uA)=V-J.\ }          \tag{13}
\]

Substituting (13) into the earlier formula

\[
 T_r=rV+{r\over c}U-rE_p(uA)
\]

recovers (1).  Hence the autocorrelation formula is algebraically
equivalent to the full coupled-square identity.  It removes the auxiliary
labels `V,A`, but does not manufacture a new positive term.

## 5. The canonical self-adjoint block bound is insufficient

The `p`-adjoint of `P` is `R`.  Therefore

\[
 J=\left\langle x,{P+R\over2}x\right\rangle_p.             \tag{14}
\]

The symmetric edge weights of `S=(P+R)/2` are

\[
 p_iS_{ij}={\pi_iP_{ij}(a_i+a_j)\over2}.
\]

Since `S1=(1+t)/2`, the edgewise inequality
`2x_ix_j>=-x_i^2-x_j^2` gives the universal bound

\[
 J\geq-N,\qquad
 N={1\over2}E_p\{(1+t)x^2\}.                             \tag{15}
\]

The corresponding spectral closure of (1) would be

\[
                               U\geq cN.                  \tag{16}
\]

It is false on the exact singular family already proved in
`rhyb_diffuse_ground_energy_obstruction`.  Use its notation

\[
 A_0=1-\gamma,\qquad
 \mathcal T=1+{A_0\theta\over\gamma}.
\]

The limiting endpoint data give

\[
 U\longrightarrow {A_0c^2\over r^2},\qquad
 J\longrightarrow-{A_0c(1-\theta)\over r^2},            \tag{17}
\]

and direct substitution of the stored limiting `p,t,x` labels gives

\[
 N\longrightarrow {A_0\over2r^2}
 \left\{1+(1-\theta)c^2
       +{A_0\theta^2\over\gamma}(1+\mathcal T)\right\}. \tag{18}
\]

For the exact specialization

\[
                  \gamma={1\over14},\qquad\theta={1\over50},
\]

the sign of `U-cN` is the sign of

\[
 2c-1-{49\over50}c^2-{1469\over125000}.                 \tag{19}
\]

This is strictly negative for

\[
                         {1\over2}\leq c\leq{51\over100},
\]

because `2c-1<=1/50` while `49c^2/50>=49/200`.  Thus
(16) fails throughout the rational strip containing `R_hyb`, even though
the true support on the same family is

\[
                         T_r\longrightarrow{A_0\theta c\over r}>0. \tag{20}
\]

The failure is informative: replacing the signed autocorrelation by the
bottom edgewise spectral bound destroys precisely the alignment that keeps
(20) positive.

## 6. Sharpness of the target coefficient

Equations (17) give

\[
                         {U\over-J}\longrightarrow{c\over1-\theta}. \tag{21}
\]

For fixed `r`, sending `theta` down to zero makes this ratio tend to `c`.
At the same time

\[
 U+cJ\longrightarrow {A_0c^2\theta\over r^2}>0
\]

for every positive `theta`, with equality approached only on the singular
boundary.  Therefore no estimate

\[
                         U\geq(c+\delta)(-J),\qquad\delta>0,
\]

can hold uniformly on the diffuse-adjoint class.  A proof of (3), if true,
must be coefficient-sharp and must use more than separate control of `U`
and the spectrum of `(P+R)/2`.

## 7. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_support_autocorrelation/verify_support_autocorrelation.py
```

The replay checks the centered scalar algebra, the deterministic two-cycle
identity, the singular-family limits (17)--(21), and the strict failure of
the canonical spectral sufficient condition on the full rational strip.
