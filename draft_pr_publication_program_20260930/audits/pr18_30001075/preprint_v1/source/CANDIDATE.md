# Common tangent loci of three convex sets have outer measure zero

**Problem:** 30001075 / OWR-2090-028, Conjecture 4 of Xavier Goaoc's problem in Oberwolfach Report 44/2008, p. 2552.

**Status:** Current candidate after three independent mathematical/source-scope audits and notation/provenance repairs; complete priority and publication gates remain pending. Historical priority is unconfirmed. This document does not claim a solution to the stronger countable-union-of-2-manifolds conjecture.

**Prepared:** 2026-09-30. Model: gpt-6-astra, reasoning effort xhigh.

## 1. Statement and source scope

A line is tangent to a convex set if it meets the set and is contained in a supporting plane of the set. The plane need not be unique, and the intersection with the line may be a segment.

**Theorem (candidate).** Let \(K_1,K_2,K_3\subset\mathbb R^3\) be pairwise disjoint convex sets. The union of the affine lines tangent to all three is contained in a Lebesgue-null set.

No closedness, boundedness, smoothness, strict convexity, positive curvature, full dimensionality, or generic-position hypothesis is imposed.

The exact source is [Oberwolfach Report 44/2008](https://ems.press/content/serial-article-files/46191), section 13, p. 2552, Conjecture 4. It distinguishes this assertion from Conjecture 3, which asks for containment in a countable union of 2-manifolds. It records closedness and empty interior as known background. The inspected underlying arguments use compact or closed convex objects; closedness does not extend to arbitrary nonclosed sets (see REVIEW_UPDATES.md for a counterexample). Empty interior alone does not imply the desired measure-zero conclusion. The proof below uses closed tangency only after its compact reduction.

The cited underlying work is Demouth–Goaoc, *Topological changes in the apparent contour of convex sets*, manuscript, 2008. Its geometric arguments are also developed in [Julien Demouth's 2008 thesis](https://theses.hal.science/tel-00342717/document), chapter 4: terminology on printed p. 48 defines objects to be closed convex sets; Theorem 3 on p. 51 and Lemma 20 on p. 66 establish nowhere density. The proof below does not use that nowhere-density result. A newly inspected undated author-uploaded manuscript version (ResearchGate upload 16 April 2015) likewise treats compact convex objects and expressly asks the measure-zero question in section 7, printed p. 11. It cites the November 2008 thesis, so its identity with the September 2008 cited manuscript has not been established. This is historical context, not a certificate of current openness.

## 2. Reduction to compact convex sets

It suffices to establish the theorem for nonempty compact convex sets. Throughout the proof, a “rational ball” means a ball from one fixed countable base in the original ambient Cartesian coordinates, independent of every line-dependent change of coordinates below. Such balls can contain any prescribed point in their interiors while having arbitrarily small diameter.

Indeed, let a line \(L\) be tangent to arbitrary pairwise disjoint convex sets \(K_i\), and choose \(a_i\in L\cap K_i\). The three points are distinct. Choose pairwise disjoint closed balls \(B_i\), with rational centers and positive rational radii, such that \(a_i\in\operatorname{int}B_i\). Set
\[
C_i=\overline{K_i}\cap B_i.
\]
These are nonempty, compact, pairwise disjoint convex sets. Every supporting plane of \(K_i\) also supports its closure, so \(L\) is tangent to all three \(C_i\). There are only countably many such triples of balls. Thus the original locus is contained in a countable union of compact-case loci. This reduction also avoids any measurability assumption on the original convex sets.

Henceforth the three sets are compact and nonempty.

## 3. Coordinates and a scalar tangency function

A local chart in the four-dimensional space of affine lines has the form
\[
L(u,v)=\{(u+zv,z):z\in\mathbb R\},\qquad u,v\in\mathbb R^2.
\tag{1}
\]
Around any prescribed line we may choose orthonormal coordinates so that the prescribed line is \(L(0,0)\).

For a compact convex set \(C\), write
\[
\pi_v(x,z)=x-zv,\qquad
h_C(\xi,\tau)=\max_{(x,z)\in C}(\xi\cdot x+\tau z).
\]
Define the Lipschitz function
\[
g_C(u,v)=\max_{n\in S^1}\{n\cdot u-h_C(n,-n\cdot v)\}.
\tag{2}
\]
The Lipschitz assertion follows directly from boundedness of \(C\) and \(|n|=1\).

Whenever \(\pi_v(C)\) has interior in \(\mathbb R^2\), we have
\[
g_C(u,v)=0\quad\Longleftrightarrow\quad
u\in\partial\pi_v(C)
\quad\Longleftrightarrow\quad L(u,v)\text{ is tangent to }C.
\tag{3}
\]
For the first equivalence, (2) is the maximum of the normalized support inequalities for the compact convex set \(\pi_v(C)\): it is negative in its interior, zero on its boundary, and positive outside. The second follows because a supporting line of the projection lifts to a supporting plane containing \(L\), and conversely.

Projection has interior for every full-dimensional \(C\). If \(C\) has affine dimension two, it has interior after projection precisely when the line direction is transverse to its affine plane. Any line meeting that plane is either transverse to it or contained in it. All lines of the latter type contribute only the plane itself to the sought locus, a null set which can be discarded.

We will use the following elementary increment estimate. For fixed \(n\in S^1\), let
\(\psi_n(u,v)=n\cdot u-h_C(n,-n\cdot v)\). For arbitrary increments \((\delta u,\delta v)\),
\[
\min_{(x,z)\in C} n\cdot(\delta u+z\delta v)
\le \psi_n(u+\delta u,v+\delta v)-\psi_n(u,v)
\le \max_{(x,z)\in C} n\cdot(\delta u+z\delta v).
\tag{4}
\]
This is the standard difference bound for two maxima, or follows immediately from the definition of \(h_C\). No derivative of the support function is used.

## 4. Two tangencies admit countably many Lipschitz two-parameter covers

**Lemma 1.** Suppose \(A,B\) are disjoint compact convex sets, both of affine dimension at least two. Discard lines contained in the affine plane of either planar set. The remaining common tangent lines are covered by countably many Lipschitz maps from open subsets of \(\mathbb R^2\) into line space. The maps are allowed to include extra lines.

**Proof.** Fix one remaining common tangent \(L_0\), take coordinates with \(L_0=L(0,0)\), and choose contacts
\[
a=(0,s)\in A,\qquad b=(0,t)\in B,\qquad s<t.
\]
Put \(d=t-s>0\). The origin is on the boundary of each of the two-dimensional projections \(\pi_0(A),\pi_0(B)\). Let \(N_A,N_B\subset S^1\) be their outward unit supporting normals at the origin. There are unit vectors \(e_A,e_B\) and positive constants \(\alpha_A,\alpha_B\) such that
\[
n\cdot e_i\ge\alpha_i>0\quad(n\in N_i).
\tag{5}
\]
For example, choose a disk \(B(w,r)\) inside the corresponding projection. Then every such \(n\) satisfies \(n\cdot w\le-r\), so \(e=-w/|w|\) works.

Choose
\[
0<\varepsilon<\min(1/4,\alpha_A/16,\alpha_B/16).
\tag{6}
\]
We can choose closed rational balls \(D_A,D_B\), containing \(a,b\) in their interiors, so small that the compact caps
\[
A'=A\cap D_A,\qquad B'=B\cap D_B
\]
have all their heights respectively in
\([s-\varepsilon d,s+\varepsilon d]\) and \([t-\varepsilon d,t+\varepsilon d]\).

At \(L_0\), the projected supporting-normal sets of these caps are still exactly \(N_A,N_B\). To see the nontrivial inclusion, a linear functional supporting a cap on \(L_0\) vanishes at \(a\), respectively \(b\). If it were positive at some point of the original set, the initial portion of the segment joining that point to the contact would be inside the ball and contradict support of the cap. The caps have the same affine dimensions as the original sets; projection therefore still has interior.

Consider two motions of the line, written as their displacement at height \(z\):
\[
V_A(z)=\frac{t-z}{d}e_A,\qquad
V_B(z)=\frac{z-s}{d}e_B.
\tag{7}
\]
They are independent vectors in line-coordinate space: evaluating at heights \(s,t\) gives, respectively, \((e_A,0)\) and \((0,e_B)\). Complete them to a linear coordinate system
\[
(u,v)=a_0 V_A+b_0 V_B+R(r),\qquad r\in\mathbb R^2,
\tag{8}
\]
where each \(V_i\) in (8) denotes its pair of intercept and slope coordinates.

By compactness of \(S^1\) and continuity in (2), every maximizing normal for \(g_{A'}\), at lines sufficiently close to \(L_0\), satisfies \(n\cdot e_A\ge\alpha_A/2\); likewise for \(B'\). Indeed, a sequence of maximizers at lines tending to \(L_0\) has a subsequence converging to a maximizer at \(L_0\), which belongs to \(N_i\).

Take a small coordinate box around zero where these facts and projection interior hold. For \(h>0\), whenever the compared points lie in this box, (4), applied to a maximizing normal at the initial point, gives
\[
g_{A'}(a_0+h,b_0,r)-g_{A'}(a_0,b_0,r)\ge m_Ah,
\quad m_A=\alpha_A/4.
\tag{9}
\]
Here the own-motion coefficient \((t-z)/d\) on \(A'\) is at least \(1-\varepsilon>1/2\). The corresponding statement holds for \(g_{B'}\) in its own coordinate \(b_0\), with \(m_B=\alpha_B/4\).

The cross-motion coefficients have absolute value at most \(\varepsilon\), so (4), now valid for every unit \(n\), also gives
\[
|g_{A'}(a_0,b_0+h,r)-g_{A'}(a_0,b_0,r)|\le\varepsilon|h|,
\]
\[
|g_{B'}(a_0+h,b_0,r)-g_{B'}(a_0,b_0,r)|\le\varepsilon|h|.
\tag{10}
\]

For fixed sufficiently small \((b_0,r)\), strict monotonicity (9) and the intermediate value theorem give a unique nearby zero
\(a_0=\rho_A(b_0,r)\). The root is Lipschitz in all its arguments, and is Lipschitz in \(b_0\) with constant at most \(\varepsilon/m_A<1/4\). Similarly the other zero is \(b_0=\rho_B(a_0,r)\), with cross Lipschitz constant less than \(1/4\). Both roots are zero at zero. After choosing a small closed square in \((a_0,b_0)\) and then a sufficiently small open ball of parameters \(r\), the map
\[
(a_0,b_0)\longmapsto
\bigl(\rho_A(b_0,r),\rho_B(a_0,r)\bigr)
\tag{11}
\]
maps that square into itself and is a contraction in the maximum norm. Its unique fixed point depends Lipschitz-continuously on \(r\). Thus the simultaneous zero set, near \(L_0\), is a Lipschitz two-dimensional graph. By (3), it contains exactly the common tangents to the two caps in that neighborhood. In particular it contains \(L_0\).

For completeness, the countability point matters: a nearby tangent of the original body need not touch the same cap. There are only countably many pairs of rational balls. For each fixed pair, consider the set of common tangents to its caps at which the preceding construction is available. The open line-space neighborhoods obtained by the construction cover that set; since line space is second countable, a countable subcover suffices. Every line in this set belongs to the simultaneous-zero set for the fixed caps, so it belongs to the graph associated with whichever neighborhood covers it. Taking the union over the countably many cap pairs covers every original common tangent under consideration. This proves the lemma. \(\square\)

## 5. A rank restriction at a tangent contact

We next use only the existence of Lipschitz two-parameter covers, and not their specific construction.

Let \(F:q\mapsto(u(q),v(q))\), \(q\in U\subset\mathbb R^2\), be a Lipschitz line-family chart. Let \(E\subset U\) be the measurable set of parameters for which the line is tangent to each of our three compact sets. Discard from the family lines contained in the plane of a planar set, and lines identical to the affine line of a one-dimensional set. Their swept loci lie in finitely many planes or lines and are null.

Compactness implies that tangency is a closed condition in line space: along a convergent sequence of tangent lines, take convergent subsequences of contact points and of unit supporting-plane normals. The limiting contact and plane witness tangency. Thus \(E\), including the stated open exclusions, is Borel.

Almost every \(q_0\in E\) is a density point of \(E\) and a differentiability point of \(F\). At such a point, write
\[
A=D u(q_0),\qquad B=D v(q_0).
\]
After a fixed affine shear and translation we may arrange that the line at \(q_0\) is \(L(0,0)\); this changes none of the arguments about convexity, tangency, or rank below. Choose any contact \((0,z_i)\) with set \(K_i\).

**Lemma 2.** At every such contact,
\[
\operatorname{rank}(A+z_iB)\le1.
\tag{12}
\]

**Proof for affine dimension three.** Suppose instead that the map \(A+z_iB\) is onto \(\mathbb R^2\). Choose an interior ball \(B(c,r)\subset K_i\), write \(c=(w,c_z)\), and select \(h\in\mathbb R^2\) with \((A+z_iB)h=w\).

The density-one property implies that there are \(q_j\in E\), \(\tau_j\downarrow0\), such that
\(q_j=q_0+\tau_jh+o(\tau_j)\). One way to see this is that \(\operatorname{dist}(q_0+\tau h,E)=o(\tau)\); otherwise a ball of radius proportional to \(\tau\), missing \(E\), would contradict density one at \(q_0\).

On the line \(F(q_j)\), take height
\(z_i+\tau_j(c_z-z_i)\). Differentiability gives its transverse coordinates as \(\tau_jw+o(\tau_j)\). Convexity implies that \(K_i\) contains the open ball of radius \(\tau_jr\), centered at
\[
(1-\tau_j)(0,z_i)+\tau_jc.
\]
Our point on \(F(q_j)\) lies inside that ball for large \(j\). This contradicts tangency.

**Proof for affine dimension two.** Let \(H=\operatorname{aff}K_i\). The retained line is transverse to \(H\). Take a relative interior disk of radius \(r\), centered at \(c=(w,c_z)\), in \(K_i\). If the map in (12) were onto, choose \(h\) and \(q_j\) as above. The intersection of a nearby line with \(H\) depends smoothly on its line coordinates. Its first-order displacement is \(\tau_j(c-(0,z_i))\): the transverse part is \(\tau_jw\), and the height component is uniquely determined by membership in \(H\). Hence the intersection lies inside the relative disk of radius \(\tau_jr\) centered at \((1-\tau_j)(0,z_i)+\tau_jc\), for large \(j\). It is a relative interior point of \(K_i\). The only supporting plane through a relative interior point is \(H\), whereas this line is transverse to \(H\). Again tangency is impossible.

More explicitly, if \(H\) has equation \(N_x\cdot x+N_z(z-z_i)=0\), transversality says \(N_z\ne0\), and its intersection height is
\[
z(q)=\frac{N_zz_i-N_x\cdot u(q)}{N_z+N_x\cdot v(q)}.
\]
Its derivative along \(h\) is \(-N_x\cdot w/N_z=c_z-z_i\), giving the claimed expansion.

**Proof for affine dimension one.** Let the supporting affine line of \(K_i\) be
\((0,z_i)+\lambda(d_x,d_z)\). Since it is not identical to \(L(0,0)\), and intersects it, \(d_x\ne0\). Every \(q\in E\) sufficiently close to \(q_0\) satisfies, at the point of intersection,
\[
\nu(q):=u(q)+z_iv(q)=(d_x-d_zv(q))\lambda(q).
\tag{13}
\]
Dotting with \(d_x\) shows that \(\lambda(q)=O(|u(q)|+|v(q)|)\). If \(n\perp d_x\), (13) gives
\(n\cdot\nu(q)=-d_z(n\cdot v(q))\lambda(q)\). Along the density sequences this is \(O(\tau_j^2)\), so
\(n\cdot(A+z_iB)h=0\) for every \(h\). Thus the image lies in the one-dimensional space spanned by \(d_x\).

**Proof for affine dimension zero.** The contact is a fixed point. Every \(q\in E\) satisfies \(u(q)+z_iv(q)=0\), so differentiation along the density sequences gives \(A+z_iB=0\). \(\square\)

## 6. Three contacts annihilate the swept Jacobian

The three contact heights \(z_1,z_2,z_3\) are distinct because the three sets are pairwise disjoint. The polynomial
\[
P(z)=\det(A+zB)
\]
has degree at most two. By Lemma 2 it has these three distinct roots, and therefore
\[
\det(A+zB)=0\quad\text{for every real }z.
\tag{14}
\]

The map sweeping the line family is
\[
G(q,z)=(u(q)+zv(q),z).
\tag{15}
\]
It is Lipschitz on each bounded parameter patch with bounded \(z\). At the differentiability points just considered,
\[
\det DG(q_0,z)=
\det\begin{pmatrix}Du(q_0)+zDv(q_0)&v(q_0)\\0\quad0&1\end{pmatrix}
=\det(A+zB)=0.
\tag{16}
\]
The exceptional parameters \(q\) form a two-dimensional null set, whose product with a bounded height interval is a three-dimensional null set. The area formula for Lipschitz maps \(\mathbb R^3\to\mathbb R^3\) now gives
\[
\mathcal L^3\bigl(G(E\times[-M,M])\bigr)=0
\quad(M<\infty),
\tag{17}
\]
first on bounded patches and then by countable union. Equivalently, the measure of the image is bounded by the integral of the absolute Jacobian, which vanishes. This includes any part of \(E\) itself having two-dimensional measure zero.

Thus the tritangent portion of any Lipschitz two-parameter line family sweeps a null set.

## 7. Covering every dimensional case

Remove first the lines contained in the affine plane of any two-dimensional \(K_i\), and the lines identical to the affine line of any one-dimensional \(K_i\). Their entire swept loci lie in finitely many planes or lines.

There are three remaining cases.

1. **At least two sets have affine dimension at least two.** Apply Lemma 1 to those two sets. Restrict each chart to the tritangent parameters and apply (17).
2. **At least one set is a point.** All common lines pass through that point. Such lines have smooth two-parameter charts, obtained from ordinary local charts for their direction. Apply (17), including the zero-dimensional case of Lemma 2.
3. **No set is a point, and at most one set has dimension at least two.** At least two sets are compact intervals in affine lines. Parameterize their points as \(a(s)\) and \(b(t)\). Their distance is bounded below by a positive constant. The line through \(a(s)\) and \(b(t)\) therefore depends Lipschitz-continuously on \((s,t)\) on suitable bounded coordinate charts in line space. These charts cover all common transversals to the two intervals, and in particular all common tangents to the three sets. The parameter domains can be enlarged locally to open subsets of \(\mathbb R^2\), with the tritangent subset still selected by the closed tangency conditions. Apply (17).

Countable unions of the null sets from these charts, together with the finitely many discarded planes and lines, give a null set containing the compact-case locus. Section 2 yields the statement for arbitrary convex sets. \(\square\)

## 8. Dependencies, checks, and novelty limits

The proof uses only compactness and elementary convexity, a contraction argument, differentiability almost everywhere of Lipschitz maps, the Lebesgue density theorem, and the equal-dimensional area formula. It uses neither a general smooth-transversality theorem nor Sard's theorem for nonsmooth functions.

The main substantive lemma requiring adversarial scrutiny is Lemma 1: localization to countably many convex caps, the signed support-gap estimates, and the resulting Lipschitz chart cover. Lemma 2 is deliberately stated at density points of the tritangent parameter subset, so it does not assume that this subset contains an open set or smooth curve.

The determinant identity and the quantitative constants are subject to modest exact checks in `verify.py`. Such checks do not replace the analytic proof.

No later resolution was located in the limited primary-source searches performed on 2026-09-30, including the proposer's current publication list, the thesis, and searches for the exact conjecture, common tritangents, visual-event surfaces, and measure zero. This negative search does not establish priority. The area formula and all general measure-theoretic tools are standard; the intended contribution is their application through the cap-chart and three-contact arguments above.

### References

- Xavier Goaoc, “Union of lines tangent to three convex sets in R3,” in [Discrete Geometry, Oberwolfach Report 44/2008](https://ems.press/content/serial-article-files/46191), p. 2552, Conjectures 3 and 4. DOI: [10.4171/OWR/2008/44](https://doi.org/10.4171/OWR/2008/44).
- Julien Demouth, [*Événements visuels de convexes et limites d'ombres*](https://theses.hal.science/tel-00342717/document), doctoral thesis, Université Nancy 2, 2008, chapter 4, especially pp. 48, 51, and 61–66.
- J. Demouth and X. Goaoc, *Topological changes in the apparent contour of convex sets*, manuscript, 2008, as cited by the OWR source; the thesis provides the inspected underlying arguments.
- Herbert Federer, *Geometric Measure Theory*, Springer, 1969, §3.2.3 (area formula).
- Lawrence C. Evans and Ronald F. Gariepy, *Measure Theory and Fine Properties of Functions*, revised edition, CRC Press, 2015, chapters 1 and 3 (density, Rademacher theorem, area formula).

- Leon Simon, [*Introduction to Geometric Measure Theory*, 2018 NTU notes](https://math.stanford.edu/~lms/ntu-gmt-text.pdf), Ch.1 Corollary3.10 (density), Ch.2 Theorem1.4 (Rademacher) and Theorem3.3 (area formula), printed pp.18,45,57–58. Full hypotheses independently inspected; locally Lipschitz open-domain area formula permits arbitrary measurable subsets and multiplicity.
