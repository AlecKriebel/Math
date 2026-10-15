# PR108 independent reproduction and adversarial audit

**Verdict: the mathematical reduction passes; the historical assertion-based verification requires hardening.** The root's separately repaired effective snapshot applies that hardening, preserves the mathematical argument and all census counts, and passes the inspected control suite. No mathematical counterexample or substantive inconsistency was found.

This audit concerns PR108, problem 30003996 / OWR-16633-013, original head `3526d46bf143b08e5055ffa7728c6278e9f958ea`. Its historical queue status is `claimed_solved`, with original allowance **2/5**, corroborated by the queue projection and prose research log. No original `status.json` or `turns.jsonl` exists in the archived attempt. This audit uses **zero additional central-proof search turns** and performs **zero priority search**. It does not establish historical novelty or human peer review.

## Pinned evidence and independence

The original source record and manifest were read before the complete Kaibel contribution on printed pp.3014-3015 of the original Oberwolfach PDF. Both PDF pages 46-47 were extracted, rendered and visually read. The PDF is 590,481 bytes, SHA-256 `a90207e0cadc310ab5a52a228c4b25a16f5e5f617542f006e9909cf90d4c72d2`, matching the original manifest. The source's Problem 1 specifies one undirected spanning tree, both arc directions and a cost vector for every root. Problem 2 has a different fixed-root path objective. The contribution's two motivations do not alter that distinction.

Only then was `original_attempt/PROOF.md` read. An independent generic evaluator and actual-tree census were constructed and frozen **before reading either historical checker, old independent review, or another audit family**. `MODEL_FREEZE.json` and `INDEPENDENCE_CHECKPOINT.json` record the order and hashes. The independent model uses no author or reviewer code. The later exact author-suite cross-census is explicitly labeled supplemental rather than early independent evidence.

Original proof SHA-256: `1a6c267c6240b66c1d804397f4bbbe246f5b6147c3930e1a68396e60b618d615`.
Original author checker: `02182aac6b9c300105b48d6049384954c26ef57cb11dae66a3908b6926dbbe7c`.
Original old-review checker: `e8f3a9130ad78356b40c45a59879386dc4130e03b69dc02d4d448848ca5c72b0`.
Complete byte counts and hashes appear in `initial_input_manifest.json` and `original_input_manifest.json`. Archived originals were not modified.

## Exact claim, assumptions and universal argument

The verified claim is strong NP-completeness of the decision problem on connected simple undirected graphs with explicitly encoded nonnegative integer costs for both directed versions of every edge at every root. A witness is one spanning tree T, with objective

\[
F(T)=\sum_{r\in V}\sum_{(u,v)\in T^r}c_r(u,v).
\]

Costs are evaluated on every oriented edge of each root-induced arborescence of that same T. Individual roots do not choose different undirected trees. The source's arbitrary real vectors contain this finitely encoded subclass. Membership in NP follows from a spanning-tree check, N traversals and polynomial-length integer addition. Reversing every cost entry transfers outward to inward conventions.

The reduction imports the standard NP-completeness of satisfiability with at most three literals per clause. Repeated literals and tautological clauses may be removed. Empty clauses and empty remaining formulas use fixed no/yes instances. Sparse variable names must be relabeled by distinct actual symbols; the largest numeric label is not the variable count. These are preprocessing requirements, not empirical assumptions.

For a nondegenerate formula with n variables and m clauses, the graph contains hubs t,f, the edge tf, both hub incidences of every variable, and clause-variable incidences. Set B=n+1 and K=Bm+n. The t-root's symmetric costs are 0 on tf, 1 on variable-hub edges and B on clause-variable edges. At a clause root, the only nonzero costs are variable-to-hub arcs representing false literals; all other roots/entries are zero.

For **any** spanning tree, let p,q,h count variable-hub edges, clause-variable edges and presence of tf. Every clause has positive degree, so q>=m. Since p+q+h=n+m+1,

\[
c_t(T^t)=p+Bq=K+(1-h)+n(q-m).
\]

Nonnegative costs prohibit compensation for either excess term. Thus F(T)<=K forces h=1 and q=m. All clause vertices are leaves. After removing them, the remaining hub-variable tree contains tf, and each variable has exactly one hub edge: neither zero attachments nor the triangle from two attachments is possible.

At clause root q_j, its selected variable's hub edge points from the variable to its chosen hub. Every other variable's hub edge points from its hub toward the variable, including variables supporting other clause leaves. Consequently only the selected literal can incur that clause vector's penalty, and every structured tree satisfies

