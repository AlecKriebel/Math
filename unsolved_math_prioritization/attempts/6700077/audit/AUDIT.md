# Independent adversarial audit: 6700077

## Verdict

**PASS WITH EXPLICIT SCOPE AND SOURCE-CONVENTION QUALIFICATIONS.** No substantive mathematical error was found in the five retained approaches. The strongest restricted result, closure for the stated two-dimensional warped class with piecewise-C2 approximants, survives a full analytic review. The general closure target remains **unresolved here, 5/5 approaches**. This verdict establishes neither a general solution nor historical novelty nor global openness. It is an independent AI-assisted review, not human peer review.

The frozen author manifest is externally bound to SHA-256 `b25e29914341432f65924b883eb5361158e3fee1249bcdab57b2281cfbb662b2`. All 12 listed payload files were checked against that anchor before and after the audit. Originals were not edited. No helper agents or remote writes were used. The safe audit is separate from privately retrieved source PDFs, extracted text, and page images.

The identifier/rank association (rank 703, ID 6700077, AMR-066-0077) comes from the supplied assignment and authored descriptor; the unavailable target page and unavailable raw AI record were not independently inspected. It must not be represented as fresh dataset verification.

## 1. Exact source and convention boundary

The fresh Gromov PDF matches the author's hash. Direct visual inspection of printed pp.80–81 confirms that [?79] is the C0 closure question, distinct from nearby smoothing and density questions. Page 80 visibly uses `≤κ`, `R>1/sqrt(κ)`, and an infimum of lower thresholds, while normalizing the round sphere by `Sc=2/R²`. These cannot simultaneously implement the stated smooth compatibility. Independently: the ball expansion reverses the printed inequality; the printed radius ranges over scalar thresholds below 2κ; Euclidean space satisfies every negative threshold, whose infimum is −∞ instead of zero. The corrected lower-bound sign, `R>sqrt(2/κ)`, and supremum interpretation are mathematical inferences, not an author-approved erratum. The packet explicitly announces its normalized interpretation; that qualification is essential. The printed wording also leaves the small-radius quantifier terse. The audit reads it as comparison throughout a sufficiently small interval, consistently with the stated intended convention. [Gromov, Section 26, pp.79–83](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf)

