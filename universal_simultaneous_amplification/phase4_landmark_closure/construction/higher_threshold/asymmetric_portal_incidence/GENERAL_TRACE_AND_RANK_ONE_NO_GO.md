# The asymmetric portal trace and a rank-one no-go theorem

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.  Every transition below
is derived from the atomic Bd and dB rules.  This is a class obstruction,
not a universal theorem about arbitrary weighted graphs.

## 1. General asymmetric model

Fix `Q` portal vertices `o_1,...,o_Q` and `T` blade types.  Among `s`
unit-weight strong pairs, let the proportion of type `t` converge to
`pi_t>0`.  An endpoint of a type-`t` blade is joined to portal `a` with
weight

\[
 {\lambda_{at}\over s},\qquad \lambda_{at}\geq0.       \tag{1}
\]

The portals have an arbitrary fixed symmetric network
`h_ab=h_ba>=0`.  Put

\[
 B_a=2\sum_t\pi_t\lambda_{at},\qquad
 d_a=B_a+\sum_{b\ne a}h_{ab}.                         \tag{2}
\]

We assume `B_a>0` and that the displayed support is connected.  Thus `d_a`
is the limiting weighted degree of portal `a`.  No exchangeability is
assumed.

### The exact portal-subset episode

Let `A` be the nonempty set of mutant portals during an episode.  Directly
from Bd updating, a mutant portal `a in A` becomes resident at rate

\[
 \delta^B_a(A)=B_a+\sum_{b\notin A}{h_{ab}\over d_b},                 \tag{3}
\]

while a resident portal `b notin A` becomes mutant at rate

\[
 \upsilon^B_b(A)=r\sum_{a\in A}{h_{ab}\over d_a}.                   \tag{4}
\]

The first term in (3) is resident-blade reproduction into `a`; the second
is resident-portal reproduction.  Successful type-`t` children are marked
at rate

\[
 \beta^B_t(A)= {2\pi_t r^2\over r+1}
                 \sum_{a\in A}{\lambda_{at}\over d_a}.              \tag{5}
\]

For dB, fitness enters the normalization at the dying portal.  The exact
rates are

\[
 \delta^D_a(A)=
 {B_a+\sum_{b\notin A}h_{ab}\over
  B_a+\sum_{b\notin A}h_{ab}
       +r\sum_{b\in A\setminus\{a\}}h_{ab}},                         \tag{6}
\]

\[
 \upsilon^D_b(A)=
 {r\sum_{a\in A}h_{ab}\over
  B_b+\sum_{c\notin A,\ c\ne b}h_{bc}
       +r\sum_{a\in A}h_{ab}},                                      \tag{7}
\]

and

\[
 \beta^D_t(A)=\pi_t r\sum_{a\in A}\lambda_{at}.                    \tag{8}
\]

The factor `1/2` for resolution of a dB singleton has already been included
in (8).

For `U in {B,D}`, let `F^U_A(z_1,...,z_T)` be the joint PGF of successful
children before the portal set next becomes empty.  With `F_empty=1`, the
complete `2^Q-1` state system is

\[
 \left\{\sum_{a\in A}\delta^U_a(A)
        +\sum_{b\notin A}\upsilon^U_b(A)
        +\sum_t\beta^U_t(A)(1-z_t)\right\}F^U_A
 =\sum_{a\in A}\delta^U_a(A)F^U_{A\setminus\{a\}}
  +\sum_{b\notin A}\upsilon^U_b(A)F^U_{A\cup\{b\}}.                \tag{9}
\]

This is an exact finite phase-type transform.  In particular, portal
identity is retained and no count-lumping assumption is present.

### The exact multitype lifetime law

A clean mutant blade of type `t` seeds portal `a` and dies successfully at
the following leading rates:

\[
 e^B_{ta}={2r\lambda_{at}\over s},\qquad
 \mu^B_t={2\over (r+1)s}\sum_a{\lambda_{at}\over d_a},               \tag{10}
\]

\[
 e^D_{ta}={2r\lambda_{at}\over s d_a},\qquad
 \mu^D_t={1\over rs}\sum_a\lambda_{at}.                             \tag{11}
\]

For example, the successful dB death rate in (11) is obtained by an
external resident replacing one endpoint at total rate
`2 sum_a lambda_at/(rs)`, followed by resident resolution of the resulting
singleton with probability `1/2`.

The total lifetime-offspring PGF of a type-`t` parent is therefore

\[
 D^U_t(\mathbf z)=
 {\mu^U_t\over
  \mu^U_t+\sum_a e^U_{ta}\{1-F^U_{\{a\}}(\mathbf z)\}}.              \tag{12}
\]

If `q^U` is the minimal fixed point of this multitype PGF, the limiting
establishment bounds from uniform initialization are

\[
 \alpha_B={r\over r+1}\sum_t\pi_t(1-q^B_t),\qquad
 \alpha_D={1\over2}\sum_t\pi_t(1-q^D_t).                            \tag{13}
\]

For every fixed cutoff `K`, the finite chain stopped when the number of
clean mutant blades reaches `0` or `K` converges to this trace.  Indeed,
heterotypic blades resolve in order-one time; an external intervention,
overlapping episode, or child collision below the cutoff has probability
`O(K/s)` per collapsed event; and the fixed finite portal chain has an
exponential episode tail.  The killed process below `K` has finite expected
event count, so the accumulated error is `o(1)`.  Fixation requires reaching
every fixed `K`.  Letting first `s` and then `K` tend to infinity gives

\[
 \limsup_{s\to\infty}\rho_U(G_s,r)\leq\alpha_U.                      \tag{14}
\]

