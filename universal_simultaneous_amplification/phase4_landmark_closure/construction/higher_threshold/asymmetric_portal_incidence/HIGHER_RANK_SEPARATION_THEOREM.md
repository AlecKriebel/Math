# A fixed-finite-rank separation theorem without direct portal edges

Date: 2026-08-02 (America/Los_Angeles)

Status: **PROVED for every fixed finite incidence rank and fixed positive
trace data when direct portal edges are absent.  Growing or singular rank
and the direct portal-network case remain OPEN.**

No literature search or external contact was used.  The proof begins with
the atomic labelled trace and uses an exact rational Bernstein certificate.
Numerical searches are reported separately and play no role in the proof.

## 1. The class and the theorem

For every size parameter `s`, take `s` disjoint unit-weight blade edges and
`Q` portal vertices.  Fix `Q,T>=1` independently of `s`, and let the number
`s_t` of type-`t` blades satisfy

\[
 \sum_t s_t=s,\qquad {s_t\over s}\longrightarrow\pi_t>0,
 \qquad\sum_t\pi_t=1.
\]

Fix every finite incidence `lambda_at>0`, independently of `s`, and join
both endpoints of a type-`t` blade to portal `a` with weight

\[
 w(o_a,x_i)=w(o_a,y_i)={\lambda_{at}\over s}
 \quad\hbox{for a type-\(t\) blade}.                    \tag{1}
\]

There are no portal--portal edges and no edges between distinct blades.  No
rank restriction is imposed on the fixed `Q by T` incidence matrix.  The
graph is connected because every blade type is incident to every portal.
Put

\[
 B_a=2\sum_t\pi_t\lambda_{at},\qquad
 f_{at}={2\pi_t\lambda_{at}\over B_a}.                 \tag{2}
\]

Thus every row of `f` is a probability vector.  Define

\[
 c_t=\sum_a f_{at},\qquad
 \ell_t=\sum_a B_af_{at}.                              \tag{3}
\]

Let `alpha_B,alpha_D` be the exact limiting branching-establishment bounds
of the stopped clean-blade trace.  As in the inherited derivation,
fixation is bounded above by establishment; no claim that establishment
implies fixation is used.

**Theorem (fixed finite rank, no direct portal edges).**  For every fixed
`Q,T`, every fixed positive data set `(pi,lambda)`, and every fixed
`3/2<=r<=2`,

\[
 \alpha_B+\alpha_D<2\left(1-{1\over r}\right).          \tag{4}
\]

For `r>=2`, dB alone has entrance factor `1/2<=p`, with strict inequality
after its positive extinction probability is included.  Consequently, for
every `r>=3/2`, the two establishment bounds cannot both exceed the
large-complete-graph limit `p=1-1/r`.  In particular, assigning different
blade types to the locally Bd-favorable and dB-favorable portal-load
regimes cannot break the `3/2` barrier in this full higher-rank class.

The proof gives the stronger typewise inequality

\[
 {r\over r+1}x^B_t+{1\over2}x^D_t<2p,                 \tag{5}
\]

where `x^U_t` is the survival probability of the limiting multitype trace
begun from a clean type-`t` mutant blade.  Averaging (5) with weights
`pi_t` gives (4).

For fixed trace data and fixed `r`, (4) has a positive gap.  Hence at least
one rule has
`alpha_U<p-delta` for some `delta>0`.  The stopped-trace upper bound and
the convergence of the complete-graph baseline to `p` imply that the
corresponding finite graph family is eventually strictly suppressing for
that rule.  Thus this is a genuine asymptotic class no-go, not merely a
failure of strictness at the limiting comparison point.  The suppressing
rule may depend on the fixed data and on `r`.

For `r>2`, (4) is not claimed or needed.  The substantive range below is
therefore `3/2<=r<2`, with `r=2` included by continuity and by the exact
certificate.

## 2. Exact survival maps

For a prospective descendant-survival vector
`s=(s_1,...,s_T) in [0,1]^T`, write

\[
 m_a=\sum_t f_{at}s_t,
 \qquad C={r^2\over r+1},\qquad D={r\over2}.            \tag{6}
\]

With no direct portal edges, an episode contains only its initially
mutant portal.  Direct substitution in the atomic rates gives

\[
 H^B_a(s)={C m_a\over B_a+C m_a},\qquad
 H^D_a(s)={D B_a m_a\over1+D B_a m_a},                 \tag{7}
\]

