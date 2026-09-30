# A credited counterexample for the four AIM ridge directions

Status: complete negative answer to the recovered AIM Problem 22, as a self-contained consequence of a published 2011 nonadditivity example. Separate adversarial review is pending. One substantive source-validation/certificate family was used. This is **credited known-result recovery**, with an explicit robust smooth-body corollary, not a claim of historical novelty or human peer review.

## 1. Exact target and attribution

The official AIM list *Fourier analytic methods in convex geometry*, printed p.6, Problem 22 by A. Daurat and R. Gardner, asks whether every planar convex body is a nonnegative superlevel set of a sum of four measurable ridge functions with the fixed linear forms
\[
\ell_1(x,y)=x,\quad\ell_2(x,y)=y,\quad
\ell_3(x,y)=2x+y,\quad\ell_4(x,y)=-x+2y.
\tag{1}
\]
We keep **arbitrary measurable finite-valued profiles** \(g_i:\mathbb R\to\mathbb R\), not only polynomials or continuous functions. The requested literal representation is
\[
K=\{(x,y):S(x,y)\ge0\},\qquad S=\sum_{i=1}^4g_i\circ\ell_i.
\tag{2}
\]
The conclusion below also excludes equality modulo planar null sets. The unrelated slab question begins at Problem 23 and is not part of this target. Normalizing the nonunit vectors in (1) merely reparametrizes the profiles.

**Prior result.** Gritzmann, Langfeld and Wiegelmann, *Uniqueness in discrete tomography: Three remarks and a corollary*, SIAM J. Discrete Math. 25(2011),1589–1599, Remark 2.3 on p.1593 and Figure 1 on p.1594, prove that the lattice-convex set
\[
F_{2,4}=\mathbb Z^2\cap\operatorname{conv}\{(2,4),(-4,2),(-2,-4),(4,-2)\}
\]
is not additive for exactly the direction set \(\{(1,0),(2,1),(0,1),(-1,2)\}\). They supply a different finite set with the same four X-rays. This published example already implies a negative answer to the literal AIM question. The source calls its vectors line directions; our profiles are indexed by normals. There is no mismatch here: taking perpendiculars simply permutes these four unoriented directions.

The imported dataset report gave low-degree polynomial completeness, ellipse and strip constructions, and a finite switching criterion, but did not find a convex-body switching certificate. Those are credited prior calculations, not repeated as discoveries. The missing certificate is available from the 2011 example. We reconstruct its obstruction explicitly below so no claim depends on reading point coordinates from a picture, trusting a numerical optimizer, or imposing additional regularity on the profiles.

## 2. The exact sixteen-point certificate

Define two disjoint eight-point sets
\[
\begin{aligned}
P=\{&(-4,2),(-3,-1),(-2,-4),(-1,3),\\
    &(1,-3),(2,4),(3,1),(4,-2)\},\\
N=\{&(-4,1),(-3,-2),(-2,3),(-1,-4),\\
    &(1,4),(2,-3),(3,2),(4,-1)\}.
\end{aligned}
\tag{3}
\]
For each of the four forms, the multisets of values on \(P\) and \(N\) are identical. Their sorted values are

| form | values on either eight-point set |
|---|---|
| x | −4, −3, −2, −1, 1, 2, 3, 4 |
| y | −4, −3, −2, −1, 1, 2, 3, 4 |
| 2x+y | −8, −7, −6, −1, 1, 6, 7, 8 |
| −x+2y | −8, −7, −6, −1, 1, 6, 7, 8 |

It follows, by regrouping finite sums, that for **every** choice of finite-valued functions \(g_i\), even without measurability,
\[
\sum_{p\in P}S(p)=\sum_{n\in N}S(n).
\tag{4}
\]
The same identity holds after translating all sixteen points by any common vector \(h\), since \(\ell_i(z+h)=\ell_i(z)+\ell_i(h)\).

