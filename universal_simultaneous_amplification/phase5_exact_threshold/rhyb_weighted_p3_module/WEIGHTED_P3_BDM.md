# The `R_hyb` dual-moment inequality for every weighted three-path

Date: 2026-08-13 (America/Los_Angeles)

No graph search, numerical optimization, or external input is used here.
The only finite sign discharge is an exact tensor-Bernstein certificate on
two scalar parameter regimes.

## 1. Theorem

Let `H` be any positively weighted three-vertex path and let its three portal
loads be arbitrary nonnegative numbers, not all zero.  At

\[
 R=R_{hyb}=1.5028569127905696267\ldots,
\]

the exact separated-module response satisfies

\[
                         D+(R-1)B<0                         \tag{1}
\]

at every positive gate scale.  Equivalently, every weighted `P_3` satisfies
the bounded dual-moment inequality (BDM), strictly and uniformly over its
portal vector.

This extends the unweighted `P_3` theorem to its full one-parameter weighted
family.  The key structural fact is stronger than portal copositivity: after
reflecting the path if necessary, the entire portal product is bounded below
by the product at the leaf incident to the heavier edge.

## 2. Normalization and exact labelled-chain data

Scale the two edge weights to `1,t`.  Reflection sends `t` to `1/t`, so it is
enough to treat

\[
                              0<t\leq1.                   \tag{2}
\]

Label the vertices `(L,C,R)`, with edge `LC` of weight `1` and edge `CR` of
weight `t`.  Thus

\[
 d=(1,1+t,t),\qquad e=(1,1/(1+t),1/t).                  \tag{3}
\]

Put

\[
 \begin{aligned}
 A&=r^2(t+1)+rt+t(t+1),\\
 B&=r^2t(t+1)+rt+t+1,\\
 N_C&=2r^3t+r^2t^2+3r^2t+r^2+rt^2+2rt+r+t^2+2t+1.
 \end{aligned}                                          \tag{4}
\]

Solving the two labelled six-state absorbing chains, and then applying type
complementation at reciprocal fitness, gives the singleton atoms

\[
 \begin{aligned}
 u=(q_{Bd,L},q_{Bd,C},q_{Bd,R})
   &=\left({t(t+1)\over A},
       {tN_C\over(2r+1)AB},{t+1\over B}\right),\\
 v=(q_{dB,L},q_{dB,C},q_{dB,R})
   &=\left({1\over2(rt+1)},
       {2r^2t+3rt^2+3r+4t\over6(r+t)(rt+1)},
       {t\over2(r+t)}\right).                           \tag{5}
 \end{aligned}
\]

The normalized mean ranks are

\[
 a={5r^2t+3rt^2+3r+t\over
             9(r-1)(r+t)(rt+1)},                       \tag{6}
\]

and

\[
 b={r^2N_B\over3(r+2)AB},                               \tag{7}
\]

where

\[
 \begin{aligned}
 N_B={}&3r^3t^3+6r^3t^2+3r^3t
       +6r^2t^3+12r^2t^2+6r^2t\\
     &+rt^4+5rt^3+9rt^2+5rt+r
       +2t^4+4t^3+6t^2+4t+2.
 \end{aligned}                                          \tag{8}
\]

Here `b=rho_Bd(H,r)` and `a=rho_dB(H,r)/(r-1)`, exactly as in the parent BDM
reduction.

Every displayed quantity respects reflection:

\[
 a(t)=a(1/t),\quad b(t)=b(1/t),\quad
 u_L(t)=u_R(1/t),\quad v_L(t)=v_R(1/t),                 \tag{9}
\]

with the centre coordinates fixed.  Moreover
`e(1/t)=t(e_R(t),e_C(t),e_L(t))`; the common factor cancels from the dB
portal law.  Thus (2) loses no portal configurations.

## 3. A portal-extremal leaf theorem

For a portal vector `x>=0`, define

\[
 q(x)={ (x\mathbin\cdot u)(x\mathbin\cdot(ev))
             \over (x\mathbin\cdot\mathbf1)(x\mathbin\cdot e)}.
                                                               \tag{10}
\]

The left leaf product is

\[
 k_0=u_Lv_L={t(t+1)\over2(rt+1)A}.                     \tag{11}
\]

We prove the all-portal inequality

\[
                             \boxed{q(x)\geq k_0.}       \tag{12}
\]

Indeed, let

\[
 \Delta_{ij}=u_i e_jv_j+u_j e_iv_i-k_0(e_i+e_j).       \tag{13}
\]

Then the numerator of `q(x)-k_0` is the quadratic form with
off-diagonal data `Delta_ij`.  Direct substitution of (3)--(5) gives
`Delta_LL=0`.  After clearing positive denominators, the other five entries
have the signs of

\[
 \begin{array}{c|c}
 LC&t(r-1)F_{LC}\\
 LR&r(r-1)(t-1)(t+1)
       \{r(t+1)^2(t-1)-2t-1\}\\
 CC&t(r-1)F_{CC}\\
 CR&(r-1)F_{CR}\\
 RR&-r(r-1)(t-1)(t+1)(t^2+t+1).
 \end{array}                                             \tag{14}
\]

The three remaining polynomials have the following degree-four Bernstein
coefficients on `0<=t<=1`:

\[
 \begin{aligned}
 \mathcal B(F_{LC})={}&\left(
 3r^2,{(4r-1)(4r+1)\over4},
 {4r^4-2r^3+27r^2+2r-4\over6},\right.\\
 &\left.{12r^4+2r^3+20r^2+7r-5\over4},
 (r+1)(4r-1)(2r^2+r+2)\right),                         \tag{15}
 \end{aligned}
\]