where `H` is one minus the marked-child PGF of the episode.  Combining
these with the exact parent seeding and death rates gives survival maps

\[
 S^B_t(s)={R^B_t(s)\over1+R^B_t(s)},\qquad
 R^B_t(s)={r^3\over c_t}\sum_a f_{at}
 {B_a m_a\over B_a+C m_a},                             \tag{8}
\]

\[
 S^D_t(s)={R^D_t(s)\over1+R^D_t(s)},\qquad
 R^D_t(s)={r^3\over\ell_t}\sum_a f_{at}
 {B_a m_a\over1+D B_a m_a}.                            \tag{9}
\]

These are exact, not mean-offspring approximations.  The survival vectors
`x^B,x^D` are the largest fixed points of the corresponding maps.

For example, the Bd parent death rate is

\[
 {c_t\over (r+1)\pi_t s},
\]

and seeding portal `a` has rate `rB_af_at/(pi_t s)`.  Multiplication by
the first expression in (7) produces the factor
`r(r+1)C=r^3` in (8).  The dB calculation similarly uses
`2r^2D=r^3`.  The independent verifier also solves the complete
seven-state labelled portal system at `Q=3,T=2` with exact rational data
and checks (7)--(9).

## 3. The affine separation map

For `3/2<=r<=2`, put

\[
 A={4(r-1)\over r},\qquad k={2r\over r+1},\qquad
 J_r(s)_t=\min\{1,A-ks_t\}.                            \tag{10}
\]

Here `A-k=2(r^2-2)/(r(r+1))>0`, so every coordinate of `J_r(s)` is
positive on the stated fitness range.  The dB portal response in (9) is
strictly increasing in each row mark; this will be used after clipping.

The central result is the map inequality

\[
 S^D(J_r(s))<J_r(S^B(s))
 \quad\hbox{coordinatewise for every }s\in[0,1]^T.     \tag{11}
\]

To see the reduction, fix a parent type `t` and set

\[
 x=S^B_t(s),\qquad X={x\over1-x}.
\]

Equation (8) says

\[
 r^3\sum_a f_{at}{B_am_a\over B_a+C m_a}=c_tX.         \tag{12}
\]

Because the affine part of `J_r` commutes with row averaging and clipping
can only decrease it, the dB row mark `n_a` satisfies

\[
 n_a=\sum_jf_{aj}J_r(s)_j
 \le \min\{1,A-km_a\}.                                 \tag{13}
\]

Also the first fraction in (8) is strictly below one for finite positive
`B_a`, so

\[
 x<x_{\max}:={r^3\over1+r^3}.                          \tag{14}
\]

If `x<=m_0`, where

\[
 m_0={A-1\over k}={(3r-4)(r+1)\over2r^2},              \tag{15}
\]

then `J_r(x)=1` and (11) is immediate.  Otherwise set
`y=A-kx<1` and `Y=y/(1-y)`.  The scalar lemma in Section 4 gives, for
each portal,

\[
 r^3\left\{
 {B_am_a\over B_a+C m_a}
 +{B_an_a\over1+D B_an_a}
 \right\}
 \le X+B_aY.                                           \tag{16}
\]

Multiplying (16) by `f_at`, summing over `a`, and using (12) cancels the
entire Bd contribution:

\[
 r^3\sum_a f_{at}{B_an_a\over1+D B_an_a}
 <\ell_tY.                                              \tag{17}
\]

Equations (9) and (17) are exactly
`S^D_t(J_r(s))<y`, proving (11).

Now take `s=x^B`.  Then `y=J_r(x^B)` is a supersolution of the dB survival
map.  The elementary branching comparison is included for completeness.
Every survival map is monotone and radially concave:

\[
 S(\theta z)\ge\theta S(z),\qquad0\le\theta\le1.       \tag{18}
\]

Indeed, conditional on the offspring vector, the left side is the
probability that at least one potentially surviving child remains after
independent thinning by `theta`; this is a concave function of `theta`.
If the largest fixed point `x^D` exceeded the positive supersolution `y`
in any coordinate, choose
`theta=1/max_t(x^D_t/y_t)<1`.  Then `theta x^D<=y`, with equality in at
least one coordinate, while monotonicity and (18) give

\[
 \theta x^D=\theta S^D(x^D)
 \le S^D(\theta x^D)\le S^D(y)<y,                     \tag{19}
\]

contradicting equality in the touching coordinate.  (The subcritical case
is immediate.)  Hence

\[
 x^D_t<A-kx^B_t.                                       \tag{20}
\]

