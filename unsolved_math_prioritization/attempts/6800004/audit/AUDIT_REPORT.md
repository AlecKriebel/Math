# Independent source-resolution audit: 6800004

**Verdict: PASS, for a credited source resolution in a recent preprint.**

Checked 2026-10-03 UTC. This independent reviewer did not prepare the frozen packet. No mathematical repair is required. This verdict is not journal peer review, a novelty claim, or authorization to publish or change a remote repository.

## 1. Object and exact scope

Reviewed candidate 6800004 / AMR-067-0004, “Biorthogonal curvature,” against the original question and the complete Chen–Zhang argument. The conclusion is existence of a smooth Riemannian metric on the smooth product S² × T² such that the average of the Levi-Civita sectional curvatures of every two-plane and its metric-orthogonal complement is strictly positive at every point.

Frozen input manifest SHA-256:

`ae22ff6876b9c75e026d197d0c6e4ef035b7acdfc6d2dda95725a6a59dabc709`

Frozen source-certificate SHA-256:

`27c8ca0299b8a2fb3e2e4384045c8d41dfaa4527cfda71186be3413b037529b3`

Every manifest-listed byte count and file hash was independently recomputed and matched. The frozen packet was not edited. The original-attempt ledger is empty; this audit does not consume an original proof-attempt turn.

## 2. Primary-source identity and status

