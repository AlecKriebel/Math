# Independent full source and proof review: diffusion tensor spectral estimation

2026-10-02. Verdict: **PASS_COMPLETE_SMOOTH_CLASS_STATISTICAL_CONVERGENCE**. No mandatory mathematical revision. The result must always retain its smooth bounded-domain, stationary reversible model and stated known class bounds. It is a consistency theorem, not a rate theorem, rough-coefficient theorem or numerical implementation guarantee.

## Frozen input and verification

Reviewed commit152882a5cfb85f09635d131db83c1e19118f4c98, branch dot/math-30003508. Author proof hashes:

- TURN_1.md: d7b56c39dd5d88ccb13796d40b363c44079b61682723a9ca35a866f6793eb4db
- TURN_2.md: e0bf8a8800a43136a381fc4c705f80e37dc7692f0859b478e794c4e6ca365f53
- TURN_2_MANIFEST.json: b37ec93e58a35af194a4844b0e2393461e59ce0182ad9b0d29f67d9cf4361280

Both manifests' bound files were hash-verified; both author checkers replayed in separate copies and reproduced their53-check receipts exactly. Independent code provides1,905 exact algebra assertions, covering differential jets in dimensions2–6, repeated-eigenspace rotations, independently solved extension coefficients and the stationary overlapping-pair covariance identity. Finite checks do not certify the elliptic or stochastic arguments; those were reviewed directly.

## Source scope assessment

The full Reiß contribution, printed pp1507–1509 in OWR24/2017, was read, and the multidimensional question on p1509 inspected visually. Its low-frequency fixed-lag setting, stationary bounded-domain reflection and self-adjoint divergence-form generator are explicit. Reversibility is therefore part of the source setting, not a newly imposed simplification. The source asks to determine the retained spectral information and analyze convergence of a tensor reconstruction with empirical eigenpairs and density; it does not impose a particular estimator or convergence rate. Primary source: https://publications.mfo.de/bitstream/handle/mfo/3588/OWR_2017_24.pdf .

The candidate supplies one construction for general symmetric matrix-valued S and unknown μ on a precise smooth nonparametric class. Smooth domain/coefficients and known positive class bounds are extra regularity specifications, transparently stated rather than inferred from the source. They do not encode inverse stability, spectral simplicity or the desired consistency. Almost-sure local uniform consistency, together with clipped global L² consistency, is a genuine convergence analysis of the requested spectral-equation approach. Thus the construction meets the informal source request with these regularity qualifications. It must not be described as covering every reflecting diffusion or every possible noisy finite eigenpair list.

The2025 Giordano–Wang primary paper studies a different scalar-conductivity likelihood method, and §1.3 explicitly lists matrix conductivity as a future extension: https://arxiv.org/pdf/2405.01372 . This supports the model distinction, not a novelty determination.

## Deterministic reconstruction

**Correct operator conjugation.** Reversibility gives a symmetric stationary pair density q. Conjugation by sqrt(μ) takes the true transition operator to a compact positive self-adjoint operator on ordinary L²(D), with strictly positive eigenvalues. The empirical operator may have negative eigenvalues; the proof does not take their logarithms.

**Exact finite normal equations.** The jet uses a factor2 on each off-diagonal Hessian coordinate, so pairing with the independent symmetric matrix entries and divergence gives div(S grad u) exactly. Treating divergence temporarily as a separate local unknown does not create nonidentifiability at the limit. The ridge equations define a unique finite-dimensional estimator even when the empirical design is singular.

**Continuous functional calculus and multiplicities.** W_n=M_nT_n gives W_n phi=κu. Thus each outer functional contributesκ, and the middle functions t_+² and t_+²log(t_+) produce the claimedκ⁴ andκ⁴logκ sums. Both middle functions are continuous at zero on a common spectral interval. Polynomial approximation therefore proves operator-norm convergence without matching individual eigenvectors or excluding collisions. The sums are exactly invariant under orthogonal changes inside repeated eigenspaces.

**Identification is proved.** If the true Gram form annihilates a vector, that vector annihilates the jet of every eigenfunction, since everyκ is positive. Every compactly supported smooth test function lies in all powers of the conormal operator domain. Graph-norm spectral convergence, elliptic regularity and Sobolev embedding give C² convergence of its spectral expansions. Cutoff affine and quadratic polynomials realize arbitrary gradient/Hessian jets at any interior point. The vector must vanish. The positive smallest Gram eigenvalue has a positive minimum on each fixed compact interior set, so no separate excitation hypothesis is concealed.

