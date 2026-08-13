# The normalized cross-rule tree reduction at fitness two

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Status

This note derives the exact shared-arrow and directed-tree form of the
normalized cross-rule endpoint target

\[
 \boxed{\frac{m_L}{b_n}+\frac{m_D}{d_n}\le 2}.                 \tag{1}
\]

Here `L` is the birth--death branching--coalescing dual at fitness two and
`D` is the fair-geometric death--birth dual.  Their stationary mean ranks
are `m_L,m_D`.  The complete-graph means are

\[
 b_n=\frac{n2^{n-1}}{2^n-1},\qquad
 d_n=\frac{(n-1)2^{n-2}}{2^{n-1}-1}.                         \tag{2}
\]

The derived tree sign is an exact equivalent, not a sufficient
strengthening.  It combines the two update rules before assigning a sign.
The sign remains **OPEN**.

The exact reductions proved below are:

1. `(1)` is one paired positive-arborescence root-cost inequality;
2. equivalently, it is one root-cost inequality for the independent product
   generator `L tensor I + I tensor D`;
3. because the fitness-two adjoint reference is uniform, every `L` in-tree
   is exactly a weight-preserving `C` out-tree, where `C` is the
   reversed-arrow unbatched dual; and
4. every `D` edge is a positive sum of target-locked `C` arrow histories.

Thus the literal remaining object is a paired **out-`C` tree / locked-history
in-tree** inequality.  Earlier dB-only tree-reflection results prove that
local complement rerooting and fixed-length history injection cannot prove
even the `D` marginal bound.  The coupling between the two tree factors is
therefore essential to this representation.

## 2. Exact dual means and complete normalizers

Let

\[
 \Omega_L=2^V\setminus\{\varnothing\},\qquad
 \Omega_D=\{A:\varnothing\ne A\subsetneq V\}.                 \tag{3}
\]

The full state `V` is transient for `D` and is deleted.  It may be retained
for `L`; the `L` dual is irreducible on `Omega_L` for a connected graph.
Let `Q_L,Q_D` denote the row generators on these spaces.  Write

\[
 \tau_L(A)=\det(-Q_L)^{\widehat A,\widehat A},\qquad
 \tau_D(B)=\det(-Q_D)^{\widehat B,\widehat B},                 \tag{4}
\]

and

\[
 \begin{array}{lll}
 Z_L=\sum_A\tau_L(A),&Y_L=\sum_A|A|\tau_L(A),&m_L=Y_L/Z_L,\\
 Z_D=\sum_B\tau_D(B),&Y_D=\sum_B|B|\tau_D(B),&m_D=Y_D/Z_D.
 \end{array}                                                   \tag{5}
\]

The equalities for the means are the directed Markov-chain tree theorem.
The complete `L` law is uniform on the nonempty subsets, so

\[
 b_n=\frac{\sum_{k=1}^n k\binom nk}{2^n-1}
     =\frac{n2^{n-1}}{2^n-1}.                                 \tag{6}
\]

The complete fair-geometric law on proper sets is proportional to `n-|A|`,
and hence

\[
 d_n=\frac{\sum_{k=1}^{n-1}k(n-k)\binom nk}
                 {\sum_{k=1}^{n-1}(n-k)\binom nk}
     =\frac{(n-1)2^{n-2}}{2^{n-1}-1}.                         \tag{7}
\]

Uniform-singleton fixation equals stationary dual mean divided by `n`.
Therefore `(1)` is exactly the normalized fixation inequality

\[
 \frac{\rho_{\rm Bd}(G,2)}{\rho_{\rm Bd}(K_n,2)}
 +\frac{\rho_{\rm dB}(G,2)}{\rho_{\rm dB}(K_n,2)}\le2.       \tag{8}
\]

In particular, simultaneous strict amplification at fitness two is
impossible if `(1)` holds.

## 3. One paired positive-tree sign

Define

\[
 \mathfrak S_n(G)
 =2b_nd_nZ_LZ_D-d_nY_LZ_D-b_nZ_LY_D.                          \tag{9}
\]

Substituting `(5)` gives the exact identity

\[
 \boxed{
 2-\frac{m_L}{b_n}-\frac{m_D}{d_n}
 =\frac{\mathfrak S_n(G)}{b_nd_nZ_LZ_D}.}                     \tag{10}
\]

Expanding the four positive partition sums gives

\[
 \boxed{
 \mathfrak S_n(G)
 =\sum_{A\in\Omega_L}\sum_{B\in\Omega_D}
   \tau_L(A)\tau_D(B)
   \{2b_nd_n-d_n|A|-b_n|B|\}.}                               \tag{11}
\]

Consequently `(1)` is equivalent to `mathfrak S_n(G)>=0`.  The cost in
braces takes both signs even on the complete graph, so this is intrinsically
a global root-transport sign.

There is an equivalent one-chain formulation.  Let

\[
 Q_\times=Q_L\otimes I+I\otimes Q_D                           \tag{12}
\]

on `Omega_L times Omega_D`, and let `tau_x(A,B)` be its in-tree cofactor.
Its stationary law is `pi_L tensor pi_D`.  Hence the tree theorem implies

\[
 \frac{\tau_\times(A,B)}{\sum_{X,Y}\tau_\times(X,Y)}
 =\frac{\tau_L(A)\tau_D(B)}{Z_LZ_D}.                          \tag{13}
\]

Equivalently there is a root-independent `kappa>0` such that