Deng explicitly normalizes positive thresholds with `sqrt(2/κ)`. His Definitions 2.1–2.3 distinguish exact Euclidean domination at zero, and Theorems 1.2/3.5 require compactness, a shared positive SC-radius, and n-dimensional normalization of the limit. The SC-radius is an infimum across comparison models, which is stronger than the per-model uniformity sufficient for Approach 1. His theorem therefore does not remove the missing sequence-uniform radius. No blanket validation of his other propositions, remainder estimates, or measure-convergence claims is used. [Deng, SIGMA 17 (2021), 013](https://sigma-journal.com/2021/013/sigma21-013.pdf)

For this audit, the positive branch is: for every `0<λ<κ`, all sufficiently small centered balls compare strictly to `S²(sqrt(2/λ))×R^(n−2)`, with locally positive witnesses. The relaxed zero branch uses every negative threshold via the sphere-product prescription. This is weaker in general than exact Euclidean domination on a radius interval. The two are kept separate below. A literal, unrepaired reading of the inconsistent printed definition is not what has been proved.

## 2. Approach 1: fixed-witness-radius closure

**Accepted with its stated extra hypothesis.** Relative quadratic-form convergence on a larger compact coordinate neighborhood gives both determinant bounds and length bounds for paths confined there. Local ellipticity and a positive coordinate buffer prevent a short path from leaving that neighborhood. This justifies the inclusions for the manifold distance, not merely for an artificially restricted path metric.

For a fixed requested radius `r<R_λ`, choose sufficiently large `j` so `sqrt(1+e_j)r<R_λ`. Then

`V_g(x,r) <= (1-e_j)^(-n/2) M_λ(sqrt(1+e_j)r)`.

The right side converges to `M_λ(r)`. No boundary-measure assertion and no limit exchange for moving balls are needed. The quantifier order is indispensable: first fix λ and r, then send j to infinity. For strict comparison at λ, use a stronger threshold `λ'` strictly between λ and κ, then the positive leading term in `M_λ−M_λ'`. The available radius may shrink with λ and with the center neighborhood.

The partition-of-unity construction is valid on the usual paracompact manifold: at a point, only finitely many constants are active, each is a valid radius there, and their weighted average is at most their largest valid radius. Strict `<R` endpoints can always be handled by a preliminary reduction. The automatic n-dimensional normalization follows from local Euclidean tensor sandwiches.

**What it does not establish:** Individual positive witnesses `R_(j,λ)` need not have a positive infimum over j. Compactness for each individual metric does not make those witnesses uniform across a sequence. This exact failure remains after all finite controls pass.

## 3. Approach 2: radial central-only control

**Accepted as a counterexample to a proof shortcut only.** Differentiation independently gives the stated `A_j=W_j'/(nr^(n−1))` and both uniform-difference identities. For `n>=2` and `r<=1/2`, the lower bound is at least `1/2`, so the fractional power defining `f_j` is legitimate.

Smoothness at the center requires more than the value `f_j(0)=0`: here `A_j` is a positive smooth even function with `A_j(0)=1`, and `(f_j/r)^2−1` is divisible by `r²` as a smooth even function. Consequently the Cartesian expression

`g_j = q_j δ + (1−q_j) (x·dx)^2/r²`, with `q_j=(f_j/r)^2`,

extends smoothly across the origin. Radial distance and volume are exactly as claimed. Uniform control of q yields uniform tensor convergence, including the origin; derivatives converge only on annuli away from it.

The scalar formula is correctly normalized: scalar curvature is twice the sum over unoriented sectional planes. The central values `+6(n+2)` and `−6(n+2)` follow from the cubic coefficient of f. As an independent concrete check, in dimension two the limit has `Sc(1/4)=−64/3`; a finite approximant with `j=37` also has strictly negative curvature there. Thus this is a genuine all-centers failure of the approximating hypothesis, not merely a failure to prove it. The metric domain and selected test points stay inside the radius-1/2 ball.

The construction is distinct from the fixed-radius proof: it explicitly realizes collapsing central witnesses by smooth metrics while exposing why the tempting counterexample is inadmissible.

## 4. Approach 3: second-order-contact transfer

**Accepted as a centered local statement.** The little-o assumption plus continuity implies equality of the tensors at p. On an h-ball of radius `Cr`, it provides a relative error `e(r)=o(r²)`. Short-path localization is justified by positive definiteness and a fixed larger coordinate buffer. The ball/density sandwich therefore loses only `O(e(r)r^n)=o(r^(n+2))`.

The C2 small-ball expansion has normalized remainder `o(r²)`; a general `O(r⁴)` normalized remainder would require additional regularity and is not used. Substitution of `r(1+O(e))` preserves the scalar coefficient. No uniformity in a neighborhood of centers follows just from this pointwise germ.

The conformal example is correctly calculated. Its centered distance uses the integral of the radial conformal coefficient, which lower-bounds every competing path by radial variation. The resulting coefficient gives `Sc(0)=−4n(n−1)a`, so big-O second-order contact cannot replace little-o. The dimensionless error `e_j/r²` explains the missing scale control but is not itself an admissible-metric counterexample.

## 5. Approach 4: warped corners, full analytic review

### 5.1 Smooth pieces and scalar normalization

For `dt²+f(t)²dy²`, `K=−f''/f` and `Sc=2K`. Hence a lower scalar bound κ implies `f''+(κ/2)f<=0` on each smooth piece. For κ>0 this follows by comparison at all strictly smaller positive thresholds. At relaxed κ=0, a point with negative classical scalar curvature is excluded by choosing a negative threshold closer to zero and applying the smooth expansion to the product with the prescribed sphere. Thus the smooth-piece inference does not accidentally assume the stronger zero convention.

### 5.2 Seam expansion and moving-ball correction

Normalize the transverse coordinate by `Y=f(0)y`; the normalized slopes are `a_+=f'_+/f(0)` and `a_−=f'_−/f(0)`. Finite one-sided second derivatives give the local remainder `O(t²)` on both sides. Under scaling by ρ, the metric has the form `I+ρH+O(ρ²)`, where H is continuous and Lipschitz, including across the seam.

For a unit endpoint `z=(cos θ,sin θ)`, the Euclidean segment is the unique minimizer of the unperturbed energy. Perturbed minimizers remain in a fixed compact coordinate region; their Euclidean energies tend to 1. The identity

`integral |γ'−z|² = integral |γ'|²−1`

then gives strong H1 convergence to the segment. Evaluating the order-ρ energy functional along minimizers converges to its segment value, while the nonnegative unperturbed energy excess supplies the lower estimate and the test segment supplies the upper estimate. The first-order energy is `a_sign cos θ sin²θ`. Taking the square root yields

`d(0,ρz)=ρ+(a_sign/2)cos θ sin²θ ρ²+o(ρ²)`.

Compactness of the direction circle makes the remainder uniform, including almost tangent directions. This does not assume geodesics themselves are coordinate radial segments.

The radial boundary shift is therefore `−(a_sign/2)cos θ sin²θ r²+o(r²)`. A uniform annular enclosure suffices even without monotonicity of distance along a coordinate ray. Its area uncertainty is `o(r³)`. On the positive half-circle, integrating the density contributes `2a_+/3`, while moving the ball boundary contributes `−a_+/3`. On the negative half-circle the corresponding signs reverse. Thus

`area B(p,r)=πr²+[(f'_+−f'_−)/(3f(0))]r³+o(r³)`.

Both the coefficient and its sign are correct. Omitting domain deformation gives a wrong factor of two.

### 5.3 Independent exact geometric seam control

A second derivation is available in the special model `f(t)=1+a max(t,0)`, `a>0`, using a locally unwrapped y-coordinate. The negative side is a Euclidean half-plane. The positive side is locally the exterior of the Euclidean disk of radius `1/a`, with the seam corresponding to its circle. Excursions into the negative half-plane cannot shorten a seam-to-seam path below its horizontal distance, so a shortest path to an exterior point is either an outward straight segment or a seam arc followed by a tangent segment.

The outward-segment region contributes a Euclidean half-disk of area `πr²/2`. For the two tangent shadow regions, let s be seam arclength and l the subsequent tangent length. Their area Jacobian is `a l`. Therefore their total area is

`2 integral_(s=0)^r integral_(l=0)^(r−s) a l dl ds = a r³/3`.

Adding the negative half-disk gives **exactly** `πr²+a r³/3` for sufficiently small r. This independently validates the seam coefficient rather than merely reusing its algebra. The argument is local: r is chosen below the strip margin and below a fixed fraction of the circumference, avoiding wraparound and distant copies.

### 5.4 Corner sign, including relaxed zero

An upward jump makes the r³ coefficient positive, whereas any smooth two-dimensional model begins its correction at order r⁴. At relaxed zero, the sphere product retains that obstruction: if the surface excess coefficient is C, integrating against leading sphere shells `2πs ds` produces

`(2πC/5) r⁵+o(r⁵)`

above the leading four-dimensional Euclidean term. With `C=(f'_+−f'_−)/(3f(0))`, the coefficient is `2π(f'_+−f'_−)/(15f(0))`. Smooth product corrections begin at r⁶. Choosing any fixed permitted negative threshold therefore already excludes an upward seam. There is no cancellation at the relevant order and no use of a zero-endpoint Euclidean hypothesis.

### 5.5 Distributional closure and mollification

Locally finite seams permit integration by parts on finitely many intervals in every test-function support. Continuity cancels delta-prime terms, and the remaining atomic coefficient in `f''` is exactly `f'_+−f'_−`. The classical inequality and nonpositive jumps imply

`integral f_j(φ''+(κ/2)φ) <= 0`, for nonnegative compactly supported smooth φ.

Local uniform convergence passes this fixed test-function integral to f. No convergence of the derivatives or of the seam locations is needed. For κ>=0, the resulting f is in particular concave and locally Lipschitz; the proof needs only the distribution inequality.

On nested compact subintervals, convolution uses only points still in I. A nonnegative mollifier preserves both positivity of f and the distribution order and commutes with the constant-coefficient operator. The smoothed functions satisfy the same κ, with no curvature slack, and converge locally uniformly. An arbitrary signed smoothing kernel would not suffice.

### 5.6 Uniform local area comparison and passage to the limit

For each smoothed metric, along a minimizing ray before cut/conjugate time, the Jacobi density J is nonnegative. Let `s_κ(u)=sin(sqrt(κ/2)u)/sqrt(κ/2)` for κ>0, or u at zero. Before its first positive zero,

`(J' s_κ−J s_κ')' = −(K−κ/2)J s_κ <= 0`.

The initial ratio is 1, so `J<=s_κ`. The usual polar integration up to cut time gives the area upper bound; dropping later portions only decreases area. No sequence-uniform injectivity radius is required.

Local incompleteness is harmless here for an explicit reason. Choose nested strips `J0×S1` inside `J1×S1` inside I×S1, with positive t-gap δ from J0 to the boundary of J1. Every path leaving J1 has length at least δ because the coefficient of dt² is exactly 1, for every smoothing. Choose a common r smaller than δ (and smaller than the spherical first-conjugate radius if κ>0). The circle is compact, f and its smoothings are uniformly bounded above and below on the larger compact strip, and minimizing short paths exist in that compact region. One may equivalently extend each smooth metric outside the region to a complete smooth metric; short minimizing paths do not see the extension. Completeness of the original open cylinder is never assumed.

The exact common comparison is

`V_κ(r)=(4π/κ)(1−cos(sqrt(κ/2)r))`, or `πr²` at κ=0.

Its expansion is `πr²−πκr⁴/24+πκ²r⁶/1440+...`, consistent with scalar, not Gaussian, normalization. The Approach 1 inclusion argument passes this fixed model inequality to the continuous limit. Strict comparisons at `λ<κ` then follow by model slack. At zero the conclusion is the stronger Euclidean domination. Its implication for every negative relaxed threshold follows directly by integrating against sphere shells; for small positive s those shells have density strictly below `2πs`.

**Conclusion:** The restricted theorem is valid as stated under the announced intended convention. It does not cover arbitrary surface metrics, arbitrary gluing hypersurfaces, negative κ, changing warped coordinates, degenerating positive definiteness, or global comparison radii on noncompact I. No such extension is claimed.

## 6. Approach 5: closed hull and regularization

**Accepted as two exact conditional reductions.** In a fixed closed manifold's C0 metric space, the diagonal choice `d(h_j,g_j)<1/j` proves closedness of the smooth-approximation class. The implications A and B are genuinely separate: smoothing a volumic metric does not establish that a nonsmooth smooth-limit is volumic. The slack version again uses the diagonal sequence, now at `κ−1/j`, and is logically correct. These are not proofs of either missing bridge.

The source attribution is appropriate. Burkhardt-Guim's Theorems 4.1 and 4.3 concern the Ricci-flow weak notion and its smooth approximation characterization on closed manifolds; Section 5's comparison with Gromov concerns cubes and dihedral angles. No volumic identification is provided there. [Burkhardt-Guim, SIGMA 16 (2020), 128](https://sigma-journal.com/2020/128/sigma20-128.pdf)

Lee's v1 Theorems 1.1–1.3 retain smooth comparison metrics and hence do not supply those bridges. The arXiv submission date is April 20, 2026, while the downloaded PDF prints April 21, 2026; that metadata distinction has no mathematical effect. [Lee, arXiv:2604.17759v1](https://arxiv.org/abs/2604.17759v1)

The inspected Fogagnolo–Gatti–Pluda theorem is about an IMCF notion, under its stated three-dimensional completeness, topology and isoperimetric hypotheses. The current note explicitly defers technical details. It is not a result about the required ball-volume notion. [Fogagnolo–Gatti–Pluda, May 26, 2026 note](https://cvgmt.sns.it/media/doc/paper/7731/FGP-Scalar-curvature-bounds.pdf)

## 7. Zero-endpoint adversarial control

The distinction at zero is mathematically necessary, not cosmetic. In the local product `S²(1)×H²(−1)`, classical scalar curvature is zero. Direct convolution of the two-dimensional sphere ball series with hyperbolic shell series yields

`V(r)=(π²/2)r⁴+(π²/4320)r⁸+O(r¹⁰)`.

Thus `V(r)/(ω4 r⁴)=1+r⁴/2160+O(r⁶)>1` for small positive r. It satisfies the relaxed numerical zero bound by smooth scalar compatibility but fails exact Euclidean domination. This independently rules out silently substituting Deng's stronger zero definition in Approach 5. In the warped two-dimensional class, the stronger conclusion of Approach 4 follows from its special distributional structure; it does not contradict this four-dimensional example.

## 8. Distinctness, executable controls, and limitations

The five approaches are distinct in their mathematical content: fixed-scale inclusion; an explicit central-only metric construction; germ transfer and sharpness; a corner-to-distribution-to-smoothing theorem; and a conditional closed-hull reduction. There is a shared C0 comparison tool, but the routes have different inputs and different obstructions. Five substantive approaches does not mean five proofs of the target.

The author suite was rerun normally and under `python3 -O`: 5,194 auxiliary checks, 25 rejected mathematical negatives, and six rejected file-tampering cases in each mode. Independently written symbolic controls add exact differentiation, model coefficients, corner-domain correction, product excess, off-center scalar failure, zero-endpoint separation, and deliberate false claims. A separate external-anchor checker adds ten tamper classes, including a changed payload with a correspondingly rewritten internal manifest. Numeric counts and full check names are in RESULTS.json and DELIBERATE_NEGATIVES.json.

The external anchor is crucial: a self-consistent rewritten manifest is not authenticated just by checking itself. This is a limitation of any unanchored checksum verifier, not an error in the packet's supplied external hash. All scripts use explicit exceptions instead of assert for validation and were checked under optimization.

Passing finite or symbolic auxiliary checks does not prove the energy-minimizer argument, local comparison theorem, universal quantifiers, or original source identity. Those were reviewed separately above. The audit does not certify every statement or proof in the cited literature. No broad historical search was repeated, and no absence-of-prior-work claim is made. The live target page failed to open, the raw report remains unavailable, and source ambiguity remains explicitly unresolved.
