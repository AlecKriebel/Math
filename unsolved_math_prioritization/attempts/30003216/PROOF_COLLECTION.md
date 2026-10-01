# Consolidated proof map and hypotheses

**Five-turn scoped partial collection; original target unresolved.** All proof files named here are bound by FROZEN_MANIFEST.json. The source and prior-result audit is in SOURCE_SCOPE.md and KNOWN_RESULTS_UPDATE.md.

## Common recovered equation

The primary conforming Galerkin solution u_H is followed by the H(div) solve

    (div sigma_h,div tau_h)+delta(A^-1 sigma_h,tau_h)
       =(f+delta u_H,div tau_h).

The full KLS2017 equation supplies the test-function divergence missing in the OWR display. Homogeneous Dirichlet data are used throughout the retained proofs. Delta is positive. No purported alternative HDG/HHO or skeleton-multiplier scheme is substituted.

## Proof dependencies

- TURN_1 sections1–3 establish the exact recovered scalar, conservation identity and fixed-delta projection limit. Sections4–5 give a deliberately fine-only sequence demonstrating why Cauchy convergence and an unaugmented mixed residual do not suffice.
- TURN_2 sections1–2 give the exact Schur/minimum-lift formulas. Section3 proves the planar RT0 tangential plus negative-norm-defect estimate via Helmholtz decomposition, quasi-interpolation and edge bubbles. Section4 proves an abstract quantitative marking transfer and leaves its termination conditions explicit.
- TURN_3 gives a complete reconstructed variable-delta algorithm. Its star-shaped polygon assumption supplies a classical uniform divergence lift, whose RT interpolation construction is spelled out. The mixed Cauchy lemma, absolute tolerance, data step, both indicator-size cases and H(div) conclusion are all included.
- TURN_4 gives a separate complete reconstructed fixed-delta algorithm on any bounded simply connected polygon. It proves primary estimator reduction/reliability, fixed-parameter flux Cauchy convergence, fine tangential reduction, overlay data consistency and positive-projection limit identification. It does not require the divergence lift used by TURN_3.
- TURN_5 adds a flux upper estimator on convex polygons. It proves the recovered-scalar/Helmholtz-potential comparison, positive projected-reaction error estimate, dual H2 coarse-residual bound and estimator convergence under TURN_4. The convexity/dual-regularity assumption is additional, not silently imposed on TURN_4.

## Scope distinctions to preserve

TURN_1's general coercive operator observations allow bounded SPD A; the planar residual and algorithm theorems use A=I. Every algorithm theorem uses RT0 for the fine flux; TURN_4–5 use conforming P1 for the primary solve. Uniform shape regularity, nested fine spaces, the exact refinement requirements and exact integration/solves are retained. TURN_3 permits independently changing coarse inputs; TURN_4 requires its own nested primary marking and overlay. The two algorithms must not be conflated.

Cauchy convergence alone is not declared consistency. In TURN_3, indicator decay plus reliability identifies the limit. In TURN_4, the positive projected-reaction equation performs that identification. No L2 estimate is converted to an unjustified summability claim, and no adaptive union is assumed globally dense. The separately credited classical lifting, trace, interpolation and elliptic regularity inputs are explicit.

The original unprinted estimator and marking/coupling policy have not been equated with these reconstructions. The collection therefore remains a partial answer to the original source request, not a claim of its full resolution.
