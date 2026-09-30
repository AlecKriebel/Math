# Curvature cancellation on a patch without mirrored triangle pairs

**30006576 / OWR-14299907-001. Scoped partial result; the original mesh characterization remains unresolved, 1/5 approaches.** No priority or human peer-review claim. Independent review is pending.

We give an exact leading-moment criterion for one extra order in the integrated Gaussian-curvature error on a shrinking graph patch. For every even interpolation degree, an odd rotational fan satisfies the criterion although it contains no centrally mirrored triangle pair of the kind used in the source. This is a local mechanism and a conditional patchwise estimate, not a characterization of all global surface meshes or an explanation of every refinement experiment.

## 1. Original setting and a newer primary source

The exact questions are in Simon Praetorius's contribution, joint with Hanne Hardering and Gentian Zavalani, [OWR5/2026, printed312–313](https://ems.press/content/serial-article-files/53599). They concern mesh structure behind parity-dependent *weighted geometric consistency*, including the Gaussian-curvature contribution to surface Stokes error estimates. They do not assert improved pointwise curvature accuracy. The report asks which internal structure is necessary and how to account for observed cases without an explicitly visible mirrored-pair structure.

The authors' subsequent full preprint, [*Odd behaviour of even geometries*, arXiv2607.29466v1,31July2026](https://arxiv.org/abs/2607.29466v1), supplies precise sufficient hypotheses and proofs. Its Definition2.7 uses **central reflection about a shared vertex**: two triangles intersect only in that vertex and their affine reference maps differ by a minus sign about it. This is not reflection across a common edge. Definitions2.7–2.10 impose such a decomposition up to a controlled boundary strip. Theorem3.2 and Corollary3.3 establish parity-dependent weighted interpolation estimates; Corollary4.4 gives the order-h^k Gaussian-curvature bilinear estimate for even k>=2. AppendixB explicitly leaves its projected-refinement and newest-vertex-bisection experiments outside the main theorem's direct coverage.

Its geometry is obtained by standard degree-k Lagrange interpolation of fixed smooth parametrizations on a reference triangulation. Its parametrization lift and closest-point lift are distinct. Below we use only graph parametrizations and the **parametrization lift**. Gaussian curvature on the discrete graph is computed separately on each triangle; no distributional curvature along edges or vertices is included. This matches the elementwise curvature convention relevant to the source. The later paper is credited for the general cancellation mechanism and the proved symmetric-mesh estimates; the argument below is a self-contained restricted calculation.

## 2. Exact local criterion

Let P be a fixed bounded connected Lipschitz polygon containing 0 in its closure, with a finite conforming triangulation \(\mathcal T\) into nondegenerate triangles. Fix an integer k>=2. On each triangle let I_k be interpolation at the standard barycentric Lagrange nodes of degree k. The resulting interpolant is continuous across edges. All second derivatives below are taken elementwise.

For a homogeneous polynomial p of degree k+1, define the symmetric matrix

\[
\mathcal M_{k,\mathcal T}(p)
=\sum_{T\in\mathcal T}\int_T D^2(I_kp-p)\,dx.
\tag{1}
\]

This is a finite-dimensional linear map, readily computed from polynomial moments. Let \(I_{k,h}\) be the same interpolation on the scaled triangulation h\(\mathcal T\) of hP, for h>0.

For a function f that is C^{k+2} on a fixed neighborhood of 0 containing hP for all sufficiently small h, write

\[
Q(f)=\frac{\det D^2f}{(1+|\nabla f|^2)^{3/2}}.
\tag{2}
\]

This is Gaussian curvature times graph area density relative to dx: K_f dA_f=Q(f)dx. Thus integrating \(Q(I_{k,h}f)-Q(f)\) compares curvature integrals under the lift \((x,I_{k,h}f(x))\mapsto(x,f(x))\).

**Theorem 1.** The following are equivalent:

1. \(\mathcal M_{k,\mathcal T}(p)=0\) for every homogeneous polynomial p of degree k+1.
2. For every such smooth f,
   \[
   \int_{hP}\bigl[Q(I_{k,h}f)-Q(f)\bigr]dx=O_f(h^{k+2})\quad(h\downarrow0).
   \tag{3}
   \]

Without the cancellation condition, the standard integrated bound is O(h^{k+1}). The factor h² from the shrinking patch area is included in both exponents. The theorem asserts a local necessary-and-sufficient condition for **all graph jets**, not necessity of a patch decomposition for a global surface estimate.

