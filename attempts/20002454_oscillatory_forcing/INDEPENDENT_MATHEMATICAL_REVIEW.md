# Independent mathematical review

Date: 2026-10-21. Outcome: **PASS for the stated scoped mathematical claims**.
No claim of novelty or resolution of the original workshop problem is made.

## Exact reviewed artifacts

- MATHEMATICAL_AUDIT.md: 14,930 bytes; SHA256 `5a5c99dc1ad2b6c4af563c8a43631480d1ce75bc6ce283dfa2962bcac37b132f`.
- verify.py: 5,660 bytes; SHA256 `110102a0464843c1f143234da316477fc099538757f201db9e31bf98d0cb3d9a`.

This review applies to those bytes. Changes require checking the changed statements. The manuscript and supplied script were not edited during this review. Bibliographic content and external source retrieval were not independently verified by this reviewer; this is a mathematical and reproducibility review, not source-provenance certification.

## Proof audit

1. **C1 flux and strict-gap inversion.** Coercivity and the stated derivative sign give the two global inverse branches. On the compact positive-distance-from-critical band, f' is continuous and nonzero, so inverse branches and cell averages are C1. Their derivatives have a single sign. Averaging therefore cannot cancel them, and the speed bound gives |E_i'| >= 1/L. No convexity, f'', or derivative Lipschitz hypothesis is used here. A fixed strict gap is essential.

2. **Domain, monotonicity, and conservation.** The negative branch reverses the ordering of constants correctly. Both displayed off-diagonal derivatives are nonnegative and their diagonal derivatives are nonnegative under CFL. The corner vectors really are global equilibria, despite cell-dependent E_i, which closes the inverse-domain induction rather than presuming it. Weighted conservation follows by cyclic flux telescoping. For a one-cell periodic mesh, neighbor and self variables coincide; the displayed separate derivative contributions must then be combined, giving the identity map. This harmless index degeneracy does not invalidate the theorem or proof.

3. **Weighted L1 contraction and adapted entropy.** The maximum/minimum comparison vectors lie in the rectangular domain, and conservation applies to both. The weighted maximum-minus-minimum argument proves contraction without assuming a uniform mesh. For negative-branch entropy, C(w)-C(z) = -|C-k|, and the right-upwind index yields Q_{i+1/2} = -|C_{i+1}-k|. Thus both entropy signs and interface indices are correct. This is the asserted stationary adapted entropy, not a proof of every constant-state entropy inequality for the discretization.

4. **Near-equilibrium bound.** Reconstruction and the reference equilibrium have fixed relative sign on each cell, so their integral absolute difference equals the absolute difference of their cell integrals. The initial averaging inequality, numerical contraction, same-source PDE contraction, and triangle inequality yield exactly the factor two. For fixed N, the continuous additive source is bounded, and its comparison contribution cancels; no uniform source derivative estimate is required. The assumed bounded entropy solution and strict-band classical stationary reference suffice. The result is uniform in N and time only in the stated sense: it bounds error by initial distance to one equilibrium. It does not tend to zero under mesh refinement for a fixed nonzero perturbation, and supplies no general mesh-consistency theorem.

5. **Critical BV classification.** On compact interior subintervals, division by the positive amplitude preserves BV. A two-valued BV function there has finitely many sign switches. Equal-flux downward jumps have entropy production 2(f(r)-f(a)) <= 0 for interior r; upward jumps are ruled out already by r=0. Therefore no two downward switches can occur without an inadmissible upward switch. Exhaustion excludes hidden switches accumulating at a cell endpoint. Zero-amplitude joins contribute no entropy atom. The displayed profiles cover endpoint parameters and interior shock parameters, and direct integration gives the stated means. This proves the claimed BV classification, not a classification of unrestricted distributional solutions.

6. **Observation lower bound.** Alternating pure-sign microcells are Lipschitz stationary entropy solutions, including the zero joins. Pairwise-aligned coarse cell integrals vanish for both opposite profiles. Their L1 separation is 8/pi, forcing the pointwise-in-time maximum error to be at least 4/pi for any deterministic output based only on the listed observations. Neither arbitrary meshes nor a single worst-case input across all times is asserted. The lower bound is sharp for this two-input decision problem because W=0 attains 4/pi for both.

7. **Quadrature qualification.** Positive normalized quadrature has the same branch derivative bound, so it preserves its own equilibria and domain. Provided the exact reference lies in that domain, inversion errors are bounded by L delta_i; cyclic differencing yields the stated 2 dt L sum(delta_i) defect. Contraction plus the fixed-reference one-step defect yields the n-step bound. The endpoint aliasing example is nonvanishing in N and correctly does not assert a nonzero update on a one-cell torus. These results do not supply a practical uniform quadrature-convergence rate.

No substantive mathematical gap was found in the claims as scoped. The general C1 theorem, resonance-specific quadratic classification, and observation-dependent obstruction must remain distinct.

## Reproducibility and additional falsification tests

Commands run successfully:

    python verify.py
    python independent_review_checks.py

The supplied script passed all 210 checks and produced CHECK_RESULTS.json with SHA256 `8dc95c57ae85e2e0f1cb89fff0785a8566125cde8319ed0590a9c6196bffa16b`.

Additional independent checks use f(u)=u^2/2+2(1-cos(u)). This flux is genuinely nonconvex, with f''(pi)=-1, while f'(u)=u+2sin(u) has the sign of u: for 0<u<pi both terms are positive; for u>=pi, u+2sin(u)>=pi-2>0; oddness handles negative u. It is coercive. Eight parameter cases cover both branches, N in {1,11}, one-cell and nonuniform three-cell meshes, and equality in a certified CFL bound. Invariance, mass, contraction, adapted entropy, equilibrium preservation, and full-map order tests all passed. The largest positive entropy residual was approximately 1.18e-16.

Independent check script SHA256: `ac04cf40d79eb9eeb7ef0dcc5e7fefc1749a57b187a6429c026c90c29722b722`.
Detailed results: INDEPENDENT_CHECK_RESULTS.json, which also records manuscript/script hash bindings.

All computations use floating-point quadrature and inversion and are falsification checks, not formal proofs or certified exact-integration implementations. The analytical proof audit is the basis for accepting the exact-average assertions.

## Publication projection and checker hardening

The mathematical manuscript is unchanged. The reproducibility commands above are directory-neutral public projections. The original independent checker hash above identifies the historical reviewed input; six removable assertions were converted mechanically into explicit RuntimeError checks in the distributed independent_review_checks.py. The complete original authored checker is retained as provenance, not executed by the validator. A whole-module AST equality test verifies that assertion conversion is the only change. Fresh exact outputs and bindings are recorded separately. This packaging validation does not enlarge the mathematical review or certify novelty.
