# Independent adversarial audit: Function Theory 6.10

Problem 2306010 / AMR-022-6010, queue rank 581. Reviewed 2026-10-04 UTC.

## Verdict

**PASS.** The frozen packet gives a complete conventional reconstruction of the
Guo–Hu counterexample. It establishes the exact exterior-domain question, including
the geometric convexity of the omitted sets, and supports **already_solved, 1/5**.
No mathematical repair is required. The construction and priority belong to
Yuankai Guo and Xiaozhe Hu; this audit makes no new-solution claim.

The accepted input is the nine-file public packet whose `SHA256SUMS.json` has
SHA-256 `3927dbc7cf71fe73904c037e36772a08cb17157e0bfed8104e5ffc7fa356f1e2`.
All eight listed file digests and the exact public file set were independently
checked. No frozen file was edited, no helper was used, and no remote write was made.

This is a mathematical and source audit, not a Lean certification. No Lean build
or full dependency/axiom audit was performed. Neither the preprint's formalization
claim nor the execution of finite arithmetic tests is used as a substitute for proof.

## 1. Target and prior resolution

The original source is Hayman–Lingham, [2018 arXiv v2](https://arxiv.org/abs/1809.07200v2).
The exact question and historical update were checked on printed p.119, PDF p.120,
including a page-image review. The notation on printed p.114, PDF p.115, was also
read and independently rendered for visual review. It requires analytic univalence
on |z|>1 and Laurent normalization z plus negative powers, with zero constant term.
The question asks whether convexity is preserved when two convex members of that
exterior class are combined with a real weight strictly between zero and one.
It is distinct from the unit-disk question immediately following it.

The answer is furnished by Guo–Hu,
[arXiv:2609.04279v1](https://arxiv.org/abs/2609.04279v1).
The primary landing page was freshly opened and gives the authors and submission
date 3 September 2026. The [primary HTML](https://arxiv.org/html/2609.04279v1)
was freshly checked against the cached six-page PDF, including its p.5 image.
The function definitions, parameters, branch evaluation, and exact negative
fraction agree. The primary license link resolves to CC BY 4.0. A fresh PDF web
request returned an internal fetch error; this does not affect the available
cached PDF plus fresh primary HTML evidence. Both cached source PDFs exactly match
the frozen source-manifest SHA-256 digests.

The landing page shows only v1. Two bounded searches using the arXiv identifier,
authors, correction/erratum/withdrawal, and counterexample/error terms did not
locate a correction or withdrawal. This is not a claim of exhaustive literature
coverage or peer review. The cached PDF's front-page manuscript date is 7 September,
whereas the HTML and arXiv submission record say 3 September; the packet correctly
uses the latter as the submission date. No chronology claim depends on the PDF date.

The selected imported statement and full previous OPEN-TRIAGE report were read.
They supply neither a competing proof nor a mathematical obstruction to the new
resolution. The packet correctly distinguishes the cached problem-corpus revision
from the repository's pinned revision. Repository duplicate checks in SOURCE_GATE
are a dated author snapshot; this audit does not assert a fresh live repository
absence check. Any publication worker must still perform its normal live gate.

## 2. Parameters and single-valued analytic primitive

The independent arithmetic starts with q=1/3−i/6, w=1−q³, r=399/400,
α=8/9+4i/9, β=w/r³. It confirms |α|²=80/81 and

    r⁶−|w|² = 2785244627851129 / 2985984000000000000 > 0.

Thus both |α| and |β| are strictly below one. The choice z₀=400/399 lies strictly
inside the exterior domain and λ=3/5 is admissible.

For any |β|^(1/3)<ρ<1, the binomial series for (1−βz⁻³)^(2/3) is analytic on
|z|>ρ, with normal convergence on compact subsets. The displayed primitive's
n-th term differentiates to binom(2/3,n)(−β)^n z^(−3n). Because 1−3n never vanishes,
there is no logarithm term. This is an explicit single-valued Laurent primitive,
so simple connectivity of the exterior domain is not being assumed. Its constant
term is zero and its first correction is βz⁻²/3, establishing G=z+O(z⁻²).
The word “rational” applies to parameters and Laurent coefficients, not to an
assertion that G itself is a rational function.

For the principal branch, |βz⁻³|<1 throughout this larger exterior neighborhood.
Hence 1−βz⁻³ lies in the right half-plane, where the principal logarithm is analytic.
The derivative G′=exp((2/3)Log(1−βz⁻³)) is nonzero there. Differentiating its log
gives G″/G′=2βz⁻⁴/(1−βz⁻³), with the correct positive sign and coefficient.
F, G, and their convex combination are therefore analytic across the unit circle.

## 3. Global injectivity, rather than local nonvanishing

The weighted-tail lemma is valid even on the closed exterior. For |z|,|v|≥1,
the factorization of u^m−w^m at u=1/z, w=1/v gives
|z^(−m)−v^(−m)|≤m|z−v|. Summing absolutely yields

    |f(z)−f(v)| ≥ (1−S)|z−v|,
    |f′(z)−1| ≤ S,

where S is the weighted absolute Laurent tail. S<1 consequently supplies both
global injectivity and a uniform nonvanishing derivative, including the boundary.
No path inside a nonconvex exterior domain is incorrectly integrated to infer this.

For a_n=|binom(2/3,n)|, the recurrence
a_(n+1)=a_n(3n−2)/(3n+3) is positive. With T_n=3na_n/2, direct cancellation gives
T_n−T_(n+1)=a_n and T_1=1. All partial sums of a_n are bounded by one; monotone
convergence gives their infinite sum at most one. Thus, for b=|β|<1,
S_G=Σ a_n b^n≤b<1. No unjustified evaluation at the endpoint of a binomial series
is needed. The exponent of the n-th primitive term is 3n−1, exactly cancelling
the denominator's absolute value in this weighted sum.

The exponents 1 and 3n−1 are distinct, and the positive real combination weights
give S_H=λ|α|+(1−λ)S_G<1. Therefore F,G,H all belong to the original normalized
class Σ. The stated stronger bound |H′|>1/300 is correct. Independently, using
|α|<179/180 and |β|<9999/10000 gives S_H<74747/75000<299/300.

## 4. Actual omitted-set geometry

This is the important interpretation gate. Analytic failure alone would not settle
the problem without a valid geometric implication. The packet supplies one.

### 4.1 Boundary, orientation, and the image of the exterior

The closed-exterior injection and boundary derivative nonvanishing make
γ(t)=f(e^(it)) a smooth regular Jordan curve. For a fixed y off γ and sufficiently
large R, f(Re^(it)) has winding number one about y because f(z)=z+O(1) at infinity.
The argument principle on the annulus gives the number of preimages as
1−Ind(γ,y). The inner contour is subtracted, as it must be for an annulus.

A clockwise Jordan boundary would have index −1 at interior points, giving two
preimages and contradicting injectivity. Thus γ is counterclockwise. Its bounded
region has no preimages in the exterior; every point of its unbounded complementary
component has one. Boundary points have no exterior preimage by closed-exterior
injectivity. Consequently the actual omitted set is exactly the compact closed
Jordan region K. There is no switch between convexity of an image and of its
complement.

### 4.2 Strictly positive turning implies convexity

The estimate |f′−1|<1 allows a periodic principal logarithm of f′ along the circle.
The tangent-angle lift θ=t+π/2+Im Log f′ has total increment 2π and derivative
Re(1+zf″/f′). If this is positive, it increases strictly through one full turn.
After rotating the tangent at any chosen point to the positive horizontal axis,
the curve's signed height increases until the tangent has rotated by π and then
decreases to zero. The height remains strictly positive between the endpoints.
Each tangent line supports the entire curve on its left.

Taking the compact convex hull C now places every curve point on ∂C. The hull has
interior because a Jordan curve is not collinear. The boundary of a planar convex
body is a Jordan curve; a proper Jordan subcurve of another Jordan curve is
impossible (remove a missing point and obtain an embedding of a circle into an
interval). Thus γ=∂C, and uniqueness of the bounded Jordan region gives K=C.
This proves the claimed global convexity, rather than asserting it from a picture
or a finite list of curvature signs.

### 4.3 Convexity forces the required nonnegative analytic expression

For a convex K, the counterclockwise regular boundary's tangent supports K on the
left. Its signed height above this tangent has a local minimum at the base point.
The second derivative there equals |γ′|θ′, so Re(1+zf″/f′)≥0 on |z|=1.
Since f′ has no zeros, P_f=1+zf″/f′ is analytic throughout the exterior and extends
at infinity with value one. Therefore P_f(1/ζ) is analytic in the unit disk and
continuous on its closure. Applying the harmonic minimum principle to its real
part yields Re P_f≥0 everywhere in the exterior.

All hypotheses of this necessity implication have already been proved for H.
There is no appeal here to an unchecked general exterior-convexity theorem.

## 5. Convexity of F,G and nonconvexity of H

Direct differentiation gives P_F=(1+αz⁻²)/(1−αz⁻²) and
P_G=(1+βz⁻³)/(1−βz⁻³). For |u|<1 the real part of (1+u)/(1−u) is
(1−|u|²)/|1−u|²>0. Because both parameter moduli are strictly below one, this
holds on the unit circle as well as outside it. Section 4.2 therefore proves
the convexity of the omitted sets for both input maps.

The fractional-power evaluation is legitimate, not just a formal cancellation:
q has positive real and negative imaginary parts and
(Re q)²−3(Im q)²=1/36>0. Thus −π/6<arg q<0 and −π/2<3arg q<0. The chosen logarithm
satisfies Log(q³)=3Log(q), and G′(z₀)=q². The same branch gives
z₀G″(z₀)=2w/q. Replacing the branch by the conjugate would be invalid.

An independent tuple-based Fraction implementation computed the component
derivatives first, formed D=H′ and N=D+z₀H″, and obtained

    D=(184794−557603i)/1800000,
    N=(5431206+2285603i)/1800000,
    N/D=(−54160961609+690164496000i)/69013985609.

The real quotient was separately checked with the integer dot product of N's
numerator with D's conjugate, divided by 184794²+557603². It is strictly negative.
If H's omitted Jordan region were convex, Section 4.3 would force the opposite
inequality at z₀. This contradiction proves actual geometric nonconvexity.
It is not necessary to mistake z₀ for a unit-circle point or to supply a sampled
plot. The argument also entails a negative boundary-turning value somewhere,
since otherwise the harmonic minimum principle would forbid the interior one.

## 6. Computation, formalization limits, and disposition

- Author replay: all **438** exact checks passed, including six negative controls.
  The entire stdout is byte-identical to frozen CHECKS.json.
- Independent audit implementation: **329** checks passed, including source/frozen
  hashes, independent exact arithmetic, six negative controls, and 96 finite
  coefficient controls. It imports no author verifier code.
- The weight-quadratic identity was independently checked coefficient by
  coefficient, not merely at the author's 21 chosen weights.
- These finite controls are supplementary. The infinite-series estimates,
  analyticity, injectivity, and topology are justified in the reasoning above.
- The pinned README and two final Lean entry points were inspected. The older
  MainTheorem conclusion denies the analytic positivity predicate; the later
  geometric entry point denies every SmoothExteriorConvexMap certificate for H.
  This distinction is properly disclosed in the packet. No claim is made that
  reading these files proves all imported definitions or dependencies correct.
- Neither `lean` nor `lake` was found on PATH; neither was installed or executed.

Recommended disposition: accept the complete, attributed reconstruction as
**already_solved** with **1/5 substantive turns**. Independent verification does
not create a second problem-solving approach or a new discovery. No additional
proof-attempt turn is mathematically needed. See CORRECTIONS.md for nonblocking
editorial notes and AUDIT_SHA256SUMS.json for this separate audit's file hashes.
