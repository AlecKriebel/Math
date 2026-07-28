# Checkpoint 2 — Formal Solution

**Date:** 2026-07-28  
**Status:** PASS after adversarial proof and scope review

## 1. Audit semantics

Fix a finite, non-adaptively selected deletion set \(A\). Let \(\Pi_A\) be a
declared family of permitted orders in which the requests in \(A\) may be
processed. The external endpoint is the retained dataset \(D\setminus A\), so
the paths in \(\Pi_A\) are declared externally equivalent.

Let \((X,d)\) be the declared comparison space. Depending on the audit, its
points may be parameter vectors, prediction vectors on a fixed probe set,
functions modulo a gauge, or output laws equipped with a metric.

A carry protocol produces a terminal response \(y_\pi\in X\) for each successful
path \(\pi\). A selected reset semantics supplies one common target \(t_A\in X\):

- a deterministic canonical trainer on \(D\setminus A\); or
- the output law of a randomized canonical trainer on \(D\setminus A\).

Warm starts, cached optimizer state, data-dependent stopping, and arbitrary
random-seed coupling are part of the response protocol. They are not silently
identified with reset retraining.

### Definition 1 (uniform all-order target claim)

The protocol satisfies a uniform \(\varepsilon\)-target claim on \(\Pi_A\) if:

1. every path in \(\Pi_A\) is defined; and
2. \(d(y_\pi,t_A)\le\varepsilon\) for every \(\pi\in\Pi_A\).

An undefined route is a directional NCS failure and rejects the claim before a
value comparison is attempted.

The problem is to falsify this claim without computing \(t_A\).

The target semantics must name one common target or law. Route-conditioned,
seed-coupled, or set-valued retraining targets require a different formulation
and are outside this checkpoint.

## 2. The optimal target-free lower bound

For a nonempty finite set \(Y=\{y_1,\ldots,y_m\}\subset X\), define its
unrestricted Chebyshev radius

\[
  r_X(Y)=\inf_{z\in X}\max_{1\le a\le m} d(y_a,z)
\]

and diameter

\[
  \operatorname{diam}(Y)=\max_{a,b}d(y_a,y_b).
\]

The infimum convention is necessary because a center need not exist in an
arbitrary metric space.

### Theorem 2 (sharp output-only certificate)

For every candidate common target \(t\in X\),

\[
  \max_a d(y_a,t)
  \ge r_X(Y)
  \ge \frac12\operatorname{diam}(Y).
  \tag{2.1}
\]

Moreover, \(r_X(Y)\) is the greatest lower bound that can be guaranteed from
\(Y\) alone when the target is otherwise unconstrained in \(X\): if a number
\(B(Y)\) satisfies

\[
  \max_a d(y_a,t)\ge B(Y)
  \quad\text{for every }t\in X,
\]

then \(B(Y)\le r_X(Y)\).

#### Proof

The first inequality follows by substituting \(z=t\) into the infimum.
For every pair \(a,b\), the triangle inequality gives

\[
  d(y_a,y_b)\le d(y_a,z)+d(y_b,z)
  \le 2\max_c d(y_c,z).
\]

Take the maximum over pairs and then the infimum over \(z\) to obtain the second
inequality.

For optimality, suppose \(B(Y)>r_X(Y)\). By the definition of infimum there is a
\(z\in X\) with \(\max_a d(y_a,z)<B(Y)\), contradicting the claimed guarantee
at target \(t=z\). \(\square\)

Here “greatest” is a population/geometric statement about the fixed finite set
of observed route outputs. It is not a claim that:

- the observed paths exhaust an unobserved route family;
- a finite-sample confidence bound is statistically optimal; or
- the 1-center problem is computationally easy in every represented metric
  space.

### Corollary 3 (one-cell rejection rule)

If two observed deletion orders satisfy

\[
  d(y_\pi,y_\sigma)>2\varepsilon,
\]

then no common target can lie within \(\varepsilon\) of both. The uniform
\(\varepsilon\)-target claim is false.

This conclusion is independent of the unobserved target and of which of the two
routes is worse.

### Restricted target knowledge

If independent information restricts the reset target to a nonempty
\(T\subseteq X\), then

\[
  r_T(Y)=\inf_{z\in T}\max_a d(y_a,z)
\]

