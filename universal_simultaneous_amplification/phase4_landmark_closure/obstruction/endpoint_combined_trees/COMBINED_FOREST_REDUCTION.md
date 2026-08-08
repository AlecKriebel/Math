# Combined endpoint trees and the reverse/complement obstruction

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## Status

This bounded cycle does **not** prove the universal endpoint inequality and
does **not** find an endpoint counterexample.

It does prove three exact statements.

1. The actual normalized Bd--dB product gap is one paired positive-tree
   partition sign.  One factor is a continuous-time Bd-dual rooted tree and
   the other is a dB post-event directed arborescence.  No separate
   orientation or batching inequality is assumed.
2. The same gap has an exact three-term bridge through the reversed-arrow
   process `C`.  This identifies where the orientation defect cancels a
   wrong-signed Palm persistence or neutral-timing term.
3. The natural forward absorbing-forest path surgery is not pointwise.  The
   state-edge factor created by reversing and complementing a root path and
   the factor on the complementary edge are exact reciprocals.  Both desired
   one-sided edge bounds fail already on the weighted path `P3` with edge
   ratio `1:17`, and fail again on both frozen batching witnesses and the
   seven-vertex windmill.

Thus the universal endpoint problem is reduced to one classical paired
forest inequality, but its sign remains **OPEN**.  The exact reciprocal
edge identity is the minimal new obstruction to a local forest involution.

## 1. Endpoint notation

Fix

\[
 r={3\over2},\qquad a=r-1={1\over2}.
\]

Let `L` be the continuous Bd branching--coalescing dual, `C` the same
unbatched dual with every base arrow reversed, and `D` the locked-target
geometric-burst dB dual.  Write

\[
 m_L=E_{\pi_L}|A|,\qquad
 m_C=E_{\pi_C}|A|,\qquad
 m_D=E_{\pi_D}|A|.
\]

For the complete graph, put

\[
 b=m_B^K={na(1+a)^{n-1}\over(1+a)^n-1},
 \qquad
 d=m_D^K={(n-1)a(1+a)^{n-2}\over(1+a)^{n-1}-1}.
\]

The already proved duality formulas give

\[
 \rho_{Bd}(G,3/2)={m_L\over n},\qquad
 \rho_{dB}(G,3/2)={m_D\over n}.
\]

Consequently the endpoint fixation-product conjecture is exactly

\[
 m_Lm_D\le bd.                                             \tag{1}
\]

It is convenient to use its reciprocal normalization

\[
 \mathcal H(G)
 ={1\over m_D}-{m_L\over bd}
 ={bd-m_Lm_D\over bd\,m_D}.                               \tag{2}
\]

The sign of `H` is precisely the sign in (1).

## 2. Exact merger through the `C` event law

Let `alpha_C` be the pre-neutral event Palm law of `C`, let `beta_C` be
its post-neutral law, and let `alpha_D` be the post-burst event law of `D`.
For

\[
 f(A)={1\over |A|},
\]

event-size bias gives

\[
 \alpha_Cf={1\over m_C},\qquad
 \alpha_Df={1\over m_D}.                                  \tag{3}
\]

Define, without assigning any sign,

\[
 \begin{aligned}
 \mathcal P&=\alpha_Df-\beta_Cf,\\
 \mathcal T&=\beta_Cf-{b\over d}\alpha_Cf,\\
 \mathcal O&={b^2-m_Lm_C\over bd\,m_C}.
 \end{aligned}                                             \tag{4}
\]

Here `P` is the exact locked-versus-refreshed persistence term, `T` is the
pre-/post-neutral timing correction, and `O` is the multiplicative
orientation defect.  A direct cancellation, using only (3), gives

\[
 \boxed{\mathcal H=\mathcal P+\mathcal T+\mathcal O.}       \tag{5}
\]

This is the promised combined endpoint identity.  It neither requires nor
implies a separate sign for an orientation or batching factor.

If

\[
 \mathcal O_{\rm mid}=2b-m_L-m_C,
\]

then the orientation contribution itself has the exact split

\[
 \mathcal O
 ={\mathcal O_{\rm mid}\over d\,m_C}
 -{(b-m_L)(b-m_C)\over bd\,m_C}.                             \tag{6}
\]

Thus the familiar `L/C` midpoint defect is not the full orientation term:
the cross correction in (6) is essential and can have either sign.