The relevant passage is Section 4, Question 4, printed page 3 of [Morgan–Pansu's author-hosted list](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf). The problem concerns the Riemannian curvature of S² × T², with complementary-plane averaging. The pinned problem record has the same manifold and hypothesis. The original page was checked in extracted text and visually.

[Chen and Zhang, arXiv:2609.08119v1](https://arxiv.org/abs/2609.08119v1), submitted 8 September 2026, is the exact affirmative source. Theorem 1.2 appears on printed page 2; its proof ends on page 12. The complete 13-page source was read, including the connection calculation, curvature entries, Hodge reduction, estimates, conformal argument, and references. The theorem page was visually checked; the [primary HTML full text](https://arxiv.org/html/2609.08119v1) agrees with the local PDF text.

The non-versioned arXiv record was also checked: it displayed only v1 and no journal reference. A targeted search found no correction or erratum. These are limited current-source observations, not a guarantee that no criticism exists. The appropriate status wording remains “answered by Chen–Zhang in a recent preprint,” not “peer-reviewed theorem.”

The earlier affine-connection material and the imported August research summary are not the basis of the PASS. The current UnsolvedMath page was not independently recovered in this audit; its frozen HTTP 403 qualification must remain. Neither that inaccessible status nor the old dataset defeats the exact original-source match.

## 3. Global metric and ordinary Levi-Civita connection

Let Xᵢ(p) = Eᵢ × p on the unit sphere and let dt₁, dt₂ be the constant one-forms on R² descending to any lattice quotient R²/Λ. Although real-valued coordinate functions tᵢ need not be global on the torus, the constant fields and one-forms are global. No rectangular-lattice or periodic-flow assumption is needed.

The proposed quadratic form is the pullback of the product inner product by the smooth fiberwise invertible shear

(V,a,b) ↦ (V − εaX₁ − εbX₂,a,b).

Consequently it is smooth, positive definite, and lattice-invariant everywhere, including both sphere poles. Multiplication by the strictly positive smooth square uε² preserves these facts. There is no patching, singular set, boundary, orbifold, or nontrivial sphere-bundle substitution.

The source's horizontal fields Hᵢ = ∂tᵢ + εXᵢ are orthonormal and perpendicular to the round vertical sphere. Their flow acts by fiber isometries. Substitution in the Koszul formula gives the listed connection, with round vertical connection, ∇H₁H₂ = F/2, ∇H₂H₁ = −F/2, and the mixed terms, where F = [H₁,H₂] = −ε²X₃. The final mixed identity follows from zero torsion. Thus this is the unique metric-compatible torsion-free connection of the stated Riemannian metric. It is not an auxiliary affine connection.

I checked the signs in D₁F = −ε³X₂ and D₂F = ε³X₁, as well as the four cases in the curvature calculation. The sign convention gives unit positive curvature on the round sphere. The negative horizontal sectional curvature −3|F|²/4 is expected; the theorem does not assert positive sectional curvature.

## 4. Why the calculation covers every plane

For a unit simple bivector α in four dimensions, the self-dual and anti-self-dual components each have norm 1/√2. Conversely every pair of unit vectors in the two Hodge summands gives a unit simple bivector after this normalization. Averaging the curvature of α and *α cancels the off-diagonal Hodge blocks. Thus the minimum biorthogonal curvature is exactly half the sum of the two least diagonal-block eigenvalues. The two minimizations are independent; no restricted class of planes is being substituted.

Write r² = |F|² and q = ⟨∇ˢe₁F,e₂⟩. Expanding the full curvature tensor in the two Hodge bases gives

A± = [[a±, b±ᵀ], [b±, c±I₂]],

a± = 1/2 − 3r²/8 ± q, and c± = r²/8 ∓ q/2.

Both off-diagonal vectors, including their signs, agree with the source. In particular the quantities needed for the estimate satisfy

r² = ε⁴(1 − z²), |q| ≤ ε²,

|b₊|² + |b₋|² = ε⁶(1 + z²)/8 ≤ ε⁶/4.

For 0 < ε ≤ 1/4,

a± − c± ≥ 1/2 − ε⁴/2 − 3ε²/2 ≥ 207/512 > 1/4.

An independent way to check the eigenvalue estimate is to complete the square in the quadratic form of A − cI. For δ = a − c > 0,

δx² + 2x(b·y) = δ(x + b·y/δ)² − (b·y)²/δ.

Cauchy–Schwarz therefore gives λmin(A) ≥ c − |b|²/δ. Applying δ > 1/4 to each block, averaging, and using cancellation of q yields

k(gε) ≥ r²/8 − 2(|b₊|² + |b₋|²)
       ≥ ε⁴(1 − z²)/8 − ε⁶/2.

This is a uniform estimate on the entire Grassmannian at every point, with no asymptotic remainder or unproved small-parameter threshold.

## 5. Conformal correction and exact positive bound

For ĝ = u²g in dimension four, the two complementary sectional-curvature transformation formulas sum to

K⊥(ĝ,σ) = u⁻²[K⊥(g,σ) − Δg u/(2u)].

I checked the connection-difference calculation and the gradient-square sign. Conformal scaling preserves orthogonal complements, and the correction is independent of the plane. The convention is Δ = div grad.

The source's frame computation gives

Δgε φ = ΔS² φ + ε²(X₁² + X₂²)φ

for functions depending only on the sphere. Acting on z² gives (1 + ε²)(2 − 6z²). The factor 1 + ε² in

uε = 1 + ε⁴z²/[24(1 + ε²)]

is therefore necessary and correctly included. Put Φ = (1 − z²)/8. Then Δgεuε/2 = ε⁴(Φ − 1/12), exactly. The corrected lower bound is

ε⁴uε⁻²[1/(12uε) + (1 − 1/uε)Φ − ε²/2]
≥ ε⁴uε⁻²[1/(12uε) − ε²/2].

The discarded term is nonnegative because Φ ≥ 0 and uε ≥ 1. On the stated interval uε < 2 and ε² ≤ 1/16. Thus the bracket is at least 1/24 − 1/32 = 1/96 and uε⁻² ≥ 1/4. This proves the claimed lower bound ε⁴/384 > 0 everywhere. At ε = 1/4, the conformal coefficient is 1/6528 and the lower bound is 1/98304, exactly as stated in the packet.

The sphere poles and limiting ε → 0 are not exceptions: the metric and conformal factor are globally smooth, the inequalities include z² = 1, and ε = 0 is only the non-strict round–flat limit, excluded from the positivity range.

## 6. Independent controls

The supplied six-point diagnostic was read and rerun successfully. It remains a finite diagnostic, not the source of the global proof.

The audit adds `independent_controls.py`, using a covariant second-metric-derivative curvature formula rather than differentiating the upper Christoffel symbols as in the frozen checker. Its results are in `independent_results.json`.

The new checks:

1. Verify the stereographic metric, the three rotation fields from their ambient cross-product definitions, and outward orientation.
2. Compute all 36 base curvature-operator entries symbolically in both chart coordinates and ε, and match every source entry, including zeros.
3. Check both complete Hodge blocks, including the b vectors, and their summed squared norm.
4. Check the algebraic Bianchi relation and the ε = 0 round–flat curvature operator as independent sign and normalization controls.
5. Recompute the Laplacian in coordinate divergence form, checking the full symbolic conformal-correction identity.
6. Differentiate the conformally modified metric itself at two exact asymmetric rational points, with ε = 1/4 and ε = 1/8, then verify every entry of the two transformed Hodge blocks against the predicted scalar shift. These points have nonzero conformal derivatives.

The base identities are symbolic on a sphere chart, rather than a larger finite sample. Since the original construction is smooth, the tensor identities extend across the omitted pole; all-plane positivity is established by the analytic inequalities above. No floating-point tolerance, random sampling, or numerical optimizer is part of the acceptance argument.

## 7. Repairs and promotion limits

**Required mathematical repairs: none.**

No change is needed to the exact claim, metric, parameter interval, uniform bound, attribution, or zero-turn accounting. Keep the recent-preprint qualification and the live-site access limitation. The frozen packet's “independent review pending” fields are historically accurate for the frozen input; this separate report supplies the subsequent review. If the publication editor elects to update those fields or include this audit in a later publication bundle, it must create a new manifest rather than silently change the reviewed frozen bytes.

Optional clarity only: the frozen diagnostic's Hodge-specific assertions explicitly check the diagonal pattern and lower off-diagonal zero, while its full curvature equality already implies the remaining block entries. The independent checker added here explicitly checks the complete blocks. This does not invalidate the existing diagnostic or require a repair to the mathematical certificate.

This audit independently verifies the mathematical source resolution and packet integrity. It does not independently repeat every GitHub history/queue scan in the gate report, certify the current inaccessible problem site's wording/status, or authorize any remote write. The local pinned records were compared for identity and their August status is correctly superseded by the September construction. Third-party PDFs, HTML, and screenshots remain outside the public packet. No remote files, PRs, releases, DOI deposits, or messages to authors were created.
