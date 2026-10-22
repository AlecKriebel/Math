# Multiplier orders and infinitely many cubic Klein continued fractions

## Scope and result

Fix a totally real cubic number field $K$. We consider the historical Klein model: the union of the eight sails defined by the three eigen-hyperplanes of an irreducible integral $3\times3$ operator, with equivalence under $\mathrm{GL}_3(\mathbb Z)$. The results below hold even if the realizing operators are required to lie in $\mathrm{SL}_3(\mathbb Z)$ and to have three positive eigenvalues.

The question is Problem 3 in Karpenkov's 2004 paper [K04, p.16], restated as Problem 13 in [K17, p.8]. The following is an arithmetic and geometric partial result for that formulation, not a claimed classification by faces, integer angles, or torus decompositions. It makes no assertion about the other sail models discussed in [K17], complex cubic fields, or a Jacobi–Perron algorithm. In particular, no single characteristic polynomial, order, or ideal class is imposed on the original problem.

**Main conclusions.**

1. The entire eight-sail union geometrically determines its three defining hyperplanes. The rational endomorphisms preserving each of these planes form a copy of $K$; its integral endomorphisms form a canonically determined order, up to ring isomorphism.
2. This multiplier order has a positive trace discriminant $\Delta(S)$, invariant under integer-linear equivalence. For every positive integer $f$, there is a continued fraction $S_f$ in the fixed field $K$ with
   $$
   \Delta(S_f)=f^4\operatorname{disc}(K).
   $$
   Thus every fixed totally real cubic field gives **countably infinitely many** equivalence classes in the stated historical model.
3. There are only finitely many classes with a prescribed multiplier order, and only finitely many with $\Delta(S)\le X$. Consequently, if $N_K(X)$ counts these classes, then
   $$
   \left\lfloor\left(\frac{X}{\operatorname{disc}(K)}\right)^{1/4}\right\rfloor
   \ \le\ N_K(X)<\infty\qquad(X\ge\operatorname{disc}(K)).
   $$
4. A complete arithmetic equivalence criterion is given by full lattices in $K$, modulo multiplication by $K^\times$ and field automorphisms. A finite conductor-sandwich construction describes each order stratum. This is useful structural reduction, but it does not determine the face or torus geometry demanded by the broader classification program.

The infinitude statement answers the finiteness issue explicitly mentioned after the historical Problem 3. We do not infer a claim of novelty or current literature status from that historical remark.

## 1 Lattices and the Klein construction

Write $V=K\otimes_{\mathbb Q}\mathbb R$, and let
$$
\sigma:V\longrightarrow\mathbb R^3,
\qquad x\longmapsto(\sigma_1(x),\sigma_2(x),\sigma_3(x))
$$
be the real-algebra isomorphism given by the three embeddings of $K$. A full lattice $I\subset K$ is a free abelian group of rank three spanning $K$ over $\mathbb Q$. Its image $\sigma(I)$ is a lattice in $\mathbb R^3$.

Put $H_i=\ker\sigma_i\subset V$. These are real planes; their intersections with the rational vector space $K\subset V$ contain only zero. Their complement has eight open cones. For such a cone $C$, let
$$
P_C(I)=\overline{\operatorname{conv}}\bigl((I\cap\overline C)\setminus\{0\}\bigr),
\qquad
S(I)=\bigcup_C\partial P_C(I).
$$
Choosing a $\mathbb Z$-basis of $I$ identifies this construction with a continued fraction in $\mathbb R^3$ with lattice $\mathbb Z^3$. A different basis changes it by $\mathrm{GL}_3(\mathbb Z)$.

The use of closed convex hull does not change the sail in the historical definition. The convex hull here has nonempty interior, as follows from the lattice-parallelepiped argument below. A full-dimensional convex set and its closure have the same topological boundary. Thus the boundaries agree whether or not closure is inserted in the hull notation.

### Lemma 1 The missing rays recover the planes

For every full lattice $I\subset K$,
$$
\{0\}\ \cup\ \{v\in V\setminus\{0\}: \mathbb R_{>0}v\cap S(I)=\varnothing\}
=H_1\cup H_2\cup H_3.
\tag{1}
$$

