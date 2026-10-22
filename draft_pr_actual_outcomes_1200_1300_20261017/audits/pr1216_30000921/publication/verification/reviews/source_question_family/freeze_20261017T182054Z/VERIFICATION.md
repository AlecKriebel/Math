# Internal adversarial verification

A separate internal adversarial subagent was used under the research validation policy. It received only standalone mathematical derivations, not the source PDF, any repository files, any candidate, any other-family report, outcomes, parent history, or later literature. It was instructed not to read files or use tools other than messages to this family. This verifies the arguments supplied to it; it is not a later-priority check or candidate comparison.

## Round 1: triangular perturbation

The reviewer found no circularity or substantive gap. It checked:

- Every index in the earlier-jet term is strictly below the current jet, so the recursion is triangular.
- The radius rho/|C_k| suffices to move a proposed scalar derivative value out of the forbidden open disk, including coincident centers.
- The perturbation is entire and its derivatives tend locally uniformly to zero, because the ratio (n+l)!/(n+l+m)! is bounded by n!/(n+m)!.
- Preservation of hypercyclicity requires the explicit dense-tail argument; the final report includes it.
- Eventual scalar orbit exclusion suffices even with finitely many earlier values.
- The cutoff estimate gives arbitrarily small perturbations on prescribed compact sets.

It also checked an optional countable common-root extension, which is not needed for the strongest report theorem.

## Round 2: annular jet construction and simultaneous polynomial failure

The reviewer confirmed the stronger statement: a dense family of differentiation-hypercyclic entire functions f satisfies |(pf)^(n)(0)| -> infinity for every nonconstant complex polynomial p simultaneously.

Its requested clarifications were incorporated in the report:

1. Baire's theorem is applied to the closed complete space X_M, with relatively open dense orbit-hitting sets. Invariance of X_M under differentiation is unnecessary.
2. Neighborhood control follows from the factorial tails. In fact, if f,g in X_M agree through index L>=M, then their norm difference on the r-disk is at most 2 sum_{n>L} log(n+e) r^n/n!, which tends to zero. The final report instead gives a direct baseline-tail and finite-block estimate, which proves the same control.

The reviewer checked the exact target error e^R/sqrt(N+1), the radial clipping, the eventual upper bounds, the reverse-triangle inequality and degree-one boundary case, and density after allowing arbitrary finite prefixes. It explicitly found no substantive gap.

## Verification limits

This is a mathematical proof review, not a machine-checked formalization. No numerical orbit sample was used. No historical novelty or priority verification has been performed.
