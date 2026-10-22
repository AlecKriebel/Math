# Final five-turn result: Melnikov's valency-variety problem

**Original question: unsolved5/5. Full independent review of the scoped partials is pending.**

For a finite simple graph of order n>=2, let w be its number of distinct vertex degrees, d=n-w, and k=chi(G). The live OPG inequality is exactly equivalent to

    n-1 <= (2k-1)d.

The five substantive turns do not prove this universally or give a counterexample. They establish the following bounded results, with explicit proofs and exact finite diagnostics:

- TURN_1: universal weaker bound n-1<=(2^k-1)d, exact rounding, and the full bipartite subcase
- TURN_2: a quadratic necessary condition from independent-set cut balance, excluding formal degree allocations that individual color capacities permit
- TURN_3: the stronger isolate-free-core inequality for all split graphs, and preservation of that property under disjoint union and complete join; this also covers the class generated from bipartite/split graphs by those operations
- TURN_4: a maximum-degree-neighborhood coloring criterion, the entire triangle-free class regardless of chromatic number, and the full deficit-one case through an explicitly credited classical antiregular recursion
- TURN_5: the complete three-color deficit-two slice by forced adjacency, including isolates; combined with earlier theorems this proves the exact source inequality for every graph of order at most15

The order15 consequence is a deduction from the written theorems. The full labeled-graph diagnostic enumeration only reaches order6. The finite receipt totals count repeated algebraic and structural assertions and must not be presented as a search or proof for every graph of order15.

## Remaining gap

The general coefficient2k-1 remains unproved. The deductions leave, for example, the parameter possibility n=16, k=4, d=2, and three-color graphs with d>=3 and n>=5d+2, outside the established structural classes. These are not constructed counterexamples. No sixth author proof-search turn is included.

## Source, credit and artifacts

SOURCE_GATE.md records the full live OPG statement and visual formula check. Its exact ceiling, floor and strict comparison are retained. Historical Vizing/Jensen–Toft formula-image access limits are disclosed; no unverified typographical correction was imposed. SOURCE_ADDITION_TURN_4.json records the antiregular primary paper and classical credit. There is no comprehensive novelty or priority claim.

The first two-turn README, count record and CHECKPOINT_MANIFEST are preserved as historical artifacts. TURN_COUNTS_v5.json and this result give the final state. FINAL_AUTHOR_MANIFEST.json binds the complete portable author packet. Full PDFs, page images, imported records and local administrative caches are reading/working inputs and are excluded.

All five exact author check scripts have reproducible receipts. The analytic arguments still require a full independent adversarial audit. Final publication and a queue change must wait for that review and approval; the current WIP backup is not a result PR.
