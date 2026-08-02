# Weighted-adjoint level capacities at `r=3/2`

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external communication was used.

## Status

This note gives an exact decomposition of the proposed fixation-product
inequality into two stationary-dual comparisons.  Neither comparison is yet
proved in arbitrary order, so the universal product inequality remains
**OPEN**.  The proved content is:

1. an exact conservative-adjoint intermediate dual and a sufficient two-step
   factorization of the product conjecture;
2. exact entropy-production signs for the two adjoint stationary laws;
3. an exact two-level signed-capacity identity;
4. exact counterexamples to five tempting pointwise/rank strengthenings; and
5. the exact rank-boundary flux identity for the geometric-burst dB dual.

The surviving level-temperature inequalities are explicitly labeled
**CONJECTURAL**.  A stronger rank monotone-likelihood-ratio route is exactly
false.

## 1. The conservative adjoint and the two sufficient factors

Put `a=r-1=1/2` and let `L` be the Bd branching--coalescing dual.  Let `C`
be the conservative generator obtained by reversing every base arrow before
taking the same unbatched dual.  Thus an occupied target `v` samples `u`
from the row `P_v*`; a neutral sample replaces `v` by `u`, while a selective
sample retains `v` and adds `u`.  Let `D` denote the geometric-burst dB dual.

Write

\[
 m_L=\mathbb E_{\pi_L}|A|,\qquad
 m_C=\mathbb E_{\pi_C}|A|,\qquad
 m_D=\mathbb E_{\pi_D}|A|.
\]

For the complete graph, the unbatched reference law is

\[
 \bar\mu(A)={a^{|A|}\over Z_\mu},\qquad
 Z_\mu=(1+a)^n-1,
\]

and its mean is

\[
 m_B^K={na(1+a)^{n-1}\over(1+a)^n-1}.
\]

The complete dB burst law is proportional to `(n-|A|)a^|A|`, with mean

\[
 m_D^K={(n-1)a(1+a)^{n-2}\over(1+a)^{n-1}-1}.
\]

Consequently the following two inequalities would imply the desired exact
fixation-product bound:

\[
 \boxed{m_Lm_C\le (m_B^K)^2,}                         \tag{1}
\]

\[
 \boxed{{m_D\over m_C}\le {m_D^K\over m_B^K}.}       \tag{2}
\]

Indeed, uniform-singleton fixation is stationary dual mean divided by `n`.
The stronger arithmetic version

\[
 \boxed{m_L+m_C\le2m_B^K}                             \tag{3}
\]

would imply (1) by AM--GM.  Targeted exact checks and separated-scale
optimization through order five support (2)--(3), with equality in (3) for
symmetric link dynamics.  These computations are diagnostics, not proofs.

## 2. Exact weighted-adjoint entropy signs

For a set `A`, write

\[
 A_\partial(A)=\sum_{i\in A,j\notin A}P_{ij},\qquad
 B_\partial(A)=\sum_{i\in A,j\notin A}P_{ji},
\]

and

\[
 V(A)=r\{A_\partial(A)-B_\partial(A)\}.
\]

There is a useful exact simplification of this defect.  If

\[
 t_i=\sum_jP_{ji},\qquad q_i=1-t_i,
\]

then row stochasticity gives

\[
 \boxed{
 A_\partial(A)-B_\partial(A)=\sum_{i\in A}(1-t_i),
 \qquad V(A)=r\sum_{i\in A}q_i,
 \qquad \sum_iq_i=0.}                                \tag{4a}
\]

Thus, up to the fixed factor `r`, the entire adjoint defect is a linear
zero-sum vertex potential.  In particular its uniform average on every
rank is zero.

The already verified weighted-adjoint identity is

\[
 L^{\dagger_\mu}=C+V.                                 \tag{4}
\]

Let `f=pi_L/mu` and `g=pi_C/mu`; normalization constants are irrelevant in
this section.  Stationarity and the adjoint of (4) give the pointwise density
equations

\[
 Cf=-Vf,\qquad Lg=Vg.                                  \tag{5}
\]

For a generator `Q` and a positive function `z`, define

