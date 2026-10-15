# Partial results on list coloring of edge critical graphs

Row 1751, problem 3200, OPG 388. Authored research and mathematical audits dated 12 October 2026 UTC. This is the first accepted substantive round in the present continuation, with two parallel directions considered together. It is a partial result, not a resolution or counterexample to the general conjecture. No novelty claim is made.

## Main result and exact scope

Let G be a finite simple graph of maximum degree Δ, with no proper Δ-edge-coloring but a proper Δ-edge-coloring after deletion of every edge. Give every edge exactly Δ permitted colors. Constant list assignments fail. The unrestricted question asks whether every nonconstant assignment succeeds.

The strongest accepted near-constant result in this edition proves that every nonconstant assignment differing from a common Δ-element set on at most four edges is colorable, with arbitrary exceptional lists and edge positions. Consequently a hypothetical bad nonconstant assignment must differ from every Δ-set appearing as a list on at least five edges. This necessary condition does not establish a counterexample.

The edition also gives complete proofs for star and triangle support, a matching plus one exceptional edge, a strict residual-deficit condition, up to Δ+1 genuinely changed one-color substitutions, and the complete degree-two case. It states an exact Hall criterion only for a fixed exterior-coloring and palette-permutation method. The equality-case obstruction is a failure of that chosen method, not a failure of the conjecture.

The second direction proves a nonconstant-preserving small-palette reduction and a minimum-palette pair-cooccurrence bound. It records a complete arbitrary-palette verification for K4 with one edge subdivided, a case already covered by Kaul–Mudrock Lemma 3. The published-theorem route is explained with an exact graph isomorphism and all hypotheses; it does not depend on the omitted computational witnesses. A complete graph census through seven nonisolated vertices and four-palette scans of six specific graphs provide bounded computational evidence. The larger graphs were tested only with four colors and are not established for arbitrary palettes.

## Complete authored contents

- NEAR_CONSTANT.md: exact setting, Hall criterion, star and clique support, deficit theorem, corrected corollaries, and necessary counterexample conditions
- ADDITIONAL_CASES.md: odd-cycle proof, matching-plus-one theorem, three-exception consequence, and fixed-method boundary
- FOUR_EXCEPTIONS.md: all cases of the four-arbitrary-exception proof and Δ+1 substitutions
- STATEMENT_CLARIFICATIONS.md: both integrated nonconstancy corrections and the source-convention qualification
- FINITE_PALETTE.md: complete finite-palette proofs, seven explicit deletion vectors, normalization and counts, known Lemma 3 route, and bounded search scope
- SOURCES.md: named primary sources, publication identities, inspection scope, related results, and literature-search limits
- AUDIT_NEAR_CONSTANT.md and NEAR_CONSTANT_ACCEPTANCE.json: complete structural audit, explicit small mathematical negative controls, finite checking coverage, and acceptance conditions
- AUDIT_FINITE_PALETTE.md and FINITE_PALETTE_ACCEPTANCE.json: complete finite-palette audit, full reported witness checking, independent bounded reruns, negative controls, and acceptance limits
- MANIFEST.json: closed identities for these actual distributed authored files, excluding the manifest itself

## What can be verified from this edition

All authored theorem proofs and the seven explicitly displayed criticality vectors are retained. The normalization recurrence and the exact Lemma 3 graph map can be checked from the prose. The named published lemma is an external mathematical input; its proof is not reproduced.

The audit prose reports complete checking of 19,791,009 positive seven-edge coloring witnesses, one constant obstruction, all 59 deletion witnesses across six graphs, and every branch of the Petersen obstruction tree. It also reports independent reruns of the bounded census and all 5,246,976 four-palette cases. These are reported computer-assisted checks with explicit finite coverage. The other 52 deletion witnesses, large coloring-witness collection, and Petersen decision tree are not distributed. They cannot be reconstructed from this prose alone. No executable programs, raw diagnostic collections, copied third-party source documents, excluded-file identities, or private coordination material are included.

The structural theorems have full symbolic proofs, so their acceptance does not rely on finite diagnostics. The seven-edge arbitrary-palette result also follows from the explained known theorem. The larger-graph computed claims require independent reimplementation and new witness generation for computational reproduction.

## Remaining problem and accounting

Arbitrary finite simple critical graphs of maximum degree at least three and arbitrary nonconstant exact Δ-list assignments remain unresolved by this work. The source check is bounded and does not certify present-day openness or historical priority. An earlier screen exists, so the total lifetime attempt count is unknown; the present continuation confirms one newly accepted substantive round, not one round per worker. No later research round is included in this edition.