## 3. One paired forest determinant

Let `Q_L` be the continuous generator of `L` on all nonempty subsets and
define its rooted-tree cofactors

\[
 \tau_L(A)=\det(-Q_L)^{\widehat A,\widehat A},\qquad
 Z_L=\sum_A\tau_L(A),\qquad
 Y_L=\sum_A |A|\tau_L(A).                                  \tag{7}
\]

Let `K_D` be the locked-target post-event kernel on the recurrent nonempty,
nonfull subsets.  Its directed in-arborescence cofactors are

\[
 \theta_D(B)=\det(I-K_D)^{\widehat B,\widehat B},\qquad
 \Theta_D=\sum_B\theta_D(B),\qquad
 \Phi_D=\sum_B{\theta_D(B)\over |B|}.                       \tag{8}
\]

The Markov tree theorem gives

\[
 m_L={Y_L\over Z_L},\qquad
 {1\over m_D}={\Phi_D\over\Theta_D}.                        \tag{9}
\]

Substitution into (2) yields the single paired-tree identity

\[
 \boxed{
 \begin{aligned}
 \mathfrak H(G)
 &:=bd\,Z_L\Phi_D-Y_L\Theta_D\\
 &=\sum_{A,B}\tau_L(A)\theta_D(B)
       \left({bd\over |B|}-|A|\right),\\
 {\mathfrak H(G)\over bd\,Z_L\Theta_D}&=\mathcal H(G).
 \end{aligned}}                                             \tag{10}
\]

Therefore

\[
 \boxed{m_Lm_D\le bd\quad\Longleftrightarrow\quad
        \mathfrak H(G)\ge0.}                                \tag{11}
\]

This is the minimal classical inequality left by this cycle: under an
independent Bd-dual tree root `A` and dB event-arborescence root `B`, the
mean transport cost `bd/|B|-|A|` must be nonnegative.  The integrand has
both signs already for the complete graph, so (11) is intrinsically a
global root-transport statement.

For comparison, if `tau_D` denotes the continuous `D` rooted-tree weights,
with partition sums `Z_D,Y_D`, the equivalent unmarked form is

\[
 bdZ_LZ_D-Y_LY_D
 =\sum_{A,B}\tau_L(A)\tau_D(B)(bd-|A||B|).                  \tag{12}
\]

The verifier reconstructs the `beta_C` refreshed-event law and `alpha_D`
locked-event law from independent arborescence cofactors, then checks that
(5), (10), and (12) are identical rational numbers after their displayed
positive normalizations.

## 4. The actual forward absorbing forests

There is also a direct forward-chain version of the same single sign.  Let
`Q_U^T` be any row-scaled transient forward generator for
`U in {Bd,dB}` and put

\[
 Z_U=\det(-Q_U^T),\qquad N_U=Z_U\rho_U.
\]

The directed matrix-forest theorem says that `Z_U` is the total weight of
outgoing forests rooted at extinction and fixation.  The numerator `N_U`
is the same forest sum, with each forest weighted by the fraction of
singleton roots whose path ends at fixation.  Hence the actual endpoint
product is equivalent to the one paired absorbing-forest sign

\[
 \boxed{
 \mathfrak A(G)
 =N_{Bd}^KN_{dB}^K Z_{Bd}Z_{dB}
  -N_{Bd}N_{dB}Z_{Bd}^KZ_{dB}^K\ge0.}                       \tag{13}
\]

Indeed,

\[
 \mathfrak A(G)
 =Z_{Bd}Z_{dB}Z_{Bd}^KZ_{dB}^K
   \{\rho_{Bd}^K\rho_{dB}^K-\rho_{Bd}\rho_{dB}\}.         \tag{14}
\]

For the weighted `P3`, the verifier enumerates every two-root outgoing
forest directly and reproduces both determinants and both fixation
numerators exactly.

## 5. Exact failure of local reverse/complement surgery

Write `P_ij=w_ij/d_i`, and for `v` outside `S` put

\[
 x=x_v(S)=\sum_{u\in S}P_{vu},\qquad
 y=y_v(S)=\sum_{u\in S}P_{uv},\qquad
 t=t_v=\sum_uP_{uv}.                                        \tag{15}
\]

For the same adjacent state edge `S <-> S+v`, the exact forward
increase/decrease biases are