\[
 \mathcal I_Q(z)(A)=
 \sum_{B\ne A}Q(A,B)
 \left\{{z(B)\over z(A)}-1-log {z(B)\over z(A)}\right\}.
\]

Every summand is nonnegative.  The elementary identity

\[
 Q\log z={Qz\over z}-\mathcal I_Q(z)
\]

and stationarity yield the exact entropy-production formulas

\[
 \boxed{
 \mathbb E_{\pi_C}V=-\mathbb E_{\pi_C}\mathcal I_C(f)\le0,
 \qquad
 \mathbb E_{\pi_L}V=\mathbb E_{\pi_L}\mathcal I_L(g)\ge0.} \tag{6}
\]

Equality forces the relevant density ratios to be one along every
state-space edge.  Thus the two stationary laws tilt in rigorously opposite
directions under the sole adjoint defect `V`.  Formula (6) is global; taking
its terms level by level is not automatically valid.

### 2.1 Why conditioning or killing at one rank does not prove the level signs

The obstruction to localizing (6) can be written exactly.  Let
`R_k={A:|A|=k}` and put

\[
 \psi_L=\log g,\qquad \psi_C=\log f.
\]

Applying the pointwise logarithmic identities before summing over one rank
gives

\[
\begin{aligned}
 \sum_{A\in R_k}\pi_L(A)V(A)
 &=\mathcal B^L_k+\mathcal R^L_k,\\
 -\sum_{A\in R_k}\pi_C(A)V(A)
 &=\mathcal B^C_k+\mathcal R^C_k,                    \tag{6a}
\end{aligned}
\]

where

\[
\begin{aligned}
 \mathcal B^L_k&=\sum_{A\in R_k}\pi_L(A)L\psi_L(A),&
 \mathcal R^L_k&=\sum_{A\in R_k}\pi_L(A)\mathcal I_L(g)(A)\ge0,\\
 \mathcal B^C_k&=\sum_{A\in R_k}\pi_C(A)C\psi_C(A),&
 \mathcal R^C_k&=\sum_{A\in R_k}\pi_C(A)\mathcal I_C(f)(A)\ge0.
\end{aligned}
\]

For either pair `(Q,pi,psi)=(L,pi_L,psi_L)` or
`(C,pi_C,psi_C)`, stationarity cancels every internal-rank term and leaves
the following precise boundary forcing:

\[
 \boxed{
 \mathcal B^Q_k
 =\sum_{\substack{A\in R_k\\B\notin R_k}}
 \{\pi(A)Q(A,B)\psi(B)-\pi(B)Q(B,A)\psi(A)\}.}       \tag{6b}
\]

Equivalently, if `J_AB=pi(A)Q(A,B)-pi(B)Q(B,A)` and
`H_AB=pi(A)Q(A,B)+pi(B)Q(B,A)`, each oriented boundary edge contributes

\[
 {1\over2}J_{AB}\{\psi(A)+\psi(B)\}
 +{1\over2}H_{AB}\{\psi(B)-\psi(A)\}.               \tag{6c}
\]

Neither summand has a prescribed sign.  Killing the chain on exit from
`R_k` does not remove (6b): the conditional restriction of `pi` is not
stationary for the killed block, and neighboring ranks inject exactly this
source term.  Numerically, on the exact unweighted `K_(1,4)` input,
`B^L_3` is approximately `-0.00373981` and `B^C_2` is approximately
`-0.0382479`, while the corresponding entropy remainders are positive and
larger.  Thus the conditional-entropy attempt leaves a genuinely
sign-indefinite boundary term; a successful version would have to bound its
negative part by `R^Q_k`, not merely discard it.

## 3. Exact two-level capacity identity

Now normalize `f=pi_L/bar(mu)` and `g=pi_C/bar(mu)` and set

\[
 h=f+g,\qquad d=f-g.
\]

For `|A|=k`, put

\[
 C_0(A)={A_\partial(A)+B_\partial(A)\over2},\qquad
 I(A)=k-A_\partial(A).
\]

The L dual has rank-up rate `a B_partial(A)` and rank-down rate `I(A)`.
The C dual has rank-up rate `a A_partial(A)` and the same rank-down rate
`I(A)`.  Stationary flux across the boundary between ranks `k` and `k+1`
therefore gives

