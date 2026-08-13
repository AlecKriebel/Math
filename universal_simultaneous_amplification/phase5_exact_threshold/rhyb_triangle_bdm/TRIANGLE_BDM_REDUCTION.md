# The stronger triangle BDM reduction (optional second stage)

Date: 2026-08-13 (America/Los_Angeles)

No external communication was used.  Numerical calculations mentioned below
are hostile tests only and are not part of a proof.

## Status

The arbitrary positive weighted-triangle BDM theorem remains **OPEN**, but it
is stronger than the corrected gate disjunction requires.  The exact minimal
portal product is now proved in `TRIANGLE_PORTAL_PRODUCT.md`; that theorem
closes the actual order-three local obligation.  This note retains BDM only
as an optional second-stage target and records two tempting routes that do
not close the stronger statement.

Let the triangle edge conductances be

\[
        (A,B,C)=(w_{01},w_{02},w_{12})>0,
\]

let `u_i` and `v_i` be the reciprocal-fitness Bd and dB singleton atoms, and
put `e_i=1/d_i`.  With

\[
 a={\rho_{dB}\over r-1},\qquad b=\rho_{Bd},\qquad
 Q=r(r-1)^2[\sqrt{ab}-\sqrt{(1-a)(1-b)}]_+^2,
\]

the arbitrary-portal inequality is

\[
 (x\cdot u)(x\cdot(ev))-Q(x\cdot\mathbf1)(x\cdot e)
       =x^TMx\ge0,
\]

where

\[
 M_{ij}={u_i e_jv_j+u_j e_iv_i-Q(e_i+e_j)\over2}.       \tag{1}
\]

Thus it would be enough for BDM (and is itself stronger than copositivity) to
prove the six scalar inequalities

\[
                     M_{ij}\ge0\quad(0\le i\le j\le2). \tag{2}
\]

Direct solution of the labelled six-state chains, followed by exact
substitution in (1), gives rational functions before the single square root
in `Q`.  In the chamber

\[
                    A=pq,\qquad B=q,\qquad C=1,
                    \qquad 0<p,q\le1,                  \tag{3}
\]

every denominator is positive.  Consequently (2), together with the already
proved path boundary, is a precise two-variable algebraic endpoint problem.
Hostile floating-point minimization found every entry positive; apparent
zero margins occur only on disconnected/path degenerations.  This is
evidence, not a certificate.

## Compact exact chain specification

The individual atoms need not be printed as expanded polynomials.  They are
defined exactly by a three-by-three Schur system.  Write `S_i` for the
singleton fixation probability at fitness `f=1/r`, and `D_ij` for the
doubleton probability.  For `{i,j,k}={0,1,2}`, Bd gives

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

Equations (4)--(7) are linear in the three `S_i` and determine `u` and `v`
exactly.  The forward versions with `f=r` give `a,b`.  They are preferable
to the expanded atoms: after naive common-denominator clearing, even one
`u_i v_i` has hundreds of monomials and obscures all symmetry.

## Complete-triangle anchor

At `A=B=C`,

\[
 a={2r\over3(r-1)(r+1)},\quad
 b={r^2\over r^2+r+1},\quad
 u_i={1\over r^2+r+1},\quad
 v_i={2\over3(r+1)}.                                   \tag{8}
\]

All six normalized entries coincide with `u_i v_i-Q`.  Rationalizing the
single radical shows positivity is equivalent to the positive sign of

\[
 {r^{10}-12r^8+4r^7+42r^6-4r^5-48r^4-12r^3+17r^2+12r+4
  \over9(r+1)^2(r^2+r+1)^2}.                           \tag{9}
\]

Modulo the hybrid sextic, the numerator in (9) reduces to

\[
 1658r^5-6161r^4+9652r^3-7510r^2+2224r-381.           \tag{10}
\]

Its six Bernstein coefficients are positive on the rational isolating
interval `[1502856912/10^9,1502856913/10^9]`.  Numerically, the complete
normalized margin is

\[
                    u_i v_i-Q=0.02462148928306\ldots.  \tag{11}
\]

## Why the path extremal proof does not extend

For a weighted path, one singleton product is a portal-independent lower
bound for the whole quotient.  On a triangle the ordering of

\[
                            k_i=u_i v_i                \tag{12}
\]

is not determined by the edge chamber (3), nor by vertex degrees.  Exact
pairwise differences factor by the expected edge-equality factor, but the
remaining chamber polynomial changes sign near the equal triangle.  For
example, the chamber point `(A,B,C)=(0.81310759,0.99644258,1)` reverses the
generic ordering of the first two products.  Therefore there is no fixed
extremal vertex to which the weighted-path argument can be copied.

This does not obstruct (2): direct entrywise comparison avoids choosing the
smallest diagonal product.

## Comparison with the minimal stationary product inequality

For the uniform Bd portal law, the dB portal law is inverse-degree weighted,
and

\[
 q_Bq_D={s_B\over3}s_D^{(h)}.                           \tag{13}
\]

The stationary product inequality (65), now proved for arbitrary triangle
portals in the companion note, gives the smaller target

\[
 q_Bq_D\ge r^3[\rho_{Bd}-p]_+[\rho_{dB}-p]_+,
 \qquad p=1-1/r.                                      \tag{14}
\]

At the complete triangle and `r=R_hyb`, the right side of (14) is

\[
 0.03116645192037\ldots,
\]

whereas the BDM target is

\[
 Q=0.03132009800338\ldots.                             \tag{15}
\]

Thus the minimal product misses the stronger BDM target already at the equal
triangle by about `0.49%`.  The actual singleton product there is
`0.05594158728644...`.  Away from equality the proved dB exchange-square
theorem lowers `a` and hence usually lowers `Q`, but (14) can collapse to
zero when either fixation excess crosses `p`.  This is not a defect for the
gate disjunction, whose exact target is (14); it only shows that BDM cannot
be deduced from the minimal theorem.

## Precise obstruction and next proof object

The all-r dB exchange-square theorem supplies strict density slack away from
the equal triangle, and the weighted-path theorem proves every connected
edge-degeneration.  A clean remaining proof would show that each scalar
entry in (2), after rationalizing its single radical, has no negative
interior minimum in the chamber (3).  Equivalently, one wants an
edge-degeneration identity of the schematic form

\[
 M_{ij}=M_{ij}^{K_3}+\sum_{\rm edge\ pairs}(w_e-w_f)^2 C_{ij;e,f}
        +\text{positive boundary terms},              \tag{16}
\]

with nonnegative rational coefficient functions.  No such identity was
found.  Blind expansion produces hundreds to thousands of terms and is not
a proof-first route.  The correct stopping point is therefore (1)--(7), not
a large Bernstein partition of the full two-dimensional chamber.
