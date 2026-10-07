# Author validation

2026-10-07. Separate independent review has not occurred in this packet.

The exact standard-library verifier passed 118,649 assertions. It checks all 15 two-center options for the six-point Euclidean example, all fractional feasibility constraints, squared radical enclosures, the strict gap lower bound, and the perturbation margins. It also checks 3,564 replicated center pairs (including duplicate-site selections), 4,875 rational opening vectors for systematic interval rounding, and positivity of every pivot in an exact LDL decomposition of the 15-by-15 Gaussian-limit covariance.

The finite-gap certificate gives I >= 25.447078 and F <= 24.8668205, so I-F >= 0.5802575. This is an exact rational lower bound, not a rounded floating-point subtraction. The fractional optimum itself is not computed exactly.

Analytic author checks:

- LP bounds, objective, data-point facilities and unsquared Euclidean metric match the source.
- The line rounding opens exactly k distinct facilities almost surely and proves equality of optimal values; it does not claim every LP vertex is integral.
- The Gaussian CLT has fixed n=6. Its covariance has independent edge-noise terms, ensuring full support. No uniform-in-n CLT claim is used.
- Common off-diagonal cost shifts cancel because both the integer optimum and fixed fractional witness use total off-diagonal mass n-k=4.
- The Gaussian concentration theorem is a relative-value bound, with a union bound that allows dependent pair distances.
- Replication proves a robust open set with positive probability at every n=6r; the event probability can vanish as r grows.
- The later stochastic-ball counterexample is described as planted exact-recovery failure. It is not substituted for a global integrality-gap theorem.

All mathematical results are limited to their stated hypotheses. None resolves the general joint random-model question. No human peer review or novelty is claimed. Retrieval and source scope are recorded separately; no source document or third-party dataset is distributed.