is a possibly stronger certificate. The claim that \(r_X\) is “greatest” always
refers to the absence of such additional target information.

## 3. Hilbert-space solution and error decomposition

Suppose \(X\) is a real Hilbert space and two routes return \(y_+\) and \(y_-\).
Write

\[
  c=y_+-y_-,
  \qquad
  m=\frac{y_++y_-}{2}.
\]

### Proposition 4 (two-route center and Pythagorean audit identity)

The unique minimum-enclosing-ball center is \(m\), with radius
\(\|c\|/2\). For every target \(t\),

\[
  \frac{\|y_+-t\|^2+\|y_--t\|^2}{2}
  =
  \|m-t\|^2+\frac{\|c\|^2}{4}.
  \tag{3.1}
\]

#### Proof

The parallelogram identity applied to
\(y_\pm-t=(m-t)\pm c/2\) proves (3.1). The maximum of two
nonnegative numbers is at least their average, so every center has maximum
squared distance at least \(\|c\|^2/4\). At \(m\), both distances equal
\(\|c\|/2\), proving optimality. Equality conditions give uniqueness. \(\square\)

The midpoint is the minimax order-neutral reconciliation and minimizes the sum
of squared corrections to the two routes. This says nothing about whether the
midpoint is close to the retraining target.

### Proposition 5 (zero-defect no-go)

No finite-valued function of route disagreement alone can give a universal
upper bound on retraining error.
Specifically, for every \(M>0\), there is a protocol whose paths all agree but
whose common output is distance \(M\) from the reset target.

#### Proof

Take \(X=\mathbb R\), target \(t=0\), and let every deletion map be the constant
map with value \(M\). Every path returns \(M\), so every relation-cell defect
and every route radius is zero, while the target error is \(M\). \(\square\)

Thus:

- a radius exceeding the declared tolerance is a sound rejection witness;
- a zero radius proves only route consistency;
- midpoint or commutator cancellation is coherence rectification, not fidelity
  rectification.

## 4. Stochastic route laws

Let the terminal response under route \(\pi\) be a law \(P_\pi\) on an output
space \(\mathcal Z\), and let the selected reset law be \(Q_A\). The laws must
match the claim's randomness:

- cloning one trained checkpoint estimates conditional laws
  \(P_{\pi\mid W=w_0}\) and must be compared with a conditional reset semantics;
  or
- an end-to-end algorithm-level claim requires independent reruns of original
  training and unlearning, producing marginal laws over both sources of
  randomness.

A conditional route law must not be compared silently with an unconditional
reset law. Equip the correctly matched laws with a declared metric
\(d_{\mathcal P}\). Theorem 2 applies verbatim:

\[
  \max_\pi d_{\mathcal P}(P_\pi,Q_A)
  \ge r_{\mathcal P}(\{P_\pi\})
  \ge \frac12\max_{\pi,\sigma}
  d_{\mathcal P}(P_\pi,P_\sigma).
  \tag{4.1}
\]

A coupled, common-seed difference does not by itself reject a claim about
marginal laws. The audit must match the semantics of the claimed guarantee.
Stochastic failure is handled either by including a distinguished failure
symbol in \(\mathcal Z\), or by separately testing a declared failure-
probability tolerance. One random crash rejects only an almost-sure
availability claim.

### 4.1 MMD specialization

Let \(k\) be a positive-definite characteristic kernel with feature map
\(\phi:\mathcal Z\to\mathcal H_k\) and

\[
  k(z,z)=\|\phi(z)\|_{\mathcal H_k}^2\le K.
\]

For a law \(P\), let
\(\mu_P=\mathbb E_P[\phi(Z)]\). Then

\[
  \operatorname{MMD}_k(P,Q)=\|\mu_P-\mu_Q\|_{\mathcal H_k}
\]

is a metric. For finitely many route laws, their Hilbert-space minimum
enclosing-ball center lies in the convex hull of their mean embeddings. That
convex combination is the mean embedding of the corresponding mixture of route
laws, so the radius is attainable within the class of probability laws.

### 4.2 A simultaneous finite-sample lower confidence bound

Suppose \(s\) route laws are audited. For route \(a\), observe
\(n_a\) independent replicates
\(Z_{a1},\ldots,Z_{a n_a}\sim P_a\), and define

