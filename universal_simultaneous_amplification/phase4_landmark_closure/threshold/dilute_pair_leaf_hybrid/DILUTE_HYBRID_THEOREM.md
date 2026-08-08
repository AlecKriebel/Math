# A dilute pair--leaf family beyond fitness three halves

Date: 2026-08-08 (America/Los_Angeles)

No literature search was used during discovery, and no external
communication was made.  A narrow post-theorem audit is recorded separately
in `LITERATURE_AUDIT.md`.

## 1. Result

Define

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1.              \tag{1}
\]

Let `R_hyb` be the unique root of `P` in `(3/2,151/100)`.  Exact Sturm
isolation gives

\[
                  R_{\rm hyb}=1.5028569127905696\ldots.    \tag{2}
\]

Put

\[
 \sigma_*={-R_{\rm hyb}^3+4R_{\rm hyb}^2-3R_{\rm hyb}-1
             \over2(R_{\rm hyb}-1)},                       \tag{3}
\]

and

\[
 \lambda_*={2(1-\sigma_*)(R_{\rm hyb}-1)
             \over1+\sigma_*(R_{\rm hyb}^2-1)}.            \tag{4}
\]

Both are positive algebraic constants, approximately

\[
 \sigma_*=0.1306772822870484,\qquad
 \lambda_*=0.7508064830318805.                             \tag{5}
\]

### Theorem

There is one explicit fitness-independent family of finite connected
loopless undirected weighted graphs `G_k`, with algebraic internal weights
and positive rational cross weights, such that for every fixed

\[
                         1<r<R_{\rm hyb},                   \tag{6}
\]

both

\[
 \rho_{Bd}(G_k,r)>\rho_{Bd}(K_{|G_k|},r),\qquad
 \rho_{dB}(G_k,r)>\rho_{dB}(K_{|G_k|},r)                   \tag{7}
\]

hold for all sufficiently large `k`.  Consequently

\[
                 \boxed{R_{\rm sim}\ge R_{\rm hyb}>3/2.}  \tag{8}
\]

This disproves the candidate exact threshold `3/2`.  It does not determine
the true value of `R_sim`.

Within the dilute `K_2`-satellite plus hub-leaf leading regime proved below,
`R_hyb` is the exact optimal threshold.

## 2. Graph construction

The graph has three ingredients.

1. A unit-weight clique `C` consisting of a hub `H` and `c` ordinary core
   vertices.
2. `m` leaves, each joined only to `H` by a unit-weight edge.
3. `q` disjoint pairs.  The internal edge of every pair has weight

   \[
                          W={c\over\sigma_*}.                \tag{9}
   \]

   Every pair vertex is joined to every clique vertex by the same positive
   cross weight `epsilon`.  There are no pair--pair edges.

All unspecified edges have weight zero.  Every cross edge is undirected.
For every `epsilon>0` the graph is connected, and all displayed weights are
positive algebraic or rational numbers independent of fitness.

The finite parameters are selected by the constructive diagonal in Section
7.  They obey

\[
 c_k\longrightarrow\infty,\quad q_k,m_k\longrightarrow\infty,
 \quad {q_k\over c_k}\longrightarrow0,\quad
 {m_k\over q_k}\longrightarrow\lambda_*,\quad
 \epsilon_k\longrightarrow0.                              \tag{10}
\]

The separation is chosen strongly enough that its fixation error is
`o(q_k/|G_k|)`, the scale of the strict gain.  An `o(1)` separation statement
would not suffice here.

## 3. Exact finite weak-cut trace

This section takes `epsilon -> 0` with `c,m,q` fixed.  It is therefore a
finite-state statement and introduces no population asymptotics.

Let `H_(c,m)` denote the clique--pendant module formed by the core clique and
its leaves.  At `epsilon=0`, the closed fast classes are exactly the states
in which `H_(c,m)` and every pair are internally homogeneous.  Label such a
class by

\[
                    (h,j)\in\{0,1\}\times\{0,\ldots,q\},   \tag{11}
\]

where `h` is the type of `H_(c,m)` and `j` is the number of mutant pairs.
Permutation of the pairs proves that these are exact macro orbits.

Partition the transient first-step matrix into mixed-module states `F` and
homogeneous-module states `M`.  At zero cross weight, the block on `F` is
invertible because every finite connected module absorbs internally.  The
Schur complement on `M`, after its common factor `epsilon` is removed,
converges to a finite macro generator.  Its transitions are obtained by:

1. making one cross introduction;
2. letting the affected module absorb internally;
3. retaining the introduction precisely when it fixes locally.

