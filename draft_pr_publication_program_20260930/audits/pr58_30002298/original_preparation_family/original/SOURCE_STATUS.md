# Fantappiè denominator vertices: a published geometric characterization

**The requested characterization follows from Akopyan–Bárány–Robins, published in 2017.** Their Definition 1 and Remark 10 identify denominator vertices with algebraic vertices, defined by a local condition on tangent cones. This note supplies the explicit pole argument and the origin convention needed to match the exact 2013 question. It claims no new discovery. Separate adversarial source and mathematical review passed; see [the report](review/REVIEW.md).

## 1. Exact source and denominator convention

The target is Question 1 on printed p.638 of Dmitrii Pasechnik's contribution to [Oberwolfach Report 11/2013](https://ems.press/content/serial-article-files/46446), pp.637–640. The measure has **unit Lebesgue density**, and the normalized transform is
$$
F_P(u)=d!\int_P(1-\langle x,u\rangle)^{-d-1}\,dx.
\tag{1}
$$
Here $P\subset\mathbb R^d$ is compact and is a finite union of convex polytopes. The source defines $V(P)$ as the intersection of the vertex sets of its triangulations. We retain this definition, rather than substituting the vertices of the convex hull or those of one chosen triangulation.

Write $F_P=N_P/\Omega_P$ in lowest terms and normalize $\Omega_P(0)=1$. The transform is analytic near zero, so this normalization is available. For $F_P=0$, take $\Omega_P=1$. The question is when
$$
\Omega_P(u)=\prod_{v\in V(P)}(1-\langle v,u\rangle).
\tag{2}
$$
The reduced-denominator interpretation is essential: the source's explicit cancellation example would make no sense if arbitrary unreduced presentations were permitted.

All indicator-function and tangent-cone identities below hold up to sets of ambient Lebesgue measure zero. Thus lower-dimensional pieces carry no mass; no atomic or surface measure is being substituted. The argument concerns $d\geq1$; the zero-dimensional case has constant denominator and is immediate.

## 2. The geometric criterion and its prior source

Translate the tangent cone of $P$ at $v$ to the origin and call it $C_v(P)$. A **line-cone** is a polyhedral cone, possibly a finite union of convex cones, invariant under translation in some nonzero direction, equivalently a union of parallel lines. Different line-cones in a sum may have different invariant directions.

Let $A(P)$ consist of those points $v$ for which there is **no** representation
$$
\mathbf1_{C_v(P)}=\sum_{j=1}^{m}c_j\mathbf1_{D_j}
\quad\text{almost everywhere},
\tag{3}
$$
where $m$ is finite, $c_j\in\mathbb R$, and the $D_j$ are line-cones. These are the algebraic vertices of Akopyan–Bárány–Robins.

The exact answer is:
$$
\boxed{\quad
\text{Equation (2) holds if and only if every }
v\in V(P)\setminus\{0\}\text{ belongs to }A(P).
\quad}
\tag{4}
$$
More precisely, the entire reduced denominator is
$$
\boxed{\qquad
\Omega_P(u)=\prod_{v\in A(P)\setminus\{0\}}(1-\langle v,u\rangle).
\qquad}
\tag{5}
$$
Every factor in this product has multiplicity one. No general-position, convexity, connectedness, or vertex-only triangulation hypothesis is required.

