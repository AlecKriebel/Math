# The `R_hyb` compactness reduction and its first dual-moment lemma

Date: 2026-08-13 (America/Los_Angeles)

No literature search, graph optimization, or external communication was used.

## 1. Status

This note makes three exact advances.

1. It corrects the sequence-level endpoint statement.  A `liminf` inequality
   does not exclude dilute amplifiers whose two gains are positive but tend to
   zero.
2. It states a response-scale trace compactness theorem with the hypotheses
   that are actually needed.  In particular, exceptional vertices must be
   eliminated by a Schur trace, not deleted from the dynamics.
3. For every bounded separated module it reduces the entire endpoint
   separator problem to one sharp inequality involving only mean ranks and
   portal-weighted singleton atoms of the two exact stationary OR duals.

The reduction is **PROVED**.  The resulting dual-moment inequality is
**OPEN**.  The strong pair `K_2` is an exact equality case at `R_hyb`; its
discriminant is precisely `r^2 P(r)`, where `P` is the hybrid sextic.

## 2. The correct sequence statement

Fix `R=R_hyb` and, for a graph `G` of order `n`, write

\[
 X_G={\rho_{Bd}(G,R)\over\rho_{Bd}(K_n,R)},\qquad
 Y_G={\rho_{dB}(G,R)\over\rho_{dB}(K_n,R)}.             \tag{1}
\]

If `R_sim>R`, one fitness-independent graph family is eventually a strict
amplifier at the fixed fitness `R`.  Thus the sequence statement needed for
an upper bound is

\[
 \boxed{\text{no graph sequence is eventually contained in }
                    \{X>1,Y>1\}.}                       \tag{2}
\]

Equivalently, every graph sequence has infinitely many indices at which
`min(X,Y)<=1`.  The weaker assertion

\[
                    \liminf_k\min(X_{G_k},Y_{G_k})\le1   \tag{3}
\]

is not sufficient: `X_k=Y_k=1+1/k` satisfies (3) and is nevertheless
strictly amplifying at every index.  This is not a cosmetic distinction;
all known dilute constructions have vanishing normalized gain.

For a hypothetical sequence satisfying (2) in the wrong direction, put

\[
 \Delta_k=(X_{G_k}-1,Y_{G_k}-1),\qquad
 \epsilon_k=\|\Delta_k\|_\infty.                        \tag{4}
\]

Then a subsequence of `Delta_k/epsilon_k` converges in the compact set

\[
 \{(u,v):u,v\ge0,\ \max(u,v)=1\}.                       \tag{5}
\]

Consequently a useful tangent theorem must approximate fixation with error
`o(epsilon_k)`, the **actual first nonzero response scale**.  An expansion
with error merely `o(module density)` can lose all information after a
leading pair--leaf cancellation.

## 3. Exceptional vertices: trace, not deletion

Let `E` be a set of vertices.  Deleting only the *initializations* in `E`
changes a uniformly averaged fixation probability by at most `|E|/n`, since
every committor lies in `[0,1]`.  Therefore initializations in `E_k` are
negligible at the response scale only under

\[
                         {|E_k|\over n_k\epsilon_k}\to0. \tag{6}
\]

The weaker condition `|E_k|=o(n_k)` is not enough.

More importantly, deleting `E` from the **dynamics** has no such bound.  A
single hub can mediate every transition between a positive number of leaves
and the bulk.  The proved hybrid itself has a one-vertex hub with vanishing
uniform-start mass and leading-order dynamical influence.  Thus an
exceptional set must be retained in the macro chain after the fast states
are Schur-eliminated.  Literal vertex deletion is not a valid compactness
operation.

## 4. A precise trace-compactness dichotomy

The following is the minimal structural theorem suggested by the exact
weak-cut calculations.  It is stated as a target, not as a proved theorem.

