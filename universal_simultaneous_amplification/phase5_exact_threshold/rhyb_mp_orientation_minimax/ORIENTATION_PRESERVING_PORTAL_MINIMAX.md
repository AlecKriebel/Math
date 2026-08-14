# An orientation-preserving minimax for the universal portal product

Date: 2026-08-13 (America/Los_Angeles)

## Status

**PROVED EXACT EQUIVALENCE.**  For any fixed module, the all-portal minimal
stationary product is equivalent to one positive diagonal operator-norm
inequality with two scalar variables.  One scalar is the global balance
between the Bd and dB root assignments.  Keeping it global retains exactly
the orientation square which the stronger root-Hellinger route discards.

The minimax has three consequences.

1. The exact portal inequality, not merely its root-Hellinger
   strengthening, needs to be checked only on portals supported on at most
   two roots.
2. Every such test has a closed two-by-two copositivity criterion.
3. That criterion is the existing root-Hellinger pair condition plus an
   explicit nonnegative `cosh` orientation repayment.

This removes the portal dimension from `(MP)`, `(SRR)`, and `(PTR)` without
weakening any of them.  It does **not** prove their universal sign: the
root-law and signed excursion quantities still depend on the full module.

## 1. Abstract portal product

Let

\[
 U_i>0,\qquad V_i>0,\qquad e_i>0\qquad(i=1,\ldots,n),
\]

put `W_i=e_iV_i`, and fix `Q>=0`.  For a nonzero portal load `x>=0`, define

\[
 \mathcal J(x)={ (x\mathbin\cdot U)(x\mathbin\cdot W)
                  \over
                  (x\mathbin\cdot\mathbf1)(x\mathbin\cdot e)}. \tag{1}
\]

The abstract all-portal inequality is

\[
 \boxed{
 (x\mathbin\cdot U)(x\mathbin\cdot W)
 \ge Q(x\mathbin\cdot\mathbf1)(x\mathbin\cdot e)
 \quad\hbox{for every }x\ge0.}                       \tag{AP}
\]

Its sharp constant is

\[
 Q_*:=\min_{x\ge0,\ x\ne0}\mathcal J(x)>0.           \tag{2}
\]

The minimum exists after normalizing `x dot 1=1`.  Thus `(AP)` is exactly
`Q<=Q_*`.  When `Q=0`, `(AP)` is automatic.  All divisions by `sqrt(Q)`
below are restricted explicitly to the active case `Q>0`.
If portals are conventionally required to be strictly positive, the same
criterion follows by continuity from their closure `x>=0`.

## 2. Exact global-orientation variational form

Normalize `x` to a probability vector `theta`.  Set

\[
 A=\theta\mathbin\cdot U,\qquad
 B=\theta\mathbin\cdot W,\qquad
 E=\theta\mathbin\cdot e.
\]

For `lambda>0`, put

\[
 c_i(\lambda)=\lambda U_i+\lambda^{-1}W_i.            \tag{3}
\]

The scalar arithmetic--geometric identity gives

\[
 AB={1\over4}\min_{\lambda>0}
       \{\lambda A+\lambda^{-1}B\}^2,                 \tag{4}
\]

with minimizer `lambda=sqrt(B/A)`.  Therefore

\[
 \boxed{
 Q_*={1\over4}\inf_{\lambda>0}\min_{\theta\in\Delta_n}
 {\{\theta\mathbin\cdot c(\lambda)\}^2
  \over\theta\mathbin\cdot e}.}                     \tag{5}
\]

There is no Cauchy loss in (5).  The same `lambda` is used at every root.
If one were to minimize each root summand separately, then

\[
 \sum_i\theta_i\min_{\lambda_i>0}
       (\lambda_iU_i+\lambda_i^{-1}W_i)
 =2\sum_i\theta_i\sqrt{U_iW_i},                       \tag{6}
\]

