# Pair ordinary blades with a growing-clique guard

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.

## 1. Outcome

A growing clique guard has exponentially small reverse establishment once it
is mutant.  Nevertheless it cannot repair the balanced pair-windmill
architecture.

**PROVED.**  Let a mutant ordinary pair have balanced ratio
`lambda_i/p_i -> c in (0,infinity)`, and suppose it first seeds the center.
Replace any mesoscopic strong-pair guard by one or more growing clique modules
connected only through that center.  If all per-vertex center couplings tend
to zero, post-center-seed fixation cannot tend to one under both dB and Bd.

Writing

\[
 \Gamma_N=\sum_{j\ne i}s_j\theta_j,
 \qquad
 \theta_j={a_j\over(s_j-1)b_j},                 \tag{1}
\]

dB requires `Gamma_N -> infinity`, while Bd requires
`Gamma_N -> 0`.  The exponentially small reverse clique probability acts
only after a clique has become mutant and therefore cannot alter this first
establishment contradiction.

## 2. Isolated clique probabilities from first principles

Consider the unit complete graph `K_s`, with mutant fitness `r>1`.  Let
`alpha_s^U(r)` be fixation from one mutant and `beta_s^U(r)` fixation of one
resident introduced into an otherwise mutant clique, for update rule `U`.

### 2.1 Birth--death

At mutant count `k`, the ratio of the down-step and up-step probabilities is
exactly `1/r`.  Solving the one-dimensional absorbing recurrence gives

\[
 \boxed{\alpha_s^{\rm Bd}(r)
 ={1-r^{-1}\over1-r^{-s}},\qquad
 \beta_s^{\rm Bd}(r)
 ={r-1\over r^s-1}.}                            \tag{2}
\]

The second formula is the first with focal fitness `1/r`.

### 2.2 Death--birth

For `1<=k<=s-1`, direct use of the dB rule gives

\[
 T_k^+={s-k\over s}{rk\over rk+s-k-1},\qquad
 T_k^-={k\over s}{s-k\over r(k-1)+s-k}.         \tag{3}
\]

Put `A_k=(r-1)k+s-1`.  The step ratio telescopes:

\[
 {T_k^-\over T_k^+}={A_k\over rA_{k-1}},\qquad
 \prod_{j=1}^k{T_j^-\over T_j^+}
 ={A_k\over(s-1)r^k}.                           \tag{4}
\]

The standard absorbing recurrence

\[
 \alpha_s^{-1}=1+\sum_{k=1}^{s-1}
                   \prod_{j=1}^k{T_j^-\over T_j^+}
\]

then yields

\[
 \boxed{\alpha_s^{\rm dB}(r)
 ={s-1\over s}{1-r^{-1}\over1-r^{-(s-1)}},\qquad
 \beta_s^{\rm dB}(r)
 ={s-1\over s}{r-1\over r^{s-1}-1}.}           \tag{5}
\]

Thus, for fixed `r>1`,

\[
\begin{array}{ll}
 \alpha_s^{\rm Bd}=1-r^{-1}+O_r(r^{-s}),
 &\beta_s^{\rm Bd}=(r-1)r^{-s}(1+O_r(r^{-s})),\\[1mm]
 \alpha_s^{\rm dB}=(1-s^{-1})(1-r^{-1})+O_r(r^{-s}),
 &\beta_s^{\rm dB}=(1-s^{-1})(r-1)r^{-(s-1)}
                    (1+O_r(r^{-(s-1)})).
\end{array}                                                       \tag{6}
\]

Both reverse probabilities are exponentially small.  This is the apparent
advantage of a growing guard.

## 3. Exact leading module rates

Module `j` is a clique of size `s_j`, every internal edge has weight `b_j`,
and every vertex has a center edge of weight `a_j`.  Define

\[
 \theta_j={a_j\over(s_j-1)b_j},\qquad
 p_j={s_ja_j\over\sum_\ell s_\ell a_\ell}.       \tag{7}
\]

Take the separated-module limit `theta_j -> 0` after fixing the finite module
sizes; for growing modules use the corresponding finite-state diagonal.  The
formulas below are the successful-conversion hazards.  As with pair blades,
they need not be interpreted as a literal center/module trace during a
heterogeneous-module excursion.

### 3.1 Death--birth

If the center is mutant and clique `j` is resident, a death in that clique
copies the center with probability

\[
 {r\theta_j\over1+r\theta_j}.
\]

There are `s_j` target vertices, and the resulting singleton fixes internally
with probability `alpha_{s_j}^dB`.  Conversely, a resident center is copied
into a mutant clique with probability `theta_j/(r+theta_j)` at each target
death, after which the resident fixes with probability `beta_{s_j}^dB`.
Hence