Put \(u=x-3y\), \(v=3x+y\), and define the rotated square
\[
K_0=\{(x,y):|u|\le10,\ |v|\le10\}.
\tag{5}
\]
The coordinate change has determinant 10. Its inverse sends the four corners \((\pm10,\pm10)\) to the four vertices in Section 1. Every point of \(P\) lies in \(K_0\). For every point of \(N\), one of \(|u|,|v|\) equals11, so every such point lies outside \(K_0\).

If (2) held for \(K_0\), each term in the left side of (4) would be nonnegative, and every term on the right would be strictly negative. This is impossible. Thus \(K_0\) is a convex-body counterexample to the exact literal question. No integral, continuity, boundedness, differentiability, or polynomial restriction on the profiles was used.

For an additional check against the discrete source, \(F=K_0\cap\mathbb Z^2\) has 45 points, and
\[
F'=(F\setminus P)\cup N
\]
has the same cardinality and the same four discrete marginals as \(F\), but is different. This is an explicit certificate of the published shape's nonadditivity; no novelty is claimed for the underlying example.

## 3. An explicit analytic, positively curved counterexample

The boundary of the square is not essential. Define
\[
\Phi(x,y)=(x-3y)^8+(3x+y)^8+(x-3y)^2+(3x+y)^2,
\]
\[
K_*:=\{(x,y):\Phi(x,y)\le210\,000\,000\}.
\tag{6}
\]
This is a compact centrally symmetric convex body with real-analytic boundary and strictly positive curvature at every boundary point.

To verify these regularity claims, let
\[
A=\begin{pmatrix}1&-3\\3&1\end{pmatrix},\qquad(u,v)^T=A(x,y)^T.
\]
Then \(A^TA=10I\), and
\[
\nabla^2\Phi=A^T\begin{pmatrix}56u^6+2&0\\0&56v^6+2\end{pmatrix}A\succeq20I.
\]
Thus \(\Phi\) is strongly convex. It is coercive, and its only critical point is the origin: both \(8u^7+2u\) and \(8v^7+2v\) vanish only at zero. The positive level in (6) has nonempty interior and nonvanishing gradient. The analytic implicit-function theorem gives an analytic boundary. Its second fundamental form on a tangent vector is the positive Hessian form divided by \(\|\nabla\Phi\|\), so its curvature is everywhere positive.

At the certificate points, exact integer evaluation gives
\[
\Phi(P)\subset\{100\,000\,100,200\,000\,200\},\qquad
\Phi(N)\subset\{214\,365\,572,220\,123\,852\}.
\tag{7}
\]
Hence all positive points are strictly inside \(K_*\) and all negative points are strictly outside. Equation (4) again excludes (2), now for the analytic body (6).

This smooth-body corollary is derived here from the credited finite obstruction. We do not assert that it is historically new.

## 4. The obstruction survives arbitrary null-set changes

**Theorem.** There are no measurable finite-valued profiles \(g_1,\ldots,g_4\) such that
\[
K_*\mathbin{\triangle}\{S\ge0\}
\]
has planar Lebesgue measure zero.

**Proof.** All sign separations in (7) persist under small common translations. An explicit uniform choice is
\[
\|h\|_\infty<1/1000.
\tag{8}
\]
Indeed, each of \(u,v\) changes by at most \(4/1000\). Positive points have \(|u|,|v|\le10\), so
\[
\Phi(p+h)\le2(2501/250)^8+2(2501/250)^2<210\,000\,000.
\tag{9}
\]
At every negative point, one transformed coordinate has absolute value 11; consequently
\[
\Phi(n+h)\ge(2749/250)^8>210\,000\,000.
\tag{10}
\]
These are exact rational inequalities.

Suppose the stated symmetric difference were contained in a measurable null set \(Z\). For each of the finitely many points \(z\in P\cup N\), the set of shifts \(h\) with \(z+h\in Z\) is null. Their finite union cannot cover the open square (8). Choose a shift outside that union. At all eight translated positive points, \(S\ge0\); at all eight translated negative points, \(S<0\). The translated version of (4) is a contradiction. QED.

This argument needs no local integrability or essential boundedness of any profile. In particular, it does not try to integrate an arbitrary measurable score against a smoothed switching measure. Measurability only makes the almost-everywhere formulation meaningful, and the contradiction remains a finite sum at one admissible translation.