\[
F(T)=K+\#\{\text{false selected clause literals}\}.
\]

A satisfying assignment and true selected literals yield a tree of cost K. Any tree of cost at most K is structured and has all selected literals true. This proves both directions for all sizes. No equivalent unsupported hardness claim is substituted for the central reduction.

There are N=n+m+2 vertices, at most 1+2n+3m edges, and 2N|E| explicit cost entries. Costs are 0,1,n+1 and K is polynomially bounded, so unary numerical encoding remains polynomial: the conclusion is strong NP-hardness and, with membership, strong NP-completeness. Adding 1 to every cost entry adds exactly N(N-1) to every objective, including the formerly zero root vectors. This proves the strictly positive variant. No planar, bounded-degree, fixed-root-count or approximation claim is inferred.

## Independent checkable computation

The independent all-root traversal is checked against an edge-cut formula. Delete a tree edge {u,v} and let U contain u. A root in U selects u->v, while every root outside U selects v->u. Therefore

\[
F(T)=\sum_{\{u,v\}\in T}\left(\sum_{r\in U}c_r(u,v)+\sum_{r\notin U}c_r(v,u)\right).
\]

This identity holds for arbitrary costs. The code enumerates actual N-1 graph-edge subsets and checks connectivity, without assuming the hub edge or clause leaves. A separate Prüfer decoder enumerates complete-graph trees and agrees with subset reconstruction for N<=5.

| Independent frozen census | Exact count |
| --- | ---: |
| Input formulas/controls | 579 |
| Satisfiable / unsatisfiable inputs | 542 / 37 |
| Actual spanning-tree/formula cases | 102,764 |
| All-root versus edge-cut equality checks | 102,764 |
| Strict-positive shift checks | 102,764 |
| Dense explicit cost-table round trips | 579 |
| Structured reduction trees | 15,798 |
| Missing tf, clause vertices all leaves | 22,591 |
| tf present, some clause vertices internal | 26,200 |
| Missing tf and some clause vertices internal | 38,172 |
| Fixed two-vertex control trees | 3 |
| Low-cost trees across all inputs | 3,825 |

The three disjoint unstructured categories total **86,963**; every such tree is excluded by the threshold. The classification covers 102,761 nondegenerate-reduction tree cases plus three fixed-control cases, not 102,764 reduction-shape cases.

The **full finite formula families** are normalized nonempty clause multisets, up to clause order, for n=1,2 with 1<=m<=3, and n=3 with 1<=m<=2. These comprise 550 formulas and **94,959** actual tree/formula cases. The additional 29 inputs comprise nine explicit boundary/sparse-ID controls and twenty seeded n=3,m=3 samples. The sampled family is not called exhaustive. Boundary cases include an empty formula, empty clause, tautology, repeated literal, contradictory units, four-clause two-variable unsatisfiability, unused variables and sparse huge IDs.

The generic dense-cost suite evaluates **1,441** actual complete-graph trees: counts 1,3,16,125,1296 for N=2,...,6. Every root/arc entry is nonzero, with up to 70-bit integer costs and sparse vertex labels. Five corrupted in-memory dense-cost controls are detected, and three cycle/disconnection/duplicate-edge candidates are rejected. The same frozen independent scientific results hold in normal and optimized mode; only timestamps and the recorded optimization flag differ.

Supplemental checks independently reconstruct the author's exact 212-input suite: **37,629** trees and **26** distinct graphs, matching its census. They also check a singleton tree, inward reversal on all 16 four-vertex trees with dense signed rational costs, rejection of missing/duplicated cost-table entries, and sparse labels with a 333-bit maximum literal ID. The latter creates six graph vertices, demonstrating that graph size depends on the count of symbols rather than their maximum label.

These are bounded, reproducible finite controls. They support the universal structural and orientation reasoning; they do not constitute a computational proof of NP-hardness or an exhaustive search across all instances.

## Historical replay, byte comparison and adversarial failure

Every historical script was copied byte-for-byte into isolated replay folders. Normal and optimized subprocess runs were journaled with actual command, timestamps, return status and exact stdout/stderr byte hashes.

| Historical replay | Nominal check count | Formulas | Tree/formula cases | Saved receipt |
| --- | ---: | ---: | ---: | --- |
| Author | 78,056 | 212 | 37,629 | 344 bytes, SHA `8d76675f24af1bbbb2399424707ef314fb5e5ca1306fc12b4410ef6716a530a1` |
| Old independent review | 600,122 | 550 | 94,959 | 1,176 bytes, SHA `5ffddb5472998529801bdd33edcb4f3fe4151daf05da29dc110622e1319cc0d9` |

