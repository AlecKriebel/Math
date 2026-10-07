# Independent mathematical audit: Reshetnyak-harmonic sphere with unbounded distortion

Problem 30006419, OWR-14299521-012, rank 969. Review date: 7 October 2026.

## Verdict

**PASS.** The frozen `PROOF.md` proves a negative answer to the general-energy question, by choosing the admissible Reshetnyak energy. It constructs a smooth homeomorphism from the round sphere to a smooth compact Riemannian sphere which satisfies the source's exact local-minimization requirement but has no finite infinitesimal quasiconformality constant.

The result does **not** identify the same map as Korevaar–Schoen harmonic. The manuscript explicitly distinguishes that restriction. Its separate positive Korevaar–Schoen theorem receives a separate audit in `KS_APPENDIX_AUDIT.md`; acceptance of the counterexample does not depend on the appendix.

No blocking error, missing target hypothesis, or unproved additional restriction on competitors was found. No correction patch is required. This is a mathematical review, not a proof-assistant certificate, a referee decision, or a historical-priority determination.

## 1. Frozen objects and review independence

The complete proof and complete companion appendix were read. The reviewer did not consult another audit, did not contribute to the manuscript, and did not edit its files. The author confirmed the final freeze before this verdict. All eight entries in the author's manifest, and the external hash of that manifest, were checked.

- `PROOF.md`: 16,750 bytes; SHA-256 `2634e714b9a06a1770ae39b0201031c7d2a7ce6e97f3330f8745d0e2453d4fef`.
- `KOREVAAR_SCHOEN.md`: 6,702 bytes; SHA-256 `4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe`.
- Author `MANIFEST.json`: 1,288 bytes; SHA-256 `9cb1f5c242224d4f04a34b1d28e660a29fb2f63d47215d16257f5d4073c001cb`.

The public source PDFs were independently downloaded from their official URLs and were byte-identical to the copies associated with the manuscript. Text inspection covered the precise hypotheses, energy definitions, quasiconformality definition, locality definition, and relevant global-minimizer result. The key question and definition pages were also visually inspected.

## 2. Source scope and version limit

