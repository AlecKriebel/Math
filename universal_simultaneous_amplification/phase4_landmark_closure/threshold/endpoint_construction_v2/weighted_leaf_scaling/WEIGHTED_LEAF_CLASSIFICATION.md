# Weighted hub leaves do not improve the dilute hybrid threshold

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Class theorem

Consider the proved dilute `K_2`-satellite construction, but allow its hub
leaves to have a common positive weight depending on population size.  Also
allow a second dilute population of leaves attached to distinct clique
vertices, with `w/C -> tau` for `tau in (0,infinity]`.

**Theorem.**  Among all common-hub weight regimes described in Section 2,
the regime

\[
                         w=o(C/m)                         \tag{1}
\]

is Pareto optimal: it has the largest Bd correction for the same dB loss.
Distinct-hub heavy leaves are strictly dominated at every `r>=3/2` after
the full far-field singleton correction is included.  Consequently none of
these weighted-leaf extensions raises the exact dilute-hybrid threshold

\[
 R_*=1.5028569127905696\ldots .                          \tag{2}
\]

This is a class-optimality theorem for the stated dilute weighted-leaf plus
`K_2` mechanisms, not a universal graph obstruction.

## 2. Many leaves on one hub

Let a unit clique `K_C` have `m` leaves on one distinguished hub, all with
edge weight `w=w(C,m)`, where

\[
                  m\longrightarrow\infty,qquad m=o(C).
\]

Put

\[
                         a={C\over mw}.                   \tag{3}
\]

Resolve successive mutant-hub excursions from one rare mutant leaf.  After
a common time change, the limiting per-particle rates are

\[
 r^2\quad\hbox{(new mutant leaf)},\qquad
 1\quad\hbox{(leaf loss)},\qquad
 r(r-1)a\quad\hbox{(successful core mark)}.             \tag{4}
\]

The first two rates come from activation and return through the same hub.
The last rate is the hub-to-core introduction rate times the exact
large-clique establishment probability `p=1-1/r`.  Conditioning an unmarked
family on extinction makes it subcritical, so the stopped branching limit
also controls the path after establishment.

If `a` tends to a value in `(0,infinity)`, let `z_r(a)` be the smaller root
in `(0,1)` of

\[
 r^2z^2-\{r^2+1+r(r-1)a\}z+1=0.                        \tag{5}
\]

The leaf fixation limit is `ell_r(a)=1-z_r(a)`.  Its normalized correction
vector per leaf is

\[
 \boxed{\left({\ell_r(a)\over p}-1,-1\right).}          \tag{6}
\]

The dB coordinate is `-1` in every regime: a rare mutant leaf dies at
order-one death-clock rate, while mutant activation of its hub is at most
`O(1/m)`.

Equation (5), together with the endpoint trace described below, gives

\[
\begin{array}{c|c|c}
\hbox{weight regime}&a&\hbox{correction vector}\\
\hline
w=o(C/m)&\infty&(1/(r-1),-1)\\[1mm]
w\sim\theta C/m&1/\theta&(\ell_r(1/\theta)/p-1,-1)\\[1mm]
C/m\ll w,\ \log(w/C)=o(m)&0&(1/r,-1).
\end{array}                                             \tag{7}
\]

The last line includes `w=Theta(C)` and, when `log C=o(m)`, every
polynomially larger scale.  In this regime a surviving supercritical leaf
family has lifetime `exp(Theta(m))`, while the successful-core mark clock is
only subexponentially slower, so it is marked with probability tending to
one.  If `w/C` grows exponentially fast enough in `m`, a second metastable
scale appears: the family can die before its first core mark.  For an
arbitrary sequence with `a->0`, the Bd coordinate in (6) therefore lies in
the rigorous interval

\[
                             -1\le\beta_B\le1/r.         \tag{8}
\]

The upper endpoint is the survival probability `1-1/r^2` divided by `p`,
minus one; no post-survival path can increase it.  This finer strong-weight
subdivision is irrelevant to optimization because every value in (8) is
strictly worse than the first line of (7).

