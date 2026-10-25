# Independent adversarial review — Zenodo 23356680

**Verdict: PASS — no substantive mathematical defect found in the claims as written.**

Reviewed: Alec Kriebel, *A smooth Reshetnyak-harmonic sphere with unbounded distortion*, version 1.0, dated 13 October 2026. All six published pages, the corresponding TeX, the package verifier and its replay scope were inspected. The two mathematical proof chains were reviewed independently before using archived computed results. No archived reviewer narrative or sibling review opinion was consulted. This is an AI-assisted adversarial review, not human peer review or a formal proof certificate.

## Identity and scope

- Published PDF: `sources/harmonic-sphere-energy-v1.0.pdf`, SHA256 `a35dae6189ec49ed00e90ac38eeeda3f72a9e6737221de62554e913ed1157125`.
- Published ZIP: `sources/harmonic-sphere-source-verification-v1.0.zip`, SHA256 `956dfbc0366eae1122ef00f0a7a8535841101f84a46234659bd0476dfa1e7968`.
- The fresh public PDF agrees with the original PDF supplied for this assignment. `input_identity.json` records the full paths. The package verifier binds its included PDF to this separately acquired PDF.
- Audit location: this directory. Downloaded primary-reference PDFs, the isolated published package and the pinned Python environment are ignored locally; their hashes and reproducible commands are retained. No website, spreadsheet, repository, release, Zenodo or outreach action was performed.

The target claims were treated as hypotheses. The principal falsification targets were: weaker meanings of harmonicity silently substituted for local minimization; a calibration only valid for image-restricted or continuous competitors; invalid critical-Sobolev Stokes reasoning; singularities at poles or seams; distortion only on a null set; confusion between local and homotopy-global minimizers; differentiating a nonsmooth seminorm; an unjustified global Hopf differential; and application of a pointwise theorem outside its hypotheses.

## Strongest verified result

The specified compact smooth Riemannian two-sphere admits the specified smooth homeomorphism from the round sphere that minimizes Reshetnyak energy in a neighborhood of every point against **every same-trace (W^{1,2}) competitor in the entire target**. Its singular-value ratio is (t^{-2}) on the punctured central belt, so no finite bound holds almost everywhere. The target satisfies the stated geodesic, local quadratic isoperimetric and small-sphere null-homotopy conditions.

The separate Korevaar–Schoen claim is also supported: in the standard essentially separably valued metric-Sobolev framework, local KS minimization on the two-sphere yields a globally vanishing angular stress and hence the stated uniform infinitesimal quasiconformality bound. The written proof of (4+\sqrt{17}) is valid; the stated older (2\sqrt2+\sqrt6) bound applies through the paper's additional SL(2)-minimality argument. Neither constant is presented as a new optimal bound.

**Exact remaining mathematical gap found:** none. The scope remains the energies and local-minimizer definition explicitly stated in the paper. First priority, novelty relative to all literature, and the wording or openness of a later 2026 journal version are not established by this review.

## Full proof audit

### 1. Meaning of harmonic and the energy distinction — pages 1–2

The local quantifier is strong enough: for each source point, one neighborhood works for every relatively compact Lipschitz subdomain and every same-trace metric Sobolev competitor. It is not merely stationarity, a small-amplitude variation test, or comparison within the reference image or homotopy class. The cited 2025 definition matches this quantifier.

In conformal source coordinates, the source conformal factor cancels for both two-dimensional energies. For a smooth Riemannian target the Reshetnyak density is the squared operator norm, whereas KS is a positive normalization of the sum of squared singular values. Comparable energies need not have the same minimizers. Zero metric seminorms satisfy the paper's quasiconformality convention; nonzero rank-one seminorms do not.

### 2. Belt calibration with unrestricted target excursions — Lemma 3, page 2

The critical assumption is Lipschitz control of the selected flat coordinate for the **ambient target distance**. A sufficiently small strongly geodesically convex ball contained in the flat patch supplies it. There is therefore a single global 1-Lipschitz scalar extension agreeing with the angular coordinate throughout the chosen image neighborhood.