**Proof.** Choose a positive integer $d$ with $dI\subset\mathcal O_K$. For every $0\ne x\in I$, the algebraic norm of $dx$ is a nonzero integer. Therefore
$$
|\sigma_1(x)\sigma_2(x)\sigma_3(x)|\ge d^{-3}=:\delta>0.
\tag{2}
$$
Fix one cone and change coordinate signs so that it becomes the positive octant. The function $g(y)=(y_1y_2y_3)^{1/3}$ is concave on the positive octant. Alternatively, the concavity of $\log(y_1y_2y_3)$ implies that its superlevel sets are convex. Thus every finite convex combination of the lattice points in this cone has coordinate product at least $\delta$. Continuity gives the same inequality on its closed convex hull. Since the hull lies in the closed octant, all its coordinates are consequently strictly positive. Hence no point of any sail lies on any $H_i$.

Conversely, take $v$ in an open cone. Express $tv$ in a lattice basis of $I$, round each of the three coefficients down, and use the eight vertices obtained by independently adding zero or one to each coefficient. Their convex hull is a lattice parallelepiped containing $tv$. Every vertex has bounded displacement from $tv$, with a bound independent of $t$. For all sufficiently large $t$, every vertex is in the open cone and is nonzero. It follows that $tv\in P_C(I)$. The same argument with one parallelepiped proves full dimensionality.

The set $\{t\ge0:tv\in P_C(I)\}$ is nonempty and closed. Inequality (2) excludes zero and a neighborhood of zero, so its infimum $t_0$ is positive and attained. The point $t_0v$ is a boundary point: points $tv$ with $t<t_0$ approach it from outside the hull. Thus the ray meets its sail. This proves (1). The three planes are individually recovered as the maximal real linear planes in the union on the right. Indeed, a plane not equal to any $H_i$ intersects each $H_i$ in a proper subspace, and a real plane is not the union of finitely many proper linear subspaces. ∎

No asymptotic visual recognition of a cone, assumed combinatorial rigidity, or supplied operator is used in this recovery.

## 2 The order recovered from the geometry

For the recovered unordered arrangement $\mathcal H=\{H_1,H_2,H_3\}$, define
$$
D_{\mathcal H}=\{T\in\operatorname{End}_{\mathbb Q}(K):
T_{\mathbb R}(H_i)\subseteq H_i\text{ for every }i\},
$$
and
$$
R_S=D_{\mathcal H}\cap\operatorname{End}_{\mathbb Z}(I).
\tag{3}
$$
The requirement is to preserve each plane individually; the planes need not be labeled. Endomorphisms in this definition need not be invertible.

### Lemma 2 The rational stabilizer algebra and its integral part

The algebra $D_{\mathcal H}$ consists precisely of multiplication maps $m_a:x\mapsto ax$, with $a\in K$. Under this identification,
$$
R_S=(I:I):=\{a\in K:aI\subseteq I\},
$$
which is an order in $K$.

**Proof.** In embedding coordinates, a linear map preserving all three coordinate hyperplanes is diagonal. If $T\in D_{\mathcal H}$ has diagonal entries $t_i$, set $a=T(1)\in K$. Evaluating at 1 gives $t_i=\sigma_i(a)$. For every $x\in K$,
$$
\sigma_i(Tx)=t_i\sigma_i(x)=\sigma_i(ax).
$$
Injectivity of any embedding gives $T(x)=ax$. Conversely, multiplication by any $a\in K$ is diagonal and preserves the planes. Formula (3) now gives the multiplier ring.

It is a unital subring. Choose a basis of $I$ and an integral basis of $\mathcal O_K$. The finitely many multiplication matrices for the latter basis have rational entries in the former. Clearing their denominators gives an integer $m>0$ with $m\mathcal O_K I\subseteq I$. Hence $\mathbb Z+m\mathcal O_K\subseteq(I:I)$. Conversely, any $a\in(I:I)$ has an integral multiplication matrix on $I$; its characteristic polynomial is monic integral and annihilates $a$. Thus $a\in\mathcal O_K$. The multiplier ring is therefore a full-rank subring of $\mathcal O_K$, namely an order. ∎

### Proposition 3 A geometric trace discriminant

For any $\mathbb Z$-basis $T_1,T_2,T_3$ of $R_S\subset\operatorname{End}_{\mathbb Q}(K)$, set
$$
\Delta(S)=\det\bigl(\operatorname{Tr}_{\mathbb Q}(T_iT_j)\bigr)_{i,j=1}^3.
\tag{4}
$$
This is a well-defined positive integer and is invariant under integer-linear equivalence of the eight-sail unions. It equals the ordinary number-theoretic discriminant of $(I:I)$.

**Proof.** Changing the integral basis multiplies the trace matrix on the left and right by unimodular transpose matrices, preserving its determinant. A lattice isomorphism taking one sail union to another takes the recovered planes to the recovered planes by Lemma 1. Conjugation therefore identifies both rational algebras and both integral rings in (3); matrix trace is conjugation invariant. Finally, $\operatorname{Tr}_{\mathbb Q}(m_am_b)=\operatorname{Tr}_{K/\mathbb Q}(ab)$, so (4) is the order discriminant. It is positive because $K$ is totally real and the trace form is the sum of the three squares on embedding coordinates. ∎

