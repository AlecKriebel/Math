# Fixed face types and the volume product in three dimensions

Problem 20001282 / AIM-CONVEX_GEOMETRY-0014. Research date: 2026-10-03.

## 1. Actual question and status

The primary problem is Question **18** in the 2010 AIM workshop list, attributed to G. Kuperberg. It concerns the volume product on every realization class of centrally symmetric three-polytopes with one fixed combinatorial type other than the cube or octahedron. It proposes absence of local minima and additionally asks whether each such class has just one critical affine orbit, which is a local maximum. The corpus title about a product-prism family is not the original question. The extracted initial “8” is a dropped digit.

This note establishes two carefully separated conclusions:

1. **The no-local-minimum assertion follows from already available shadow-system results.** The specific modern source is Chen–Li–Xi–Xu, arXiv:2605.13795v1 (2026), Proposition 3.8 and Lemmas 4.1, 5.2. Sections 2–4 give the fixed-stratum deduction and the underlying count, with attribution. This is a consequence of a current preprint, not a claim to have first solved this assertion.
2. **For the hexagonal-bipyramid and hexagonal-prism face types, the full critical-point question has an explicit affirmative answer.** Sections 5–8 give a complete three-coordinate chart, including nonplanar equators, exact volumes, and the unique critical point. This goes beyond restricting the calculation to Cartesian-product prisms. The global maximum 12 was already announced in Alexander's 2017 BIRS slides; no priority is claimed for that value or for the present local classification.

**The unique-critical-orbit/local-maximum question for all other face types is not resolved here.** Consequently this is a partial answer to the compound original question.

Translate the symmetry center to zero and put

\[
P(K)=|K|\,|K^\circ|,\qquad
K^\circ=\{y:x\cdot y\leq1\text{ for all }x\in K\}.
\]

Work in the Hausdorff topology on origin-symmetric realizations of a prescribed face lattice. Local extrema are understood relative to that class. On a smooth marked chart, criticality means vanishing of all derivatives after removing the linear-coordinate freedom. Polarity is a continuous involution, preserves P, and interchanges a face lattice with its dual. The affine quotient is relevant because P(TK)=P(K).

## 2. Admissible shadows and local minima

The construction and counting argument in Sections 2–4 follow the method of Chen–Li–Xi–Xu [CLXX]. Their source is a preprint; its bibliographic status should not be silently upgraded. We include the argument to make the fixed-type implication checkable. The analytic input is the established Meyer–Reisner shadow-system theorem [MR, Theorem 1 and Proposition 7]: inverse polar volume is convex along a nondegenerate shadow system; if primal volume and inverse polar volume are both affine in the parameter, the bodies are related by the corresponding affine shears. Polars in that theorem are based at the Santaló point, which is zero for the symmetric bodies used here.

Fix a unit vector \(\theta\). For vertices \(x_i\) of \(K=-K\), choose scalar speeds \(\alpha_i\), odd under antipodal pairing, and set

\[
K_t=\operatorname{conv}\{x_i+t\alpha_i\theta\}.
\]

Call the speeds admissible when their restriction to each facet whose plane is not parallel to \(\theta\) agrees with an affine scalar function on that plane. A facet parallel to \(\theta\) imposes no such restriction: its moving vertices already stay in its plane.

For sufficiently small \(|t|\), these conditions preserve the face lattice. On a nonparallel facet the map is an affine perturbation of the identity; on a parallel facet the vertices remain in the original plane. Strict supporting inequalities for vertices outside each facet persist. Strict convexity of each facet polygon also persists. Thus the same vertices, edges and facets remain incident. Odd speeds preserve central symmetry.

Triangulate the boundary consistently with its fixed face lattice. Each determinant in the cone-volume formula is affine in t: every term containing two displacement columns vanishes because both columns are multiples of \(\theta\). It follows that

\[
a(t)=|K_t|\quad\text{is affine},\qquad b(t)=|K_t^\circ|^{-1}\quad\text{is convex}.
\]

If t=0 were a local minimum of \(P(K_t)=a(t)/b(t)\), shrink to a symmetric closed interval on which it is a minimum. With \(\lambda=b(0)/a(0)\),