For positive finite `a`, implicit differentiation of (5), or its explicit
smaller-root formula, shows that `z_r(a)` decreases with `a`.  Hence, over
all common-hub regimes including the metastable strong-weight cases,

\[
 -1\le\beta_B\le {1\over r-1}.                          \tag{8a}
\]

Thus (1) supplies the most Bd gain per unit dB loss.  Changing the common
weight cannot improve the `K_2` hybrid.

## 3. One heavy leaf on a distinct hub

Now attach one leaf of weight `w=\tau C` to a clique vertex, with fixed
`tau>0`.  A dilute growing population uses different clique hubs, so the
heavy loads do not aggregate.  The first local calculation alone is not the
answer: each of the `C+O(1)` ordinary clique singleton values changes by
`Theta(C^-1)`, and their sum contributes at leading order.

Let `u_{10}` and `u_{01}` denote the limiting fixation probabilities from a
mutant decorated hub and mutant leaf.  Resolving the three local transient
states `10,01,11` and thinning a hub-to-core seed by the core establishment
probability gives

\[
 u_{10}^{B}={(r-1)(r^2\tau^2+2r^2\tau+r^2+r\tau^2-r+\tau^2)
  \over(r\tau+r+2\tau+1)(r^2\tau+r^2-r+\tau^2)},        \tag{9}
\]

\[
 u_{01}^{B}={r(r-1)(\tau+1)\over
                    r^2\tau+r^2-r+\tau^2},             \tag{10}
\]

\[
 u_{10}^{D}={(r-1)(2r^2\tau+r+1)\over
 r(r+1)(2r\tau-2\tau+1)},\qquad
 u_{01}^{D}={\tau(r-1)\over2r\tau-2\tau+1}.            \tag{11}
\]

For reference, the local transition rates are

\[
\begin{array}{c|ccc}
 &\hbox{success}&\hbox{other local mutant state}&\hbox{extinction/reversion}\\
\hline
B:10&(r-1)/(1+\tau)&11:r\tau/(1+\tau)&00:2\\
B:01&0&11:r&00:\tau/(1+\tau)\\
B:11&(r-1)/(1+\tau)&01:1&0\\[1mm]
D:10&r-1&11:1&00:1\\
D:01&0&11:r\tau/(1+r\tau)&00:1\\
D:11&r-1&01:1/(1+r\tau)&0.
\end{array}                                             \tag{12}
\]

## 4. The far-field correction

For `i` rare ordinary core mutants, the leading branching generator is

\[
 (\mathcal G_0g)(i)=ri\{g(i+1)-g(i)\}
                  +i\{g(i-1)-g(i)\}.                   \tag{13}
\]

If the local defect state is `x`, its leading fixation harmonic is

\[
                         f_x(i)=1-r^{-i}e_x,             \tag{14}
\]

where `e_x` is the local failure probability.  Substitution of (14) into
the exact `(i,h,l)` orbit rates at the all-resident defect gives

\[
 \mathcal G_Bf={i r^{-i}\over C}
 \left\{r u_{10}^{B}-{r-1\over1+\tau}\right\}+o(C^{-1}),\tag{15}
\]

\[
 \mathcal G_Df={i r^{-i}\over C}
 \left\{-r(r-1)+{r u_{10}^{D}\over1+\tau}\right\}
 +o(C^{-1}).                                            \tag{16}
\]

Since

\[
 \mathcal G_0\{i r^{-i}\}=-(r-1)i r^{-i},              \tag{17}
\]

the ordinary-singleton Poisson correction is the brace in (15) or (16),
divided by `Cr(r-1)`.  Finally one must compare with the exact complete-graph
baselines.  The Bd baseline has no algebraic `C^-1` term, while the dB
baseline

\[
 \rho_{dB}(K_n,r)={(n-1)(r-1)r^{n-2}\over
                         n(r^{n-1}-1)}
\]

has term `-p/C`.  Combining the local and far-field contributions gives the
full correction vector

\[
 \boxed{
 B(r,\tau)=
 -{(2\tau+1)(r\tau^3-2r\tau-r+2\tau^3+\tau^2)
 \over(\tau+1)(r\tau+r+2\tau+1)
       (r^2\tau+r^2-r+\tau^2)},}                       \tag{18}
\]

