# Singleton Kac-cycle form of the exact minimal product

Date: 2026-08-13 (America/Los_Angeles)

No external communication, graph enumeration, or kernel search was used.

## Status

**EXACT REFORMULATION AND SCOPED PATH-SPACE OBSTRUCTION.**  This note does
not prove the universal minimal stationary product `(MP)`.  It rewrites the
already proved one-/two-root portal criterion entirely in Kac return-cycle
variables.  On the active branch, every stationary normalizer and both
global density excesses cancel.  The exact diagonal target becomes

\[
 r^3\psi_{B,i}\psi_{D,i}\le1,                        \tag{D-KAC}
\]

where `psi_U,i` is the expected signed excess reward in one return cycle to
singleton `i`, measured per unit initial holding time.  The pair target is
an explicit two-by-two copositivity inequality in the reciprocals of the
four Kac rewards.

The note then audits the canonical time-reversal/Hellinger route.  Three
exact facts block that route as usually formulated.

1. The unexpanded Bd and dB return-cycle laws have singular macro-path
   support already on a weighted three-path.
2. Expanding a dB burst into target-locked arrow histories restores local
   support, but leaves a repeated-source likelihood factor which is not an
   endpoint coboundary even on a closed singleton return cycle.
3. The cycle reward is pathwise signed at `R_hyb`, while scalar Hellinger
   also retains only the geometric mean of the two root assignments and
   drops the exact orientation square.

This refutes only the canonical positive scalar Hellinger/time-reversal
composition.  An assignment-valued, multiplicity-labelled Feynman--Kac or
path transport could still prove the theorem.  That full-cycle inequality
remains open.

## 1. Kac return cycles at a singleton

Let `Q` be the row generator of a finite irreducible continuous-time Markov
chain on `Omega`, let `i` be a distinguished state, and put

\[
 q_i=-Q(i,i)>0,qquad R_i=\Omega\setminus\{i\},
 \qquad G_i=(-Q_{R_iR_i})^{-1}\ge0.                  \tag{1}
\]

Start the chain at `i`.  Let `sigma_i` be its first departure time and let
`theta_i` be the first return time to `i` after that departure.  For a
column reward `g`, define the expected cycle time and signed cycle reward

\[
 \mathscr T_i=\mathbb E_i\theta_i,
 \qquad
 \mathscr R_i=\mathbb E_i\int_0^{\theta_i}g(A_t)\,dt. \tag{2}
\]

The initial holding time has mean `1/q_i`, the departure law is
`Q(i,R_i)/q_i`, and `G_i` is the killed occupation kernel before return.
Therefore

\[
 q_i\mathscr T_i
 =1+Q(i,R_i)G_i\mathbf1=: \vartheta_i,               \tag{3}
\]

and

\[
 \boxed{
 q_i\mathscr R_i
 =g(i)+Q(i,R_i)G_ig_{R_i}=:\psi_i.}                  \tag{4}
\]

Thus `psi_i` is precisely the one-root Schur reward.  Regeneration at
successive entrances to `i` gives the Kac identities

\[
 \boxed{
 \pi(i)=\frac1{q_i\mathscr T_i}=\frac1{\vartheta_i},
 \qquad
 \pi\mathbin\cdot g=\frac{\mathscr R_i}{\mathscr T_i}
 =\pi(i)\psi_i.}                                    \tag{5}
\]

The second equality is valid for every root `i`, although the cycle law and
the two quantities in (2) depend on `i`.

## 2. Exact cancellation of the global excesses

Apply Section 1 to the exact recurrent Bd and dB duals.  Use the density
excess reward

\[
 g(A)=\frac{|A|}{s}-p,qquad p=1-\frac1r,            \tag{6}
\]

and write

\[
 \beta_B=\rho_{Bd}-p,qquad \beta_D=\rho_{dB}-p.    \tag{7}
\]

