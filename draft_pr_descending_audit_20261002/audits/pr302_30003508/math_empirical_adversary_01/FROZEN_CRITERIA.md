# PR302 empirical-convergence adversary: criteria frozen before candidate access

Frozen at 2026-10-05 04:15:20 UTC. Original source identifier supplied by parent: PR302, head eb6e0e999521d84a65f9857d338cad76b84d30db, original author 2/5. No candidate body or prior review was read before these criteria.

This independent family tests whether a fully specified stochastic estimator actually has the claimed almost-sure fixed-lag convergence. A successful result must state assumptions that do not assume the target empirical limit, define measurable finite-sample estimates, and prove all transitions below.

1. Reconstruct the process, state space, reference measure, lag and boundary conventions. Locate any hidden stationarity, reversibility, mixing, density, ellipticity, compactness or smoothness assumptions, and separate model assumptions from consequences.
2. Reconstruct the estimator, including overlapping pairs, normalization, regularization, cutoffs, interpolation or extension, smoothing, rank and treatment of a finite-sample zero denominator. Check every claimed positivity, unit integral, measurability and operator-domain conclusion.
3. Reproduce the covariance/variance argument for overlapping lagged pairs, short distances, long distances and any mixing bound. Verify that constants are uniform over the required lag, bandwidth and spatial variables. Reject a variance argument that merely ignores overlaps.
4. Check the route from moment/tail bounds to almost sure convergence, including summability, subsequences and interpolation to every integer sample size. Determine whether claimed rates hold for the actual changing bandwidth or only for a fixed test function.
5. Audit every net and union bound, its cardinality, extension between net points, bandwidth factors and required summability. Challenge diagonalization over compact exhaustion and lags, including countability and deterministic versus sample-dependent selections.
6. Verify boundary extension followed by smoothing: preservation of positivity/normalization, approximation on interior and near boundary, and compatibility with the reference measure and finite-rank claim.
7. Check any imported heat-kernel regularity or semigroup facts in their actual geometric domain, time range and hypotheses using primary sources or explicit derivations. Do not silently replace a pointwise result by uniform derivative bounds.
8. Construct analytic or exact controls at boundary/overlap/zero-density/slow-mixing cases, and at least one reproducible test or counterexample with falsifiable expected outcomes. Numerical evidence alone cannot certify a universal probabilistic theorem.
9. Identify the strongest theorem actually proved, exact unsupported gap and repairability. Distinguish a legitimate conditional theorem from a circular assumption that supplies the desired empirical convergence.

Verdicts: PASS only with no remaining mathematical gap in this family; REPAIRABLE if explicit local changes or hypotheses close it; HOLD if the central convergence is unsupported or a counterexample exists. Report mathematical completion separately from merge/publication authorization.

Scope: read-only original snapshot and primary sources; write only this dedicated directory; no Git/index/config/shared-status/service mutations, external individual contact or publication. Prior review conclusions and other approach-family conclusions remain unread during the independent phase.