This proves the standard separated trace directly from the absorbing linear
system.  In particular, if `P_U^H` and `P_U^A` are the macro fixation
probabilities from `(1,0)` and `(0,1)`, respectively, then

\[
 \boxed{
 \rho_U^0(c,m,q;r)
 ={c+m+1\over N}\rho_U(H_{c,m},r)P_U^H
 +{2q\over N}\rho_U(K_2,r)P_U^A,}                         \tag{12}
\]

where `N=c+m+1+2q`.  Formula (12) is exact in the finite separated limit.

For each compact fitness interval, the Schur-complement convergence is
uniform: all finite denominators stay positive.  Thus, after the finite
parameters have been selected, a positive rational `epsilon` can be chosen
so that the difference between (12) and the actual connected-graph fixation
is arbitrarily small.

## 4. The dilute clique--pendant module

Put

\[
 p(r)=1-{1\over r}.                                      \tag{13}
\]

First take `c=a m` with fixed `a>0` and let `m -> infinity`.  Directly from
the six lumped transition rates of the clique--pendant module:

- a mutant ordinary core vertex establishes with probability `p(r)`;
- after any diverging mesoscopic core seed, fixation follows with
  probability tending to one;
- a dB mutant leaf fixes with probability tending to zero;
- a Bd mutant leaf fixes with probability `ell_r(a)=1-z_r(a)`, where
  `z_r(a)` is the smaller root in `(0,1)` of

\[
 r^2z^2-{r^2+1+r(r-1)a\}z+1=0.                         \tag{14}
\]

Here (14) comes from the killed branching process seen from a rare mutant
leaf.  On the slow leaf time its per-particle birth, death, and successful
core-mark rates, after multiplication by their common factor, are

\[
                 r^2,\qquad1,\qquad r(r-1)a.              \tag{15}
\]

The stopped path convergence follows by resolving successive hub
excursions.  A successful core mark reaches a diverging seed with
probability `p(r)` and then fixes by the preceding post-establishment
statement.  Conditioning an unmarked family on extinction makes it
subcritical, which removes the fixed cutoff in the stopped argument.

All drift gaps in this proof are uniform when `r` lies in a compact subset
of `(1,infinity)`.  Therefore the limits are uniform on such compacts.

Now let `a -> infinity`, equivalently let the leaf proportion tend to zero.
Equation (14) gives

\[
                         \ell_r(a)\longrightarrow1         \tag{16}
\]

uniformly on compact fitness intervals.  Uniform singleton initialization
in the module consequently gives the first-order normalized effects

\[
 \text{one leaf:}\qquad
 \left({1\over r-1},-1\right)                             \tag{17}
\]

for `(Bd,dB)`.  Indeed a leaf replaces a core individual whose limiting
fixation is `p`: under Bd its own fixation tends to one, giving
`1/p-1=1/(r-1)`; under dB its fixation tends to zero, giving `-1`.
The single hub has vanishing initialization mass after the inner population
limit.

## 5. One dilute pair satellite

Let

\[
                         \sigma={c\over W}.                 \tag{18}
\]

Suppose one pair has fixed mutant while the large module is resident.  No
other resident pair can change before this unique gate is resolved.  Listing
the favorable and adverse cross introductions directly gives raw rate
ratios

\[
                         r\sigma\quad(Bd),\qquad
                         {r^2\over\sigma}\quad(dB).         \tag{19}
\]

The favorable core introduction fixes with probability `p(r)+o(1)`.  The
adverse resident introduced into a mutant pair fixes with the exact
reciprocal-fitness `K_2` probability.  Hence the successful gate odds tend
to

\[
 Z_B=\sigma(r^2-1),\qquad
 Z_D={2r(r-1)\over\sigma}.                               \tag{20}
\]

Once the large module is mutant, the chance that any of `O(c)` resident
pairs reverses it before being converted is `o(1)`.  To see this without a
branching heuristic, stop the number of resident core vertices at a fixed
fraction of `c`.  The embedded ratio is at most `r^{-1}+o(1)`, so reaching
that fraction from one resident has probability `exp(-gamma_r c)`.  A union
bound over the pairs and over the `O(q log q)` successful/failed macro
attempts is still `o(1)`.  The core then converts every remaining pair with
probability tending to one.  This proves both macro limits

\[
 P_U^H\longrightarrow1,\qquad
 P_U^A\longrightarrow{Z_U\over1+Z_U}.                     \tag{21}
\]

The estimates are again uniform on compact fitness intervals.

Since

\[
 \rho_{Bd}(K_2,r)={r\over r+1},\qquad
 \rho_{dB}(K_2,r)={1\over2},                              \tag{22}
\]

