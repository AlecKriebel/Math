# Mathematical audit and acceptance scope: geodesic cycles

Record 3169 / OPG-500. Audit date: 2026-10-11 UTC.

This is an AI-assisted, unrefereed internal AI audit of a prior public candidate. It is not human peer review or formal proof-assistant certification. The source construction and the C09/C10 arguments are credited to vibemathing at commit a41fe59b4535851ea55f6e868e938b9aaf81e924. No new discovery, novelty or priority is claimed. This prose edition is not a computational reproduction package.

PROOF.md and this report are complementary parts of one completed audit, not independent evidence from two reviewers. PROOF.md preserves original §§2–7 in full; this report preserves the verdict, source review, finite-check coverage and stopping limits. References to §§2–7 refer to PROOF.md. Historical program/receipt descriptions below report the completed audit; no mathematical program was rerun for this prose edition.

## Verdict and exact accepted scope

**Accepted as a complete written counterexample proof, with independent exact finite checks.** The eight-vertex graph specified in PROOF.md §2 is finite, simple and 3-connected, and **for every assignment of strictly positive real lengths to all its edges, at least one vertex-pair-geodesic cycle is nonperipheral**. Thus the universally quantified affirmative answer posed in OPG-500 is false.

The primary accepted argument is the all-ties tight-subgraph argument in the inspected C10 candidate. This audit reconstructs its mathematical bridges in full, independently checks the finite graph and necessary rank obstruction, and historically supplied a complete exact rational witness extractor with independently checked distance certificates. The C09 perturbation argument is also mathematically sound under its stated uniqueness reduction; a freshly derived exhaustive Boolean certificate supports its finite part.

No mathematical correction to either universal argument is needed. There is one **expository clarification**: the all-points definition is not strictly stronger on a finite graph with its usual positive-length metric realization. It is equivalent to the vertex-pair definition; a proof is given in PROOF.md §7. This does not change the accepted theorem.

This is local mathematical acceptance, not a Lean/kernel-checked proof, external peer review, a novelty claim, an admission in the source author's system, or a claim that its repository has changed status. No author scripts, author certificates, Lean source, or proof-assistant project were executed. Copied third-party source texts, programs, raw certificate arrays and private coordination material are outside this public prose edition. Preparing it does not alter the source author's historical status.

## 1. Source statement and provenance

The original Open Problem Garden page asks whether each finite 3-connected graph admits a positive real edge-length assignment for which every length-geodesic cycle is peripheral. Its definition tests pairs of **vertices** and excludes a path strictly shorter than both cycle arcs. Consequently equal-length shortest alternatives are permitted.

The local PDF is Agelos Georgakopoulos and Philipp Sprüssel, *Geodetic topological cycles in locally finite graphs*, arXiv:0911.3999v1, dated 20 November 2009. Its §3.1, physical page 5, explicitly uses the finite vertex-pair convention and proves Theorem 3.1, that weighted geodetic cycles generate the finite cycle space. Problem 3, physical page 15, poses the peripheral-cycle question. The length functions in §2.2 take values in the positive reals. Peripheral means induced and nonseparating; here nonseparating means that deleting the cycle's vertices leaves a connected or empty graph. In this example every induced cycle has three vertices and leaves five vertices, so no empty-complement convention affects the result.

Public source identities:

- https://www.openproblemgarden.org/op/geodesic_cycles_and_tuttes_theorem
- https://arxiv.org/abs/0911.3999
- https://arxiv.org/pdf/0911.3999
- https://github.com/vibemathing/problem-opg-500-geodesic-cycles/tree/a41fe59b4535851ea55f6e868e938b9aaf81e924
- C09: `research/artifacts/candidates/opg500-a01-c09/root-counterexample.md`
- C10: `research/artifacts/candidates/opg500-a01-c10/tight-rank.md`
- C11: `research/artifacts/candidates/opg500-a01-c11/faithfulness.md`
- C12: `research/artifacts/candidates/opg500-a01-c12/finite-descent.md`

During the completed audit, all five cited repository prose files matched their recorded byte counts, SHA-256 hashes, Git blob IDs in the complete recorded tree at the pinned commit, and recorded retrieval bodies. This authenticates local integrity against frozen source records, not a new live retrieval. Their public identities are recorded in SOURCES.json; source bodies are excluded.

