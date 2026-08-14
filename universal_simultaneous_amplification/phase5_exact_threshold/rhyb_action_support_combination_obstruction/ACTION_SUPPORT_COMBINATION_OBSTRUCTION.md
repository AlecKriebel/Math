# A regular-combination obstruction for the endpoint actions

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel search, parameter search, coefficient search,
numerical optimization, literature search, or external communication was
used.

## 1. Result and scope

Write

\[
 c=r-1,\qquad
 T=cE_pq-E_ps,
 \qquad
 U=cE_pq-E_p\mathcal F_r(cq),
 \quad
 \mathcal F_r(y)={rRy\over1+rRy}.
 \tag{1}
\]

The scaled-first theorem proves `U>=0` for

\[
                         {3\over2}\leq r\leq{151\over100}.
\]

The global-action theorem proves

\[
 \Delta_B=J_B(s)-J_B(b)\geq0,
 \qquad
 \Delta_D=J_D(b)-J_D(s)\geq0.                         \tag{2}
\]

These three nonnegative scalars do **not** admit a regular positive exact
combination equal to `T`.  More precisely, fix any `r` in the displayed
interval.  There are no nonnegative coefficient formulas

\[
             A_B(\mathcal E),\quad A_D(\mathcal E),
             \quad B(\mathcal E),                       \tag{3}
\]

which

1. depend on the endpoint data
   `mathcal E=(pi,a,t,q,h)` but not on the kernel `P` itself;
2. are continuous, and hence nonsingular for the present argument, at
   the homogeneous endpoint

   \[
        \mathcal E_0=(\pi,\mathbf1,\mathbf1,
                      r^{-1}\mathbf1,r^{-1}\mathbf1);
   \]

3. satisfy on every nearby physical endpoint datum the exact identity

   \[
              T=A_B(\mathcal E)\Delta_B
                +A_D(\mathcal E)\Delta_D+B(\mathcal E)U. \tag{4}
   \]

The obstruction remains after resolving each action remainder into the two
nonnegative pieces supplied by the global theorem: its scalar Bregman
remainder and its Picone edge square.  In fact, at the quadratic tangent the
scaled-first term is forced to have zero coefficient, while matching the
target slope would require the aggregate Picone coefficient to be `-r/2`.

The same conclusion holds if (4) is multiplied by a continuous positive
factor which is nonzero at `mathcal E_0`, since one may divide by that
factor.

This is a proof-route obstruction, not a counterexample to `T>=0`.  It does
not rule out a coefficient rule singular or discontinuous at the homogeneous
endpoint, an inequality which retains additional linked endpoint data, or a
different coupled action.  In particular, a ratio of vanishing endpoint
deviations can recover the kernel mode and evade the continuity hypothesis;
such a rule is not a regular consequence of the three unsigned scalar
remainders.

## 2. The analytic physical tangent family

Let

\[
 P_\lambda={1\over2}
 \begin{pmatrix}
 1+\lambda&1-\lambda\\
 1-\lambda&1+\lambda
 \end{pmatrix},\qquad
 \pi={1\over2}(1,1),\qquad f=(1,-1)^T,                 \tag{5}
\]

where `-1<lambda<1`, and put

\[
                         a_\epsilon=\mathbf1+\epsilon f,
 \qquad |\epsilon|<1.                                  \tag{6}
\]

This is a positive reversible two-state family.  With

\[
 p=\pi a,\qquad R=D_a^{-1}P_\lambda D_a,
 \qquad t={P_\lambda a\over a},                         \tag{7}
\]

the active endpoint branches are analytic at `epsilon=0`.  Put

\[
 Q={c(\lambda-1)\over r(r-\lambda)}.                    \tag{8}
\]

The exact implicit expansion begins

\[
 \begin{aligned}
 q&={1\over r}\mathbf1+\epsilon Qf+O(\epsilon^2),\\
 h&={1\over r}\mathbf1-\epsilon Qf+O(\epsilon^2).
 \end{aligned}                                         \tag{9}
\]

The second-order constants are included in the replay and are needed to
evaluate the averaged linear targets correctly.  The important feature is
that every endpoint datum in (7)--(9) converges to the same
`mathcal E_0`, independently of `lambda`.  A kernel-independent coefficient
formula continuous at `mathcal E_0` must therefore have one common limiting
value along every member of this family.

## 3. Exact quadratic data

Write `[epsilon^2]Z` for the quadratic Taylor coefficient of `Z`.  Direct
substitution in the endpoint equations and the scaled map gives

\[
 \boxed{
 { [\epsilon^2]T\over Q^2}
       ={r\{r+c\lambda\}\over c},}                    \tag{10}
\]

