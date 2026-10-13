# Sparse low-rank zero squares: accepted partial approach

Problem 30006403, rank 1213, alias OWR-14299518-027. Status: **UNRESOLVED, approach 1 of 5**.

For an n by n matrix of rank r with E nonzero entries, this report proves over every field the sparse-basis bound z≥max{0,ceil(n−sqrt(rE))} and a with-replacement oversampling bound z/n≥[(k−r)/(2k−r)]·(1−E/n²)^k for all integers k>r≥1, together with a stronger quadratic inequality. Here z is the largest all-zero square side with independent row and column choices.

For E≤εn² and 0<ε<1/2, these imply z≥ceil(n exp(−6 max{sqrt(εr),εr})). The target square-root exponent holds for εr≤1, but the full arbitrary-real conjecture remains open for unbounded εr. The characteristic-two example is only a limitation of field-independent methods; the same array has real rank 2^d−1. The report also gives exact rank-one and real set-intersection parameters.

## Reading order

- [APPROACH_1.md](APPROACH_1.md): complete substantive authored mathematics, proofs, attribution, invalid reductions and exact remaining gap.
- [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md): full substantive mathematical and source audit.
- [ACCEPTANCE.md](ACCEPTANCE.md): accepted claims, conditions, limitations and exact edition identities.
- [SOURCE_LEDGER.json](SOURCE_LEDGER.json): public source titles, URLs, PDF identities, retrieval/inspection history and verification limits.
- [PROVENANCE.md](PROVENANCE.md), [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): editorial boundary, scoped status and exact inventory.

Singer–Sudan's probabilistic dimension-drop argument is credited as the prior method. HMST's exact target, small-density antecedent and nonnegative/mean-based theorem are distinguished. No novelty or best-known-real-bound claim is made. AI-assisted and unrefereed; the independent audit is not external human peer review or proof-assistant certification. This edition changes no queue entry or historical approach count.
