# A rank-four vector five-coloring for every diameter subgraph

**Checkpoint:** 2026-08-01

**Status:** exact necessary condition and graph-first screening theorem; this
does not yet give an ordinary five-coloring.

No literature search or external construction catalogue was used.

## 1. Result

Normalize a finite point set in \(\mathbb R^4\) to diameter one. A graph
\(G\) is a *diameter subgraph* when every edge of \(G\) joins points at
distance one; other pairs are allowed to be accidental diameter pairs.

> **Center-vector theorem.** If \(G\) is a diameter subgraph of a finite set
> in \(\mathbb R^4\), there are unit vectors \(n_v\in S^3\), one for every
> vertex, such that
> \[
>       \langle n_u,n_v\rangle\le -\frac14
>       \qquad(uv\in E(G)).                         \tag{1}
> \]

Thus the Gram matrix \(X=(\langle n_u,n_v\rangle)\) is positive
semidefinite, has diagonal one and rank at most four, and has entries at most
\(-1/4\) on all prescribed edges. In graph terminology this is a rank-four
vector five-coloring. It is only a relaxation of an ordinary coloring:
(1) by itself does not partition the original points.

The theorem remains valid for a non-induced diameter subgraph, so it is a
cheap necessary condition before any coordinate or Gram-rank search.

## 2. A sharp cap lemma for diameter-neighbor directions

We first prove the exact local statement.

> **Lemma.** Let \(A\subset S^3\) be a nonempty finite set satisfying
> \[
>       \langle a,b\rangle\ge\frac12
>       \qquad(a,b\in A).                            \tag{2}
> \]
> There is a unit vector \(n\) such that
> \[
>       \langle n,a\rangle\ge\sqrt{\frac58}
>       \qquad(a\in A).                              \tag{3}
> \]

### Proof

Let \(B(c,\rho)\) be the Euclidean minimum enclosing ball of \(A\), and let
\(T\) be the points on its boundary. Minimum-ball optimality gives
\(c\in\operatorname{conv}T\): otherwise a strict separating direction lets
one move the center slightly toward \(\operatorname{conv}T\), decreasing
all active distances while the finitely many inactive inequalities retain
their slack.

Every convex combination of points satisfying (2) is nonzero. Indeed, if
\(z=\sum_i\lambda_i a_i\), then
\[
 \lVert z\rVert^2
 \ge \sum_i\lambda_i^2+rac12\sum_{i\ne j}\lambda_i\lambda_j
 =\frac12+\frac12\sum_i\lambda_i^2>0.                \tag{4}
\]
In particular \(c\ne0\).

For every active point \(a\in T\), expansion of
\(\lVert a-c\rVert^2=\rho^2\) and \(\lVert a\rVert=1\) shows that
\[
       \langle a,c\rangle
       =\frac{1+\lVert c\rVert^2-\rho^2}{2}.          \tag{5}
\]
Hence \(T\) lies in an affine hyperplane of dimension at most three. By
Caratheodory in that hyperplane, write
\[
       c=\sum_{i=1}^m\lambda_i a_i,
       \qquad a_i\in T,\quad \lambda_i>0,\quad
       \sum_i\lambda_i=1,\quad m\le4.                \tag{6}
\]
Taking the inner product of (6) with \(c\) shows that the common value in
(5) is \(\lVert c\rVert^2\). Applying (4) and Cauchy--Schwarz to (6) gives
\[
       \lVert c\rVert^2
       \ge\frac12+\frac12\sum_i\lambda_i^2
       \ge\frac12+\frac1{2m}
       \ge\frac58.                                   \tag{7}
\]

For an arbitrary \(a\in A\), ball containment and (5) give
\[
 \lVert a-c\rVert^2\le\rho^2
 \quad\Longrightarrow\quad
 \langle a,c\rangle\ge\lVert c\rVert^2.             \tag{8}
\]
Therefore \(n=c/\lVert c\rVert\) satisfies
\(\langle n,a\rangle\ge\lVert c\rVert\ge\sqrt{5/8}\),
as claimed. \(\square\)

The constant is sharp. Four unit vectors with every off-diagonal inner
product \(1/2\) have normalized sum \(n\) satisfying
\(\langle n,a_i\rangle^2=5/8\).

## 3. Proof of the center-vector theorem

