# Accepted partial result: reduced denominators (EP68 / 1910)

For H_N = sum_{n=2}^N 1/(n!-1), write Q_N for its positive reduced denominator, and let S be the infinite sum. The complete elementary proof establishes:

1. limsup log(Q_N)/(N^(3/2) log N) >= 1/3.
2. For every fixed 0 < c < 1/3, the set A_c = {N >= 2: log Q_N >= c N^(3/2) log N} has lower asymptotic density at least 1/2.
3. Q_N(S-H_N) tends to positive infinity as N tends to infinity through A_c.

The essential cancellation lemma is P | D G^2 for a reciprocal sum with denominator product P, reduced sum denominator D, and product G of pairwise gcds. A factorial-gap estimate and a terminal-block argument then bound Q_N Q_(N-k), and residue-class chains on fourth-power intervals give the lower-density conclusion.

Cook's inspected manuscript is acknowledged for the starting factorial-gap and terminal-block strategy, which it applies to the unreduced lcm. All needed mathematics, including the cancellation lemma and transfer to reduced prefix denominators, is proved here. No computational or formalization claim from that manuscript is imported.

This establishes neither rationality nor irrationality of S. It does not give pointwise growth of every Q_N, a threshold claim at c = 1/3, density exactly 1/2, density one, optimality, or exclusion of a favorable sparse subsequence. The original irrationality target remains unresolved by this work. No novelty or exhaustive current-status claim is made.

The independent internal AI audit accepts only this partial scope. The authored documents are unrefereed; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. Historical exact checks are summarized, with executable programs and detailed outputs omitted. See PROOF.md, AUDIT.md, and ACCEPTANCE.md for the complete statements and review.