The smooth elliptic input is classical and applies to general strongly elliptic second-order operators with suitable first-order Neumann-type conditions, including conormal reflection. Grubb's primary account of Seeley theory, §2 and Theorem2.2, explicitly identifies all positive power domains with the corresponding Sobolev boundary-compatibility spaces: https://arxiv.org/pdf/1412.3744 . The finite-dimensional constant eigenspace causes no problem, and adding an identity shift handles it when using invertible-operator formulations. Positive-time semigroup smoothing and the same regularity justify the differentiated kernel/series expressions; they are not being assumed for a rough domain.

**Ridge and boundary conclusion.** The proof's uniform compact lower bound suffices for any positive ridge tending to zero; no unproved noise-to-ridge comparison is needed once this bound holds. Projection onto the known ellipticity interval is nonexpansive in Frobenius norm and leaves the truth fixed. Local convergence plus bounded projected error on a finite-volume domain gives L² convergence. No uniform boundary convergence of the reconstructed coefficient derivatives is asserted.

## Empirical construction and probability argument

**Boundary correction is genuine.** The seven reflected coefficients solve all matching equations through order6. Local chart cutoffs and a finite partition of unity produce a bounded finite-order extension agreeing with the original function. Mollifying the extension and changing variables in its finitely many reflection integrals yields actual deterministic kernels with derivative bounds h^(-d-r). Positivity and exact mass preservation are unnecessary. Tensor products of the extension handle the mixed derivatives of q. Smoothness of the true positive-time conormal heat kernel is available under the stated smooth uniformly elliptic assumptions.

**Actual observed pairs, not independent fictitious data.** The kernel estimate uses consecutive observed states and symmetrizes their empirical pair measure. Its expectation is exactly the smoothed reversible pair density. Its feature space is finite dimensional. Normalizing a smooth clipped marginal estimate gives positive density for every sample and does not alter derivatives eventually, because the truth lies strictly inside the clipping identity interval.

**Dependence control is sufficient.** Weighted Poincaré and ellipticity give a strict spectral gap for the fixed-lag Markov operator. Conditioning the overlapping pair observations at their meeting endpoints gives the covariance <r,P^(l−1)s>. Both conditional functions are centered and have L² norm bounded by the pair's centered norm. Summing the geometric covariance bound yields a variance constant times ||F||∞²/n. This works also for bandwidth-dependent F; the unknown gap constant need not enter the estimator's tuning schedule.

**Uniform derivative consistency.** At dyadic sample sizes the worst summand derivative bound is a polynomial in j, while n=2^j. A2d-dimensional net of mesh2^(-j/(4d)) has at most a constant times2^(j/2) points. Chebyshev at threshold1/(j+1) consequently leaves a summable polynomial times2^(-j/2). One additional derivative gives a deterministic polynomial Lipschitz bound and hence vanishing net interpolation error. The kernels exist in a fixed neighborhood, so nonconvexity of D does not invalidate the short-distance interpolation. The marginal argument is lower dimensional. Borel–Cantelli and vanishing deterministic bias establish the strong kernel convergence used in turn1, on one event. There is no premise that empirical eigenpairs are already consistent.

Dyadic data reuse still converges along every sample size, since floor(log2N) tends to infinity and uses only available observations. The finite number of positive empirical eigenpairs may vary; functional calculus already controls this variation and discarded nonpositive eigenvalues.

## Final disposition and limits

The two turns jointly establish the proposed explicit smooth-class statistical convergence theorem, after separate source and analytical review. The source's tensor and unknown-density difficulties are both addressed, and spectral multiplicities are handled without a simplicity assumption. No mandatory correction was found.

A result notice or abstract should say what is actually proved: almost-sure consistency of a specified weighted spectral estimator for smooth stationary reversible uniformly elliptic matrix diffusions on known smooth bounded domains, locally uniformly in the interior and in L² after clipping. It should not imply minimax rates, uniform rates over unrestricted smoothness norms, nonreversible models, rough boundaries, hidden observation noise, efficient computation, or numerical quadrature/eigensolver errors. The limited literature check does not establish priority. This is independent AI-assisted review, not human peer review or formal verification.