\[
 \tau_\times(A,B)=\kappa\tau_L(A)\tau_D(B).                  \tag{14}
\]

Thus `(11)` is, up to the positive factor `kappa`, one ordinary directed
arborescence root-cost sum for the product chain.  No independence
assumption beyond the deliberately formed product generator is hidden here.

## 4. The exact shared-arrow representation

Let `P` be the reversible vertex request kernel and let `C` be the
unbatched set generator obtained by reversing every graphical arrow in `L`.
At fitness two the weighted-adjoint reference

\[
 \mu(A)=(r-1)^{|A|}
\]

is constant.  The proved adjoint identity therefore becomes

\[
 Q_L^T=Q_C+V,\qquad
 V(A)=2\{A_\partial(A)-B_\partial(A)\},                       \tag{15}
\]

where `V` is diagonal.  In particular, for distinct states,

\[
 \boxed{Q_L(B,A)=Q_C(A,B).}                                  \tag{16}
\]

Reversing every edge of an `L` in-arborescence rooted at `A` therefore
gives a `C` out-arborescence rooted at the same state with exactly the same
weight.  This is a bijection, so

\[
 \tau_L(A)=sum_{T\in\mathcal T_A^{\rm out}(C)}w_C(T).        \tag{17}
\]

The dB side uses exactly the same row-`P` arrows, but locks the target during
a fair-geometric batch.  If `S_v` is one selective row sample, `N_v` is one
neutral row replacement, and `G_v` is the fair-geometric burst kernel, then

\[
 \boxed{
 G_v=\sum_{j\ge0}2^{-(j+1)}S_v^jN_v,
 \qquad (I-S_v/2)(G_v-I)=\frac12 C_v,}                       \tag{18}
\]

where

\[
 C_v=(N_v-I)+(S_v-I).                                        \tag{19}
\]

The series in `(18)` is positive entrywise.  Thus each off-diagonal `D`
tree edge is a positive sum of labelled histories consisting of `C` row
arrows with one common retained target: zero or more selective arrows and a
final neutral arrow.  Multilinearly expanding all `D` tree edges in `(11)`
gives the promised literal form:

> `(1)` is equivalent to a single signed root-cost sum over a
> weight-preserving out-arborescence of the unbatched `C` arrow process and
> an independent in-arborescence whose edges are positive target-locked
> histories of those same row-`P` arrows.

This retains the two distinct structures that a proof must use: original
arrow reversal on the first factor and geometric target persistence on the
second.

## 5. Exact bridge through `C`

Let `m_C` be the stationary mean rank of `C`.  Pure algebra gives

\[
 \boxed{
 2-\frac{m_L}{b_n}-\frac{m_D}{d_n}
 =\left\{2-\frac{m_L+m_C}{b_n}\right\}
  +\left\{\frac{m_C}{b_n}-\frac{m_D}{d_n}\right\}.}           \tag{20}
\]

The first bracket is the centered orientation defect and the second is the
normalized batching defect.  Exact diagnostics at fitness two support both
individual signs, but neither sign is used in `(9)--(19)`.  At lower
fitnesses analogous split lemmas remained open and several stronger local
forms were false.  The theorem target of this note is therefore the combined
sign `(11)`, with `(20)` retained only as a bridge for compatible
adjoint/resolvent identities.

## 6. Minimal obstruction to local tree surgery

The existing fair-geometric tree-reflection theorem supplies an exact
warning.  On unweighted `K_3`, a dB in-tree of weight `4/59049` maps under
complement plus edge reversal to an out-tree of weight `1/59049`.  A fixed
undirected state-tree skeleton can have only a rank-two supported root, whose
conditional mean `2` is above the complete dB mean `4/3`.  Moreover the
labelled-history rank difference has both positive and negative
coefficients before evaluating the fair geometric parameter.

Hence the `D` factor in `(11)` cannot be signed treewise by complement
rerooting, skeletonwise, or by an injection preserving total burst length.
Those are exact route closures, not counterexamples to `(1)`.  In the
shared-arrow form they say that a proof must exchange mass between the
out-`C` factor and target-locked histories, or derive a global determinant
identity coupling the two partitions.

## 7. Exact audit

`verify_cross_rule_tree_reduction.py` independently constructs `L,C,D`
from their atomic rules over `QQ`, computes every tree cofactor, verifies
`(10)--(18)`, and checks the exact weighted three-path fingerprint

\[
 b_3=\frac{12}{7},\quad d_3=\frac43,\quad
 m_L=\frac{584}{341},\quad m_C=\frac{118}{75},\quad m_D=\frac65,
\]

\[
 2-\frac{m_L}{b_3}-\frac{m_D}{d_3}=\frac{1033}{10230}>0.      \tag{21}
\]

The audit is finite verification of the identities, not a proof of the open
all-graph sign.

## 8. Precise remaining identity

The proof-first branch now has one named target:

### Shared-Arrow Paired-Tree Inequality `SAPT_n`

For every loopless irreducible reversible request kernel `P`, the exact tree
partition in `(11)`, with the out-`C` / locked-history interpretation
`(17)--(18)`, satisfies

\[
 \boxed{\mathfrak S_n(G)\ge0.}                              \tag{SAPT_n}
\]

`SAPT_n` is exactly the normalized cross-rule endpoint inequality.  It would
rule out simultaneous amplification at fitness two.  No sign theorem beyond
this equivalence is claimed here.
