# Regular adjoint kernels have no quadratic Bd-catalyst ray

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note closes a broad correlated dense normal form.  It is not a screen of
one fixed graph.

Consider an arbitrary finite latent-type kernel and its adjoint, which are
the exact rare-mutant limits of Bd and dB on a diffuse undirected weighted
clone blow-up.  Perturb an arbitrary regular reversible base kernel; the
base need not be complete, its rank is unrestricted, and a sequence of bases
may have rank tending to infinity or spectral gap tending to zero.

At fitness `r=2`, let `G(epsilon)` be the uniform-singleton Bd survival gain
over `1/2`, and let `L(epsilon)` be the dB survival loss below `1/2`.  If the
first nonzero response is the ordinary quadratic tangent, then

\[
 \boxed{L_2\ge2G_2.}                                 \tag{1}
\]

Equality is possible only in the period-two eigenmode of the base kernel.
Thus no regular quadratic perturbation, even of growing rank, can have
positive Bd response and little-oh dB cost.

This theorem does not close singular higher-order tangencies, non-diffuse
collisions, sparse order-one shared edges, or perturbations that are not
trace-resolved before their response scale.  Those are precisely the
remaining constructive exits.

## 1. Exact adjoint branching normal form

Let `p=(p_i)` be a positive probability vector and let `P` be an irreducible
row-stochastic kernel.  Write

\[
 \langle f,g\rangle_p=\sum_i p_i f_i g_i,
 \qquad P^*=D_p^{-1}P^T D_p,
 \qquad t=P^*\mathbf1.                               \tag{2}
\]

The normalization `E_p t=1` is automatic.

For a symmetric dense clone profile with type proportions `p_i`, edge
weights `W_ij=W_ji`, and

\[
 \delta_i=\sum_jp_jW_{ij},\qquad
 P_{ij}={p_jW_{ij}\over\delta_i},                   \tag{3}
\]

the rare Bd particle of type `i` dies at rate `t_i`, gives birth at rate two,
and samples its child from row `P_i`.  The rare dB particle dies at rate one
and gives type-`j` children at rate `2P^*_{ij}`.  These rates follow directly
from the finite Moran rules exactly as in the rank-one clone derivation.

Let `b_i,s_i` be their nonzero survival probabilities.  First-event
conditioning gives the exact nonlinear adjoint pair

\[
 t_i b_i=2(1-b_i)(Pb)_i,                            \tag{4}
\]

\[
 s_i=2(1-s_i)(P^*s)_i.                              \tag{5}
\]

Uniform singleton initialization is exactly the `p` average

\[
 \beta=E_pb,
 \qquad \sigma=E_ps.                                \tag{6}
\]

The derivation below in fact needs only the adjoint pair (4)--(5), so it is
valid for a larger abstract class than reversible clone kernels.

## 2. Two exact nonlinear response identities

Put

\[
                        b={1\over2}\mathbf1+z.
\]

Average (4).  The adjoint relation gives
`E_p(Pz)=E_p(tz)`, and all linear temperature terms cancel.  What remains is
the exact identity

\[
 \boxed{\displaystyle
       \beta-{1\over2}=-2\langle z,Pz\rangle_p.}     \tag{7}
\]

This explains why Bd gain requires an anticorrelated type mode rather than
degree heterogeneity by itself.

Similarly put

\[
                        s={1\over2}\mathbf1+v.
\]

Divide (5) by `1-s_i`, average, and use
`E_p(P^*s)=E_ps`.  The elementary expansion

\[
 {1/2+v\over1/2-v}
 =1+4v+{8v^2\over1-2v}
\]

gives the second exact identity

\[
 \boxed{\displaystyle
 {1\over2}-\sigma
     =4E_p\left[{v^2\over1-2v}\right]\ge0.}         \tag{8}
\]

Thus the dB loss is a strictly convex dispersion functional.  Equations
(7)--(8) hold globally, not only near a regular kernel.

## 3. Expansion about an arbitrary regular reversible base

Let `P_epsilon` be a differentiable row-stochastic path with

