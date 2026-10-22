# EP1095 digit-cylinder discrepancy continuation

12 October 2026. AI-assisted authored mathematics and independent AI mathematical review. The principal accepted result is

\[
\limsup_{k\to\infty}\frac{\log g(k)}k\le\frac67<0.86<1,
\qquad g(k)<\exp(0.86k)<L_k\quad\text{for every sufficiently large integer }k,
\]

where all logarithms are natural and

\[
g(k)=\min\{n>k+1:p\nmid\tbinom nk\text{ for every prime }p\le k\},
\qquad L_k=\operatorname{lcm}(1,\ldots,k).
\]

The proof uses the prime number theorem. It improves the preceding accepted coefficient 813/875 by a distinct discrepancy mechanism: disjoint digit cylinders with different prime-power moduli compress the joint CRT endpoint-error budget while preserving every local digit condition and its exact density. For an omitted prime p>k/2, the compressed local weight is exactly p, including at p=k. The two conditions at one prime are never treated as independent events.

The argument proves an actual survivor in a finite initial multiplier interval. It does not locate the first survivor from a full-period density heuristic. No effective numerical onset is given. The main problem remains unsolved: this is still an exponential upper bound, and neither subexponential growth, an all-k strict lcm comparison nor either successive-ratio conjecture follows.

## Complete argument and independent review

- [Complete accepted proof](DIGIT_DISCREPANCY_THEOREM_v2.md): all seven mathematical sections, including the mixed-modulus finite sieve, exact digit arithmetic, local cylinder minimality, lattice and strict domain, asymptotic bound, homogeneous Bonferroni threshold, residual budget theorem, and earlier generating-function comparison
- [Complete substantive independent audit](INDEPENDENT_PROOF_REVIEW.md): full mathematical reasoning, exact strict-margin arithmetic, correction assessment, aggregate finite checks, source qualifications, and limits of the conclusions
- [Exact authored mathematical correction history](CORRECTION_HISTORY.md): the two prose ambiguities resolved before acceptance; no theorem, parameter or proof calculation changed
- [Acceptance and scope](ACCEPTANCE.md)
- [Dated source scope and credit](SOURCE_SCOPE.md)
- [Public member manifest](MANIFEST.json)

## What the barrier does and does not say

The local minimality result is exact only for unsigned covers by residue cylinders modulo p or p² contained in the bad set. It is not an optimality theorem for signed descriptions or cancellation-sensitive estimates.

For a separate family of omission sets, assuming all but o(k/log k) primes in (3k/5,3k/4] are omitted, the exact odd Bonferroni coefficient can be positive only at truncation degree at least (kappa-o(1))N, where kappa is the unique relevant entropy root and 4/5<kappa<5/6. Consequently the split absolute-error budget has liminf log(E)/k >= 3kappa/20 > 3/25; the full prime-square budget has the doubled lower bound 3kappa/10 > 6/25.

This obstruction concerns the explicit positive certificate TQ-E>0. It is not a lower bound for actual discrepancy, the actual first survivor, or g(k), and does not disprove subexponential growth. The fixed 3/4-cutoff construction used for the principal 6/7 theorem does not satisfy that separate omitted-block hypothesis.

## Relation to preceding results

This is a separate follow-on to the [813/875 continuation](../continuation_20261012/README.md) and the [earlier partial-results packet](../README.md). Their mathematical texts remain unchanged. The current proof is complete in its own right; the sibling is background rather than a missing proof premise. Its stronger 6/7 coefficient supersedes the numerical bound 813/875 without invalidating that earlier theorem or changing its historical review.

Independent AI acceptance is not external human peer review, formal proof-assistant certification or journal acceptance. No novelty, priority, best-known status or exhaustive literature claim is made. The lcm construction and classical Brun/Bonferroni machinery are explicitly credited.

This prose edition preserves the complete mathematical proof and substantive independent review. It distributes no programs, raw diagnostic records or case certificates, datasets, copied third-party source bodies or private coordination material. Its manifest hashes only actual public members. Aggregate finite diagnostics supplement the proof; they do not supply its asymptotic conclusion or an effective onset.
