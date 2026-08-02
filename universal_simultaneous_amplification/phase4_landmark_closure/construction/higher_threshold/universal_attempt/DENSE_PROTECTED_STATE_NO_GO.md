# Dense entry cannot gain through a weak bounded protected state

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.  This note is a proved
no-go for a broad construction mechanism, **not** a resolution of the global
problem.

## 1. Outcome

Two exact facts close the most direct version of the proposed dense-entry
route.

1. **PROVED (collision-free cap).**  The uniformly averaged survival
   probability of the dB rare-mutant branching process on any finite weighted
   population is at most

   \[
      p=1-\frac1r.                                      \tag{1}
   \]

   Equality is possible only in the isothermal case.  Thus a diffuse
   singleton phase cannot itself create a dB gain above the limiting complete
   baseline.  Any gain must use collisions between related mutants.

2. **PROVED (bounded protected-state penalty).**  Overlay any fixed finite
   undirected gadget on a complete, density-one background, and retain *all*
   local mutant configurations in the exact rare-colony process.  If the
   gadget edge shares have common small scale `epsilon`, then the uniform dB
   establishment probability is

   \[
   p-\frac{r-1}{r^2}
     \left\{\operatorname{Var}(d_i)
       +\frac{2(r-1)}k\sum_{i<j}a_{ij}^2\right\}
       \varepsilon^2+O(\varepsilon^3).          \tag{2}
   \]

   Here `k` is the gadget order, `a_ij` are its normalized internal weights,
   and `d_i=sum_j a_ij`.  The coefficient is strictly negative for every
   nonzero gadget and every `r>1`.  It already includes singleton-to-pair,
   pair-to-triple, repeated repair, and every higher protected state inside
   the gadget.  Consequently no weak bounded gadget, nor any bounded
   multiscale hierarchy whose largest internal edge share tends to zero, can
   improve dB establishment at its first nonzero order.

For weighted partner pairs an additional exact expansion gives

\[
 \rho^{\rm est}_{Bd}
 =p-\frac{r-1}{r^3}
 \left(\mu^3-3\mu\nu+2\kappa\right)\varepsilon^3
 +O(\varepsilon^4),                              \tag{3}
\]

where `mu=E a`, `nu=E a^2`, and `kappa=E a^3` over pair vertices.  The cubic
bracket is nonnegative, and is zero only when all partner strengths agree.
Thus heterogeneous dense pairs hurt Bd as well; equal pairs are globally
weighted regular and tie the complete Bd baseline.  This includes the
degenerate constant-zero overlay: it has no leading protected edge, the
cubic coefficient vanishes, and the underlying regular graph still ties Bd.

The remaining escape routes are genuinely mesoscopic or global: gadget order
must grow, or the construction must exploit a finite-population correction
smaller than the establishment scale.  Formula (2) does not rule those out.

## 2. Collision-free dB cap

Let `D_v=sum_u w_uv` and define

\[
 A_{uv}=\frac{w_{uv}}{D_v}.                     \tag{4}
\]

In the collision-free dB process a mutant at `u` dies at rate one and creates
a child at `v` at rate `r A_uv`.  The matrix `A` is column stochastic:
`sum_u A_uv=1`.  If `s_u` is the survival probability from type `u`, direct
first-event conditioning gives

\[
 s_u=f((As)_u),\qquad f(x)=\frac{rx}{1+rx}.      \tag{5}
\]

The function `f` is strictly concave.  Since column stochasticity gives
`sum_u(As)_u=sum_u s_u`, Jensen's inequality yields, with
`bar s=n^{-1}sum_u s_u`,

\[
 \bar s\le f(\bar s).                            \tag{6}
\]

For the positive survival solution, (6) is equivalent to `bar s<=p`.  If
equality holds, strict concavity makes `As` constant.  Equation (5) then
makes `s` constant; averaging the row sums of `A` shows `A 1=1`, and (5)
gives `s=p 1`.  This proves the equality statement.

This is an establishment theorem.  By itself it is not a fixation upper
bound: the complete finite dB baseline lies below `p` by order `1/n`, and
post-collision states can change fixation.

## 3. Exact dense-gadget colony process

Fix a symmetric nonnegative `k` by `k` matrix `a` with zero diagonal.  Take
`M` labelled copies of its vertex set, put unit weight on every edge between
different copies, and put leading weight

\[
     n\varepsilon a_{ij},\qquad n=kM,            \tag{7}
\]

on the internal edge `ij` of every copy.  Adding a background unit weight to
internal edges changes only the vanishing `O(1/n)` terms.  The graph is
connected through its complete inter-copy support.

The order of limits in this section is essential.  First hold `k`, `r`, and
`epsilon>0` fixed and send `M->infinity`; this gives the rare-colony process
below.  Only after that limit do we expand its establishment probability as
`epsilon->0`.  No uniform finite-`n` fixation expansion is asserted.

Put

\[
 d_i=\sum_j a_{ij},\quad
 x_i=(1+\varepsilon d_i)^{-1},\quad
 H=\frac1k\sum_i x_i.                           \tag{8}
\]

Until two externally generated lineages enter the same copy, an occupied
copy is described exactly by its nonempty mutant set `S`.  Directly from the
dB rule, its local rates are as follows.  If `v` is resident, then

\[
 S\longrightarrow S\cup\{v\}\quad\hbox{at rate}\quad
 \frac{r\varepsilon\sum_{u\in S}a_{uv}}
 {1+\varepsilon d_v+(r-1)\varepsilon\sum_{u\in S}a_{uv}}.    \tag{9}
\]

