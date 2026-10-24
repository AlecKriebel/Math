# Algebraic / probabilistic route log

## 2026-10-24T19:30:07Z — independent opening

Completion estimate toward the full claim: **3%**. Work is confined to this folder. The exact target is every subset of size greater than two of every finite abelian group of odd order. Whole-group cycles, rainbow cycle covers, and small-cardinality cases are explicitly insufficient.

Approach families retained independently: (1) character / polynomial nonvanishing, (2) random-order collision counting, (3) algebraic cycle switches and induction. Every successful route must force one cycle, not merely a permutation with distinct row sums. No external communication, Git, or publication actions are delegated here.

Initial observation for switching: if disjoint edges `{a,b}`, `{c,d}` have the same sum, replacing them by `{a,c}`, `{b,d}` gives two unequal sums in a group without 2-torsion. Indeed equality of the replacement sums together with `a+b=c+d` implies `2(a-d)=0`, hence `a=d`, contradicting disjointness. The reconnection preserving one cycle depends on the cyclic order. This local fact alone gives no improvement because the new sums may collide with other edges.

## 2026-10-24T19:35:09.678337+00:00 — partial-family checkpoint

Completion estimate: **12%**. Proved the exact first-moment criterion, derived a standard canonical-event local-lemma sufficient condition, and proved rectification for groups whose least prime factor exceeds `2^(n−1)`. The proofs and precise universal gaps are in `PARTIAL_RESULTS.md`. No full solution and no novelty claim. Imported theorem checked in the primary Lu–Székely paper. Polynomial subagent reports systematic invariant cancellation and characteristic obstructions; details pending.

## 2026-10-24T19:42:49.251020+00:00 — reduced polynomial and formal-group checkpoint

Completion estimate: **20%**. Dropping the automatic adjacent-edge collision factors gives degree `n(n−2)` and allowed-monomial coefficient contents with no odd primes for every `n=3,...,9` (exact and independently checked witnesses in `polynomial/`). A new integral analytic transfer lemma appears to extend each characteristic-p certificate to all finite abelian p-groups via Lubin–Tate torsion; original Theorem2(b) checked in cached primary paper, and complete proof recorded in `FORMAL_GROUP_TRANSFER.md`. The all-n coefficient assertion and mixed-prime groups remain exact gaps. Adversarial audit is pending before promotion even as a partial theorem.

## 2026-10-24T19:47:27.039781+00:00 — candidate n10–11 and exact reduction obstruction

Completion estimate: **22%**. Exact Python-integer permutation/Lagrange formulas independently match all n3–9 reduced-polynomial coefficients and produce candidate certificates for n10 (min1 content2) and n11 (fixed-zero content1); fresh reproduction requested before promotion. `FORMAL_GROUP_TRANSFER.md` frozen for independent audit. `MIXED_PRIME_MODEL_OBSTRUCTION.md` proves that a concrete nine-element subset of C3×C5 has no injective equality-preserving model in any single p-group, via integral3- and5-annihilators. The subset has an explicitly verified rainbow cycle, so this blocks a reduction only.

## 2026-10-24T19:51:11.565408+00:00 — family final checkpoint

Completion estimate: **22%**. n10 and n11 witnesses independently reproduced from the actual polynomial with exact Python integer arithmetic; all151 overlapping coefficients match independent complete expansions. Strongest partial result: all subsets of cardinalities3–11 of every finite abelian odd-p group, arbitrary rank/exponent; n11 also p2. Full all-n reduced-content assertion unsupported; single-primary model reduction blocked by exact mixed-prime example. Consolidated `FINAL_REPORT.md`; no further finite extensions pursued. Parent fresh audit remains separate and may downgrade a partial statement if it finds a gap.