the normalized effect of replacing two core vertices by one pair is

\[
 b(r,\sigma)
 =2\left\{{\rho_{Bd}(K_2,r)Z_B/(1+Z_B)\over p(r)}-1\right\}
 ={2(\sigma-1)\over1+\sigma(r^2-1)},                       \tag{23}
\]

\[
 d(r,\sigma)
 =2\left\{{\rho_{dB}(K_2,r)Z_D/(1+Z_D)\over p(r)}-1\right\}
 ={2\{r(2-r)-\sigma\}\over\sigma+2r(r-1)}.               \tag{24}
\]

These are exact algebraic simplifications, not fitted coefficients.

## 6. Combined iterated asymptotics

The order of limits is kept explicit.  Fix an integer dilution parameter
`A` and first send `t` to infinity with

\[
 c=At,\qquad q=t,\qquad
 m=\lfloor\lambda t\rfloor.                              \tag{25}
\]

The clique--pendant aspect ratio in Section 4 is then `a=A/lambda`.  If
`ell_r(a)` denotes the Bd leaf value in (14)--(16), direct substitution in
the exact trace (12) gives the finite-`A` scaled corrections

\[
 \Phi_{Bd}(A;r)
 =b(r,\sigma)+\lambda\left\{{\ell_r(A/\lambda)\over p(r)}-1\right\},
                                                                    \tag{26a}
\]

\[
 \Phi_{dB}(A;r)=d(r,\sigma)-\lambda.                    \tag{26b}
\]

Before subtracting the complete baseline, the limiting Bd numerator,
multiplied by `A+lambda+2`, is

\[
 A p(r)+\lambda\ell_r(A/\lambda)
 +2\,{r\over r+1}\,{Z_B\over1+Z_B}.
\]

The corresponding dB expression is `A p(r)+Z_D/(1+Z_D)`.  Thus
(26a)--(26b) retain the complete post-establishment trace rather than adding
independent singleton heuristics.

Now send `A` to infinity.  By (16), `ell_r(A/lambda)` tends to one uniformly
on compact fitness intervals.  The complete-graph baselines derived from
their one-dimensional count chains then give

\[
 \boxed{
 {N\over q}\left\{{\rho_{Bd}(G,r)\over\rho_{Bd}(K_N,r)}-1\right\}
 \longrightarrow
 B(r;\sigma,\lambda)
 :=b(r,\sigma)+{\lambda\over r-1}.}                       \tag{27}
\]

\[
 \boxed{
 {N\over q}\left\{{\rho_{dB}(G,r)\over\rho_{dB}(K_N,r)}-1\right\}
 \longrightarrow
 D(r;\sigma,\lambda)
 :=d(r,\sigma)-\lambda.}                                 \tag{28}
\]

Here and below the arrows mean the iterated limit `t -> infinity` and then
`A -> infinity`.  The convergence is uniform on compact subintervals of
`(1,infinity)`.  The single hub is `o(q)`, the failed post-gate probability
is exponentially small in `c`, and the finite pair-gate errors are `o(1)`
per pair.  Section 7 selects one diagonal on which their sum and the
positive-cut error are `o(q/N)`.

## 7. One fitness-independent diagonal

Here is a deterministic construction of the sequence asserted in the
theorem.  It is written as a least-integer diagonal so the quantifiers are
explicit and the graph never depends on the subsequently chosen fitness.

For `k` sufficiently large put

\[
 I_k=[1+1/k,R_{\rm hyb}-1/k].                            \tag{29}
\]

Define

\[
 \mu_k=\min_{r\in I_k}\min\{B(r;\sigma_*,\lambda_*),
                            D(r;\sigma_*,\lambda_*)\}>0,
 \qquad
 \tau_k=\min\{1/k,\mu_k/8\}.                             \tag{30}
\]

First let `A_k` be the least integer `A>=k` for which both finite-`A`
corrections (26a)--(26b), with `sigma=sigma_*` and `lambda=lambda_*`,
differ from `B,D` by at most `tau_k` throughout `I_k`.  Existence follows
from the compact-uniform outer limit in Section 6.

Having fixed `A_k`, let `t_k` be the least integer `t>=k` for which the
separated finite trace with

\[
 c_k=A_kt,\qquad q_k=t,\qquad
 m_k=\lfloor\lambda_*t\rfloor                           \tag{31}
\]

differs from (26a)--(26b), after multiplication by `N/q_k`, by at most
`tau_k` throughout `I_k`.  Existence follows from the compact-uniform inner
limit.

