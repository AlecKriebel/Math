# Research log

3 October 2026. Five distinct substantive mathematical routes were pursued. This is an account of the investigation, not five claims of novelty.

## 1. Reference-dependent multinomial risk

Constructed an explicit point-mass reference estimator and a paired-sign mixture around the uniform reference. Proved a chi-square bound and transferred it to squared-error lower bounds. This gives a polynomial separation on the same alphabet at the same sample size. It does not give the optimal uniform-reference rate.

## 2. Sharp existing theory

Recovered and checked the precise fixed-reference theorem of Jiao–Han–Weissman, including its logarithmic regime restrictions. Applied it to a uniform reference and gave the Poisson-to-fixed-sample reduction. The unrestricted extrapolation was rejected because it contradicts the parametric lower bound at a point mass. The sharp discrete reference effect is credited prior work.

## 3. Symmetry and neighborhoods

Proved invariance of minimax risks and tolerant testing under experiment isomorphisms. This rules out reference effects in the unrestricted Gaussian location example. Then proved boundary/interior Bernoulli local risk bounds under a different, explicitly defined neighborhood criterion. These examples do not supply a universal classification.

## 4. General reductions

Proved the estimator-to-tester direction by Markov's inequality and a finite-grid converse from a uniform family of threshold tests, including sample amplification. The route stops because a single null radius does not control the whole family; no sharp reference-sensitive complexity follows without additional model-specific work.

## 5. Exact parametric transition

Reduced the Bernoulli boundary tolerant test to two endpoints by monotone likelihood ratio. Computed Hellinger affinity and established matching sample-complexity bounds, yielding the critical-gap interpolation. This settles that example only. Major multidimensional and nonparametric results already exist, while the broad source request remains unclosed by this work.

## Checks and verdict

The standard-library script performs 16,459 exact rational assertions covering mixture second moments, point-reference risks, Hellinger identities, endpoint testing inequalities, and grid reconstruction. These checks are deliberately small and algebraic.

No full resolution; five approaches complete. No novelty or first-resolution claim. The author package is frozen for fresh adversarial review before any result is published.