**Proof.** Put a=\(\nabla f(0)\), H=\(D^2f(0)\), and let p be the homogeneous degree-(k+1) part of the Taylor polynomial of f at 0. Polynomial reproduction and affine scaling give, uniformly on the elements,

\[
\nabla(I_{k,h}f-f)=O(h^k),\qquad
D^2(I_{k,h}f-f)(hy)=h^{k-1}D^2(I_kp-p)(y)+O(h^k).
\tag{4}
\]

Here and below constants may depend on the fixed patch, k, and a bounded C^{k+2} norm of f, but not on h. The nodal Taylor remainder is O(h^{k+2}); differentiating its interpolant twice gives O(h^k), which justifies (4) also for the interpolated remainder.

For symmetric 2-by-2 matrices, the linear term of det(H+E)-det H is cof(H):E. The gradients differ by O(h^k); replacing the smooth gradient and Hessian coefficients by their values at 0 incurs another O(h) times the leading Hessian error. The term quadratic in that Hessian error is O(h^{2k-2}), which is O(h^k) for k>=2. Consequently

\[
Q(I_{k,h}f)(hy)-Q(f)(hy)
=h^{k-1}(1+|a|^2)^{-3/2}\operatorname{cof}(H):D^2(I_kp-p)(y)+O(h^k).
\tag{5}
\]

Integration yields

\[
\int_{hP}[Q(I_{k,h}f)-Q(f)]dx
=h^{k+1}(1+|a|^2)^{-3/2}\operatorname{cof}(H):\mathcal M_{k,\mathcal T}(p)+O(h^{k+2}).
\tag{6}
\]

This proves sufficiency. Conversely, if a real homogeneous p has nonzero moment M, choose H=cof(M), a=0 and \(f(x)=\tfrac12x^THx+p(x)\). Since k+1>=3, these are independent Taylor coefficients. In dimension two cof(cof M)=M, so the coefficient in (6) is M:M>0. Equation (3) then fails. Complex polynomials, when useful for calculation, are simply the complexification of this real linear criterion. ∎

**Weighted form.** If condition1 holds, then for all \(\varphi\in W^{1,1}(hP)\),

\[
\left|\int_{hP}[Q(I_{k,h}f)-Q(f)]\varphi\,dx\right|
\le C h^k\bigl(\|\varphi\|_{L^1(hP)}+\|\nabla\varphi\|_{L^1(hP)}\bigr).
\tag{7}
\]

Indeed the leading scalar function in (5) has mean zero and L-infinity norm O(h^{k-1}). Subtract the mean of \(\varphi\), then use the scaled L¹ Poincaré inequality on the connected Lipschitz polygon. Its remainder is bounded by Ch^k\(\|\varphi\|_1\). No compactness argument on varying mesh families is needed for this fixed-patch statement.

## 3. Odd rotational fans satisfy the criterion for every even degree

Fix even k>=2 and an **odd** integer q>k+3; for example q=k+5. Identify the plane with the complex numbers and set \(\zeta=e^{2\pi i/q}\). Let P be the regular q-gon with vertices \(1,\zeta,\ldots,\zeta^{q-1}\), and triangulate it by

\[
T_j=\operatorname{conv}\{0,\zeta^j,\zeta^{j+1}\},\qquad 0\le j<q.
\tag{8}
\]

This is a fixed conforming shape-regular fan, with constants allowed to depend on q.

**Theorem 2.** This fan has \(\mathcal M_{k,\mathcal T}=0\). It contains no symmetric triangle pair in the sense of the source's Definition2.7.

**Proof.** It suffices to use the complex homogeneous basis \(p(z,\bar z)=z^a\bar z^b\), a+b=k+1. Let \(\ell=a-b\), which is odd and satisfies |ell|<=k+1. Standard Lagrange interpolation commutes with rotation because its barycentric nodes do. If \(e_j=(I_kp-p)|_{T_j}\), then

\[
e_j(\zeta^j z)=\zeta^{j\ell}e_0(z).
\]

For r=0,1,2, the Wirtinger derivatives transform as

\[
(\partial_z^r\partial_{\bar z}^{2-r}e_j)(\zeta^jz)
=\zeta^{j(\ell+2-2r)}(\partial_z^r\partial_{\bar z}^{2-r}e_0)(z).
\tag{9}
\]

Rotation preserves area. Each exponent \(\ell+2-2r\) is odd, nonzero, and has absolute value at most k+3<q. Its sum over the q rotations is therefore zero. The three second Wirtinger derivatives span the three entries of the complexified real Hessian, so the sum of their integrals vanishes exactly as required in (1).

