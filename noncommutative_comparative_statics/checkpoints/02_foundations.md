# Checkpoint 2 — Revised Foundations

**Status:** accepted as a synthesis/framework checkpoint after a 9/14
adversarial re-review; rejected as a novelty-bearing theorem checkpoint.

The rejected first draft is preserved as `02a_foundations_rejected.md`. The
main corrections are:

1. responses now live in partial **Lipschitz**, not necessarily nonexpansive,
   maps;
2. failure is reported by a domain/value signature instead of being collapsed
   into the numbers \(0\) and \(+\infty\);
3. the Moore–Penrose rectification estimate is acknowledged as imported
   Hyers–Ulam theory;
4. signed-distance guard robustness is used as an imported baseline for when a
   finite order difference becomes a hard one-sided feasibility failure;
5. native applications instantiate the same object and yield prospective
   falsifiable consequences.

## 1. Weighted presented intervention data

### Definition 1.1 (intervention presentation)

An intervention presentation is finite data

\[
K=(K_0,K_1,K_2,\{p_\sigma\Rightarrow q_\sigma\}_{\sigma\in K_2},w_1,w_2),
\]

where:

- \(K_0,K_1\) form a directed graph;
- \(p_\sigma,q_\sigma\) are nonempty parallel paths;
- \(w_1(e)>0\) and \(w_2(\sigma)>0\) are operational weights.

The cell \(p_\sigma\Rightarrow q_\sigma\) declares that the two paths have the
same net *external* meaning. This independence/exchange semantics is model
data, not a mathematical consequence.

Let \(\operatorname{Path}(K)\) be the free path category and let

\[
\mathcal C_K=\operatorname{Path}(K)/\langle
p_\sigma=q_\sigma:\sigma\in K_2\rangle
\]

be the presented intervention category.

The weighted presentation is intentionally part of the physical protocol. A
duplicated relation that carries no new evidence must split the original cell
weight among its copies. This convention makes the weighted residual energy
unchanged by literal duplication, but it does not solve general quantitative
Tietze/refinement invariance.

## 2. Response assignments

### Definition 2.1 (partial Lipschitz category)