\[
\begin{aligned}
 (1,\text{resident }j)\to(1,\text{mutant }j):&\quad
 s_j{r\theta_j\over1+r\theta_j}\alpha_{s_j}^{\rm dB}(r)
 \sim s_jr\theta_j\alpha_{s_j}^{\rm dB}(r),\\
 (0,\text{mutant }j)\to(0,\text{resident }j):&\quad
 s_j{\theta_j\over r+\theta_j}\beta_{s_j}^{\rm dB}(r)
 \sim {s_j\theta_j\over r}\beta_{s_j}^{\rm dB}(r).
\end{aligned}                                                       \tag{8}
\]

At a center death, mutant and resident monomorphic modules contribute parent
masses `r p_j` and `p_j`, respectively, exactly as for pair blades.

### 3.2 Birth--death

A center birth targets module `j` with probability `p_j`.  A mutant or
resident singleton introduced there fixes with (2), giving

\[
\begin{aligned}
 (1,\text{resident }j)\to(1,\text{mutant }j):&\quad
 rp_j\alpha_{s_j}^{\rm Bd}(r),\\
 (0,\text{mutant }j)\to(0,\text{resident }j):&\quad
 p_j\beta_{s_j}^{\rm Bd}(r).
\end{aligned}                                                       \tag{9}
\]

Births from a monomorphic module into the center have rates

\[
 \text{mutant }j\to\text{center}:\quad
 s_jr{\theta_j\over1+\theta_j},\qquad
 \text{resident }j\to\text{center}:\quad
 s_j{\theta_j\over1+\theta_j}.                  \tag{10}
\]

Equations (8)--(10) specialize to the pair formulas at `s_j=2`.

## 4. The establishment-scale contradiction

Fix a balanced ordinary source pair `i`, condition on its typical handoff
state (source pair and center mutant, every other module resident), and put

\[
 \Gamma_N=\sum_{j\ne i}s_j\theta_j,
 \qquad \max_{j\ne i}\theta_j\longrightarrow0.  \tag{11}
\]

The direct handoff from a heterogeneous source pair has probability `o(1)`;
thus conditioning on center seeding leaves the source pair monomorphic with
probability `1-o(1)`.

### 4.1 Necessary dB scale

The mutant center reverts at a center death with probability tending one,
because its only mutant neighbors are the source pair and `p_i -> 0`.  Before
that reversion, the exact total rate of producing the first mutant child in
the resident modules is

\[
 C_{\rm dB}
 =\sum_{j\ne i}s_j{r\theta_j\over1+r\theta_j}
 \sim r\Gamma_N.                                \tag{12}
\]

Even if this first child is declared an immediately fixed, perfectly
persistent guard, its probability of appearing before center reversion tends
one only if

\[
 \Gamma_N\longrightarrow\infty.                \tag{13}
\]

To see that tending one is necessary, expose the event that the first center
episode is childless and that, after reversion, the ordinary source is erased
before reseeding the center.  The latter event has limiting probability
`c/(r^2+c)>0` by the exact balanced dB handoff calculation.  Therefore any
post-handoff fixation probability tending one forces the first episode to be
non-childless with probability tending one, which is (13).

Multiplying (12) by `alpha_s^dB` to demand completed clique establishment
does not weaken (13): for growing cliques `alpha_s^dB -> 1-1/r`, while
declaring the first child successful was already the most favorable bound.

### 4.2 Necessary Bd scale

The mutant center produces a child in a resident module at total
unnormalized rate

\[
 C_{\rm Bd}=r(1-p_i)\longrightarrow r.           \tag{14}
\]

Resident clique vertices replace that center at total rate

\[
 K_{\rm Bd}
 =\sum_{j\ne i}s_j{\theta_j\over1+\theta_j}
 \sim\Gamma_N.                                  \tag{15}
\]

Thus even granting that the first center child fixes its clique with
probability one, the probability of a child before center loss tends one
only if

\[
 \Gamma_N\longrightarrow0.                     \tag{16}
\]

Again this condition is necessary, not merely convenient: after a childless
center loss, the balanced source pair is erased before another seed with
limiting probability

\[
 {1\over1+2r(r+1)c}>0.
\]

The actual forward establishment factor `alpha_s^Bd -> 1-1/r<1` can only
reduce success.  The exponential reverse factor
`beta_s^Bd asymptotic (r-1)r^{-s}` becomes relevant only after establishment
and cannot change the child-versus-center-loss race (14)--(15).

Conditions (13) and (16) contradict one another.  Multiple growing cliques,
several mesoscopic scales, and arbitrary later sweep dynamics do not help,
because the proof sums all initially resident module couplings and grants
success at the first mutant copy.

## 5. Status

**PROVED:** isolated clique probabilities (2) and (5), all leading module
hazards (8)--(10), and the post-center-seed scale contradiction.

**FALSIFIED:** a growing-clique guard as a simultaneous dB booster and
Bd-persistent guard for a balanced ordinary pair source.

**NOT CLAIMED:** an obstruction for architectures in which fixation can avoid
the single center bottleneck or modules interact away from the center.