\[
h(t)=b(t)-\lambda a(t)\leq0,\qquad h(0)=0.
\]

A convex function bounded above by zero and attaining zero at an interior point is identically zero on this interval. Hence b is affine. The equality statement in [MR] supplies

\[
K_t=A_tK_0,\qquad A_t(x)=x+t(w\cdot x+\beta)\theta.
\]

Centers of symmetry give \(\beta=0\). For sufficiently small t, the distinct moving vertices have the same labels as \(A_tx_i\), since both converge to \(x_i\). Therefore \(\alpha_i=w\cdot x_i\). Such speeds form exactly a three-dimensional vector space: the vertices span \(\mathbb R^3\).

**Local obstruction.** A fixed-type local minimum has only these globally linear speeds, for every \(\theta\). Its polar has the same property, because polarizing a sufficiently small type-preserving deformation gives a small deformation in the original class. This argument needs neither a global minimum nor a bounded-vertex minimization problem.

## 3. The dimension count

Write V, E, F for the vertex, edge and facet counts. For a facet G write m(G) for its number of vertices, and define

\[
C_\theta(K)=\tfrac12\sum_{G:\theta\parallel G}(m(G)-3).
\]

The space of odd speeds has dimension V/2. Each nonparallel facet imposes at most m(G)-3 independent restrictions; an opposite facet imposes the same restrictions. Consequently the space \(A_\theta\) of admissible odd speeds satisfies

\[
\begin{aligned}
\dim A_\theta
&\geq \tfrac V2-\tfrac12\sum_{G:\theta\not\parallel G}(m(G)-3)\\
&=\tfrac V2+\tfrac{3F}2-E+C_\theta\\
&=\tfrac{F-V}2+2+C_\theta.
\end{aligned}
\]

The last line uses Euler's identity V−E+F=2. If this bound exceeds 3, a nontrivial shadow exists and the local obstruction applies.

Suppose neither K nor its polar has a nontrivial admissible shadow. Applying the estimate to both gives \(|V-F|\leq2\). Both V and F are even, so there are three possibilities.

- **V=F+2.** In the polar, the lower bound is \(3+C_\theta\). A vertex of K of degree at least four would give a nonsimplicial dual facet; choosing a direction parallel to that facet makes \(C_\theta\geq1\), a contradiction. Thus K is simple, \(2E=3V\). Euler's identity now gives V=8 and F=6. The three pairs of opposite facet planes describe an invertible linear image of a cube.
- **F=V+2.** Apply the preceding argument to the polar. K is a linear image of an octahedron.
- **V=F.** No facet can have five or more vertices, since a parallel direction would make \(C_\theta\geq2\). Nor can two quadrilateral facets share an edge: choosing its direction makes the same bound at least four. If p and q count triangular and quadrilateral facets, then
  \[
  p+q=V,\quad 3p+4q=2E=4V-4,
  \]
  so p=4. Each quadrilateral edge borders a triangle, hence \(4q\leq3p=12\). Symmetry makes q even, so q≤2 and V=p+q≤6. Full dimension forces V=6; a symmetric three-polytope with six vertices is an octahedron with eight facets, contradicting V=F.

This proves the classification of shadow-rigid pairs used in [CLXX, Lemma 5.2].

## 4. General fixed-type no-minimum consequence

If K were a local minimum in its centrally symmetric realization class, Section 2 would make both K and its polar shadow-rigid. Section 3 would force K to be a cube or an octahedron up to linear equivalence. Therefore every other centrally symmetric three-dimensional face type has **no local minimum of P**.

The source dependence and novelty boundary are important: this is the fixed-type consequence of the 2026 admissible-shadow-system argument, with the classical analytic input [MR]. It is stronger than the logical consequence of the global three-dimensional Mahler lower bound alone. The latter would not exclude a nonglobal constrained local minimum.

## 5. A complete chart for the hexagonal-bipyramid stratum

Let \(\mathcal B\) be the class of centrally symmetric polytopes with the face lattice of a hexagonal bipyramid. The two degree-six vertices are antipodal and intrinsically distinguished; call them ±a. The equatorial six-cycle is antipodally paired. A finite choice of cyclic marking lets its vertices be written

