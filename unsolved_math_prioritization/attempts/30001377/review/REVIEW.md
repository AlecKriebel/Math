# Independent audit of the AND-layer sensitivity obstruction package

**Verdict: PASS_SCOPED_BOUNDS_AND_OBSTRUCTIONS.** No mandatory mathematical correction. Both the original polylogarithmic implication and its weaker subpolynomial variant remain **unsolved, 2/5**. This is an independent AI review; historical novelty and human peer review are not established.

Reviewed `OBSTRUCTION.md`: SHA-256 `5160155e7d1ed63adf017773a279bd833b4e9a6090874f488e9baac32d583996`. Date: 2026-09-30. Actual reviewer metadata: inherited runtime, exact model identifier not exposed; no model or reasoning switch made.

## Primary statement

The [EMS report](https://ems.press/journals/owr/articles/4135) and its full cached contribution on printed pp.2825–2826 were inspected, including the rendered definition page. Rossman's statistic is the expectation of the pointwise maximum of sensitivities. His proposed induction has n arbitrary input functions on n bits and n conjunction outputs. It does not assume those arbitrary factors have shallow circuits. The separate balanced-graph-property conjecture is not part of this target. The submitted statement retains all these distinctions.

The author's source discussion correctly distinguishes ordinary average sensitivity of bounded-depth formulas and worst-case sensitivity results from the present family statistic. This audit verifies those scope distinctions, not every external theorem or present-day openness of the conjecture.

## Boundary accounting

At a zero output of a conjunction, choose any factor currently zero. Any adjacent input changing the conjunction to one necessarily changes that chosen factor, so every sensitive coordinate is included in its sensitive set. This proves the pointwise zero-side domination without monotonicity and even when several factors are zero.

At a one output, all factors are one. A coordinate changes the conjunction precisely when at least one factor changes; the union bound gives the fan-in factor. Empty conjunctions are constant and cause no exception, including K=0 for a wholly constant output family. Taking the maximum and expectation preserves the K bound. Consequently logarithmic fan-in yields the specified polylogarithmic implication for that restricted class only.

For one output, uniform cube edges are counted once from each side of its cut. Hence the zero- and one-side sensitivity sums agree, and its mean sensitivity is at most twice the input family statistic. This equality cannot be moved through a maximum over outputs: the maximizing output may differ at the two endpoints. The submitted package appropriately retains only the much weaker sum-over-outputs estimate.

## Disjoint-block amplification

A k-bit conjunction has sensitivity k on the all-one input, one on exactly-one-zero inputs, and zero otherwise. For disjoint blocks these events are independent across blocks. The two cases determining the maximum are (i) some all-one block and (ii) no all-one block but some exactly-one-zero block. Their probabilities give the stated formula; it also remains correct at k=1, where the two positive sensitivity values coincide.

Choosing m=2^k and n=km gives a probability greater than one half of an all-one block. Therefore the output statistic lies between k/2 and k, while the coordinate-factor input statistic is one. Since k≤log₂n≤2k, a logarithmic loss really occurs along this family. There are exactly n inputs; repeating an output pads m outputs to n without changing the maximum. This disproves a universal constant-factor comparison, but is consistent with the conjectured logarithmic factor. No counterexample to either original implication follows.

## Syndrome obstruction and its limit

For n=2^r−1, the parity-check columns enumerate every nonzero vector of F₂^r. Flipping coordinate v changes syndrome by exactly v. For a nonzero color a, its indicator has n sensitive coordinates at syndrome a and exactly one at every other syndrome. For r≥2 there is always a zero-valued indicator of sensitivity one, including at a nonzero syndrome. Hence the zero-side maximum is identically one.

The syndrome map is onto because the standard basis columns are present. All fibers have the same cardinality, so the syndrome is uniform. The full family maximum is one at syndrome zero and n at each of the other n syndromes. This gives (n²+1)/(n+1), growing linearly. Thus the proposed universal logarithmic, or subpolynomial, transfer from output zero-side maximal sensitivity to full output maximal sensitivity is false.

Crucially, that output-only statistic discards the original factorization hypothesis. The displayed conjunction realization uses both literals of each syndrome coordinate; every such parity literal is sensitive in exactly 2^{r−1} input coordinates at every input. For r≥3 there are at most n literals, so padding to n is possible, but their average maximal sensitivity is (n+1)/2. It is linear, and the output statistic is at most twice it. The representation therefore fails the low-input-statistic premise. The package does not claim that all other possible representations must have large input sensitivity; proving or disproving that would require additional work.

The Hamming construction is credited and its used properties are proved directly. No unexamined coding theorem is needed for the obstruction.

## Exact independent controls

The submitted standard-library verifier was replayed in a separate directory. All 48,145 assertions reproduce with a byte-identical receipt, and the final proof, code, and receipt hashes match the author's confirmation.

The independent checker uses bitmask truth tables for all 4,096 triples of Boolean functions on two bits and all eight choices of conjunction factors. It separately enumerates block Hamming weights with exact binomial multiplicities for 30 block parameter pairs, rather than reusing the author's full-cube AND enumeration. Finally it enumerates all 32,768 vertices of the actual 15-dimensional cube, checking every syndrome-indicator sensitivity and every parity-coordinate sensitivity by coordinate flips. Final exact assertion counts are in `independent_results.json`.

These controls supplement the parameterized arguments and do not infer an asymptotic conjecture from small truth tables. The original target remains unresolved, and the source's full input-family statistic must remain explicit in any publication summary.