\[
  \widehat\mu_a=\frac1{n_a}\sum_{\ell=1}^{n_a}\phi(Z_{a\ell}).
\]

Replicates must be independent within each route. Dependence across routes,
including common random numbers paired by replicate, is allowed because the
proof uses marginal concentration and a union bound.
Each replicate reruns the complete route with a fresh within-route seed.

For confidence level \(1-\delta\), with \(0<\delta<1\), set

\[
  e_a(\delta)
  =
  \sqrt{\frac K{n_a}}
  +
  \sqrt{\frac{2K\log(s/\delta)}{n_a}}.
  \tag{4.2}
\]

### Theorem 6 (simultaneous MMD margin certificate)

With probability at least \(1-\delta\), simultaneously for all \(a\),

\[
  \|\widehat\mu_a-\mu_a\|_{\mathcal H_k}\le e_a(\delta).
  \tag{4.3}
\]

Consequently, for every pair \(a,b\),

\[
  \operatorname{MMD}_k(P_a,P_b)
  \ge
  L_{ab}
  :=
  \left[
  \|\widehat\mu_a-\widehat\mu_b\|
  -e_a-e_b
  \right]_+.
  \tag{4.4}
\]

If \(\widehat r\) is the minimum-enclosing-ball radius of
\(\{\widehat\mu_a\}_{a=1}^s\) in \(\mathcal H_k\), then

\[
  r_{\mathcal H_k}(\{\mu_a\})
  \ge
  L_{\mathrm{rad}}
  :=
  \left[\widehat r-\max_a e_a\right]_+.
  \tag{4.5}
\]

Therefore either of the following rejects, with family-wise error at most
\(\delta\), the claim that every route law lies within MMD distance
\(\varepsilon\) of one common reset law:

\[
  \max_{a,b}L_{ab}>2\varepsilon,
  \qquad\text{or}\qquad
  L_{\mathrm{rad}}>\varepsilon.
  \tag{4.6}
\]

#### Proof

For one route,

\[
\begin{aligned}
\mathbb E\|\widehat\mu_a-\mu_a\|
&\le
\sqrt{\mathbb E\|\widehat\mu_a-\mu_a\|^2}\\
&=
\sqrt{\frac1{n_a}
\left(\mathbb E\|\phi(Z)\|^2-\|\mu_a\|^2\right)}
\le \sqrt{\frac K{n_a}}.
\end{aligned}
\]

Changing one replicate changes the empirical mean, and hence the norm of its
error, by at most \(2\sqrt K/n_a\). McDiarmid's inequality gives

\[
  \Pr\!\left[
  \|\widehat\mu_a-\mu_a\|
  >
  \sqrt{K/n_a}+t
  \right]
  \le
  \exp\!\left(-\frac{n_a t^2}{2K}\right).
\]

Choose \(t=\sqrt{2K\log(s/\delta)/n_a}\) and union-bound the
\(s\) routes to obtain (4.3).

Equation (4.4) follows from the reverse triangle inequality. For (4.5), the two
finite point sets \(\{\mu_a\}\) and \(\{\widehat\mu_a\}\) are within Hausdorff
distance at most \(\max_a e_a\). A minimum-enclosing-ball radius changes by at
most the Hausdorff distance: use the same center for the perturbed set in each
direction. Finally apply (4.1). \(\square\)

### Audit-design constraints

1. The kernel, tolerance, route family, and confidence level must be
   predeclared or selected on independent data. A predeclared finite kernel
   family may use a simultaneous multiplicity correction; continuous
   data-adaptive optimization needs sample splitting or a valid uniform
   confidence bound.
2. Ordinary rejection of \(P_a=P_b\) is insufficient for a nonzero tolerance.
   The lower confidence **margin** must exceed \(2\varepsilon\), or the radius
   margin must exceed \(\varepsilon\).
3. If replicates are temporally dependent, the concentration argument must be
   replaced by a valid dependent-sample bound.
4. MMD measures the declared output law. It is not by itself a privacy or
   deletion semantic.
5. The empirical statistic in Theorem 6 is the RKHS norm of the two empirical
   mean embeddings (the biased MMD), not the usual unbiased estimator of
   \(\operatorname{MMD}^2\), which can be negative.