The paper PDF is 254,595 bytes, SHA-256 `b1090df57c16ff9c00b4a378a15251940058cd19f64af9fa4ea6c618443b29c9`. This audit inspected text on physical pages 1, 4, 5, 6 and 15, the metric-definition subsection on page 3, and visually inspected pages 5 and 15. In particular the entire finite Theorem 3.1 proof was read, not just its statement. The remaining infinite-graph proofs were not audited. All of C09, C10, C11 and C12's supplied prose was read. C11/C12's actual Lean files and external executable certificates were not supplied as audit inputs and are not claimed to have been checked. SOURCES.json records the public inspection bounds and source identities. Its historical intake status is distinguished explicitly from this completed written audit.

The frozen candidate documents explicitly say `candidate_only` and `best_verified_result: none`. A website's “proved” presentation is not used as evidence. This audit gives its own local verdict and leaves those historical status statements unchanged.

## 8. Exact checks and adversarial coverage

The completed audit used a newly authored checker relying only on Python's standard library, exact integers and exact fractions. It neither imported nor executed source-author code. Correctness checks used explicit exceptions, so Python optimization did not remove them. The program is not distributed in this prose edition and was not rerun during editorial preparation.

The completed audit's omitted local certificates contained the following coverage; these descriptions and aggregate counts are verification metadata, not distribution of the arrays:

- Every simple cycle of H with its edge mask, vertex list, chords, deletion components and peripheral classification; all 37 small vertex deletions.
- All 5,913 admissible triangle-free core/dominating-link patterns, with actual triangle-span ranks and positive rank gaps. Enumeration by core/link products is checked against an independent complete 18-edge-mask scan. The gap multiplicities for gaps 1 through 5 are 768, 2,752, 2,019, 366 and 8. All 64 core masks are covered; 23 contain a core triangle and 41 do not.
- All 4,770 cycle/external-simple-path splits, including the two child cycles, exact XOR identity, subgraph inheritance and coefficient identities proving strict weighted decrease whenever the external path is shorter than both arcs. Completeness follows by enumerating every cycle, each pair of its vertices, and every simple path avoiding its other vertices and its edges. These are conditional symbolic identities, not samples of the real-weight inequalities.
- The freshly derived 76-clause Boolean abstraction, its full 262,144-assignment UNSAT check, and all 832 reduced conflict rows.
- 64 exact positive rational assignments: four symmetric cases, powers of two in both orders, ascending lengths, 32 deterministic integer vectors, 24 deterministic rational vectors, and a positive scaling. Branch counts are A:24, B:27, C:13. Each includes all-pairs distances, attaining simple paths, every pair comparison for the returned bad cycle, its nonperipheral evidence, and the complete geodesic/bad-cycle lists.

Distances are first calculated with exact Floyd–Warshall, checked against complete minimization over all 2,628 simple paths between unordered endpoint pairs, and separately certified by anchored edge-Lipschitz potentials plus attaining paths. The latter supplies a lower bound for every possible path by telescoping, and a matching upper bound from the attaining path. No floating-point infeasibility, sampling inference or external solver claim is involved.

Mathematical negative controls reject zero and negative lengths, a forged distance, a peripheral alleged witness, a nongeodesic core-triangle witness in the tie example, and a nonsimple attaining path. Countermodels explicitly demonstrate the need for C09 uniqueness and the insufficiency of excluding core triangles alone.

Independent integrity controls reject changed input bytes of the same size, missing members, source symlinks, a changed handoff manifest, an omitted graph cycle, a forged peripheral flag, a zeroed rank gap, an omitted tight pattern, a corrupted or omitted symbolic split, a changed Boolean clause sign, and a changed rational domain. Sealed-packet controls also reject missing/modified/extra files, symlinks, an extra empty directory, changed inventory and a changed external seal. The completed audit ran normal, `-O` and `-OO` modes. VERIFICATION.json records authenticated historical results and exact receipt identities. The public edition excludes executable code and raw certificate/receipt contents; it does not enable replay of the finite computations. The full universal written proof is included in PROOF.md.

## 9. Stopping condition

The completed local audit accepted the theorem after source authentication, the full written proof, exact certificates, all three optimization modes, negative controls and closed-inventory seal checks passed. That establishes the stated counterexample at the written-mathematics level and finite executable support at the declared scope. No further sampling is needed to justify the universal theorem. Broader literature priority, external review, source-repository admissions and formalization remain outside this acceptance. This public edition does not imply those outcomes.