This is the discriminant of the recovered **order**, not the discriminant of an arbitrary realizing operator's characteristic polynomial. Those may differ. It is also not the discriminant of a ternary plane cubic norm form, whose geometric reducibility makes that different invariant inappropriate here.

## 3 Exact arithmetic equivalence and realization

### Theorem 4 Equivalence of full lattices

For full lattices $I,J\subset K$, their eight-sail continued fractions are integer-linearly equivalent if and only if
$$
J=a\tau(I)
\quad\text{for some }a\in K^\times,\quad
\tau\in\operatorname{Aut}_{\mathbb Q}(K).
\tag{5}
$$

**Proof.** An integer-linear equivalence is a real-linear isomorphism $T:V\to V$ with $T(I)=J$ taking sail union to sail union. Since the lattices span $K$ over $\mathbb Q$, it restricts to a rational-linear map $K\to K$. Lemmas 1 and 2 show that conjugation by $T$ is an automorphism of the multiplication algebra $K$. Thus there is a field automorphism $\tau$ such that
$$
Tm_xT^{-1}=m_{\tau(x)}\quad(x\in K).
$$
Set $a=T(1)\ne0$. Then
$$
T(x)=T(m_x1)=m_{\tau(x)}T(1)=a\tau(x),
$$
proving (5). Conversely, $a\tau$ permutes the embedding hyperplanes: $\tau$ permutes the embeddings and multiplication by $a$ rescales the coordinates by nonzero real numbers. It consequently permutes the eight cones. If it takes $I$ to $J$, it takes the defining lattice-point sets, their convex hulls, and their boundaries to the corresponding objects. It is therefore an equivalence. ∎

Only genuine field automorphisms occur in (5), not arbitrary permutations of the three embeddings. No narrow-ideal condition is appropriate for the union of all eight sails. Also, the union is centrally symmetric. In dimension three, replacing a determinant-minus-one equivalence $T$ by $-T$ gives a determinant-plus-one equivalence. Thus the historical determinant-one commuting criterion does not create an extra orientation class for the entire union; we retain the geometric $\mathrm{GL}_3(\mathbb Z)$ definition throughout.

### Proposition 5 Every full lattice occurs in the historical model

For every full lattice $I\subset K$, some operator in $\mathrm{SL}_3(\mathbb Z)$, in a basis of $I$, has irreducible characteristic polynomial, three distinct positive real eigenvalues, and exactly the planes used to define $S(I)$.

**Proof.** Let $R=(I:I)$. Dirichlet's unit theorem for orders [C, Theorem 1.1] gives an infinite-order unit $u\in R^\times$, since the unit rank of a totally real cubic order is two. Put $\varepsilon=u^2$. Its three embeddings are positive, its norm is one, and multiplication by it takes $I$ bijectively to itself. The corresponding matrix is therefore integral of determinant one.

The element $\varepsilon$ is not rational: a rational algebraic-integer unit is (1) or $-1$, while $u^2$ has infinite order. Since $[K:\mathbb Q]=3$ is prime, $\mathbb Q(\varepsilon)=K$. Its three conjugates are distinct by separability, and the multiplication operator's characteristic polynomial is its irreducible cubic minimal polynomial. In embedding coordinates the operator is diagonal with these conjugates, so its eigen-hyperplanes are exactly the three coordinate hyperplanes. ∎

Conversely, an irreducible rational $3\times3$ operator $A$ with field $\mathbb Q[A]\cong K$ makes $\mathbb Q^3$ a one-dimensional vector space over $K$. To see this explicitly, choose $0\ne v\in\mathbb Q^3$; the map $x\mapsto x(A)v$ from $K$ is injective because every nonzero $x(A)$ is invertible, and hence is an isomorphism by dimension. The preimage of $\mathbb Z^3$ is a full lattice $I$, and the real eigen-hyperplanes become the embedding hyperplanes. Thus Theorem 4 and Proposition 5 cover the whole stated historical class.

## 4 Infinite classes in every fixed field

### Theorem 6 The scalar-conductor family

Let $\mathcal O=\mathcal O_K$, and for $f\ge1$ put
$$
R_f=\mathbb Z+f\mathcal O,
\qquad I_f=R_f.
$$
Then the continued fractions $S(I_f)$ are pairwise inequivalent, and
$$
\Delta(S(I_f))=f^4\operatorname{disc}(K).
$$