\[
 \boxed{
 \sum_{|A|=k}\{B_\partial(A)f(A)+A_\partial(A)g(A)\}
 =\sum_{|B|=k+1}I(B)h(B).}                             \tag{7}
\]

Equivalently,

\[
 \boxed{
 \sum_{|A|=k}C_0(A)h(A)-\sum_{|B|=k+1}I(B)h(B)
 ={1\over2}\sum_{|A|=k}
 \{A_\partial(A)-B_\partial(A)\}d(A).}               \tag{8}
\]

The midpoint `M=(L+C)/2` is the dual with symmetric link rates
`(P_ij+P_ji)/2`, and is reversible under `bar(mu)`.  Thus (8) says exactly
that the signed temperature covariance on its right is the net rank-`k`
capacity flux of the combined density `h` under `M`.

Let

\[
 h_k={1\over{n\choose k}}\sum_{|A|=k}h(A),\quad
 B_0(k)={k(n-k)\over n-1},\quad
 I_0(k+1)={k(k+1)\over n-1}.
\]

Since `B_0(k) binom(n,k)=I_0(k+1) binom(n,k+1)`, (8) gives the fully
explicit adjacent-rank identity

\[
\boxed{
\begin{aligned}
 B_0(k){n\choose k}(h_k-h_{k+1})
 &=\sum_{|A|=k}\{B_0(k)-C_0(A)\}h(A)\\
 &\quad+\sum_{|B|=k+1}\{I(B)-I_0(k+1)\}h(B)\\
 &\quad+{1\over2r}\sum_{|A|=k}V(A)d(A).
\end{aligned}}                                        \tag{9}
\]

The exact and numerical diagnostics support the stronger statements

\[
 \sum_{|A|=k}f(A)V(A)\ge0,
 \qquad
 \sum_{|A|=k}g(A)V(A)\le0                              \tag{10}
\]

for every `k`, and hence the nonnegativity of the last line of (9).
The inequalities (10) are **OPEN**.  Optimization aimed directly at
violating each individual level sign in (10), through order five and over
edge scales `exp(+-8)`, returned only the symmetric equality locus.

### 3.1 Linear vertex-marginal form of the level conjecture

Formula (4a) reduces (10) to only `n` conditional inclusion marginals.  Set

\[
 p^L_{i,k}=\Pr_{\pi_L}\{i\in A\mid |A|=k\},\qquad
 p^C_{i,k}=\Pr_{\pi_C}\{i\in A\mid |A|=k\}.
\]

Because `bar(mu)` is constant on each rank,

\[
\begin{aligned}
 \sum_{|A|=k}f(A)V(A)
 &= {rZ_\mu\pi_L(R_k)\over a^k}\sum_iq_i p^L_{i,k},\\
 \sum_{|A|=k}g(A)V(A)
 &= {rZ_\mu\pi_C(R_k)\over a^k}\sum_iq_i p^C_{i,k}. \tag{11}
\end{aligned}
\]

Hence (10) is exactly the pair of aggregate covariance inequalities

\[
 \sum_iq_i p^L_{i,k}\ge0,
 \qquad \sum_iq_i p^C_{i,k}\le0.                    \tag{11a}
\]

This is a substantive reduction from set densities to vertex Palm
marginals.  It does not, however, close by a pairwise rearrangement.  Since
`sum_i q_i=0`,

\[
 \sum_iq_ip_i={1\over n}\sum_{i<j}(q_i-q_j)(p_i-p_j), \tag{11b}
\]

but the individual summands need not have the desired sign.  On the
weighted `K_4` with lexicographically ordered edge weights

\[
 (w_{01},w_{02},w_{03},w_{12},w_{13},w_{23})=(1,1,2,3,1,2),
\]

the Bd-dual singleton level has

\[
 (q_1-q_3)(p^L_{1,1}-p^L_{3,1})
 =-{46269978481148084\over249339373524498200277}<0,  \tag{11c}
\]

even though the total covariance in (11a) is positive.  Thus (4a) sharpens
the target and suggests a vertex-Palm or exchange argument, but vertexwise
monotone ordering is already exactly false.

For clarity, if the now-falsified rank MLR statement
`h_1>=...>=h_n` had held, (3) would have followed immediately.  Indeed, with

