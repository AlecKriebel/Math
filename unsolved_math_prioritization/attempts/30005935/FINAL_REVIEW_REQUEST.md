# Final independent review request: 30005935

The complete five-turn author packet is frozen. Review all source scope and proofs without undertaking a sixth author search. Give a qualified PASS or FAIL with any mandatory corrections recorded separately. Do not certify novelty or treat algebraic controls as an SPDE proof.

## Original target and formula reconciliation

Read SOURCE_SCOPE.md, SOURCE_MANIFEST.json, SOURCE_ADDITION_TURN_2.json and SOURCE_ADDITION_TURN_3.json. Full original Cohen contribution: OWR26/2024 pp1495–1498. The targeted question is on p1496 (PDF page52). It concerns a single real Brownian motion, Itô noise, Dirichlet data and the superlinear power5/4, while separately mentioning a weak-rate problem. Do not substitute the next page's space-time-white-noise question.

OWR equation2 and the cited primary time-noise paper equation5 omit the old-value factor. The latter's equations6–8 and linear exactness statement specify the intended update with that factor. Equation8 on PDF page4 was visually checked. This reconciliation is explicit rather than silently changing the target.

Primary PDFs reside separately in sibling `sources/`; none is republished in the packet. The source manifests bind all eight local PDF hashes. They include the original report, cited time-noise and SDE weak papers, current related2026 papers, Lawler's Bessel notes, the older positivity paper and Geng's time-change notes. Read scopes are recorded; no entire-book or entire-external-proof audit is claimed.

## Highest-risk mathematical checks

- Turn1: pathwise bounded nonlinear substep, conditional first moment, common-noise cross term, uniform interior heat-kernel lower bound, and actual Gaussian tail divergence
- Turn2: uniform-in-first-increment kernel ratio; log-Jensen coefficient; extension to every later grid index by conditional mean and Jensen; exact BES6 transform and fixed-time moment threshold; globally Lipschitz cutoff construction; positive-part energy comparison with a scalar process having nonzero boundary value; local mild versus global L2 definitions; coupling argument avoiding subtraction of infinities
- Turn3: normalized principal eigenfunction and weighted weak equation; strict positivity of the mass; random clock as a stopping time in the time-changed filtration; no independence assumption on that clock; optional sampling of a nonnegative local martingale; exact Laplace/Gaussian mean-loss formula; fixed-horizon, timestep-independent error conclusion
- Turn4: Gaussian derivative identities use h=vf', not an unbounded f' estimate; H1 chain-rule estimates require only bounded g'; justify H1 regularity from the H Picard solution without asserting global H1 Lipschitzness; maximal Hilbert energy/BDG bounds; residual decomposition; all constants grow at most polynomially in L times exp(C L2); one-dimensional interpolation and stopped identification of original and cutoff schemes
- Turn5: exact cutoff growth B_K≤C(1+K)exp(C sqrt(K)); event identifying entire interpolated paths, including possible intermediate values above K; optimization K proportional to log(eM)^2; uniformity over bounded-Lipschitz tests; no inference about a positive algebraic rate or higher dimensions

## Disposition boundaries

The superlinear unconditional mean-square assertion is refuted if the proofs pass. Bounded-Lipschitz weak convergence in one dimension is a positive scoped result; it coexists with nonconvergence for unbounded linear mass. The wider source weak question, including unspecified test classes, higher dimensions and sharper algebraic rates, is not declared fully solved. Five author turns are exhausted; publication status must reflect that distinction.

## Replay

Run Python standard-library scripts verify_turn1.py through verify_turn5.py from the frozen packet. Compare stdout bytes to TURN_1_CHECKS.json through TURN_5_CHECKS.json. Check all historical manifests and FINAL_AUTHOR_MANIFEST.json. FINAL_REPLAYS.json binds expected outputs. Exact finite assertions are controls, not a substitute for the analytical proof audit.

Preserve all frozen author files. Put any correction, limitation or final review in new review artifacts. No GitHub publication is requested by this document itself.
