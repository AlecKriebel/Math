# Five-turn partial result: original rational-base power sums

**Proposed status: unsolved, 5/5 substantive author turns. Independent adversarial review pending.** No full polynomial-time comparison algorithm, impossibility result or hardness classification was established. No novelty or priority is claimed.

## Exact source correction

Neil Olver’s OWR 50/2018 question, printed p. 3015, uses **(2/3)^r_i**, not the extracted **2^(r_i/3)**. The original also asks the more general fixed-rational-base sign question with rational input coefficients. Binary exponent lengths, term count, coefficient bit lengths and all standard zero/sign delimiters belong to the bit-complexity model. An arithmetic-operation bound with unit-cost huge integers is insufficient.

## Retained partial results

1. A direct polynomial bit-time equality test, credited to classical sparse rational-root/equality territory; an explicit fixed-parameter pruning algorithm for the positive unit-coefficient example
2. An exact descending-cluster sign algorithm for arbitrary signed rational coefficients at each fixed rational base, with F_α(m)·poly(L) rather than polynomial dependence on variable m; the integer and reciprocal-integer branches are polynomial
3. Polynomial exact zero-block deletion and certified adaptive truncation with an explicit, unbounded separation parameter; an actual exponential-work family for the conservative implementation that the adaptive method resolves immediately
4. A unique simple near-threshold positive root, locally separated from other complex roots by 1/(1024n), and a positive fixed-term comparison gap whose available quantitative bound remains doubly exponential in n
5. Polynomial sparse carry normalization of nonnegative rational-base sums into unique bounded-digit words; an exact reduction of the general sign task to numeric comparison of those words; explicit failures of naive lexical and finite nonnegative-integer-certificate rules

## Unresolved mathematical step

For variable term count and a noninteger rational base, there is no proved polynomial bound on the comparison precision after structural simplification, and no different polynomial-time order algorithm for the canonical sparse words. The original positive (2/3)^r sum remains unresolved as well as the general rational-coefficient formulation. Root simplicity, local isolation, equality testing and canonical representations do not supply the missing order theorem.

The exponential implementation family is not a complexity lower bound. The small-value examples with exactly canceling blocks are not hardness examples. Fixed-parameter algorithms, generic-input theorems and precision-dependent root algorithms are not relabeled as worst-case polynomial-bit algorithms.

## Validation and publication gate

Five locally authored exact checker programs accompany the five turn files. Their checks support the stated reductions and bounds; the universal arguments are written out in those files. Separate independent review is required before a partial-result draft PR. Only the target’s eventual QUEUE row may be changed to unsolved, 5/5; no campaign queue regeneration, source-PDF redistribution or sixth author proof-search turn is part of this outcome.

Earlier per-turn manifests record historical checkpoint states. The final FROZEN_MANIFEST.json binds the current package; mutable ledgers and README files were updated between those historical checkpoints. Source reading copies remain outside the portable folder.
