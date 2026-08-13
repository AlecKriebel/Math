# Exact ground-energy decomposition of the factor-one gap

Date: 2026-08-13 (America/Los_Angeles)

## Status

**PROVED EXACT IDENTITY.**  For every finite undirected-realizable diffuse
adjoint kernel at fitness two, the unresolved factor-one gap is

\[
 \boxed{
  1-\beta-\sigma
  ={K\over2}+{1\over2}E_p\!\left[
     h\left(Px-{x+2u\over h}\right)^2\right] .}              \tag{1}
\]

Here

\[
 x=b-{1\over2}={1\over2}-q,\qquad
 u=s-{1\over2}={1\over2}-h,                                 \tag{2}
\]

and the special ground energy is

\[
 K=4E_p\left[{t x^2\over q}\right]
       -E_p\left[h\left(Px-{x\over h}\right)^2\right].      \tag{3}
\]

Although (3) appears to involve the nonlocal quantity `Px`, the pointwise
Bd equation eliminates it.  Indeed,

\[
 Px=Pb-{1\over2}={t(1-q)\over2q}-{1\over2}.
\]

Consequently, with `z=2q-1`,

\[
 \boxed{
 K=E_p\!\left[
       {t z^2\over q}
       -{h\over4}\left{
          {t(1-q)\over q}-1+{z\over h}
        \right\}^{\!2}
     \right].}                                               \tag{3a}
\]

Thus `K>=0` is an exact three-label equilibrium inequality in `(t,q,h)`;
no further operator estimate is hidden in its statement.  The labels are
not independent, since they still arise from the two adjoint ground
equations.

Consequently `K>=0` proves `beta+sigma<=1`, with the displayed square as a
quantitative remainder.  Conversely, every counterexample to factor one
must have `K<0`.  Thus the special ground-energy problem is not an auxiliary
analogy: (1) makes it the exact remaining sign obstruction, up to a manifest
square.

The already available Jensen contraction also gives `K>=M`, where `M` is an
explicit node marginal.  Hence the strongest current proof target is the
scalar-looking but still globally constrained inequality `M>=0` in (18)
below.

## 1. Setup

Let `P` be row-stochastic and self-adjoint in `L^2(pi)`.  Let `a>0` be
normalized by `E_pi a=1`, and put

\[
 p_i=\pi_i a_i,\qquad
 R=D_a^{-1}PD_a,\qquad t=R\mathbf1={Pa\over a}.               \tag{4}
\]

At fitness two the positive endpoint solutions obey

\[
 t b=2(1-b)Pb,qquad s=2(1-s)Rs.                             \tag{5}
\]

Write `q=1-b`, `h=1-s`, and use (2).  All expectations below are under
`p` unless another measure is displayed.

## 2. The two endpoint quadratic deficits

Define

\[
 B=4E_p\left[{t x^2\over1-2x}\right],\qquad
 D=4E_p\left[{u^2\over1-2u}\right].                          \tag{6}
\]

Both are nonnegative.  Self-adjointness and the Bd equation give

\[
 E_p\left[tb\left({1\over2q}-1\right)\right]=0.              \tag{7}
\]

Since

\[
 {b x\over q}=x+{4x^2\over1-2x},                             \tag{8}
\]

(7) says

\[
                             E_p(tx)=-B.                      \tag{9}
\]

Similarly, `E_p(Rs)=E_p(s)` and the dB equation imply

\[
 E_p\left[s\left({1\over2h}-1\right)\right]=0.
\]

Using

\[
 {s u\over h}=u+{4u^2\over1-2u},                             \tag{10}
\]

we obtain

\[
                             E_pu=-D.                         \tag{11}
\]

Thus `D=1/2-sigma` is the exact dB cost.

## 3. Dirichlet cross-energy identity

Let

\[
 \mathcal E(a,b)=\langle a,(I-P)b\rangle_\pi
 ={1\over2}\sum_{i,j}\pi_iP_{ij}(a_i-a_j)(b_i-b_j).          \tag{12}
\]

Because `P1=1`, `Pa=at`, and `P` is self-adjoint,

\[
 \mathcal E(a,b)=E_p[(1-t)x].                                \tag{13}
\]

Equations (9) and (13) therefore give the exact Bd gain formula

\[
                       \beta-{1\over2}=\mathcal E(a,b)-B.     \tag{14}
\]

Combining (11) and (14),

\[
                1-\beta-\sigma=B+D-\mathcal E(a,b).          \tag{15}
\]

This isolates the only dangerous term as a two-ground Dirichlet
cross-energy.

## 4. Completion of the square

The dB equation in centered variables is

\[
 {1\over2}+u=2h\left({t\over2}+Ru\right),
\]

so

\[
                         1-t=2Ru-{2u\over h}.                 \tag{16}
\]

Adjointness of `P` and `R` in `L^2(p)` turns (13) into

\[
 \mathcal E(a,b)
   =2E_p\left[u\left(Px-{x\over h}\right)\right].            \tag{17}
\]

Put `A=Px-x/h`.  Since `D=2E_p(u^2/h)`, completing the square
in (15) gives

\[
\begin{aligned}
 1-\beta-\sigma
 &=B-{1\over2}E_p(hA^2)
   +{1\over2}E_p\left[h\left(A-{2u\over h}\right)^2\right]\\
 &={K\over2}
   +{1\over2}E_p\left[h\left(Px-{x+2u\over h}\right)^2\right],
\end{aligned}
\]

which proves (1).

## 5. Exact Jensen marginal below `K`

Let `z=2q-1=-2x` and define

\[
 C(q)={(4-q)(2q-1)^2\over4q},\qquad
 A_0(q,h)={2q-1\over2}
       -{(2q-1)^2(1+h)\over8h},
\]

and

\[
                         M=E_p[tC(q)+A_0(q,h)].                \tag{18}
\]

Direct expansion, using the Bd identity (9), yields

\[
 K-M=E_p\left[t x^2-h(Px)^2-{s x^2\over2h}\right].           \tag{19}
\]

Jensen's inequality `(Px)^2<=P(x^2)`, adjointness, and
`Rh=t-s/(2h)` give

\[
 E_p[h(Px)^2]
 \leq E_p[hP(x^2)]
 =E_p[x^2Rh]
 =E_p\left[x^2\left(t-{s\over2h}\right)\right].              \tag{20}
\]

Therefore

\[
                              \boxed{K\geq M}.                 \tag{21}
\]

In particular,

\[
 1-\beta-\sigma
 \geq {M\over2}
   +{1\over2}E_p\left[h\left(Px-{x+2u\over h}\right)^2\right].
                                                                    \tag{22}
\]

The open proof obligation has consequently been reduced to `M>=0`.  A
failure of `M>=0` would only refute this sufficient marginal route; a
failure of `K>=0` would refute the exact ground-energy route but would not,
by itself, refute factor one because the square in (1) may compensate it.
Only a negative value of the full right side of (1) is an endpoint
counterexample.

## 6. Conditional catalyst implication

Once `K>=0` (or the stronger `M>=0`) is proved, every diffuse adjoint
branching trace at fitness two has dB cost at least its Bd gain.  Therefore
no catalyst construction whose limiting response is completely captured by
this independent diffuse normal form can approach a positive Bd response
with little-oh dB cost.  A sharp lower construction toward every fixed
`r<2` must then retain a non-diffuse same-scale interaction that the
branching reduction discards.
