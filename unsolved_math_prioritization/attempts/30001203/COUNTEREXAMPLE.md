# Negative observability curvature does not imply global observability

**Problem 30001203 / OWR-3394-020. Complete counterexample; separate adversarial AI review passed.** This has not undergone human peer review; see [the review](review/REVIEW.md). One substantive construction family. The argument uses classical covering-space theory and Nash's smooth isometric embedding theorem. Historical priority is not established.

## 1. Exact source scope

Arthur J. Krener's contribution “Global Observability of Spaces of Negative Curvature,” in [OWR 11/2009, printed pages 674–675](https://ems.press/content/serial-article-files/46211), considers an autonomous observed system on an arbitrary smooth state manifold M:
\[
 \dot x=f(x),\qquad y=h(x)\in\mathbb R^p.
\]
Global observability on a fixed interval means injectivity of the map from the initial state to its entire output history. The question assumes a uniformly positive definite and bounded local observability Gramian and asks whether uniform negative curvature of that metric, together with geodesic completeness, ensures global observability.

The printed statement does not require M to be simply connected, does not restrict the output dimension p, and does not exclude the zero vector field. Its coordinates are explicitly local coordinates on a manifold, not a single global Euclidean chart. These points matter in the example below.

Uniform positive definiteness and boundedness are verified both relative to any fixed smooth background metric on the compact state manifold and, more concretely, by uniform matrix bounds in hyperbolic coordinate charts. No arbitrary rescaling of coordinates is assumed to preserve matrix eigenvalues.

The adjacent imported record 30001204 / OWR-3394-021 restates this same source question. It is a duplicate, not a second result.

## 2. Counterexample theorem

**Theorem.** There exist a connected compact smooth surface M, a smooth observation map \(h:M\to\mathbb R^{17}\), and a complete smooth vector field \(f=0\) such that, for \(T=1\):

1. the local observability Gramian is a smooth positive definite metric, uniformly bounded above and below;
2. its Gaussian and sectional curvature are identically \(-1\);
3. this metric is geodesically complete;
4. the system is locally observable at every state, but every output history comes from exactly two distinct initial states.

In particular, the proposed implication is false in its stated manifold scope.

### Construction

Let \((S,g)\) be a closed connected oriented hyperbolic surface of genus two, with curvature \(-1\). Such a surface can be obtained by identifying paired sides of a regular hyperbolic octagon with angle \(\pi/4\). The eight identified corner angles sum to \(2\pi\), and the paired geodesic sides have smooth hyperbolic neighborhoods, so the resulting metric has no cone singularities.

Choose a connected two-sheeted covering
\[
 \pi:M\longrightarrow S.
\]
For example, with the usual presentation
\[
 \pi_1(S)=
 \langle a_1,b_1,a_2,b_2\mid[a_1,b_1][a_2,b_2]=1\rangle,
\]
send \(a_1\) to the nonidentity element of \(\mathbb Z/2\) and the other generators to the identity. This defines a surjection, since its target is abelian and the relator maps to zero. The subgroup of index two given by its kernel determines a connected unramified double cover. The cover inherits the smooth structure of S. It is compact and has genus three, since
\[
 \chi(M)=2\chi(S)=-4.
\]
Equip M with the pullback metric
\[
 \widetilde g=\pi^*g.
\]

Nash's smooth isometric embedding theorem gives a smooth embedding
\[
 e:(S,g)\longrightarrow(\mathbb R^{17},\langle\cdot,\cdot\rangle),
 \qquad e^*\langle\cdot,\cdot\rangle=g.
\]
Here 17 is the bound \(n(3n+11)/2\) for \(n=2\) in Nash's compact theorem. Only existence of a finite-dimensional smooth isometric embedding is needed. This is the smooth theorem, not a merely \(C^1\) isometric embedding result.

Define
\[
 f\equiv0,\qquad h=e\circ\pi.
 \tag{1}
\]

### Exact Gramian computation

The state trajectory from x is constant for all real times. In every local state chart,
\[
 F(t)=Df(x)=0,\qquad \Phi(t)=I,\qquad H(t)=Dh(x).
\]
Consequently, for any fixed \(T>0\),
\[
 P_T(x)=\int_0^T \Phi(t)^TH(t)^TH(t)\Phi(t)\,dt
       =T\,Dh(x)^TDh(x).
 \tag{2}
\]
Intrinsically, for \(v,w\in T_xM\),
\[
\begin{aligned}
 P_T(x)(v,w)
 &=T\langle dh_xv,dh_xw\rangle\\
 &=Tg_{\pi(x)}(d\pi_xv,d\pi_xw)
  =T\widetilde g_x(v,w).
\end{aligned}
 \tag{3}
\]
Thus the Gramian at \(T=1\) is exactly the hyperbolic metric \(\widetilde g\).