\[
 \begin{aligned}
 \mathcal B(F_{CC})={}&\left(
 3r^2,{2r^3+16r^2+r-1\over4},
 {4r^4+4r^3+28r^2+5r-5\over6},\right.\\
 &\left.{(2r-1)(4r^3+4r^2+11r+8)\over4},
 2(r-1)(r+1)(2r^2+r+2)\right),                         \tag{16}
 \end{aligned}
\]

and

\[
 \begin{aligned}
 \mathcal B(F_{CR})={}&\left(
 3r(r+1)(2r+1),
 {r(2r+3)(2r^2+12r+7)\over4},\right.\\
 &{16r^4+52r^3+93r^2+47r-1\over6},
 {20r^4+38r^3+70r^2+40r-3\over4},\\
 &\left.(r+1)(4r-1)(2r^2+r+2)\right).                 \tag{17}
 \end{aligned}
\]

Each entry in (15)--(17) has nonnegative power coefficients after
`r=3/2+y`, and a positive constant coefficient.  Hence the three `F`'s are
strictly positive for `r>=3/2`.  In the `LR` row of (14), both
`t-1` and `r(t+1)^2(t-1)-2t-1` are nonpositive; the second is strictly
negative.  The `RR` row is also nonnegative.  Thus every `Delta_ij>=0`,
which proves (12).

For `0<t<1`, equality in (12) occurs only when the portal is concentrated at
`L`.  At `t=1`, equality holds for every portal supported on the two leaves.

## 4. The scalar endpoint inequality

Let

\[
 C=r(r-1)^2,\qquad s=a+b-1,qquad K_0={C\over k_0}.     \tag{18}
\]

First, `0<a,b<1` throughout `r>=3/2`, `0<t<=1`.  For example, after clearing
positive denominators, the degree-two Bernstein coefficients of `1-a` are

\[
 3r(3r-4),\quad{(r+1)(9r^2-5r-10)\over2},\quad
 (r+1)(9r^2-5r-10),                                    \tag{19}
\]

and the degree-four Bernstein coefficients of `1-b` are

\[
 \begin{aligned}
 &2r^2(r+2),
 {3(r^4+5r^3+9r^2+3r+2)\over4},\\
 &{5(r^4+3r^3+5r^2+3r+2)\over2},
 3(r^2+2r+2)(2r^2+r+2),\\
 &6(r^2+2r+2)(2r^2+r+2).
 \end{aligned}                                          \tag{20}
\]

Let

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1                \tag{21}
\]

and use the rational isolating interval

\[
 I=[1502856912/10^9,1502856913/10^9].                  \tag{22}
\]

The polynomial (21) has exactly one root in `I`, namely `R_hyb`.  Two exact
tensor-Bernstein certificates finish the scalar inequality.

### Small edge ratio

On

\[
                   (r,t)\in I\times(0,1/250],
\]

all 70 tensor-Bernstein coefficients of the numerator of

\[
                              1-K_0s                    \tag{23}
\]

are strictly positive after the affine map to the unit square.  Its
denominator is

\[
 9t(r+2)(r+t)(t+1)B>0.                                 \tag{24}
\]

Consequently `K_0s<1`.

### Remaining edge ratios

On `I` times each of

\[
 \begin{gathered}
 [1/250,1/100],\ [1/100,1/20],\ [1/20,1/10],\
 [1/10,1/4],\ [1/4,1/2],\ [1/2,3/4],\ [3/4,1],
 \end{gathered}                                         \tag{25}
\]

all 221 tensor-Bernstein coefficients of the numerator of

\[
              4k_0(1-a)(1-b)-Cs^2                     \tag{26}
\]

are strictly positive.  Its denominator is

\[
 81(r-1)(r+2)^2(r+t)^2(rt+1)^2A^2B^2>0.                \tag{27}
\]

These are fixed exact polynomial certificates, not sampled signs or a sweep
over weighted graphs.  The replay constructs every coefficient over the
rationals and checks it individually.

## 5. Hellinger conclusion

Write

\[
 U=\sqrt{ab},\qquad V=\sqrt{(1-a)(1-b)}.
\]

If `s<=0`, the positive-part target in BDM vanishes.  If `s>0`, then
`s=(U-V)(U+V)` and

\[
 (U-V)^2<s,
 \qquad
 (U-V)^2\le {s^2\over4V^2}.                            \tag{28}
\]

In the small regime, (23) says `k_0>Cs`, and hence

\[
 k_0>C(U-V)^2.
\]

In the remaining regime, (26) and the second inequality in (28) give the
same strict conclusion.  Combining this with (12) yields

\[
 q_Bq_D=q(x)>
 C\left[\sqrt{ab}-\sqrt{(1-a)(1-b)}\right]_+^2.         \tag{29}
\]

Together with `a<1`, (29) is strict BDM.  The exact quadratic/Hellinger
equivalence in the parent reduction now gives (1) for every positive gate
scale.

## 6. Scope

This proves BDM for every weighted graph of order three whose support is a
path.  Together with the complete-module theorem it covers the path boundary
and the equal-weight interior point of the three-vertex parameter space.
Arbitrary positive weighted triangles remain open: the existing triangle
exchange-square theorem proves dB suppression, but not the portal-uniform
BDM product.  This result also does not prove BDM for order four or for
arbitrary bounded modules.

The portal reduction (12) is the reusable part: it converts a continuum of
degree-reweighted portal laws into one extremal singleton product before any
endpoint algebra is needed.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_weighted_p3_bdm.py
```

The replay rebuilds all four labelled chains (both rules at `r` and `1/r`),
checks type complementation and reflection, reconstructs every portal-matrix
entry, verifies the explicit Bernstein lists (15)--(17), and checks every
tensor-Bernstein coefficient in (23) and (26).
