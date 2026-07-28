# Checkpoint 2 — Exact Foundations and First Rectification Theory

**Status:** rejected by adversarial review; preserved for provenance.

This checkpoint fixes one deliberately narrow foundational setting. Extensions
to set-valued maps, probability kernels, arbitrary divergences, and continuous
stratified spaces are deferred until the deterministic theory is stable.

## 1. Presented intervention complexes

### Definition 1.1 (finite directed intervention 2-complex)

A finite directed intervention 2-complex is data

\[
K=(K_0,K_1,K_2,s,t,\{(p_\sigma,q_\sigma)\}_{\sigma\in K_2}),
\]

where:

- \((K_0,K_1,s,t)\) is a finite directed graph;
- \(p_\sigma\) and \(q_\sigma\) are nonempty parallel directed paths with
  the same source and target.

The 2-cell \(\sigma\) is *external semantics*: it declares that
\(p_\sigma\) and \(q_\sigma\) represent the same net exogenous intervention
performed in two admissible orders. It does not assert that the system's
responses commute.

Let \(\operatorname{Path}(K)\) be the free category on the graph. Let
\(\sim_K\) be the least path congruence containing
\(p_\sigma\sim_Kq_\sigma\) for every 2-cell, and define the external
intervention category

\[
\mathcal C_K=\operatorname{Path}(K)/{\sim_K}.
\]

This is standard category-presentation / directed-concurrency machinery. It is
the source language of NCS, not a claimed invention.

## 2. Target category and failure semantics

### Definition 2.1 (partial nonexpansive map)

For extended metric spaces \(X,Y\), a partial nonexpansive map
\(T:X\rightharpoonup Y\) is a subset
\(\operatorname{Dom}(T)\subseteq X\) and a 1-Lipschitz map
\(T:\operatorname{Dom}(T)\to Y\). Composition uses the usual pullback domain

\[
\operatorname{Dom}(S\circ T)
=\{x\in\operatorname{Dom}(T):T(x)\in\operatorname{Dom}(S)\}.
\]

These objects and arrows form the category
\(\mathbf{pMetPar}_1\).

### Definition 2.2 (response assignment)

A deterministic response assignment on \(K\) is a functor

\[
R:\operatorname{Path}(K)\longrightarrow\mathbf{pMetPar}_1.
\]

Equivalently, it assigns:

- an extended metric feasible-state space \((X_b,d_b)\) to every vertex;
- a partial nonexpansive response \(R_e:X_{s(e)}\rightharpoonup X_{t(e)}\)
  to every elementary intervention edge.

The functor on the free category is obtained by composition. The response
assignment is *exact* or *order-independent relative to \(K\)* when it factors
through \(\mathcal C_K\).

Partiality represents infeasible or undefined adjustment. It must not be
silently removed by restricting every comparison to a favorable common
domain.

### Definition 2.3 (failure-completed route outcome)

For each fiber adjoin a failure symbol \(\bot_b\) and extend its metric by

\[
\widehat d_b(\bot_b,\bot_b)=0,\qquad
\widehat d_b(\bot_b,x)=\widehat d_b(x,\bot_b)=+\infty.
\]

For a path \(p:a\to b\), define the total outcome notation

\[
\widehat R_p(x)=
\begin{cases}
R_p(x),&x\in\operatorname{Dom}(R_p),\\
\bot_b,&x\notin\operatorname{Dom}(R_p).
\end{cases}
\]

This completion is used only to compare outcomes; it does not claim that the
totalized map is nonexpansive across a domain boundary.

## 3. Defects, memory, and exact descent

### Definition 3.1 (cell and path defects)

For a 2-cell \(\sigma\) with common source \(a\) and target \(b\), define

\[
\delta_\sigma(x)
=\widehat d_b(\widehat R_{p_\sigma}(x),
               \widehat R_{q_\sigma}(x)),
\qquad
\|\delta_\sigma\|_\infty
=\sup_{x\in X_a}\delta_\sigma(x).
\]

Thus a route-domain mismatch has infinite defect. Two routes that are both
undefined agree as partial maps at that input; applications may separately
record common failure prevalence.

For any parallel paths \(p,q:a\to b\), define