\[
u,w,v,-u,-w,-v.
\]

The triangle with vertices a,v,−u is a facet. Its plane excludes zero, so a,u,v are linearly independent. Normalize u=e₁, v=e₂ and a=e₃; then write w=(p,q,r). The orientation of the facet fan at e₃ gives p>0 and q>0. Thus every marked member has a representative

\[
B_{p,q,r}=\operatorname{conv}\{\pm e_1,\pm e_2,\pm e_3,\pm(p,q,r)\}.
\]

The exact open chamber is

\[
\mathcal D=\{p,q>0:\quad |r|<p+q-1,\quad |p-q|+|r|<1\}.
\tag{1}
\]

Here is a direct incidence check. The twelve desired triangular facets consist of either apex and one edge of the displayed equatorial cycle. At apex \(\sigma e_3\), \(\sigma\in\{\pm1\}\), the three representative supporting normals, normalized to supporting value 1, are

\[
\left(1,\frac{1-p-\sigma r}{q},\sigma\right),\qquad
\left(\frac{1-q-\sigma r}{p},1,\sigma\right),\qquad
(-1,1,\sigma).
\]

Their antipodal counterparts give the other facets. Requiring all other vertices to lie strictly below the corresponding supporting planes is equivalent to (1). Thus these are precisely twelve triangular facets, with all eight indicated vertices distinct and extreme. Conversely, in a bipyramid realization the same facet inequalities are necessary, so this chart misses no marked realization. It is a full local coordinate chart after linear normalization, with only finitely many markings.

The r coordinate cannot be discarded. For r≠0, the equatorial vertices e₁,e₂,(p,q,r) span three dimensions; no invertible linear map can turn their equatorial set into a plane. Such a bipyramid is not an affine image of a geometric double cone with a planar equator. Its polar is a combinatorial hexagonal prism that is not affinely a Cartesian product prism.

## 6. Exact primal and polar volumes

Coning each triangular facet to zero gives

\[
|B_{p,q,r}|=\frac23(p+q+1).
\tag{2}
\]

Indeed, for either apex the six determinant magnitudes are q,p,1,q,p,1. The r coordinate cancels because the apex is parallel to e₃.

The polar is

\[
B_{p,q,r}^{\circ}
=\{(x,y,z):|x|,|y|,|z|\leq1,\ |px+qy+rz|\leq1\}.
\]

At each height z∈[−1,1], condition (1) says that the strip removes exactly the two opposite corners of the square [−1,1]² and leaves its mixed-sign corners. The two removed triangle areas are

\[
\frac{(p+q-1+rz)^2}{2pq},\qquad
\frac{(p+q-1-rz)^2}{2pq}.
\]

Integrating their complement gives

\[
|B_{p,q,r}^{\circ}|=8-\frac{2}{pq}\left((p+q-1)^2+\frac{r^2}{3}\right).
\tag{3}
\]

Multiplying (2) and (3),

\[
\boxed{P(B_{p,q,r})=\frac43(p+q+1)
\left[4-\frac{(p+q-1)^2+r^2/3}{pq}\right].}
\tag{4}
\]

At r=0 the bipyramid is a geometric double cone and its polar is a product prism. Formula (4) contains the familiar product identity \(P(H\times[-a,a])=\frac43P(H)\), but also includes the missing transverse term for the entire realization stratum.

## 7. All critical points and sharp bounds

Put s=p+q and d=p−q. The chamber becomes

\[
s>1,\qquad |r|<\min(s-1,1-|d|).
\]

First,

\[
\frac{\partial P}{\partial r}
=-\frac{8(s+1)r}{9pq}.
\]

Every critical point has r=0. At r=0,

\[
\frac{\partial P}{\partial d}
=-\frac{32(s+1)(s-1)^2d}{3(s^2-d^2)^2}.
\]

Thus d=0. On this line,

\[
P=\frac43\left(8+\frac4s-\frac4{s^2}\right),\qquad
\frac{dP}{ds}=\frac{16(2-s)}{3s^3}.
\]