6. A numerical minimum-enclosing-ball routine must return a certified lower
   bound, or its proven optimization error must be subtracted before rejection.
   An unqualified approximate enclosing radius can be an anti-conservative
   overestimate.

## 5. Boolean-cube presentation of deletion requests

Let \(A=\{1,\ldots,q\}\). External vertices are subsets \(S\subseteq A\).
For \(i\notin S\), the edge

\[
  S\xrightarrow{i}S\cup\{i\}
\]

processes deletion \(i\). For \(i,j\notin S\), attach the contextual square

\[
  (S\xrightarrow{i}S i\xrightarrow{j}Sij)
  \;\Rightarrow\;
  (S\xrightarrow{j}S j\xrightarrow{i}Sij).
  \tag{5.1}
\]

For \(q\ge2\), there are

\[
  \binom q2 2^{q-2}
\]

contextual squares in the full Boolean cube. This exponential count must not be
misreported as merely quadratic.

Let the response edges be context-dependent partial maps

\[
  U_i^S:X_S\rightharpoonup X_{S\cup\{i\}}.
\]

### Proposition 7 (contextual-square completeness)

If, on every contextual square, the two composites have equal domains and equal
values, then all monotone deletion paths with the same endpoints induce the
same partial response map.

#### Proof

Any two permutations of a fixed set differ by adjacent transpositions. Each
adjacent transposition is one contextual square (5.1). Equality of partial maps
is preserved by composition, so replacing squares along a transposition chain
proves equality of the path composites. \(\square\)

This is standard cubical/confluence reasoning. Its value here is to specify the
correct audit units and to keep domain failure distinct from value error.

### Stateless specialization

If all fibers are one common \(X\), all maps are total, and \(U_i^S=U_i\) is
independent of context, then equality for every subset endpoint (equivalently,
for all request words up to permutation) holds iff the \(\binom q2\)
identities

\[
  U_jU_i=U_iU_j
  \quad(i<j)
\]

hold. Pairwise commutation need not be necessary if one checks only the
full-\(A\) endpoint: a noncancellative suffix can mask an earlier
noncommuting pair.

For approximate cells, a bound on a long-path defect additionally requires the
NCS filling calculation: each local cell residual is multiplied by the
Lipschitz modulus of the suffix that transports it to the endpoint. Small local
defects alone do not imply a small global defect under an amplifying suffix.

## 6. Complete affine cell tests

Suppose one contextual square has common affine domain \(\mathbb R^d\) and
affine edge maps. Its defect is

\[
  \Omega(\theta)
  =
  U_j^{S\cup i}U_i^S(\theta)
  -
  U_i^{S\cup j}U_j^S(\theta)
  =
  M\theta+c.
\]

Let \(\theta_0,\ldots,\theta_r\) be an affine basis of an \(r\)-dimensional
reachable affine hull \(L\). Define linear maps \(V,W\) from
\(\mathbb R^r\), where \(V\) is injective (indeed, an isomorphism onto
\(\operatorname{dir}(L)\)), by

\[
\begin{aligned}
  Va&=\sum_{k=1}^r a_k(\theta_k-\theta_0),\\
  Wa&=\sum_{k=1}^r a_k
  \bigl(\Omega(\theta_k)-\Omega(\theta_0)\bigr).
\end{aligned}
\]

Paired route evaluations reconstruct the restriction invariantly:

\[
\boxed{
  \Omega(\theta_0+Va)=\Omega(\theta_0)+Wa
  \quad\text{for every }a\in\mathbb R^r.
}
  \tag{6.1}
\]

In any chosen coordinate chart on \(L\), this is the usual affine
interpolation formula. When \(r<d\), the probes determine only the affine
restriction to \(L\); they do not identify a unique ambient matrix \(M\) or
offset \(c\).

### Proposition 8 (affine-basis completeness)

The affine square commutes on \(L\) iff its defect vanishes on one affine basis
of \(L\). On the simplex
\(\Delta=\operatorname{conv}\{\theta_0,\ldots,\theta_r\}\),

\[
  \sup_{\theta\in\Delta}\|\Omega(\theta)\|
  =
  \max_{0\le a\le r}\|\Omega(\theta_a)\|.
  \tag{6.2}
\]