which is exactly the stronger root-Hellinger replacement.  The difference
between the two routes is exact.  If
`A_i=theta_iU_i`, `B_i=theta_iW_i`, and
`H=sum_i sqrt(A_iB_i)`, then after the square in (4) it is

\[
 AB-\mathcal H^2={1\over2}\sum_{i,j}
 \left(\sqrt{A_iB_j}-\sqrt{A_jB_i}\right)^2.          \tag{6a}
\]

Thus the global `lambda` retains the full root-assignment orientation
square literally.

## 3. Exact support-two theorem

For fixed `lambda`, abbreviate `c=c(lambda)` and consider

\[
 m(c)=\min_{\theta\in\Delta_n}
           { (\theta\mathbin\cdot c)^2
             \over\theta\mathbin\cdot e}.             \tag{7}
\]

At a minimizer, put `C=theta dot c` and `E=theta dot e`.  Every active
coordinate obeys the Lagrange equation

\[
 {2C\over E}c_i-{C^2\over E^2}e_i=\hbox{constant}.    \tag{8}
\]

Thus all active points `(c_i,e_i)` lie on one affine line.  The two moments
`(C,E)` can be reproduced by a convex combination of the two extreme
active points.  Hence a minimizer of (7) exists with support at most two.

Positivity makes the objective in (5) coercive as `lambda` tends to zero or
infinity, uniformly over the compact simplex, so a joint minimizer exists.
Apply the preceding argument to such a minimizer.  Replacing its portal law by the
support-two minimizer for the same global `lambda` cannot increase (5), and
global minimality forces equality.  Consequently

\[
 \boxed{
 Q_*=\min_{1\le i\le j\le n}
       \ min_{\substack{x\ge0,\ x\ne0\\
                        \operatorname{supp}x\subseteq\{i,j\}}}
       \mathcal J(x).}                                \tag{9}
\]

In particular:

> `(AP)` holds for every portal load if and only if it holds for every
> portal load supported on at most two roots.

This is an equivalence for the exact product.  It is not the previously
known pair reduction of the stronger root-Hellinger condition.

## 4. One positive diagonal operator norm

The variational form (5) also has an exact minimax expression.  For a fixed
positive vector `c`, make the bijective change of probability law

\[
 \eta_i={\theta_ic_i\over\theta\mathbin\cdot c}.
\]

Its inverse is proportional to `eta_i/c_i`, and direct substitution gives

\[
 m(c)^{-1}
 =\max_{\eta\in\Delta_n}
   \left(\eta\mathbin\cdot{\mathbf1\over c}\right)
   \left(\eta\mathbin\cdot{e\over c}\right).          \tag{10}
\]

For two positive linear means, global arithmetic--geometric minimization
and finite-dimensional minimax give

\[
 2\sqrt{m(c)^{-1}}
 =\inf_{t>0}\max_i {t+e_i/t\over c_i}.                 \tag{11}
\]

There is no noncompactness gap in (11).  If
`a_i=1/c_i` and `b_i=e_i/c_i`, every individual minimizer lies in

\[
 \left[\sqrt{\min b/\max a},\sqrt{\max b/\min a}\right],
\]

and outside that compact interval all functions
`t a_i+b_i/t` move in the same direction.  On the compact interval, Sion's
minimax theorem applies because the expression is linear in `eta` and
convex in `t`.

Let `E=diag(e_i)` and

\[
 D_\lambda=\operatorname{diag}
       \{\lambda U_i+\lambda^{-1}W_i\}_{i=1}^n.       \tag{12}
\]

Combining (5), (10), and (11) proves

\[
 \boxed{
 Q_*=\mathfrak N^{-2},\qquad
 \mathfrak N=\sup_{\lambda>0}\inf_{t>0}
 \left\|D_\lambda^{-1}(tI+t^{-1}E)\right\|_{\infty\to\infty}.} \tag{13}
\]

The operator inside (13) is positive and diagonal, and its norm is exactly

\[
 \max_i {t+e_i/t\over\lambda U_i+\lambda^{-1}W_i}.    \tag{14}
\]

