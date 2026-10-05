# Source gate: spectral reconstruction of diffusion tensors

Target30003508 / OWR-15432-001, queue rank322. Checked2026-10-02. Substantive author turns consumed:0/5.

## Full original scope

The original contribution is Markus Reiß, with Jakub Chorowski, Emmanuel Gobet and Marc Hoffmann, “SDE estimation from discrete observations as inverse problems,” in OWR24/2017, printed pp1507–1509. The full contribution was read, and the displayed multidimensional paragraph on p1509 was visually checked. DOI10.4171/OWR/2017/24 refers to the2017 workshop; publication was in2018.

The context is stationary low-frequency observations X_(nΔ), Δ>0 fixed, N→∞, of a reflecting diffusion on a bounded domain D⊂R^d, d>1. Its reversible generator is Lu=μ^(-1)div(S∇u), where S is positive definite and Σ=2S/μ. The eigenfunctions satisfy div(S∇u_k)=ν_k μu_k with Neumann boundary conditions. The paper asks for convergence analysis of reconstructing S from empirical versions of both eigenpairs and μ, with K still to be chosen.

The source does not specify a fixed multidimensional least-squares objective, regularization parameter, smoothness class, eigenfunction noise norm or choice of K. These are parts of the requested construction and analysis, not supplied hypotheses. In particular, an arbitrary prescribed noisy finite list does not come with a convergence regime. A result restricted to one-dimensional or isotropic scalar conductivity does not settle this target. Neither a finite-K nonidentifiability example nor a deterministic theorem assuming unproved eigenpair convergence would alone settle the intended statistical question.

For a symmetric matrix coefficient, the natural Neumann condition in a self-adjoint divergence-form weak formulation is the conormal condition n·S∇u=0. Ordinary normal differentiation cannot be substituted silently. Eigenvalue multiplicities and empirical basis alignment also require care. The original adjective empirical/noisy refers to finite-sample estimation error; additional sensor-noise/HMM assumptions are not part of the original statement.

## Success test

Provide a concrete spectral-reconstruction estimator for a stated nonparametric class of general symmetric positive definite matrix fields and unknown invariant densities, select its retained eigenpairs and regularization consistently, and prove convergence from the low-frequency observation model. Every added regularity, compactness or excitation hypothesis must be explicit; assumptions that encode the missing inverse stability or statistical consistency are an identified gap rather than a solution. Rates are valuable but the source's stated target is convergence. A restricted deterministic theorem should be labeled as a scoped partial.

## Source retrieval and prior-work gate

The requested unsolvedmath URL was attempted and was inaccessible. The fallback used the repository's pinned UnsolvedMath snapshot37e53eabe540fb458758e198be61634bd02ee008. The complete imported record was read. The local problems.json and research_results.json matched the manifest sizes and SHA-256 hashes exactly. No research-results key matching OWR-15432-001 or15432 is present, so there is no attached upstream prior report to reuse.

Live exact-ID PR and branch searches were empty. Title and spectral/diffusion PR searches were empty. Main has no attempts/30003508 directory and no path commits. A recovered374-ref repository has no exact-ID/path/title matching author history. Code search returned only desk-review assignment metadata. Related-target groups contain no match. Main state has no entry; catalog/assessment records show queued0/5 and no holds. The review hash is b6b5099c060375a6bcea8613927d04f5394016b6ca8d0006603a93a83d164917. No prior campaign attempt was found.

## Current primary-literature check

Giordano and Wang, “Statistical algorithms for low-frequency diffusion data: a PDE approach,” Annals of Statistics53(2025),1150–1175, DOI10.1214/25-AOS2496, arXiv2405.01372v3, was checked in its introduction and model definition. It studies the scalar conductivity f in L_f=div(f∇), with a uniform invariant distribution, and evaluates likelihoods/gradients using elliptic spectral problems. Section1.3 explicitly identifies anisotropic matrix-valued conductivity as a future extension. It does not establish the requested general-tensor empirical-eigenpair reconstruction theorem. Its cited Bayesian scalar-conductivity consistency results likewise must not be generalized without proof.

The source's2004 Gobet–Hoffmann–Reiß result and Chorowski's frequency-adaptive work concern scalar one-dimensional diffusions. Narrow current searches found no exact tensor spectral-consistency resolution. This is a bounded literature check, not a worldwide novelty certificate.

## References

- Full original report: https://publications.mfo.de/bitstream/handle/mfo/3588/OWR_2017_24.pdf
- Official report identity: https://ems.press/journals/owr/articles/15432
- Giordano–Wang author manuscript: https://arxiv.org/pdf/2405.01372
- Scalar spectral baseline: https://arxiv.org/abs/math/0503680
- Scalar frequency-adaptive baseline: https://arxiv.org/abs/1507.07139

Source PDFs and imported record copies are local-only. This checkpoint contains no substantive proof attempt and consumes no author turn. Completion estimate5%, subjective and uncalibrated.
