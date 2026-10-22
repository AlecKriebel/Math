# Reviewed scope addendum

The independent audit accepts the five approaches as sound partial work with the following clarifications. The disposition remains **unsolved, 5/5**, with no full-resolution or novelty claim. The original authored files and the complete safe audit are preserved byte-for-byte.

## C1. Dense prefixes are different from the published sparse grid

The counterexample in the original Approach 3 uses every prefix size in its specified range. It does not challenge the manuscript's spaced-size Algorithm 2. For total sample size n=k², validation size k and its square-root grid, the probability of any exceptional candidate is at most

(H_(k−2)−1)/k = O(log n / sqrt n),

which tends to zero. This union bound holds irrespective of dependence between sampled subsets. Thus pointwise limits fail for the dense collection used in the counterexample, while this particular learner has simultaneous control on the paper's sparse grid.

## C2. The selector cannot inspect a future test label or refit

Read “every measurable selector” as a selector measurable with respect to training, independent validation and independent auxiliary randomization. The fresh test pair is independent of that information. The returned predictor must be one of the unchanged training candidates. The final conditional-risk statement excludes future-test-label access and any subsequent refit whose risk has not been controlled.

## C3. The candidate losses are bounded

In the rare-event construction, squared loss is at most 4 for the specified response distribution and candidate predictions. Squared loss is not globally bounded on arbitrary real arguments. If a globally bounded loss is desired, clipping squared loss at 4 leaves every calculation for that construction unchanged.

## C4. The Gaussian conditioning distinction is substantive

Hastie et al. condition on the design and integrate training-response noise, whereas this packet conditions on the full training data. The independent concentration proof supplies that additional step and restores independent test-noise variance. Its result is conditional risk 11/3 for the specified shrinkage procedure versus envelope 4, not merely a comparison of expected risks.

## Review and numerical scope

The original RESULT.json's unreviewed status describes its historical freeze; the separately bound audit records the later review. The 1,800 Gaussian fits in the audit are numerical sanity checks, not proofs of convergence, optimality or monotonicity. The exact controls and mathematical arguments are distinguished from those simulations throughout the audit.
