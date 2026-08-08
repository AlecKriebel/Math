# Direct portal networks: exact trace and a two-portal separator

Date: 2026-08-08 (America/Los_Angeles)

Status: **the full fixed-`Q,T` trace is exactly derived.  For two portals
and one blade type, arbitrary unequal positive loads and an arbitrary
positive direct portal edge are rigorously excluded for every `r>=3/2`.
Higher-rank incidence and three or more direct portals remain open.**

No literature search or external contact was used.  Every rate below comes
from the atomic Bd and dB rules.  Fixation is only bounded above by the
clean-blade establishment trace; no independent-genealogy assertion is used.

## 1. General direct-portal trace

Fix `Q,T` independently of `s`.  There are `s` disjoint unit-weight blade
edges.  The fraction of type-`t` blades tends to `pi_t>0`.  Both endpoints
of a type-`t` blade are joined to portal `a` with weight

\[
 {\lambda_{at}\over s}.
\]

The portals have a fixed symmetric network `h_ab=h_ba>=0`.  Define

\[
 B_a=2\sum_t\pi_t\lambda_{at},\qquad
 d_a=B_a+\sum_{b\ne a}h_{ab},\qquad
 f_{at}={2\pi_t\lambda_{at}\over B_a}.
\tag{1}
\]

Each row of `f` is a probability vector.  During a rare-mutant portal
episode let `A` be the nonempty set of mutant portals.  Direct first-event
conditioning gives the following exact rates.

For Bd, mutant portal `a in A` is lost and resident portal `b notin A` is
gained at rates

\[
 \delta^B_a(A)=B_a+\sum_{b\notin A}{h_{ab}\over d_b},\qquad
 \upsilon^B_b(A)=r\sum_{a\in A}{h_{ab}\over d_a}.       \tag{2}
\]

Successful type-`t` children are marked at rate

\[
 \beta^B_t(A)={2\pi_t r^2\over r+1}
                  \sum_{a\in A}{\lambda_{at}\over d_a}. \tag{3}
\]

For dB the corresponding rates are

\[
 \delta^D_a(A)=
 {B_a+\sum_{b\notin A}h_{ab}\over
  B_a+\sum_{b\notin A}h_{ab}
       +r\sum_{b\in A\setminus\{a\}}h_{ab}},           \tag{4}
\]

\[
 \upsilon^D_b(A)=
 {r\sum_{a\in A}h_{ab}\over
  B_b+\sum_{c\notin A,\ c\ne b}h_{bc}
       +r\sum_{a\in A}h_{ab}},                         \tag{5}
\]

and

\[
 \beta^D_t(A)=\pi_t r\sum_{a\in A}\lambda_{at}.       \tag{6}
\]

The factor `1/2` from resolution of a dB singleton child is already included
in (6).  If `F^U_A(z)` is the joint PGF of marked children before the portal
set first becomes empty, then `F^U_empty=1` and the complete exact system is

\[
 \left[\sum_{a\in A}\delta^U_a(A)
       +\sum_{b\notin A}\upsilon^U_b(A)
       +\sum_t\beta^U_t(A)(1-z_t)\right]F^U_A
 =\sum_{a\in A}\delta^U_a(A)F^U_{A\setminus\{a\}}
  +\sum_{b\notin A}\upsilon^U_b(A)F^U_{A\cup\{b\}}.  \tag{7}
\]

This retains all `2^Q-1` labelled portal subsets; no count lumping is used.

For a descendant-survival vector `s`, put

\[
 H^U_a(s)=1-F^U_{\{a\}}(1-s),\qquad
 m_a=\sum_t f_{at}s_t.                                 \tag{8}
\]

The parent blade's exact lifetime survival map is

\[
 S^U_t(s)={R^U_t(s)\over1+R^U_t(s)},                   \tag{9}
\]

where direct substitution of its seeding and death rates gives