If `v` is mutant, then

\[
 S\longrightarrow S\setminus\{v\}\quad\hbox{at rate}\quad
 \frac{1+\varepsilon\sum_{u\notin S}a_{uv}}
 {1+\varepsilon\sum_{u\notin S}a_{uv}
      +r\varepsilon\sum_{u\in S\setminus\{v\}}a_{uv}}.    \tag{10}
\]

Each mutant in `S` also produces external singleton colonies at total rate
`rH`; their label law is

\[
       \Pr(i)=\frac{x_i}{kH}.                    \tag{11}
\]

Equations (9)--(11) retain every internal collision.  They define a finite
`2^k-1` type branching process, obtained as the direct rare-colony limit
`M->infinity`.

Let `q_S` be extinction from local state `S`, and let

\[
 Q=\frac1{kH}\sum_i x_i q_{\{i\}}.              \tag{12}
\]

If `L_ST` denotes the rates (9)--(10), first-event conditioning is the exact
linear system, for fixed `Q`,

\[
 0=\sum_T L_{ST}(q_T-q_S)
    +|S|rHq_S(Q-1),\qquad q_\varnothing=1,       \tag{13}
\]

together with the scalar consistency equation (12).  This proves exact
lumpability of the colony state: no branching-only independence assumption
is made *within* a gadget.

## 4. Expansion and strict sign

Write

\[
 \mu=\frac1k\sum_i d_i,\qquad
 \nu=\frac1k\sum_i d_i^2,qquad
 E_2=\sum_{i<j}a_{ij}^2.                        \tag{14}
\]

At `epsilon=0`, independent lineages give

\[
 q_S=r^{-|S|},\qquad Q=r^{-1}.                  \tag{15}
\]

Differentiate (12)--(13).  For singletons and doubletons write

\[
 q_{\{i\}}=r^{-1}+\varepsilon X_i+\varepsilon^2Y_i+O(\varepsilon^3),
 \quad
 q_{\{i,j\}}=r^{-2}+\varepsilon X_{ij}+O(\varepsilon^2).    \tag{16}
\]

The first-order equations give

\[
 X_i=\frac{r-1}{r^2}(\mu-d_i),                  \tag{17}
\]

\[
 X_{ij}=\frac{r-1}{r^3}
   \{2\mu-d_i-d_j-(r-1)a_{ij}\}.                \tag{18}
\]

In particular `k^{-1}sum_i X_i=0`.  Averaging the second-order singleton
equations and using (12) gives

\[
 \frac1k\sum_iY_i
 =\frac{r-1}{r^2}
   \left\{\nu-\mu^2+\frac{2(r-1)}kE_2\right\}.  \tag{19}
\]

Since uniform establishment is
`1-k^{-1}sum_i q_{\{i\}}`, equations (17)--(19) prove (2).
The first term in braces is the variance of the internal weighted degrees;
the second is positive for every nonzero gadget.  Hence the sign is strict.

For fixed `k` and fixed `r>1`, if the normalized gadget shape is allowed to
vary with `epsilon`, normalize it by `E_2=1` and take a convergent
subsequence.  The coefficient in (19) is at least
`2(r-1)^2/(kr^2)`.  Analyticity of the finite system (13) makes the remainder
uniform on this fixed-`k`, fixed-`r` compact set.  Thus bounded-order
multiscale shapes do not evade the sign.  This statement is not uniform as
`k` grows or as `r->1`.

## 5. Pair corollary under both rules

Partition a bounded gadget into disjoint partner pairs.  Let `a` be the
partner strength seen from a uniformly selected vertex and put
`z=epsilon a`.  In the Bd colony process define

\[
 x=(1+z)^{-1},\quad H=E x,\quad h=1-x.           \tag{20}
\]

For a singleton pair, external erasure, internal growth, and external birth
have rates `H+h`, `rh`, and `rx`.  For a double pair, shrinkage and external
birth have rates `2H` and `2rx`.  If `T` is uniform establishment and
`Q=1-T`, exact first-event conditioning gives

\[
 \frac{q_2(a)}{q_1(a)}=\frac{H}{H+rxT},          \tag{21}
\]

\[
 q_1(a)=\frac{H+h}
 {H+h+rh+rxT-rh\,q_2(a)/q_1(a)},qquad
 Q=E q_1(a).                                    \tag{22}
\]

Expanding (21)--(22) gives (3).  Its bracket factors as

\[
 \mu^3-3\mu\nu+2\kappa
 =\underbrace{(\kappa-\mu\nu)}_{\operatorname{Cov}(a^2,a)\ge0}
 +\underbrace{E[a(a-\mu)^2]}_{\ge0}.            \tag{23}
\]

Both terms vanish only for constant `a`, including the constant-zero
degenerate case.  This proves the pair claim.

## 6. Scope

**PROVED:** (1)--(3), the exact colony rates (9)--(13), and the uniform
strict sign for every fixed gadget order.

**NUMERICALLY OBSERVED:** direct solution of the full colony systems for
orders three and four, over broad random internal weights at `r=1.51`, found
no positive dB establishment candidate away from the weak-overlay regime.

**NOT PROVED HERE:** a finite-population fixation comparison when
`epsilon=epsilon_n` vanishes at the same scale as `1/n`; a growing gadget
order; or a universal Bd--dB obstruction.  Those are the remaining places
where a dense construction could still hide.  In particular, the successive
`M->infinity` then `epsilon->0` theorem above must not be read as a uniform
statement along an arbitrary diagonal `epsilon=epsilon_n`.