These are effective definitions.  Formula (14) defines `ell_r` by a
quadratic with a specified root interval, so the first uniform comparison is
an exact real-algebraic decision problem.  For fixed `(A,t)`, both finite
lumped absorbing systems have algebraic rational functions of `r`;
denominator positivity and the second pair of uniform inequalities on the
algebraic interval `I_k` are decidable by exact Sturm and subresultant
arithmetic.

Having fixed `(c_k,m_k,q_k)`, let `e_k` be the least positive integer for
which the actual connected graph with

\[
                         \epsilon_k=2^{-e_k}              \tag{32}
\]

differs from its separated trace, after the same `N/q_k` scaling, by at most
`tau_k` for both rules throughout `I_k`.  Finite Schur-complement continuity
proves existence; the same exact interval procedure makes the least choice
effective.  Thus every vertex count and every edge weight is fixed before
fitness is quantified.  For the finitely many empty intervals in (29), take
any connected graph and continue the sequence afterward.

For any fixed `r in (1,R_hyb)`, eventually `r in I_k`.  The three scaled
errors are at most `3 tau_k<=3 mu_k/8`, so both corrections are strictly
positive.  Moreover,

\[
 {N_k\over q_k}(x_k(r)-1)\longrightarrow
 B(r;\sigma_*,\lambda_*),\qquad
 {N_k\over q_k}(y_k(r)-1)\longrightarrow
 D(r;\sigma_*,\lambda_*).                              \tag{32a}
\]

This is exactly the required order of quantifiers.

A second, simpler count diagonal is independently audited in
`threshold/endpoint_construction_v2`.  It takes `q=t`,
`m=floor(lambda_* t)`, `C=t^4`, and chooses the least dyadic positive
coupling whose scaled cut error is at most `1/t` on `I_t`.  Its
logarithmic-cutoff estimate proves the same `o(q/C)` center-module control.

## 8. Exact optimization and the sextic

For fixed `r,sigma`, positivity of (27)--(28) is equivalent to the existence
of a leaf/pair ratio `lambda` satisfying

\[
 L(r,\sigma)<\lambda<U(r,\sigma),                         \tag{33}
\]

where

\[
 L={2(1-\sigma)(r-1)\over1+\sigma(r^2-1)},\qquad
 U={2\{r(2-r)-\sigma\}\over\sigma+2r(r-1)}.              \tag{34}
\]

Their difference has the sign opposite to the quadratic

\[
 F_r(\sigma)
 =(r-1)\sigma^2+(r^3-4r^2+3r+1)\sigma+r(2r-3).          \tag{35}
\]

The minimizing value is exactly

\[
 \sigma(r)={-r^3+4r^2-3r-1\over2(r-1)},                  \tag{36}
\]

and direct completion of the square gives

\[
                   \min_\sigma F_r(\sigma)
                   =-{P(r)\over4(r-1)}.                   \tag{37}
\]

Sturm's theorem shows that `P` has no root in `(1,3/2)` and exactly one in
`(3/2,151/100)`.  Equations (3)--(4) choose the tangency at that root.
For fixed `sigma_*`, `L` is strictly increasing and `U` strictly decreasing
on `(1,R_hyb)` because

\[
 \partial_rL={2(\sigma-1)\{\sigma(r-1)^2-1\}
                 \over\{1+\sigma(r^2-1)\}^2}>0,
 \qquad
 \partial_rU={4r(\sigma-r)\over\{2r(r-1)+\sigma\}^2}<0. \tag{38}
\]

At `R_hyb` both equal `lambda_*`; below it

\[
                   L(r,\sigma_*)<\lambda_*<U(r,\sigma_*), \tag{39}
\]

so both limits in (32a) are positive.  Just above `R_hyb` both inequalities
reverse.  Therefore `R_hyb` is the exact threshold of this optimized
two-mechanism leading family, although it is only a lower bound for the
unrestricted `R_sim`.

## 9. Verification and status

Run

```bash
./universal_simultaneous_amplification/phase4_landmark_closure/threshold/dilute_pair_leaf_hybrid/replay.sh
```

The verifier checks over exact symbolic arithmetic:

- the sextic root count and isolating interval;
- the quadratic identity (35);
- the optimizer (36) and minimum (37);
- the tangency parameters;
- the derivative factorizations (38).

Classification:

- finite weak-cut trace (12): **PROVED**;
- core--pendant singleton and post-establishment limits: **PROVED**;
- pair gate and post-gate limits: **PROVED**;
- combined `o(q/N)` limits (27)--(28): **PROVED**;
- fitness-independent constructive diagonal: **PROVED**;
- exact hybrid threshold `R_hyb`: **PROVED**;
- universal exact value of `R_sim`: **OPEN**.