\[
 p_k={\binom nk a^k\over Z_\mu},
\]

normalization gives `sum p_k h_k=2`, while

\[
 2m_B^K-(m_L+m_C)
 =\sum_{i<j}p_ip_j(j-i)(h_i-h_j).                     \tag{12}
\]

The sign of the temperature term alone, even cumulatively over ranks, does
not control (12): (8) controls a conductance-weighted boundary average,
while (12) uses uniform averages within each rank.  The exact star
counterexample below confirms this gap within the actual graph class.  The
two dispersion terms in the first two lines of (9), or the full stationary
equations, remain essential.

### 3.2 Exact reversible Poisson reduction

There is a sharper exact formulation of the remaining sum problem.  Put

\[
 M={L+C\over2},\qquad K={L-C\over2},\qquad
 \kappa(A)=|A|-m_B^K.
\]

The midpoint `M` is reversible under `bar(mu)`.  Let `phi` be the unique
`bar(mu)`-mean-zero solution of

\[
 M\phi=\kappa.                                         \tag{13}
\]

The density equations (5) give

\[
 Mh=(K-V)d.                                            \tag{14}
\]

Moreover `(K-V)^(dagger_mu)=-K`, directly from (4).  Self-adjointness of
`M` therefore yields

\[
 \boxed{
 2m_B^K-m_L-m_C=\langle K\phi,d\rangle_{\bar\mu}.}    \tag{15}
\]

This is an exact occupation/capacity reduction of the adjoint sum.
Attractiveness of the symmetric-link dual gives the semigroup formula

\[
 \phi(A)=-\int_0^\infty
 \{\mathbb E_A|A_t|-m_B^K\}\,dt.                     \tag{16}
\]

Hence `phi(A)>=phi(B)` whenever `A` is contained in `B`.  If `F(k)` is a
cardinality function, then

\[
 KF(A)=-{a\over2r}V(A)\{F(k+1)-F(k)\}.               \tag{17}
\]

Thus the rank-average part of `phi` has the desired sign under (10).
The within-rank remainder cannot be omitted: on `K_(1,4)`, its contribution
to (15) is approximately `-0.82812`, while the radial contribution is
approximately `0.98483`, leaving the exact positive total approximately
`0.15671`.  A closure must quantitatively dominate this negative
within-rank term using the reversible Dirichlet form or conditional entropy.

### 3.3 A proved triangle rank boundary

Although rank MLR is false in general, its top boundary is exactly provable
for every positive weighted triangle.  Let the three edge weights be
`x,y,z`, and put

\[
 e_1=x+y+z,\qquad e_2=xy+xz+yz,\qquad e_3=xyz.
\]

Direct symbolic solution of `L` and `C` gives

\[
 h_2-h_3={95\mathcal P(x,y,z)\over\mathcal Q(x,y,z)}, \tag{18}
\]

where every coefficient of `Q` is positive and

\[
 \mathcal P=e_1^3e_3+56e_1^2e_2^2-60e_1e_2e_3-149e_2^3. \tag{19}
\]

For fixed `e_1,e_2`, this symmetric polynomial is affine in `e_3`.  The
feasible values of `e_3` form an interval: at an endpoint, the cubic with
roots `x,y,z` has either a zero root or a repeated root.  On those two
boundaries,

\[
 \mathcal P(x,y,0)=x^2y^2(56x^2-37xy+56y^2)>0,
\]

and

\[
 \mathcal P(x,t,t)
 =3t^2(x-t)^2(75x^2+88xt+25t^2)\ge0.                 \tag{20}
\]

The first quadratic is positive because its discriminant is negative.
Affineness in `e_3` now proves `P>=0` throughout the positive cone, with
equality only at `x=y=z`.  Hence

\[
 \boxed{h_2\ge h_3\quad\text{for every weighted triangle},}
\]

strictly unless all three weights are equal.  The lower boundary `h_1-h_2`
has a much larger symmetric numerator and remains uncertified by this route.
The same polynomial also appears in the top-level temperature conjecture:
the numerator of

\[
 -\sum_{|A|=2}g(A)V(A)
\]

