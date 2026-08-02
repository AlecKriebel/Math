# Balanced ordinary blades and mesoscopic guard blocks

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.

## 1. Outcome

Consider pair-windmill sequences with a density-one class of ordinary blades.
For an ordinary blade `i`, suppose

\[
 p_i\longrightarrow0,\qquad \lambda_i\longrightarrow0,
 \qquad {\lambda_i\over p_i}\longrightarrow c\in(0,\infty).   \tag{1}
\]

Two exact conclusions hold.

**PROVED (necessary handoff window).**  Even if center seeding were followed
by fixation with probability one, a positive limiting simultaneous gain at
fixed fitness `r` requires

\[
 \boxed{
 {r-1\over2r}<c<{r^2(2-r)\over2(r-1)}.}          \tag{2}
\]

This interval is nonempty precisely when

\[
 (r-1)^2<r^3(2-r).                               \tag{3}
\]

Its unique closing point in `(1,2)` is

\[
 r_{\rm hand}
 ={1+\sqrt2+\sqrt{2\sqrt2-1}\over2}
 =1.883203505913525864\ldots.                    \tag{4}
\]

Thus this pair-handoff architecture cannot give a positive limiting
simultaneous gain above `r_hand`.  At equality the leading window collapses;
the calculation alone does not decide a vanishing finite-size gain.
For eventual strict amplification whose gain is allowed to vanish, the
corresponding necessary window is the closure
`c_B(r)<=c<=c_D(r)`.  Hence every `r>r_hand` is still rigorously excluded,
whereas the critical endpoint is not.

**PROVED (mesoscopic guard no-go).**  Suppose all blades are strong pairs,
`max_j lambda_j -> 0`.  Conditional on an ordinary mutant pair first seeding
the center, no growing collection of initially resident pair blades can make
the subsequent fixation probability tend to one under both update rules.
Death--birth requires their total ratio mass

\[
 L_N=\sum_{j\ne i}\lambda_j
\]

to diverge, whereas birth--death requires the same `L_N` to tend to zero.
This contradiction is unaffected by splitting the exceptional vertices into
multiple booster or guard blocks, and it uses only the first center-mutant
episode plus the positive probability of source erasure after a failed
episode.

## 2. Exact limiting handoff probabilities

Stop when the resident center is first seeded or the ordinary mutant lineage
is erased.  As in `MODIFIED_SCALE_AUDIT.md`, let `M` mean that both vertices
of the ordinary blade are mutant and `H` that exactly one is mutant.

### 2.1 Death--birth

The exact dB equations are

\[
 D_M={q_2+2xD_H\over q_2+2x},\qquad
 D_H={q_1+yD_M\over1+q_1+y},                    \tag{5}
\]

where

\[
 q_2={rp\over1+(r-1)p},\quad
 q_1={rp\over2+(r-1)p},\quad
 x={\lambda\over r+\lambda},\quad
 y={r\over r+\lambda}.                          \tag{6}
\]

Substituting `lambda=cp` and sending `p -> 0` gives

\[
 D_M\longrightarrow {r^2\over r^2+c},\qquad
 \boxed{D_H\longrightarrow {r^2\over2(r^2+c)}}. \tag{7}
\]

The second value is the maximal possible dB fixation from either singleton
ordinary vertex if everything after center seeding is declared successful.

### 2.2 Birth--death

For Bd, global fitness normalization cancels separately in each transient
state.  Put

\[
 s_M={2r\lambda\over1+\lambda},\quad
 s_H={r\lambda\over1+\lambda},\quad
 u={r\over1+\lambda},\quad
 v={1\over1+\lambda}+{p\over2}.                 \tag{8}
\]

Here `s_M` is center seeding from `M`; `p` is resident-center invasion of the
mutant pair; from `H`, `s_H,u,v` are respectively center seeding, restoration
to `M`, and erasure.  Therefore

\[
 B_M={s_M+pB_H\over s_M+p},\qquad
 B_H={s_H+uB_M\over s_H+u+v}.                   \tag{9}
\]

With `lambda=cp` and `p -> 0`,

\[
 B_M\longrightarrow
 {2r(r+1)c\over1+2r(r+1)c},\qquad
 \boxed{B_H\longrightarrow
 {2r^2c\over1+2r(r+1)c}}.                       \tag{10}
\]

Equations (5) and (9) include all repeated `M <-> H` excursions.  They are
not isolated-event approximations.

## 3. Derivation of the window

The complete-graph fixation baseline tends to

\[
 \rho_\infty(r)=1-{1\over r}={r-1\over r}
\]

under either update rule.  Since fixation requires the center handoff, (7)
and (10) are upper bounds even under a perfect post-handoff mechanism.