**Proof.** The set $R_f$ is a unital ring: the product of $n+fx$ and $m+fy$ is again in $\mathbb Z+f\mathcal O$. It is a full lattice. Since $1\in R_f$, any $a$ with $aR_f\subseteq R_f$ lies in $R_f$ by evaluating at 1; the reverse inclusion follows from ring closure. Hence $(I_f:I_f)=R_f$.

The element 1 is primitive in the free abelian group $\mathcal O$: if $1=n\alpha$, with integer $n>1$ and $\alpha\in\mathcal O$, then $\alpha=1/n$ would be a nonintegral rational algebraic integer. Extend 1 to an integral basis $1,\omega_2,\omega_3$. Then $1,f\omega_2,f\omega_3$ is a basis of $R_f$, of index $f^2$ in $\mathcal O$. The trace Gram matrix changes by $D_f^{\mathsf T}GD_f$, where $D_f=\operatorname{diag}(1,f,f)$, so its determinant is $f^4\operatorname{disc}(K)$. Different positive $f$ give different geometric invariants by Proposition 3. Proposition 5 realizes every one by the required operators. ∎

There are at most countably many full lattices in $K$, because $K$ is countable and each is generated by three elements. Theorem 6 therefore proves exact countable infinitude, not merely an unbounded sequence of operator presentations for one continued fraction.

## 5 Finite order strata

### Theorem 7 A finite conductor sandwich

Fix an order $R\subset\mathcal O$. Up to multiplication by $K^\times$, there are finitely many full lattices $I\subset K$ with $(I:I)=R$. More concretely, choose representatives $J_1,\ldots,J_h$ for the fractional ideal classes of $\mathcal O$ and put
$$
\mathfrak c=\{x\in\mathcal O:x\mathcal O\subseteq R\}.
$$
Every such lattice is homothetic to a lattice in one of the finite intervals
$$
\mathfrak c J_i\ \subseteq\ I\ \subseteq\ J_i,
\tag{6}
$$
subject to $RI\subseteq I$, $\mathcal OI=J_i$, and $(I:I)=R$.

**Proof.** The ring of integers is Dedekind and has finite ideal class group [W, II.3 and IV.2]. For a full lattice $I$, the $\mathcal O$-span $J=\mathcal OI$ is a nonzero fractional ideal. Multiplying $I$ by a nonzero field element, arrange $J=J_i$. By the conductor definition and the $R$-stability of $I$,
$$
\mathfrak cJ_i=\mathfrak c\mathcal OI\subseteq RI\subseteq I\subseteq J_i.
$$
The conductor contains $m\mathcal O$ for some positive integer $m$, because $R$ has finite index in $\mathcal O$. Thus $J_i/\mathfrak cJ_i$ is finite. The lattices in (6) correspond to subgroups of this finite abelian group, so there are finitely many possibilities. The three stated conditions select exactly the normalized lattices of interest. ∎

Within a single interval with $\mathcal OI=\mathcal OI'=J_i$, a homothety $I'=aI$ implies $aJ_i=J_i$. Invertibility of the fractional ideal $J_i$ implies $a\mathcal O=\mathcal O$, so $a\in\mathcal O^\times$. The remaining homothety identifications are consequently the orbits of a finite permutation action of $\mathcal O^\times$ on the eligible subgroups of $J_i/\mathfrak cJ_i$. Field automorphisms supply the additional identifications specified in Theorem 4, possibly permuting both orders and ideal classes. This describes a finite arithmetic quotient for each order orbit without incorrectly restricting to invertible ideals of the nonmaximal order $R$.

### Corollary 8 Bounded discriminant gives finitely many classes

Every order $R\subset\mathcal O$ has
$$
\operatorname{disc}(R)=[\mathcal O:R]^2\operatorname{disc}(K).
$$
Thus a bound on $\Delta(S)$ bounds the index of its multiplier order. There are only finitely many subgroups of a free abelian group of fixed rank and bounded index: for index $m$, the subgroup contains $m\mathcal O$ and comes from a subgroup of the finite group $\mathcal O/m\mathcal O$. There are therefore finitely many relevant orders. Apply Theorem 7 and then quotient by field automorphisms. Combining this finiteness with Theorem 6 gives the asserted bounds on $N_K(X)$.

This shows precisely why restricting the original problem to one order would lose infinitely many distinct geometric objects, even though each separate order stratum is finite.

## 6 A small exact example

