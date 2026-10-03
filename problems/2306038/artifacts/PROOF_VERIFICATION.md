# Proof verification and dependency scope

## Main deduction

The target is an immediate specialization of V. I. Milin (1981), Theorem 2. Normalization, coefficient indexing, weight monotonicity, summability, and the positive exponent are checked in `PROOF.md`. The independently written endpoint argument verifies univalence and divergent unweighted square variation without relying on numerical asymptotics.

## Reading of the resolving proof

The complete relevant argument through Corollary 1 was read, including its internal dependencies. The chain is:

1. Theorem 1 obtains a logarithmic-coefficient estimate from Lebedev's area inequality and a classical distortion estimate.
2. Its corollary selects a unit phase at each radius. This phase is allowed to depend on that radius.
3. The square-root coefficient factorization and the Lebedev–Milin exponential inequality give Lemma 1. The s=1 specialization is the one needed.
4. Parseval's area identity controls the first moment of squared phase-adjusted differences. The reverse triangle inequality removes the phase, leaving squared differences of moduli.
5. Choosing a radius depending on N gives a linear bound for the partial sums of k d_k^2.
6. Abel summation with decreasing nonnegative weights gives Theorem 2; taking weights k^(-1-epsilon) gives Corollary 1.

The area theorem, classical distortion estimates, a classical uniform coefficient bound for odd univalent functions, and the Lebedev–Milin inequality are external established inputs. Their original foundational proofs were not independently re-proved. This is a checked application of the published theorem, not a formalization or a claim of a new derivation from elementary axioms.

## Auxiliary checks

`verify.py` checks in exact arithmetic:

- identities in Q(sqrt(2)), including beta_0=3-2sqrt(2), its reciprocal, and the factor-of-two substitution;
- positivity via rational bounds for sqrt(2);
- Abel summation and its telescoping coefficient identity for rational test data;
- the binomial coefficient recurrence and the endpoint-difference indexing;
- the exact polynomial identity underlying the endpoint lower bound;
- finite instances of the endpoint lower bound.

These tests are regression checks for algebra and indexing. They do not establish univalence, infinite-series convergence or divergence, the cited analytic inequality, or the absence of earlier literature. Those conclusions come from the written argument and explicitly credited theorem.