This computation uses the actual observation map and the actual variational dynamics. It does not merely select an unrelated negatively curved metric on the state space.

### Uniform bounds

First, let q be any fixed smooth Riemannian background metric on M. The q-unit tangent bundle is compact, and the positive continuous function
\[
 (x,v)\longmapsto\widetilde g_x(v,v),\qquad q_x(v,v)=1,
\]
has a positive minimum and finite maximum. Therefore there are constants
\(0<c\le C<\infty\) with
\[
 cq\le P_1=\widetilde g\le Cq
 \tag{4}
\]
on all of M. The background metric need not be chosen equal to the Gramian.

The local-coordinate bounds can also be exhibited explicitly. Cover the compact hyperbolic surface M by finitely many isometric hyperbolic disk charts centered at their chart origins and restricted to Euclidean radius at most \(1/2\) in the Poincaré disk model. In every such chart \(z=(u,v)\),
\[
 P_1(z)=\frac{4}{(1-u^2-v^2)^2}I_2.
\]
Hence throughout every chart,
\[
 4I_2\le P_1(z)\le\frac{64}{9}I_2.
 \tag{5}
\]
Each point has a sufficiently small hyperbolic chart; restricting each to the indicated radius preserves a neighborhood of its center, and compactness supplies a finite subcover. A common injectivity-radius estimate is not required for these coefficient bounds.

A demand for the same constants in every possible reparametrization would not be a meaningful coordinate-invariant hypothesis, even for the Euclidean metric. Equations (4) and (5) verify the usual intrinsic and fixed-atlas meanings of the source's uniform bounds.

### Curvature, completeness and local observability

The covering projection is a local isometry for \(\widetilde g\), so its Gaussian curvature is \(-1\). On a surface this is also the sectional curvature. Completeness follows from compactness of the smooth Riemannian manifold. Equivalently, the compact base is complete and its Riemannian covering is complete.

The map \(\pi\) is a local diffeomorphism and e is an embedding, so h is locally injective and its differential has rank two everywhere. Because output histories are constant functions with value h(x), the system is locally observable on every interval of positive length.

### Failure of global observability

For any s in S, write its two distinct lifts as \(x_+\ne x_-\). Then
\[
 h(x_+)=e(s)=h(x_-).
\]
Since the dynamics is zero, their full output histories agree for all times:
\[
 y_{x_+}(t)=e(s)=y_{x_-}(t)\qquad(t\in\mathbb R).
 \tag{6}
\]
Moreover, e is injective, so equality of output values is equivalent to equality of their projections under \(\pi\). Each output history therefore has precisely two possible initial states. No increase of the observation interval distinguishes them. This proves the theorem. \(\square\)

## 3. Why intrinsic curvature misses this obstruction

For zero dynamics, the observation-history map is simply the observation map repeated over time, and its Gramian records the pullback Euclidean metric. A local isometry to a measured base space can preserve that metric while identifying distinct covering sheets.

Negative curvature controls intrinsic local and geodesic geometry. It does not force an isometric immersion into an observation space to be globally injective. Completeness of the source does not change this distinction. The construction makes the observational ambiguity a finite covering ambiguity while keeping the induced metric genuinely negatively curved.

There is no conflict with the obstruction to a complete smooth surface of curvature \(-1\) in three-dimensional Euclidean space: the output dimension here is 17. Nash's higher-codimension embedding theorem is the appropriate input.

For the same system at any other fixed \(T>0\), equation (3) gives the complete metric \(T\widetilde g\) with constant curvature \(-1/T\), and the indistinguishable states remain indistinguishable. The construction is not confined to a single exceptional time.

## 4. Dependencies, validation and limits

The external mathematical inputs are classical:
- existence of a closed hyperbolic genus-two surface;
- realization of an index-two subgroup by a connected smooth covering;
- Nash's smooth compact isometric embedding theorem;
- compact Riemannian manifolds are geodesically complete.

Nash's original **Theorem 2 on printed page 59** was checked directly in the [1956 paper](https://sites.math.rutgers.edu/~feehan/teaching/math866/nash.pdf). The theorem includes smooth metrics and smooth embeddings and gives the dimension used above. The source theorem is imported; this package does not reprove Nash's iteration.

The modest checker verifies the local curvature formula, its scaling with T, the uniform Poincaré-chart bounds, the double-cover monodromy relation and elementary Gramian identities. It does not numerically construct a Nash embedding or infer a geometric theorem from finite tests.

The original source has been read in full for this contribution, including its definition of global observability and the entire curvature conjecture. The cited Krener–Ide paper uses the same local Gramian and separates local distinguishability from global injectivity. Bounded current-source searches located no earlier explicit resolution of this conjecture; this does not establish historical novelty.

The counterexample settles the literal manifold formulation. It makes no claim about separately strengthened questions with additional hypotheses absent from that formulation.