\[
 \boxed{
 D(r,\tau)=
 -{r^2\tau^2+r^2\tau+r\tau^2+r-2\tau^2-2\tau+1
 \over(r+1)(\tau+1)(2r\tau-2\tau+1)}.}                \tag{19}
\]

For `r=3/2`, these simplify to

\[
 B=-{4(\tau-1)(2\tau+1)(7\tau^2+9\tau+3)
 \over(\tau+1)(7\tau+5)(4\tau^2+9\tau+3)},\qquad
 D=-{7\tau^2+\tau+10\over10(\tau+1)^2}.                \tag{20}
\]

In particular, `D<0` for every positive `tau`.  At `tau=5/2`, (18)--(19)
give exactly

\[
                         B=-{2216\over3535},\qquad
                         D=-{45\over98}.                 \tag{21}
\]

These agree with the independent finite orbit chain as `C` grows.  The
earlier local-only values omit (15)--(17) and are not valid population
corrections.

## 5. Exact dominance for every `r>=3/2`

Ordinary common-hub leaves have vector `(1/(r-1),-1)`.  A distinct-heavy
defect can improve their Bd/dB tradeoff only if

\[
                         D+(r-1)B>0.                    \tag{22}
\]

Let `x=r-3/2`.  The denominator of (22), after inserting (18)--(19), is
positive.  Its numerator is `-Q(x,tau)`, where

\[
\begin{aligned}
Q={}&{45\over16}+{375\over32}\tau+{561\over32}\tau^2
 +{845\over32}\tau^3+{1109\over32}\tau^4+{119\over8}\tau^5\\
&+x\left({21\over2}+{425\over16}\tau+{535\over16}\tau^2
 +{1431\over16}\tau^3+{2101\over16}\tau^4+{227\over4}\tau^5\right)\\
&+x^2\left({25\over2}+{125\over4}\tau+{181\over4}\tau^2
 +{413\over4}\tau^3+{561\over4}\tau^4+{135\over2}\tau^5\right)\\
&+x^3\left(6+{43\over2}\tau+{83\over2}\tau^2
 +{123\over2}\tau^3+{125\over2}\tau^4+29\tau^5\right)\\
&+x^4\left(1+{15\over2}\tau+{37\over2}\tau^2
 +{41\over2}\tau^3+{25\over2}\tau^4+4\tau^5\right)\\
&+x^5(\tau+3\tau^2+3\tau^3+\tau^4).
\end{aligned}                                           \tag{23}
\]

Every coefficient is nonnegative and the constant is positive.  Therefore

\[
             D(r,\tau)+(r-1)B(r,\tau)<0
             \quad(r\ge3/2,\ \tau>0).                  \tag{24}
\]

The polynomial certificate also has a positive value at the formal
`tau=0` boundary, and (24) persists in the `tau->infinity` limit.  The class
theorem asserted here uses `w/C->tau` with `tau in (0,infinity]`; no claim is
made here for a distinct-hub weight sequence without such a heavy-scale
limit.  Mixtures of finitely or dilutely many covered heavy-weight regimes
add their first-order corrections, so (24) persists under mixing.

For a `K_2` satellite correction `(F_B,F_D)`, eliminating the ordinary-leaf
count leaves the separator `F_D+(r-1)F_B`.  Equations (8)--(8a) show that other
common-hub scalings can only decrease it, while (24) shows that every
distinct-heavy population decreases it strictly once `r>=3/2`.  Since the
optimized `K_2` separator first vanishes at (2), the weighted-leaf extension
has the same exact class threshold and no larger one.

## 6. Verification status

- Equations (4)--(8): **PROVED** by the killed branching trace.
- Local chain (9)--(12): **EXACTLY COMPUTED** from the update rules.
- Far-field terms (15)--(19): **PROVED** by the displayed Poisson equation.
- Dominance (23)--(24): **EXACT POLYNOMIAL CERTIFICATE**.
- Finite labelled lumping and finite-size convergence: independently
  replayed by the scripts in this folder.
- Any improvement of the unrestricted global `R_sim`: **OPEN**.
