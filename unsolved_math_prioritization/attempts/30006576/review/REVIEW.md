# Independent review: local curvature moments and pair-free rotational fans

**Problem:** 30006576 / OWR-14299907-001.  
**Verdict:** **PASS_SCOPED_LOCAL_CURVATURE_MOMENT_CRITERION**, no mandatory correction.  
**Recommended status:** **unsolved, 1/5**. The global mesh characterization is not established. This is a separate adversarial AI review, not human peer review or a priority assessment.

## 1. Frozen artifact and source conventions

I read the complete `PARTIAL.md` at SHA-256

`edfa4b49222d53f440b888179798371e17d78049c2f3344e50c91928b2613c36`.

The frozen checker has SHA-256 `0212b654bb3eff2740a7ada408a30a0df9f53bdec7d1f8f8d421e62d581212c8`; the submitted receipt has SHA-256 `1ab729c11e34599940c371add199e06b4c518e8e028f2cbb54b1279a39e5014b`. No mathematical source file was edited during this audit.

I read the exact contribution in [OWR 5/2026](https://ems.press/content/serial-article-files/53599), printed pp. 312–313, and visually inspected p. 312. It concerns weighted geometric consistency, including Gaussian curvature, for smooth two-dimensional surfaces in R3 under high-order parametric approximation. The stated improvement concerns integrals and bilinear terms, while the pointwise geometry estimates keep their usual orders. The open questions ask about the requisite internal mesh structure and observations beyond the visible paired-triangle setting. Thus an exact local moment criterion is relevant but is not automatically a solution of the full source question.

I also checked the full retrieved [Hardering–Praetorius–Zavalani preprint, arXiv:2607.29466v1](https://arxiv.org/abs/2607.29466v1), uploaded 31 July 2026. The current record shows that version, with no withdrawal notice visible. Definition 2.7 on p. 7, also visually inspected, uses **central reflection about the unique common vertex**, not reflection across an edge. Lemma 2.8 and Definition 2.10 describe a pair decomposition with controlled unmatched boundary elements. Theorem 3.2, Corollary 3.3 and Corollary 4.4 supply the credited sufficient weighted estimates. Appendix B explicitly keeps projected refinement and its newest-vertex-bisection experiments outside the direct scope of the main theorem. Some compatible NVB patterns may exhibit pairs, but the paper does not prove a blanket result for every observed NVB mesh.

The full earlier Zavalani–Shehu–Hecht author preprint, [arXiv:2301.02996v2](https://arxiv.org/abs/2301.02996v2), was additionally checked at Definition 3.1 and Theorem 3.3. It assumes symmetric pairs with an O(h^(-1)) unmatched remainder and studies integration of an interpolated smooth integrand. It does not supply the missing all-mesh intrinsic-curvature characterization.

The candidate uses elementwise curvature of interpolated **graphs** and a parametrization lift. It does not equate this with distributional curvature of the piecewise-smooth surface, nor silently identify the parametrization lift with the closest-point lift. Those qualifications are essential and are correctly retained.

## 2. Independent derivation of the graph density

For a graph `(x,y,f(x,y))`, the first fundamental form is `I+a a^T`, where `a=grad f`, and has determinant `1+|a|^2`. The second fundamental form is `D^2 f/sqrt(1+|a|^2)`. Hence

\[
K_f=\frac{\det D^2f}{(1+|\nabla f|^2)^2},\qquad
K_f\,dA_f=\frac{\det D^2f}{(1+|\nabla f|^2)^{3/2}}\,dxdy.
\]

Thus the exponent 3/2 in the candidate is correct for **curvature times area density**, even though pointwise Gaussian curvature has exponent 2. The discrete graph uses its own area factor, and pulling both integrals to their common planar parameter domain gives exactly the difference of Q's in the statement.

No mesh-interface delta curvature is included. This agrees with the elementwise geometric quantity being audited; adding such a distributional term would define a different target.

## 3. The all-jet local equivalence is valid

Let the finite triangulated patch be fixed, and scale it by h. Affine invariance and polynomial reproduction of the degree-k nodal interpolant give a Hessian interpolation error of order h^(k-1). Only the homogeneous Taylor term p of degree k+1 contributes at that order. The interpolated Taylor remainder has nodal size O(h^(k+2)); two physical derivatives multiply by h^(-2), leaving O(h^k). The true remainder has the same derivative order. There is no differentiability of a merely pointwise remainder being assumed without justification: the stated C^(k+2) regularity supplies the derivative Taylor remainder, and finite-dimensional nodal interpolation supplies the interpolated bound.

With `H=D^2 f(0)` and `a=grad f(0)`, differentiating Q with respect to its Hessian variable gives

\[
E\longmapsto(1+|a|^2)^{-3/2}\operatorname{cof}(H):E.
\]

The gradient interpolation error is one order smaller, O(h^k). Replacing smooth coefficients by their values at zero costs O(h) times the leading Hessian error. The determinant's quadratic remainder is O(h^(2k-2)), which is O(h^k) for every k>=2, including equality at k=2. The denominator and its derivatives are uniformly bounded on the bounded jet range; it never vanishes. This proves the candidate's pointwise elementwise expansion with a uniform O(h^k) remainder.

Integrating over the shrinking patch contributes h². The leading coefficient is therefore h^(k+1) times the cofactor contraction with the integrated Hessian moment. Vanishing of every such matrix moment is sufficient for O(h^(k+2)).

Necessity really holds for **every graph jet**, not merely for a scalar trace condition. If a real p has a nonzero symmetric moment matrix M, choose the quadratic Hessian H=cof(M), zero linear term, and the same p as the higher Taylor term. Since k+1>=3, these choices are independent. In dimension two, cof(cof(M))=M, and the leading contraction is `M:M>0`. Thus the h^(k+1) coefficient is nonzero and cannot be O(h^(k+2)). This works for indefinite and singular matrices as well; positive curvature or Hessian invertibility was never required.

The theorem is consequently an exact necessary-and-sufficient condition for the particular fixed shrinking graph patch and all smooth jets. It is not a necessity theorem for arbitrary global mesh decompositions.

## 4. Rotational cancellation and the absence of source-defined pairs

The interpolation commutes with the rotations because the full standard barycentric node set is transported with each triangle. For a complex homogeneous monomial `z^a conjugate(z)^b` of degree k+1, the rotation character is ell=a-b. Applying two Wirtinger derivatives gives the characters `ell+2`, `ell`, and `ell-2`. When k is even, every one is odd and nonzero. Under q>k+3, none is divisible by q. Summing the character over all q triangles is therefore zero.

I independently checked the derivative signs: a z-derivative lowers the character by one and a conjugate-z derivative raises it by one. This gives exactly `ell+2-2r` for r z-derivatives. The three resulting derivatives linearly span the entries of a complexified real symmetric Hessian. Complexification is harmless because the desired moment map is real linear and the real and imaginary parts give the real polynomial test space.

The geometric exclusion of pairs also checks out. All fan triangles contain the center. Adjacent ones have an entire edge in common and cannot be source pairs. Nonadjacent ones meet only at the center, so that center is the only possible reflection center allowed by the source definition. Reflection would require opposite boundary vertices, which an odd regular polygon does not have. The condition q odd is used here, in addition to the nonresonance argument. The fan is a fixed finite nondegenerate triangulation, so its shape-regularity constants may depend on q, as the statement permits. There is no assertion of constants uniform as the interpolation degree tends to infinity.

These facts show pair-free **local cancellation**, not a complete fixed-domain refinement family.

## 5. Degree-three failure and independent interpolation calculation

I independently solved the ten-node degree-three interpolation problem by a rational Vandermonde matrix and integrated the Hessian by **boundary flux**, rather than using the submitted barycentric-basis/moment computation. On the triangle with vertices `(0,0),(1,0),(c,s)`, the resulting radial quartic trace is

\[
-\frac{(c^2+s^2)((c-1)^2+s^2)}{3s}.
\]

For `c^2+s^2=1`, it becomes `2(c-1)/(3s)`, as claimed. In a regular q-fan with q>=7, s>0 and c<1, so it is strictly negative. The polynomial and the Laplacian are rotationally invariant, making every triangle's contribution equal. The trace moment is therefore nonzero after summation.

Taking `f=(x^2+y^2)/2+(x^2+y^2)^2` gives Hessian I and zero gradient at the patch center. For degree three, the h⁴ leading coefficient is the nonzero trace moment, so an O(h⁵) estimate fails. The ordinary h⁴ patch-area-normalized estimate remains valid. This does not imply a worse pointwise bound than the standard order, and the candidate does not claim one.

For the single reference triangle at degree two, the interpolant of x³ and its nonzero integrated xx error also check out. Cancellation is a property of the selected patch, rather than an automatic elementwise identity.

## 6. Weighted and conditional global consequences

The leading scalar error has mean zero and L-infinity norm O(h^(k-1)). The scaled L1 Poincaré inequality on a connected bounded Lipschitz patch gives

`||phi-average(phi)||_1 <= C h ||grad phi||_1`.

Subtracting the average in the leading term and retaining the O(h^k) remainder proves the candidate's weighted estimate. This is why the connected-Lipschitz assumption matters. It is not legitimate to obtain the same bound on arbitrary changing patches with uncontrolled Poincaré constants, and no such claim is made.

For a decomposition into rotated, translated, comparable-h copies of finitely many admissible patches, the constants are uniform. Summing the local estimates is valid because patches partition the elements up to boundaries of planar measure zero. The product of two H1 functions lies in W^(1,1), with its norm bounded by the product of the H1 norms by Cauchy–Schwarz and the weak product rule. Thus the conditional bilinear consequence follows.

The missing global ingredients are substantial and explicitly preserved: no fixed-domain mesh family tiled by odd regular fans is constructed; no boundary-strip estimate is supplied for that construction; no transfer of every geometric consistency term or closest-point-lift statement is proved; no full characterization of projected/NVB observations follows. Cancellation across patches or approximate moments could also yield global improvements without an exact patchwise decomposition. Therefore the local equivalence cannot be relabelled as a global necessity theorem.

## 7. Reproduction, independent diagnostics and final disposition

All **3,745 submitted exact assertions** reproduced byte for byte in an isolated copy. The independent checker uses rational Vandermonde interpolation, boundary-flux integrals, exact cyclotomic arithmetic on complete degree-two seven-fans and degree-four eleven-fans, and separate graph-density/cofactor/scaling checks. All **4,971 independent exact assertions** pass; their category counts and case list are recorded in `independent_results.json`.

The direct fan controls assemble each triangle's interpolation system and coordinate inverse and sum the integrated Hessians after suppressing the identical nonzero area Jacobian common to every triangle of each fan. They do not merely sample trigonometric values. Nevertheless, these remain finite diagnostics. The all-even-degree result is proved by the nonresonant character argument, and the all-smooth-jet and weighted estimates require the analytic reasoning above.

No mandatory correction is required. The package is suitable for a scoped partial-result draft, with **unsolved 1/5**, the credited later preprint, the exact local/conditional quantifiers, and the absence of a claimed global odd-fan family or priority assertion retained.