Let `u_i` and `v_i` be the Bd and dB stationary singleton atoms.  Equation
(5) gives, root by root,

\[
 \beta_B=u_i\psi_{B,i},qquad
 \beta_D=v_i\psi_{D,i}.                             \tag{8}
\]

If either beta is nonpositive, the positive-part right side of `(MP)` is
zero and `(MP)` is automatic.  On the active branch
`beta_B,beta_D>0`, every Kac reward in (8) is strictly positive and

\[
 u_i=\frac{\beta_B}{\psi_{B,i}},qquad
 v_i=\frac{\beta_D}{\psi_{D,i}}.                    \tag{9}
\]

For a physical portal load `x>=0`, put `e_i=1/d_i` and

\[
 \gamma_i=\frac{x_i}{x\mathbin\cdot\mathbf1},
 \qquad
 \alpha_i=\frac{e_ix_i}{x\mathbin\cdot e}.          \tag{10}
\]

The two portal fixation contributions are

\[
 q_B^\gamma
 =\beta_B\frac{x\mathbin\cdot\psi_B^{-1}}
                    {x\mathbin\cdot\mathbf1},
 \qquad
 q_D^\alpha
 =\beta_D\frac{x\mathbin\cdot(e\psi_D^{-1})}
                    {x\mathbin\cdot e}.             \tag{11}
\]

Cancel the positive product `beta_B beta_D`.  The exact all-portal minimal
product is now

\[
 \boxed{
 (x\mathbin\cdot\psi_B^{-1})
 (x\mathbin\cdot(e\psi_D^{-1}))
 \ge r^3(x\mathbin\cdot\mathbf1)(x\mathbin\cdot e)
 \quad\hbox{for every }x\ge0.}                      \tag{KMP}
\]

This is not a sufficient strengthening: on the active branch `(KMP)` is
exactly `(MP)`.  It is the orientation-preserving portal product with

\[
 U_i=\psi_{B,i}^{-1},\qquad
 V_i=\psi_{D,i}^{-1},\qquad Q=r^3.                  \tag{12}
\]

The global signed means have disappeared, but their cancellation has not
made the pathwise rewards positive.  Each `psi` is still the expectation
of the signed integral in (2)--(4).

## 3. Exact diagonal, pair, and minimax forms

For each root define

\[
 \boxed{
 d_i=e_i\left(\frac1{\psi_{B,i}\psi_{D,i}}-r^3\right),}       \tag{13}
\]

and for `i!=j` define

\[
 \boxed{
 k_{ij}
 ={e_j\over\psi_{B,i}\psi_{D,j}}
 +{e_i\over\psi_{B,j}\psi_{D,i}}
 -r^3(e_i+e_j).}                                     \tag{14}
\]

The support-two theorem proved in
`../rhyb_mp_orientation_minimax/ORIENTATION_PRESERVING_PORTAL_MINIMAX.md`
applied to (12) gives the exact Kac criterion

\[
 \boxed{
 d_i\ge0\quad(i\in V),\qquad
 k_{ij}+2\sqrt{d_id_j}\ge0\quad(i\ne j).}           \tag{15}
\]

The factor `2` corresponds to the convention in which `k_ij` is the full
coefficient of `x_i x_j`.  In particular, the diagonal condition is
exactly `(D-KAC)`.

The exit rates at a singleton are explicit.  If

\[
 t_i=\sum_uP_{ui},                                   \tag{16}
\]

then the loopless Bd singleton has neutral exit rate `t_i` and selective
exit rate `(r-1)t_i`, while the loopless dB singleton rings at rate one and
always changes state.  Hence

\[
 q_{B,i}=rt_i,qquad q_{D,i}=1.                      \tag{17}
\]

In the raw expected cycle rewards from (2), `(D-KAC)` is therefore

\[
 \boxed{
 r^4t_i\mathscr R_{B,i}\mathscr R_{D,i}\le1}        \tag{18}
\]