\[
 R^B_t(s)=r(r+1)
 {\sum_a B_af_{at}H^B_a(s)\over
  \sum_a B_af_{at}/d_a},                               \tag{10}
\]

\[
 R^D_t(s)=2r^2
 {\sum_a B_af_{at}H^D_a(s)/d_a\over
  \sum_a B_af_{at}}.                                  \tag{11}
\]

Equations (2)--(11) are the exact finite portal-episode offspring maps for
arbitrary fixed direct portal networks.

## 2. The asymmetric two-portal scalar class

Now take `Q=2,T=1`.  Equivalently, every blade endpoint has weights
`lambda_1/s,lambda_2/s` to the two portals, and the portal edge has weight
`h>0`.  Put

\[
 B_i=2\lambda_i>0,\qquad d_i=B_i+h.                   \tag{12}
\]

This includes unequal portal loads.  It is strictly more general than the
previous exchangeable protected-pair calculation.

For a scalar child mark `v=1-q`, let `H_U(v)=(H_{U,1},H_{U,2})^T` be the
probability of at least one retained child before portal extinction.  State
order is `{1},{2},{1,2}`.  It is the first two entries of the exact solution

\[
 M_U(v)\widehat H_U(v)=k_U(v).                         \tag{13}
\]

For Bd, with `C=r^2/(r+1)`,

\[
 k_B=\left(C{B_1v\over d_1},
           C{B_2v\over d_2},
           Cv\left({B_1\over d_1}+{B_2\over d_2}\right)\right)^T,
\tag{14}
\]

\[
 M_B=\begin{pmatrix}
 B_1+h/d_2+rh/d_1+k_1&0&-rh/d_1\\
 0&B_2+h/d_1+rh/d_2+k_2&-rh/d_2\\
 -B_2&-B_1&B_1+B_2+k_{12}
 \end{pmatrix}.                                      \tag{15}
\]

For dB, with `D=r/2`,

\[
 k_D=(DB_1v,DB_2v,D(B_1+B_2)v)^T,                    \tag{16}
\]

\[
 M_D=\begin{pmatrix}
 1+rh/(B_2+rh)+k_1&0&-rh/(B_2+rh)\\
 0&1+rh/(B_1+rh)+k_2&-rh/(B_1+rh)\\
 -B_2/(B_2+rh)&-B_1/(B_1+rh)&
 B_2/(B_2+rh)+B_1/(B_1+rh)+k_{12}
 \end{pmatrix}.                                      \tag{17}
\]

Every denominator is positive.  More intrinsically, a matrix of the form
in (13) has determinant

\[
 abk_{12}+a\,t_2(\ell_2+k_2)+b\,t_1(\ell_1+k_1)>0,   \tag{18}
\]

where `a=ell_1+u_1+k_1`, `b=ell_2+u_2+k_2`, and `t_i`
are the two rates out of the double-mutant state.  Thus (13) has no hidden
sign choice.

The scalar total-lifetime offspring PGFs are

\[
 D_B(q)={\mu_B\over
 \mu_B+r\{B_1H_{B,1}(1-q)+B_2H_{B,2}(1-q)\}},
\quad
 \mu_B={1\over r+1}\left({B_1\over d_1}+{B_2\over d_2}\right),
\tag{19}
\]

\[
 D_D(q)={\mu_D\over
 \mu_D+r\{B_1H_{D,1}(1-q)/d_1+B_2H_{D,2}(1-q)/d_2\}},
\quad
 \mu_D={B_1+B_2\over2r}.                             \tag{20}
\]

## 3. Exact separator theorem

Let

\[
 q_B^0={1\over r^2},\qquad q_D^0={2-r\over r},        \tag{21}
\]

and define the two exact PGF test margins

\[
 T_B=q_B^0-D_B(q_B^0),\qquad
 T_D=q_D^0-D_D(q_D^0).                                \tag{22}
\]

