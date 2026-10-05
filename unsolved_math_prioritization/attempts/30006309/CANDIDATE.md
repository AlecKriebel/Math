# A combinatorial comparison of the discriminant and Hurwitz-vector polytopes

**Candidate for the smooth polarized toric regime of the cited theorem; independent review pending.** The equality of the geometric weight polytopes is already known. The proposed contribution here is a direct comparison of their two explicit polytopal models, using products of faces, normalized simplex volumes, a finite-difference identity, and the standard GKZ normal-fan theorem. No K-energy formula or Cayley identity is used to prove that comparison. Historical novelty is unestablished.

## 1. Source scope and what is proved

Sano's talk in [OWR19/2025, pp.919–921](https://ems.press/content/serial-article-files/51856) asks for a combinatorial reproof of the coincidence between the discriminant and Hurwitz weight polytopes. Its preceding theorem gives the Hurwitz-vector model. The cited full paper, [Sano, Theorem1.4](https://arxiv.org/abs/2302.09801), assumes a smooth polarized toric variety embedded by its complete very ample linear system, with degree at least two. We retain those assumptions. The short report abbreviates the boundary/massive-face convention and does not repeat all of those hypotheses; it is not a license to claim the unweighted formulas for arbitrary singular configurations.

Let Q be the n-dimensional lattice polytope of that polarization, with n≥1, and let \(A=Q\cap\mathbb Z^n\). Thus Q is Delzant and the face lattices have the full induced lattice normalization. Let

\[
B=A\times\operatorname{Vert}(\Delta_{n-1}),\qquad
P=Q\times\Delta_{n-1},\qquad d=2n-1,
\]

where \(\Delta_{n-1}=\operatorname{conv}(0,e_1,\ldots,e_{n-1})\) is the standard lattice simplex. Write

\[
\pi:\mathbb R^B\longrightarrow\mathbb R^A,
\qquad \pi(z)_a=\sum_{v\in\operatorname{Vert}(\Delta_{n-1})}z_{(a,v)}.
\tag{1}
\]

This is the weight projection for the torus acting on the first Segre factor and trivially on the second; it is not the full coefficient torus on B.

For a triangulation T of (Q,A), let \(\eta_{T,j}\in\mathbb Z^A\) have coordinate at a equal to the sum of the normalized j-volumes of all j-simplices of T that contain a as a vertex and lie in a j-face of Q. Such simplices are called **massive**. Every top-dimensional simplex is massive. In dimension n−1, only boundary simplices count. The zero-dimensional volume is one.

For a triangulation U of (P,B), use the same convention and put

\[
m_U=\sum_{k=0}^{d}(-1)^{d-k}\eta_{U,k}.
\tag{2}
\]

Define the two combinatorial polytopes

\[
\mathcal D(P)=\operatorname{conv}\{m_U:U\text{ regular}\},
\quad
\mathcal H(Q)=\operatorname{conv}\{n\eta_{T,n}-\eta_{T,n-1}:T\text{ regular}\}.
\tag{3}
\]

**Theorem.** Under the hypotheses above,

\[
\boxed{\quad \pi\mathcal D(P)=\mathcal H(Q).\quad}
\tag{4}
\]

The proof below is a polyhedral/combinatorial comparison of these two defined polytopes. The standard GKZ identification gives \(\mathcal D(P)=\operatorname{Newt}(\Delta_{X\times\mathbb P^{n-1}})\); the right side is the Hurwitz-vector model in the source. Thus (4) supplies the requested comparison of the two known weight-polytope descriptions in the cited smooth regime. It is not a new assertion of the already-known geometric equality, nor a reproof of every foundational GKZ theorem.

## 2. The precise established GKZ input

We use the following standard property, including the alignment of vertices with height vectors, not only a list of vertices.

**GKZ height compatibility.** For a smooth toric configuration C with polytope R, its discriminant Newton polytope has vertices
\(m_V=\sum_j(-1)^{\dim R-j}\eta_{V,j}\), indexed by the D-equivalence classes of regular triangulations V. If a generic height h induces V by its lower convex hull, then m_V minimizes the functional \(z\mapsto\langle h,z\rangle\) on that polytope. If h lies on a wall, a regular triangulation induced by a sufficiently small generic perturbation of h labels a vertex in the minimizing face for h.

This is the combination of [GKZ, Chapter11, Theorem3.2 and Theorem3.4(a), pp.361–363](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/gelkapzel.pdf), with the secondary-polytope height convention in Chapter7 and the initial-monomial formula of Chapter10, Theorem1.4. Chapter11 states its theorem for the regular A-determinant; the same chapter explicitly identifies that determinant with the ordinary discriminant when the toric variety is smooth. The product X×P^(n−1) is smooth, so the distinction causes no extra factor here.