Thus, for `Q>0`, `(AP)` is equivalent to the single positive-cone norm
inequality

\[
 \boxed{\mathfrak N\le Q^{-1/2}.}                     \tag{15}
\]

The quantifiers in (13)--(15) are important.  Equivalently,

\[
 \boxed{
 \text{for every }\lambda>0\text{ there exists }t>0\text{ such that}
 \quad
 \lambda U_i+\lambda^{-1}W_i
 \ge\sqrt Q\,(t+e_i/t)\quad\hbox{for every }i.}      \tag{16}
\]

Neither `lambda` nor `t` may be selected separately at each root.  Swapping
`for every lambda` and `there exists t` is a genuine strengthening and is
not asserted.

## 5. Interval and Helly form

For `Q>0`, define

\[
 I_i(\lambda;Q)=
 \left[
 {c_i(\lambda)-\sqrt{c_i(\lambda)^2-4Qe_i}\over2\sqrt Q},
 {c_i(\lambda)+\sqrt{c_i(\lambda)^2-4Qe_i}\over2\sqrt Q}
 \right],                                             \tag{17}
\]

declaring the interval empty if its discriminant is negative.  The
coordinate inequality in (16) is exactly `t in I_i(lambda;Q)`.  Hence

\[
 (AP)\quad\Longleftrightarrow\quad
 \bigcap_i I_i(\lambda;Q)\ne\varnothing
 \quad\hbox{for every }\lambda>0.                     \tag{18}
\]

For each fixed `lambda`, a finite family of closed real intervals has a
common point if and only if every pair intersects.  This one-dimensional
Helly theorem gives an independent quantifier audit of (9): pair-supported
portal validity says exactly that every pair of intervals intersects for
every `lambda`, which forces (18).  Degenerate one-point intervals cover
the equality boundary without any strictness assumption.

## 6. Closed pair criterion

Put

\[
 h_i=U_iV_i,\qquad
 \Delta_i=U_iW_i-Qe_i=e_i(h_i-Q),                      \tag{19}
\]

and, for `i!=j`,

\[
 k_{ij}=U_iW_j+U_jW_i-Q(e_i+e_j).                     \tag{20}
\]

On the pair `{i,j}`, the homogeneous gap in `(AP)` is

\[
 \Delta_ix_i^2+k_{ij}x_ix_j+\Delta_jx_j^2.           \tag{21}
\]

The elementary two-by-two copositivity criterion, together with (9), now
gives the exact all-portal theorem

\[
 \boxed{
 h_i\ge Q\quad(i=1,\ldots,n),\qquad
 k_{ij}+2\sqrt{\Delta_i\Delta_j}\ge0\quad(i\ne j).} \tag{22}
\]

All inequalities in (22) are non-strict.  If `Delta_i=0`, the square-root
term vanishes normally.  For `Q=0`, positivity of `U,V,e` makes (22)
automatic, in agreement with `(AP)`.

The existing entrywise portal target is `k_ij>=0`.  Equation (22) proves
precisely that it is sufficient but not necessary: it discards the
nonnegative diagonal repayment `2sqrt(Delta_i Delta_j)`.

## 7. Exact orientation-square form

For a pair `i!=j`, define

\[
 \delta_{ij}={1\over2}\log
 {U_i e_jV_j\over U_j e_iV_i},
 \qquad
 \epsilon_{ij}={1\over2}\log{e_i\over e_j}.          \tag{23}
\]

Dividing the pair condition in (22) by `2sqrt(e_i e_j)` gives

\[
 \boxed{
 \sqrt{h_ih_j}\cosh\delta_{ij}
 +\sqrt{(h_i-Q)(h_j-Q)}
 \ge Q\cosh\epsilon_{ij}.}                           \tag{24}
\]

Indeed,

\[
 U_iW_j+U_jW_i
 =2\sqrt{e_ie_jh_ih_j}
  +\left(\sqrt{U_iW_j}-\sqrt{U_jW_i}\right)^2.        \tag{25}
\]

