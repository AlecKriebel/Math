# Full five-turn independent review request

Read SOURCE_SCOPE.md, RESULT.md, all five TURN_n.md proofs and their source bindings. FINAL_AUTHOR_MANIFEST.json binds the complete public packet; all historical files are preserved. Final status is CURRENT_STATE_T5.json. CURRENT_STATE.json is the unchanged source-gate snapshot, not a current-turn claim.

Critical source checks: OWR26/2024 printed1495–1498, especially second setting1497/PDF53; published BCU Theorem6 printed1325/PDF10 versus Corollary7 printed1326/PDF11; the exact vector LT update with its old-state factor and independent sqrt(N)-scaled spatial-cell Brownian drivers. Distinguish the prior time-only target30005935 and Ulander's different LTE method.

Critical proof checks:

1. Common coefficient constants through the nonsmooth global-Lipschitz approximation; fixed-mesh dominated convergence must not be claimed mesh-uniform.
2. High-p BDG, discrete convolution, G_N versus G error imported only through fixed additive/noiseless cases of the credited spatial theorem; explicit exp(CL^4) dependence and NL²τ<=1; grid cardinality needs balanced refinement.
3. Nonnegative unweighted mass supermartingale under killed Dirichlet boundary; measurable stopping/Hölder seminorms; parabolic effective dimension3; amplitude R^(5/4), with no hidden Lipschitz-dependent Hölder constant; near-boundary high excursions.
4. Exact and numerical cutoff agreement with frozen inputs even if an intermediate geometric substep exceeds the cutoff; bilinear interpolation; R proportional to log(e/h); bounded-test rate and coupling convergence in probability.
5. White-noise bracket integral phi²u^(5/2), normalized phi and weighted Hölder constant, drift-removal exponent; the explicit concave barrier and its C² extension at zero; localized Itô drift, first Fatou, and terminal Fatou without uniform integrability. Verify conditional heat domination and the strict weighted-loss transfer to the fixed midpoint, not merely integrated mass. Check first-moment preservation of the numerical recursion, sine discrete eigenvalue and balanced-mesh contradiction.

The final turn deliberately avoids a random-clock proof: a lower bracket bound does not by itself permit an unbounded optional-sampling assertion. All required barrier signs, time orientations and limit passages are included. The inverse-Bessel mean calculation is supplementary and self-contained.

All checkers are standard-library Python and deterministic. Replay each and compare output bytes to TURN_n_CHECKS.json; these are finite controls, not stochastic simulations. Verify all historical manifest bindings and the final freeze. Report mandatory corrections additively so frozen evidence remains unchanged. No sixth author search is authorized.

Proposed disposition is unresolved5/5 for the original bundle, with a complete negative superlinear continuum mean-square subquestion and positive explicitly bounded-test results. No infinite second-moment claim, arbitrary weak-test claim, optimality or novelty certification should be inferred.