For clarity about the minimizer label: the Newton polytope of the principal determinant is the secondary polytope. Its normal fan refines the discriminant normal fan, since the latter polytope is a Minkowski summand. The initial-monomial formulas identify the corresponding discriminant vertex with m_V. Lower-hull heights use minima; the opposite upper-hull convention uses negatives and maxima. Passing a perturbation to zero preserves the weak minimizing inequalities.

The new comparison does not invoke the equality (4) to establish this input. It is the general discriminant/secondary-polytope theorem already available before the Hurwitz-vector conjecture. The proof below does not use the analytic theorem of Sano as an inequality, support-function identity, or cone-refinement input. That theorem is cited only to identify the name of the source's right-hand model.

## 3. Product refinements and the projected massive vectors

Fix any triangulation T of (Q,A). Suppose U triangulates P using B and refines the subdivision with cells

\[
\sigma\times\Delta_{n-1},\qquad \sigma\in T,
\tag{5}
\]

using only products of vertices of T with simplex vertices. For example, this is true of the small generic regular refinements constructed in Section5. Regularity is not needed for the following vector computation.

**Product-face identity.** For \(0\le k\le2n-1\),

\[
\boxed{\quad
\pi\eta_{U,k}
=\sum_{\substack{0\le j\le n,\;0\le l\le n-1\\j+l=k}}
\binom n{l+1}\binom{k+1}{j+1}\eta_{T,j}.
\quad}
\tag{6}
\]

Here is a complete verification, including the lattice factors.

Every k-face of P is uniquely F×E, where F is a j-face of Q and E is an l-face of the standard simplex, with j+l=k. There are \(\binom n{l+1}\) choices of E. The induced affine lattice is a product lattice. Its normalized volume satisfies

\[
\operatorname{Vol}_{\mathbb Z}(\sigma\times E)
=\binom{j+l}{j}\operatorname{Vol}_{\mathbb Z}(\sigma)
\tag{7}
\]

for a j-simplex σ, since E has normalized volume one.

Let a be a vertex of σ, and let \(\lambda_a\) be its barycentric coordinate on σ, extended constantly in the E direction. On any k-simplex τ in a triangulation of σ×E, λ_a is affine and at each vertex equals one or zero according to whether that vertex projects to a. The centroid identity for a simplex therefore gives

\[
\sum_{\tau}\operatorname{Vol}_{\mathbb Z}(\tau)
\#\{\text{vertices of }\tau\text{ projecting to }a\}
=\frac{k+1}{j+1}\operatorname{Vol}_{\mathbb Z}(\sigma\times E)
=\binom{k+1}{j+1}\operatorname{Vol}_{\mathbb Z}(\sigma).
\tag{8}
\]

The middle equality uses that the average barycentric coordinate over a simplex is 1/(j+1), which remains so after taking a product. This identity can be read entirely as additivity of volume-weighted centroids of finite subdivisions; no analytic energy or limiting measure formula is involved. It is valid for every triangulation of the product with the specified vertices, not just a staircase triangulation.

Now restrict U to F×E. It refines the products of the top-dimensional simplices in T restricted to F with E. Sum (8) over those simplices. Shared lower-dimensional boundaries contribute no top-dimensional volume. Then sum over all F and all E. Massive k-simplices lie in unique k-faces of P, so no simplex is counted twice. This is exactly (6), coordinate by coordinate. Points of A unused by T also have zero contribution on both sides, by the vertex restriction in (5).

## 4. A finite-difference cancellation

Substitute (6) into (2). The coefficient of \(\eta_{T,j}\) in \(\pi m_U\) is

\[
c_{n,j}=
\sum_{l=0}^{n-1}(-1)^{2n-1-j-l}
\binom n{l+1}\binom{j+l+1}{j+1}.
\tag{9}
\]

Set r=l+1 and add the zero term r=0. If \(f_j(r)=\binom{j+r}{j+1}\), then

\[
c_{n,j}=(-1)^{n-j}
\sum_{r=0}^n(-1)^{n-r}\binom nr f_j(r)
=(-1)^{n-j}\Delta^n f_j(0).
\tag{10}
\]

Pascal's identity gives \(\Delta\binom{j+r}{q}=\binom{j+r}{q-1}\). Consequently,

\[
c_{n,j}=
\begin{cases}
0,&0\le j\le n-2,\\
-1,&j=n-1,\\
n,&j=n.
\end{cases}
\tag{11}
\]