For Bd, `B_H>rho_infinity` is equivalent to

\[
 c>{r-1\over2r}=:c_{\rm B}(r).                  \tag{11}
\]

For dB, `D_H>rho_infinity` is equivalent to

\[
 c<{r^2(2-r)\over2(r-1)}=:c_{\rm D}(r),         \tag{12}
\]

which already forces `r<2`.  Comparing (11) and (12) gives (3).

The equality polynomial is reciprocal:

\[
 (r-1)^2-r^3(2-r)
 =r^4-2r^3+r^2-2r+1.                            \tag{13}
\]

After division by `r^2` and substitution `z=r+r^{-1}`, it becomes
`z^2-2z-1=0`.  Since `r>1`, `z=1+sqrt(2)`, which gives (4).  Monotonicity of
`r+r^{-1}` on `(1,infinity)` proves uniqueness.

## 4. Exact guard-block contradiction

Fix an ordinary blade `i` satisfying (1).  Condition on the overwhelmingly
typical handoff state in which blade `i` is monomorphic mutant, the center is
mutant, and every other blade is resident.  Direct seeding from state `H` has
probability `O(p_i)` under either rule, so it does not alter the limit.

Let

\[
 L_N=\sum_{j\ne i}\lambda_j,
 \qquad \max_j\lambda_j\longrightarrow0.        \tag{14}
\]

### 4.1 dB needs `L_N -> infinity`

While the center is mutant, it reverts at its next death with effective rate

\[
 d_{\rm dB}
 ={1-p_i\over r p_i+1-p_i}\longrightarrow1.     \tag{15}
\]

For either vertex of a resident blade `j`, a death produces a mutant copy
from the center with probability `r lambda_j/(1+r lambda_j)`.  Thus the
total rate of the first mutant offspring outside the source pair is

\[
 A_{\rm dB}
 =2\sum_{j\ne i}{r\lambda_j\over1+r\lambda_j}.   \tag{16}
\]

Deleting self-loops, the probability of producing any such offspring before
center reversion is exactly

\[
 g_{\rm dB}={A_{\rm dB}\over A_{\rm dB}+d_{\rm dB}}.           \tag{17}
\]

If the center reverts without offspring, the process returns to `M` with all
other blades resident.  By (7), the source is then erased before another
center seed with limiting probability

\[
 \delta_{\rm dB}={c\over r^2+c}>0.              \tag{18}
\]

Consequently, conditional post-handoff fixation is at most

\[
 1-(1-g_{\rm dB})(\delta_{\rm dB}+o(1)).         \tag{19}
\]

For this bound to tend to one it is necessary that `g_dB -> 1`, hence
`A_dB -> infinity`.  Under the strong-pair assumption in (14),

\[
 A_{\rm dB}\sim2rL_N,
\]

so dB requires

\[
 L_N\longrightarrow\infty.                     \tag{20}
\]

### 4.2 Bd needs `L_N -> 0`

Under Bd, the mutant center produces a type-changing offspring in a resident
blade at total unnormalized rate

\[
 A_{\rm Bd}=r(1-p_i)\longrightarrow r.          \tag{21}
\]

The resident vertices of blade `j` replace the mutant center at total rate
`2 lambda_j/(1+lambda_j)`.  Hence

\[
 d_{\rm Bd}=2\sum_{j\ne i}{\lambda_j\over1+\lambda_j},\qquad
 g_{\rm Bd}={A_{\rm Bd}\over A_{\rm Bd}+d_{\rm Bd}}.           \tag{22}
\]

After a childless center reversion, (10) shows that the source is erased
before another seed with limiting probability

\[
 \delta_{\rm Bd}={1\over1+2r(r+1)c}>0.          \tag{23}
\]

The analogue of (19) makes `g_Bd -> 1` necessary for conditional fixation to
tend one.  Therefore `d_Bd -> 0`.  Because `max_j lambda_j -> 0`, this is
equivalent to

\[
 L_N\longrightarrow0.                           \tag{24}
\]

Conditions (20) and (24) are incompatible.  The proof treats the first
offspring as immediate success, so internal pair resolution, overlapping
introductions, and every later sweep can only decrease the true fixation
probability.  It therefore rules out arbitrary mesoscopic partitions of the
resident strong-pair block, not merely a homogeneous guard.

## 5. Scope and status

**PROVED:** exact handoff limits (7) and (10), window (2), algebraic closing
point (4), and the strong-pair mesoscopic guard no-go (20) versus (24).

**NOT CLAIMED:** a universal obstruction for graphs outside the pair-windmill
architecture, or an endpoint obstruction at `r=r_hand` based on subleading
finite-size terms.
