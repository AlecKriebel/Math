# Candidate: spectral estimation of a reversible diffusion tensor

Target 30003508 / OWR-15432-001. Complete proposed candidate obtained in substantive turn 2/5. Independent mathematical and source-scope review is pending. No historical novelty or minimax-rate claim is made.

## Claim

On a known bounded connected smooth domain, for every smooth symmetric uniformly elliptic S and smooth positive invariant density μ within known class bounds, an explicitly defined weighted spectral equation-fitting estimator from a stationary fixed-lag diffusion sample converges almost surely to S locally uniformly in the interior. Its clipped tensor version converges in L²(D). Both S and μ are unknown.

The estimator uses all positive eigenpairs of a symmetric finite-rank empirical transition-kernel approximation, κ^4 weights, and vanishing ridge. It handles repeated eigenvalues and spurious small/negative empirical eigenvalues through continuous operator functions. No excitation or identifiability assumption is left unproved.

## Reading order

1. SOURCE_GATE.md: full original setting, exact provenance, prior-attempt audit and scope cautions
2. TURN_1.md: spectral jet estimator, deterministic consistency, identification and boundary handling
3. TURN_2.md: explicit construction of the empirical kernels/density and strong consistency from actual low-frequency observations
4. TURN_STATE_v2.json: current candidate status. Prior states and manifests remain unchanged

Run python verify_turn1.py and python verify_turn2.py (SymPy1.14.0 used). The53 exact controls check algebra and construction bookkeeping; they are not independent statistical verification.

## Audit priorities

- Natural conormal reflection and self-adjointness with unknown μ
- Completeness of spectral jets and global smooth elliptic inputs
- Continuous functional calculus near zero; finite-rank positivity truncation and κ^4 weights
- Existence and bounds for the boundary-extension mollifier kernel
- Variance estimates for overlapping consecutive pairs, rather than independent pairs
- Uniform derivative nets and almost-sure bandwidth schedule
- Clipping/normalization and local-to-L² tensor convergence
- Whether a pointwise consistency theorem under the explicit smooth-domain/class assumptions fully meets the informal source problem

## Not claimed

No result for arbitrary rough domains or coefficients, nonreversible diffusions, unmodeled sensor noise, uniform minimax rates, or numerical approximation errors is supplied. The estimator is mathematically finite dimensional, but computational efficiency is not asserted. The deliberately slow smoothing schedule is for consistency. The full original does not prescribe a specific multidimensional estimator or spectral cutoff; this package specifies one.

Current primary-literature check is bounded. The2025 Giordano–Wang likelihood algorithm treats isotropic scalar conductivity and identifies anisotropic matrix conductivity as a future extension; it does not certify the present result's novelty.