## 5. A concrete measurable competitor with the same X-rays

The same margin gives a direct geometric interpretation. Let \(B=(-1/1000,1/1000)^2\), and replace the eight interior patches by the eight exterior patches:
\[
E=\left(K_*\setminus\bigcup_{p\in P}(p+B)\right)
\cup\bigcup_{n\in N}(n+B).
\tag{11}
\]
All sixteen patches are pairwise disjoint, since their centers are distinct integer lattice points. By (9)–(10), every positive patch lies inside \(K_*\), and every negative patch lies outside. Thus (11) is bounded and measurable, differs from \(K_*\) by positive area, and its indicator satisfies the exact finite identity
\[
\mathbf1_E=\mathbf1_{K_*}-\sum_{p\in P}\mathbf1_{p+B}
+\sum_{n\in N}\mathbf1_{n+B}.
\]
For each \(i\), the line-integral X-ray of a translated patch in direction \(\ker\ell_i\) depends on its center only through \(\ell_i\) of that center. The balanced multisets therefore cancel all patch contributions on every line. Consequently \(E\) and \(K_*\) have identical X-rays in all four directions. The kernels of the four forms permute the original four unoriented AIM directions.

There is no contradiction with uniqueness **among convex bodies** in the problem's background. The competitor (11) has holes and added exterior patches and is not convex. Nor is finite atomic equality alone confused with equality of continuous X-rays: the common patch translation explicitly supplies the latter.

## 6. Provenance and verification

The earlier imported ridge-spanning and switching lemmas are preserved as prior work. They are not attributed to this attempt. The key published source omitted from that report is the 2011 paper above. Its complete primary 11-page PDF was retrieved from the Technical University of Munich repository; the relevant Section 2, Remark 2.3 and Figure 1 were read, and the direction tuple and square definition were visually verified.

The certificate in (3) was reconstructed by one small linear feasibility calculation on the 81-point grid \([-4,4]^2\cap\mathbb Z^2\). Its floating-point output was immediately converted to exact rational weights and checked; after scaling the weights are precisely eight plus ones and eight minus ones. The final proof and standard-library verifier do not require that optimizer and do not use its success as evidence in place of the certificate.

The exact checker verifies all four multisets, the45-point lattice-square comparison, the integer values (7), the rational uniform bounds (9)–(10), the invertible coordinate map and Hessian lower-bound algebra. Additional rational translation tests are finite controls only: the all-shifts and almost-everywhere statements are proved in Sections3–4.

The recovered original question is fully answered negatively. The recommended status is a **credited known resolution**, with one validation/certificate approach recorded, rather than a newly solved open problem. The smooth and almost-everywhere corollaries are explicit consequences of the certificate, with no independent historical-priority claim.

## References

1. AIM, [Fourier analytic methods in convex geometry: problem list](https://aimath.org/WWN/fourierconvex/fourierconvex.pdf), Problem 22, printed p.6. Full source obtained; adjacent Problem 23 excluded.
2. P. Gritzmann, B. Langfeld and M. Wiegelmann, [Uniqueness in discrete tomography: Three remarks and a corollary](https://mediatum.ub.tum.de/doc/1370776/document.pdf), SIAM J. Discrete Math. 25(4)(2011),1589–1599, [DOI10.1137/100803262](https://doi.org/10.1137/100803262). Remark 2.3 and Figure 1 are the decisive credited prior result. Third-party PDF is not republished in this repository.
3. P. Dulio and C. Peri, [Intersecting polytopes and tomographic reconstructions](https://www.mate.polimi.it/biblioteca/add/quaderni/qdd108.pdf), QDD 108(2011), introduction and Section2. Retrieved for definitions and the distinction among additivity, inscribability and uniqueness; its earlier discussion of the conjecture does not supersede the subsequent November 2011 counterexample.
4. The pinned upstream report for AIM-CONVEX_GEOMETRY-0044, archived separately in this attempt, supplies the already-proved low-degree special cases and finite zero-marginal criterion. It had not located the convex counterexample.