Both modes reproduce both saved receipts **byte-identically**. The independently frozen shared full suite also reproduces the review's 32 unsatisfiable formulas, 80,285 noncanonical cases, 56,157 cases without tf, 59,320 with extra clause edges and 14,674 canonical cases. The last two unstructured counts overlap; they must not be added as disjoint classes.

Byte-identical optimized receipts are **not valid check evidence**. The original author's six `assert` predicates and the reviewer's checksum `assert` and `ck` assertion disappear under `python -O`, while counters and unconditional `all_pass` remain. The actual control matrix establishes this failure:

| Control | Original normal | Original -O | Suggested explicit guards, normal/-O |
| --- | --- | --- | --- |
| Author's final SAT equivalence predicate deliberately false | rejects | accepts | rejects / rejects |
| Reviewer's `ck(False, ...)` | rejects | accepts | rejects / rejects |
| Either checker: t-root hub-edge costs corrupted in memory | rejects | accepts | rejects / rejects |
| Reviewer's proof-copy bytes changed | rejects | accepts; emits byte-identical stale success receipt | rejects / rejects |
| Cycle/disconnected graph enumeration controls | correct | correct | correct / correct |

`guard_adversary.py` isolates exact original definitions by omitting only top-level suite execution/receipt writes, then identifies the actual final predicate or explicitly corrupts the in-memory cost data. These probes are labeled transformed in their metadata rather than called unchanged complete-script replays. The proof-byte probe runs the complete copied reviewer script. `controls_*.json` and all corresponding actual subprocess journals preserve the observations. The frozen independent verifier's explicit known-false guard exits nonzero in both modes.

## Separate minimal repairs and inspected effective snapshot

`suggested_guard_repairs/author.diff` and `suggested_guard_repairs/old_review.diff` replace only disappearing assertions with explicit `require` calls and add receipt provenance fields `guard_mode` and `verifier_sha256`. They change no graph, cost, formula suite or proof. Their actual regenerated normal/-O receipts retain every original scientific field. Their receipt bytes intentionally change: author 498 bytes and old review 1,330 bytes. The exact count/byte comparison records which new fields account for this change. Fresh subprocess journals also differ in paths, commands, timestamps and environment; they are not presented as historical byte-identical journals.

The root adopted those guards into `repaired_diagnostics_v1`, additionally made the fixed yes/no preprocessing and dense relabeling explicit, and rebound the reviewer to the exact effective proof. On request, I read and checked that entire effective proof and both effective scripts before sealing this report. No substantive inconsistency was found. The effective proof and its reviewer copy are byte-identical; the reviewer's EXPECTED hash is correct; neither script retains an AST `assert` node.

Effective snapshot:

- Proof: 8,061 bytes, SHA `2818eab189445649ae1ba98d55e3da3e5fab918de88f1779de86962ba99a3393`.
- Author checker: 3,510 bytes, SHA `46173f3fa54eae9da12a0525494b7d73d1544980cefea9040f8341340cf7385e`.
- Reviewer checker: 6,519 bytes, SHA `a298835e88bf4a6528d3ff3d39f6036a5edfb4e6dc525cae13f3f9f631357a7c`.

The root's actual `root_effective_reproductions_20261006/REPRODUCTION_RECEIPT.json` records **12** subprocess runs: four valid normal/-O replays with 78,056 or 600,122 effective guards, and eight rejected false/corrupt controls. `effective_candidate_inspection.json` records the inspected bytes and receipt. The effective hashes differ from the original archive because of explicitly recorded preprocessing prose, guards and proof binding; no mathematical failure or new research attempt is inferred from those byte differences.

## Disposition and artifact custody

The strongest verified result is the all-size strong NP-completeness reduction for the source's exact aggregate all-root objective, with the guards hardened in the inspected effective snapshot. The mathematical gap is closed under the stated finite encoding and imported 3-CNF satisfiability theorem. Historical priority remains unestablished and was not searched by this audit; the work remains unrefereed.

All audit writes occurred in this assigned folder. No Git, index, remote service, publication, editor or outreach action was taken. Original source PDFs were only read. All third-party PDF extracts and rendered pages are under `private/`, ignored and excluded from public manifests. Private custody hashes appear only in `PRIVATE_EXCLUSIONS.json`. Output manifests exclude themselves as specified to avoid circular hashes, and `SHA256SUMS` authenticates the output manifest. All important findings, timestamps and best-guess completion estimates are in `RESEARCH_LOG.md`.