For any competitor (v), composing with that extension gives a scalar Sobolev map (f) whose trace is the affine coordinate (x), with (\int|\nabla f|^2\le E_+^2(v)). Writing (f=x+w), where (w\in W_0^{1,2}), the cross term integrates to zero by scalar Sobolev approximation. Thus (\int|\nabla f|^2=|\Omega|+\int|\nabla w|^2\ge|\Omega|). The reference derivative has operator norm one because (|h'|\le1). This proves the full comparison, including competitors that leave the flat patch or wrap around the angular coordinate. The proof does not require a globally defined target angular coordinate.

### 3. Cap calibration at critical Sobolev regularity — Lemma 4, pages 2–3

After shrinking the source neighborhood, the cutoff can equal one near its image and have area integral (0<a<A/2). The form (omega=((1+b)\eta-b)dA), (b=a/(A-a)), has coefficient in ([-b,1]), equals the area form near the reference image and has zero total integral. On the oriented sphere this makes it globally exact, with a smooth primitive (alpha). In particular, a whole-sphere bubble contributes zero to this chosen form; using the nonexact area form globally would not have justified that conclusion.

The Sobolev identity is adequately proved. Write the global one-form as a finite sum (f_j,dg_j) of global smooth functions, using cutoffs in a finite atlas. Their compositions with a compact-target Sobolev map are bounded (W^{1,2}) scalar functions. For bounded scalar (F,G\in W^{1,2}_{\mathrm{loc}}), bounded mollifications give (F_\epsilon dG_\epsilon\to FdG) in (L^2) and (dF_\epsilon\wedge dG_\epsilon\to dF\wedge dG) in (L^1). Consequently (d(v^*\alpha)=v^*d\alpha) distributionally. No density of smooth target-valued maps is assumed.

Matching traces permit gluing (v) inside the Lipschitz domain to (u) outside it. The difference of the pulled-back primitives is an (L^2) one-form with compact support in the source neighborhood. Testing its derivative against a cutoff identically one on that support yields equality of the two (omega)-integrals. The pointwise bound (v^*\omega\le|\operatorname{Jac}v|\le\|dv\|_{\mathrm{op}}^2), with equality for the reference conformal map, finishes the comparison. Orientation reversal, different degrees, arbitrary image excursions and noncontinuous (W^{1,2}) competitors cause no unaccounted boundary term.

### 4. Smooth target, homeomorphism, coverage and limiting cases — pages 3–4

The bump quotient has positive denominator and is flat at its endpoints. The target conformal factor is one for (|s|\le2) and exactly (e^{-|s|}) for (|s|\ge3). The two stated exponential coordinates make the metric exactly Euclidean near each added pole. The absolute value at zero is harmless because its multiplier vanishes on a neighborhood of zero. Thus the compactification is a smooth positive Riemannian metric, not a conical or cusp completion.

The function (a) is smooth, even, lies in ([0,1]), vanishes only at zero, equals (t^2) in the central interval and one outside the transition. Its integral (h) is strictly increasing despite (h'(0)=0), tends to the correct infinities and is a homeomorphism. Near each pole the map is exactly multiplication by (e^c) in the appropriate smooth coordinates, so it is globally smooth. Smooth invertibility at the equator is neither claimed nor required.

For (|t|<1), the reference image lies inside the flat belt and the scalar calibration applies after choosing a sufficiently small convex target ball. For (|t|>1/2), including the poles, the map is orientation-preserving conformal and the cap calibration applies. These are overlapping open regimes, leaving no transition-circle gap.

Compact smooth geometry gives a uniform contractible normal-ball scale and geodesicity. A sufficiently small-diameter sphere image lies in one such ball. A sufficiently short Lipschitz loop lies in a controlled chart; the radial cone remains in a convex Euclidean chart image, has finite Sobolev energy and area bounded by a constant times squared length, and retains the given boundary parametrization. Returning to the manifold preserves a uniform quadratic area bound.

The distortion is unbounded on sets of **positive round area**: on (0<|t|<1/4), the ratio is exactly (t^{-2}), with the common source conformal rescaling canceling. For any finite (Q), the band (0<|t|<\delta<\min(1/4,Q^{-1/2})) has round area (4\pi\tanh\delta>0). The null equator alone is not being used as a counterexample.

### 5. Admissible energy and two nonclaims — page 4

The maximum-square seminorm energy has the required homogeneity, monotonicity and rotation invariance. Its unit sublevel is compact: the restrictions of the seminorms to the unit circle are bounded and uniformly Lipschitz, and the limit retains the seminorm axioms. Convexity of the squared operator norm and the average-derivative identity prove the stated quasiconvexity condition, including its normed-target formulation.

The conformal coordinate identity has Reshetnyak energy equal to target area and is homotopic to (u). The change of variable (s=h(t)) gives an excess (4\pi c>0) for the example. Therefore local minimization does not incorrectly become minimization over its homotopy class.

Within a positive central rectangle, the KS first variation under a nonnegative compactly supported first-coordinate perturbation is (-4\int t\psi<0). The variation stays in the flat patch for small parameter. This directly excludes KS harmonicity of the example. The nonsmooth operator-norm energy is not assigned the unique global stress later used for the KS proof.

### 6. General-target KS argument — pages 4–5

I independently derived the angular change of variables: its Jacobian is (det A/|Av|^2), and homogeneity produces the additional inverse-length factor. The displayed denominator (pi(det A)^2|A^{-1}w|^4) is correct. It makes the transformed energy smooth in (A) even when the underlying seminorm has corners or a kernel; differentiation does not require differentiating the seminorm itself. Uniform derivative bounds by (CM(s)^2) are integrable for a metric Sobolev map.

The approximate metric chain rule and a domain change of variables hold the seminorm at the new fixed point. The matrix factor is (D\phi_\epsilon\circ\phi_\epsilon^{-1}); differentiating at zero gives (DV). A compactly supported field is an admissible fixed-trace variation for both signs, on a Lipschitz subdomain inside a minimizing chart. This yields the distributionally divergence-free, symmetric, tracefree stress.

Writing the matrix as [[a, b], [b, −a]], the divergence equations give the Cauchy–Riemann equations for (a-ib). Distributional holomorphic regularity, the explicitly checked scaling/rotation covariance and holomorphic coordinate changes make this a global holomorphic quadratic differential. The poles each have their own local minimizing equation; no missing puncture-removal hypothesis enters. A holomorphic quadratic differential on the sphere vanishes, as follows from the entire coefficient in a plane chart and its (O(|z|^{-4})) behavior at infinity.

For a nonzero normalized balanced seminorm, choosing a minimizing direction and its perpendicular gives (L^2\ge1-m^2) by the triangle inequality. Comparing with (r(v)=L|v_1|) gives (|s^2-r^2|\le2m) and stress difference at most (8m); direct circle integration gives (T(r)=L^2\operatorname{diag}(1,-1)). Thus (1-m^2\le8m), excluding nonzero rank-one differentials and yielding (M/m\le4+\sqrt{17}). The zero seminorm is correctly treated separately.

For the stronger inherited bound, (J(A)=I(s\circ A)) is convex and differentiable at the identity by the same angular formula. Balance makes its derivative (I(s)\operatorname{tr}D). The supporting-plane inequality on positive determinant-one symmetric matrices and polar decomposition prove actual SL(2)-minimality, not merely stationarity on that group. The pointwise older bound therefore applies. For inner-product seminorms the exact formula is (T=2G-\operatorname{tr}(G)I); for general norms, fourfold symmetry can make the stress zero without Euclidean roundness, as the paper correctly acknowledges.

## Primary-source scope checks

The successful downloads, hashes, precise inspected material and failed retrievals are in `reference_sources.json`.

- [Meier–Vikman–Wenger, arXiv v1](https://arxiv.org/pdf/2503.08553v1): Question 1.9 uses the general fixed-energy setting; Definition 3.1 includes the two energies at issue; Definition 6.1 has the neighborhoodwise all-competitor local quantifier. The global homotopy-minimizer result implies local minimization, not its converse. These are the scopes used in the note.
- [Meier's Oberwolfach contribution](https://ems.press/content/serial-article-files/52249?nt=1), pp.1624–1626: checked the target assumptions and Question 1 on p.1625 against the paper's historical characterization.
- [Lytchak–Wenger, *Energy and area minimizers*](https://arxiv.org/pdf/1507.02670): checked pointwise SL(2)-minimality and the bound in Lemma 3.1/§3.3. The disk-reparametrization statement in Lemma 4.1 is stronger than fixed-boundary local comparison; the note does not incorrectly invoke it to make the Reshetnyak example quasiconformal. The exact author-hosted manuscript link timed out, so the successfully retrieved primary arXiv copy is the scope of this inspection.
- [Lytchak–Wenger, *Area minimizing discs*](https://arxiv.org/pdf/1502.06571): checked the metric-derivative energy representation (Proposition 4.6), chain rule (Lemma 4.9) and trace/gluing discussion. These apply in the stated complete-target Sobolev framework without an NPC assumption.
- [Logaritsch–Spadaro](https://arxiv.org/pdf/1112.0122), Theorem 0.1 and surrounding discussion: independently corroborates the directional representation and the distinction between these energies. The separable-target statement is compatible with the standard essentially separably valued framework.

The original KS93 publisher DOI was inaccessible in the browser. I did not read or claim a full review of that 99-page original article; the exact imported calculus is available in the primary treatments above and the key new first-variation computation is proved in the note. The scalar extension formula and exact-form comparison were checked directly, not accepted solely because the bibliography cites classical work. No exhaustive priority search or authentication of the 2026 final article was performed, and the reviewed note expressly disclaims those stronger historical claims.

## Checkable computation and replay

`fresh_controls.py` was written independently from the displayed equations without importing the archived checks. Its result is `fresh_controls.json` and its console record is `fresh_controls.log`. It passes **53 controls: 13 exact families and 40 numerical diagnostics**.

The exact controls include the inner-product and rank-one stress tensors, matrix first variation, rotation covariance, three scalar calibration polynomial examples, three fixed-boundary Jacobian-integral examples, an explicit negative KS variation, the algebraic distortion constant and an unbounded rational distortion sequence. One fixed-boundary Jacobian example has value (-1859/16) at an interior point but total integral one, testing that orientation reversal does not invalidate the exact-form identity. On the rectangle (1/16<t<3/16, 0<x<1), the chosen nonnegative polynomial Sobolev perturbation has KS derivative exactly **(-1/58982400)**. Smooth compactly supported nonnegative approximants preserve this strict sign.

The numerical checks cover the transition, the angular substitution and its derivative for Euclidean, (ell^1), (ell^infty), anisotropic (ell^infty), rank-one and zero seminorms, plus non-Euclidean fourfold balance. With 131,072 angular samples, the maximum tested substitution discrepancy is (3.43\times10^{-9}) and the maximum derivative discrepancy (6.93\times10^{-7}). The numerical transition integral is approximately (c=0.372427320021913), consistent with the proved interval (47/192<c<1/2). These are floating-point diagnostics, not rigorous error enclosures or proofs of universal statements.

The **complete published package verifier passed** in an isolated copy with the package's pinned versions: NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 and mpmath 1.3.0. Exact command, from this review directory:

```sh
PYTHONDONTWRITEBYTECODE=1 tmp/replay-venv/bin/python tmp/package/verify_package.py --pdf /Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23356680/sources/harmonic-sphere-energy-v1.0.pdf
PYTHONDONTWRITEBYTECODE=1 tmp/replay-venv/bin/python fresh_controls.py
```

The initial attempt used an existing environment and stopped on the verifier's exact dependency-version guard. Its stderr is preserved separately; no source modification was needed. The successful result is `archived_package_replay_pinned.json`, with empty corresponding stderr and exit code zero. It reports 257 byte-identical author exact controls, 673 executed historical mixed checks (two historical source-PDF identity checks intentionally omitted by that replay mode), another mixed audit within its stated tolerance, six additional proof-control families, KS controls, 43 additional exact controls, 67 original integrity mutations and 19 additional integrity mutations. The mixed audit output is **not** byte-identical; it passes its specified numerical comparator. Primary-source retrieval and inspection in this review are separate from that source-free replay.

The package manifest hash reported by the successful verifier is `e96eb05184d4e3e468bebd09bd828eef341867a7ff709346b4375c58faed557b`. Hash/inventory and mutation checks establish reproducibility and binding, not analytic correctness. Neither the archived count nor the fresh count formally verifies all Sobolev maps or establishes priority.

## Disposition and limits

No substantive defect, hidden missing hypothesis or invalid comparison was identified. Both main theorems and the explicit distinctions are supported by the written arguments and the stated primary-source inputs. There is no deferred mathematical repair from this review.

Any public presentation should preserve the words **Reshetnyak**, **local minimizer**, and **unrefereed**. It should not imply the example is KS harmonic, minimizes its homotopy class, disproves a theorem about such global minimizers, establishes first priority, settles unchanged 2026 wording, or has received independent human/journal peer review. This verdict concerns mathematical readiness under the assigned gate; it is not itself publication authorization.