Let $\theta$ be a root of $t^3-3t+1$, and let $R_0=\mathbb Z[\theta]$. The polynomial has no rational root and has one root in each of $(-2,-1),(0,1),(1,2)$, so $K=\mathbb Q(\theta)$ is totally real cubic. We do **not** need to assert that $R_0$ is maximal.

In the basis $1,\theta,\theta^2$, multiplication by $\theta$ is
$$
C=\begin{pmatrix}0&0&-1\\1&0&3\\0&1&0\end{pmatrix}.
$$
Let $U=C^2$ and $A=U^3=C^6$. On the lattice $R_3=\mathbb Z+3R_0$, with basis $1,3\theta,3\theta^2$, the same multiplication by $\theta^6$ is represented by $B=D_3^{-1}AD_3$. Explicitly,
$$
A=\begin{pmatrix}1&-9&6\\-6&28&-27\\9&-6&28\end{pmatrix},
\qquad
B=\begin{pmatrix}1&-27&18\\-2&28&-27\\3&-6&28\end{pmatrix}.
$$
Both matrices have determinant one and characteristic polynomial
$$
t^3-57t^2+570t-1.
$$
This polynomial is irreducible by the rational-root test. Its roots are the positive, distinct sixth powers of the conjugates of $\theta$. Distinctness also follows from the irreducibility and characteristic-zero separability. Thus both are admissible operators with exactly the same characteristic polynomial and exactly the same cubic field.

Nevertheless their eight-sail continued fractions are inequivalent. The trace Gram matrix for $1,\theta,\theta^2$ is
$$
G=\begin{pmatrix}3&0&6\\0&6&-3\\6&-3&18\end{pmatrix},
\qquad \det G=81.
$$
Their multiplier orders are $R_0$ and $R_3$, respectively, because each lattice is itself a unital ring. Their geometric trace discriminants are $81$ and $3^4\cdot81=6561$. Proposition 3 separates them.

For an additional direct calculation, multiplication by $a+b\theta+c\theta^2$ in the basis $1,f\theta,f\theta^2$ is
$$
\begin{pmatrix}
a&-fc&-fb\\
b/f&a+3c&3b-c\\
c/f&b&a+3c
\end{pmatrix}.
$$
For rational $a,b,c$, integrality of this matrix is equivalent to $a\in\mathbb Z$ and $b,c\in f\mathbb Z$. This independently recovers the multiplier order of $\mathbb Z+fR_0$.

The ordinary norm form is
$$
\begin{aligned}
N(x+y\theta+z\theta^2)={}&x^3+6x^2z-3xy^2+3xyz+9xz^2\\
&-y^3+3yz^2+z^3.
\end{aligned}
$$
It is supplied as an exact algebraic check, not as a replacement for the missing-ray proof or a computation of all sail faces.

## 7 What this establishes and what remains

The discriminant obstruction is extracted from the actual geometric union, and the infinite family is realized inside the exact historical operator class. The finite-order reduction keeps all orders and all full lattices, including noninvertible ideals of nonmaximal orders. These results do not rely on the historical paper's commuting-conjugacy statement.

The broader request for a geometrically informative classification remains only partially answered here. We have not enumerated or characterized the possible face types, adjacency, integer distances and angles, or decorated torus decompositions for a fixed field. Nor have we established a simple necessary-and-sufficient combinatorial criterion for those data. The complete arithmetic equivalence criterion in Theorem 4 should not be presented as having supplied those absent geometric descriptions. In particular, this note is not a claim to have solved all of Problem 13 in the larger 2017 survey context.

## References

- [K04] Oleg Karpenkov, *On examples of two-dimensional periodic continued fractions*, arXiv:math/0411054 (2004). Definitions 1.1–1.2 and Statement 1.2, pp.3–4; same-field discussion and Problem 3, pp.15–16. https://arxiv.org/pdf/math/0411054
- [K17] Oleg Karpenkov, *Open Problems in Geometry of Continued Fractions*, arXiv:1712.01450v1 (2017). Problem 13, p.8; scope and geometric-classification context, pp.3–9. https://arxiv.org/pdf/1712.01450
- [C] Keith Conrad, *Dirichlet's Unit Theorem*, Theorem 1.1, p.1, for orders in number fields. https://kconrad.math.uconn.edu/blurbs/gradnumthy/unittheorem.pdf
- [W] Tom Weston, *Algebraic Number Theory*. Theorem II.2.22, p.39, for the integral-basis theorem; Proposition II.3.3, p.43, and Proposition II.3.6, pp.45–46, for Dedekindness and invertibility; Corollary IV.2.3, p.83, for finite class number. https://kconrad.math.uconn.edu/math5230f08/weston.pdf