is exactly `855 P`, again over a positive-coefficient denominator.  Thus the
second inequality in (10) is proved on the top proper level of every
weighted triangle.

## 4. Exact failures of stronger shortcuts

Five plausible strengthenings are false.

1. **Level-mean product fails on a triangle.**  For edge weights `(1,4,2)`,
   at level one,

   \[
   \left({1\over3}\sum_{|A|=1}f(A)\right)
   \left({1\over3}\sum_{|A|=1}g(A)\right)-1
   ={1163361305883\over19038384631138}>0.
   \]

2. **Pointwise tilt alignment fails on the four-star.**  At the state made
   of three leaves,

   \[
   (f-g)V=-{15080\over76923}<0.
   \]

3. **Pointwise density product fails at order five.**  On the complete
   support with upper-triangular integer weights

   \[
   (1,60000,500000,1500000,1000000,70000,250,1,2,6000),
   \]

   listed in lexicographic edge order, the singleton state `{3}` satisfies

   \[
   f(\{3\})g(\{3\})-1>0.0049.
   \]

4. **Rank MLR fails on the unweighted five-star.**  For `K_(1,4)`,

   \[
   h_4-h_3={126581643\over905995090}>0.
   \]

   Nevertheless the desired adjoint sum has the strict correct sign:

   \[
   2m_B^K-m_L-m_C
   ={14979081573\over95582481995}>0.
   \]

5. **Pairwise vertex-marginal alignment fails at order four.**  The exact
   weighted complete graph in (11c) has a negatively aligned vertex pair on
   the Bd-dual singleton level, although its aggregate level covariance has
   the conjectured positive sign.

All five statements are checked over exact rationals by the companion
verifier.  Thus AM--GM must be applied only after a genuinely global or
rank-capacity estimate.

## 5. Exact burst boundary flux for `D`

The dB burst can cross several ranks upward, so its analogue of (7) is a
boundary, rather than adjacent-edge, identity.  For an occupied target `v`
in `A`, let `U_v` be the union of a geometric number of independent row
`P_v*` samples and put

\[
 F_v(A)=(A\setminus\{v\})\cup U_v.
\]

For a rank boundary `k`, define

\[
 U_k^D(A)=\sum_{v\in A}\Pr\{|F_v(A)|>k\},\quad |A|\le k,
\]

and

\[
 D_k^D(A)=\sum_{v\in A}\Pr\{|F_v(A)|\le k\},\quad |A|>k.
\]

Since one burst removes only its target, downward crossing is possible only
from rank `k+1`.  If

\[
 x_v(A)=\sum_{u\notin A}P_{vu},
\]

then the exact geometric generating function gives

\[
 \boxed{
 D_k^D(A)=\sum_{v\in A}{1-x_v(A)\over1+a x_v(A)},
 \qquad |A|=k+1.}                                     \tag{21}
\]

Stationarity of `D` therefore gives

\[
 \boxed{
 \sum_{j\le k}\sum_{|A|=j}\pi_D(A)U_k^D(A)
 =\sum_{|B|=k+1}\pi_D(B)
 \sum_{v\in B}{1-x_v(B)\over1+a x_v(B)}.}             \tag{22}

\]

For `C`, the corresponding exact boundary identity is simply

\[
 \boxed{
 a\sum_{|A|=k}\pi_C(A)A_\partial(A)
 =\sum_{|B|=k+1}\pi_C(B)I(B).}                        \tag{23}
\]

The complete graph makes (22)--(23) agree after the hole-Palm tilt
`(n-|A|)a^|A|`.  On an arbitrary graph, the multi-rank upward term in (22)
and the collision denominators on its right are the unresolved batching
capacity.  A rank ordering strong enough to prove (2) has not yet been
found: simple ratios of the `D` likelihood to the `C` likelihood are not
monotone even on the four-star.

## 6. Verification

`verify_adjoint_diagnostics.py` independently builds `L` and `C`, solves
their exact stationary equations, checks (4a), (5), (6b), (8), and the five
rational counterexamples above.  `verify_triangle_top_rank.py` reconstructs
both symbolic triangle laws and verifies (18)--(20), including denominator
positivity.  `search_adjoint_split.py` and `search_rank_mlr.py` are discovery
programs only.
