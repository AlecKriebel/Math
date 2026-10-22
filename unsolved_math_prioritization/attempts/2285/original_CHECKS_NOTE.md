# Exact checks and correction record

`checks.py` uses Python integer arithmetic and Fraction rational arithmetic. Running it produced `CHECKS.json` with all checks passing.

- Enumerated every point subset of the projective planes of prime orders 2 and 3 (128 and 8,192 subsets). Checked the exact first and second line-intersection moments for each subset.
- For each possible subset cardinality, checked the exact covariance-trace formula against the enumerated distribution of size histograms.
- Checked the Bernoulli shared-point covariance identity at each of those rational densities.
- Checked 10,470 rational hypergeometric-to-binomial total-variation cases with population size at most 40 and sample size at most half the population.
- Checked the power-of-two order selection and all displayed density, sample-length, and nontriviality conditions for every n from 10 through 100,000 (99,991 cases).

A first draft's threshold n≥8 was too low: n=9 gives q=8 and q+1=n. Both the independent audit and the finite test caught this. The research proof now uses n≥10, for which the conditions follow analytically from q<sqrt(8n) and sqrt(8n)+1<n. The finite checks supplement, rather than replace, the proofs. No search over arbitrary PBDs or claim of resolving the sqrt(n) target is involved.