on the active branch.  Although both expectations in (18) are positive,
the random integrals being averaged need not be.

There is also an exact hyperbolic pair form.  Put

\[
 H_i={1\over r^3\psi_{B,i}\psi_{D,i}},
 \quad
 \delta_{ij}={1\over2}\log
 {e_j\psi_{B,j}\psi_{D,i}\over
  e_i\psi_{B,i}\psi_{D,j}},
 \quad
 \epsilon_{ij}={1\over2}\log{e_i\over e_j}.        \tag{19}
\]

Then (15) on `{i,j}` is

\[
 \boxed{
 \sqrt{H_iH_j}\cosh\delta_{ij}
 +\sqrt{(H_i-1)(H_j-1)}
 \ge\cosh\epsilon_{ij}.}                            \tag{20}
\]

The same exact portal minimax says that `(KMP)` holds if and only if, for
every `lambda>0`, there exists `t>0` such that

\[
 \boxed{
 {\lambda\over\psi_{B,i}}
 +{\lambda^{-1}e_i\over\psi_{D,i}}
 \ge r^{3/2}(t+e_i/t)
 \quad\hbox{for every }i.}                           \tag{21}
\]

The two scalars are global; choosing either separately at each root would
drop the orientation term.

## 4. Compatibility with a literal two-root Schur trace

The Kac form also explains the cancellation in a literal two-source trace.
Eliminate every state except singleton roots `{i,j}`.  For Bd write its
trace generator and reward as

\[
 T_B=\begin{pmatrix}-a&a\\ b&-b\end{pmatrix},
 \qquad \phi_B=(\phi_{B,i},\phi_{B,j})^T,            \tag{22}
\]

and for dB write

\[
 T_D=\begin{pmatrix}-c&c\\ d&-d\end{pmatrix},
 \qquad \phi_D=(\phi_{D,i},\phi_{D,j})^T.            \tag{23}
\]

All four off-diagonal rates are positive.  Trace stationarity gives
`u_i/u_j=b/a` and `v_i/v_j=d/c`.  Combining this with (8) gives

\[
 \begin{array}{ll}
 \displaystyle
 \psi_{B,i}={Y_B\over b},&
 \displaystyle\psi_{B,j}={Y_B\over a},\\[2mm]
 \displaystyle
 \psi_{D,i}={Y_D\over d},&
 \displaystyle\psi_{D,j}={Y_D\over c},
 \end{array}                                         \tag{24}
\]

where

\[
 Y_B=b\phi_{B,i}+a\phi_{B,j},
 \qquad
 Y_D=d\phi_{D,i}+c\phi_{D,j}.                       \tag{25}
\]

On the active branch `Y_B,Y_D>0`.  Multiplying the pair polynomial from
(13)--(14) by the positive product `Y_BY_D` gives diagonals

\[
 e_i\{bd-\widehat Q\},qquad
 e_j\{ac-\widehat Q\},                              \tag{26}
\]

and cross coefficient

\[
 e_jbc+e_iad-\widehat Q(e_i+e_j),qquad
 \widehat Q=r^3Y_BY_D.                               \tag{27}
\]

Thus the literal two-root Green/Schur criterion and the singleton Kac
criterion are the same quadratic after one positive scaling.  Each
two-state trace is reversible by itself.  The open content is not that
time reversal: it is the cross-rule comparison of the four trace rates
with the two signed Green rewards in (25).

## 5. Macro return-cycle laws are singular

Consider the weighted three-path

\[
 u\mathbin{-}^{a}v\mathbin{-}^{b}w,
 \qquad a,b>0,                                       \tag{28}
\]

and start a return cycle at singleton `{v}`.  Put

\[
 z=P_{vu}={a\over a+b}\in(0,1).                     \tag{29}
\]

At its first dB event, `v` is removed and replaced by the union of a
geometric number of row-`P_v` samples.  If

