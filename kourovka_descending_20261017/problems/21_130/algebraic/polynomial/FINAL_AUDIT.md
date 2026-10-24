# Consolidated independent polynomial audit

Checkpoint: 2026-10-24T19:49:21Z. Best-guess completion toward the full Kourovka claim: **15%**. No new finite extensions are being attempted after this checkpoint.

## Strongest verified scope

The reduced cyclic polynomial Q_n, the exact integer coefficient witnesses, and the independently audited integral formal-group transfer together prove:

1. Every subset of size **3≤n≤11** in every finite abelian p-group for an **odd prime p** has a cyclic enumeration with pairwise distinct adjacent sums.
2. At **n=11**, the same conclusion holds in every finite abelian p-group for **every prime p**, including p=2.

The polynomial argument alone uses an additive finite-field embedding and covers elementary abelian groups. The arbitrary-exponent extension uses the parent's sourced Lubin–Tate construction and the convergent monic-grid quotient argument; details and source checks are in `FORMAL_GROUP_AUDIT.md`.

This audit does not independently establish any proposed mixed-prime transfer. General n and arbitrary mixed-prime odd-order groups remain outside the verified scope of this audit. No novelty claim is made.

## Cardinality ten: independent actual-polynomial evaluation

The parent supplied a list of low-exponent coefficients. I independently checked these two coefficients by the original finite-difference interpolation formula, evaluating the actual integer polynomial Q_n=V(x)∏_(nonadjacent i<j)(s_j−s_i):

| Exponents t | [x^t]Q_10 |
|---|---:|
|(0,8,9,9,9,9,9,9,9,9)|−30955393332|
|(1,9,8,8,9,9,9,9,9,9)|−125404419790|

Their gcd is **2**, so no odd prime divides both. This certifies every odd characteristic at n=10 and, by the formal-group transfer, every finite abelian odd-p group at this cardinality. It is unnecessary to rely on the complete fixed-zero list with gcd6 or the complete minimum-exponent-one list.

The second witness is not divisible by 3 and removes the extra prime3 obstruction in the fixed-zero family. The witness gcd2 does not by itself determine whether the content of the entire truncated Q_10 is 1 or 2; that exact content is not claimed here.

Reproduce with:

    python3 fixed_zero_audit.py --n10-combined

The output is preserved in `n10_combined_verification.txt`. The run evaluated 21784 nonzero Q values and completed in 0.89 seconds.

## Cardinality eleven: independent actual-polynomial evaluation

The independently checked coefficients are

| Exponents t | [x^t]Q_11 |
|---|---:|
|(0,9,10,10,10,10,10,10,10,10,10)|11098103614834|
|(0,10,9,10,10,10,10,10,10,10,10)|189427196282499|

Their gcd is **1**. They therefore certify every prime characteristic, including 2. Unlike n=10, this also proves the entire retained coefficient content is exactly1, since it divides the gcd of a subset of its coefficients. Full sparse polynomial expansion is not needed for that deduction.

Reproduce with:

    python3 fixed_zero_audit.py --n 11 --positions 1 2

The output is preserved in `fixed_zero_n11_verification.txt`. `FIXED_ZERO_N11_AUDIT.md` independently derives the parent's simplified formula, including sign and factorial denominator, from the original grid formula.

## Independence of the computation

`fixed_zero_audit.py` imports no parent coefficient implementation. It uses the original formula

    [x^t]Q_n = (1/∏t_i!) · ∑_(0≤a_i≤t_i)
                (-1)^(∑(t_i−a_i)) (∏binom(t_i,a_i)) Q_n(a).

The Vandermonde forces a to be a permutation of 0,...,n−1. The implementation enumerates the permitted first coordinate, then the remaining permutations. It computes the color factor first to discard zero evaluations, then explicitly multiplies all vertex-difference factors to obtain V(a). It computes the original binomial weights and original factorial denominator separately for each witness. All arithmetic is exact over Z, and every final division is checked for zero remainder. No finite-characteristic factorial division is used.

For n=3,...,9, `slack_coefficient_audit.py` supplies a second set of exact integer grid certificates, independent of sparse polynomial expansion. `SLACK_RESULTS.md` and `SLACK_AUDIT.md` record those witnesses and their verification.

## Other audited mechanisms and blocked routes

- The original central CN coefficient is identically zero for every even n by reflection. Its odd-n characteristic restrictions are genuine limitations of that certificate and are superseded at small n by the reduced polynomial.
- The naive exterior sum cancels identically for even n and for n≡3 modulo4. This is a rigorous invariant obstruction, not a counterexample to the graph statement.
- A squarefree determinant can encode several cycles. The vertex-nilpotent trace construction enforces one cycle exactly, but its nonvanishing is equivalent to the original hard requirement; no nonvanishing theorem is claimed.
- The parent's canonical-event local-lemma count and large-least-prime-factor rational rectification passed independent checks. See `PARENT_ROUTE_AUDIT.md`. These methods do not establish a general result in the dense small-prime regime.

The exact remaining polynomial task is a universal odd-prime nonvanishing/content theorem for Q_n, plus a valid route from the p-primary cases to arbitrary mixed-prime finite groups if one is to reach the full original scope. These are recorded as gaps rather than inferred from the finite computations.