\[
 B_{Bd}(S,v)=r{y\over t-y},\qquad
 B_{dB}(S,v)=r{x\over1-x}.                                  \tag{16}
\]

The dB replacement denominator cancels within the edge bias.  Let

\[
 S^\star=V\setminus(S\cup\{v\}).
\]

Then `x_v(S^star)=1-x`, `y_v(S^star)=t-y`, and therefore

\[
 B_{Bd}(S,v)B_{Bd}(S^\star,v)=r^2,
 \qquad
 B_{dB}(S,v)B_{dB}(S^\star,v)=r^2.                          \tag{17}
\]

In particular the cross-orientation factor produced by reversing and
complementing a path edge is

\[
 \Xi(S,v)={B_{Bd}(S,v)\over B_{dB}(S,v)}
 ={y(1-x)\over x(t-y)},
 \qquad
 \boxed{\Xi(S^\star,v)=\Xi(S,v)^{-1}.}                      \tag{18}
\]

There is an equally sharp statement after complete-graph normalization.
For `k=|S|`, let

\[
 \overline B_k={rk\over n-1-k},\qquad
 \Pi(S,v)={B_{Bd}(S,v)B_{dB}(S,v)\over\overline B_k^2}.
\]

Then

\[
 \boxed{\Pi(S^\star,v)=\Pi(S,v)^{-1}.}                     \tag{19}
\]

Thus neither `Xi<=1` nor `Xi>=1`, and neither `Pi<=1` nor `Pi>=1`, can
hold statewise unless every admissible edge is already balanced.  On the
path with weights `w_02=1,w_12=17`, take `S={0}` and `v=2`.  Exactly,

\[
 x={1\over18},\quad y=1,\quad t=2,\quad
 \Xi=17,\quad\Pi={1\over17}.                                \tag{20}
\]

The complementary state is `S^star={1}` and has

\[
 \Xi={1\over17},\qquad\Pi=17.                               \tag{21}
\]

This exactly refutes a termwise weight-nonincreasing forest involution based
only on reverse/complement root paths.  Complement pairing supplies
reciprocal factors; applying AM--GM to a pair gives a lower bound, not the
upper domination required by (13).  Moreover, the dB denominator discarded
by (16) remains on all unchanged side branches.  A successful forest proof
must therefore transport mass among multiple root paths and side branches,
or work directly with the global partition sign (10) or (13).

## 6. Mandatory exact hostile screen

Every line below is asserted over `QQ`.  Decimal magnitudes are printed only
for readability; they are not used to decide a sign.

| Graph | `bd-m_L m_D` | `P,T,O` signs | `Xi, Xi*` | `Pi, Pi*` |
|---|---:|---|---|---|
| `K4` | exactly `0` | `0,0,0` | `1,1` on every edge | `1,1` |
| weighted `P3`, `1:17` | `7807954339/14795921490 > 0` | `+,+,+` | `17,1/17` | `1/17,17` |
| persistence witness `W_P` | exact `>0` | `-,+,+` | `1360/109,109/1360` | `85/1744,1744/85` |
| timing witness `W_T` | exact `>0` | `+,-,+` | `21/20,20/21` | `945/1024,1024/945` |
| seven-vertex dB windmill | exact `>0` | `+,-,+` | `1801/222,222/1801` | `1801/28771200,28771200/1801` |

The negative `P` on `W_P` is canceled by timing plus orientation.  The
negative `T` on `W_T` and on the windmill is canceled by persistence plus
orientation.  The cross correction in (6) is negative on the weighted path
and `W_P`, positive on `W_T` and the windmill, and zero on `K4`.  Hence none
of these pieces is being silently promoted to a universal sign.

The exact rational fingerprints and all full numerators and denominators
are regenerated by the two verifier scripts in this directory.

## 7. What remains open

The only universal sign asserted here is equivalence:

\[
 \mathfrak H(G)\ge0
 \quad\Longleftrightarrow\quad
 \mathfrak A(G)\ge0
 \quad\Longleftrightarrow\quad
 \rho_{Bd}(G,3/2)\rho_{dB}(G,3/2)
 \le \rho_{Bd}(K_n,3/2)\rho_{dB}(K_n,3/2).
\]

Whether this sign holds for every connected undirected weighted graph is
**OPEN**.  The present cycle closes the naive local forest-surgery route,
not the global paired-tree inequality.