\[
\Delta_{p,q}(x)
=\widehat d_b(\widehat R_p(x),\widehat R_q(x)).
\]

### Proposition 3.2 (zero defect is exact descent; baseline)

\(R\) factors through \(\mathcal C_K\) if and only if
\(\|\delta_\sigma\|_\infty=0\) for every \(\sigma\in K_2\).

**Proof.** Zero extended defect means equality of route domains and equality
of route values, hence equality of the corresponding partial maps. The
universal property of a category presented by generators and relations gives
the factorization. The converse is immediate. \(\square\)

This is a path-category fact, not a novelty claim.

### Definition 3.3 (continued or residual order memory)

An immediate order defect need not persist. For a common continuation
\(r:b\to c\), define

\[
M_{r;p,q}(x)
=\widehat d_c(\widehat R_{rp}(x),\widehat R_{rq}(x)).
\]

If \(R_r\) is \(\rho\)-Lipschitz on the two reachable outcomes, then

\[
M_{r;p,q}(x)\le \rho\,\Delta_{p,q}(x).
\]

Thus a contraction may erase order memory; “order effect” and “persistent
memory” are distinct terms in NCS.

## 4. Morphisms and gauge

### Definition 4.1 (response morphism)

A response morphism \((f,\eta):(K,R)\to(K',R')\) consists of:

1. a graph map \(f\) sending each relation
   \(p_\sigma\sim q_\sigma\) to a valid relation in \(K'\);
2. total nonexpansive maps
   \(\eta_b:X_b\to X'_{f(b)}\);
3. exact intertwining of partial maps,

\[
\eta_{t(e)}R_e=R'_{f(e)}\eta_{s(e)},
\]

including equality of the two composition domains.

A response isomorphism has an invertible presentation map and bijective
fiberwise isometries. A **gauge transformation** is a response isomorphism
whose base map is the identity.

### Lemma 4.2 (gauge invariance; baseline)

If \(R'_e=\phi_{t(e)}R_e\phi_{s(e)}^{-1}\) for fiberwise bijective
isometries \(\phi_b\), then

\[
\delta'_\sigma(\phi_a x)=\delta_\sigma(x).
\]

**Proof.** Intermediate conjugacies cancel along every path, leaving the same
isometry \(\phi_b\) on both target outcomes. Domains transform bijectively and
target distance is preserved. \(\square\)

A coordinate or unit change that is not isometric must push the metric/cost
forward as part of the model. Scalar defect is not invariant if an analyst
changes coordinates but silently reinstalls a Euclidean metric.

## 5. Cost-generated carry response and reset response

### Definition 5.1 (cost-generated edge response)

Suppose the fibers lie in an ambient decision space \(Z\). For an edge
\(e:a\to b\), a carry-cost rule \(c_e:X_a\times X_b\to[0,\infty]\) generates

\[
R_e(x)=\operatorname*{arg\,min}_{y\in X_b}c_e(x,y)
\]

when the minimizer exists and is unique. Nonexistence or unresolved
nonuniqueness makes the deterministic response undefined. In a Hilbert space,
\(c_e(x,y)=\|x-y\|^2\) and a nonempty closed convex target fiber give the
metric projection \(P_{X_b}\), which is total and nonexpansive.

### Definition 5.2 (reset response)

Given a distinguished state \(s_b\in X_b\) at every vertex, the reset rule is

\[
R^{\mathrm{reset}}_e(x)=s_{t(e)}.
\]

It discards the current state and recomputes from a fixed reference.

### Proposition 5.3 (reset/carry separation; baseline)

Every reset response has zero path defect between nonempty parallel paths.
The same feasible fibers can support a carry response with nonzero defect.

**Proof.** Every nonempty reset path ending at \(b\) is the constant map with
value \(s_b\). The carry counterexample is computed in Section 9. \(\square\)

## 6. Baseline filling bound

Suppose paths \(P_0=p,\ldots,P_N=q\) form an admissible square-swap derivation
at \(x\). At step \(i\), a common prefix \(a_i\) is followed by one side
\(u_i\) or \(v_i\) of a 2-cell and then a common suffix \(b_i\). Assume every
route in the derivation is defined at \(x\).

### Proposition 6.1 (derivation bound; baseline)

\[
d(R_p x,R_q x)
\le
\sum_{i=0}^{N-1}
\operatorname{Lip}(R_{b_i})
d(R_{u_i}R_{a_i}x,R_{v_i}R_{a_i}x).
\]

**Proof.** Apply the triangle inequality across
\(R_{P_0}x,\ldots,R_{P_N}x\), and propagate each local comparison through its
common suffix with the suffix Lipschitz constant. \(\square\)

The **response filling cost** is the infimum of this right-hand side over
admissible swap derivations. For nonexpansive responses and uniform local
defect \(\varepsilon\),

\[
d(R_p x,R_q x)
\le \varepsilon\,\operatorname{Area}_K(p,q),
\]

where \(\operatorname{Area}_K\) is the minimum number of relation cells in a
directed derivation. This is quantitative-rewriting / metric-enriched-category
territory and is included as a bridge result, not a headline theorem.

## 7. Rectification: the central new question

Cell defects measure failure to descend. **Rectification** asks a stronger
question:

> When is an approximately descending response assignment close to an exact
> assignment that factors through \(\mathcal C_K\)?

This is an Ulam-stability problem for response functors. Its answer must depend
on the intervention presentation and the target class.

### 7.1 Translation responses

Let every fiber be the same finite-dimensional real Hilbert space \(H\), and
let

\[
R_e(x)=x+a_e,\qquad a_e\in H.
\]

For every relation \(\sigma\), define the signed path-edge incidence

\[
D_{\sigma e}
=\#\{e\text{ in }p_\sigma\}
 -\#\{e\text{ in }q_\sigma\}.
\]

Writing \(a=(a_e)_{e\in K_1}\), the vector cell defect is

\[
c=(D\otimes I_H)a.
\]

Use the unweighted \(\ell^2\) norms on edge and cell copies of \(H\). Weighted
versions follow by conjugating \(D\) with the square roots of the weight
matrices.

### Theorem 7.1 (presentation-conditioned Hilbert rectification)

For translation responses, the nearest exact response in edge \(\ell^2\)
distance is

\[
\bar a=\bigl(I-D^\dagger D\bigr)\otimes I_H\,a,
\]

where \(D^\dagger\) is the Moore–Penrose inverse. Moreover,

\[
\operatorname{dist}_2(R,\operatorname{Exact}(K))
=\|(D^\dagger D\otimes I_H)a\|_2
\le \|D^\dagger\|_{2\to2}\,\|c\|_2.
\]

The optimal uniform constant over all nonexact translation assignments is

\[
\mathfrak S^{\mathrm{tr}}_2(K)
=\frac{1}{\sigma_{\min}^+(D)},
\]

with value \(0\) when \(D=0\).

**Proof.** Exact descent is equivalent to
\((D\otimes I_H)\bar a=0\), so exact assignments form the closed subspace
\(\ker(D\otimes I_H)\). Orthogonal projection onto this kernel is
\((I-D^\dagger D)\otimes I_H\), proving the first two formulas. On the
orthogonal complement of the kernel, the ratio
\(\|a\|_2/\|(D\otimes I_H)a\|_2\) is maximized by a right singular vector for
the smallest positive singular value of \(D\). \(\square\)

This theorem uses standard Hilbert projection/SVD machinery. The NCS
contribution is the interpretation of
\(\mathfrak S_2(K)\) as a **protocol rectifiability condition number**:
it distinguishes small observed local order defect from actual proximity to a
path-independent response protocol.

### 7.2 A genuinely noninvertible sector

Let every edge response be a constant map

\[
R_e(x)=a_e\in H.
\]

Such maps are 0-Lipschitz and noninvertible unless the fibers are trivial. A
nonempty path response is the constant attached to its last edge. Define the
terminal relation matrix

\[
D^{\mathrm{term}}_{\sigma e}
=\mathbf 1\{e=\operatorname{last}(p_\sigma)\}
 -\mathbf 1\{e=\operatorname{last}(q_\sigma)\}.
\]

### Corollary 7.2 (constant-map rectification)

Theorem 7.1 holds verbatim for constant responses after replacing \(D\) by
\(D^{\mathrm{term}}\).

**Proof.** Exactness is precisely
\((D^{\mathrm{term}}\otimes I_H)a=0\); the same orthogonal-projection argument
applies. \(\square\)

Thus the rectification question is meaningful beyond invertible holonomy or
group representations.

### Proposition 7.3 (no source-independent rectification constant)

For each \(N\ge1\), let \(K_N\) have two vertices, \(N+1\) parallel edges
\(e_0,\ldots,e_N\), and relations \(e_{i-1}\sim e_i\). Let
\(X_s=\{\ast\}\), \(X_t=\mathbb R\), and define the noninvertible constant
responses

\[
R_{e_i}(\ast)=i\varepsilon.
\]

Every elementary cell defect is \(\varepsilon\), but every exact response
\(\bar R\) satisfies

\[
\max_i d_\infty(R_{e_i},\bar R_{e_i})
\ge \frac{N\varepsilon}{2}.
\]

The bound is sharp.

**Proof.** Exactness forces all \(\bar R_{e_i}(\ast)\) to equal a common
\(c\). The smallest interval centered at \(c\) containing
\(\{0,\varepsilon,\ldots,N\varepsilon\}\) has radius
\(N\varepsilon/2\), attained at \(c=N\varepsilon/2\). \(\square\)

Consequently, local defect tending to zero does not imply uniform closeness
to exact response when presentation size/conditioning is uncontrolled. Taking
\(N=\lceil1/\varepsilon\rceil\) keeps the best rectification distance near
\(1/2\).

For the corresponding \(\ell^2\) problem, \(D^{\mathrm{term}}\) is the
path-graph difference matrix and

\[
\sigma_{\min}^+(D^{\mathrm{term}})
=2\sin\!\left(\frac{\pi}{2(N+1)}\right),
\]

so the stability constant grows asymptotically like \((N+1)/\pi\).

## 8. Smooth sector as a reduction

Let \(\pi:E\to B\) be a smooth feasible bundle with a Riemannian metric on
internal directions. Minimum-norm infinitesimal carry response is the
metric-orthogonal Ehresmann connection. This statement is classical.

For regular equality constraints \(F(b,x)=0\), put

\[
A=D_xF,\qquad C=D_bF,
\]

and let \(M\) be the positive-definite internal adjustment metric. The
minimum-cost feasible internal velocity over a base velocity \(u\) is

\[
v^*(u)=
-M^{-1}A^\top(AM^{-1}A^\top)^{-1}Cu.
\]

### Proposition 8.1 (small-square reduction; baseline)

For \(C^3\) data, commuting base directions \(u,v\), and a sufficiently small
coordinate square of side \(\varepsilon\), let \(P_{uv}^\varepsilon\) and
\(P_{vu}^\varepsilon\) be the two horizontal transports to the common target
fiber. In a vertical normal chart,

\[
\operatorname{vlog}\!\left(
P_{uv}^\varepsilon(x),P_{vu}^\varepsilon(x)\right)
=\varepsilon^2\Omega_x(u,v)+O(\varepsilon^3),
\]

uniformly on compact regular sets. Consequently,

\[
d(P_{uv}^\varepsilon(x),P_{vu}^\varepsilon(x))
=\varepsilon^2\|\Omega_x(u,v)\|+O(\varepsilon^3).
\]

**Proof sketch.** Expand the two ordered horizontal flows to second order or
apply the Baker–Campbell–Hausdorff commutator expansion. Their vertical
second-order difference is the vertical bracket of horizontal lifts, which is
the Ehresmann curvature up to the chosen sign convention. \(\square\)

The vector-valued first formula is primary; a scalar norm loses orientation
and nonabelian information.

## 9. Active-set seam sector and scaling separation

Let the common ambient state space be \(\mathbb R^2\), start at \(0\), and for
\(\varepsilon>0\) define

\[
A_\varepsilon=\{(x,y):x\ge\varepsilon\},\qquad
B_\varepsilon=\{(x,y):x+y\ge\varepsilon\}.
\]

The intervention square has vertices
\(\varnothing,A,B,AB\) with fibers

\[
X_S=\bigcap_{i\in S}i_\varepsilon.
\]

Every edge that adds a constraint carries the Euclidean projection onto the
new cumulative feasible fiber. Therefore every edge actually lands in its
declared target fiber.

Direct calculation gives

\[
\begin{aligned}
0\xrightarrow{A}(\varepsilon,0)
  \xrightarrow{B}(\varepsilon,0),\\
0\xrightarrow{B}(\varepsilon/2,\varepsilon/2)
  \xrightarrow{A}(\varepsilon,\varepsilon/2).
\end{aligned}
\]

Hence the order defect is exactly \(\varepsilon/2\). A full reset from the
original reference to \(A_\varepsilon\cap B_\varepsilon\) gives
\((\varepsilon,0)\), illustrating the reset/carry distinction on the same
feasible family.

### Proposition 9.1 (defect-scaling separation)

The following three small-intervention scalings are all possible:

1. regular smooth carry transport:
   \(\Delta_\varepsilon=\Theta(\varepsilon^2)\) when curvature is nonzero;
2. the active-set projection square above:
   \(\Delta_\varepsilon=\varepsilon/2=\Theta(\varepsilon)\);
3. a discontinuous route selection with two fixed distinct target outcomes:
   \(\Delta_\varepsilon=\Theta(1)\).

In particular, a measured \(\Theta(\varepsilon)\) or
\(\Theta(1)\) order defect cannot be reproduced, to leading order, by a
locally bounded \(C^2\) Ehresmann connection, whose square defect is
\(O(\varepsilon^2)\).

**Proof.** Item 1 is Proposition 8.1; item 2 is the exact projection
calculation; item 3 follows from the fixed target separation. The final claim
compares asymptotic orders. \(\square\)

This scaling signature is a falsifiable way to distinguish smooth curvature
from seam or jump response. It does not claim that every nonsmooth system
falls into exactly one of these three classes.

## 10. Stratified realization: restricted claim

A stratified response realization consists of:

- a stratified external space;
- a smooth response connection on each regular stratum;
- explicit, protocol-dependent partial seam maps for allowed stratum
  crossings;
- explicit junction ordering/regularization data where several seams meet.

A compatible finite directed cellulation produces a response assignment in
the sense of Definition 2.2. The general invariant at a seam or junction is
the two-route defect after composing the declared smooth and seam maps.

There is **no canonical additive decomposition** into “curvature + seam +
junction” for arbitrary metric fibers and noninvertible maps. Such a formula
requires additional affine or invertible structure. In the general theory,
only subadditive filling comparisons are claimed. This avoids conflating NCS
with scattering diagrams, exit-path transport, saltation products, or
distributional gauge curvature.

## 11. Exact computational checks

`examples/verify_foundations.py` checks three independent predictions:

1. for \(z-b_1x-b_2y=0\), the normalized two-order transport difference
   converges to the analytically computed curvature vector
   \((-y,x)\) at \(b=0\);
2. the unscaled active-set order defect is \(0.5\) at
   \(\varepsilon=1\);
3. a rectangular translation grid attains equality in the
   nonexpansive local-to-global bound.

The machine-readable results are stored in
`examples/results/foundation_checks.json`.

## 12. Novelty statement after formalization

The following are explicitly **not** claimed new:

- presented path categories or trace equivalence;
- quantitative diamonds or the telescoping derivation bound;
- edge transport, plaquette curvature, or gauge conjugacy;
- Ulam stability as a general question;
- Ehresmann curvature and small-loop holonomy;
- ordered projections, hybrid resets, wall crossing, or sequential recourse.

The proposed NCS contribution is narrower:

1. comparative-statics semantics for response functors whose state fibers and
   adjustments are part of the model;
2. failure-aware defects for partial/noninvertible repair protocols;
3. a presentation-conditioned rectifiability invariant, with exact positive
   and negative results in invertible and noninvertible sectors;
4. a common scaling diagnostic separating regular curvature, active-set seam,
   and jump order effects;
5. an application-facing program for testing and rectifying order-sensitive
   adjustment protocols across optimization, hybrid, computational, and
   economic systems.

Whether this combination warrants the name “new branch” remains contingent on
the adversarial review and on stronger cross-regime results in Checkpoint 3.