\[
 \boxed{
 { [\epsilon^2]U\over Q^2}
       =r+(3r-5)\lambda+{(r-2)^2\over r}\lambda^2,}    \tag{11}
\]

and the two cross-action remainders have the common coefficient

\[
 \boxed{
 { [\epsilon^2]\Delta_B\over Q^2}
 ={ [\epsilon^2]\Delta_D\over Q^2}
       =2(r-\lambda).}                                  \tag{12}
\]

For reference, (11) can also be read from the exact reciprocal decomposition
of the endpoint gap.  If `C` denotes the quadratic coefficient of its
oriented fluctuation remainder, then

\[
 {C\over Q^2}
 =-\lambda(r-2)\left(2+{\lambda(r-2)\over r}\right),
 \qquad
 [\epsilon^2]U={c\over r}[\epsilon^2]T-C.              \tag{13}
\]

Now resolve (12) using the new global action decompositions.  Denote the
nonnegative scalar and Picone terms by

\[
 \Delta_B=S_B+E_B,\qquad \Delta_D=S_D+E_D.              \tag{14}
\]

The same exact tangent calculation gives

\[
 \boxed{
 { [\epsilon^2]S_B\over Q^2}
 ={ [\epsilon^2]S_D\over Q^2}=2c,}                     \tag{15}
\]

\[
 \boxed{
 { [\epsilon^2]E_B\over Q^2}
 ={ [\epsilon^2]E_D\over Q^2}=2(1-\lambda).}           \tag{16}
\]

Thus the scalar term records only the homogeneous curvature, while the
Picone term records the varying edge mode.

## 4. No regular positive combination of the full remainders

Assume (4).  By continuity, let

\[
 A=A_B(\mathcal E_0)+A_D(\mathcal E_0)\geq0,
 \qquad B=B(\mathcal E_0)\geq0.                         \tag{17}
\]

Divide the quadratic coefficient of (4) by `Q^2`.  Equations (10)--(12)
would imply, for every `lambda` in an interval,

\[
 {r(r+c\lambda)\over c}
 =2A(r-\lambda)
 +B\left\{r+(3r-5)\lambda
             +{(r-2)^2\over r}\lambda^2\right\}.      \tag{18}
\]

This passage needs no differentiability of the coefficient formulas.  Each
remainder is `epsilon^2` times its displayed coefficient plus
`o(epsilon^2)`, while each multiplier equals its value at
`mathcal E_0` plus `o(1)`.  Divide (4) by `epsilon^2` and let `epsilon`
tend to zero.

Because `r!=2`, the quadratic coefficient forces `B=0`.  The linear
coefficient then forces

\[
                              A=-{r\over2},              \tag{19}
\]

contrary to (17).  In fact, even allowing `A` to be signed does not give an
identity: after (19), the constant terms in (18) are still unequal.

No scalar coefficient search is involved.  The varying kernel mode creates
the quadratic term in (11), and coefficient comparison proves the
obstruction immediately.

## 5. Resolving the positive pieces does not help

Allow the stronger representation

\[
 \begin{aligned}
 T={}&A_{B,s}(\mathcal E)S_B+A_{B,e}(\mathcal E)E_B
      +A_{D,s}(\mathcal E)S_D+A_{D,e}(\mathcal E)E_D\\
    &+B(\mathcal E)U,                                    \tag{20}
 \end{aligned}
\]

with all five coefficient formulas nonnegative and continuous at
`mathcal E_0`.  Let `A_s,A_e,B_0` be the sums of the two limiting scalar
coefficients, the two limiting edge coefficients, and the limiting
scaled-first coefficient, respectively.  Equations (10)--(11) and
(15)--(16) give

\[
 {r(r+c\lambda)\over c}
 =2cA_s+2(1-\lambda)A_e
 +B_0\left\{r+(3r-5)\lambda
             +{(r-2)^2\over r}\lambda^2\right\}.       \tag{21}
\]

Again the quadratic coefficient forces `B_0=0`.  The linear coefficient is
then

\[
                             r=-2A_e,                    \tag{22}
\]

so the required aggregate Picone coefficient is exactly `-r/2`.  This is
the structural failure: the globally nonnegative edge square enters with
the opposite sign from the one needed to reproduce the support target.

Consequently, global endpoint minimality is genuine new unsigned control,
but it cannot be converted into `T>=0` by any regular positive exact mixing
of its cross remainders with the proved scaled-first scalar slack.  A live
proof must retain a linked signed identity not compressed into these
nonnegative scalars.

## 6. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_action_support_combination_obstruction/\
verify_action_support_combination.py
```

The replay reconstructs the analytic endpoint tangent, verifies both
endpoint equations through quadratic order, calculates `T`, `U`, both full
cross-action remainders, their four positive scalar/Picone components, and
the two polynomial coefficient obstructions.
