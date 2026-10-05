# Controlling mathematical correction: zero-endpoint hypothesis

Problem 30001408 / OWR-4199-001, rank 696. Independent review date: 2026-10-05 UTC.

## Binding and precedence

This correction applies only to the frozen author's `RESULT.md`, 19,582 bytes, SHA-256 `899104bab4c4f25bd2bf5a5f7bd6cdb6d72ff037e113db3935c01f610e16765d`, bound by `AUTHOR_MANIFEST.json` SHA-256 `938d14791569ca0c77c9f19b13a71bd33219df81395d778c86e6703300c9bb34`.

It replaces the whole paragraph in Section 5 beginning “For c>0, requiring a concave density with g(0)=0” and ending “the endpoint conditions exclude alpha=0 and alpha=1.” That paragraph is line 127 of the frozen UTF-8 file. Its 275 UTF-8 bytes, excluding the terminating newline, have SHA-256 `9e99172a34672df479a076a0470045f6d69cbd6b578422c2d941b1adec1c8f8e`.

The original bytes are preserved for provenance. The replacement below is authoritative over the identified paragraph. Any release relying on the audit must include this correction, bind it in its release manifest, and make its precedence explicit. The frozen paragraph is mathematically false as written; this is not merely a bibliographic clarification. The audit does not issue an unconditional pass for the unamended frozen document.

## Complete replacement paragraph

For c>0 and g(s)=c s^alpha on s>0, impose the finite representation theorem's actual endpoint assumptions: g is concave on [0,infinity), g(0)=0, lim(s down to 0) g(s)=0, and lim(s to infinity) g(s)/s=0. These conditions hold exactly when 0<alpha<1, equivalently -n<q<n for alpha=(n-q)/(2n). Indeed, on s>0 the second derivative has the sign of alpha(alpha-1), so concavity requires 0<=alpha<=1. The right-limit condition at zero excludes alpha=0 because c>0, and sublinear growth at infinity excludes alpha=1 because g(s)/s=c. Conversely, when 0<alpha<1 the power is concave, extends continuously by zero at zero, and has sublinear growth. The right-limit condition is essential: assigning g(0)=0 alone does not imply it. These are additional hypotheses of the finite representation theorem, not consequences established here for an arbitrary extended-valued valuation.

## Exact counterexample to the replaced implication

Fix c>0. Define j(0)=0 and j(s)=c for every s>0. This function is concave on [0,infinity). To prove the concavity inequality, take x,y>=0 and 0<=lambda<=1. If lambda x+(1-lambda)y>0, its j-value is c, while lambda j(x)+(1-lambda)j(y)<=c. If the convex combination is zero, every endpoint with positive weight is zero, so both sides are zero. Thus concavity holds in all cases.

Furthermore j(0)=0 and j(s)/s=c/s tends to zero at infinity. On the positive half-line j(s)=c s^0, so alpha=0 satisfies every condition stated in the original paragraph. But lim(s down to 0) j(s)=c, not zero. This explicitly falsifies the original inference and identifies the missing hypothesis.

## Source of the repaired hypothesis

Ludwig and Reitzner, *A classification of SL(n) invariant valuations*, Annals of Mathematics 172 (2010), Theorem 5, printed p.1222, explicitly requires the density's limit at zero to vanish. The same limit is used in Section 5, printed p.1262, in deriving the homogeneous classification. DOI: https://doi.org/10.4007/annals.2010.172.1219 . Public publisher PDF: https://annals.math.princeton.edu/wp-content/uploads/annals-v172-n2-p09-p.pdf . Freshly downloaded PDF: 1,659,946 bytes, SHA-256 `8e0a5459d4695ec7adc783b75a0317d57a46df8666da774dc9d29d357ccdd739`.

The correction restores that hypothesis rather than postulating a new representation theorem. The independently checked equation from balls is alpha=(n-q)/(2n).

## Complete downstream dependency trace

1. **Section 2, finite-valued list:** unchanged. It invokes Annals Theorem 4 directly; it does not derive the classification from the defective paragraph. Its coefficients, exceptional degrees, strict-positivity restrictions, and extended-valued gap remain as stated.
2. **Section 3, Boolean support and finite-part reconstruction:** unchanged. Their proofs use upper semicontinuity, positive scalar homogeneity, and absorbing extended addition, not curvature densities.
3. **Section 4, rejected infinity supports:** unchanged. The explicit unions/intersections and density arguments are independent of the endpoint inference.
4. **Section 5, ball calculation:** unchanged. Assuming the extra integral representation and a finite c=g(1), dilation of balls gives the power law for positive arguments. It does not determine g(0).
5. **Section 5, concave power range:** the replacement supplies the previously missing premise. With it, the range 0<alpha<1 and -n<q<n is correct. Neither this repair nor the source theorem gives the missing representation for a mixed finite/infinite target valuation.
6. **Section 5, Holder finiteness bound:** unchanged once 0<alpha<1 is explicitly stipulated. The bound needs that range, finite cone volume, and the credited polar-curvature measure inequality. It does not need the defective endpoint implication after the range is established correctly.
7. **Section 5, alpha>=1 rounded-cube obstruction:** unchanged and independent. Its geometric positive patch supplies a nonzero lower bound at alpha=1 and divergence at alpha>1 while the cube value is zero.
8. **Section 5, negative powers with g(0)=infinity:** unchanged. Polytope-to-ball approximation directly contradicts upper semicontinuity.
9. **Section 5, alpha=0:** the existing superellipsoid proof independently rejects the zero-at-zero jump density j above as a target valuation. Let E_m={sum_i x_i^(2m)<=1}, m positive integers, n>=2. These smooth bodies converge to P=[-1,1]^n. Their curvature is positive off coordinate-zero sections of surface measure zero, so the integral of j is c times their cone measure, c n V_n(E_m). The inclusions n^(-1/(2m))P subset E_m subset P imply V_n(E_m) tends to V_n(P)>0. On P the generalized Gaussian curvature is zero almost everywhere and j(0)=0, so the integral is zero. Consequently the upper-semicontinuity inequality fails at P. This argument requires no concavity-at-zero inference. When g is identically c including at zero, the integral is simply c n V_n, the permitted volume term.
10. **Section 5, polar-volume endpoint:** unchanged. The raw alpha=1 density accounts only for the absolutely continuous curvature measure; the full polar-volume measure contains a singular component.
11. **Sections 6 and 7:** unchanged. Dissection obstructions and the complete one-dimensional theorem do not use the defective paragraph.
12. **Section 8, approach accounting, and status:** unchanged at unsolved, five substantive approaches used. The curvature approach retains valid partial results after repair, and no sixth approach or complete higher-dimensional classification is created by this audit.

## Audit of the replacement

The independent reviewer checked the replacement's necessity and sufficiency analytically, checked its source hypothesis in the downloaded primary article, and included a separate exact counterexample control for the false original inference. The derivative and endpoint arguments are valid for every real alpha and c>0. The zero coefficient c=0 remains the separately stated degenerate case; no conclusion about g(0) is obtained from the positive-curvature power calculation alone.