The last square is exactly the swapped root-assignment orientation term.
Equivalently, its contribution to (24) is

\[
 \sqrt{h_ih_j}\{\cosh\delta_{ij}-1\}\ge0.           \tag{26}
\]

The previously defined root-Hellinger pair criterion is exactly (24) with
`cosh(delta_ij)` replaced by one.  Therefore (24) is the requested exact
pairwise formulation which retains, rather than estimates away, the root
orientation square.

## 8. Normalization audit for `(MP)`, `(SRR)`, and `(PTR)`

The abstract theorem applies at all three existing resolutions.

### Raw stationary form `(MP)`

Let `u_i` and `v_i` be the Bd and dB stationary singleton atoms.  A physical
portal load has

\[
 q_B={x\mathbin\cdot u\over x\mathbin\cdot\mathbf1},
 \qquad
 q_D={x\mathbin\cdot(ev)\over x\mathbin\cdot e}.      \tag{27}
\]

Use

\[
 U=u,\quad V=v,\quad
 Q=r^3[\rho_{Bd}-p]_+[\rho_{dB}-p]_+.                 \tag{28}
\]

Then `(AP)` is exactly `(MP)` after multiplying by the two positive portal
denominators.

### Normalized singleton-root form `(SRR)`

Write `u=c_B lambda_B`, `v=c_D lambda_D` and

\[
 \rho_{Bd}-p=c_B\overline\phi_B,qquad
 \rho_{dB}-p=c_D\overline\phi_D.                     \tag{29}
\]

Both sides of the raw inequality contain the common factor `c_Bc_D`.
Indeed, positivity of the singleton masses gives
`[c_U bar(phi)_U]_+=c_U[bar(phi)_U]_+`.  After cancellation, use

\[
 U=\lambda_B,\quad V=\lambda_D,\quad
 Q=Q_0:=r^3[\overline\phi_B]_+
              [\overline\phi_D]_+.                   \tag{30}
\]

Thus (5), (9), (13), (22), and (24) are exact formulations of the
all-portal `(SRR)`.

### Root-tree form `(PTR)`

Let

\[
 U_i=\tau_{Bd}(\{i\}),\qquad
 V_i=\tau_{dB}(\{i\}),                                \tag{31}
\]

and

\[
 Q=r^3[\mathcal T_{Q_{Bd}}(g)]_+
       [\mathcal T_{Q_{dB}}(g)]_+.                    \tag{32}
\]

Since

\[
 \mathcal T_{Q_{Bd}}(f_\gamma)
 ={x\mathbin\cdot U\over x\mathbin\cdot\mathbf1},
 \qquad
 \mathcal T_{Q_{dB}}(f_\alpha)
 ={x\mathbin\cdot(eV)\over x\mathbin\cdot e},      \tag{33}
\]

`(AP)` is exactly the all-portal `(PTR)`.

No stationary or tree normalizer is introduced in passing among these
forms.  The raw-to-normalized cancellation in (29)--(30) and the already
normalizer-free tree coordinates in (31)--(33) preserve the sign exactly.

## 9. Scope and next target

The portal quantifier is now finite and pairwise, and the precise amount of
orientation repayment is visible in (24).  What remains is not a portal
optimization problem.  For every finite module and every pair of roots one
must prove (24), with `h_i`, `delta_ij`, and the signed reward product `Q`
generated by the two full recurrent dual chains.

The minimax does not compare those chains and does not prove universal
`(MP)` or `(PTR)`.  It shows exactly what an operator proof must establish:
the degree mismatch on the right of (24) must be paid jointly by the
same-root excess terms and the swapped-root orientation square.

## 10. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_mp_orientation_minimax/verify_orientation_minimax.py
```

The replay reconstructs the generic two-root quadratic, the global
orientation identity, the reciprocal probability transform behind the
operator norm, both normalization cancellations, and exact strictness
audits separating `(AP)` from its entrywise and root-Hellinger
strengthenings.