The published source is Arseniy Akopyan, Imre Bárány and Sinai Robins, **“Algebraic vertices of non-convex polyhedra,” Advances in Mathematics 308 (2017), 627–644**, DOI [10.1016/j.aim.2016.12.026](https://doi.org/10.1016/j.aim.2016.12.026). The complete [author manuscript, arXiv:1508.07594v2](https://arxiv.org/pdf/1508.07594v2), was inspected. Definition 1 introduces (3); Lemma 6 characterizes the kernel of the cone Fourier–Laplace valuation; Theorem 1 gives minimality under signed simplex decompositions; and Remark 10 explicitly identifies the Fantappiè denominator vertices with these algebraic vertices.

The source's phrase “geometric characterization” is therefore realized by the local line-cone condition. It is not enough to require that the tangent cone itself fail to be a line-cone, nor can signed linear combinations in (3) be replaced by disjoint unions.

## 3. Why the published criterion gives the exact reduced denominator

The following details explain (5), including cancellation and multiplicities, without asserting additional novelty.

Choose any finite triangulation, and use its full-dimensional simplices to represent $\mathbf1_P$ almost everywhere. Let $W$ be its vertex set. For a $d$-simplex $\Delta$,
$$
F_\Delta(u)=\frac{d!\operatorname{Vol}(\Delta)}
                 {\prod_{w\in\operatorname{Vert}(\Delta)}(1-\langle w,u\rangle)}.
\tag{6}
$$
Consequently $\Omega_P$ divides the squarefree product over $W\setminus\{0\}$. This already excludes higher multiplicities and any additional factors.

For $w\in W$, define the rational homogeneous function
$$
c_w(u)=(-1)^d
\sum_{\substack{\Delta\\w\in\operatorname{Vert}(\Delta)}}
\frac{d!\operatorname{Vol}(\Delta)}
{\prod_{z\in\operatorname{Vert}(\Delta)\setminus\{w\}}\langle z-w,u\rangle}.
\tag{7}
$$
It has degree $-d$. The simplex partial-fraction identity gives
$$
F_P(u)=\sum_{w\in W}\frac{c_w(u)}{1-\langle w,u\rangle}.
\tag{8}
$$
For example, (6) and the identity used in (8) appear as Corollary 3 and Theorem 2, equation (1.9), of [Gravin–Pasechnik–Shapiro–Shapiro](https://arxiv.org/pdf/1210.3193v2). Applying that identity to each simplex requires no simplicity assumption on $P$.

The coefficient $c_w$ is the Fourier–Laplace valuation of $C_w(P)$, using the convention with kernel $e^{\langle u,x\rangle}$. A simplicial cone with generators $q_1,\ldots,q_d$ has valuation
$$
(-1)^d\frac{|\det(q_1,\ldots,q_d)|}
               {\prod_i\langle q_i,u\rangle}.
$$
Contributions from simplices containing $w$ on a positive-dimensional face are line-cones and have zero valuation. Thus (7) indeed describes the local tangent cone, independently of the chosen triangulation. By Akopyan–Bárány–Robins, Lemma 6,
$$
c_w\ne0\quad\Longleftrightarrow\quad w\in A(P).
\tag{9}
$$

Fix a nonzero $v\in W$ and set $L_v=1-\langle v,u\rangle$. The affine hyperplane $L_v=0$ differs from all $L_w=0$ for $w\ne v$ and from every homogeneous edge-denominator hyperplane in (7). At a generic point of it, multiplying (8) by $L_v$ and restricting gives precisely $c_v|_{L_v=0}$. Hence $L_v$ occurs in the reduced denominator if and only if this restriction is not identically zero.

Homogeneity makes the last condition equivalent to $c_v\ne0$. Indeed, if $c_v$ vanished on $\langle v,u\rangle=1$, scaling $u$ by $1/\langle v,u\rangle$ would make it vanish on a nonempty open set, and hence as a rational function. There is no hidden cancellation between the distinct affine vertex factors. Equations (9) and the squarefree divisibility prove (5).

Finally, $A(P)\subseteq V(P)$. If an algebraic vertex were absent from some triangulation's vertex set, the tangent cone of every simplex at that point would be either empty or a line-cone. Summing those tangent indicators would contradict (3). This argument works directly with the triangulations in the source and does not require identifying different conventions for non-face-to-face dissections. Comparing the distinct normalized factors in (2) and (5) proves (4).

## 4. A finite local geometric version

The line-cone condition can be checked without computing a rational transform. This is the cone-flipping argument in the proof of Lemma 6 of Akopyan–Bárány–Robins.

Partition $C_v(P)$, up to null boundaries, into internally disjoint full-dimensional simplicial cones $K_i=\operatorname{pos}(q_{i1},\ldots,q_{id})$. Choose a vector $\eta$ having nonzero scalar product with every generator. Replace each generator by
$$
q_{ij}^{+}=\operatorname{sign}\langle\eta,q_{ij}\rangle\,q_{ij},
\qquad
\varepsilon_i=\prod_j\operatorname{sign}\langle\eta,q_{ij}\rangle,
$$
and put $K_i^+=\operatorname{pos}(q_{i1}^+,\ldots,q_{id}^+)$. The criterion is
$$
v\in A(P)\quad\Longleftrightarrow\quad
\sum_i\varepsilon_i\mathbf1_{K_i^+}\ne0
\quad\text{on a set of positive measure}.
\tag{10}
$$
Equivalently, after overlaying the finitely many facet hyperplanes, some full-dimensional chamber has nonzero signed coverage count.

Flipping one generator changes a cone indicator, modulo line-cones, by a minus sign. All flipped cones lie in the common pointed cone generated by their finitely many generators; away from its apex this cone is contained in $\langle\eta,x\rangle>0$. On such cones the Fourier–Laplace transform is injective on signed indicator functions; equivalently, Lemma 5 followed by the overlay decomposition in Lemma 6 gives this injectivity. Thus the flipped signed function is zero exactly when the original cone is a signed sum of line-cones. The outcome is independent of the chosen triangulation and generic vector.

This is a local geometric characterization with a finite certificate of nonvanishing, not a generic-position assumption on the vertices of $P$.

## 5. The origin and the source's cancellation example

For $v=0$, the nominal factor $1-\langle v,u\rangle$ is the unit polynomial 1. Thus the literal equality (2) cannot test whether the origin is an algebraic vertex. After choosing an origin outside the finite vertex set, condition (4) simply says $A(P)=V(P)$. For a fixed origin, the exclusion in (4) is necessary.

The source takes two opposite tetrahedra meeting at their common vertex. With standard basis vectors $e_i$, let
$$
P_\pm=\operatorname{conv}(v,v\pm e_1,v\pm e_2,v\pm e_3),
\qquad P=P_+\cup P_-.
$$
Writing $L=1-\langle v,u\rangle$ gives
$$
F_P(u)=
\frac{2(L^2+u_1u_2+u_1u_3+u_2u_3)}
     {(L^2-u_1^2)(L^2-u_2^2)(L^2-u_3^2)}.
\tag{11}
$$
The nonzero common-apex factor cancels. Locally its two opposite orthants have indicator
$$
h_1h_2h_3+(1-h_1)(1-h_2)(1-h_3)
=1-h_1-h_2-h_3+h_1h_2+h_1h_3+h_2h_3,
$$
where $h_i=\mathbf1_{\{x_i>0\}}$. Every term on the right is a line-cone indicator, including the whole-space term. This explicitly exhibits the signed geometric cancellation.

For the standard example with $v=0$, all six nonzero vertices still supply their factors, and (2) holds because the missing apex factor is already 1. Translating the same configuration to, for example, $v=(2,3,4)$ makes that canceled factor nonconstant and (2) fails. This explains why omitting the origin convention would state a stronger, false criterion.

## 6. Disposition

The exact Question 1 has a prior published characterization. Recommend **already_solved**, with credit to Akopyan–Bárány–Robins and the transform identities of Gravin–Pasechnik–Shapiro–Shapiro. The explanatory pole calculation is not promoted as a discovery.

The finite checker passes 284 exact assertions. It verifies rational identities, squarefree reduced denominators, artificial-vertex cancellation, a nonconvex example with a surviving reentrant vertex, the opposite-simplex parity control, and the literal origin exception. It does not replace the cited general theorem. No claim is made about the report's separate Questions 2–3, arbitrary polynomial densities, or reconstruction algorithms.