The only critical chart point is (s,d,r)=(2,0,0), or (p,q,r)=(1,1,0). Its Hessian in (s,d,r) coordinates is

\[
\operatorname{diag}(-2/3,-2,-8/3).
\]

Hence it is a nondegenerate strict local maximum in full affine moduli. In fact it is the strict global maximum: (4) decreases with r²; with r=0 and s fixed it increases with pq, whose maximum is s²/4. Finally

\[
8+4/s-4/s^2=9-(s-2)^2/s^2\leq9.
\]

Therefore P≤12 with equality only at this orbit.

There are no local minima even without Section 4: at any chart point, a sufficiently small increase in |r| stays in the open chamber and decreases (4). At r=0 either sign of a small nonzero r works. In particular,

\[
P(B_{1,1,\varepsilon})=12-\frac43\varepsilon^2,\qquad |\varepsilon|<1.
\]

For completeness, the sharp lower limit can also be verified directly. Subtraction gives

\[
P-\frac{32}{3}
=\frac{16}{3(s^2-d^2)}
\left[(s-1)(1-d^2)-\frac{(s+1)r^2}{3}\right].
\]

Let a=s−1>0 and b=1−|d|∈(0,1]. Because \(r^2<\min(a,b)^2\), it suffices to show

\[
(a+2)\min(a,b)^2\leq3ab(2-b).
\]

If a≤b, use \(a(a+2)\leq b(b+2)\leq3b(2-b)\). If a≥b, use \(a(3-2b)\geq b\), equivalently \((a+2)b\leq3a(2-b)\). Thus P>32/3. Taking p=q=1 and r→1 approaches 32/3; at r=1 the polytope has the cube face type. The chamber is convex, so continuity together with these endpoints also gives the exact range

\[
P(\mathcal B)=(32/3,12].
\]

## 8. Dual prism conclusion and remaining gap

Polarity identifies the entire hexagonal-bipyramid class with the entire centrally symmetric hexagonal-prism class, preserving P and local criticality on the normalized smooth charts. Both classes therefore have exactly one critical affine orbit, represented respectively by an affine-regular planar hexagon with symmetric apices and its polar product prism. This is a full-stratum statement; it does not assume that every combinatorial prism is a geometric product.

No argument above supplies uniqueness of critical points for a general other face lattice. In particular, a direction lowering a function somewhere near each point does not classify its critical points. Even stationary restrictions to many one-parameter shadows do not automatically control cross terms in an arbitrary multi-parameter Hessian. Nontrivial topology or boundary degeneration of realization spaces also cannot be ignored. The unproved universal secondary assertion is the stopping point of this investigation.

## References

- **[AIM]** American Institute of Mathematics, *Mahler's conjecture and duality in convex geometry*, August 9–13, 2010, Question 18, printed page 3. https://aimath.org/WWN/mahlerduality/mahlerduality.pdf
- **[MR]** M. Meyer and S. Reisner, *Shadow systems and volumes of polar convex bodies*, Mathematika 53 (2006), 129–148, Theorem 1 and Proposition 7; arXiv version 2. https://arxiv.org/abs/math/0606305 ; https://doi.org/10.1112/S0025579300000061
- **[CLXX]** S. Chen, Y. Li, D. Xi and Z.-F. Xu, *The Symmetric Mahler Inequality in Dimension Three via Admissible Shadow Systems*, arXiv:2605.13795v1, submitted 13 May 2026; Proposition 3.8, Lemmas 4.1 and 5.2. **Preprint.** https://arxiv.org/abs/2605.13795v1
- **[IS]** H. Iriyeh and M. Shibata, *Symmetric Mahler's conjecture for the volume product in the three-dimensional case*, Duke Math. J. 169 (2020), 1077–1134. https://arxiv.org/abs/1706.01749 ; https://doi.org/10.1215/00127094-2019-0072
- **[A17]** M. Alexander, *Polytopes of maximal volume product*, BIRS talk, 25 May 2017, joint work with M. Fradelizi and A. Zvavitch; the symmetric eight-vertex maximum is announced on PDF pages 33–35 and discussed again on pages 65–70. https://archive.birs.ca/files/2017/17w5074/files/Alexander_Banff.pdf