#### Proof

An affine map is determined by its values on an affine basis, proving the first
claim and (6.1). For
\(\theta=\sum_a\lambda_a\theta_a\) in the simplex,

\[
  \|\Omega(\theta)\|
  =
  \left\|\sum_a\lambda_a\Omega(\theta_a)\right\|
  \le
  \sum_a\lambda_a\|\Omega(\theta_a)\|
  \le
  \max_a\|\Omega(\theta_a)\|.
\]

The reverse inequality holds because the vertices belong to the simplex.
\(\square\)

This replaces infinitely many state queries by \(r+1\) paired evaluations per
affine cell under a trusted affine-map promise, a common valid domain
containing the tested hull, and exact evaluations. It does not:

- make invalid or unreachable basis probes legitimate;
- establish from the basis agreement alone that a black box is affine;
- audit unequal partial domains;
- remove the exponential number of contextual cells in the general
  context-dependent cube; or
- certify fidelity to retraining.

Noisy evaluations require a separate statistical and conditioning analysis,
especially for a nearly singular affine basis.

## 7. Fixed-preconditioner relinearized ridge deletion

Consider the fixed-normalization ridge objective

\[
  F_D(\theta)
  =
  \frac12\sum_{k\in D}(x_k^\top\theta-y_k)^2
  +\frac\lambda2\|\theta\|^2,
  \qquad \lambda>0.
  \tag{7.1}
\]

Write

\[
  H=\lambda I+\sum_{k\in D}x_kx_k^\top,
  \qquad
  b=\sum_{k\in D}y_kx_k,
  \qquad
  \theta_D=H^{-1}b.
\]

Fix a symmetric positive-definite preconditioner \(P\). The relinearized
single-request update is

\[
  U_i^\tau(\theta)
  =
  \theta+\tau P x_i(x_i^\top\theta-y_i),
  \tag{7.2}
\]

where \(\tau\in[0,1]\) is deletion amplitude. This is a specific approximate
protocol: it re-evaluates example \(i\)'s residual at the current carried state
while retaining the same preconditioner.

Let

\[
  r_i(\theta)=x_i^\top\theta-y_i,
  \qquad
  \alpha_{ij}=x_j^\top P x_i.
\]

### Theorem 9 (exact ridge relation-cell defect)

For distinct requests \(i,j\) and every \(\tau\in[0,1]\),

\[
\boxed{
  U_j^\tau U_i^\tau(\theta)
  -
  U_i^\tau U_j^\tau(\theta)
  =
  \tau^2\alpha_{ij}
  \left[
  P x_j r_i(\theta)-P x_i r_j(\theta)
  \right].
}
  \tag{7.3}
\]

For \(\tau\in(0,1]\), nonzero features, and positive-definite \(P\), the two
affine maps commute at every state iff either

\[
  x_i^\top P x_j=0,
  \tag{7.4}
\]

or there is a nonzero scalar \(c\) with

\[
  (x_j,y_j)=c(x_i,y_i).
  \tag{7.5}
\]

At \(\tau=0\), both maps are the identity regardless of (7.4)--(7.5). If the
coefficient in (7.3) is nonzero at a start state that is independent of
\(\tau\), this cell has NCS response order \(2\) under the calibrated amplitude
\(\tau\).

#### Proof

Because

\[
  r_j(U_i^\tau\theta)
  =
  r_j(\theta)+\tau x_j^\top P x_i\,r_i(\theta),
\]

direct substitution in the two composites leaves exactly (7.3).

If \(\alpha_{ij}=0\), the defect vanishes. Suppose
\(\alpha_{ij}\ne0\). The affine bracket vanishes for every \(\theta\) only if

\[
  x_jx_i^\top-x_ix_j^\top=0
  \quad\text{and}\quad
  x_jy_i-x_iy_j=0,
\]

after multiplying by \(P^{-1}\). For nonzero real vectors, the first identity
means \(x_j=cx_i\) for some nonzero \(c\); the second then gives
\(y_j=cy_i\). The converse is immediate. Exact quadratic scaling by
\(\tau^2\) proves the response-order statement. \(\square\)

### Corollary 10 (target-free parameter and objective lower bounds)

In this corollary write \(U_i=U_i^{\tau=1}\), and let

