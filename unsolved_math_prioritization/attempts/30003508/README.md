# Fixed-lag spectral consistency for smooth reversible diffusion tensors

**Target 30003508 / OWR-15432-001. Status: claimed_solved, 2/5 substantive author turns.** Independent analytical and source-scope review passed. The claim is the precise consistency theorem below. Historical priority is not established. This is an AI-assisted research draft, not human peer review or formal verification.

## Theorem and observation model

Let D be a known bounded connected C∞ domain in R^d, d ≥ 2, and Δ > 0 a known fixed observation lag. Let S = Sᵀ and μ be smooth on the closure, with known bounds ell I ≤ S ≤ Lambda I, 0 < c ≤ μ ≤ C, and integral_D μ = 1. Observe exact stationary positions X_0, X_Δ, …, X_(NΔ) from the reflecting diffusion with generator

    Lu = μ^(-1) div(S ∇u),       n·S∇u = 0 on the boundary.

Both the anisotropic tensor S and invariant density μ are unknown. In the source's notation the diffusion covariance is Σ = 2S/μ.

The specified weighted spectral estimator converges almost surely to S, locally uniformly in the interior. The separately fitted divergence coordinates converge locally uniformly to div S. Projection of its symmetric tensor onto the known ellipticity interval gives almost-sure L²(D) convergence. The result is pointwise consistency at each fixed parameter pair in the stated nonparametric class.

The estimator constructs boundary-corrected smooth empirical density and symmetric finite-rank transition-kernel estimates from consecutive observations. It uses all positive empirical eigenpairs, weights κ⁴, and any positive ridge tending to zero. The retained spectral count is finite and data dependent. A continuous-functional-calculus formulation handles repeated eigenvalues and the small/negative empirical spectrum. Full spectral-jet identification and the required empirical derivative convergence are proved, rather than assumed.

## Prior work and contribution claimed

Crommelin and Vanden-Eijnden's 2011 paper, [Diffusion Estimation from Multiscale Data by Operator Eigenpairs](https://ir.cwi.nl/pub/18934/), already develops spectral fitting of drift and diffusion, including multidimensional examples. This package does not claim to invent spectral fitting. The claim here is a proved fixed-lag almost-sure nonparametric consistency theorem under the explicit smooth stationary reversible model above, including unknown invariant density and general matrix coefficients.

The 2011 manuscript's §§3.2 and 4.2 defer a detailed general convergence analysis and infinite-expansion nonparametric treatment. Ren–Lu–Ying–Rotskoff's AAAI 2024 bound retains a sampling-interval bias and does not establish this fixed-positive-lag result. These bounded comparisons do not establish historical priority or rule out other prior theorems. See the preserved [primary-source comparison](review/PRIOR_SOURCE_COMPARISON.md).

The original source is Markus Reiß's contribution with Chorowski, Gobet and Hoffmann, “SDE estimation from discrete observations as inverse problems,” [OWR 24/2017, pp. 1507–1509](https://publications.mfo.de/bitstream/handle/mfo/3588/OWR_2017_24.pdf). The independent review finds that this smooth-class construction answers its informal convergence request with the stated regularity qualifications.

## Proof and audit

1. [SOURCE_GATE.md](SOURCE_GATE.md): exact original model, provenance and prior-attempt audit
2. [TURN_1.md](TURN_1.md): deterministic spectral reconstruction, multiplicity-safe normal equations, identification, and clipping
3. [TURN_2.md](TURN_2.md): explicit empirical construction and almost-sure kernel convergence for dependent fixed-lag observations
4. [Independent analytical/source review](review/ADVERSARIAL_REVIEW.md) and [additive literature comparison](review/PRIOR_SOURCE_COMPARISON.md)
5. [REVIEWED_STATE.json](REVIEWED_STATE.json): current disposition and [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json): exact packet hashes

All 15 author files at commit 152882a5cfb85f09635d131db83c1e19118f4c98 are preserved byte-for-byte, including their historical pending-review descriptions. The two original author manifests and both review manifests are unchanged. This README and REVIEWED_STATE.json record the later disposition; they do not rewrite historical states.

Run the following with Python 3 and SymPy (1.14.0 used):

    python verify_turn1.py
    python verify_turn2.py
    python review/independent_controls.py

The 53 author algebra checks and 1,905 independent exact controls pass and reproduce the saved receipts. Finite algebra controls supplement, but do not prove, the elliptic regularity and probability arguments reviewed in the report.

## Limits

No minimax or uniform rate, rough-domain/coefficient theorem, nonreversible result, additional sensor-noise model, efficient implementation, or numerical quadrature/eigensolver error guarantee is claimed. No globally uniform boundary convergence for the reconstructed tensor derivatives is asserted. Smooth boundary and coefficient assumptions, stationarity, exact observations, and known positive class bounds are part of the theorem. No mathematical gap was found within this scope; historical priority remains unestablished.