\[
 P_0=Q,qquad Q^*=Q,qquad Q\mathbf1=\mathbf1.       \tag{9}
\]

Thus `p` is stationary for the reversible base `Q`, or equivalently the
base clone profile has equal limiting weighted degrees.  Put

\[
 h=\left.{d\over d\epsilon}P_\epsilon^*\mathbf1
                         \right|_{\epsilon=0}.       \tag{10}
\]

Since `E_p t_epsilon=1`, `E_p h=0`.  The Jacobians of (4)--(5) at
`b=s=1/2` are `2I-Q` and its adjoint.  Their spectra lie in `[1,3]`, so the
positive survival solutions are differentiable without any spectral-gap
assumption.  Define

\[
 u=-{1\over2}(2I-Q)^{-1}h.                          \tag{11}
\]

Direct differentiation gives

\[
 b_\epsilon={1\over2}\mathbf1+\epsilon u+O(\epsilon^2),
 \qquad
 s_\epsilon={1\over2}\mathbf1-\epsilon u+O(\epsilon^2). \tag{12}
\]

In particular, both uniform averages have zero first derivative.  Insert
(12) into the exact identities (7)--(8):

\[
 \beta_\epsilon-{1\over2}
   =-2\epsilon^2\langle u,Qu\rangle_p+O(\epsilon^3),\tag{13}
\]

\[
 {1\over2}-\sigma_\epsilon
   =4\epsilon^2\langle u,u\rangle_p+O(\epsilon^3).  \tag{14}
\]

The reversible Markov operator `Q` is a self-adjoint contraction, with
spectrum in `[-1,1]`.  Hence

\[
 4\langle u,u\rangle_p
 -2\{-2\langle u,Qu\rangle_p\}
 =4\langle u,(I+Q)u\rangle_p\ge0.                  \tag{15}
\]

If the Bd coefficient in (13) is positive, (15) is exactly (1).  Equality
holds precisely when the responding component of `u` lies in the
`-1` eigenspace of `Q`; for an irreducible base this is the bipartite
period-two mode.

## 4. Growing-rank consequence and full-response scope

The proof uses no lower spectral-gap bound: the inverse in (11) has operator
norm at most one because the spectrum of `2I-Q` lies in `[1,3]`.  Therefore
the same coefficient inequality holds stage by stage for arbitrary
reversible bases `Q_k`, including ranks tending to infinity and nearly
decomposable kernels.

More precisely, suppose a growing-rank perturbation diagonal has expansions
(13)--(14) with remainders `o(c_k)`, where

\[
 c_k=\epsilon_k^2\langle u_k,u_k\rangle_{p_k}>0.    \tag{16}
\]

Then its normalized branching response satisfies

\[
 \liminf_k {1/2-\sigma_k\over c_k}
 \ge2\limsup_k{(\beta_k-1/2)_+\over c_k}.           \tag{17}
\]

For diffuse clone realizations, choose the clone multiplier after the
profile and a growing mutant cutoff so the stopped-chain error is `o(c_k)`.
Fixation is contained in the event of reaching the cutoff.  Hence actual Bd
gain is no larger than the branching gain, while actual dB loss is no
smaller than the branching loss.  If additionally `1/n_k=o(c_k)`, the exact
complete-graph dB finite-size correction is negligible and (17) passes to
the full uniform-singleton fixation response.  No post-establishment path
is discarded in this one-sided passage.

Thus a quadratic correlated perturbation cannot realize the catalyst target

\[
 B_k/c_k\to b>0,
 \qquad D_k/c_k\to0.                                \tag{18}
\]

The hypothesis on the remainder in (16) is substantive.  A diagonal whose
quadratic coefficient vanishes and whose first response occurs at a
singular higher order is not excluded here.  Nor is a module whose sparse
collisions survive before every trace cutoff.  The next positive search
must exploit one of those mechanisms rather than another regular dense
degree perturbation.

## 5. Exact replay

`verify_regular_adjoint_catalyst_tangent.py` checks the two global identities
symbolically, differentiates a nontrivial rational two-type path, and
certifies the sharp period-two equality case `L_2=2G_2` exactly.