> **Response-scale trace dichotomy (target).**  Let `G_k` be an eventually
> simultaneous endpoint sequence and let `epsilon_k` be (4).  After a
> subsequence there are source-negligible exceptional sets `E_k` satisfying
> (6) and one of the following alternatives.
>
> **Bulk alternative.**  A nonvanishing fraction of the update activity
> remains between nonabsorbed blocks.  After removal of row atoms and
> temperature outliers of `o(n_k epsilon_k)` source mass, the induced kernels
> have a compact finite-type/diffuse limit.  The normalized fixation germ is
> then governed by a finite-order bulk obstruction.
>
> **Dilute alternative.**  The complement of `E_k` has a partition into
> internally absorbing modules.  Uniformly for both update rules, a module
> absorbs before the next boundary event with failure probability whose
> uniformly averaged contribution is `o(epsilon_k)`.  Simultaneous boundary
> events and intermodule interactions also contribute `o(epsilon_k)`.  The
> exact Schur trace, with `E_k` retained as a macro reservoir, puts every
> nonzero limit of `Delta_k/epsilon_k` in the closed response-germ cone of
> the isolated modules.

The dilute conclusion follows directly under its displayed assumptions.
For a finite absorbing generator, eliminate the fast mixed-module block by
its Schur complement.  Every retained transition is then exactly one
boundary introduction, isolated local absorption, and a macro transition.
The assumed `o(epsilon_k)` bound makes the resolvent error negligible after
division by (4).  Nonnegative module counts give a nonnegative response
measure, and subsequential compactness gives its closed-cone limit.

What is not proved is that every arbitrary graph sequence admits this
dichotomy.  Two uniformities are indispensable:

1. absorption/trace error must be small relative to `epsilon_k`, not merely
   relative to vertex density;
2. growing modules require tightness of their full trace data, not only of
   their orders, degrees, or first moments.

Even for bounded modules, the first local inequality needed to identify the
closed cone was previously missing.  It is isolated next.

## 5. Exact OR-dual coordinates of one bounded module

Fix `r>1`.  Let `H` be a connected loopless undirected weighted graph on
`s>=2` vertices, with internal degrees `d_i`, and let `x_i>0` be portal
loads.  For `U in {Bd,dB}`, let `mu_U` be the stationary law of the exact OR
dual of the isolated rule-`U` process at fitness `r`, started from all
vertices.  Put

\[
 m_U=E_{\mu_U}|A|,\qquad q_{U,i}=\mu_U(A=\{i\}).          \tag{7}
\]

Boolean duality and type complementation give exactly

\[
 h_U^+(i)=\Pr_{\mu_U}(i\in A),\qquad
 h_U^-(i)=1-h_U(V\setminus\{i\};r)=q_{U,i}.              \tag{8}
\]

Hence the isolated uniform fixation probability is `m_U/s`, while every
reciprocal-invasion term is a singleton atom of the same fitness-`r` dual.

Define the two portal laws

\[
 \gamma_i={x_i\over\sum_jx_j},\qquad
 \alpha_i={x_i/d_i\over\sum_jx_j/d_j},                  \tag{9}
\]

and their singleton averages

\[
 q_B=\sum_i\gamma_iq_{Bd,i},\qquad
 q_D=\sum_i\alpha_iq_{dB,i}.                            \tag{10}
\]

The exact separated-module invariant becomes

\[
 \boxed{K={r(r-1)^2\over q_Bq_D}.}                      \tag{11}
\]

Indeed, (11) is just the normal-form product

\[
 {r(r-1)^2(\sum x_i/d_i)(\sum x_i)\over
   (\sum x_iq_{Bd,i})(\sum (x_i/d_i)q_{dB,i})}.
\]

Let `z>0` be the free Bd gate odds, so the dB gate odds are `K/z`.  With

\[
 b={m_{Bd}\over s}=\rho_{Bd}(H,r),\qquad
 a={m_{dB}\over s(r-1)}={\rho_{dB}(H,r)\over r-1},       \tag{12}
\]

the normalized response of the module is

\[
 B=s\left\{{rb\over r-1}{z\over1+z}-1\right\},\qquad
 D=s\left\{ra{K\over K+z}-1\right\}.                   \tag{13}
\]

Therefore

\[
 {D+(r-1)B\over s}
 =ra{K\over K+z}+rb{z\over1+z}-r.                       \tag{14}
\]

