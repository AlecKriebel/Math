# A natural Fenchel--Bregman obstruction for the endpoint actions

Date: 2026-08-13 (America/Los_Angeles)

No graph search, parameter search, numerical optimization, literature search,
or external communication was used.

## 1. Status and scope

**PROVED: A NATURAL VARIATIONAL-ROUTE OBSTRUCTION.**  Put

\[
 \Phi(z)=-z-\log(1-z),\qquad
 \Phi'(z)={z\over1-z},\qquad
\Phi''(z)={1\over(1-z)^2}.                                \tag{1}
\]

Throughout,

\[
                         {3\over2}\leq r\leq{151\over100},
 \qquad c=r-1,
\]

and \(R_{\rm hyb}\) lies in the interior of this interval.

The Bd and dB endpoint equations are stationary equations for two natural
actions.  Their active stationary Hessians have exact positive ground-state
representations.  Nevertheless, these actions do not form a genuine
Fenchel-conjugate pair:

1. they are globally nonconvex, already on the homogeneous one-state model;
2. their active Hessians fail the inverse-Hessian condition required by
   Legendre duality under the natural `L^2(pi)` pairing;
3. their exact cross-stationary remainders are a positive scalar Bregman term
   minus a kinetic quadratic, rather than Bregman divergences of convex
   actions;
4. on one analytic physical two-state family, the support target crosses
   both natural cross remainders and the genuine nodewise Fenchel gaps.

Consequently, the outstanding support

\[
                         T=(r-1)E_pq-E_ps                  \tag{2}
\]

is neither one of the two natural Fenchel/Bregman gaps nor a fixed,
kernel-independent scalar combination of them.  At every interior fitness,
including `R_hyb`, neither natural orientation supplies a coefficient-one
bound on `T` in either direction.  Even the symmetric sum of the two full
variational remainders crosses `T`.

This result is deliberately narrow.  It does not rule out an engineered
`P`-dependent convex action, a nonunit quantitative comparison using extra
endpoint information, or a different coupled variational principle.  It
does not prove or refute `T>=0`.

## 2. Endpoint actions and stationary equations

Let `P` be a finite row-stochastic kernel self-adjoint in `L^2(pi)`.  Let
`a>0`, normalized by `E_pi a=1`, and put

\[
 p=\pi a,\qquad t={Pa\over a},\qquad R=D_a^{-1}PD_a.        \tag{3}
\]

Suppose the positive endpoint data obey

\[
 tb=rqPb,\qquad s=rhRs,\qquad q=1-b,\quad h=1-s.           \tag{4}
\]

Equivalently,

\[
 Pb={t\over r}\Phi'(b),
 \qquad
 P(as)={a\over r}\Phi'(s).                                \tag{5}
\]

Define

\[
 \begin{aligned}
 J_B(z)&={1\over r}E_\pi\{t\Phi(z)\}
          -{1\over2}\langle z,Pz\rangle_\pi,\\
 J_D(z)&={1\over r}E_\pi\{a^2\Phi(z)\}
          -{1\over2}\langle az,P(az)\rangle_\pi.
 \end{aligned}                                              \tag{6}
\]

Their exact first variations are