For `3/2<=r<2`, convexity of a scalar PGF shows that Bd establishment
exceeds `p=1-1/r` exactly when `T_B>0`, and dB establishment exceeds `p`
exactly when `T_D>0`.

**Theorem (arbitrary direct edge, unequal two-portal loads).**  For every

\[
 {3\over2}\le r\le2,\qquad B_1,B_2,h>0,
\]

the exact strict separator

\[
 T_B+{81\over200}T_D<0                               \tag{23}
\]

holds.  Consequently the clean-blade establishment bounds cannot both
exceed `p` for any `r>=3/2`.  At `r=2`, dB has entrance factor `1/2=p` and
positive extinction probability; for `r>2`, its entrance factor is already
strictly below `p`.

For fixed parameters, (23) supplies a strict establishment gap for at least
one rule.  Since finite-graph fixation requires reaching every fixed
clean-blade cutoff, the stopped-trace convergence gives
`limsup rho_U<=alpha_U<p` for that rule.  The corresponding finite graph
family is therefore eventually suppressing relative to its complete-graph
baseline.  The suppressing rule may depend on `r` and on the fixed graph
parameters.

## 4. Exact certificate

Substitute

\[
 r={3+a\over2},\qquad a\in[0,1],\qquad
 B_i={u_i\over1-u_i},\quad h={u_3\over1-u_3}.          \tag{24}
\]

After putting the negative of the left side of (23) over its common positive
denominator and clearing positive factors, the numerator has multidegree

\[
 (14,11,11,11)                                       \tag{25}
\]

in `(a,u_1,u_2,u_3)` and 7,323 nonzero power coefficients.  The
compactified mixed Bernstein tensor has 1,039 negative coefficients before
subdivision.  A fixed exact de Casteljau cover uses 11 boxes and maximum
depth five.  The common denominator has 7,323 strictly positive monomial
coefficients.  Every terminal numerator coefficient is nonnegative, and an
exact audit of all 282 terminal relative faces meeting
`[0,1] x (0,1)^3` finds an active positive coefficient.  This proves strict
positivity on the whole physical domain, including `r=3/2` and `r=2`.

`verify_q2_scalar_separator.py` regenerates the rational numerator from
(13)--(22), verifies positivity of the common denominator, rebuilds the
mixed Bernstein tensor without floating point, follows the fixed 11 paths,
and audits strictness on every physical face.

`verify_direct_trace_exact.py` independently constructs all seven nonempty
labelled portal subsets for unequal rational `Q=3,T=2` data, checks every
first-step row balance and PGF normalization, and verifies (8)--(11) against
the raw incidence rates.

## 5. Search outcome and remaining scope

At `r=31/20`, direct optimization of the full exact establishment trace gave
no simultaneous candidate.  Representative best minimum gaps were about
`-0.03232544` for `Q=2,T=2` and `-0.03209860` for `Q=3,T=2`.  A relaxed
search optimizing row marks and prospective-parent weights directly also
found positive affine-separation margins (about `0.6182` for `Q=2` and
`0.6030` for `Q=3`).  These numbers are **NUMERICAL OBSERVATIONS ONLY**;
they are not global optimality claims and do not enter the theorem.

**PROVED:** the full labelled fixed-`Q,T` direct-portal trace; the strict
two-portal, one-type separator (23) for every `r in [3/2,2]`; and the
resulting fixed-class obstruction for every `r>=3/2`.

**EXACTLY COMPUTED:** the two three-state episode resolvents and the fixed
11-box rational Bernstein certificate.

**NUMERICALLY OBSERVED:** no higher-rank direct-portal candidate at or near
`r=31/20` in the searches recorded here.

**OPEN:** `Q>=3` direct networks, genuinely higher-rank incidence with
direct edges, growing portal count or incidence rank, singular parameter
scales, and the universal graph problem.  This class theorem does not prove
`R_sim=3/2`.