This is the promised exact dual-coordinate reduction.

## 6. The concave quadratic and Hellinger form

Put `c=rb` and `d=ra`.  Clearing the positive denominator in (14) gives

\[
 \boxed{
 N(z)=(c-r)z^2+\{K(c+d-r)-r\}z+K(d-r).}                 \tag{15}
\]

Since `0<=b<=1`, the leading coefficient is nonpositive.  Thus (14) is
nonpositive for every `z>=0` if and only if

\[
 a\le1,qquad
 \{K(a+b-1)-1\}_+^2\le4K(1-a)(1-b).                    \tag{16}
\]

Substituting (11) and using

\[
 a+b-1=ab-(1-a)(1-b)
\]
turns (16) into the sharp singleton-mass inequality

\[
 \boxed{
 q_Bq_D\ \ge\ r(r-1)^2
 \left[\sqrt{ab}-\sqrt{(1-a)(1-b)}\right]_+^2.}         \tag{17}
\]

The square-root expression is understood only after the separate condition
`a<=1`; `b<=1` is automatic.  Equations (15)--(17) are mutually equivalent.

This yields the first missing bounded-module theorem.

> **Bounded dual-moment lemma at `R_hyb` (BDM, open).**  At
> `r=R_hyb`, every finite `H` and every positive portal vector satisfy
> `rho_dB(H,r)<=r-1` and (17).  Equality in the nontrivial branch occurs only
> for a strong `K_2`, up to internal scale and arbitrary positive portal
> loads.

BDM implies the stronger affine inequality
`D+(r-1)B<=0` for every separated bounded module and every scale.  In
particular it implies the required nonlinear alternative
`D<=0` or `D+(r-1)B<=0`.  It does not assert an affine separator for
non-dilute graphs; the stored weak-cut `K_2--K_20` witness lies outside this
one-module conclusion.

## 7. Exact `K_2` equality and the hybrid sextic

For `H=K_2`, symmetry makes the portal laws irrelevant and

\[
 b={r\over r+1},\quad a={1\over2(r-1)},\quad
 q_B={1\over r+1},\quad q_D={1\over2},                    \tag{18}
\]

\[
 c={r^2\over r+1},\quad d={r\over2(r-1)},\quad
 K=2r(r-1)^2(r+1).                                      \tag{19}
\]

Writing

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1,                 \tag{20}
\]

the discriminant of (15) factors exactly as

\[
 \boxed{\operatorname{disc}_zN=r^2P(r).}                \tag{21}
\]

At the unique root `R_hyb` in `(3/2,151/100)`, (15) is a negative square
with double root

\[
 z_*=-{(r+1)(r^3-4r^2+3r+1)\over2}
     =(r^2-1){-r^3+4r^2-3r-1\over2(r-1)}.               \tag{22}
\]

This is exactly `z_*=(r^2-1)sigma_*` from the pair--leaf construction.
Thus BDM is not an invented strengthening: its equality condition is the
algebraic tangency that defines the proved lower endpoint.

### 7.1 BDM is proved for every complete module

The equality calculation extends to an exact all-order radial theorem.  For
`H=K_s`, arbitrary positive portal loads give the same two singleton
averages by symmetry, and

\[
 \begin{aligned}
 b_s&={(r-1)r^{s-1}\over r^s-1},&
 a_s&={(s-1)r^{s-2}\over s(r^{s-1}-1)},\\
 q_{B,s}&={r-1\over r^s-1},&
 q_{D,s}&={(s-1)(r-1)\over s(r^{s-1}-1)}.              \tag{22a}
 \end{aligned}
\]

At `r=R_hyb`, (16) holds for every `s>=2`, strictly for `s>=3`.
Consequently

\[
 D+(R_{hyb}-1)B\le0                                    \tag{22b}
\]

for every complete separated module and every positive scale, with equality
only for `K_2` at the gate scale (22).

Here is a proof without an order scan.  First, `a_s<1` for all `s>=2` and
`r>3/2`, because the numerator of `1-a_s` is

\[
 r^{s-2}\{sr-(s-1)\}-s,                                \tag{22c}
\]