Thus (13) is used only as an establishment upper bound.  No independent
genealogy or establishment-implies-fixation assertion is made.

## 2. A fully nonexchangeable rank-one theorem

Set all portal-network edges to zero, but allow arbitrary positive portal
loads.  More generally than one blade class, assume the incidence matrix
has rank one:

\[
 \lambda_{at}=c_a v_t,\qquad c_a>0,\quad v_t>0.                    \tag{15}
\]

There is no symmetry among the `c_a`.  Let

\[
 \bar v=\sum_t\pi_t v_t,qquad B_a=2c_a\bar v.                       \tag{16}
\]

Although the portal vertices have no direct edges, the graph is connected:
every portal is joined through every strong-pair blade to every other
portal.

**PROVED (arbitrary finite portal count and arbitrary unequal loads).**
For every `Q>=1`, every positive `c_a,v_t,pi_t`, and every `r>1`, the family
(15) cannot asymptotically amplify both update rules.  At least one rule has

\[
 \limsup_{s\to\infty}\rho_U(G_s,r)<1-{1\over r}.                    \tag{17}
\]

The parameters are completely independent of fitness.  The conclusion is
pointwise in `r`, so allowing arbitrary portal-specific weights does not
improve the simultaneous interval within this rank-one, portal-separated
regime.

## 3. Scalar reduction and exact sign tests

Under (15), every parent type has the same lifetime law after a harmless
time change, and every child type is sampled from

\[
 \eta_t={\pi_t v_t\over\bar v}.                                     \tag{18}
\]

Consequently the extinction vector is constant and (12) reduces exactly
to a scalar PGF.  A portal-`a` episode has

\[
 F^B_a(z)={B_a\over B_a+{r^2\over r+1}(1-z)},                       \tag{19}
\]

\[
 D_B(z)={Q\over Q+r(r+1)\sum_aB_a\{1-F^B_a(z)\}},                   \tag{20}
\]

and

\[
 F^D_a(z)={1\over1+{rB_a\over2}(1-z)},                              \tag{21}
\]

\[
 D_D(z)={\sum_aB_a\over
              \sum_aB_a+2r^2\sum_a\{1-F^D_a(z)\}}.                \tag{22}
\]

For a scalar PGF, its smallest fixed point lies below `z in (0,1)` exactly
when `D(z)<z`.  Bd establishment exceeds `p=1-1/r` exactly when its
extinction root lies below

\[
 z_B={1\over r^2}.                                                     \tag{23}
\]

Substitution into (19)--(20) gives the exact criterion

\[
 \alpha_B>p
 \quad\Longleftrightarrow\quad
 \sum_a\Phi_B(B_a)>0,qquad
 \Phi_B(B)={B-1\over B+r-1}.                                        \tag{24}
\]

For `1<r<2`, dB establishment exceeds `p` exactly when its extinction root
lies below

\[
 z_D={2-r\over r}.                                                     \tag{25}
\]

Equations (21)--(22) give

\[
 \alpha_D>p
 \quad\Longleftrightarrow\quad
 \sum_a\Phi_D(B_a)>0,qquad
 \Phi_D(B)=
 {B(1+r-r^2-B)\over1+(r-1)B}.                                       \tag{26}
\]

The two portal contributions satisfy the pointwise identity

\[
 \Phi_B(B)+\Phi_D(B)
 =-{\mathcal N_r(B)\over
       (B+r-1)\{1+(r-1)B\}},                                        \tag{27}
\]

where

\[
 \mathcal N_r(B)=
 (B-1)^2(B+1)
 +(r-1)B^2
 +(r-1)^2B(B+1)
 +(r-1)^3B.                                                          \tag{28}
\]

Every denominator is positive and `N_r(B)>0` for `r>1,B>0`.  Summing
(27) over the portals proves that the two strict conditions (24) and (26)
cannot hold simultaneously.  In fact, at least one sum is strictly
negative, which gives the strict inequality in (17) through (14).

For `r>=2`, dB has entrance factor `1/2<=p`; at `r=2` its extinction
probability is still positive because every parent has a positive death
rate.  Hence dB is strictly below `p` and the remaining fitness range is
also covered.

## 4. What the theorem does and does not close

The theorem permits an arbitrary finite number of unequal portals and an
arbitrary positive rank-one blade profile.  It therefore rules out the
most direct strategy of assigning a spectrum of portal loads to one common
strong-pair population.

It does **not** cover a genuinely higher-rank incidence matrix.  That case
has the full multitype law (9)--(13).  The obstruction above cannot simply
be applied type by type: at `r=8/5`, a portal with `B=1/100` has
`Phi_D>0>Phi_B`, while a portal with `B=2` has `Phi_B>0>Phi_D`.  Separate
blade types can therefore select opposite portal regimes.  Whether the
coupled multitype fixed point can turn those opposite local gains into two
uniformly averaged establishment gains remains open.

Discovery optimization retaining all `2^Q-1` portal subsets found no
positive simultaneous gap for `Q<=3`, `T<=3` at `r=8/5`; the best values
collapsed toward an effectively rank-one environment.  This is only
**NUMERICALLY OBSERVED** and is not used in the theorem.

The broader portal-network inequality suggested by the experiments is

\[
 r d_a H^B_a+r^2(2-r)H^D_a
 \le (r-1)(1+d_a),                                                    \tag{29}
\]

where `H^U_a` is the special-mark killing probability from singleton
portal `a`.  It survived random tests but has not been proved and is marked
**OPEN**.  Even (29), if true, resolves only rank-one parent incidence;
higher-rank averaging needs an additional argument.
