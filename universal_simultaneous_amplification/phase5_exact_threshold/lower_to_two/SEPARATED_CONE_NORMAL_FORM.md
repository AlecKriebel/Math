# Separated module-response cone and its exact dual

Date: 2026-08-08 (America/Los_Angeles)

## 1. Complete fixed-gadget separated normal form

Fix `r>1` and a connected weighted gadget `H` of order `s`, with internal
weighted degrees `d_i` and positive portal loads `x_i`.  Let
`h_U^+(i)` and `h_U^-(i)` be its isolated fixation probabilities from
singleton `i` at fitness `r` and `1/r`.  Define

\[
 A_U={1\over s}\sum_i h_U^+(i),
 \quad
 S_0=\sum_i{x_i\over d_i},
 \quad
 S_B^-=\sum_i x_i h_B^-(i),
 \quad
 S_D^-=\sum_i{x_i h_D^-(i)\over d_i},
 \quad P=\sum_i x_i.
\]

If the internal physical weights have scale `C/a`, direct summation of the
rare cross events gives

\[
 Z_B={a(r-1)S_0\over S_B^-},
 \qquad
 Z_D={r(r-1)P\over aS_D^-}.                             \tag{1}
\]

Hence

\[
 K_H(r):=Z_BZ_D
 ={r(r-1)^2S_0P\over S_B^-S_D^-}                       \tag{2}
\]

is independent of the free internal scale.  Writing `z=Z_B`, the complete
response is

\[
 \boxed{
 v_H(r;z)=s\left(
 {A_Bz\over p(1+z)}-1,
 {A_DK_H\over p(K_H+z)}-1
 \right),\quad z>0,}                                  \tag{3}
\]

where `p=1-1/r`.  Formula (3) includes local fixation, reciprocal invasion,
the gate to the large core, the post-gate sweep, uniform initialization, and
the subtraction of the `s` core vertices being replaced.

**Normal-form theorem.**  Equation (3) is the unique first-order response of
every fixed-order dilute module satisfying all of the following hypotheses:

1. the core is asymptotically complete and has diverging order;
2. module count is `o(C)`;
3. modules do not interact at the response scale;
4. before the next cross event, the affected module or core locally absorbs;
5. after a successful core gate, the remaining dilute modules are swept with
   probability `1-o(1)` uniformly on compact fitness intervals.

The proof is the finite Schur trace: every successful macro transition is
one introduction, exact local absorption, and either fixation or reciprocal
recovery.  Conditions 1--5 leave only the four sums in (1), so no further
fixed-gadget response coordinate is available.  The theorem is a complete
normal form for its stated separated architecture; it is not a claim that
arbitrary graph families satisfy those hypotheses.

## 2. Scalar optimization at a fixed fitness

Put

\[
 a_B={A_B\over p},\qquad a_D={A_D\over p}.
\]

The leaf-eliminated separator per module vertex is

\[
 \Psi_H(r;z)=
 {a_DK_H\over K_H+z}
 +(r-1){a_Bz\over1+z}-r.                              \tag{4}
\]

After multiplying by the positive denominator `(1+z)(K_H+z)`, its sign is
the sign of the explicit quadratic

\[
 \begin{aligned}
 N_H(z)={}&\{(r-1)a_B-r\}z^2\\
 &+\{K_H((r-1)a_B+a_D)-r(K_H+1)\}z\\
 &+K_H(a_D-r).                                        \tag{5}
 \end{aligned}
\]

Thus every exact finite-gadget screen reduces to four isolated harmonic
sums followed by a one-variable quadratic sign test.  No numerical gate
optimization is needed.

An ordinary leaf has response

\[
 \ell(r)=(1/(r-1),-1)
\]

and satisfies `D+(r-1)B=0`.  For a mixture `w` of non-leaf modules, some
nonnegative number of ordinary leaves makes both coordinates positive at a
fixed `r` exactly when

\[
 D_w(r)>0,
 \qquad D_w(r)+(r-1)B_w(r)>0.                          \tag{6}
\]

This is often more stable than balancing the two original coordinates.

## 3. The interval cone

Let `I` be compact in `(1,infinity)`, and let `mathcal H` be a finite menu of
exact response functions.  In the Banach space

\[
 X_I=C(I)\times C(I),
\]

define

\[
\mathcal C_I=\left\{\sum_{H\in\mathcal H}c_Hv_H:
 c_H\ge0\right\}.                                    \tag{7}
\]

Strict interval amplification is the feasibility problem

\[
 \exists c_H\ge0,\ \exists\gamma>0:
 \quad
 \sum_Hc_HB_H(r)\ge\gamma,
 \quad
 \sum_Hc_HD_H(r)\ge\gamma
 \quad(r\in I).                                       \tag{8}
\]

The exact dual alternative is a pair of finite nonnegative Borel measures
`(mu_B,mu_D)`, not both zero, such that

\[
 \int_I B_H\,d\mu_B+\int_I D_H\,d\mu_D\le0
 \qquad(H\in\mathcal H).                              \tag{9}
\]

Indeed, the span of a finite menu is finite dimensional.  Separating its
closed conic hull from the open positive cone and applying the Riesz
representation theorem gives (9); conversely (9) contradicts (8) after
integration.  Atomic rational measures give finite exact LP certificates.
Polynomial or rational response functions allow the remaining interval
signs to be discharged by Sturm or Bernstein certificates.

For an infinite admissible menu, the same statement applies to the closure
of its response cone whenever that cone is closed in `X_I`.  Without a
compactness theorem for gadgets, closure is a genuine proof obligation and
must not be assumed.

## 4. Growing menus and one fitness-independent diagonal

Set

\[
 I_k=[1+1/k,2-1/k],\qquad k\ge3.
\]

Suppose that for every `k` a finite menu and rational nonnegative density
vector produce a certified margin `gamma_k>0` on `I_k`, and the associated
finite separated traces have compact-uniform error moduli.  Choose the core
size, module counts, and positive weak completion weights at stage `k` so
that every response error is below `gamma_k/3` at the actual dilute scale.
All choices are made using `k` only.  Then, for a fixed `1<r<2`, every
sufficiently large stage has `r in I_k` and both finite-graph gains are
strictly positive.  This constructs one fitness-independent diagonal and
proves `R_sim>=2`.

Consequently a growing menu is a logically valid route to two.  What is
missing is not diagonalization but a generator with a positive exact margin
near two.

## 5. What the recovered cone says now

The checked library contains ordinary and weighted leaves, all clique
satellites, the optimized pair--leaf hybrid, general invariant separated
gadgets, strong integrated gadgets, portal clones, and symmetric pair
doublets.  The currently certified positive combination reaches `R_hyb`;
none of the named, exactly audited extensions has produced a certified
combination beyond it.  This is not a completeness theorem for all weighted
gadgets.

The new second-order theorem closes the portal-clone boundary for every
fixed order: its first nonzero dB motion is negative definite.  Therefore a
route to two must now exploit an interior positive-internal gadget, a
growing order for which the remainder is not uniform, inter-module
correlation, or genuinely nonseparated dynamics.