\[
  z_{ij}=U_jU_i(\theta_D),
  \qquad
  z_{ji}=U_iU_j(\theta_D),
\]

and let \(\theta_{-ij}\) be the unique exact ridge minimizer after deleting
\(i,j\). In every norm,

\[
  \max\{\|z_{ij}-\theta_{-ij}\|,
         \|z_{ji}-\theta_{-ij}\|\}
  \ge \frac12\|z_{ij}-z_{ji}\|.
  \tag{7.6}
\]

Let

\[
  H_{-ij}=H-x_ix_i^\top-x_jx_j^\top.
\]

Because \(H_{-ij}\succeq\lambda I\),

\[
  \max\{
  F_{-ij}(z_{ij})-F_{-ij}(\theta_{-ij}),
  F_{-ij}(z_{ji})-F_{-ij}(\theta_{-ij})
  \}
  \ge
  \frac18\|z_{ij}-z_{ji}\|_{H_{-ij}}^2
  \ge
  \frac\lambda8\|z_{ij}-z_{ji}\|_2^2.
  \tag{7.7}
\]

Thus an operator that knows the retained Hessian, or only the regularization
floor \(\lambda\), obtains a target-free lower bound on worst-route objective
excess without solving for \(\theta_{-ij}\).

#### Proof

Equation (7.6) is Theorem 2 (or directly the triangle inequality). For the
quadratic retained objective,

\[
  F_{-ij}(z)-F_{-ij}(\theta_{-ij})
  =\frac12\|z-\theta_{-ij}\|_{H_{-ij}}^2.
\]

Apply (7.6) in the \(H_{-ij}\) norm, square it, multiply by \(1/2\), and use
\(H_{-ij}\succeq\lambda I\). \(\square\)

### Exact error decomposition

Let \(m=(z_{ij}+z_{ji})/2\). Proposition 4 gives

\[
\begin{aligned}
&\frac{
 [F_{-ij}(z_{ij})-F_{-ij}(\theta_{-ij})]
 +[F_{-ij}(z_{ji})-F_{-ij}(\theta_{-ij})]
}{2}\\
&\qquad
=
\frac12\|m-\theta_{-ij}\|_{H_{-ij}}^2
+\frac18\|z_{ij}-z_{ji}\|_{H_{-ij}}^2.
\tag{7.8}
\end{aligned}
\]

The second term is the exact antisymmetric order contribution to mean
two-route objective excess. The first, target-dependent term can remain large
after perfect order symmetrization.

## 8. Protocol distinctions and exact quadratic reset

### Frozen-vector influence is coherent but can be wrong

If residuals are frozen at one reference state \(\theta_0\),

\[
  \widetilde U_i(\theta)
  =
  \theta+P x_i r_i(\theta_0),
\]

then every update is a translation and all updates commute. Proposition 5
still applies: zero cell defect does not bound retraining error.

### Exact batch ridge deletion

For a batch \(A\) whose feature columns form the matrix \(X_A\), and label vector
\(y_A\), define

\[
  G_A=X_A^\top\theta_D-y_A.
\]

If \(H-X_AX_A^\top\) is positive definite, Sherman--Morrison--Woodbury gives

\[
  \theta_{-A}
  =
  \theta_D
  +
  H^{-1}X_A
  (I-X_A^\top H^{-1}X_A)^{-1}
  G_A.
  \tag{8.1}
\]

This depends only on the deletion set, not its ordering. An exact
retained-Hessian quadratic Newton update is the same reset target and has zero
cell defect. Formula (8.1) is established quadratic algebra, used here as a
validation oracle rather than a claimed contribution.

### Why half-commutator correction is insufficient

For two points let
\[
  G=x_ix_i^\top+x_jx_j^\top,
  \qquad
  g=x_ir_i(\theta_D)+x_jr_j(\theta_D),
  \qquad P=H^{-1}.
\]

The exact target displacement is

\[
  \theta_{-ij}-\theta_D
  =
  (I-PG)^{-1}Pg.
\]

If
\(\rho=\|H^{-1/2}GH^{-1/2}\|_2<1\), its Neumann expansion is

\[
  Pg+PGPg+R_3,
  \qquad
  \|R_3\|_H
  \le
  \frac{\rho^2}{1-\rho}\|Pg\|_H.
  \tag{8.2}
\]