Strictness in (11) follows because, when its target coordinate is one, a
parent still has a positive extinction probability; otherwise the scalar
certificate is strictly positive on the physical domain.  Finally
`k/2=r/(r+1)` and `A/2=2p`, so (20) is precisely (5).

## 4. Exact scalar lemma

**Lemma.**  Let `3/2<=r<=2`, `m_0<x<x_max`, `0<=m<=1`, and `B>0`.
Set

\[
 y=A-kx,\qquad n=\min\{1,A-km\},\qquad
 X={x\over1-x},\qquad Y={y\over1-y}.                  \tag{21}
\]

Then

\[
 r^3\left\{{Bm\over B+Cm}+{Bn\over1+DBn}\right\}
 \le X+BY.                                             \tag{22}
\]

This is the only polynomial sign statement in the proof.  It has a short
exact Bernstein certificate.  Split at `m=m_0` and make the substitutions

\[
 r={3+a\over2},\quad
 x=m_0+(x_{\max}-m_0)u,\quad
 B={b\over1-b},                                        \tag{23}
\]

with `a,u,b in [0,1]`.  In the low-mark case put `m=m_0v,n=1`; in the
high-mark case put

\[
 m=m_0+(1-m_0)v,\qquad n=A-km,                         \tag{24}
\]

where `v in [0,1]`.  After multiplying (22) by

\[
 (1-x)(1-y)(B+Cm)(1+DBn)>0,                            \tag{25}
\]

and clearing the manifestly positive substitution denominators, the two
numerators have multidegrees

\[
 (14,2,1,3),\qquad(16,2,2,3)                           \tag{26}

\]

in `(a,u,v,b)`.  Exact de Casteljau subdivision produces respectively 6
and 11 boxes, of maximum depths 3 and 6.  Every Bernstein coefficient on
every terminal box is a nonnegative rational number.  The verifier also
checks every terminal-box face meeting the physical domain `0<u,b<1`;
each such face has an active positive coefficient.  Thus (22) is strict
on the stated physical domain.  The fixed subdivision
paths and all exact coefficients are regenerated and checked by
`verify_higher_rank_separation.py`; no floating-point interval decision
is present.

The small certificate is structural: the apparent high-degree sign
problem is only the combination of two harmonic portal-response terms,
and the single split `m<=m_0` versus `m>=m_0` resolves the clipping in
`n=min(1,A-km)`.

## 5. Scope and unresolved gap

**PROVED.**  Every fixed finite incidence rank, with fixed unequal positive
portal loads and fixed positive limiting blade-type proportions, cannot beat
the simultaneous `3/2` establishment barrier when direct portal edges are
absent.  The portal proportion vanishes, while every admitted blade class
grows linearly with `s`.

**EXACTLY COMPUTED.**  The two Bernstein covers and the independent
`Q=3,T=2` labelled-chain audit pass exactly.

**NUMERICALLY OBSERVED.**  Full labelled searches with direct portal
edges found no positive simultaneous gap.  A two-class exact count lumping
was independently checked against the labelled chain, and its growing
portal-class boundary process also found no hit.  At `r=8/5`, the best
growing two-class search value found in this run was

\[
 \min(\alpha_B-p,\alpha_D-p)\approx-0.02667812.         \tag{27}
\]

This number is discovery evidence only and is not an optimality claim.

**NOT COVERED.**  Growing `Q` or `T`, vanishing blade proportions, zero or
`s`-dependent incidences, a portal--blade scale other than `1/s` relative to
the unit blade edge, and positive-proportion portal populations.  The fixed
strict gap is not claimed uniformly along any such singular sequence.

**OPEN.**  Direct portal edges make an episode visit several portal
identities.  The row mark is then propagated through a nonlinear
portal-subset resolvent, so the scalar harmonic-response lemma above no
longer applies directly.  The exact candidate statement is nevertheless
unchanged: if `S^{B,h},S^{D,h}` denote the full labelled-subset survival
maps, prove or refute

\[
 S^{D,h}(J_r(s))<J_r(S^{B,h}(s))                    \tag{28}
\]

coordinatewise.  This resolvent separation survived random tests through
`Q=4,T=3` and global optimization at `Q=T=2`, but that is only
**NUMERICALLY OBSERVED**.  Proving (28), or finding a counterexample in a
genuinely higher-rank growing portal network, remains the exact gap.  This
theorem therefore does not resolve the main asymptotically universal
amplification question.