\[
 \begin{aligned}
 DJ_B(z)[u]
   &={1\over r}E_\pi\{t\Phi'(z)u\}-\langle u,Pz\rangle_\pi,\\
 DJ_D(z)[u]
   &={1\over r}E_\pi\{a^2\Phi'(z)u\}
       -\langle au,P(az)\rangle_\pi.
 \end{aligned}                                              \tag{7}
\]

Thus (5) says exactly

\[
                            DJ_B(b)=0,
 \qquad DJ_D(s)=0.                                         \tag{8}
\]

The Hessians at an arbitrary interior label `z` are

\[
 \begin{aligned}
 D^2J_B(z)[u,v]
  &={1\over r}E_\pi\!\left[{tuv\over(1-z)^2}\right]
       -\langle u,Pv\rangle_\pi,\\
 D^2J_D(z)[u,v]
  &={1\over r}E_\pi\!\left[{a^2uv\over(1-z)^2}\right]
       -\langle au,P(av)\rangle_\pi.
 \end{aligned}                                              \tag{9}
\]

## 3. Exact ground-state Hessians

Write `C_ij=pi_i P_ij=C_ji`.  The standard ground-state identity says that,
for every positive ground `g`,

\[
 \left\langle w,
  \left(D_{Pg/g}-P\right)w\right\rangle_\pi
 ={1\over2}\sum_{i,j}C_{ij}g_ig_j
   \left({w_i\over g_i}-{w_j\over g_j}\right)^2.           \tag{10}
\]

For the Bd ground `b`, equation (5) gives

\[
                         {Pb\over b}={t\over rq}.
\]

Since

\[
 {t\over rq^2}-{Pb\over b}={tb\over rq^2},
\]

(9)--(10) yield

\[
 \boxed{
 \begin{aligned}
 D^2J_B(b)[u,u]
  ={}&{1\over2}\sum_{i,j}C_{ij}b_ib_j
       \left({u_i\over b_i}-{u_j\over b_j}\right)^2\\
    &+{1\over r}E_\pi\!\left[{tbu^2\over q^2}\right].
 \end{aligned}}                                             \tag{11}
\]

For the dB ground `g=as`, use the variation `w=au`.  Equation (5) gives

\[
                         {P(as)\over as}={1\over rh}.
\]

Therefore

\[
 \boxed{
 \begin{aligned}
 D^2J_D(s)[u,u]
  ={}&{1\over2}\sum_{i,j}C_{ij}(a_is_i)(a_js_j)
       \left({u_i\over s_i}-{u_j\over s_j}\right)^2\\
    &+{1\over r}E_\pi\!\left[{a^2su^2\over h^2}\right].
 \end{aligned}}                                             \tag{12}
\]

Every term in (11)--(12) is nonnegative, and the node terms are strictly
positive for nonzero `u` on the active positive branch.  Hence both active
endpoints are strict local minima of their own actions.

## 4. Why this is not Fenchel duality

The local positivity in (11)--(12) does not make the actions convex.  On the
homogeneous one-state model `P=1`, `a=t=1`, both actions reduce to

\[
                         J(z)={1\over r}\Phi(z)-{z^2\over2}. \tag{13}
\]

The zero and active stationary points have opposite curvature:

\[
 J''(0)={1\over r}-1=-{r-1\over r}<0,
 \qquad
 J''\!\left({r-1\over r}\right)=r-1>0.                    \tag{14}
\]

Thus neither natural action is a convex Fenchel generator on its full
endpoint domain.

There is also an independent local obstruction.  At homogeneous active data
`a=t=1` and `b=s=(r-1)/r`, the two Hessian operators coincide:

\[
                         H_B=H_D=rI-P.                      \tag{15}
\]

Hessians of a differentiable Legendre-conjugate pair, after the natural
endpoint recentering, must be inverse operators.  On a `P`-eigenmode with
eigenvalue `lambda`, (15) would require

\[
                              (r-\lambda)^2=1.              \tag{16}
\]

This already fails on the constant mode `lambda=1`, because
`1/2<=r-1<=51/100`.  Linear recentering does not alter this Hessian
obstruction.  Consequently `J_B` and `J_D` are not a Fenchel-conjugate pair
under the natural identity pairing.

## 5. Exact stationary Bregman remainders

Take `Phi` on the endpoint domain `0<=z<1`.  Its scalar conjugate on the
endpoint-relevant dual half-line is

\[
 \Phi^*(y)=y-\log(1+y),\qquad y\geq0.                       \tag{17}
\]

Its directed Bregman divergence has the useful complement form

\[
 \begin{aligned}
 D_\Phi(x,y)
  &:=\Phi(x)-\Phi(y)-\Phi'(y)(x-y)\\
  &={1-x\over1-y}-1-\log\!\left({1-x\over1-y}\right)
  \geq0.
 \end{aligned}                                               \tag{18}
\]

It is exactly the cross Fenchel--Young gap

\[
 \Phi(x)+\Phi^*\{\Phi'(y)\}-x\Phi'(y)=D_\Phi(x,y).         \tag{19}
\]

Using stationarity to cancel the linear terms gives, for every interior `x`,

\[
 \boxed{
 J_B(x)-J_B(b)
 ={1\over r}E_\pi\{tD_\Phi(x,b)\}
  -{1\over2}\langle x-b,P(x-b)\rangle_\pi,}               \tag{20}
\]

and

\[
 \boxed{
 J_D(x)-J_D(s)
 ={1\over r}E_\pi\{a^2D_\Phi(x,s)\}
  -{1\over2}\langle a(x-s),P\{a(x-s)\}\rangle_\pi.}      \tag{21}
\]

The natural cross quantities are therefore

\[
 \begin{aligned}
 B_B&={1\over r}E_\pi\{tD_\Phi(s,b)\},\\
 B_D&={1\over r}E_\pi\{a^2D_\Phi(b,s)\},                  \tag{22}
 \end{aligned}
\]

for the genuine nodewise Fenchel gaps, and

\[
 \begin{aligned}
 \Delta_B&:=J_B(s)-J_B(b)
   =B_B-{1\over2}\langle q-h,P(q-h)\rangle_\pi,\\
 \Delta_D&:=J_D(b)-J_D(s)
   =B_D-{1\over2}\langle a(q-h),P\{a(q-h)\}\rangle_\pi
 \end{aligned}                                               \tag{23}
\]

for the full stationary remainders.  Equations (20)--(23) exhibit the exact
structural issue: the action remainders are scalar Bregman gaps minus kinetic
quadratics.  They are not Bregman divergences generated by convex `J_B` and
`J_D`.

## 6. A physical eigenmode tangent

Take the conceptual reversible family

\[
 P_\lambda={1\over2}
 \begin{pmatrix}
 1+\lambda&1-\lambda\\
 1-\lambda&1+\lambda
 \end{pmatrix},\qquad
 \pi={1\over2}(1,1),\qquad f=(1,-1)^T,                     \tag{24}
\]

with `-1<=lambda<1`, and put

\[
                         a_\epsilon=1+\epsilon f,
 \qquad |\epsilon|<1.                                      \tag{25}
\]

Writing the endpoint residuals in the variables `(q,h)`, both Jacobians at
`epsilon=0` are `P_lambda-rI`; writing the dB residual in `s` reverses its
sign.  Their eigenvalues are `1-r` and `lambda-r`, hence they are invertible
for the stated parameters.  The implicit-function theorem therefore gives
unique analytic endpoint branches through the homogeneous active point, and
these branches remain positive for sufficiently small `|epsilon|`.

The positive endpoint branches through the homogeneous active point have the
exact first-order expansions

\[
 \begin{aligned}
 q&={1\over r}+\epsilon Qf+O(\epsilon^2),\\
 h&={1\over r}-\epsilon Qf+O(\epsilon^2),\\
 Q&={c(\lambda-1)\over r(r-\lambda)}.
 \end{aligned}                                              \tag{26}
\]

The second-order coefficient of the support target is

\[
 \boxed{
 T_2:=[\epsilon^2]T
 ={(\lambda-1)^2c\{r+\lambda c\}
       \over r(r-\lambda)^2}>0.}                            \tag{27}
\]

Since `s-b=q-h=2epsilon Qf+O(epsilon^2)`, the
homogeneous active Hessian `rI-P_lambda` and the scalar Hessian
`Phi''(c/r)=r^2` give

\[
 \boxed{
 [\epsilon^2]B_B=[\epsilon^2]B_D=2rQ^2,}                   \tag{28}
\]

and

\[
 \boxed{
 [\epsilon^2]\Delta_B=[\epsilon^2]\Delta_D
       =2(r-\lambda)Q^2.}                                  \tag{29}
\]

All four quantities in (28)--(29) are strictly positive for `lambda<1`.

## 7. Exact ratio and unit-bound obstruction

Let `B_2` and `Delta_2` denote either common coefficient in (28) and (29).
Equations (27)--(29) give

\[
 \boxed{
 {T_2\over B_2}={r+\lambda c\over2c},
 \qquad
 {T_2\over\Delta_2}
 ={r\{r+\lambda c\}\over2c(r-\lambda)}.}                  \tag{30}
\]

Both ratios are strictly increasing in `lambda`:

\[
 {\partial\over\partial\lambda}{T_2\over B_2}={1\over2},
 \qquad
 {\partial\over\partial\lambda}{T_2\over\Delta_2}
 ={r^3\over2c(r-\lambda)^2}>0.                             \tag{31}
\]

At every `3/2<r<=151/100`, the node-gap ratio satisfies

\[
 {T_2\over B_2}\bigg|_{\lambda=-1}={1\over2c}<1,
 \qquad
 {T_2\over B_2}\bigg|_{\lambda=0}={r\over2c}>1.           \tag{32}
\]

For the full variational remainder, throughout the closed strip
`3/2<=r<=151/100`,

\[
 {T_2\over\Delta_2}\bigg|_{\lambda=-1}
 ={r\over2c(r+1)}<1,
 \qquad
 {T_2\over\Delta_2}\bigg|_{\lambda=0}
 ={r\over2c}>1.                                            \tag{33}
\]

Thus neither natural orientation equals `T`, and neither supplies a
coefficient-one bound in a fixed direction.  Because the two orientations
have equal quadratic coefficients while the ratios (30) vary with
`lambda`, no fixed, kernel-independent scalar combination of `B_B,B_D` or
of `Delta_B,Delta_D` can represent `T`.

The symmetric full remainder also fails a unit comparison in either
direction.  At `lambda=-1`, (33) gives

\[
                         T_2<\Delta_{B,2}+\Delta_{D,2}.
\]

At `lambda=1/2`, the condition for the reverse strict inequality reduces to

\[
 r\left(r+{c\over2}\right)-4c\left(r-{1\over2}\right)
 =-{5r^2-11r+4\over2}>0.                                  \tag{34}
\]

Writing `r=3/2+z/100`, `0<=z<=1`, the last expression is

\[
 {5\over8}-{z\over50}-{z^2\over4000},                     \tag{35}
\]

whose degree-two Bernstein coefficients on `[0,1]` are

\[
                         {5\over8},\qquad {123\over200},
 \qquad {2419\over4000}.                                  \tag{36}
\]

They are all positive.  Hence

\[
                         T_2>\Delta_{B,2}+\Delta_{D,2}
 \qquad(\lambda=1/2)                                      \tag{37}
\]

uniformly on the full fitness strip.

The contradiction between (33) and (37) is a physical, analytic,
low-dimensional obstruction.  It uses no search and no off-physical Farkas
relaxation.

## 8. What remains

The positive Hessian formulas (11)--(12) remain potentially useful for a
local or coupled action argument.  What fails is the direct natural
Fenchel/Bregman closure: convex duality and exact fixed scalar representation
break throughout the strip; the node-gap coefficient-one comparison breaks
at every interior fitness (including `R_hyb`), while the full-remainder
comparisons already break on the closed strip.

A successful variational proof of `T>=0` must therefore add a genuinely
coupled term, retain further endpoint linkage, or construct a different
convex action whose mode curvature is not just the natural `rI-P` curvature.

## 9. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_endpoint_fenchel_bregman_obstruction/verify_fenchel_bregman.py
```

The replay uses exact symbolic arithmetic only.