Let \(\mathbf{pMetPar}_{\mathrm{Lip}}\) have separated extended metric spaces
as objects. An arrow \(T:X\rightharpoonup Y\) consists of a domain
\(\operatorname{Dom}T\subseteq X\) and a map
\(T:\operatorname{Dom}T\to Y\) for which some finite \(L\) satisfies
\[
d_Y(Tx,Tx')\le Ld_X(x,x')
\]
whenever \(d_X(x,x')<+\infty\). Its modulus
\(\operatorname{Lip}T\) is the infimum of such \(L\). This convention avoids
the undefined product \(0\cdot+\infty\). Composition uses

\[
\operatorname{Dom}(S\circ T)=
\{x\in\operatorname{Dom}T:T(x)\in\operatorname{Dom}S\}.
\]

Lipschitz constants multiply, so these arrows form a category. Partial
nonexpansive maps are the \(L\le1\) subcategory.

### Definition 2.2 (response assignment)

A deterministic response assignment is a functor

\[
R:\operatorname{Path}(K)\longrightarrow
\mathbf{pMetPar}_{\mathrm{Lip}}.
\]

Thus every parameter vertex has a feasible-state fiber \(X_b\), and every
elementary intervention has a possibly partial stateful response
\(R_e:X_{s(e)}\rightharpoonup X_{t(e)}\).

A cost or optimization model *generates* such an edge only after existence,
selection, and a finite Lipschitz modulus have been proved or declared.
Uniqueness of an argmin alone is insufficient: minimizing
\((y-2x)^2\) produces the expansive map \(x\mapsto2x\). Metric projections
onto nonempty closed convex Hilbert sets are an important nonexpansive special
case.

The response is exact relative to \(K\) when it factors through
\(\mathcal C_K\).

## 3. Domain/value order signature

Let \(p,q:a\to b\) be parallel paths and write
\(D_p=\operatorname{Dom}R_p\), \(D_q=\operatorname{Dom}R_q\).

### Definition 3.1 (deterministic signature)

The order signature of \(p,q\) consists of:

\[
\begin{aligned}
\mathsf A^+_{p,q}&=D_p\setminus D_q
&&\text{(only \(p\) succeeds)},\\
\mathsf A^-_{p,q}&=D_q\setminus D_p
&&\text{(only \(q\) succeeds)},\\
\mathsf C_{p,q}&=X_a\setminus(D_p\cup D_q)
&&\text{(both fail)},\\
\mathsf V_{p,q}(x)&=d_b(R_px,R_qx),
\quad x\in D_p\cap D_q
&&\text{(value defect)}.
\end{aligned}
\]

This keeps three scientifically different events separate:

- route-asymmetric feasibility;
- common failure, which is order-independent but undesirable;
- finite disagreement between two successful outcomes.

The old failure completion is retained only as shorthand. It is never used as
the sole reported statistic.

### Definition 3.2 (distributional summary)

For a probability measure \(\mu\) on \(X_a\), a truncation scale \(M>0\), and
measurable domains/maps, define the directional failure rates

\[
\begin{aligned}
A_\mu^+(p,q)&=\mu(D_p\setminus D_q),\\
A_\mu^-(p,q)&=\mu(D_q\setminus D_p),\\
C_\mu(p,q)&=\mu(\mathsf C_{p,q}),\\
V_{\mu,M}(p,q)&=
\int_{D_p\cap D_q}
\min\!\left\{1,\frac{d_b(R_px,R_qx)}{M}\right\}\,d\mu(x).
\end{aligned}
\]

The quadruple
\((A_\mu^+,A_\mu^-,C_\mu,V_{\mu,M})\) is the empirical order signature. Its
total route-asymmetric failure rate is
\(A_\mu^{\leftrightarrow}=A_\mu^++A_\mu^-\). The split is essential: the
total alone cannot report which order fails. After totalizing a partial map by
an undefined symbol, this is a decomposed bounded \(L^1\) comparison plus
common-undefined mass; it is proposed as application-facing reporting, not as
a new mathematical object.

### Proposition 3.3 (exact descent; baseline)

\(R\) factors through \(\mathcal C_K\) if and only if, for every relation
cell \(\sigma\),

\[
\mathsf A^+_\sigma=\mathsf A^-_\sigma=\varnothing,
\qquad
\mathsf V_\sigma\equiv0.
\]

Common failure may remain and must be reported separately.

**Proof.** The displayed conditions say exactly that the two partial maps have
the same domain and the same value at every point in that domain. The
universal property of the presented category gives the factorization.
\(\square\)

We assume separated extended metrics and adopt
\(\sup\varnothing=0\), \(\inf\varnothing=+\infty\).

## 4. Morphisms, equivalence, and gauge

### Definition 4.1 (presentation-response morphism)

An **unweighted semantic morphism**
\((F,\eta):(K,R)\to(K',R')\) consists of:

1. a functor
   \(F:\operatorname{Path}(K)\to\operatorname{Path}(K')\) satisfying
   \(F(p_\sigma)\sim_{K'}F(q_\sigma)\) for every relation of \(K\);
2. a natural transformation with total finite-Lipschitz components
   \(\eta:R\Rightarrow R'F\) in
   \(\mathbf{pMetPar}_{\mathrm{Lip}}\), including equality of the relevant
   partial-map domains.

This permits one elementary intervention to map to a refined path.
Composition is functor and natural-transformation composition. This notion
deliberately forgets \(w_1,w_2\). A quantitative morphism must additionally
choose target derivations for source cells and bound edge-path and
cell-derivation weight distortion; no canonical version is asserted here.

A response isomorphism has an inverse of the same kind. A gauge equivalence
has \(F=\mathrm{id}\) and fiberwise bijective isometries. Under gauge
equivalence, route domains correspond and all value defects are preserved.
Uniformly bi-Lipschitz fiber changes give two-sided distortion bounds.

Presentation equivalence, semantic equivalence of the quotient categories,
and gauge equivalence of responses are distinct notions.

## 5. Baseline filling calculus

Let \(P_0=p,\ldots,P_N=q\) be a square-swap derivation at \(x\) such that every
route \(P_i\) is defined at \(x\). At swap \(i\), write the two routes as a
common prefix \(a_i\), alternative cell sides \(u_i,v_i\), and common suffix
\(b_i\). Choose a positive finite Lipschitz bound \(L_{b_i}>0\) for every
suffix response.

### Proposition 5.1 (admissible derivation bound; baseline)

\[
d(R_px,R_qx)\le
\sum_{i=0}^{N-1}
L_{b_i}\,
d(R_{u_i}R_{a_i}x,R_{v_i}R_{a_i}x).
\]

**Proof.** Use the triangle inequality across successive route outcomes and
the Lipschitz bound for each common suffix. \(\square\)

Using positive bounds avoids the indeterminate product \(0\cdot+\infty\) in
extended metrics. The response filling cost is the infimum of the right-hand
side over such *admissible* derivations and valid positive suffix bounds. It
is \(+\infty\) if none exists. Ordinary combinatorial filling area can replace
it only for total maps or under a domain-robustness hypothesis. This
proposition is quantitative-rewriting prior art, not a novelty theorem.

## 6. Imported guard-robustness baseline for partial response

The key partial-map phenomenon is that a small finite value defect can be
converted by a later intervention into one-sided infeasibility.

For a subset \(D\subseteq Y\), define the membership margin

\[
m_D(y)=
\begin{cases}
\operatorname{dist}(y,Y\setminus D),&y\in D,\\
\operatorname{dist}(y,D),&y\notin D.
\end{cases}
\]

Empty-set distances are \(+\infty\).

### Lemma 6.1 (signed-distance guard robustness; imported)

Let \(p,q:X\rightharpoonup Y\) be two route responses, let
\(r:Y\rightharpoonup Z\) be a continuation with domain \(D\) and Lipschitz
constant \(L\), and fix \(x\in\operatorname{Dom}p\cap\operatorname{Dom}q\).
Put

\[
y=p(x),\qquad y'=q(x),\qquad \delta=d_Y(y,y').
\]

If

\[
\delta<m_D(y),
\]

then \(y\in D\) if and only if \(y'\in D\). If they lie in \(D\), then

\[
d_Z(r(y),r(y'))\le L\delta.
\]

The same conclusion follows with \(m_D(y')\) in place of \(m_D(y)\).

**Proof.** If \(y\in D\) and \(y'\notin D\), then by definition
\(\delta\ge\operatorname{dist}(y,Y\setminus D)=m_D(y)\), a contradiction.
The case \(y\notin D,y'\in D\) is identical. Once both lie in \(D\), the
Lipschitz inequality applies. \(\square\)

This is the absolute signed-distance robustness certificate for the Boolean
predicate \(1_D\). Fainekos and Pappas proved the corresponding
truth-preservation result for predicates and temporal/hybrid traces. The NCS
substitution \(y=p(x),y'=q(x)\) supplies response-path semantics but no new
mathematical theorem.

### Corollary 6.2 (one-step boundary-exposure bound; baseline)

For \(E=\operatorname{Dom}p\cap\operatorname{Dom}q\), put
\(\delta(x)=d_Y(p(x),q(x))\). Assume the quantities below are measurable and
define the two-sided one-step seam exposure

\[
S_\mu^\cap(p,q;r)=
\mu\!\left(
\left\{x\in E:
\max(m_D(p(x)),m_D(q(x)))\le\delta(x)
\right\}\right).
\]

Then

\[
A_\mu^{\leftrightarrow}(rp,rq)
\le A_\mu^{\leftrightarrow}(p,q)+S_\mu^\cap(p,q;r).
\]

**Proof.** Partition inputs into original one-sided prefix failure, common
prefix failure, and common prefix success. The first class is charged to
\(A_\mu^{\leftrightarrow}(p,q)\); in the second, both composites fail. In the
third, continuation membership can differ only if both endpoint margins are
at most their mutual distance, by Lemma 6.1. \(\square\)

If \(\delta(x)\le\varepsilon\) on \(E\), the final set may be enlarged by
replacing \(\delta(x)\) with \(\varepsilon\). This is an indicator union bound
closely related to adversarial boundary risk, not a novelty theorem. Its NCS
role is to specify which independently measurable quantities can predict
failure conversion.

### Necessity of the margin term

Take \(p(\ast)=0\), \(q(\ast)=\varepsilon\), and let the continuation domain be
\((-\infty,\varepsilon/2)\). The prefix value defect is \(\varepsilon\), but
exactly one continuation succeeds. Both endpoints lie within
\(\varepsilon\) of the seam. No bound based only on \(L\delta\) can capture
this conversion.

## 7. Affine-contractive rectification as an imported baseline

The first draft incorrectly presented a Moore–Penrose residual bound as a new
rectification theorem. The correct role of that result is baseline
Hyers–Ulam theory.

Let each vertex carry a finite-dimensional Hilbert space \(H_b\). Give every
edge a fixed linear contraction

\[
A_e:H_{s(e)}\to H_{t(e)}
\]

and an adjustable bias \(a_e\in H_{t(e)}\), defining

\[
R_e^a(x)=A_ex+a_e.
\]

These maps are total, nonexpansive, and can be genuinely noninvertible.
Assume the linear background is relation-exact:

\[
A_{p_\sigma}=A_{q_\sigma}
\quad\text{for all }\sigma.
\]

For a path \(p=e_n\cdots e_1\), its bias is

\[
B_p(a)=
a_{e_n}+A_{e_n}a_{e_{n-1}}+\cdots+
A_{e_n}\cdots A_{e_2}a_{e_1}.
\]

The **affine relation operator**

\[
D_A:\bigoplus_{e\in K_1}H_{t(e)}
\longrightarrow
\bigoplus_{\sigma\in K_2}H_{t(p_\sigma)}
\]

is

\[
(D_Aa)_\sigma=B_{p_\sigma}(a)-B_{q_\sigma}(a).
\]

Exact affine response is equivalent to \(D_Aa=0\).

### Proposition 7.1 (Hyers–Ulam affine rectification; imported)

With the declared Hilbert direct-sum norms, the closest exact affine bias is

\[
\bar a=(I-D_A^\dagger D_A)a,
\]

and

\[
\operatorname{dist}(a,\ker D_A)
\le\|D_A^\dagger\|\,\|D_Aa\|.
\]

The optimal constant is
\(1/\sigma_{\min}^+(D_A)\) when \(D_A\ne0\).

**Proof.** This is orthogonal projection onto the kernel of a finite
Hilbert-space operator. It is a direct instance of the known theorem that the
optimal Hyers–Ulam stability constant is the norm of the Moore–Penrose
inverse. \(\square\)

Under affine Hilbert-space gauges
\(\phi_b(x)=Q_bx+g_b\), with \(Q_b\) orthogonal,

\[
A'_e=Q_{t(e)}A_eQ_{s(e)}^{-1},\qquad
a'_e=Q_{t(e)}a_e+g_{t(e)}-A'_eg_{s(e)},
\]

and \(D_{A'}Q_E=Q_CD_A\) for block-orthogonal \(Q_E,Q_C\). Hence singular
values, residual norm, and rectification distance are gauge invariant within
this affine sector: the extra translation term is an \(A'\)-coboundary in
\(\ker D_{A'}\), and \(D_{A'}a'=Q_CD_Aa\). Constant responses are the case
\(A_e=0\); translations are the single-trivialization case \(A_e=I\).

The declared weighted norms are

\[
\|a\|_E^2=\sum_e w_1(e)\|a_e\|^2,\qquad
\|c\|_C^2=\sum_\sigma w_2(\sigma)\|c_\sigma\|^2.
\]

The relevant ordinary-Euclidean normalized operator is

\[
\widetilde D_A=W_C^{1/2}D_AW_E^{-1/2}.
\]

The resulting condition number belongs to the **weighted presentation**, not
to the quotient category alone. Splitting a duplicated cell's weight among
its copies preserves
\(\widetilde D_A^\ast\widetilde D_A\), removing the simplest duplication
artifact. General quantitative presentation comparison remains open.

### Proposition 7.2 (growth obstruction; baseline)

Let \(K_N\) have \(N+1\) parallel edges and adjacent equality relations. For
noninvertible constant maps \(\ast\mapsto i\varepsilon\), every local defect is
\(\varepsilon\), while the closest total exact constant response in uniform
edge distance is \(N\varepsilon/2\) away. The associated smallest positive
singular value is

\[
2\sin\!\left(\frac{\pi}{2(N+1)}\right).
\]

This is a changing-presentation Poincaré/conditioning example, not a
fixed-source Ulam-instability theorem.

## 8. Scale-calibrated order signature

Scaling exponents are meaningful only after intervention amplitude is part of
the model.

### Definition 8.1 (amplitude-calibrated cell germ)

A cell germ is a family \((\sigma_\tau,x_\tau)\) with physical intervention
amplitude \(\tau\downarrow0\). Amplitude may come from a base Riemannian norm,
a Hausdorff distance between feasible sets, or a declared engineering unit.
Admissible reparameterizations are cofinal increasing homeomorphisms
\(\tau'=\phi(\tau)\) satisfying \(c\tau\le\phi(\tau)\le C\tau\) near zero.

Fix reference units \(\Delta_0,\tau_0>0\). Let \(S\) be the cofinal set of
scales on which both routes succeed with finite value defect
\(\Delta(\tau)\). Define the lower response order

\[
\operatorname{ord}\Delta
=\liminf_{\substack{\tau\downarrow0\\ \tau\in S}}
\frac{\log(\Delta(\tau)/\Delta_0)}
{\log(\tau/\tau_0)},
\]

using \(\log0=-\infty\); thus eventual exact agreement has order \(+\infty\).
The failure-scale set
\[
\mathcal F=\{\tau:\text{exactly one route succeeds at scale }\tau\}
\]
is recorded separately, including whether zero is merely an accumulation
point or failure is eventual. If successful scales are not cofinal, no value
order is assigned.

### Proposition 8.2 (order calculus)

1. Response order is invariant under uniformly bi-Lipschitz fiber gauges and
   amplitude reparameterizations.
2. If a uniformly Lipschitz continuation is defined on both route outcomes
   for all sufficiently small \(\tau\in S\), it cannot decrease the response
   order when both orders use the same tail of \(S\).
3. Under the same common-scale hypothesis, a uniformly bi-Lipschitz
   continuation preserves the response order.

**Proof.** Multiplicative constants contribute bounded terms to logarithms,
which vanish after division by \(\log\tau\). The Lipschitz inequalities give
the second and third claims on the same scale set. A partial continuation
that deletes a cofinal subsequence can change a liminf. \(\square\)

For a fixed \(C^3\) smooth response connection in a common chart, with
uniformly bounded derivatives, \(x_\tau\to x_0\), and a nonzero limiting
curvature coefficient on the chosen directions, square cells have order
\(2\). The scaled
convex-projection example

\[
A_\tau=\{x\ge\tau\},\qquad
B_\tau=\{x+y\ge\tau\}
\]

has exact defect \(\tau/2\) and order \(1\). A discontinuous protocol whose
shrinking external cells cross a fixed jump and select target states distance
one apart has order \(0\). A family with order \(1\) or \(0\), or with
route-asymmetric failures accumulating at zero, cannot be represented to
leading order by one fixed uniformly regular smooth connection.

These are comparison reductions, not claims that curvature, projections, or
hybrid jumps are new.

## 9. Three native application tests

### 9.1 Configuration repair

Let a configuration be \(z=(x,y)\in\mathbb R_+^2\), and let
\(\lambda>0\). Two independently deployable policies are

\[
A:x\ge\lambda,\qquad B:x+y\ge2\lambda.
\]

Fibers are the cumulative feasible sets
\[
X_\varnothing=\mathbb R_+^2,\quad
X_A=A,\quad X_B=B,\quad X_{AB}=A\cap B,
\]
and edge carry responses are Euclidean projections onto target fibers. From
\(z_0=0\),

\[
\begin{aligned}
A\text{ then }B &:\
0\mapsto(\lambda,0)\mapsto
(3\lambda/2,\lambda/2),\\
B\text{ then }A &:\
0\mapsto(\lambda,\lambda)\mapsto
(\lambda,\lambda).
\end{aligned}
\]

The defect is \(\lambda/\sqrt2\). Resetting from the baseline gives
\((\lambda,\lambda)\) under either order.

The homogeneous model gives the closed-form \(\lambda=2\) extrapolation
\((3,1)\), \((2,2)\), and defect \(\sqrt2\). This is not an empirical
holdout. A prospective test could calibrate the metric and single-policy maps
at \(\lambda=1\), predeclare \(\lambda=2\), and use deviation to falsify the
Euclidean edit-cost, homogeneity, or carry-rule assumption.

### 9.2 Online allocation with hard failure

There are two unit servers. Flexible job \(A\) prefers server 1 but can use
either; rigid job \(B\) can use only server 1. Carry semantics is nonpreemptive
greedy allocation.

The external cell declares that both arrival orders have the same final demand
set. Starting empty:

\[
A\text{ then }B:
\quad\varnothing\mapsto(A\to1)\mapsto\text{failure},
\]

whereas

\[
B\text{ then }A:
\quad\varnothing\mapsto(B\to1)\mapsto
(B\to1,A\to2).
\]

Equip all fibers with unit discrete metrics and set
\[
\begin{aligned}
X_\varnothing&=\{\varnothing\},&
X_A&=\{A\to1,A\to2\},\\
X_B&=\{B\to1\},&
X_{AB}&=\{(B\to1,A\to2)\}.
\end{aligned}
\]
The elementary maps send
\(\varnothing\mapsto A\to1\),
\(\varnothing\mapsto B\to1\),
\(A\to2\mapsto(B\to1,A\to2)\) with \(A\to1\) outside the domain, and
\(B\to1\mapsto(B\to1,A\to2)\). These are partial nonexpansive maps. The
signature has route-asymmetric feasibility. A batch reset/migration solver
reaches \((B\to1,A\to2)\) from either history.

Preferences, compatibility, and nonpreemption are protocol assumptions here.
A prospective calibration would require forced-unavailability trials for
compatibility and sequential trials for nonpreemption, with the target pair
withheld. An explicit reservation policy placing \(A\) on server 2, or
migration of \(A\) when \(B\) arrives, makes both orders succeed.

### 9.3 A downstream guard that converts value debt to failure

Add to the configuration model a validation intervention \(C\) whose response
is the identity on the partial domain
\[
D_C=\{(x,y):y\ge3\lambda/4\}.
\]
The two \(AB\) prefixes are both feasible and differ by
\(\lambda/\sqrt2\). The \(A\)-then-\(B\) endpoint has \(y=\lambda/2\)
and fails \(C\), whereas the \(B\)-then-\(A\) endpoint has \(y=\lambda\)
and passes. Each endpoint is \(\lambda/4\) from the guard, which is no larger
than their mutual distance. Thus the imported guard lemma correctly
localizes the conversion. The guard is constructed here as a demonstration;
in a prospective test it must be declared before the two-path outcomes are
observed.

These mechanisms have extensive prior art in configuration repair, projection
methods, online matching, and economic path dependence. Their purpose here is
to show that one NCS signature transfers without changing definitions.

## 10. Smooth and stratified embeddings

Smooth horizontal transport and hybrid seam maps enter
\(\mathbf{pMetPar}_{\mathrm{Lip}}\) only on regions where finite Lipschitz
moduli are available. On a compact regular chart this is a local condition,
not a universal property of Ehresmann transport.

For regular equality constraints \(F(b,x)=0\), with
\(D_xF\) full row rank and smooth positive-definite internal metric \(M\),
the minimum internal velocity over base velocity \(u\) is the standard

\[
v^*(u)=
-M^{-1}A^\top(AM^{-1}A^\top)^{-1}Cu,
\quad A=D_xF,\ C=D_bF.
\]

Small two-order squares have vector defect
\(\tau^2\Omega(u,v)+O(\tau^3)\) after choosing a local trivialization and
back-transport convention. This is ordinary connection theory.

A stratified realization additionally requires explicit partial seam maps and
junction-order data. The stratification alone does not choose them. General
metric/noninvertible response admits subadditive comparisons and seam-margin
bounds, not a canonical additive curvature/seam/junction formula.

## 11. Checkpoint novelty ledger

| Item | Status |
|---|---|
| Path presentations, trace swaps | imported |
| Partial/Lipschitz response functor | synthesis/application object |
| Domain/value signature | useful reporting synthesis; standard after totalization |
| Filling bound | imported quantitative-rewriting baseline |
| Affine pseudoinverse rectification | imported Hyers–Ulam baseline |
| Guard-margin lemma and boundary-exposure bound | imported robustness baseline |
| Amplitude-calibrated response order | order-of-vanishing synthesis |
| Smooth curvature, projection, jump reductions | imported comparison sectors |
| Configuration and allocation predictions | application evidence |

The proposal now makes a narrow claim: NCS is a candidate field organized
around the **composition, failure conversion, scaling, and rectification of
stateful response protocols**, not a claim to have invented noncommutativity,
partial maps, confluence, curvature, or sequential repair.

Checkpoint 2 therefore passes only as a coherent synthesis framework. The
adversary's 9/14 verdict rejects it as a novelty-bearing mathematical
foundation. Advancement to Checkpoint 3 requires:

1. no novelty claim for the guard lemma or reporting decomposition;
2. verification that directional failure and the two-sided seam exposure are
   implemented correctly;
3. the affine-contractive construction and gauge covariance;
4. the prospective application tests and their stated falsifiers;
5. a useful open-problem agenda whose success criteria are stronger than
   repackaging.