which is increasing in `r`, vanishes at `(s,r)=(2,3/2)`, and is positive
for `s>=3` already at `r=3/2`.

For `s>=7`, direct subtraction gives

\[
 1-a_s-b_s={r^{2s-2}-2sr^{s-1}+(s-1)r^{s-2}+s\over
              s(r^{s-1}-1)(r^s-1)}.                    \tag{22d}
\]

The numerator is

\[
 r^{s-2}\{r^s-2sr+s-1\}+s.
\]

The bracket is increasing for `r>=3/2`.  At `r=3/2` it is
`(3/2)^s-2s-1`, positive at `s=7`; moreover

\[
 \left\{(3/2)^{s+1}-2(s+1)-1\right\}
 -{3\over2}\left\{(3/2)^s-2s-1\right\}=s-{3\over2}>0.
\]

Thus `a_s+b_s<1`, so the middle coefficient in (15) is negative and the
claim follows immediately.

Only `s=3,4,5,6` remain.  Exact Sturm reduction over the isolating interval
of `R_hyb` gives

\[
 \operatorname{disc}_zN<0\quad(s=3,4,5),\qquad
 K(a_6+b_6-1)-1<0.                                    \tag{22e}
\]

The replay constructs these rational polynomials and proves each sign by a
zero root count plus one rational endpoint evaluation.  This is a finite
boundary discharge forced by (22d), not a gadget catalogue.  Together with
(21), it proves the complete-module theorem and its equality class.

## 8. Portal coupling and the exact pointwise target

The two portal averages in (10) are coupled by the same `x`, but one is
degree-reweighted.  Let

\[
 u_i=q_{Bd,i},\qquad v_i=q_{dB,i},\qquad e_i=1/d_i,
\]

and denote the right side of (17) by `Q`.  Requiring (17) for every positive
portal vector is exactly

\[
 (x\cdot u)(x\cdot(ev))
       \ge Q(x\cdot\mathbf1)(x\cdot e)\qquad(x\ge0).     \tag{23}
\]

Equivalently, the symmetric matrix

\[
 M_{ij}={u_i e_jv_j+u_j e_iv_i-Q(e_i+e_j)\over2}         \tag{24}
\]

must be copositive.  Portal concentration at vertex `i` gives the necessary
pointwise inequalities

\[
                         u_iv_i\ge Q.                    \tag{25}
\]

But (25) alone is not sufficient: mixed portals test the off-diagonal terms
in (24), and degree reweighting can emphasize a different vertex in the dB
factor.  The actual local theorem is copositivity (24), not an uncoupled
minimum of the diagonal products.

## 9. What first-level stationarity supplies

Let `P_ij=w_ij/d_i`, `t_i=sum_j P_ji`, and let
`p^U_ij=mu_U(A={i,j})`.  Put

\[
                         g_r(x)={x\over r-(r-1)x}.        \tag{26}
\]

Stationarity of each singleton state gives the exact coordinate balances

\[
 \boxed{r t_iq_{Bd,i}=\sum_jP_{ij}(q_{Bd,j}+p^{Bd}_{ij}),} \tag{27}
\]

\[
 \boxed{q_{dB,i}=\sum_jg_r(P_{ji})(q_{dB,j}+p^{dB}_{ij}).} \tag{28}
\]

After summation these become the rank-one boundary-flow identities

\[
 (r-1)\sum_it_iq_{Bd,i}
   =\sum_{i<j}(P_{ij}+P_{ji})p^{Bd}_{ij},                \tag{29}
\]

\[
 \sum_iq_{dB,i}\left(1-\sum_jg_r(P_{ij})\right)
   =\sum_{i<j}\{g_r(P_{ij})+g_r(P_{ji})\}p^{dB}_{ij}.    \tag{30}
\]

These balances are necessary but not by themselves sufficient for BDM:
they do not constrain probability stored on ranks three and above.  The
first missing proof step is therefore a cross-rule stationary inequality,
not another marginal profile guess.