All triangles contain 0. Adjacent fan triangles share an edge, so cannot be a source pair. Any pair meeting only at one point meets at 0, and central reflection about 0 would require vertices opposite to vertices of the regular q-gon. Odd q has no such opposite vertices. Thus no source pair exists. ∎

This proves that the pair mechanism is not logically necessary for the **local tensor cancellation** in Theorem1. It does not yet disprove any stronger necessity claim about complete fixed-domain refinement families.

## 4. An exact odd-degree diagnostic on the same fan

The cancellation is not a consequence of rotational symmetry alone at every interpolation degree. Keep the odd q-gon fan (q>=7), use degree3 interpolation, and take \(p(x,y)=(x^2+y^2)^2\). Put \(c=\cos(2\pi/q)\) and \(s=\sin(2\pi/q)>0\). On the first triangle \(T_0=\operatorname{conv}\{(0,0),(1,0),(c,s)\}\), direct polynomial interpolation gives

\[
\int_{T_0}\Delta(I_3p-p)\,dxdy=\frac{2(c-1)}{3s}<0.
\tag{10}
\]

Here is an exact reproducible calculation. Use x=r+ct, y=st on the reference triangle r,t>=0, r+t<=1. Interpolate p(r+ct,st) at the degree3 barycentric nodes. For any polynomial g(r,t), the physical Laplacian times s² is

\[
(s^2+c^2)g_{rr}-2cg_{rt}+g_{tt},
\]

and \(\int r^it^jdrdt=i!j!/(i+j+2)!\). Applied to the interpolation error, this gives the general expression

\[
-\frac{(c^2+s^2)((c-1)^2+s^2)}{3s},
\]

which reduces to (10) when c²+s²=1. This calculation uses the full ten degree3 nodes, not a fitted or numerical quadrature rule.

Since p and the Laplacian are rotationally invariant, all q triangles have the same integral. Therefore the trace of the moment matrix is \(2q(c-1)/(3s)\ne0\). For the graph \(f(x,y)=\tfrac12(x^2+y^2)+(x^2+y^2)^2\), equation (6) at k=3 gives a nonzero h⁴ leading curvature-integral error, so it is not O(h⁵). On the same fan, degree2 has the all-jet O(h⁴) estimate of Theorems1–2. This is a local even/odd diagnostic with patch-area normalization included.

For comparison, on the single reference triangle, \(I_2x^3=\tfrac32x^2-\tfrac12x\), and \(\int D_{xx}(I_2x^3-x^3)=1/2\). Individual triangles can retain the leading error; cancellation occurs only after summation over a suitable patch.

## 5. Conditional global consequence and precise remaining gap

Suppose a fixed bounded polygonal graph domain admits conforming triangulations partitioned into disjoint connected patches that are translated, rotated and scaled copies of finitely many fixed patches satisfying (1). Suppose their scale factors are uniformly comparable to h, and f has a uniform C^{k+2} bound on a neighborhood of the domain. The constants in (7) are then uniform. Sum (7) over patches to obtain

\[
\left|\int[Q(I_{k,h}f)-Q(f)]\varphi\,dx\right|
\le Ch^k\|\varphi\|_{W^{1,1}}.
\tag{11}
\]

In particular \(\varphi=v\cdot w\), with v,w in H¹, gives Ch^k\(\|v\|_{H^1}\|w\|_{H^1}\) by the product rule and Cauchy–Schwarz. This is the graph-parametrization version of the curvature bilinear estimate. An additional boundary strip could be handled under a separately verified strip estimate; it is not silently assumed here.

No construction of a full fixed-domain mesh family tiled by the odd regular fans is supplied. A regular odd polygon generally does not tile the plane, so local rotational fans alone do not establish the global hypothesis of (11). Nor is it proved that global superconvergence requires any such patchwise zero moment: cancellation between different patches, approximate moments, or a boundary mechanism could suffice. We also do not prove a closest-point-lift transfer, all other geometric consistency terms, a complete closed-surface Stokes error theorem, or the projected-refinement/newest-vertex-bisection observations outside the cited main theorem.

The verified advance is the finite local criterion, its pair-free rotational realization, the odd-degree diagnostic, and the conditional weighted estimate. These isolate an exact remaining global structure problem. The one substantive route stops at that gap. Recommended original status: **unsolved, 1/5**.