The [Oberwolfach report](https://ems.press/content/serial-article-files/52249), printed page 1625, fixes an energy before its first question. The [cited arXiv v1 paper](https://arxiv.org/pdf/2503.08553v1), Question 1.9 and Definition 3.1, permits Reshetnyak energy and requires quasiconvexity. Definition 6.1 asks for a neighborhood at each point, then energy comparison on every Lipschitz domain compactly contained there, against all same-trace Sobolev maps. There is no image, continuity, or homotopy restriction on those competitors. Definition 2.3 concerns a single finite bound on directional stretch at almost every point. These are the scope anchors used here.

The [author's bibliography](https://people.math.ethz.ch/~damameier/research.html) lists the article in *J. Reine Angew. Math.* 838 (2026), 137–169. The final publisher text was not inspected. The source-level verdict is bound to the retrieved v1 and Oberwolfach report; it does not certify unchanged wording in the published version or exhaust later literature.

## 3. Scalar calibration: unrestricted competitors really are covered

The flat-patch argument needs more than the angular coordinate having gradient of norm one. It needs the coordinate to be Lipschitz with respect to the **whole target's** distance on the chosen patch. This is correctly supplied by taking a sufficiently small strongly geodesically convex ball inside a flat coordinate chart. Between any two points in that ball, an ambient minimizing geodesic stays in it. Integrating the coordinate differential along that geodesic bounds the coordinate difference by ambient distance.

The selected angular lift is therefore 1-Lipschitz on this smaller set. Its McShane extension is globally 1-Lipschitz and finite on the compact target. For any competitor, including one crossing a pole or covering the entire target, composition with this extension is an ordinary scalar Sobolev map. Its weak gradient is bounded by the competitor's operator-norm differential, and its trace equals the angular source coordinate.

Subtracting that coordinate gives an element of `W^{1,2}_0`. The mixed term in its Dirichlet energy is the integral of a weak coordinate derivative, which vanishes by zero-trace approximation. Thus every competitor has Reshetnyak energy at least the Euclidean area of the domain. The proposed map has differential `diag(h',1)` with `0 <= h' <= 1`, and attains that lower bound exactly. The conformal factor of the round source cancels from both sides.

This proof handles arbitrary Lipschitz subdomains of the selected coordinate neighborhood, including domains with holes. It does not assume that the competitor remains in the chart, is continuous, or is homotopic to the original map. The strong-convexity step is substantive: an angular lift on the entire cylinder would fail the ambient-distance condition across an angular cut.

## 4. Cap calibration: the critical Sobolev exactness step

### 4.1 Construction of a usable global form

The image of a sufficiently small conformal source neighborhood lies in a target neighborhood supporting a cutoff `eta` whose integral `m` is less than half the total target area `A`. With `b=m/(A-m)`, the coefficient of

`omega = ((1+b) eta - b) dA`

lies between `-b` and `1`. Consequently its comass is at most one; it equals the area form near the original image; and its integral over the target is zero. The target is an oriented smooth sphere, so the latter condition implies that the form is globally exact. This use of top-degree de Rham cohomology is correct, and would not be justified merely by saying that the image patch is contractible.

For any differential between oriented two-dimensional inner-product spaces, the pullback density of such a form is at most the absolute Jacobian, which is at most the square of the largest singular value. No orientation assumption on the **competitor** is required. The original conformal, orientation-preserving map attains equality.

### 4.2 Why the boundary integral remains invariant at Sobolev regularity

The proof does not silently invoke smooth density for sphere-valued maps. Its global primitive is written as a finite sum `alpha = sum f_j dg_j`, with globally smooth scalar functions on the compact target. A finite atlas and partition of unity give such a representation: multiply each coordinate coefficient by the partition function, and cut off each coordinate function so that it agrees with the coordinate on a neighborhood of that coefficient's support. The extra cutoff derivatives then occur where the corresponding coefficient is zero.

After composition with a Sobolev competitor, each scalar function is bounded and in `W^{1,2}`. For bounded scalar functions `F,G` in that class, the distributional identity

`d(F dG) = dF wedge dG`

is valid. To check the endpoint regularity explicitly, mollify locally. The mollified coefficients remain uniformly bounded. Their products with the approximated gradients converge in `L^2`, after using almost-everywhere convergence and dominated convergence on the term with the fixed gradient. Products of the two strongly convergent `L^2` gradients converge in `L^1`. These are exactly the convergence strengths needed to pass the displayed identity to distributions. The target chain rule then identifies the resulting form with the almost-everywhere pullback of `d alpha`.

Matching traces allow the competitor to be glued to the original map outside the subdomain. The glued map is Sobolev; equivalently, this can be checked after a smooth compact-target embedding or with the metric Sobolev gluing theorem. The difference of the two pulled-back primitives is an `L^2` one-form supported in the closure of the comparison domain. Pairing its distributional derivative with a cutoff equal to one near that closure yields zero. This proves equality of the two integrals of `omega`.

The argument is not invalidated by an extra spherical bubble, rough target excursions, or orientation reversal inside the competitor. Global exactness is precisely what avoids a degree ambiguity. Combining this identity with the pointwise comass inequality establishes the required unrestricted minimization on cap neighborhoods.

## 5. The target and its hypotheses

### Smooth metric and compactness

The target cylinder factor is identically one on `|s| <= 2`. Its cutoff is smooth at both transition endpoints; the absolute value causes no singularity at zero because the exponent vanishes on a neighborhood of zero. For `s <= -3`, the metric becomes `|d(e^{s+i theta})|^2`; for `s >= 3`, it becomes `|d(e^{-s-i theta})|^2`. These are positive Euclidean metrics in the two added pole charts. Thus the construction is a smooth positive metric on a compact sphere, rather than a cylinder with singular or incomplete ends.

### Geodesicity and small-sphere contractibility

A compact Riemannian manifold is complete and its length metric is geodesic. It is therefore quasiconvex with constant one. A uniform radius below the injectivity radius gives contractible normal balls. An image of diameter smaller than that radius is contained in such a ball centered at any one of its image points, proving the stated small-diameter null-homotopy condition.

### Local quadratic isoperimetry

Uniformly controlled nested charts may be chosen with convex Euclidean coordinate images. A sufficiently short Lipschitz loop lies in one of the smaller charts. Its Euclidean image can be coned to an image point without leaving the larger chart. If `L` controls both chart Lipschitz constants, the Euclidean image has length at most `L ell`, and every point lies within `L ell/2` of the chosen cone point by taking the shorter loop arc. The Euclidean cone area is at most `L^2 ell^2/4`. Returning through the inverse chart multiplies area by at most `L^2`, producing the manuscript's `L^4 ell^2/4` bound.

This radial cone is a Sobolev filling with the original boundary parametrization; the Lipschitz assumption on that parametrization controls its angular derivative. Compactness makes the chart constants and small-length threshold uniform. No unjustified global convexity or global quadratic inequality is needed.

## 6. The map, every seam, and the exact local quantifier

The prescribed even cutoff gives `a(t)=t^2` on the central quarter-unit interval and `a(t)=1` outside the half-unit interval. It is a convex combination of `t^2` and `1` wherever the cutoff is nonzero, hence lies in `[0,1]`, and vanishes only at zero. Integrating makes `h` smooth, odd, strictly increasing, and onto. A vanishing derivative at one point does not prevent strict monotonicity.

Near the ends, `h(t)=t-c` on the positive side and `h(t)=t+c` on the negative side, with `0<c<1/2`. In the corresponding complex pole charts, the map is multiplication by the same positive number `e^c`. Thus the forward map is smooth through both poles. It is a homeomorphism, but not a diffeomorphism at the equator; the proof states this distinction. Smoothness on the compact domain implies membership in the required Sobolev class.

For every source point with `|t|<1`, a sufficiently small neighborhood maps into the flat target belt and can be further restricted to a strongly convex angular-lift patch. Scalar calibration applies there to **all** relatively compact Lipschitz subdomains. For points with `|t|>1/2`, including neighborhoods of the poles, the map is conformal and orientation-preserving. The exact-form lemma applies to **all** relatively compact Lipschitz subdomains of a smaller neighborhood.

Those two open regimes overlap. Points at `|t|=1/2` are covered by the belt regime; points at `|t|=1` are covered by the conformal regime. The equator is covered by scalar calibration despite its rank-one differential. Every source point is therefore covered, and the neighborhoods are chosen before the comparison subdomain and competitor. This is the source's actual quantifier order.

## 7. Distortion and energy admissibility

On the punctured central band, the coordinate singular values are `1` and `t^2`. The round source rescales them equally and the target factor is one, so the ratio is exactly `t^{-2}`. For every finite proposed bound, the proof supplies an open band of positive round area on which the ratio is larger. This establishes essential unboundedness, not just a defect on a null equator. It directly violates the source's definition.

The maximum-square energy has the required continuity, monotonicity, degree-two homogeneity, and rotation invariance. In its unit sublevel, the seminorms are bounded by the Euclidean norm and are uniformly Lipschitz on the unit circle. The seminorm axioms survive uniform limits, so Arzelà–Ascoli gives compactness in the source metric.

For a finite-dimensional normed target, the square of the operator norm is a convex function of a linear map. A smooth fixed-affine-boundary competitor has average derivative equal to the prescribed linear derivative, componentwise by integration by parts. Jensen's inequality gives quasiconvexity, in fact for the larger class of all smooth competitors. The source's immersion restriction therefore presents no gap.

## 8. Independent negative controls

### Global homotopy minimization

The coordinate identity map is a smooth conformal degree-one map into this target. It has energy equal to the target area and is homotopic to the proposed map. Direct computation yields the strictly positive difference `4 pi c`. The author did not accidentally construct a counterexample to the cited global homotopy-minimizer result.

Independent numerical integration gives:

- `c = 0.3724273200219335`;
- the computed energy-minus-area agrees with `4 pi c` within `10^{-10}`.

One may also interpolate the radial coordinate as `(1-lambda) h(t) + lambda t`. The same computation makes the excess `4 pi c (1-lambda)`. Such whole-sphere variations do not invalidate the verified neighborhoodwise minimum property. The maximum-singular-value energy is nonsmooth at conformal differentials; an unsupported local-to-global linear first-variation argument would be inappropriate.

### Korevaar–Schoen energy

On a belt rectangle strictly on the positive side of the equator, the scalar first coordinate has second derivative `2t`. A nonnegative compactly supported perturbation has KS first variation `-4 integral(t psi)`, which is strictly negative. All images remain in the flat patch for sufficiently small perturbations. Hence the counterexample is genuinely **not** KS-harmonic. This excludes using equivalence of Sobolev spaces or comparability of energies to identify their minimizers.

### Finite controls and their limits

The independent script passed 675 checks in normal and optimized Python. They include frozen-file and fresh-source identities, cutoff and pole identities, positive-area distortion witnesses, the integrated energy gap, arbitrary-matrix scalar and two-form inequalities, exact symbolic KS descent, and separate stress checks for nonsmooth seminorms. Explicit exceptions rather than Python `assert` statements enforce failures.

The finite checks support the calculations and expose nearby wrong formulations. They are **not** substitutes for the analytic checks in Sections 3–7. In particular, sampling cannot prove the full arbitrary-competitor assertion, Sobolev pullback calculus, de Rham exactness, smooth endpoint extension, or uniform target hypotheses.

## 9. Final acceptance scope

The proof at the frozen hash is accepted as an authored counterexample for the general admissible-energy question. Preserve the phrase “for Reshetnyak energy” and the distinction from the KS restriction in summaries. The exact source version, lack of final-publisher-text inspection, and absence of a novelty certificate should remain disclosed. No manuscript correction is necessary for this verdict.