When the difference order exceeds the polynomial degree, the result is zero; this also covers n=1 with its empty first range. Thus every product-refining U satisfies the **vector identity**

\[
\boxed{\quad\pi m_U=n\eta_{T,n}-\eta_{T,n-1}.\quad}
\tag{12}
\]

For n=2 this specializes to the vertical-prism identity already proved by Ogusu–Sano, Proposition3.5. The argument above proves it uniformly in dimension and is independent of the choice of refinement. That surface special case is prior work, not a discovery claimed here.

## 5. Regular refinements at equal-column heights

Let w be a generic height on A inducing the regular triangulation T. Put

\[
\widehat w(a,v)=w(a)\qquad((a,v)\in B).
\tag{13}
\]

The regular subdivision induced on P by \(\widehat w\) is precisely the product subdivision (5). Indeed, its lower convex envelope is \(g_w(x)\), independent of the simplex coordinate y. For any convex representation of (x,y), the sum of its heights is at least g_w(x). Conversely, if \(x=\sum_a\alpha_a a\) realizes g_w(x) and \(y=\sum_v\beta_v v\), the coefficients \(\alpha_a\beta_v\) realize (x,y) with exactly that height. On each lower simplex of T this yields the whole product cell.

A sufficiently small generic perturbation

\[
\widehat w+\varepsilon q,\qquad \varepsilon>0,
\tag{14}
\]

gives a regular triangulation U refining those cells. This is the standard regular-refinement property and also follows from the finite strict inequalities for supporting faces: preserve all nonzero old inequalities and choose q outside the finitely many circuit hyperplanes that remain tied. Fix q and take ε sufficiently small; the signs are then constant, so U can be held fixed as ε tends to zero. Points strictly above the old lower hull remain above it, hence the vertices of U are products of vertices of T and simplex vertices, as required in Section3.

By GKZ height compatibility, m_U minimizes \(\widehat w+\varepsilon q\) on \(\mathcal D(P)\). Letting ε decrease to zero shows it minimizes \(\widehat w\). Using (1) and (12),

\[
\min_{z\in\pi\mathcal D(P)}\langle w,z\rangle
=\langle w,\pi m_U\rangle
=\langle w,n\eta_{T,n}-\eta_{T,n-1}\rangle.
\tag{15}
\]

This is the missing reverse-direction mechanism: an arbitrary triangulation of P need not project to a vertex, and no claim that it does has been used. For each testing functional on the smaller coordinate space, an exposed vertex can instead be selected through an equal-column height and its product refinement.

## 6. Both polytope inclusions

For every regular T, Section5 supplies a regular product-refining U. Its massive vector belongs to \(\mathcal D(P)\), and (12) gives its projection. Therefore

\[
\mathcal H(Q)\subseteq\pi\mathcal D(P).
\tag{16}
\]

For every generic w, (15) attains the minimum over the larger polytope at a point of \(\mathcal H(Q)\). The two minima are therefore equal. Generic heights inducing regular triangulations are dense: their complement is contained in finitely many circuit hyperplanes. The minimum of a linear functional over a fixed compact polytope is continuous in that functional. Thus the two minima agree for every w. A closed convex polytope is determined by these minima, so (16) is an equality. This proves (4).

No enumeration of all regular triangulations of the higher-dimensional product is needed. In particular, non-product triangulations and their possibly nonextreme projections are handled by support functions rather than incorrectly assumed absent.

## 7. Scope, dependence and verification boundary

The proof's combinatorial mechanism consists of the exact product-face identity (6), the finite binomial cancellation (11), regular refinements at equal-column heights, and convex separation. It uses the general GKZ combinatorial description and normal-fan map as established inputs. It neither invokes K-energy nor reasons that the desired polytopes are equal merely because the two defining polynomials coincide. It is a combinatorial comparison within the GKZ framework, not an attempt to replace the full algebraic foundations of that framework.

Smoothness matters in identifying the regular determinant with the discriminant. The report's abbreviated wording must not be used to extend this unweighted formula to arbitrary singular X_A, sparse configurations with lattice-index defects, or incomplete embeddings. Those extensions are outside this candidate. Degree-one/dual-defective cases would require conventions for a constant discriminant; they are not asserted as part of the geometric source conclusion.

The exact checker tests the finite-difference identity, volume factors and projected massive vectors on explicit low-dimensional product triangulations, including nonunimodular cells and unused lattice points. These tests do not establish the infinite family of configurations or the GKZ normal-fan input; those are covered by the written proof and cited source theorem. No historical novelty claim is made. A separate review must assess both the mathematical argument and its match to the requested combinatorial proof mechanism before any resolution claim.