where

\[
  R_3=\sum_{k\ge2}(PG)^kPg,
  \qquad
  \|PG\|_{H\to H}
  =
  \|H^{-1/2}GH^{-1/2}\|_2
  =\rho.
\]

The midpoint of the two relinearized sequential routes cancels the
antisymmetric commutator but contains only half of the two cross terms and none
of the required self-interaction terms. Therefore commutator cancellation does
not recover the second-order batch correction.

## 9. Solved audit protocol

### Algorithm: PC-Audit

**Input**

- a declared conditional-on-checkpoint or end-to-end randomness semantics;
- one clonable checkpoint for a deterministic or conditional audit, or
  independent training reruns for an end-to-end audit;
- a fixed, non-adaptive deletion set;
- permitted deletion orders or contextual exchange cells;
- a declared comparison space and metric;
- tolerance \(\varepsilon\);
- for stochastic output, a predeclared bounded characteristic kernel,
  route replicate counts, and family-wise error \(\delta\).

**Procedure**

1. Generate route replicates under the declared randomness semantics. Clone the
   same checkpoint for each path only in the deterministic or conditional
   setting.
2. Execute the selected externally equivalent deletion orders.
3. Record route-definedness. In a deterministic audit, reject an all-order
   availability claim on any directional failure. In a stochastic audit,
   include failure in the output law or audit its probability separately.
4. Deterministic case:
   compute the observed Chebyshev radius when tractable, a certified numerical
   lower bound, or the half-diameter lower bound. Reject if the certified lower
   bound exceeds \(\varepsilon\).
5. Stochastic case:
   compute empirical mean embeddings, the pair bounds (4.4), and, when useful,
   the empirical mean-embedding radius. Reject only under (4.6).
6. Affine internal audit:
   only under a trusted affine promise and state-injection access, use a common
   valid reachable affine basis to reconstruct each tested square defect by
   (6.1). Exact equality of every relevant contextual square, including its
   domain, implies path consistency by Proposition 7.
7. If no rejection occurs, return **inconclusive**, never “certified
   unlearned.”

### What the certificate supplies

At the population/geometric level, the construction defines the sharp
output-only lower bound for a fixed observed route family:

> From path outputs alone, identify the sharp unrestricted common-target lower
> bound; compute it when the declared space has a tractable certified
> minimum-enclosing-ball method, or return a sound weaker bound such as half
> the diameter; and reject only when the certified bound crosses the declared
> margin.

Exact computation is available in the Hilbert and small finite cases used
below; the half-diameter remains an always-computable certified lower bound
once pairwise distances are available. The construction also gives a
conservative finite-sample family-wise MMD rejection rule and, under its
explicit promises, a complete finite-query test for each affine relation cell
on a declared reachable affine hull.

PC-Audit is a sound, incomplete rejection certificate, not a decision or
semidecision procedure for all failures. Proposition 5 supplies false target
claims that it can never reject.

### What remains unsolved

- positive certification that data were forgotten;
- selection of a semantically adequate output metric;
- scalable coverage of exponentially many context-dependent squares;
- adaptive deletion requests whose choice depends on intermediate releases;
- high-dimensional affine-basis testing when off-manifold states are invalid;
- deep-model empirical validation sufficient for a standalone ML systems
  claim.

## 10. Theorem-level prior-art boundary

The following ingredients are established and are not standalone novelty
claims:

- Chebyshev radii, minimum enclosing balls, and the half-diameter inequality;
- the Hilbert midpoint/parallelogram identity;
- kernel mean embeddings, MMD concentration, and tolerance-margin testing;
- Boolean-cube/confluence generation by adjacent swaps;
- determination of an affine map from an affine basis;
- influence-function and fixed-preconditioner expansions;
- Sherman--Morrison--Woodbury exact ridge deletion; and
- Neumann-series remainder bounds.

The proposed contribution is the unlearning-specific synthesis: declare
deletion permutations as NCS relation cells, use their population radius as
the sharp output-only lower bound against an otherwise unconstrained common
retraining target, and attach a valid conservative stochastic rejection rule.
Theorem 9 is an exact illustrative calculation for one named protocol, not a
new general theory of order-dependent unlearning.