\[
 g_r(z)={z\over r-(r-1)z},                           \tag{30}
\]

then the exact probability that the sampled union is both leaves is

\[
\begin{split}
 \chi_r(z)
 &=1-g_r(z)-g_r(1-z)\\
 &={ (r^2-1)z(1-z)\over
     \{r-(r-1)z\}\{1+(r-1)z\}}>0.                  \tag{31}
\end{split}
\]

Consequently

\[
 Q_D(\{v\},\{u,w\})=\chi_r(z)>0.                    \tag{32}
\]

A Bd arrow from singleton `{v}` either replaces `v` by one source or
retains `v` and adds one source.  Hence

\[
 Q_B(\{v\},\{u,w\})=0.                              \tag{33}
\]

More importantly for time reversal, a single Bd arrow from `{u,w}` cannot
remove both leaves and land at `{v}`.  Therefore

\[
 Q_B(\{u,w\},\{v\})=0,\qquad
 Q_B^*(\{v\},\{u,w\})
 ={\pi_B(\{u,w\})\over\pi_B(\{v\})}
   Q_B(\{u,w\},\{v\})=0,                             \tag{34}
\]

where `Q_B^*` is the stationary time reverse.  The dB `{v}`-return-cycle
law gives positive mass to cycles whose first jump is (32) and which later
return to `{v}`; the reversed Bd return-cycle law gives that event zero
mass.  Thus the two macro-cycle laws are not mutually absolutely
continuous.  A direct path-space Hellinger affinity assigns no paired
overlap to this singular sector, so it would require a separate
singular-mass reward estimate.

The singular sector is reward-relevant.  At `r=R_hyb` one has
`3/2<r<2`, and on this order-three module

\[
 g(\{v\})={1\over3}-p<0,
 \qquad
 g(\{u,w\})={2\over3}-p>0.                           \tag{35}
\]

Conditional on (32), the holding time at `{u,w}` has an unbounded
exponential tail, and a positive-probability sequence returns to `{v}`.
After also restricting the singleton holding times to be short, the
singular event carries arbitrarily large positive cycle reward.  It cannot
be removed from a proof of (18).

## 6. Arrow expansion does not create a cycle coboundary

One can restore common local support by expanding a dB burst into a
target-locked history: a geometric sequence of row samples, interpreted as
selective samples followed by the neutral sample.  The exact obstruction
then moves from support to likelihood.

For retained target `v`, the reversed-arrow source law `C` and the
Bd-oriented source law `L` are

\[
 p_v^C(x)={w_{xv}\over d_v},
 \qquad
 p_v^L(x)={{w_{xv}/d_x}\over t_v},
 \qquad
 t_v=\sum_y{w_{yv}\over d_y}.                        \tag{36}
\]

With `c_v=d_v/t_v`, one sample has exact likelihood ratio

\[
 {p_v^L(x)\over p_v^C(x)}={c_v\over d_x}.            \tag{37}
\]

For a history of `n` samples `x_1,...,x_n`, the common geometric factor
cancels and

\[
 {W_L\over W_C}={c_v^n\over\prod_{ell=1}^n d_{x_ell}}.          \tag{38}
\]

If `B` is the set of distinct sampled sources and `n_x` their
multiplicities, removing the natural endpoint degree potential leaves

\[
 \boxed{
 {W_L/W_C\over D(\{v\})/D(B)}
 ={1\over t_v}c_v^{n-1}
   \prod_{x\in B}d_x^{1-n_x},
 \qquad D(A)=\prod_{x\in A}d_x.}                    \tag{39}
\]

The repeated-source factor in (39) survives closure of the path.  On (28),

\[
 d_u=a,qquad d_w=b,qquad d_v=a+b,qquad
 t_v=2,qquad c_v={a+b\over2}.                       \tag{40}
\]

An all-`u` history of length `n` has the same projected macroedge
`{v}->{u}` for every `n`, but its likelihood ratio is

