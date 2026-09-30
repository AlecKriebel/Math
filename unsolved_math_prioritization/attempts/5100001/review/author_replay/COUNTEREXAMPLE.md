# A primitive four-period counterexample to the printed invariant k107

**Status:** complete counterexample candidate; separate adversarial review pending. Two approach families recorded. AI-assisted research draft, not human peer reviewed. Historical priority is unestablished.

## 1. The exact source statement is false

For the ellipse

\[
E:\quad \frac{x^2}{16}+\frac{y^2}{9}=1
\]

and its fixed confocal elliptical caustic

\[
C:\quad \frac{x^2}{256/25}+\frac{y^2}{81/25}=1,
\tag{1}
\]

two primitive, convex, four-period billiard orbits in the same Poncelet family give the following different values of the printed quantity:

\[
\boxed{\quad
\left(\frac{A'}A\prod_{i=1}^4\sin\frac{\theta_i}2\right)_{\!D}
=\frac{288}{625}
\ne
\frac{625}{1152}
=\left(\frac{A'}A\prod_{i=1}^4\sin\frac{\theta_i}2\right)_{\!R}.
\quad}
\tag{2}
\]

The vertices, in counterclockwise order, are

\[
\begin{aligned}
D&=((4,0),(0,3),(-4,0),(0,-3)),\\
R&=((16/5,9/5),(-16/5,9/5),(-16/5,-9/5),(16/5,-9/5)).
\end{aligned}
\tag{3}
\]

Thus the universal assertion k107 for N congruent to zero modulo four is refuted already at N=4. No repeated traversal, hyperbolic caustic, zero area, singular tangent intersection or self-intersection is involved.

### Source conventions

Reznik--Garcia--Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11, Figure 1 and Sections 2--3.1, define P' by intersecting consecutive tangent lines to the **outer ellipse at the orbit vertices**, A and A' as signed polygon areas, and theta_i as the angles of the original orbit. Its Table 2, printed p.5, lists

\[
k_{103}=A'/A,\qquad k_{105}=\prod_i\sin(\theta_i/2),\qquad
k_{107}=k_{103}k_{105},\qquad N\equiv0\pmod4.
\]

The published companion, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341--355, Table 2 on p.345, prints exactly the same entry. Both table pages were visually checked. The dataset extraction is faithful to that printed entry. Both polygons in (3) are convex and positively oriented, so their signed areas equal their ordinary positive areas, and the half-angle sines are unambiguously positive.

## 2. A general pair of four-period orbits

The example works for every a>b>0. Put

\[
s=\sqrt{a^2+b^2},\qquad
\lambda=\frac{a^2b^2}{a^2+b^2},
\]

and fix

\[
E:\frac{x^2}{a^2}+\frac{y^2}{b^2}=1,
\qquad
C:\frac{x^2}{a^4/s^2}+\frac{y^2}{b^4/s^2}=1.
\tag{4}
\]

The two ellipses are confocal because

\[
a^2-a^4/s^2=b^2-b^4/s^2=\lambda,
\]

and 0<lambda<b², so C is a strictly nested, nondegenerate ellipse.

Consider the axis diamond D with vertices (a,0),(0,b),(-a,0),(0,-b), and the rectangle R with successive vertices (a²/s,b²/s),(-a²/s,b²/s),(-a²/s,-b²/s),(a²/s,-b²/s).

All eight displayed vertices lie on E. The diamond edge from (a,0) to (0,b) has line x/a+y/b=1. Its support value on C is

\[
\sqrt{\frac{a^4/s^2}{a^2}+\frac{b^4/s^2}{b^2}}=1,
\]

so it is tangent to C. The contact point is (a³/s²,b³/s²), lying strictly inside that edge. Reflections in the coordinate axes verify the other three edges. The rectangle's sides are x=±a²/s and y=±b²/s, exactly the four axis tangents of C, with contact points in the side interiors.

The billiard reflection law can also be checked directly, without merely inferring it from tangency. At each diamond vertex, the two incident directions are interchanged by reflection in the corresponding coordinate axis, which is the normal line to E there. At a rectangle vertex (epsilon a²/s,eta b²/s), the ellipse normal is parallel to (epsilon,eta); this bisects its right angle and interchanges the incident horizontal and vertical rays. Hence both polygons are genuine billiard orbits. They each have four distinct vertices and no earlier return to the initial oriented state, so their least period is four.

## 3. They belong to one continuous family with the same caustic

For clarity, the common family need not be inferred from a numerical caustic computation. It has an explicit parametrization. For c=cos t and d=sin t set

\[
\Delta=\sqrt{a^4d^2+b^4c^2},\qquad
P=(ac,bd),\qquad
Q=\left(-\frac{a^3d}{\Delta},\frac{b^3c}{\Delta}\right).
\tag{5}
\]

The normalized map on the unit circle is

\[
T(c,d)=\frac{(-a^2d,b^2c)}{\sqrt{a^4d^2+b^4c^2}}.
\]

Its square is minus the identity: at T(c,d) the new denominator is a²b²/Delta, giving T²(c,d)=(-c,-d). Thus (P,Q,-P,-Q) varies continuously through primitive quadrilaterals. Indeed

\[
\det(P,Q)=\frac{ab(a^2d^2+b^2c^2)}\Delta>0,
\]

so all four vertices are distinct and are traversed counterclockwise. The map T is orientation preserving because it is induced by an invertible linear map of positive determinant followed by radial normalization.

Every edge is tangent to the fixed C in (4). Here is an explicit calculation for PQ; the other edges follow by applying T. Let S=a²+b² and U=a²d²+b²c². A normal to PQ is

\[
n=\bigl(b(d-b^2c/\Delta),-a(c+a^2d/\Delta)\bigr),
\quad n\cdot P=-abU/\Delta.
\]

The support-square identity for C is

\[
\begin{aligned}
\frac{a^4}{S}n_x^2+\frac{b^4}{S}n_y^2
 &=\frac{a^2b^2}{S\Delta^2}
 \left[a^2(\Delta d-b^2c)^2+b^2(\Delta c+a^2d)^2\right]\\
 &=\frac{a^2b^2}{S\Delta^2}U(\Delta^2+a^2b^2)
 =\frac{a^2b^2U^2}{\Delta^2}
 =(n\cdot P)^2,
\end{aligned}
\]

where Delta²+a²b²=S U. This is precisely tangency of the line PQ to C.

For completeness, the usual confocal tangent construction gives the billiard reflection law along the whole family. If v is a unit direction along a line through P=(x,y) on E, its tangency to C is equivalent to

\[
(P\mathbin\times v)^2=(a^2-\lambda)v_y^2+(b^2-\lambda)v_x^2,
\]

which, using x²/a²+y²/b²=1, reduces to

\[
\left(\frac{xv_x}{a^2}+\frac{yv_y}{b^2}\right)^2
 =\frac\lambda{a^2b^2}.
\tag{6}
\]

Consequently the two inward unit directions of the two distinct tangent chords have the same strictly negative projection on the outward normal, and opposite tangential projections. They are symmetric about the normal line. The incoming ray is the reverse of one of these inward directions; reflection therefore gives the other outgoing ray. Thus the family in (5) is a family of billiard orbits, not merely inscribed quadrilaterals.

At t=0 it is D. At c=a/s,d=b/s, its consecutive vertices are precisely those of R. This explicitly establishes that the two examples lie in the same oriented Poncelet family for the same fixed confocal caustic.

## 4. Areas and half-angle products

For D, the orbit area is A_D=2ab. The tangents to E at its vertices are x=±a,y=±b, so D' is the rectangle with area A'_D=4ab. Hence A'_D/A_D=2.

At (a,0), the two incident vectors toward neighboring vertices are (-a,b) and (-a,-b), each of length s. Their angle has cosine (a²-b²)/s², and hence its half-angle sine is b/s. At (0,b) that sine is a/s. Opposite angles agree, so

\[
\prod_{i=1}^4\sin(\theta_i(D)/2)=\frac{a^2b^2}{s^4},
\qquad
k_{107}(D)=\frac{2a^2b^2}{(a^2+b^2)^2}.
\tag{7}
\]

For R, all internal angles are right angles, and their half-angle product is 1/4. Its area is A_R=4a²b²/s². At (epsilon a²/s,eta b²/s), the tangent line to E is epsilon x+eta y=s. Thus R' has vertices (s,0),(0,s),(-s,0),(0,-s) and area 2s². Therefore

\[
\frac{A'_R}{A_R}=\frac{s^4}{2a^2b^2},
\qquad
k_{107}(R)=\frac{(a^2+b^2)^2}{8a^2b^2}.
\tag{8}
\]

Since (a²+b²)²>4a²b² when a>b, equations (7)--(8) give

\[
k_{107}(D)<\tfrac12<k_{107}(R).
\]

The values can agree only in the excluded circular limit a=b. Substitution a=4,b=3 gives (1)--(3). Their exact difference is 58849/720000, which is strictly positive.

## 5. Cross-checks, prior results and claim boundary

Both displayed orbits have perimeter 4s and Joachimsthal constant 1/s. They share the same caustic by the direct support calculation. Their area products agree:

\[
A_DA'_D=A_RA'_R=8a^2b^2.
\]

This agrees with the established even-period area-product result of Chavez-Caliz, Theorem 6, rather than contradicting it. The half-angle product theorem of Akopyan--Schwartz--Tabachnikov, Corollary 6.4, is restricted to odd periods and supplies no constancy here.

For these two four-period representatives the **quotient** k103/k105 agrees, taking the value 2s⁴/(a²b²). This observation can help diagnose a possible product/quotient or parity error in the table, but is not an all-period corrected invariant theorem. The separately assigned k108 statement concerns N congruent to two modulo four and is a different target. This note does not rely on any result about k108.

Earlier campaign results k603 and k405 concern focal antipedal distances and centroids, respectively. Their source/caustic conventions were consulted, but no theorem from either is a dependency of this counterexample. All geometry needed for the counterexample and its continuous family is proved above. The imported upstream report only gave open triage and component-invariant references; it did not contain this calculation or an identified earlier Alec/campaign attempt.

The accompanying standard-library verifier checks the exact rational example, ordinary reflection law, tangency, positive signed areas and half-angle products. Additional exact quadratic-field controls check the continuous family away from its symmetric representatives. These are diagnostics supporting the algebraic proof, not approximate orbit simulations.

This resolves the literal printed k107 assertion by counterexample. It does not assert that no corrected invariant exists, identify the authors' intended replacement, or claim that this source-table issue was previously unknown. No external author contact was made.

## Sources

1. D. Reznik, R. Garcia and J. Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11, 29 October 2020, Figure 1, Sections 2--3.1 and Table 2 p.5. [Primary preprint](https://arxiv.org/abs/2004.12497v11).
2. The same authors, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Math. J. 7 (2021), 341--355, Figure 1 p.342, definitions pp.343--344, Table 2 p.345. [Full published primary PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf).
3. A. C. Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Arnold Math. J. 7 (2021), 91--106, Theorem 6 and proof pp.103--104. [Full published primary PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf). Related known area-product theorem; not needed as a proof dependency.
4. A. Akopyan, R. Schwartz and S. Tabachnikov, *Billiards in ellipses revisited*, European J. Math. 8 (2022), 1313--1327, Corollary 6.4 p.1324. [Full published primary PDF](https://par.nsf.gov/servlets/purl/10408491). Related odd-period half-angle theorem; not applicable to the even-period target.