This insufficiency is exact, not merely a warning.  Equations (27)--(28) are
homogeneous in the exact rank-one and rank-two state masses.  Starting from
any two probability laws satisfying them, multiply all masses on ranks one
and two by `lambda in (0,1)` and put the remaining probability on any
rank-three state.  The rescaled laws still satisfy every singleton-state
balance.

Take order `s=8` and let `lambda->0`.  Both limiting mean ranks are three, so

\[
 b\longrightarrow{3\over8},\qquad
 a\longrightarrow{3\over8(r-1)}.                        \tag{31}
\]

Throughout the exact isolating interval
`3/2<r<151/100`, one has `0<a<1` and

\[
 a+b-1>{25\over34}+{3\over8}-1={15\over136}>0.          \tag{32}
\]

The right side of (17) therefore tends to a strictly positive number, while
`q_Bq_D=O(lambda^2)`.  Thus the first-level stationary LP itself violates
BDM for all sufficiently small `lambda`.  These rescaled laws need not be
stationary for the higher-rank equations, so this is not a graph
counterexample.  It proves that no argument using only (27)--(30),
positivity, and normalization can establish BDM.  At least one genuine
higher-rank flow identity is logically necessary.

The separate condition `a<=1` is the dB density assertion

\[
                         \rho_{dB}(H,R_{hyb})\le R_{hyb}-1. \tag{33}
\]

It is not presently proved.  The stronger complementary-level conjecture
for the dB dual would imply `E|A|<=s/2`, hence (33), because
`R_hyb-1>1/2`.  Singleton-state balance alone cannot imply it: the same
rank-three rescaling on four or more vertices can make the mean rank exceed
`s(R_hyb-1)` while leaving (28) intact.

There is an exact finite product-chain formulation.  Set
`C=r(r-1)^2`, let `A,A'` be independent `mu_Bd` sets and `D` an independent
`mu_dB` set, and define

\[
 U(A)=\sum_i\gamma_i\mathbf1_{A=\{i\}},\qquad
 V(D)=\sum_i\alpha_i\mathbf1_{D=\{i\}}.                 \tag{34}
\]

After clearing the denominators in (17), the BDM gap is the stationary mean
of

\[
 \begin{split}
 F_z(A,A',D)={}&C\left[(1+z)
       \left(1-{|D|\over s(r-1)}\right)
       -z{|A'|\over s}\right]\\
 &+zU(A)V(D)\left[1+z\left(1-{|A'|\over s}\right)\right].
                                                               \tag{35}
 \end{split}
\]

Thus a proof may seek a potential `Phi_z` on the three-copy product chain
such that

\[
 F_z+(L_{Bd}^{A}+L_{Bd}^{A'}+L_{dB}^{D})\Phi_z\ge0       \tag{36}
\]

pointwise.  Equation (36) is a finite LP dual certificate for fixed `H,z`;
its stationary mean is exactly BDM.  A universal construction of this
certificate, with equality rigidity at `K_2`, is the smallest currently
visible proof obligation.

## 10. Remaining compactness stack

The matching-upper program now has a definite order.

1. **Bounded local step:** prove BDM, equivalently (17), (24), or the
   product-chain inequality (36).  The exact scaling obstruction above
   proves that singleton-state balances are too weak; the certificate must
   use higher-rank flow.
2. **Equality step:** control the next response scale near the `K_2` equality
   ray; a first-order cone cannot decide a zero tangent.
3. **Dilute global step:** prove response-scale trace tightness for growing
   module arrays, retaining exceptional hubs in the Schur trace.
4. **Bulk step:** prove that a regular non-dilute limit has a finite-order
   obstruction, or exhibit the missing positive-density mechanism.

The first item is a finite exact stationary inequality and is strictly
smaller than the original arbitrary-sequence problem.  Failure of BDM would
immediately identify a bounded module that improves the lower construction;
success would make `K_2` the exact local equality generator at `R_hyb`.

## 11. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_dual_moment_reduction.py
```

The replay checks the normal-form reduction, the equivalence of the
quadratic/discriminant/Hellinger forms, the portal copositivity identity, and
the exact `K_2` factorization (21)--(22).