\[
 \left({a+b\over2a}\right)^n.                       \tag{41}
\]

Append the deterministic-source leaf event `{u}->{v}`.  It has likelihood
ratio one under the two source laws, so (41) is also the ratio of a closed
expanded return cycle with projected macro path
`{v}->{u}->{v}`.  The cases `n=1` and `n=2` have the same projected closed
cycle and the same physical reward law but different ratios whenever
`a!=b`.  A state endpoint potential telescopes to one on both cycles and
therefore cannot represent these ratios.  Comparing all-`u` and all-`w`
histories at the same length also rules out a clock depending only on the
retained target and history length.

Thus closing at a Kac root does not repair the non-telescoping collision
factor.  This refutes endpoint-diagonal time reversal after the canonical
target-locked expansion.  It does not refute a global regrouping which
keeps every source multiplicity as part of the path state.

## 7. Signed reward and scalar-orientation obstructions

There are two further losses in a standard scalar Hellinger step.

First, let `Y_U(omega)` be the signed integral in (2), and consider the
formally reward-weighted cycle measure

\[
 d\Xi_{U,i}(\omega)=q_{U,i}Y_U(\omega)\,
                     d\mathbb P_{U,i}(\omega).       \tag{42}
\]

Its total mass is `psi_U,i`, but it is a signed measure.  On the three-path
at `R_hyb`, a short cycle using only singleton states has negative reward by
(35), while a cycle which holds sufficiently long in a doubleton has
positive reward.  Both events have positive probability for both duals.
Hence `Xi_U,i` has a nontrivial positive and negative part.  On an active
instance its total mass is nevertheless positive.  Standard Hellinger
affinity applies to positive measures.  Replacing `Xi` by its positive part
or total variation deletes the Kac cancellation and asks a strictly
stronger question.

Second, put

\[
 A_i={1\over\psi_{B,i}},qquad
 C_i={e_i\over\psi_{D,i}}.                           \tag{43}
\]

The two swapped root assignments in (14) obey the exact identity

\[
 A_iC_j+A_jC_i
 =2\sqrt{A_iC_jA_jC_i}
  +(\sqrt{A_iC_j}-\sqrt{A_jC_i})^2.                 \tag{44}
\]

A scalar Hellinger pairing returns only the geometric term in (44).  The
last square is precisely the root-orientation repayment retained by the
exact pair condition (15) and the `cosh(delta_ij)` factor in (20).  Dropping
it gives the stronger root-Hellinger problem, not `(MP)`.

Combining Sections 5--7, a surviving path proof must simultaneously:

1. expand and retain the hidden dB source multiplicities;
2. transport a signed Feynman--Kac derivative rather than a positive reward
   mass; and
3. be two-component or assignment-valued so that (44) is not replaced by
   its geometric mean.

No such inequality is proved here.  The canonical macro Hellinger,
endpoint-coboundary micro reversal, and scalar reward-weighted Hellinger
routes stop at the exact obstructions above.

## 8. Exact remaining path theorem

The unresolved result can now be stated without stationary normalization.
For every module and every singleton pair at `r=R_hyb`, prove (13)--(15)
for the four signed Kac return rewards.  Equivalently, prove the literal
two-root Schur inequalities (26)--(27).  Any path-space proof must retain
the multiplicity, sign, and assignment information listed above.

This is an exact reformulation of universal `(MP)`, not evidence that its
sign is false.  The obstruction is scoped to canonical scalar positive
time reversal/Hellinger; an assignment-valued full-cycle inequality remains
open.

## 9. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_kac_cycle_mp/verify_kac_cycle_mp.py
```

The replay independently verifies Kac/Green normalization on an exact
finite generator, cancellation to `(KMP)`, the pair coefficients, the
literal two-root scaling, the exact macro singular mass (31), and the
non-coboundary micro-history ratios (38)--(41).  It checks algebraic
identities only and performs no graph enumeration.