For a nonisolated graph vertex \(v\), let
\[
 A_v=\{p_u-p_v:uv\in E(G)\}.
\]
Every member has norm one. If \(a=p_u-p_v\) and \(b=p_w-p_v\), then
\[
 \lVert a-b\rVert=\lVert p_u-p_w\rVert\le1,
\]
so \(\langle a,b\rangle\ge1/2\). Apply the cap lemma and call its unit cap
center \(n_v\). At an isolated vertex choose \(n_v\) arbitrarily.

Fix an edge \(uv\) and put \(e=p_v-p_u\). The two cap inequalities give
\[
       \langle n_u,e\rangle\ge\alpha,
       \qquad
       \langle n_v,e\rangle\le-\alpha,
       \qquad \alpha=\sqrt{\frac58}.                 \tag{9}
\]
Write the two unit vectors as axial and transverse components relative to
\(e\). If their axial magnitudes are \(s,t\ge\alpha\), Cauchy--Schwarz on
the transverse components yields
\[
 \begin{aligned}
 \langle n_u,n_v\rangle
 &\le-st+\sqrt{1-s^2}\sqrt{1-t^2}\\
 &\le-\alpha^2+(1-\alpha^2)
 =-\frac14.                                          \tag{10}
 \end{aligned}
\]
For the second inequality, put \(s=\cos\theta\), \(t=\cos\phi\) with
\(0\le\theta,\phi\le\arccos\alpha\); the first line is
\(-\cos(\theta+\phi)\), which is maximized at the two upper endpoints.
This proves (1).

All inequalities are intentionally non-strict. Equality occurs for the
regular-tetrahedral cap, so this theorem cannot by itself supply the uniform
gap needed for compact infinite sets.

The same proof in \(\mathbb R^d\) has active support size at most \(d\), so
\[
 \lVert c\rVert^2\ge\frac{d+1}{2d}
 \quad\text{and}\quad
 \langle n_u,n_v\rangle\le-\frac1d.                  \tag{11}
\]
Thus every finite diameter subgraph in dimension \(d\) has a rank-\(d\)
vector \((d+1)\)-coloring. The point of the four-dimensional version is not
that the relaxation is an ordinary coloring, but that it sharply constrains
which six-chromatic graph families deserve a realization search.

## 4. Exact spectral obstruction

Let \(G\) be a \(k\)-regular graph on \(N\) vertices, with adjacency matrix
\(A\) and least eigenvalue \(\tau\). If \(G\) is a diameter subgraph in
\(\mathbb R^4\), let \(X\) be the Gram matrix from (1). Since
\(A-\tau I\) and \(X\) are positive semidefinite,
\[
       \operatorname{tr}(AX)\ge \tau\operatorname{tr}X=\tau N. \tag{12}
\]
On the other hand, summing (1) over the \(Nk\) ordered edge incidences gives
\[
       \operatorname{tr}(AX)\le-\frac{Nk}{4}.         \tag{13}
\]
Consequently every regular diameter subgraph in \(\mathbb R^4\) must obey
\[
       \boxed{k\le-4\tau}.                            \tag{14}
\]

This is an exact, embedding-independent rejection test. More generally one
may use any nonnegative edge-supported symmetric weight matrix whose least
eigenvalue and constant row sum are known exactly.

## 5. Application to the unsigned golden graph

The previously derived unsigned golden relation graph has 60 vertices and
exact adjacency spectrum
\[
       \{20^1,5^{16},0^{18},(-4)^{25}\}.
\]
It is therefore 20-regular with \(\tau=-4\). Condition (14) would require
\(20\le16\), a contradiction. Thus this abstract six-chromatic graph cannot
occur even as a diameter subgraph of any point set in \(\mathbb R^4\),
regardless of coordinates, switchings, or accidental extra diameter edges.

This explains conceptually why the tempting 60-line construction could not
be oriented into a counterexample. The earlier explicit five-coloring of its
120-vertex signed cover remains a stronger family-specific certificate, but
is no longer the only obstruction.

## 6. Consequence for future graph-first searches

Any finite counterexample graph must simultaneously satisfy
\[
       \chi(G)\ge6
       \quad\text{and}\quad
       \exists X\succeq0:\ X_{vv}=1,\quad
       \operatorname{rank}X\le4,\ X_{uv}\le-1/4
       \text{ on edges}.                              \tag{15}
\]
Thus high-chromatic graphs whose vector relaxation already exceeds five can
be discarded before solving the much harder Euclidean diameter-realization
equalities and nonedge inequalities.

The companion checker verifies the sharp rational constants and replays the
exact golden-graph spectral application:

```text
python3 borsuk_dimension4/verification/verify_vector_five_bound.py
```
